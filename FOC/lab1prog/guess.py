from random import randint
n=None
while(n==None):
    key=input("enter e/E for easy, m/M for medium or h/H for hard diffuculty  ")
    if key=='e' or key=='E':
        n=5;
    elif  key=='m' or key=='M':
        n=10
    elif key=='h' or key=='H':
        n=100
    else:
        print("invalid entry mate!  ")

randnum= randint(0,n)
num=int(input("Can you guess what number am I thinking of?  "))
while(num != randnum):
    if(num<randnum):
        num=int(input("Too low, try again:  "))
    else:
        num=int(input("Too high, try again:  "))
print("yaaaas mate!")
