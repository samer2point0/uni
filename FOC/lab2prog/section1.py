import IO
A=[]
Table=IO.readcsv("football.csv")
for item in Table[1:]:
    A.append(abs(int(item[5])-int(item[6])))

print ("the team with the smallest team difference is: ", Table[A.index(min(A))+1][0])
