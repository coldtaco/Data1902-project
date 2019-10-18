import pandas as pd
from os import listdir
import os
from os.path import isfile, join
import re
from selenium import webdriver
import traceback
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from tqdm import tqdm
import numpy as np
import pickle
df = pd.DataFrame()
#Gets all the files in their folders and excludes unwanted ones
mypath = "./Text"
folders = [join(mypath,f) for f in listdir(mypath) if not isfile(join(mypath, f))]
folders = [f for f in folders if f != ".git"]
speeches = [join(g,f) for g in folders for f in listdir(g)  if isfile(join(g, f)) and (not "links" in f and not "failed" in f and "git" not in f)]
i = 0
probabilityDict = {}
#Lemmatizes each sentence and inserts it into Document term matrix
for _file in tqdm(speeches):
    try:
        opened = open(_file,'r', encoding="utf8").readlines()
        labels = opened.pop(0).split("|")
        if labels[0] == 'Donald Trump':
            txt = " ".join(opened)
            txt = txt.replace('.',' .')
            txt = txt.replace(',',' ,')
            txt = txt.replace('-',' ')
            txt = txt.replace('  ',' ')
            txt = txt.replace('"','')
            txt = txt.replace("'",'')
            txt = txt.replace('\n','')
            for front,back in zip(txt.split(" ")[0:-1],txt.split(" ")[1:]):
                front,back = front.lower(),back.lower()
                if not front in probabilityDict:
                    probabilityDict[front] = {back:0}
                if not back in probabilityDict[front]:
                    probabilityDict[front] = {back:0}
                probabilityDict[front][back] += 1
    except:
        print(_file)
        traceback.print_exc()
        continue

for key in probabilityDict:
    toBeRemoved = []
    for key2 in probabilityDict[key]:
        if probabilityDict[key][key2] < 5:
            toBeRemoved.append(key2)
    for r in toBeRemoved:
        del probabilityDict[key][r]
pickle.dump(probabilityDict,open('probabilityDict.pkl','wb'))