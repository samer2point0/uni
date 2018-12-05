#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import testsets
import evaluation
import re
import jsonlines
import nltk
import os
import collections
import math
nltk.download()

def prep(text):
    username=re.compile(r'@[^\s]+\b')
    text=username.sub('usrmntn',text)
    urls=re.compile(r'http[^\s]+\b',)
    text=urls.sub('urllink',text)
    nonalpha=re.compile(r'[^a-z0-9\s]+')
    text=nonalpha.sub('',text)
    num=re.compile(r'\b[0-9]+\b')
    text=num.sub('',text)
    #short=re.compile(r'\b[a-z]{1}\b')
    #text=short.sub('',text)
    return text

#Lemmatize takes a list of words and returns lemmatized version of text as a list
def lemmatize(text):
    wnl=nltk.WordNetLemmatizer()
    return [wnl.lemmatize(word) for word in text]

def readFile(path):
    dict={}
    with open(path, 'r') as reader:
        for line in reader:
            line=line.split('\t')
            text=prep(line[2].lower().strip())
            dict[line[0]]={'tag':line[1],'text':text}
    return dict

devDict=readFile('./semeval-tweets/twitter-dev-data.txt')
print(devDict)

for classifier in ['myclassifier1', 'myclassifier2', 'myclassifier3']: # You may rename the names of the classifiers to something more descriptive
    if classifier == 'myclassifier1':
        print('Training ' + classifier)
        # TODO: extract features for training classifier1
        # TODO: train sentiment classifier1
    elif classifier == 'myclassifier2':
        print('Training ' + classifier)
        # TODO: extract features for training classifier2
        # TODO: train sentiment classifier2
    elif classifier == 'myclassifier3':
        print('Training ' + classifier)
        # TODO: extract features for training classifier3
        # TODO: train sentiment classifier3

    for testset in testsets.testsets:
        # TODO: classify tweets in test set

        predictions = {'163361196206957578': 'neutral', '768006053969268950': 'neutral', '742616104384772304': 'neutral', '102313285628711403': 'neutral', '653274888624828198': 'neutral'} # TODO: Remove this line, 'predictions' should be populated with the outputs of your classifier
        evaluation.evaluate(predictions, testset, classifier)

        evaluation.confusion(predictions, testset, classifier)
