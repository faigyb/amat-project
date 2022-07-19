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


def my_load_model():
    model_path=params.model_path
    model = load_model(params.model_path)
    return model

def load_labels():
    with open(params.labels_json, 'r') as f:
        classes_names = json.load(f) #load classes names
        return  classes_names

def predict(image_path):
    model=my_load_model()
    labels=load_labels()

    image = Image.open(image_path)
    image = np.asarray(image)
    image = [image]
    image = np.asarray(image)
    image_pred = model.predict(image)
    ind = np.where(image_pred[0] == 1)[0][0]
    return labels[str(ind)]

