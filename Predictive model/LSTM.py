import pickle
import tensorflow as tf
import keras
import pandas as pd
import numpy as np
import traceback
import datetime
import gc

intake = pickle.load(open('trumpInput.pkl','rb'))
target = pickle.load(open('trumpTarget.pkl','rb'))
vocab = len(pickle.load(open('newTrumpDict.pkl','rb'))) + 1
try:
    model = keras.models.load_model('trump.h5')
    print('load model successful')
except:
    model = keras.Sequential()
    model.add(keras.layers.Embedding(vocab,512))
    model.add(keras.layers.LSTM(512,return_sequences=True))
    model.add(keras.layers.LSTM(512,return_sequences=True))
    model.add(keras.layers.LSTM(1024))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(vocab,activation='softmax'))
    model.compile('adam',loss='categorical_crossentropy', metrics=['accuracy'])
earlyStop = keras.callbacks.EarlyStopping(monitor='loss', min_delta=0.001, patience=9, verbose=0, mode='min', baseline=None, restore_best_weights=True)
rlr = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2,patience=7, min_lr=1e-6, mode='auto', verbose=1)
log_dir="logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

intake,target = np.array(intake), keras.utils.to_categorical(target,num_classes=vocab)

model.fit(intake,target,validation_split=0.10, epochs=2000, batch_size=128, verbose=1,callbacks=[earlyStop,rlr,tensorboard_callback])
model.save('trump.h5')