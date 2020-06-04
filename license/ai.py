import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import random
from random import shuffle
import tensorflow as tf
from keras.preprocessing import image
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import pickle
from tqdm import tqdm


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

training_data = []
MODEL_NAME = 'license-character-rec.h5'
TRAINDIR = os.path.join(BASE_DIR, 'trainDataset')
IMG_SIZE = 100
IMG_HEIGHT = 1

letters = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D',
    'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O','P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z' ]

def create_training_data():
    for letter in letters:
        # letter = str(letter)
        # print(letter)
        path = os.path.join(TRAINDIR, letter)
        class_num = letters.index(letter)
        for img in tqdm(os.listdir(path)):
            try:
                img1 = image.load_img(os.path.join(path, img),color_mode = "grayscale", target_size=(IMG_SIZE,IMG_SIZE))
                img1 = image.img_to_array(img1)
                img1 = img1/255
                # img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                # thres = cv2.adaptiveThreshold(img_array, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                # newimg_array = cv2.resize(thres, (IMG_SIZE, IMG_SIZE))
                training_data.append([img1, class_num])
            except Exception as e:
                print("Error: "+ os.path.join(path, img)+ e)
    return training_data

def printed():
    create_training_data()
    # random.shuffle(training_data)

    x = []
    y = []

    for features, label in training_data:
        x.append(features)
        y.append(label)

    x = np.array(x).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    y = np.array(y)
    # x= x/255.0
    # print(len(letters))
    # print(y)


def main():
    # print(TRAINDIR)
    create_training_data()
    # print(training_data)
    random.shuffle(training_data)

    x = []
    y = []

    for features, label in training_data:
        x.append(features)
        y.append(label)

    # x = np.array(x)
    x = np.array(x).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    y= np.array(y)

    # x= x/255.0

    model = Sequential([
        Conv2D(64, 3, activation='relu', input_shape=(IMG_SIZE, IMG_SIZE ,1)),
        MaxPooling2D(pool_size=(2,2)),
        Conv2D(256, 3, activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(512, 3, activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dropout(0.5),
        Dense(512,activation='relu'),
        Dropout(0.5),
        Dense(len(letters),activation='softmax'),
    ])
    model.compile(optimizer='adam',
                  loss="sparse_categorical_crossentropy",
                  metrics=['accuracy'])
    model.fit(x,y, batch_size=100,epochs=10, validation_split= 0.2,verbose=2)
    model.summary()
    model.save(MODEL_NAME)

if __name__ == "__main__":
    main()



