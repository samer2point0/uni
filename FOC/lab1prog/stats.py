def getList():
    print('enter as many numbers as you luck and then type \"done\" to get some interesting stats  ')
    i=0
    A=list()
    while True: #woooooo dude ar eyou trying to get us stuck?
        entry=input()
        if entry=='stop' or entry=='Stop':
            return A
        try:
            A.append(int(entry))
        except ValueError:
            print('dude! invalid entry, try again  ')


A=getList()
print('maximun number is: ', max(A))
print('minimum number is: ', min(A))
print('the mean is : ', sum(A)/len(A))
