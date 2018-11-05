import random
import string
"""This game plays hangman with the user."""
class Hangman:

    def __init__(self):
        self.hidden_word = self.find_word()
        self.blank_string = "-" * len(self.hidden_word)
        self.lives = 6

        #For debugging only ;)
        print (self.hidden_word)
        print (self.blank_string)

    def process_guess(self, guess):
        tempblank=list(self.blank_string)
        if guess in self.hidden_word:
            i=self.hidden_word.index(guess)
            tempblank[i]=guess
            self.blank_string=''.join(tempblank)
        else:
            self.lives=self.lives-1

    def find_word(self):
        #This method is complete
        dictionary = open('/usr/share/dict/words','r')
        words = list(dictionary)
        return random.choice(words).lower().strip()

    def draw_hangman(self):
        if self.lives == 6:
            print ("=========\n ||     |\n ||\n ||\n ||\n ||\n/  \\")
        elif self.lives == 5:
            print ("=========\n ||     |\n ||     O\n ||\n ||\n ||\n/  \\")
        elif self.lives == 4:
            print ("=========\n ||     |\n ||     O\n ||     |\n ||\n ||\n/  \\")
        elif self.lives == 3:
            print ("=========\n ||     |\n ||    \O\n ||     |\n ||\n ||\n/  \\")
        elif self.lives == 2:
            print ("=========\n ||     |\n ||    \O/\n ||     |\n ||\n ||\n/  \\")
        elif self.lives == 1:
            print ("=========\n ||     |\n ||    \O/\n ||     |\n ||    /\n ||\n/  \\")
        elif self.lives == 0:
            print ("=========\n ||     |\n ||     O \n ||    /|\\\n ||    / \\\n ||\n/  \\")

    def won_game(self):
        if self.hidden_word==self.blank_string:
            return True
        else:
            return False

    def play(self):
        while True:
            self.draw_hangman()
            print(self.blank_string)
            #human turn
            guess=input('enter your guess: ')
            self.process_guess(guess)
            if self.won_game():
                print('yooouuuu winnn, the word is:', self.hidden_word)
                break
            if self.lives==0:
                self.draw_hangman()
                print('yooouuuu looose, the word is:', self.hidden_word)
                break

if __name__ == "__main__":
    game = Hangman()
    game.play()
