import random


def display_board(board):
    print("\n")
    for i in range(1, len(board)):
        # Prints each element of the board in a single line with spaces.
        # Prints a newline character after every third index.
        if i % 3 == 0:
            print(board[i], "\n")
        else:
            print(board[i], " ", end=' ')


def place_marker(board, marker, pos):
    board[pos] = marker


def win_check(board, mark):
    # check diagonal win condition
    d_win = [[1, 5, 9], [3, 5, 7]]
    # check horizontal win condition
    h_win = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # check vertical win condition
    v_win = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    for i in d_win:
        if board[i[0]] == board[i[1]] == board[i[2]] == mark:
            return True
    for i in h_win:
        if board[i[0]] == board[i[1]] == board[i[2]] == mark:
            return True
    for i in v_win:
        if board[i[0]] == board[i[1]] == board[i[2]] == mark:
            return True
    return False


def choose_first():
    # 50/50 chance of X or O going first
    chance = random.randint(0, 100)
    if chance < 50:
        print("O goes first")
        return "O"
    elif chance >= 50:
        print("X goes first")
        return "X"


def space_check(board, pos):
    return board[pos] == "-"


def full_board_check(board):
    return "-" not in board


def player_choice(board):
    while True:
        try:
            pos = int(input("Where do you want to place your marker (1-9) "))
        except ValueError:
            # Catches exceptions when entered string cannot convert to int due to incompatible type.
            print("Invalid type. Please enter an integer number")
            continue
        if pos not in range(1, 10):
            # Check whether given input is in valid range, continue loop if invalid.
            print("Invalid position")
            continue
        if space_check(board, pos):
            # Check availability and return position if available.
            return pos
        else:
            print("Position unavailable, please try again")


def replay():
    re = input("Play again? (Y = Yes, Anything else = No) ")
    if re.lower() == "y" or re.lower() == "yes":
        return True
    else:
        return False


print("Welcome to Tic Tac Toe\n\n")

while True:
    # Generate an empty board every time a new game starts.
    # Empty positions are denoted by a dash/hyphen. space_check and full_board_check test for those characters.
    game_board = ['#', '-', '-', '-', '-', '-', '-', '-', '-', '-']
    display_board(game_board)
    turnstring = "OX"*5
    # A string of 10 alternating Xs and Os is used here to cycle between turns.
    # There can be maximum of 9 turns in any given game before the board fills up.
    # Depending on output of choose_first, turnstring is sliced to a string of 9 characters with X or O at index 0.
    if choose_first() == "O":
        turnstring = turnstring[:-1]
        # String of 9 letters starting with O.
    else:
        turnstring = turnstring[1:]
        # String of 9 letters starting with X.
    for turn in turnstring:
        # Iterate through the sliced turnstring in order to switch between X and O for maximum of 9 turns.
        print("\n\nPlayer", turn, ":")
        position = player_choice(game_board)
        place_marker(game_board, turn, position)
        print("\n"*100)
        # I wrote this on PyCharm so did not use IPython.display to clear the output
        display_board(game_board)
        if win_check(game_board, turn):
            # At the end of the turn, check winning conditions.
            print("\n", turn, "wins the game")
            break
        if full_board_check(game_board):
            # If board fills up and nobody wins, a draw is declared.
            print("\nDraw!")
            break
    if not replay():
        break
