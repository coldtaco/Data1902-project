import pickle
import tensorflow as tf
import keras
import pandas as pd
import numpy as np

x = pickle.load(open('trumpInput.pkl','rb'))
y = pickle.load(open('trumpTarget.pkl','rb'))
vocab = len(pickle.load(open('newTrumpDict.pkl','rb'))) + 1
model = keras.Sequential()
model.add(keras.layers.Embedding(vocab,512))
model.add(keras.layers.LSTM(512,return_sequences=True))
model.add(keras.layers.LSTM(1024))
model.add(keras.layers.Dropout(0.2))
model.add(keras.layers.Dense(vocab,activation='softmax'))
model.compile('adam',loss='categorical_crossentropy', metrics=['accuracy'])
earlyStop = keras.callbacks.EarlyStopping(monitor='loss', min_delta=0.001, patience=9, verbose=0, mode='min', baseline=None, restore_best_weights=True)
rlr = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2,patience=7, min_lr=1e-6, mode='auto', verbose=1)

def getInpOut(ind):
    if (ind+1)*500 > len(x):
        return (x[500*ind:],y[500*ind:])
    return (x[500*ind:500*(ind+1)],y[500*ind:500*(ind+1)])

for i in range(x//500 +1):
    x,y = getInpOut(i)
    y = keras.utils.to_categorical(y,num_classes=vocab)
    model.fit(x,y,validation_split=0.10, epochs=1000, batch_size=32, verbose=2,callbacks=[earlyStop,rlr])
model.save('trump.h5')