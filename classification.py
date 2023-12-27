from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf

from tensorflow.keras import datasets, layers, models
print(tf.__version__)


import json
import numpy as np
import os
import shutil
import zipfile
from random import shuffle
from scipy.io import wavfile
from google.colab import files



def upload_kaggle_credentials():
    print("Upload the Kaggle API credentials (kaggle.json) file")
    uploaded = files.upload()
    #!mkdir -p ~/.kaggle
    #!mv kaggle.json ~/.kaggle/
    #!chmod 600 ~/.kaggle/kaggle.json

def download_dataset(dataset_name):
    #!kaggle datasets download -d {dataset_name}

def extract_dataset(zip_file, extraction_path):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)

def rename_files(directory, prefix):
    counter = 1
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            old_path = os.path.join(directory, filename)
            new_filename = f"{prefix}{counter}.wav"
            new_path = os.path.join(new_directory, new_filename)
            os.rename(old_path, new_path)
            counter += 1

def remove_empty_folders(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

def count_files(directory):
    file_count = sum([1 for filename in os.listdir(directory) if os.path.isfile(os.path.join(directory, filename))])
    return file_count

# Upload Kaggle API credentials
upload_kaggle_credentials()

# Download and extract the dataset
download_dataset('mhantor/russian-voice-dataset')
extract_dataset('russian-voice-dataset.zip', './data')

new_directory = '/content/data'

# Rename files in the "Normal Voices" directory
normal_directory = '/content/data/Normal Voices/Normal Voices'
rename_files(normal_directory, 'healthy')

# Rename files in the "Disorder Voices" directory
disorder_directory = '/content/data/Disorder Voices/Disorder Voices'
rename_files(disorder_directory, 'pathology')

# Remove empty folders
remove_empty_folders('/content/data')

# Count the number of files in the dataset
file_count = count_files(new_directory)
print("Number of files in the dataset:", file_count)