def readcsv(filename):
    i=0
    A=[]
    try:
        with open(filename, "r") as txt:
            for line in txt:
                A.append(line.strip().split(','))
                i=i+1
    except IOError:
        print('wrong file name ')
    return (A)
