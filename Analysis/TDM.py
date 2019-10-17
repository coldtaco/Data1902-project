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
from paragraphLemma import lemmaS
import numpy as np

#if change to false if unlemma'd form is desired
lemma = False
print(f'lemma = {lemma}')
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
        if lemma:
            txt = [" ".join(lemmaS(opened))]
        else:
            txt = [" ".join(opened)]
        vec = CountVectorizer(token_pattern=u"(?u)\\b\\w+\\b")
        X = vec.fit_transform(txt)
        df_ = pd.DataFrame(np.array(X.toarray(),dtype='int32'), columns=vec.get_feature_names())
        labs = labels.split("|")
        df_['Name'],df_['Title'],df_['Date'] = labs[0],labs[1],labs[2]
        df = df.append(df_,sort=True).fillna(0)
    except:
        print(_file)
        traceback.print_exc()
        continue
'''print(df)
cols = list(df.columns)
cols = [x for x in cols if not re.search("[0-9]",x)]'''
#Removes occurances of words < 5
'''
sums = df.sum()
sums = sums.drop(['Date','Title','Name'])
sums = sums[sums > 5].reset_index()['index'].tolist()
sums += ['Date','Title','Name']
df = df.loc[:,sums]'''

test = open(f'./DTM{"lemma"if lemma else ""}.csv','w',encoding='UTF-8')
test.write(df.to_csv(index=False))
test.close()