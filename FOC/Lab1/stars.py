def incstars(n,mode='f'):
    if mode=='r':
        for x in range(0,n):
            print('*'*(n-x))
    else :
        for x in range(0,n):
            print('*'*(x+1))

num=int(input("enter number of stars:  "))
incstars(num)
incstars(num,'r')
