import math
import copy

class Shape:
    """This class is a convenient place to store the tolerance variable"""
    TOLERANCE = 1.0e-6

class Point(Shape):
    def __init__(self, x, y):
        self.x=x
        self.y=y
    def __str__(self):
        return '('+str(self.x)+','+str(self.y)+')'
    #do I need to deepcopy for setters?
    def setX(self,x):
        self.x=x
    def setY(self,y):
        self.y=y
    def getX(self,x):
        return copy.deepcopy(self.x)
    def getY(self,y):
        return copy.deepcopy(self.y)

    def equals(self,point):
        return (abs(self.x-point.x) <self.TOLERANCE and abs(self.y-point.y) <self.TOLERANCE)

    def distance(self, point):
        return ((self.x - point.x)**2 + (self.y - point.y)**2 )**0.5

class Circle(Shape):

    def __init__(self,centre,radius):
        self.centre=Point(centre[0],centre[1])
        self.radius=radius
    def __str__(self):
        return 'This circle has its centre at '+ self.centre +' and a radius of ' + str(self.radius)
    def setCentre(self, point):
        self.centre=point
    def setRadius(self, radius):
        self.radius=radius
    def getCentre(self):
        return copy.deepcody(self.centre)
    def getRadius(self):
        return copy.deepcody(self.radius)

    def area(self):
        return (self.radius**2)*math.pi

    def compare(self,shape):
        if abs(self.area() - shape.area())< self.TOLERANCE:
            return 0
        elif self.area()>shape.area():
            return 1
        else self.area()<shape.area():
            return -1

    def envelops(self,shape):
        #test
        if isinstance(shape, Circle):
            return (self.radius > (self.centre.distance(shape.centre)+shape.radius) )
        else:
            #assuming square allign with x,y axes
            furthestPoint=Point(shape.topLeft.getX()+shape.getLength,shape.topLeft.getY()+shape.getLength)
            return (self.radius > self.centre.distance(furthestPoint))

    def equals(self, circle):
        return(self.centre.equals(circle.centre) and abs(self.radius - circle.radius)<self.TOLERANCE)

class Square(Shape):

    #what is actually passed to the constructor point object v (x,y)
    def __init__(self,top_left,length):
        self.topLeft=Point(top_left[0],top_left[1])
        self.length=length
    def __str__(self):
        #test
        return 'This square\'s top left is at '+ self.topLeft +' and the side length is ' + str(self.length)
    def setTopLeft(self, point):
        self.topLeft=point
    def setLength(self, length):
        self.length=length
    def getTopLeft(self):
        return copy.deepcody(self.TopLeft)
    def getLength(self):
        return copy.deepcody(self.length)

    def area(self):
        return self.length**2

    def compare(self,shape):
        #test
        if abs(self.area() - shape.area())< self.TOLERANCE:
            return 0
        elif self.area()>shape.area():
            return 1
        else self.area()<shape.area():
            return -1

    def envelops(self,shape):
        if isinstance(shape, Square):
            #double check
            topLeftCondition= ((self.topLeft.getX() > shape.topLeft.getX()) and (self.topLeft.getY() < shape.topLeft.getY()))
            lengthCondition= self.length() > shape.length + max((self.topLeft.getX() - shape.topLeft.getX()), (self.topLeft.getY() - shape.topLeft.getY()))
            return topLeftCondition and lengthCondition
        else:
            #double check
            minCentreToXEdge=min((shape.centre.getX()-self.topLeft.getX()),(self.topLeft.getX()-shape.centre.getX()+self.length))
            minCentreToYEdge=min((shape.centre.getY()-(self.length+self.topLeft.getY())),(self.topLeft.getY()-shape.centre.getY()))
            return (minCentreToYEdge > 0 and minCentreToYEdge < shape.radius) and (minCentreToXEdge > 0 and minCentreToXEdge < shape.radius)

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
            s=shape.split()pass #your code here
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
        print('the largest square area is: ', self.max_squtopLeftCondition= ((self.topLeft.getX() > shape.centre.getX()) and (self.centre.getY() < shape.topLeft.getY()))
            shape.are_area())
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
            r=float(c[3])pass #your code here
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
