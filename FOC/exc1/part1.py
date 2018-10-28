"""This module should filter and sort uk phone numbers from the text file provided. """
import re

def isValid(num): #returns true if the passed number starts with 44 and has 12 numbers
    if  len(num)==12 and num[:2]=='44':
        return True
    else:
        return False

def formatNum(num): #44XXXXXXXXXX => 0XXXX XXXXXX
    return '0'+num[2:6]+' '+num[6:]


if __name__ == "__main__":
    #file read
    nF= open('phone_log.txt','r')
    log=nF.read()
    nF.close()
    #remove alphabet characters and spaces and puts them in a list
    regEx=re.compile(r'[a-z]+|[\s]+',re.I)
    log=regEx.sub( '', log)
    nList=log.split('+')

    validList=[]
    #going through numbers list and creating a new list with only valid numbers with the right format
    for num in nList:
        if isValid(num):
            validList.append(formatNum(num))

    validList.sort()
    for num in validList:
        print(num)
