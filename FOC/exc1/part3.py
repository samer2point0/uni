"""
This module represents some classes for a simple word game.

There are a number of incomplete methods in the which you must implement to make fully functional.

About the game board!
The board's tiles are indexed from 1 to N, and the first square (1,1) is in the top left.
A tile may be replaced by another tile, hence only one tile may occupy a space at any one time.
"""

class LetterTile:
    """ This class is complete. You do not have to do anything to complete this class """
    def __init__(self, letter):
        self.letter = letter.lower()


    def get_letter(self):
        """ Returns the letter associatedd with this tile. """
        return self.letter

    def get_score(self):
        """ Returns the score asscoiated with the letter tile """
        return {
           'a' :  1,
           'b' :  2,
           'c' :  2,
           'd' :  3,
           'e' :  1,
           'f' :  3,
           'g' :  2,
           'h' :  3,
           'i' :  1,
           'j' :  3,
           'k' :  2,
           'l' :  3,
           'm' :  5,
           'n' :  3,
           'o' :  1,
           'p' :  2,
           'q' :  2,
           'r' :  3,
           's' :  1,
           't' :  1,
           'u' :  1,
           'v' :  3,
           'w' :  3,
           'x' :  5,
           'y' :  3,
           'z' :  5
         }[self.letter]


class GameBoard:
    """ This class represents the gameboard itself.
        You are requried to complete this class.
    """

    def __init__(self,width,height):
        """ The constructor for setting up the gameboard """
        self.board=[]
        self.height=height
        self.width=width
        #fill the board with place holders
        for j in range(height):
            self.board.append([])
            for i in range(width):
                self.board[j].append('-')

    def isEmpty(self,x=0,y=0,tile=None):
        if not tile:
            tile=self.board[y][x]
        return tile=='-'

    def set_tile(self,x,y,tile):
        """ Places a tile at a location on the board. """
        self.board[y][x]=tile

    def get_tile(self,x,y):
        """ Returns the tile at a location on the board """
        return self.board[y][x]

    def remove_tile(self,x,y):
        """ Removes the tile from the board and returns the tile"""
        tile=self.board[y][x]
        self.board[y][x]='-'
        return tile

    def get_words(self):
        """ Returns a list of the words on the board sorted in alphabetic order."""
        verTemp=['' for x in range(self.width)]
        words=[]
        for j in range(self.height):
            horizTemp=''
            for i in range(self.width):
                letter=self.board[j][i]
                if self.isEmpty(tile=letter):
                    verTemp[i]=verTemp[i]+'-'
                    if len(horizTemp)>1:
                        words.append(horizTemp)
                        horizTemp=''
                else:
                    horizTemp=horizTemp+letter.get_letter()
                    verTemp[i]=verTemp[i]+letter.get_letter()

        # format such that words filer at the end
        words.extend(verTemp)
        return words.sort()


    def top_scoring_words(self):
        """ Returns a list of the top scoring words.
            If there is a single word, then the function should return a single item list.
            If multilpe words share the highest score, then the list should contain the words sorted alphabetically.
        """
        pass #your code here

    def print_board(self):
        """ Prints a visual representation of the board
            Please use the - character for unused spaces
        """
        for j in range(self.height):
            for i in range(self.width):
                if self.isEmpty(x=i,y=j):
                    print( ' |', '-', end='')
                else:
                    print(' |', self.board[j][i].get_letter(), end='')
            print(' |')

    def letters_placed(self):
        """ Returns a count of all letters currently on the board """
        total=0
        for j in range(self.height):
            total=total+sum(1 for x in self.board[j] if not self.isEmpty(tile=x))
        return total

if __name__ == "__main__":
    """ This is just a sample for testing you might want to add your own tests here """
    board = GameBoard(10,10);
    a = LetterTile('a')
    d = LetterTile("d")
    e = LetterTile("e")
    m = LetterTile("m")
    o = LetterTile("o")

    board.set_tile(1,1,d)
    board.set_tile(2,1,e)
    board.set_tile(3,1,m)
    board.set_tile(4,1,o)
    board.set_tile(2,2,m)
    board.set_tile(2,3,o)
    board.set_tile(1,2,a)

    board.print_board()
    print("There are {} letters placed on the board.".format(board.letters_placed()))
    print(board.get_words())

    # Uncomment below once you have implemented get_words
    # print "=== Words ==="
    # for word in board.get_words():
    #     print(word)

    # Uncomment below once you have implmented top_scoring_words
    # print "=== Top Scoring Words ==="
    # for word in board.top_scoring_words():
    #     print(word)
