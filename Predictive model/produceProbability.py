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
#Lemmatizes each sentence and inserts it into Document term matrix
for _file in tqdm(speeches):
    try:
        opened = open(_file,'r', encoding="utf8").readlines()
        labels = opened.pop(0)
        txt = [" ".join(opened)]
        vec = CountVectorizer(token_pattern=u"(?u)\\b\\w+\\b",ngram_range=(2,2))
        X = vec.fit_transform(txt)
        df_ = pd.DataFrame(np.array(X.toarray(),dtype='int32'), columns=vec.get_feature_names())
        labs = labels.split("|")
        df_['Name'],df_['Title'],df_['Date'] = labs[0],labs[1],labs[2]
        df = df.append(df_,sort=True).fillna(0)
    except:
        print(_file)
        traceback.print_exc()
        continue
pickle.dump(df,open('pairTDM.pkl','wb'))

counts = df
counts = counts[counts["Name"]=='Donald Trump']
counts.drop(['Date','Name','Title'],axis=1)
sums = counts.sum().reset_index()
pairs = sums['index']
print(pairs)
dic = {}
for pair in pairs:
    front,back = pair.split()
    if front not in dic:
        dic[front] = {back : None}
    dic[front][back] = sums[pair]
pickle.dump(dic,open('probabilityDict.pkl','wb'))