
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import json
import params
import create_data
from typing import List

def my_load_model():
    model_path = params.model_path
    model = load_model(model_path)
    return model

def load_json(file:str)->List:
    with open(file, 'r') as f:
        list = json.load(f)
        print(type(list))#load classes names
        return list

def load_labels()->List:
    with open(params.labels_json, 'r') as f:
        classes_names = json.load(f) #load classes names
        return  classes_names

def predict(image_path:str,model)->List:
    labels=load_labels()
    image = Image.open(image_path)
    image = np.asarray(image)
    image = image.astype('float32')
    image /= 255
    image = [image]
    image = np.asarray(image)
    image_pred = model.predict(image).flatten()
    return image_pred

def predict_without_pro(image_path:str,model)->str:
    labels = load_json(params.labels_json)
    image_pred = predict(image_path,model)
    ind=np.argmax(image_pred)
    return labels[str(ind)]

def predict_pro(image_path:str,model)->str:

    labels = load_json(params.labels_json)
    threshes = load_json(params.thresh_json)
    image_pred_prob = predict(image_path,model)
    print(f"max: {np.mean(image_pred_prob)},\nargmax: {np.argmax(image_pred_prob)}\nmaxPro: {np.max(image_pred_prob)}\nthr: {threshes}")

    if np.max(image_pred_prob) >= threshes[str(np.argmax(image_pred_prob))]:
         ind=labels[str(np.argmax(image_pred_prob))]
    else:ind='none'
    print(f"probs: {image_pred_prob}\nind: {ind}")
    return ind
