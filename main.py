from scipy import signal
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import seaborn as sns

import os
import pandas as pd
import tensorflow as tf

from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Flatten, Dropout, BatchNormalization
from tensorflow.keras.callbacks import ModelCheckpoint

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

import keras
from keras.callbacks import ReduceLROnPlateau
from keras.models import Sequential
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout, BatchNormalization
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint


pathDisorfer = "data/DataSets/Disorder Voices/"
pathNormal = "data/DataSets/Normal Voices/"


voicePathDirs = os.listdir(pathDisorfer)
voiceNormDirs = os.listdir(pathNormal)

file_voices = []
file_path = []

for file in voicePathDirs:
    # storing file paths
    file_path.append(pathDisorfer + file)
    file_voices.append('pathology')

for file in voiceNormDirs:
    file_path.append(pathNormal + file)
    file_voices.append('normal')
# dataframe for pathology classification of files
voices_df = pd.DataFrame(file_voices, columns=['Voices'])

# dataframe for path of files
path_df = pd.DataFrame(file_path, columns=['Path'])
voiceData_df = pd.concat([voices_df, path_df], axis=1)
voiceData_df.to_csv("voiceData_df.csv", index=False)
voiceData_df.head()


typeVoice = 'pathology'
path = np.array(voiceData_df.Path[voiceData_df.Voices == typeVoice])[1]
data, sampling_rate = librosa.load(path)


typeVoice = 'normal'
path = np.array(voiceData_df.Path[voiceData_df.Voices == typeVoice])[1]


def extract_features(data, sample_rate):
    result = np.array([])

    # Root Mean Square Value
    rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
    result = np.hstack((result, rms))  # stacking horizontally

    return result

def get_features(path):
    data, sample_rate = librosa.load(path)
    result = np.array(extract_features(data, sample_rate))

    return result


X, Y = [], []
for path, voice in zip(voiceData_df.Path, voiceData_df.Voices):
    if librosa.get_duration(path=path) != 0:
        feature = get_features(path)
        for ele in feature:
            X.append(ele)
            Y.append(voice)
    else:
        print('audiofile {0} is empty'.format(path))


len(X), len(Y), voiceData_df.Path.shape


Features = pd.DataFrame(X)
Features['labels'] = Y
Features.to_csv('features.csv', index=False)
Features.head()


X = Features.iloc[:, :-1].values
Y = Features['labels'].values


encoder = OneHotEncoder()
Y = encoder.fit_transform(np.array(Y).reshape(-1, 1)).toarray()


x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=0, shuffle=True)


scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)


x_train = np.expand_dims(x_train, axis=2)
x_test = np.expand_dims(x_test, axis=2)


model = Sequential()
model.add(Conv1D(256, kernel_size=5, strides=1, padding='same', activation='relu', input_shape=(x_train.shape[1], 1)))
model.add(MaxPooling1D(pool_size=5, strides=2, padding='same'))

model.add(Conv1D(256, kernel_size=5, strides=1, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=5, strides=2, padding='same'))

model.add(Conv1D(128, kernel_size=5, strides=1, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=5, strides=2, padding='same'))
model.add(Dropout(0.2))

model.add(Conv1D(64, kernel_size=5, strides=1, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=5, strides=2, padding='same'))

model.add(Flatten())
model.add(Dense(units=32, activation='relu'))
model.add(Dropout(0.3))

model.add(Dense(units=2, activation='softmax'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.summary()


rlrp = ReduceLROnPlateau(monitor='loss', factor=0.4, verbose=0, patience=2, min_lr=0.0000001)
history = model.fit(x_train, y_train, batch_size=64, epochs=50, validation_data=(x_test, y_test), callbacks=[rlrp])


print("Accuracy of our model on test data : ", model.evaluate(x_test, y_test)[1]*100, "%")

epochs = [i for i in range(50)]
train_acc = history.history['accuracy']
train_loss = history.history['loss']
test_acc = history.history['val_accuracy']
test_loss = history.history['val_loss']


pred_test = model.predict(x_test)
y_pred = encoder.inverse_transform(pred_test)
y_test = encoder.inverse_transform(y_test)

print(classification_report(y_test, y_pred))

model.save("Voice-Classification-Model.keras")