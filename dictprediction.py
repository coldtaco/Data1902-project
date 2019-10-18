import pickle
import random
dic = pickle.load(open('probabilityDict.pkl','rb'))
def getHighest(word):
    highestPair = (list(dic[word].keys())[0],dic[word][list(dic[word].keys())[0]])
    return list(dic[word].keys())[random.randint(0,len(dic[word])-1)]
    for x in dic[word]:
        if dic[word][x] > highestPair[1]:
            highestPair = (x,dic[word][x])
    return highestPair[0]
while True:
    taken = input('enter a word')
    sentence = []
    if taken not in dic:
        print('not in dict')
        continue
    try:
        num = int(input('how many words?'))
    except ValueError:
        print('not a number')
        continue
    for i in range(num):
        sentence.append(taken)
        taken = getHighest(taken)
    print(" ".join(sentence))