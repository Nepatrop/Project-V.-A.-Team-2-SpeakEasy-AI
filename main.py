from scipy import signal
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import os
import pandas as pd


overlap = 1024
frame_length = 2048

from scipy.io import wavfile

def readAudio(audio):
    fs, amp = wavfile.read(audio)
    dt = 1/fs
    n = len(amp)
    t = dt*n

    if t > 1.0:
        amp = amp[int((t/2 - 0.5)/dt):int((t/2 + 0.5)/dt)]
        n = len(amp)
        t = dt*n

    return(amp, fs, n, t)

### automatic download of files from a folder
path = r'data'              ## main path "/content/"
files = os.listdir(path)

for filename in files:
     audio_data, sampling_rate = wavfile.read(filename)

import librosa
import matplotlib.pyplot as plt
from google.colab import files

uploaded_files = files.upload()     # Upload .wav normal or disorder voice file here

# extract audio and sample rate from audio file
for file_name, file_content in uploaded_files.items():
    audio_data, sampling_rate = librosa.load(file_name)

# return amr , fs , n , t
def process_audio_data(audio_data, sampling_rate):
    amp = audio_data
    fs = sampling_rate
    n = len(audio_data)
    t = len(audio_data) / sampling_rate
    return amp, fs, n, t

amp, fs, n, t = process_audio_data(audio_data, sampling_rate)

# Audio signal drawing
fig = plt.figure(figsize=(10, 4))
plt.plot(amp)
plt.ylabel('amplitude')
plt.xlabel('sample')
plt.title('signal')
plt.show()
# Sample values and sample rate

S = librosa.feature.melspectrogram(y=amp*1.0, sr=fs, n_fft=frame_length, hop_length=overlap, power=1.0)
fig = plt.figure(figsize=(10, 4))

librosa.display.specshow(librosa.power_to_db(S, ref=np.max), y_axis='mel', fmax=8000, x_axis='time')
plt.colorbar(format='%+2.0f dB')
plt.title('Mel spectrogram')
plt.tight_layout()

import cv2

print('original shape: ', librosa.power_to_db(S,ref=np.max).shape)
img = cv2.resize(librosa.power_to_db(S,ref=np.max),(64,64))
librosa.display.specshow(img, y_axis='mel', fmax=8000, x_axis='time')
plt.colorbar(format='%+2.0f dB')
plt.title('Mel spectrogram')
plt.tight_layout()

print(librosa.power_to_db(S,ref=np.max).shape)

import numpy as np

dS = np.gradient(librosa.power_to_db(S,ref=np.max), axis=0)
dS.shape
ddS = np.gradient(dS, axis=0)
# this code calculates the first and second derivative of the image converted to decibels

img = cv2.resize(dS, (64, 64))
librosa.display.specshow(img, y_axis='mel', fmax=8000, x_axis='time')
plt.colorbar(format='%+2.0f dB')
plt.title('Mel spectrogram')
plt.tight_layout()