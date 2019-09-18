from os import listdir
import os
from os.path import isfile, join
import re
from selenium import webdriver
import traceback
mypath = "./"
folders = [f for f in listdir(mypath) if not isfile(join(mypath, f))]
folders = [f for f in folders if f != ".git"]
speeches = [join(g,f) for g in folders for f in listdir(g)  if isfile(join(g, f))]
for _file in speeches:
    print(_file)
    txt = open(_file,'r').readlines()
    temp = []
    for line in txt:
        temp.append(re.sub("[\(\[].*?[\)\]]", "", line))
    with open(_file,'w') as replace:
        for line in temp:
            replace.write(f"{line}")

def getNumber(s,i=0):
    try:
        int(s[-1*(i+1)])
    except:
        return int(s[-1*i:])
    return getNumber(s,i+1)

