import math

class Shape:
    """This class is a convenient place to store the tolerance variable"""
    TOLERANCE = 1.0e-6

class Point(Shape):
    def __init__(self, x, y):
        self.x=x
        self.y=y
    def setX(self,x):
        self.x=x
    def setY(self,y):
        self.y=y
    def equals(self,point):
        return (abs(self.x-point.x) <self.TOLERANCE and abs(self.y-point.y) <self.TOLERANCE)

    def distance(self, point):
        return ((self.x - point.x)**2 + (self.y - point.y)**2 )**0.5

class Circle(Shape):

    def __init__(self,centre,radius):
        self.centre=Point(centre[0],centre[1])
        self.radius=radius

    def area(self):
        return (self.radius**2)*math.pi

    def compare(self,shape):
        pass #your code here

    def envelops(self,shape):
        pass #your code here

    def equals(self, circle):
        return(self.centre.equals(circle.centre) and abs(self.radius - circle.radius)<self.TOLERANCE)

class Square(Shape):

    def __init__(self,top_left,length):
        self.topLeft=Point(top_left[0],top_left[1])
        self.length=length

    def area(self):
        return self.length**2

    def compare(self,shape):
        pass #your code here

    def envelops(self,shape):
        pass #your code here

    def equals(self, square):
        return(self.topLeft.equals(square.topLeft) and abs(self.length - square.length)<self.TOLERANCE)


class Assignment:

    def __init__(self): #initilising instance variables
        self.pointsList=[]
        self.circlesList=[]
        self.squaresList=[]

    def analyse(self, filename):
        #copying file contents into a temporary list
        shapesFile=open(filename,'r')
        tempList=shapesFile.read().strip().split('\n')
        shapesFile.close()
        #classifying different shapes and storing them in different lists
        for shape in tempList:
            s=shape.split()
            if s[3]==str(0):
                s[0]='point'
                self.pointsList.append(s)
            elif s[0]=='circle':
                self.circlesList.append(s)
            elif s[0]== 'square':
                self.squaresList.append(s)
        #printing out statistics
        print('the shapes count is: ', self.shape_count())
        print('the circles count is: ', self.circle_count())
        print('the squares count is: ', self.square_count())
        print('the largest circle area is: ', self.max_circle_area())
        print('the smallest circle area is: ', self.min_circle_area())
        print('the largest square area is: ', self.max_square_area())
        print('the smallest square area is: ', self.min_square_area())

    def shape_count(self):
        return len(self.squaresList)+len(self.circlesList)

    def circle_count(self):
        return len(self.circlesList)

    def square_count(self):
        return len(self.squaresList)

    def max_circle_area(self):
        maxr=0
        for c in self.circlesList:
            r=float(c[3])
            if r>maxr:
                maxr=r
        circle=Circle((0,0),maxr)
        return circle.area()

    def min_circle_area(self):
        minr=999999999
        for c in self.circlesList:
            r=float(c[3])
            if r<minr:
                minr=r
        circle=Circle((0,0),minr)
        return circle.area()

    def max_square_area(self):
        maxl=0
        for s in self.squaresList:
            l=float(s[3])
            if l>maxl:
                maxl=l
        square=Square((0,0),maxl)
        return square.area()

    def min_square_area(self):
        minl=999999999
        for s in self.squaresList:
            l=float(s[3])
            if l<minl:
                minl=l
        square=Square((0,0),minl)
        return square.area()

    def mean_circle_area(self):
        pass #your code here

    def mean_square_area(self):
        pass #your code here

    def std_dev_circle_area(self):
        pass #your code here

    def std_dev_square_area(self):
        pass #your code here

    def median_circle_area(self):
        pass #your code here

    def median_square_area(self):
        pass #your code here


if __name__ == "__main__":
    #You should add your own code heere to test your work
    print ("=== Testing Part 2 ===")
    assignment = Assignment()
    assignment.analyse("smallshapetest.data")
    print(assignment.shape_count())
