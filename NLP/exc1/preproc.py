import re
import jsonlines
import nltk
import os

nltk.download()

os.system('rm ./text.txt')
os.system('rm ./preptext.txt')
os.system('touch ./text.txt')
os.system('touch ./preptext.txt')
TF=open('text.txt','r+')
procTF=open('preptext.txt','r+')

with open('./signal-news1/opinion-lexicon-English/positive-words.txt', 'r') as pWF:
    pWords=pWF.read().split()

with open('./signal-news1/opinion-lexicon-English/negative-words.txt', 'r') as nWF:
    nWords=nWF.read().split()

def readtextline(reader):
    json=reader.read()
    text=json['content']
    return text

def prep(text):
    urls=re.compile(r'http[\w\W]*\b')
    text=urls.sub('',text)
    nonalpha=re.compile(r'[^a-z0-9\s]+')
    text=nonalpha.sub('',text)
    num=re.compile(r'\b[0-9]+\b')
    text=num.sub('',text)
    short=re.compile(r'\b[0-9a-z]{1,3}\b')
    text=short.sub('',text)
    return text

def lemmatize(text):
    wnl=nltk.WordNetLemmatizer()
    return [wnl.lemmatize(word) for word in text]

def posVneg(pnCount,artText):
    PWs=0
    NWs=0
    for word in artText:
        if word in pWords:
            PWs=PWs+1
        elif word in nWords:
            NWs=NWs+1

    pnCount['pCount']=pnCount['pCount']+PWs
    pnCount['nCount']=pnCount['nCount']+NWs
    if(PWs>NWs):
        pnCount['pArticles']=pnCount['pArticles']+1
    elif(NWs>PWs):
        pnCount['nArticles']=pnCount['nArticles']+1
    return pnCount


pnCount={'pArticles':0,'nArticles':0, 'pCount':0, 'nCount':0}
with jsonlines.open('./signal-news1/signal-news1.jsonl', 'r') as reader:
    for line in reader:
        text=line['content'].lower()

        proctext=prep(text).split()
        lemT=lemmatize(proctext)
        pnCount=posVneg(pnCount,lemT)
        print('*')
        #output to files
        TF.write(text)
        procTF.write(' '.join(lemT))

print('*****')
TF.close()
procTF.seek(0)
T=procTF.read()
procTF.close()

Tlist=T.split()
del T, lemT, text
tCount=len(Tlist)
V=set(Tlist)
vCount=len(V)

trigram_measures= nltk.collocations.TrigramAssocMeasures()
finder = nltk.TrigramCollocationFinder.from_words(Tlist)
print(sorted(finder.nbest(trigram_measures.raw_freq, 25)))
print(pnCount)
print(vCount, tCount)
