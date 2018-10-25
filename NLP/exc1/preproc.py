import re
import jsonlines
import nltk
import os

nltk.download()

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
    return ' '.join([wnl.lemmatize(word) for word in text])


os.system('rm ./text.txt')
os.system('rm ./preptext.txt')
os.system('touch ./text.txt')
os.system('touch ./preptext.txt')
TF=open('text.txt','r+')
procTF=open('preptext.txt','r+')

with jsonlines.open('./signal-news1.jsonl', 'r') as reader:


    for line in reader:
        text=line['content'].lower()

        proctext=prep(text).split()
        lemT=lemmatize(proctext)
        #output to files
        TF.write(text)
        procTF.write(lemT)


    #close files
TF.close()
T=procTF.read()
Tlist=T.split()
procTF.close()
tCount=len(Tlist)
vCount=len(set(Tlist))

trigram_measures= nltk.collocations.TrigramAssocMeasures()
finder = nltk.TrigramCollocationFinder.from_words(T)
print(sorted(finder.nbest(trigram_measures.raw_freq, 25)))

print(vCount, tCount)
