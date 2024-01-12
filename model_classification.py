import tensorflow as tf
from tensorflow.keras.models import load_model
import librosa
import numpy as np
import keras
from sklearn.preprocessing import OneHotEncoder


model = keras.models.load_model('Voice-Classification-Model.keras')

def start():
    predictions = model.predict(preprocess_audio('data/voice.wav'))
    return predictions


def preprocess_audio(audio_file):
    audio, _ = librosa.load(audio_file, sr=44100)
    result = tf.expand_dims(np.array(np.hstack((np.array([]), np.mean(librosa.feature.rms(y=audio).T, axis=0)))), axis=-1)
    return result