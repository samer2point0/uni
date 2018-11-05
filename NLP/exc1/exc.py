"""This is a program that analyses a news corpus and prints off some interesting stats"""

#First importing the neccassary modules for the program adn downloading nltk
import re
import jsonlines
import nltk
import os
import collections
import math
nltk.download()

#Saving lists of negative and positive words in global variables nWords and pWords respectively
with open('./signal-news1/opinion-lexicon-English/positive-words.txt', 'r') as pWF:
    pWords=pWF.read().split()
with open('./signal-news1/opinion-lexicon-English/negative-words.txt', 'r') as nWF:
    nWords=nWF.read().split()

"""Function prep takes a piece of text and removes urls, nonalphanumeric characters,
 numbers and all one lettter words and then returns the text"""
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

#Lemmatize takes a list of words and returns lemmatized version of text as a list
def lemmatize(text):
    wnl=nltk.WordNetLemmatizer()
    return [wnl.lemmatize(word) for word in text]

"""Function pVn takes a peice of text and counts the number of positive and negative words
 in it and stores the value in the pnCount dictionary, it also adds one to the number of positive
  articles if the total number of positive words was larger than negative words and vice versa"""
def pVn(pnCount,artText):
    PWs=0
    NWs=0
    #add number of positive words in article text to the PWs count
    for word in pWords:
        if word in artText:
            PWs=PWs+artText[word]
            del artText[word]
    #add number of negattive words in article text to the PWs count
    for word in nWords:
        if word in artText:
            NWs=NWs+artText[word]
    #edit the global variable pnCount by adding number of new positive and negative words seen
    pnCount['pCount']=pnCount['pCount']+PWs
    pnCount['nCount']=pnCount['nCount']+NWs

    #classify article into positive or negative and edit pnCount['pArticles'/'nArticles'] accordingly
    if(PWs>NWs):
        pnCount['pArticles']=pnCount['pArticles']+1
    elif(NWs>PWs):
        pnCount['nArticles']=pnCount['nArticles']+1

"""Function topTrigram takes a sorted list of trigrams and a bigram and returns the most
 likely trigram given the bigram based only on seen trigrams (no smoothing)"""
def topTrigram(trigrams, bigram):
    triList=[]
    tempTri=trigrams
    #Binary search for bigram in sorted trigrams list
    while True:
        #if more than 1 element left split list according to bigram possition
        if len(tempTri)>1 and tempTri[int(len(tempTri)/2)][0][:2] < bigram:
            tempTri=tempTri[int(len(tempTri)/2):]
        elif len(tempTri)>1 and tempTri[int(len(tempTri)/2)][0][:2] > bigram:
            tempTri=tempTri[:int(len(tempTri)/2)]
        #runs if bigram found or search exhausted
        else:
            #if bigram not found return None
            if len(tempTri)<1 or tempTri[int(len(tempTri)/2)][0][:2] != bigram:
                return None

            i,j=0,1
            #add all trigrams starting with bigram to the triList
            while int(len(tempTri)/2)-i>0 and tempTri[int(len(tempTri)/2)-i][0][:2]==bigram:
                triList.insert(0, tempTri[int(len(tempTri)/2)-i])
                i=i+1
            while int(len(tempTri)/2)+j<len(tempTri) and tempTri[int(len(tempTri)/2)+j][0][:2]==bigram:
                triList.append(tempTri[int(len(tempTri)/2)+j])
                j=j+1
            break

    #find the maximumm occuring trigram and return it
    topTri=max(triList, key=lambda x: x[1])[0]
    return topTri

"""finish sentence takes a sorted list of trigrams, an ngram and a sentence length(n) it uses a
trigram model to recursively find out the next most likely n words based on the trigrams seens so far"""
def finishSentence(trigrams, ngram, n):
    #find bigram out of sentence passed
    bigram=tuple(ngram.split()[-2:])
    topTri=topTrigram(trigrams,bigram)
    #if no trigram starting with bigram found return the sentence constructed so far
    if not topTri:
        return ngram
    #find most liekely next word and add it to sentence so far
    topWord=topTri[-1]
    ngram=ngram+' '+topWord

    #if the length of the sentence so far is less than n call finishSentence witht the new ngram
    if len(ngram.split())<n:
        sentence=finishSentence(trigrams, ngram, n)
    else:#if length of ngram is n return ngram
        sentence=ngram

    return sentence

"""Function preplexity takes list of trigrams and bigrams from training corpus and a list of
 trigrams from the test corpus and evaluates the preplexity using laplace smoothing and a
  second order markov assumption"""
def preplexity(trainTrigrams, trainBigrams, testTrigrams):
    ppxsum=0
    N=0
    V=len(trainBigrams)
    #trigramCount, bigramCount=0,0
    for trigram in testTrigrams:
        #find occurances of bigram in training data and adding V for laplace smoothing
        bigram=trigram[:2]
        try:
            bigramCount=trainBigrams[bigram]+V
        except (KeyError):
            bigramCount=V

        #find occurances of trigram in training data and adding 1 for laplace smoothing
        try:
            trigramCount=trainTrigrams[trigram]+1
        except (KeyError):
            trigramCount=1

        #calculate the probablity of each trigram and add it to sum
        prTriGivenBi=trigramCount/bigramCount
        #add no of time trigram occured in test data to total no of words
        testTriCount=testTrigrams[trigram]
        N=N+testTriCount
        #using log and addition to cope with very large numbers
        ppxsum=ppxsum+math.log(prTriGivenBi,2)*testTriCount

    #return the preplexity
    return pow(2,-ppxsum/N)


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
            del lemT, tempV

    #Count vocabulary size and token size and print them, then print total number of positive/negative words and positive negative articles
    vCount=len(set(T))
    tCount=len(T)
    print('vocabulary size is: ',vCount,'\ntoken size is: ', tCount)
    print('there are ',pnCount['nArticles'], 'negative articles', '\nthere are ',pnCount['pArticles'], 'positive articles')
    print('there are ',pnCount['nCount'], 'negative words', '\nthere are ',pnCount['pCount'], 'positive words')

    #sorts the trigrams by occurances and lists the top 25
    tri= collections.Counter(nltk.trigrams(T))
    topTri=sorted(tri.items(), key=lambda x: x[1], reverse=True)
    del tri
    print('the top 25 trigrams are: \n',topTri[:25])
    del topTri

    #lists the trigrams and bigrams of the training dataset and also the trigrams of the test corpus.
    #a sorted version of the training set trigrams(Sortedtri1) is then passed to the finishsentence function
    tri1=collections.Counter(nltk.trigrams(T[:breakFlag]))
    bi1=collections.Counter(nltk.bigrams(T[:breakFlag]))
    tri2=collections.Counter(nltk.trigrams(T[breakFlag:]))
    del T
    sortedTri1=sorted(tri1.items(), key=lambda x: x[0])
    print('the generated sentence starting with (is this) is:  ', finishSentence(sortedTri1, 'is this', 10))
    del sortedTri1

    #calculates the preplexity of the language model on the rest of the jsonlines rows, given trigrams and bigrams on test and trainign data
    print('the preplexity of the language model is: ', preplexity(tri1, bi1, tri2))
    del tri1, bi1, tri2
