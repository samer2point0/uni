import itertools

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
	This method should take a list of strings as input. Each string is equivalent to one letter
	(i.e. one morse code string). The entire list of strings represents a word.

	This method should convert the strings from morse code into english, and return the word as a string.

	"""
	# Please complete this method to perform the above described function
	word=''
	for char in inputStringList:
		word=''.join([word, Code[char].lower()])
	return word



def morsePartialDecode(inputStringList):
    dictionaryFileLoc ='./dictionary.txt'
    Dict=[]

    with open(dictionaryFileLoc,'r') as DF:
        for line in DF:
            Dict.append(line.strip())

    Dict.sort()
    lettersList=[]
    #creates list of tuples with containing the possible letters for each morse code sequence
    for pchar in inputStringList :

        tempdot=pchar.replace('x', '.')
        tempdash=pchar.replace('x', '-')

        if tempdot in Code and tempdash in Code:
            lettersList.append((Code[tempdot],Code[tempdash]))
        elif tempdot in Code:
            lettersList.append((Code[tempdot]))
        elif tempdash in Code:
            lettersList.append((Code[tempdash]))
        else:
            print('invalid char code')

    print(lettersList)
    #could also implement recursivly, complexity 2^n
    tup=lettersList.pop()
    wordList=[tup[0],tup[1]]
    while lettersList != []:
        #staring from last letter because more efficient
        tup=lettersList.pop()
        tempList=wordList.copy()
        for word in tempList:
            wordList.remove(word)
            for i in range(len(tup)):
                wordList.append(''.join([tup[i],word]))


    tempList=wordList.copy()
    for word in tempList:
        if not (word in Dict):
            wordList.remove(word)

    return wordList


class Maze:
    def __init__(self):
        """
		Constructor - You may modify this, but please do not add any extra parameters
		"""
        self.grid=[[1]]
        self.opens=[]

    def addCoordinate(self,x,y,blockType):
        """
        Add information about a coordinate on the maze grid
        x is the x coordinate
        y is the y coordinate
        blockType should be 0 (for an open space) of 1 (for a wall)
        """
        for j in range(len(self.grid)):
            if y >= len(self.grid):
                self.grid.append([1 for x in range(len(self.grid[0]))])
            for i in range(x - len(self.grid[j])+1):
                self.grid[j].append(1)

        self.grid[y][x]=blockType


    def printMaze(self):
        """
        Print out an ascii representation of the maze.
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
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x]==0:
                    self.opens.append((x,y))


    def findMove(self, route,pos, goal):
        x,y=pos[0],pos[1]
        Move=None
        allmovesList=[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
        allmovesList=list(filter(lambda x: x in self.opens, allmovesList))

        choice=list(filter(lambda x: not x in route, allmovesList))

        if goal in allmovesList:
            return goal
        elif choice:
            return choice.pop()
        else:
            return (x,y)


    def findRoute(self,x1,y1,x2,y2):
        """
        This method should find a route, traversing open spaces, from the coordinates (x1,y1) to (x2,y2)
        It should return the list of traversed coordinates followed along this route as a list of tuples (x,y),
        in the order in which the coordinates must be followed
        If no route is found, return an empty list
        """
        move=(x1,y1)
        route=[move]
        self.open()
        #depth first search
        i=0
        while True:
            i=i+1
            x,y=move[0],move[1]
            move=self.findMove(route,(x,y),(x2,y2))
            if move==(x2,y2):
                route.append(move)
                break
            elif move==(x,y):
                route.remove(move)
                self.opens.remove(move)
                move=route[-1]
            else:
                route.append(move)


            if i > 2*len(self.grid)*len(self.grid[0]):
                print(route)
                return []

        return route


def morseCodeTest():
	"""
	HELLO to the decode method. It should receive a string "HELLO" in return.
	This is provided as a simple test example, but by no means covers all possibilities, and you should
	fulfill the methods as described in their comments.
	"""

	hello = ['....','.','.-..','.-..','---']
	print(morseDecode(hello))

def partialMorseCodeTest():
	"""
	This test program passes the partial morse code as a list of strings
	to the morsePartialDecode method. This is provided as a simple test example, but by
	no means covers all possibilities, and you should fulfill the methods as described in their comments.
	"""

	# This is a partial representation of the word TEST, amongst other possible combinations
	test = ['x','x','x..','x']
	print(morsePartialDecode(test))

	# This is a partial representation of the word DANCE, amongst other possible combinations
	dance = ['x..','x-','x.','x.-.','x']
	print(morsePartialDecode(dance))


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

def main():
	morseCodeTest()
	partialMorseCodeTest()
	mazeTest()

if(__name__ == "__main__"):
	main()
