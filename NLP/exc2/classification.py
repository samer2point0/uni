
#importing neccessary libraries, numpy, scipy, regex, nltk, pickle, gensim, sklearn
import testsets
import evaluation
import numpy as np
from scipy import spatial as SP
import re
import nltk
import pickle
from gensim.models.keyedvectors import KeyedVectors
from gensim.models import Word2Vec
from sklearn import linear_model, pipeline, preprocessing, svm, neighbors,tree

#nltk.download()

#reading the positive and negative lexicons provided by uci and saving them to pWrods and nWords lists
with open('./positive-words.txt', 'r') as pWF:
    pWords=pWF.read().split()
with open('./negative-words.txt', 'r') as nWF:
    nWords=nWF.read().split()

#the prep function takes in the tweet text, preprocesses and returns a list containing lemmatised words
def prep(text):
    #remove usernames and urls
    username=re.compile(r'@[^\s]+\b')
    text=username.sub('',text)
    urls=re.compile(r'http[^\s]+\b',)
    text=urls.sub('',text)
    #remove nonalphanumeric charecters and numbers
    nonalpha=re.compile(r'[^a-z0-9\s]+')
    text=nonalpha.sub('',text)
    num=re.compile(r'\b[0-9]+\b')
    text=num.sub('',text)
    #remove stopwords
    stopwords=nltk.corpus.stopwords.words('english')
    #create and return finished list
    textList=text.split()
    textList=[word for word in textList if not word in stopwords]
    return textList

#Lemmatize takes a list of words and returns lemmatized version of text as a list using the wnl lemmatiser
def lemmatize(text):
    wnl=nltk.WordNetLemmatizer()
    return [wnl.lemmatize(word) for word in text]

#function readFile reads the tweet data and returns a dictionary containing each tweet with the id as key
def readFile(path):
    dict={}
    with open(path, 'r') as reader:
        for line in reader:
            line=line.split('\t')
            #lemmatize and preprocess text
            textList=lemmatize(prep(line[2].strip().lower()))
            dict[line[0]]={'tag':line[1],'text':textList}
    return dict

#pvnWords takes list of words and returns the number of positive words minus negative words
def pvnWords(tList):
    pnCount=0
    for word in tList:
        if word in pWords:
            pnCount=pnCount+1
        elif word in nWords:
            pnCount=pnCount-1
    return pnCount

#tweetVectors takes a words list and returns the summation of all the w2vec of the words
def tweetVectors(tList):
    w2v=glove['neutral']
    for word in tList:
        try:
            w2v=np.add(w2v,glove[word])
        except KeyError:
            #if words not in dictionary skip it
            pass
    return w2v

#takes a w2vector and a list of w2vectors and computes the cosine similarity between each one
def cosSim(tweetV,ref):
    sim=[]
    for word in ref:
        sim.append(SP.distance.cosine(tweetV,word))
    return sim

#Takes Dictionary of all tweets and returns an array of features depending on the classifier being used
def featureExtract(Dict, classif):
    #initialise contants
    fDict={'ids':[],'pnCounts':[],'tweetVec':[],'tags':[], 'wordsNo':[], 'tweetSim':[]}
    l=len(Dict.keys())
    #reference list of words representing positive and negative words
    ref=[tweetVectors(['excellent','happy', 'love']),tweetVectors(['terrible','angry','hate'])]

    #for each tweet in thte dictionary add the neccessary features in order to the appropriate list
    for key,tweet in Dict.items():
        text=tweet['text']
        fDict['ids'].append(key)
        fDict['tags'].append(tweet['tag'])
        fDict['pnCounts'].append(pvnWords(text))
        #the first classifier only requires the items collected so far so skip rest
        if(classif=='lexiconClass'):
            continue
        fDict['wordsNo'].append(len(text)/10)
        tweetv=tweetVectors(text)
        fDict['tweetVec'].append(tweetv.tolist())
        fDict['tweetSim'].append(cosSim(tweetv, ref))

    y=np.asarray(fDict['tags'])#output array
    fDict['pnCounts']=np.asarray(fDict['pnCounts']).reshape(l,1)#list of positive-negative words for each tweet
    #return features require by classifier 1 for traingin or predictions
    if(classif=='lexiconClass'):
        x=fDict['pnCounts']
        return fDict['ids'],x,y
    fDict['wordsNo']=np.asarray(fDict['wordsNo']).reshape(l,1)#no of words in each tweet
    #fDict['tweetVec'] is an array containing the summed w2vecs for each word in each tweet
    fDict['tweetVec']=preprocessing.normalize(np.asarray(fDict['tweetVec']).reshape(l,50))
    #fDict['tweetSim'] contains the list of similarity of tweetVectors and reference lists of postivie or negative words
    fDict['tweetSim']=preprocessing.normalize(np.asarray(fDict['tweetSim']).reshape(l,2))

    #return features require by classifier 2,3 for traingin or predictions
    if(classif=='cosSimDT'):
        x=np.concatenate((fDict['tweetSim'],fDict['wordsNo']),axis=1)
    elif(classif=='hierarchicalDT'):
        x=fDict['tweetVec']#np.concatenate((fDict['tweetVec'], fDict['wordsNo']),axis=1)

    return fDict['ids'],x,y

#lexiconClassifier takes the positive minus negative words of tweet and returns a list of predicted tags
def lexiconClassifier(pvn):
    predictions=[]
    for pnCount in np.nditer(pvn):
        if(pnCount >0):
            predictions.append('positive')
        elif(pnCount <0):
            predictions.append('negative')
        #only neutral when no of positive words equal negative words
        else:
            predictions.append('neutral')
    return predictions

#a function that takes in two classifiers and an input array and returns the predicted output
def hier(KNN,logreg,DT,x):

    y1=KNN.predict_proba(x)#predict objective vs subjective
    l=int(y1.size/2)
    print(y1)
    y2=logreg.predict_proba(x)#predict negative vs positive

    y=DT.predict(np.concatenate((y1,y2),axis=1))#from the probabilities predict the final output

    return y

def formatglove(filename='glove.twitter.27B.50d.txt'):
    return KeyedVectors.load_word2vec_format("gensim_vectors_50d.txt", binary=False)

#uncomment line below if reading glove.twitter.27B.50d.txt and edit file name if not the smae
#glove=formatglove()
#reading glove vectors dictionary using pickle
vecFile=open('keyedVectors_50d.txt','rb')
glove=pickle.load(vecFile)
vecFile.close()
#reading data and saving it to trainDict
trainDict=readFile('./twitter-training-data.txt')


for classifier in ['hierarchicalDT']:#'lexiconClass','cosSimDT',
    if classifier == 'lexiconClass':
        print('Training ' + classifier)
        """this classifier uses a simple lexicon counting approach"""
        #classify fucntion contains the current classifier
        classify=lambda **kwargs: dict(zip(kwargs['ids'],lexiconClassifier(kwargs['x'])))

    elif classifier == 'cosSimDT':
        print('Training ' + classifier)
        """this classifier uses the similarity between the tweet vectors and two reference vectors and
        uses a decision tree to classify features"""
        ids,x,y=featureExtract(trainDict, classifier)
        #build decision tree and train the decision tree
        #the commoneted code bellow shows the steps used to geenerate the pickle object being laoded
        """
        DT=tree.DecisionTreeClassifier(min_samples_leaf=100)
        DT.fit(x,y)
        classFile=open('cosSimDT.txt','wb')
        pickle.dump(DT,classFile)
        classFile.close()
        """

        classFile=open('cosSimDT.txt','rb')
        DT=pickle.load(classFile)

        classify=lambda **kwargs: dict(zip(kwargs['ids'],DT.predict(kwargs['x']).tolist()))


    elif classifier == 'hierarchicalDT':
        print('Training ' + classifier)
        """this classifief consists of three classifiers. A nearest neighbor clsssifier is used to predict
        wether the tweet is objective or subjective, a logistic regression model to detect wether it's
        positive or negative and a decision tree that takes the probabilities outputed form the previous
        classifier and decideds the final output"""

        ids, x,y=featureExtract(trainDict, classifier)

        #the commoneted code bellow shows the steps used to geenerate the pickle object being laoded

        """
        #format output from positive and negative to subjective for the knn classifier and then fit it
        y1=np.asarray(' '.join(y).replace('positive','subjective').split())
        y1=np.asarray(' '.join(y1).replace('negative','subjective').split())
        KNN=neighbors.KNeighborsClassifier(n_neighbors=30,weights='distance')
        KNN.fit(x,y1)


        ytemp,xtemp=[],[]
        j=0
        #filter only the subjective samples to train the logistic regression classifier and then fit it
        for i in range(y.size):
            if y1[i]=='subjective':
                j=j+1
                ytemp.append(y[i])
                xtemp.append(x[i,:].tolist())
        y2=np.asarray(ytemp)
        x2=np.asarray(xtemp).reshape(j,50)
        logreg=linear_model.LogisticRegression(solver='lbfgs', multi_class='ovr', max_iter=1000)
        logreg.fit(x2,y2)

        #predict the probabilities of each class for the two classifiers above
        proba1,proba2,=KNN.predict_proba(x),logreg.predict_proba(x)
        proba=np.concatenate((proba1,proba2),axis=1)
        #initialise and train the decsion tree on the probabilities of the previous classifiers
        DT=tree.DecisionTreeClassifier(max_depth=4)#min_samples_leaf=100)
        DT.fit(proba,y)


        model=[KNN,logreg,DT]
        classFile=open('hierarchicalDT.txt','wb')
        pickle.dump(model,classFile)
        classFile.close()
        """

        classFile=open('hierarchicalDT.txt','rb')
        model=pickle.load(classFile)
        KNN=model[0]
        logreg=model[1]
        DT=model[2]


        classify=lambda **kwargs: dict(zip(kwargs['ids'],hier(KNN, logreg, DT,kwargs['x'])))


    for testset in testsets.testsets:
        # TODO: classify tweets in test set
        ids,x,y=featureExtract(readFile(testset),classifier)

        predictions=classify(ids=ids,x=x)

        evaluation.evaluate(predictions, testset, classifier)

        evaluation.confusion(predictions, testset, classifier)
