import re
import jsonlines
import nltk
import os
import collections
nltk.download()

with open('./signal-news1/opinion-lexicon-English/positive-words.txt', 'r') as pWF:
    pWords=pWF.read().split()
with open('./signal-news1/opinion-lexicon-English/negative-words.txt', 'r') as nWF:
    nWords=nWF.read().split()


def prep(text):
    urls=re.compile(r'http[\w\W]*\b')
    text=urls.sub('',text)
    nonalpha=re.compile(r'[^a-z0-9\s]+')
    text=nonalpha.sub('',text)
    num=re.compile(r'\b[0-9]+\b')
    text=num.sub('',text)
    short=re.compile(r'\b[a-z]{1}\b')
    text=short.sub('',text)
    return text

def lemmatize(text):
    wnl=nltk.WordNetLemmatizer()
    return [wnl.lemmatize(word) for word in text]

def pVn(pnCount,artText):
    PWs=0
    NWs=0
    for word in pWords:
        if word in artText:
            PWs=PWs+artText[word]
            del artText[word]
    for word in nWords:
        if word in artText:
            NWs=NWs+artText[word]

    pnCount['pCount']=pnCount['pCount']+PWs
    pnCount['nCount']=pnCount['nCount']+NWs
    if(PWs>NWs):
        pnCount['pArticles']=pnCount['pArticles']+1
    elif(NWs>PWs):
        pnCount['nArticles']=pnCount['nArticles']+1
    return pnCount


pnCount={'pArticles':0,'nArticles':0, 'nCount':0, 'pCount':0}
T,V=[],[]
breakFlag=0
with jsonlines.open('./signal-news1/signal-news1.jsonl', 'r') as reader:
    i=0
    for line in reader:
        i=i+1
        text=line['content'].lower()

        #preocess text and lemmatize it and add it ot list
        proctext=prep(text).split()
        del text
        lemT=lemmatize(proctext)
        del proctext

        print(i)
        T.extend(lemT)
        if(i==160):
            breakFlag=len(T)

        tempV=collections.Counter(lemT)
        del lemT
        pnCount=pVn(pnCount,tempV)

        if(i==200):
            break

vCount=len(set(T))
tCount=len(T)
print(vCount, tCount)
print(pnCount)

V1=collections.Counter(T[:breakFlag])
tri= collections.Counter(nltk.util.ngrams(T,3))

topTri=sorted(tri.items(), key=lambda x: x[1])
print(topTri[-25:])

#sortedTri1=removeTri2(tri,tri2)

V2=set(T2)
