import pandas as pd
from os import listdir
import os
from os.path import isfile, join
import re
from selenium import webdriver
import traceback
from sklearn.feature_extraction.text import CountVectorizer
df = pd.DataFrame()
docs = [['why hello there', 'omg hello pony', 'she went there? omg why why'],['why hello there', 'omg hello pony', 'she went there? omg why why']]
mypath = "./Text"
folders = [join(mypath,f) for f in listdir(mypath) if not isfile(join(mypath, f))]
folders = [f for f in folders if f != ".git"]
speeches = [join(g,f) for g in folders for f in listdir(g)  if isfile(join(g, f)) and (not "links" in f and not "failed" in f and "git" not in f)]
i = 0
print(speeches)
for _file in speeches:
    print(_file)
    opened = open(_file,'r', encoding="utf8").readlines()
    labels = opened.pop(0)
    txt = [" ".join(opened),]
    vec = CountVectorizer()
    X = vec.fit_transform(txt)
    df_ = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
    print(labels.split("|"))
    df_['name'],df_['title'],df_['date'] = labels.split("|")
    df = df.append(df_).fillna(0)
print(df)
test = open('test.csv','w')
test.write(df.to_csv(index=False))