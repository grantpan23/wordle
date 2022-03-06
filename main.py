import re

colour_dictionary = {
    'GREEN': '🟩',
    'YELLOW': '🟨',
    'RED': '🟥'
}


def guess():
    return input("Guess a word: ")


# Check if guessed letter matches answer letter
def is_match(guess_letter, actual_letter):
    return guess_letter == actual_letter


# A valid guess is strictly a String with length 5
def is_valid_guess(g):
    return len(g) == 5 and re.match("^[a-z]*$", g)


class Letter:
    # A Letter is akin to one of the "blocks" in Wordle; each block has a letter and colour
    # The 'colour' attribute is used to look up the dictionary to populate the answer matrix
    # The 'taken' attribute detects when a guess letter is "linked" to an answer letter -- more on this later
    def __init__(self, letter):
        self.letter = letter
        self.taken = False
        self.colour = ""

    def get_letter(self):
        return self.letter

    def set_colour(self, c):
        self.colour = c

    def get_colour(self):
        return self.colour

    def become_taken(self):
        self.taken = True

    def is_taken(self):
        return self.taken


class Game:
    def __init__(self, ans):
        self.answer_str = ans
        self.answer_matrix = []
        self.guess_number = 0
        self.last_guess = ""
        self.win = False

    # A Game is won if the last guess is equivalent to the answer
    def is_won(self):
        self.win = self.last_guess == self.answer_str
        return self.win

    # A Game ends after 6 rounds or if the player wins
    def is_ongoing(self):
        return self.guess_number <= 5 and not self.is_won()

    def add_answer_row(self):
        self.answer_matrix.append([""] * 5)

    def print_answer_matrix(self):
        for row in self.answer_matrix:
            print("".join(row))

    # Guess number references the row of the matrix, while i references the column
    # Look up the dictionary using the colour stored in each Letter to populate the matrix
    def fill_answer_matrix(self, g_letters):
        for i in range(5):
            self.answer_matrix[self.guess_number][i] = colour_dictionary[g_letters[i].get_colour()]

    def play_round(self):
        # Restart the round if guess isn't valid
        guess_str = guess()
        if not is_valid_guess(guess_str):
            print("Please enter a valid word.")
            self.play_round()
        else:
            # When scanning for letter matches, there is a certain priority sequence:
            # First, the two words and scanned for exact matches (same letter, same position)
            # Then, they are scanned for non-exact letter matches (same letter, different position)
            # However, non-exact letters must not be matched to letters with an existing match
            # For example, for the answer "dread", the guess "greed" should return 🟥🟩🟩🟥🟩
            # If there are more non-exact matches than non-taken matches, the first non-exact matches take priority
            # For the same answer "dread", the guess "racer" should return 🟨🟨🟥🟨🟥
            # The first 'r' becomes matched with the 'r' in "dread", and is unavailable to match with the second 'r'

            # Increment guess number, store last guess, and add an answer row to the answer matrix
            self.guess_number += 1
            self.last_guess = guess_str
            self.add_answer_row()

            # Create two arrays of Letters using the guess and answer Strings
            guess_letters = [Letter(guess_str[i]) for i in range(5)]
            answer_letters = [Letter(self.answer_str[i]) for i in range(5)]

            # Scan for letters that are exact matches
            for i in range(5):
                # Isolate two letters in the same position in each String
                guess_let = guess_letters[i]
                ans_let = answer_letters[i]

                # "Taken" indicates that a letter has been matched and is unavailable for further matches
                # If letters match, set both to taken and set colour of guess letter
                if is_match(guess_let.get_letter(), ans_let.get_letter()):
                    guess_let.become_taken()
                    ans_let.become_taken()
                    guess_let.set_colour('GREEN')

            # Scan for matches between non-taken letters, and set taken and colour
            for g in guess_letters:
                if not g.is_taken():
                    for a in answer_letters:
                        if not a.is_taken() and is_match(g.get_letter(), a.get_letter()):
                            g.become_taken()
                            a.become_taken()
                            g.set_colour('YELLOW')

            # Set all remaining unmatched guess letters to red
            for g in guess_letters:
                if not g.is_taken():
                    g.set_colour('RED')

            # Populate answer matrix
            self.fill_answer_matrix(guess_letters)

    # Play rounds while valid and print newly updated answer matrix at the end of each round
    def play_game(self):
        while self.is_ongoing():
            self.play_round()
            self.print_answer_matrix()

        if self.is_won():
            print("You won!")
        else:
            print("You lost")


if __name__ == '__main__':
    game = Game('frank')
    game.play_game()
