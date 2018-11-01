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

    #setters and getters
    def setX(self,x):
        self.x=x
    def setY(self,y):
        self.y =y
    def getX(self):
        return self.x
    def getY(self):
        return self.y

    def equals(self,point):#returns is differences in x and y are less than tolerance ?
        return (abs(self.x-point.x) <self.TOLERANCE and abs(self.y-point.y) <self.TOLERANCE)
    def distance(self, point):#calculates eucledian  between two points
        return ((self.x - point.x)**2 + (self.y - point.y)**2 )**0.5

class Circle(Shape):

    def __init__(self,centre,radius):
        self.centre=copy.deepcopy(centre)
        self.radius=radius
    def __str__(self):
        return 'This circle has its centre at '+ str(self.centre) +' and a radius of ' + str(self.radius)

    #setters and getters using deepcopy when neccassary to avoid unintended alterations
    def setCentre(self, point):
        self.centre=copy.deepcopy(point)
    def setRadius(self, radius):
        self.radius=radius
    def getCentre(self):
        return copy.deepcopy(self.centre)
    def getRadius(self):
        return self.radius

    def area(self):
        return (self.radius**2)*math.pi
    #checks if passed shape is equal, larger or smaller than calling circle and returns 0,1 and-1 respectively
    def compare(self,shape):
        if abs(self.area() - shape.area())< self.TOLERANCE:
            return 0
        elif self.area()> shape.area():
            return 1
        else:
            return -1

    def envelops(self,shape):# retrun true if calling circle envelops passed shape
        if isinstance(shape, Circle):
            return (self.radius >= (self.centre.distance(shape.getCentre())+shape.getRadius()) )
        else:
            #assuming square alligns with x,y axes find bottom right corner
            envelopsTopLeft=(self.radius >= (self.centre.distance(shape.getTopLeft())))
            envelopsBottomRight=(self.radius >= self.centre.distance(shape.getBottomRight()))
            #if two diagonal corners are enveloped then return true
            return (envelopsTopLeft and envelopsBottomRight)

    def equals(self, circle):#returns true if centre and radius are equal within tolerence
        return(self.centre.equals(circle.getCentre()) and abs(self.radius - circle.getRadius())<self.TOLERANCE)

class Square(Shape):

    def __init__(self,top_left,length):
        self.topLeft=top_left
        self.length=length
        self.bottomRight=Point(top_left.getX()+length, top_left.getY()-length)
    def __str__(self):
        return 'This square\'s top left is at '+ str(self.topLeft) +' and the side length is ' + str(self.length)

    #setters and getters using deepcopy when neccassary to avoid unintended alterations
    def setTopLeft(self, point):
        self.topLeft=copy.deepcopy(point)
    def setLength(self, length):
        self.length=length
    def getTopLeft(self):
        return copy.deepcopy(self.topLeft)
    def getBottomRight(self):
        return copy.deepcopy(self.bottomRight)
    def getLength(self):
        return self.length

    def area(self):
        return self.length**2
    #checks if passed shape is equal, larger or smaller than calling circle and returns 0,1 and-1 respectively
    def compare(self,shape):
        if abs(self.area() - shape.area())< self.TOLERANCE:
            return 0
        elif self.area()>shape.area():
            return 1
        else:
            return -1

    def envelops(self,shape):# retrun true if calling circle envelops passed shape
        if isinstance(shape, Square):
            envelopsTopLeft= min((shape.topLeft.getX()-self.topLeft.getX()),(self.topLeft.getY()-shape.topLeft.getY())) >= 0
            envelopsBottomRight= max((shape.bottomRight.getX()-self.bottomRight.getX()),(self.bottomRight.getY()-shape.bottomRight.getY())) <= 0
            return envelopsTopLeft and envelopsBottomRight
        else:
            #find minimmum distance form center of circle to edges
            minCentreToXEdge=min((shape.centre.getX()-self.topLeft.getX()),(self.bottomRight.getX()-shape.centre.getX()))
            minCentreToYEdge=min((shape.centre.getY()-(self.bottomRight.getY()),(self.topLeft.getY()-shape.centre.getY())))
            #if min centere to edges are positive then centre is within square area
            #if distance from edges of square to centre are all bigger than radius of circle then circle is enveloped by square
            return minCentreToYEdge >= shape.radius and minCentreToXEdge >= shape.radius

    def equals(self, square):#returns true if centre and radius are equal within tolerence
        return (self.topLeft.equals(square.topLeft) and abs(self.length - square.length)<self.TOLERANCE)


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
        print(self.shape_count())
        print(self.circle_count())
        print(self.square_count())
        print(self.max_circle_area())
        print(self.min_circle_area())
        print(self.max_square_area())
        print(self.min_square_area())
        print(self.mean_circle_area())
        print(self.mean_square_area())
        print(self.std_dev_circle_area())
        print(self.std_dev_square_area())
        print(self.median_circle_area())
        print(self.median_square_area())

    def shape_count(self):
        return len(self.squaresList)+len(self.circlesList)

    def circle_count(self):
        return len(self.circlesList)

    def square_count(self):
        return len(self.squaresList)

    def max_circle_area(self):
        maxr=0
        #find circle with largest radius
        for c in self.circlesList:
            r=float(c[3])
            if r>maxr:
                maxr=r
        circle=Circle(self.origin,maxr)
        #return area of circle with largest radius
        return circle.area()

    def min_circle_area(self):
        minr=999999999
        #find circle with smallest radius
        for c in self.circlesList:
            r=float(c[3])
            if r<minr:
                minr=r
        circle=Circle(self.origin,minr)
        #return area of circle with smallest radius
        return circle.area()

    def max_square_area(self):
        maxl=0
        #find square with largest length
        for s in self.squaresList:
            l=float(s[3])
            if l>maxl:
                maxl=l
        square=Square(self.origin,maxl)
        #return area of square with largest radius
        return square.area()

    def min_square_area(self):
        minl=999999999
        #find square with smallest length
        for s in self.squaresList:
            l=float(s[3])
            if l<minl:
                minl=l
        square=Square(self.origin,minl)
        #return area of square with smallest radius
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
        #sort list of circles by radius and then find median radius
        self.circlesList.sort(key=lambda x: x[3])
        medianLoc=math.floor(len(self.circlesList)/2)
        medianRadius=float(self.circlesList[medianLoc][3])
        #return circle area of median circle
        circle=Circle(self.origin, medianRadius)
        return circle.area()

    def median_square_area(self):
        #sort list of squares by radius and then find median radius
        self.squaresList.sort(key=lambda x: x[3])
        medianLoc=math.floor(len(self.squaresList)/2)
        medianLength=float(self.squaresList[medianLoc][3])
        #return square area of median circle
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


if __name__ == "__main__":
    #You should add your own code heere to test your work
    print ("=== Testing Part 2 ===")
    assignment = Assignment()
    #test=Test()
    #test.pTest()
    #test.cTest()
    #test.sTest()
    assignment.analyse("1000shapetest.data")
