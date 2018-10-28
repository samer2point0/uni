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
        pass #your code here

    def set_tile(self,x,y,tile):
        """ Places a tile at a location on the board. """
        pass #your code here

    def get_tile(self,x,y):
        """ Returns the tile at a location on the board """    
        pass #your code here

    def remove_tile(self,x,y):
        """ Removes the tile from the board and returns the tile"""    
        pass #your code here
        
    def get_words(self):
        """ Retuns a list of the words on the board sorted in alphabetic order. 
        
        """
        pass #your code here
    
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
        pass #your code here
        

    def letters_placed(self):
        """ Returns a count of all letters currently on the board """
        pass #your code here
        
if __name__ == "__main__":
    """ This is just a sample for testing you might want to add your own tests here """
    board = GameBoard(10,10);
    
    d = LetterTile("d")
    e = LetterTile("e")
    m = LetterTile("m")
    o = LetterTile("o")
    
    board.set_tile(1,1,d)
    board.set_tile(2,1,e)
    board.set_tile(3,1,m)
    board.set_tile(4,1,o)
    
    print "There are {} letters placed on the board.".format(board.letters_placed())

    # Uncomment below once you have implemented get_words
    # print "=== Words ==="
    # for word in board.get_words():
    #     print(word)
    
    # Uncomment below once you have implmented top_scoring_words
    # print "=== Top Scoring Words ==="
    # for word in board.top_scoring_words():
    #     print(word)