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
        self.x=copy.deepcopy(x)
    def setY(self,y):
        self.y =copy.deepcopy(y)
    def getX(self):
        return copy.deepcopy(self.x)
    def getY(self):
        return copy.deepcopy(self.y)

    def equals(self,point):
        return (abs(self.x-point.x) <self.TOLERANCE and abs(self.y-point.y) <self.TOLERANCE)

    def distance(self, point):
        return ((self.x - point.x)**2 + (self.y - point.y)**2 )**0.5

class Circle(Shape):

    def __init__(self,centre,radius):
        self.centre=centre
        self.radius=radius
    def __str__(self):
        return 'This circle has its centre at '+ str(self.centre) +' and a radius of ' + str(self.radius)
    def setCentre(self, point):
        self.centre=copy.deepcopy(point)
    def setRadius(self, radius):
        self.radius=radius
    def getCentre(self):
        return copy.deepcopy(self.centre)
    def getRadius(self):
        return copy.deepcopy(self.radius)

    def area(self):
        return (self.radius**2)*math.pi

    def compare(self,shape):
        if abs(self.area() - shape.area())< self.TOLERANCE:
            return 0
        elif self.area()> shape.area():
            return 1
        else:
            return -1

    def envelops(self,shape):
        #test
        if isinstance(shape, Circle):
            return (self.radius >= (self.centre.distance(shape.centre)+shape.radius) )
        else:
            #assuming square allign with x,y axes
            furthestPoint=Point(shape.topLeft.getX()+shape.getLength(),shape.topLeft.getY()+shape.getLength())
            return (self.radius >= self.centre.distance(furthestPoint))

    def equals(self, circle):
        return(self.centre.equals(circle.centre) and abs(self.radius - circle.radius)<self.TOLERANCE)

class Square(Shape):

    #what is actually passed to the constructor point object v (x,y)
    def __init__(self,top_left,length):
        self.topLeft=top_left
        self.length=length
    def __str__(self):
        #test
        return 'This square\'s top left is at '+ str(self.topLeft) +' and the side length is ' + str(self.length)
    def setTopLeft(self, point):
        self.topLeft=copy.deepcopy(point)
    def setLength(self, length):
        self.length=length
    def getTopLeft(self):
        return copy.deepcopy(self.TopLeft)
    def getLength(self):
        return copy.deepcopy(self.length)

    def area(self):
        return self.length**2

    def compare(self,shape):
        #test
        if abs(self.area() - shape.area())< self.TOLERANCE:
            return 0
        elif self.area()>shape.area():
            return 1
        else:
            return -1

    def envelops(self,shape):
        if isinstance(shape, Square):
            #double check
            topLeftCondition= ((self.topLeft.getX() >= shape.topLeft.getX()) and (self.topLeft.getY() <= shape.topLeft.getY()))
            lengthCondition= self.length >= shape.length + max((self.topLeft.getX() - shape.topLeft.getX()), (self.topLeft.getY() - shape.topLeft.getY()))
            return topLeftCondition and lengthCondition
        else:
            minCentreToXEdge=min((shape.centre.getX()-self.topLeft.getX()),(self.topLeft.getX()-shape.centre.getX()+self.length))
            minCentreToYEdge=min((shape.centre.getY()-(self.topLeft.getY()-self.length)),(self.topLeft.getY()-shape.centre.getY()))
            #check if centre of circle is inside the square and if distance from edges of square to centre are all bigger than radius
            return (minCentreToYEdge >= 0 and minCentreToYEdge >= shape.radius) and (minCentreToXEdge >= 0 and minCentreToXEdge >= shape.radius)

    def equals(self, square):
        return(self.topLeft.equals(square.topLeft) and abs(self.length - square.length)<self.TOLERANCE)


class Assignment:



    def __init__(self): #initilising instance variables
        self.pointsList=[]
        self.circlesList=[]
        self.squaresList=[]
        self.origin=Point(0,0)

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
        print('the mean of circles area is: ', self.mean_circle_area())
        print('the mean of squares area is: ', self.mean_square_area())
        print('the standard deviation of circles area is: ', self.std_dev_circle_area())
        print('the standrad deviation of squares area is: ', self.std_dev_square_area())
        print('the median area of the circles is: ', self.median_circle_area())
        print('the median area of the squares is: ', self.median_square_area())

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
        circle=Circle(self.origin,maxr)
        return circle.area()

    def min_circle_area(self):
        minr=999999999
        for c in self.circlesList:
            r=float(c[3])
            if r<minr:
                minr=r
        circle=Circle(self.origin,minr)
        return circle.area()

    def max_square_area(self):
        maxl=0
        for s in self.squaresList:
            l=float(s[3])
            if l>maxl:
                maxl=l
        square=Square(self.origin,maxl)
        return square.area()

    def min_square_area(self):
        minl=999999999
        for s in self.squaresList:
            l=float(s[3])
            if l<minl:
                minl=l
        square=Square(self.origin,minl)
        return square.area()

    def mean_circle_area(self):
        circle=Circle(self.origin,1)
        sum=0
        for c in self.circlesList:
            r=float(c[3])
            circle.setRadius(r)
            sum=sum+circle.area()
        return sum/len(self.circlesList)

    def mean_square_area(self):
        square=Square(self.origin,1)
        sum=0
        for s in self.squaresList:
            l=float(s[3])
            square.setLength(l)
            sum=sum+square.area()
        return sum/len(self.squaresList)

    def std_dev_circle_area(self):
        mean=self.mean_circle_area()
        circle=Circle(self.origin,1)
        sum=0
        for c in self.circlesList:
            r=float(c[3])
            circle.setRadius(r)
            sum=sum+(circle.area()-mean)**2
        return (sum/(len(self.circlesList)-1))**0.5

    def std_dev_square_area(self):
        mean=self.mean_square_area()
        square=Square(self.origin,1)
        sum=0
        for s in self.squaresList:
            l=float(s[3])
            square.setLength(l)
            sum=sum+(square.area()-mean)**2
        return (sum/(len(self.squaresList)-1))**0.5

    def median_circle_area(self):
        self.circlesList.sort(key=lambda x: x[3])
        medianLoc=math.floor(len(self.circlesList)/2)
        medianRadius=float(self.circlesList[medianLoc][3])
        circle=Circle(self.origin, medianRadius)
        return circle.area()

    def median_square_area(self):
        self.squaresList.sort(key=lambda x: x[3])
        medianLoc=math.floor(len(self.squaresList)/2)
        medianLength=float(self.squaresList[medianLoc][3])
        square=Square(self.origin, medianLength)
        return square.area()

class Test():
    def __init__(self):
        self.p1=Point(0,0)
        self.p2=Point(1,1)
        self.c1=Circle(self.p1, 1)
        self.c2=Circle(self.p2, 3)
        self.s1=Square(self.p1, 0.5)
        self.s2=Square(self.p1, 2)

    def pTest(self):
        p3=copy.deepcopy(self.p1)
        assert self.p1.distance(self.p2)==2**0.5
        assert self.p1.equals(p3)
        p3.setX(1)
        assert not self.p1.equals(p3)
        print('point testing all good')

    def cTest(self):
        c3=copy.deepcopy(self.c1)
        assert self.c1.equals(c3)
        assert not self.c1.equals(self.c2)
        assert self.c1.compare(c3)==0
        assert self.c1.compare(self.c2)==-1
        assert self.c2.compare(self.c1)==1
        assert self.c1.envelops(c3)
        assert self.c2.envelops(self.c1)
        assert not self.c1.envelops(self.c2)
        assert self.c1.envelops(self.s1)
        assert not self.c1.envelops(self.s2)
        print(str(self.c1),'\ncircle testing all good')

    def sTest(self):
        s3=copy.deepcopy(self.s1)
        assert self.s1.equals(s3)
        assert not self.s1.equals(self.s2)
        assert self.s1.compare(s3)==0
        assert self.s1.compare(self.s2)==-1
        assert self.s2.compare(self.s1)==1
        assert self.s1.envelops(s3)
        assert self.s2.envelops(self.s1)
        assert not self.s1.envelops(self.s2)
        self.s2.setTopLeft(Point(-1,1))
        assert self.s2.envelops(self.c1)
        assert not self.s1.envelops(self.c1)
        print(str(self.s1),'\nsquare testing all good')


if __name__ == "__main__":
    #You should add your own code heere to test your work
    print ("=== Testing Part 2 ===")
    assignment = Assignment()
    test=Test()
    test.pTest()
    test.cTest()
    test.sTest()
    assignment.analyse("1000shapetest.data")
