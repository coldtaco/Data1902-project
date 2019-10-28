import pandas as pd
from os import listdir
import os
from os.path import isfile, join
import re
import traceback
import numpy as np
import pickle
from tqdm import tqdm
#if change to false if unlemma'd form is desired
#Gets all the files in their folders and excludes unwanted ones
mypath = "./Text"
folders = [join(mypath,f) for f in listdir(mypath) if not isfile(join(mypath, f))]
folders = [f for f in folders if f != ".git"]
speeches = [join(g,f) for g in folders for f in listdir(g)  if isfile(join(g, f)) and (not "links" in f and not "failed" in f and "git" not in f)]

def getWordVector(name,df):
    df = df[df['Name']==name]
    df = df.drop(['Date','Title','Name'],axis=1)
    sums = df.sum()
    sums = sums[sums > 0].reset_index()['index'].tolist()
    sums = [s for s in sums if not re.search('[0-9]',s)]
    dictionary  = {}
    rdict = {}
    print(len(sums))
    for i,x in enumerate(sums):
        dictionary[x.lower()] = i+1
        rdict[str(i+1)] = x.lower()
    dictionary['.'] = len(dictionary)+1
    rdict[len(dictionary)+1] = x.lower()
    dictionary[','] = len(dictionary)+2
    rdict[len(dictionary)+2] = x.lower()
    open('vectorLength.txt','a').write(f'{name},{len(dictionary)}')
    pickle.dump(dictionary,open(f'{name} dict.pkl','wb'))
    pickle.dump(rdict,open(f'{name} rdict.pkl','wb'))
    return dictionary

def vectorize(directory,dictionary):
    vSpeech = []
    speeches = [join(directory,f) for f in listdir(directory)  if isfile(join(directory, f)) and (not "links" in f and not "failed" in f and "git" not in f)]
    for s in tqdm(speeches):
        speech = open(s,'r',encoding='UTF-8').readlines()
        speech.pop(0)
        speech = [line.replace('.',' .') for line in speech]
        speech = [line.replace(',',' ,') for line in speech]
        speech = [line.replace('-',' ') for line in speech]
        vectorized = []
        for line in speech:
            for word in line.strip().split(' '):
                if word.isalpha():
                    vectorized.append(dictionary[word.lower()])
        vSpeech.append(vectorized)
    return vSpeech

DTM = pd.read_csv('DTM.csv',encoding='UTF-8')

with open('wordVectorizedSpeechesTrump.pkl', 'wb') as f:
        pickle.dump(vectorize('./Text/Trump speeches', getWordVector('Donald Trump',DTM)),f)

with open('wordVectorizedSpeechesScomo.pkl', 'wb') as f:
        pickle.dump(vectorize('./Text/Scomo speeches', getWordVector('Scott Morrison',DTM)),f)

with open('wordVectorizedSpeechesMay.pkl', 'wb') as f:
        pickle.dump(vectorize('./Text/May speeches', getWordVector('Theresa May',DTM)),f)