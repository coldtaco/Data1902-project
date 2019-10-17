import pickle
import pandas as pd
import numpy
speeches = pickle.load(open('./wordVectorizedSpeechesTrump.pkl','rb'))
df = pd.read_csv('DTM.csv')
sums = df.sum()
sums = sums.drop(['Name','Date','Title'])
sumsd = sums[sums >= 5]
sums = sums.reset_index()
sums = sums.reset_index()
sums = sums.rename(columns={'level_0':'fullVecInd'})
sumsd = sumsd.reset_index()
sumsd = sumsd.reset_index()
sumsd = sumsd.rename(columns={'level_0':'pVecInd'})
convert = pd.merge(sums,sumsd,'left',on='index')
convert = convert.fillna(-1)
translate = dict(zip((convert['fullVecInd'].to_numpy()+1).tolist(),(convert['pVecInd'].to_numpy()+1).tolist()))
nConvert = pd.merge(sums,sumsd,'right',on='index')
newDict = dict(zip((nConvert['pVecInd'].to_numpy()+1).tolist(),convert['index'].tolist()))
countdown = 0
x = []
y = []
for s in speeches:
    s = [translate[w] for w in s]
    for data in zip(s[:-5],s[1:-4],s[2:-3],s[3:-2],s[4:-1],s[5:]):
        if 0 in data:
            continue
        x.append(data[0:5])
        y.append(data[5])
pickle.dump(x,open('trumpInput.pkl','wb'))
pickle.dump(y,open('trumpTarget.pkl','wb'))
pickle.dump(newDict,open('newTrumpDict.pkl','wb'))