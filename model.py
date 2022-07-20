# load and evaluate a saved model
from numpy import loadtxt
from tensorflow.keras.models import load_model
import os
import numpy as np
import pandas as pd
from PIL import Image
import os
import json
import params
import create_data


def my_load_model():
    model_path = params.model_path
    model = load_model(r"C:\Users\1\Desktop\imagesProject2\keras_cifar10_trained_model_dataAugmentation2.h5")
    return model
def load_json(file):
    with open(file, 'r') as f:
        list = json.load(f)
        print(type(list))#load classes names
        return list
def load_labels():
    with open(params.labels_json, 'r') as f:
        classes_names = json.load(f) #load classes names
        return  classes_names

def predict(image_path,model):
    labels=load_labels()

    image = Image.open(image_path)
    image = np.asarray(image)
    image = image.astype('float32')
    image /= 255
    image = [image]
    image = np.asarray(image)
    image_pred = model.predict(image)[0]
    print (image_pred)
    ind=np.argmax(image_pred)
    return labels[str(ind)]
def predict_pro(img,model):
    #model = my_load_model()
    labels = load_json(params.labels_json)
    threshes = load_json(params.thresh_json)
    image = Image.open(img)
    image = np.asarray(image)
    image = image.astype('float32')
    image /= 255
    image = [image]
    image = np.asarray(image)
    image_pred_prob = model.predict(image)
    print(f"max: {np.mean(image_pred_prob)},\nargmax: {np.argmax(image_pred_prob)}\nmaxPro: {np.max(image_pred_prob)}\nthr: {threshes}")

    if np.max(image_pred_prob) >= threshes[str(np.argmax(image_pred_prob))]:
         ind=labels[str(np.argmax(image_pred_prob))]
    else:ind='none'
    print(f"probs: {image_pred_prob}\nind: {ind}\n {type(image_pred_prob[0][0])}")
    return ind
create_data.define_thresh_json()
print(predict_pro(r"C:\Users\1\Pictures\amat_images\fish_2.png",my_load_model()))