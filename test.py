import tensorflow as tf
from tensorflow.keras.models import load_model
import librosa
import numpy as np
import keras
from sklearn.preprocessing import OneHotEncoder


model = keras.models.load_model('Voice-Classification-Model.keras')


def start(path):
    def extract_features(data, sample_rate):
        result = np.array([])
        rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
        result = np.hstack((result, rms))
        return result


    def get_features(path):
        data, sample_rate = librosa.load(path)
        result = np.array(extract_features(data, sample_rate))
        return result


    X = []
    if librosa.get_duration(path=path) != 0:
        feature = get_features(path)
        for ele in feature:
            X.append(ele)
        else:
            print('audiofile {0} is empty'.format(path))


    encoder = OneHotEncoder()
    pred_test = model.predict(X)
    y_pred = encoder.inverse_transform(pred_test)
    return y_pred