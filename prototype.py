import re


def guess():
    return input("Guess a word: ")


def add_answer_row(matrix):
    matrix.append([""] * 5)


def play_round(game):
    guess_str = guess()
    if not (len(guess_str) == 5 and re.match("^[a-z]*$", guess_str)):
        print("Please enter a valid word.")
        play_round(game)
    else:
        add_answer_row(game.answer_matrix)
        for i in range(5):
            if guess_str[i] == game.answer_str[i]:
                game.answer_matrix[game.guess_number][i] = "🟩"
            elif guess_str[i] in game.answer_str:
                game.answer_matrix[game.guess_number][i] = "🟨"
            else:
                game.answer_matrix[game.guess_number][i] = "🟥"
        game.guess_number += 1
        game.last_guess = guess_str


def play_game(game):
    while game.guess_number <= 5 and not game.win:
        play_round(game)
        game.win = game.last_guess == game.answer_str
        print_answer_matrix(game.answer_matrix)

    if game.win:
        print("You won!")
    else:
        print("You lost")


def print_answer_matrix(matrix):
    for row in matrix:
        print("".join(row))


class Game:
    def __init__(self, answer_str):
        self.answer_str = answer_str

    last_guess = ""

    answer_matrix = []

    guess_number = 0

    win = False
