# This code imports data from a local CSV file and applies Logistic Regression algorithm on a dataframe
# in order to predict the fate of Titanic passengers. Since the data is already given and filled, this code
# and data can be used to test the accuracy of the algorithm (for this dataset)

# Making necessary package imports


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from IPython.display import display


# We begin by creating a Pandas Dataframe from the CSV file using the read_csv function

ttnc = pd.read_csv("titanic_train.csv")

# We check the structure and info on the dataframe using head() and info()
# We also check for missing values using isnull() and a Seaborn heatmap so we see where the missing values are

display(ttnc.head())
ttnc.info()
sns.heatmap(ttnc.isnull())
plt.show()

# Upon inspection, we observe that PassengerID is just a sequence, Name and Ticket are random strings
# and Fare is probably a consequence of Pclass, so those columns can be dropped as they do not
# affect our Target class, which is Survived (Target class is what we're trying to make our computer predict
# From the heatmap, we also observe that Cabin has many missing values, so we should drop that as well

ttnc.drop(['Name', 'PassengerId', 'Ticket', 'Fare', 'Cabin'], axis=1, inplace=True)

# In order to deal with missing values in the Age column, we will fill them with numbers based on
# a correlation between Age and Pclass. This correlation can be seen using a seaborn boxplot


sns.boxplot(x='Pclass', y='Age', data=ttnc)
plt.show()

# Making a visual approximation, we notice that the distribution of ages in Pclass 1 is centered around 37 years
# For 2, it's around 29 years, while for 3 it is around 24 years. We can use these assumed values and replace
# our missing data with them


def impute_age(cols):
    age = cols[0]
    pclass = cols[1]
    if pd.isnull(age):
        if pclass == 1:
            return 37
        elif pclass == 2:
            return 29
        else:
            return 24
    else:
        return age


ttnc['Age'] = ttnc[['Age', 'Pclass']].apply(impute_age, axis=1)

# Since our dataframe has 2 columns that have non-numerical values, we must first convert them to integers
# using get_dummies. This will give us a new dataframe that represents Sex as 0 or 1 and the categories
# under Embarked as 0 or 1.

new_df = pd.concat([ttnc.drop(['Sex', 'Embarked'], axis=1),
                    pd.get_dummies(ttnc['Sex'], drop_first=True),
                    pd.get_dummies(ttnc['Embarked'], drop_first=True)], axis=1)

# We then split this new dataframe into our training and testing data using train_test_split

X_train, X_test, y_train, y_test = train_test_split(new_df.drop('Survived', axis=1), new_df['Survived'], test_size=0.3)

# The class for the Logistic Regression model that we are going to use in this analysis has already been imported.
# An object of LogisticRegression class is created to fit our data into it.
# We then use the model to make predictions on the testing data and measure its accuracy against the data
# that we already have

model = LogisticRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print(confusion_matrix(y_test, predictions))

# In conclusion, the confusion matrix shows us that roughly 40-50 predictions out of 268 test rows are incorrect
# which means this model is roughly 80% accurate for this data set

