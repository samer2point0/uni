<<<<<<< HEAD
import itertools

def morseDecode(inputStringList):
	"""
	This method should take a list of strings as input. Each string is equivalent to one letter
	(i.e. one morse code string). The entire list of strings represents a word.

	This method should convert the strings from morse code into english, and return the word as a string.

	"""
	# Please complete this method to perform the above described function
	pass

def morsePartialDecode(inputStringList):
	"""
	This method should take a list of strings as input. Each string is equivalent to one letter
	(i.e. one morse code string). The entire list of strings represents a word.

	However, the first character of every morse code string is unknown (represented by an 'x' (lowercase))
	For example, if the word was originally TEST, then the morse code list string would normally be:
	['-','.','...','-']

	However, with the first characters missing, I would receive:
	['x','x','x..','x']

	With the x unknown, this word could be TEST, but it could also be EESE or ETSE or ETST or EEDT or other permutations.

	We define a valid words as one that exists within the dictionary file provided on the website, dictionary.txt
	When using this file, please always use the location './dictionary.txt' and place it in the same directory as
	the python script.

	This function should find and return a list of strings of all possible VALID words.
	"""

	dictionaryFileLoc = './dictionary.txt'
	# Please complete this method to perform the above described function
	pass

class Maze:
	def __init__(self):
		"""
		Constructor - You may modify this, but please do not add any extra parameters
		"""

		pass

	def addCoordinate(self,x,y,blockType):
		"""
		Add information about a coordinate on the maze grid
		x is the x coordinate
		y is the y coordinate
		blockType should be 0 (for an open space) of 1 (for a wall)
		"""

		# Please complete this method to perform the above described function
		pass

	def printMaze(self):
		"""
		Print out an ascii representation of the maze.
		A * indicates a wall and a empty space indicates an open space in the maze
		"""

		# Please complete this method to perform the above described function
		pass

	def findRoute(self,x1,y1,x2,y2):
		"""
		This method should find a route, traversing open spaces, from the coordinates (x1,y1) to (x2,y2)
		It should return the list of traversed coordinates followed along this route as a list of tuples (x,y),
		in the order in which the coordinates must be followed
		If no route is found, return an empty list
		"""
		pass

def morseCodeTest():
	"""
	This test program passes the morse code as a list of strings for the word
=======
Code = {'.-':'a',      '-...': 'b',    '-.-.':'c',
        '-..':'d',    '.':'e',      '..-.':'f',
        '--.':'g',     '....':'h',   '..':'i',
         '.---':'j',    '-.-':'k',     '.-..':'l',
         '--':'m',      '-.':'n',      '---':'o',
        '.--.':'p',   '--.-':'q',   '.-.':'r',
      	'...':'s',     '-':'t',       '..-':'u',
        '...-':'v',    '.--':'w',     '-..-':'x',
         '-.--':'y',    '--..':'z',

         '-----':'0',   '.----':'1',   '..---':'2',
        '...--':'3',   '....-':'4',   '.....':'5',
         '-....':'6',   '--...':'7',   '---..':'8',
         '----.':'9'
        }


def morseDecode(inputStringList):
	"""
	This method should take a list of strings containg a morse code letter sequence
     as input and converts each string to it's equivelent letter
	"""
	word=''
    #for each charrecter append to the word so far
	for char in inputStringList:
		word=''.join([word, Code[char].lower()])
	return word



def morsePartialDecode(inputStringList):
    #initiate variables and read dictionary file
    dictionaryFileLoc ='./dictionary.txt'
    Dict=[]
    lettersList=[]
    with open(dictionaryFileLoc,'r') as DF:
        for line in DF:
            Dict.append(line.strip())

    #creates list of tuples containing the possible letters for each morse code sequence read
    for pchar in inputStringList :
        tempdot=pchar.replace('x', '.')
        tempdash=pchar.replace('x', '-')
        # after replacing the first signal with dot/dash check if such a letter exists
        #and if it does append it to the letters list
        if tempdot in Code and tempdash in Code:
            lettersList.append((Code[tempdot],Code[tempdash]))
        elif tempdot in Code:
            lettersList.append((Code[tempdot]))
        elif tempdash in Code:
            lettersList.append((Code[tempdash]))
        else:
            print('invalid char code')

    #next part creates a list of all the possible sequences given the letters list generated
    #this part is implemented iteratively because otherwise it could escape python's recursive depth
    tup=lettersList.pop()
    #add the possible lastst letters as the beggining of the words list
    wordList=[tup[0],tup[1]]
    while lettersList != []:
        #staring from last letter because more efficient
        tup=lettersList.pop()
        tempList=wordList.copy()
        """for each word concatenated in the list so far remove it and replace it with
        one or two words depending on the next possible letter in the letters list"""
        for word in tempList:
            wordList.remove(word)
            for i in range(len(tup)):
                wordList.append(''.join([tup[i],word]))

    #for each word in wors list check if word is in dictionary, if not remove it
    tempList=wordList.copy()
    for word in tempList:
        if not (word in Dict):
            wordList.remove(word)

    return wordList


class Maze:
    def __init__(self):
        #initialise grid and a opens which is a list of the open locations
        self.grid=[[1]]
        self.opens=[]

    def addCoordinate(self,x,y,blockType):
        """if x or y is out of range of the self.grid variable add coulumns and
         rows untill x,y fit, aand fill each entry with 1"""
        for j in range(len(self.grid)):
            if y >= len(self.grid):
                self.grid.append([1 for x in range(len(self.grid[0]))])
            for i in range(x - len(self.grid[j])+1):
                self.grid[j].append(1)

        #add actuall coordinate
        self.grid[y][x]=blockType


    def printMaze(self):
        """
        Prints out an ascii representation of the maze.
        A * indicates a wall and a empty space indicates an open space in the maze
        """
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x]==0:
                    print(' ', end='')
                else:
                    print('*',end='')
            print('\n')


    def open(self):
        """updates the variable opens containing the available spaces as a tuple of (x,y)"""
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x]==0:
                    self.opens.append((x,y))


    def findMove(self, route,pos, goal):
        """returns goal if it's a possible move, if not return a move that's not going backwards
        otherwise return same position"""

        x,y=pos[0],pos[1]
        Move=None
        #all possible moves filtered on whats is also an open spance still
        allmovesList=[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
        allmovesList=list(filter(lambda x: x in self.opens, allmovesList))

        #find all possible moves that are not backwards and store them in choice
        choice=list(filter(lambda x: not x in route, allmovesList))

        #return goal, otherwise one of the choice moves, otherwise same locations
        if goal in allmovesList:
            return goal
        elif choice:
            return choice.pop()
        else:
            return (x,y)


    def findRoute(self,x1,y1,x2,y2):
        """
        This method finds a route, traversing (depth first search) open spaces, from the coordinates (x1,y1) to (x2,y2)
        It should return the list route containing the path if no route found it returns an empty list
        """
        #initialise first move, route , and open spaces
        move=(x1,y1)
        route=[move]
        self.open()

        """depth first search is implemeted, by following a path until it's blocked and then traversing back until
         the last open space, filling the return route as deadends on the way"""
        i=0
        while True:
            i=i+1
            x,y=move[0],move[1]
            move=self.findMove(route,(x,y),(x2,y2))
            #if move is goal append it to route and break from loop
            if move==(x2,y2):
                route.append(move)
                break
            #else if move returned is the same location, mark that location as a deadend by removing it form self.opens variables
            #after that traverse back by taking a step backwards and removing a move from the route
            elif move==(x,y):
                route.remove(move)
                self.opens.remove(move)
                move=route[-1]
            #if move is not goal and not deadend append it to route
            else:
                route.append(move)

            #if the loop ran for more than the number of possible positions twice, infer no possible route and hence return empty list
            if i > 2*len(self.grid)*len(self.grid[0]):
                print(route)
                return []

        return route


def morseCodeTest():
	"""
>>>>>>> 5b688ca46a9b52a1ebfa08507cbb19b66bd85d2e
	HELLO to the decode method. It should receive a string "HELLO" in return.
	This is provided as a simple test example, but by no means covers all possibilities, and you should
	fulfill the methods as described in their comments.
	"""

	hello = ['....','.','.-..','.-..','---']
	print(morseDecode(hello))

def partialMorseCodeTest():
<<<<<<< HEAD

	"""
	This test program passes the partial morse code as a list of strings 
=======
	"""
	This test program passes the partial morse code as a list of strings
>>>>>>> 5b688ca46a9b52a1ebfa08507cbb19b66bd85d2e
	to the morsePartialDecode method. This is provided as a simple test example, but by
	no means covers all possibilities, and you should fulfill the methods as described in their comments.
	"""

	# This is a partial representation of the word TEST, amongst other possible combinations
	test = ['x','x','x..','x']
	print(morsePartialDecode(test))

	# This is a partial representation of the word DANCE, amongst other possible combinations
	dance = ['x..','x-','x.','x.-.','x']
	print(morsePartialDecode(dance))

<<<<<<< HEAD
def mazeTest():
	"""
	This sets the open space coordinates for the example
	maze in the assignment.
	The remainder of coordinates within the max bounds of these specified coordinates
	are assumed to be walls
	"""
	myMaze = Maze()
	myMaze.addCoordinate(1,0,0)
	myMaze.addCoordinate(1,1,0)
	myMaze.addCoordinate(7,1,0)
	myMaze.addCoordinate(1,2,0)
	myMaze.addCoordinate(2,2,0)
	myMaze.addCoordinate(3,2,0)
	myMaze.addCoordinate(4,2,0)
	myMaze.addCoordinate(6,2,0)
	myMaze.addCoordinate(7,2,0)
	myMaze.addCoordinate(4,3,0)
	myMaze.addCoordinate(7,3,0)
	myMaze.addCoordinate(4,4,0)
	myMaze.addCoordinate(7,4,0)
	myMaze.addCoordinate(3,5,0)
	myMaze.addCoordinate(4,5,0)
	myMaze.addCoordinate(7,5,0)
	myMaze.addCoordinate(1,6,0)
	myMaze.addCoordinate(2,6,0)
	myMaze.addCoordinate(3,6,0)
	myMaze.addCoordinate(4,6,0)
	myMaze.addCoordinate(5,6,0)
	myMaze.addCoordinate(6,6,0)
	myMaze.addCoordinate(7,6,0)
	myMaze.addCoordinate(5,7,0)
=======

def mazeTest():
    """
    This sets the open space coordinates for the example
    maze in the assignment.
    The remainder of coordinates within the max bounds of these specified coordinates
    are assumed to be walls
    """
    myMaze = Maze()
    myMaze.addCoordinate(1,0,0)
    myMaze.addCoordinate(1,1,0)
    myMaze.addCoordinate(7,1,0)
    myMaze.addCoordinate(1,2,0)
    myMaze.addCoordinate(2,2,0)
    myMaze.addCoordinate(3,2,0)
    myMaze.addCoordinate(4,2,0)
    myMaze.addCoordinate(6,2,0)
    myMaze.addCoordinate(7,2,0)
    myMaze.addCoordinate(4,3,0)
    myMaze.addCoordinate(7,3,0)
    myMaze.addCoordinate(4,4,0)
    myMaze.addCoordinate(7,4,0)
    myMaze.addCoordinate(3,5,0)
    myMaze.addCoordinate(4,5,0)
    myMaze.addCoordinate(7,5,0)
    myMaze.addCoordinate(1,6,0)
    myMaze.addCoordinate(2,6,0)
    myMaze.addCoordinate(3,6,0)
    myMaze.addCoordinate(4,6,0)
    myMaze.addCoordinate(5,6,0)
    myMaze.addCoordinate(6,6,0)
    myMaze.addCoordinate(7,6,0)
    myMaze.addCoordinate(5,7,0)


    myMaze.printMaze()
    print(myMaze.findRoute(5,7,1,0))
>>>>>>> 5b688ca46a9b52a1ebfa08507cbb19b66bd85d2e

def main():
	morseCodeTest()
	partialMorseCodeTest()
	mazeTest()

if(__name__ == "__main__"):
	main()
