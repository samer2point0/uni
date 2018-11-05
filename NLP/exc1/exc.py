import re
import jsonlines
import nltk
import os
import collections
import math
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

def topTrigram(trigrams, bigram):
    triList=[]
    tempTri=trigrams
    while True:
        if len(tempTri)>1 and tempTri[int(len(tempTri)/2)][0][:2] < bigram:
            tempTri=tempTri[int(len(tempTri)/2):]
        elif len(tempTri)>1 and tempTri[int(len(tempTri)/2)][0][:2] > bigram:
            tempTri=tempTri[:int(len(tempTri)/2)]
        else:
            if len(tempTri)<1 or tempTri[int(len(tempTri)/2)][0][:2] != bigram:
                return None

            i,j=0,1
            while int(len(tempTri)/2)-i>0 and tempTri[int(len(tempTri)/2)-i][0][:2]==bigram:
                triList.insert(0, tempTri[int(len(tempTri)/2)-i])
                i=i+1
            while int(len(tempTri)/2)+j<len(tempTri) and tempTri[int(len(tempTri)/2)+j][0][:2]==bigram:
                triList.append(tempTri[int(len(tempTri)/2)+j])
                j=j+1
            break

    topTri=max(triList, key=lambda x: x[1])[0]
    return topTri

def finishSentence(trigrams, ngram, n):
    bigram=tuple(ngram.split()[-2:])
    topTri=topTrigram(trigrams,bigram)
    if not topTri:
        return ngram
    topWord=topTri[-1]
    ngram=ngram+' '+topWord

    if len(ngram.split())<n:
        sentence=finishSentence(trigrams, ngram, n)
    else:
        sentence=ngram

    return sentence


def preplexity(trainTrigrams, trainBigrams, testTrigrams):
    ppx=1
    N=0
    V=len(trainBigrams)
    #trigramCount, bigramCount=0,0
    for trigram in testTrigrams:
        #find occurances of bigram in training data and adding V and 1 for laplace smoothing
        bigram=trigram[:2]
        try:
            bigramCount=trainBigrams[bigram]+V
        except (KeyError):
            bigramCount=V

        try:
            trigramCount=trainTrigrams[trigram]+1
        except (KeyError):
            trigramCount=1

        prTriGivenBi=trigramCount/bigramCount
        testTriCount=testTrigrams[trigram]
        N=N+testTriCount
        ppx=ppx+math.log(prTriGivenBi,2)*testTriCount

    return pow(2,-ppx/N)


if __name__=='__main__':
    #initialising variables
    #pnCount dictionary saves the number of negative/positive words and articles
    pnCount={'pArticles':0,'nArticles':0, 'nCount':0, 'pCount':0}
    T,V=[],[]
    breakFlag=0
    i=0

    #reading from file formatting it and storing it in T
    with jsonlines.open('./signal-news1/signal-news1.jsonl', 'r') as reader:
        for line in reader:
            i=i+1
            text=line['content'].lower()

            #preocess text, lemmatize it and add it ot list
            proctext=prep(text).split()
            del text
            lemT=lemmatize(proctext)
            del proctext
            T.extend(lemT)

            #flag to deperate first 16000 line from test corpus
            if(i==16000):
                breakFlag=len(T)

            #create temporary article vocabulary and pass it to pVn that counts positive vs negative words and artcles
            tempV=collections.Counter(lemT)
            pVn(pnCount,tempV)
            del lemT


    vCount=len(set(T))
    tCount=len(T)
    print('vocabulary size is: ',vCount,'\ntoken size is: ', tCount)
    print('there are ',pnCount['nArticles'], 'negative articles', '\nthere are ',pnCount['pArticles'], 'positive articles')
    print('there are ',pnCount['nCount'], 'negative words', '\nthere are ',pnCount['pCount'], 'positive words')

    tri= collections.Counter(nltk.trigrams(T))
    topTri=sorted(tri.items(), key=lambda x: x[1], reverse=True)
    del tri
    print('the top 25 trigrams are: \n',topTri[:25])
    del topTri

    tri1=collections.Counter(nltk.trigrams(T[:breakFlag]))
    bi1=collections.Counter(nltk.bigrams(T[:breakFlag]))
    tri2=collections.Counter(nltk.trigrams(T[breakFlag:]))
    del T
    sortedTri1=sorted(tri1.items(), key=lambda x: x[0])
    print('the generated sentence starting with (is this) is:  ', finishSentence(sortedTri1, 'is this', 10))
    del sortedTri1

    print('the preplexity of the language model is: ', preplexity(tri1, bi1, tri2))
    del tri1, bi1, tri2




#
