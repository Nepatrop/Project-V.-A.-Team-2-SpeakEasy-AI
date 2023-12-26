from __future__ import absolute_import, division, print_function, unicode_literals
import os
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import pandas as pd

print(tf.__version__)

path = "Disorder Voices"  ## put the right directory

voicePathDirs = os.listdir(path)
file_pathology = []
file_path = []

for file in voicePathDirs:
    # storing file paths
    file_path.append(path + file)

    # extracting information for pathology classification
    part = file.split('_')

    # checking if the file is normal, abnormal, or unknown
    if 'nrm' in part[2].lower():
        file_pathology.append('normal')
    elif 'ptho' in part[2].lower():
        file_pathology.append('pathology')
    else:
        file_pathology.append('unknown')

# dataframe for pathology classification of files
pathology_df = pd.DataFrame(file_pathology, columns=['Pathology'])

# dataframe for path of files
path_df = pd.DataFrame(file_path, columns=['Path'])
voiceData_df = pd.concat([pathology_df, path_df], axis=1)
voiceData_df.head()

## Data division

from sklearn.model_selection import train_test_split

train_data, test_data, train_labels, test_labels = train_test_split(X, y, test_size=0.2, random_state=1)
train_data, val_data, train_labels, val_labels = train_test_split(train_data, train_labels, test_size=0.2, random_state=1)

train_data.shape()

## Convolutional base

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu',
                        input_shape=(28, 28, 1)))  ## input_shape depends on Data division part output.
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.summary()
## Dense layer at the top

model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(2, activation='sigmoid'))

model.summary()

## train model

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_data, train_labels, epochs=10, validation_data=(val_data, val_labels))

## Test model

test_loss, test_acc = model.evaluate(test_data, test_labels)
print(test_acc)

import matplotlib.pyplot as plt

f = plt.figure(figsize=(10, 6))
plt.plot(history.history["loss"], label="train loss")
plt.plot(history.history["val_loss"], label="val_loss")
plt.xlabel('epoch', fontsize=14)
plt.ylabel('loss', fontsize=14)
plt.title('loss history', fontsize=14)
plt.legend(fontsize='large')

f.savefig('loss_history.pdf', bbox_inches='tight')

f = plt.figure(figsize=(10, 6))
plt.plot(history.history["acc"])
plt.xlabel('epoch', fontsize=14)
plt.ylabel('acc', fontsize=14)

f.savefig('accuracy.pdf', bbox_inches='tight')