import pickle
import numpy as np
def predict(model,inp,length):
    dic = pickle.load(open('newTrumpDict.pkl','rb'))
    rdic = pickle.load(open('newTrumprDict.pkl','rb'))
    intake = []
    for word in inp.split(" "):
        if not word in rdic:
            print(word)
            print('not in dict')
            return
        intake.append(rdic[word])
    for n in range(length):
        prediction = model.predict_classes(np.array(intake))[0]
        intake.append(prediction)
        print(prediction)
    intake = " ".join([dic[x] for x in intake])
    print(intake)
    return  