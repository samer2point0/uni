import IO

def differ():
    print("this is a function that computes the difference between two coloumns")
    A=[]
    f=input("enter the name of the file: ")
    Table=IO.readcsv(f)
    while True:
        try:
            col1=Table[0].index(input("enter the label of the first coloumn: "))
            col2=Table[0].index(input("enter the label of the second coloumn: "))
            break
        except TypeError:
            print("invalid coloumn label, maybe try again")

    ent=Table[0][0]

    for item in Table[1:]:
        A.append(abs(int(item[col1])-int(item[col2])))

    print ("the ", ent, " with the smallest difference is: ", Table[A.index(min(A))+1][0])

differ()
