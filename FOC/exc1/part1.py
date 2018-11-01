"""This module should filter and sort uk phone numbers from the text file provided. """
import re

def isValid(num): #returns true if the passed number starts with 44 and has 12 numbers
    if  len(num)==12 and num[:2]=='44':
        return True
    else:
        return False

def formatNum(num): #transform number formats from 44XXXXXXXXXX => 0XXXX XXXXXX
    return '0'+num[2:6]+' '+num[6:]


if __name__ == "__main__":
    #file read
    nF= open('phone_log.txt','r')
    log=nF.read()
    nF.close()

    #use regex to remove alphabet characters and spaces
    regEx=re.compile(r'[a-z]+|[\s]+',re.I)
    log=regEx.sub( '', log)
    #given every numbr starts with + split the numbers on +
    nList=log.split('+')

    validList=[]
    #going through the nList and creating a new list (validList) with only valid numbers with the right format
    for num in nList:
        if isValid(num):
            validList.append(formatNum(num))

    #sort the list and print numbers
    validList.sort()
    for num in validList:
        print(num)
