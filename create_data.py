
import numpy as np
from PIL import Image
import os
import pandas as pd
import json
from typing import Dict,List

import params,funcs


def add_our_pictures(directory,target_directory_path=params.our_images_directory):
    funcs.create_dir(target_directory_path)
    df=pd.DataFrame(columns=['path','labels'])
    df.to_csv(params.our_images_csv,index=False)
    images_path=[]
    files_list=os.listdir(directory)
    files_list= [x for x in files_list if x.endswith('jpg') or x.endswith('jpeg') or x.endswith('png')]
    for image_name in files_list:
        path=os.path.join(directory, image_name)
        image_resized=funcs.resize_to_3x32x32(path)
        image_path=funcs.save_image(image_name,image_resized,target_directory_path)
        images_path.append(image_path)
    funcs.add_to_CSV(params.our_images_csv,images_path)



def add_one_image(image_path,target_directory_path):
    funcs.create_dir(target_directory_path)
    image_path=image_path.lower()
    if(image_path.endswith('jpg') or image_path.endswith('jpeg') or image_path.endswith('png') or image_path.endswith('jfif')  ):
        image_resized = funcs.resize_to_3x32x32(image_path)
        if '//' in image_path:
            image_name=image_path.split('\\')[-1]
        else:
            image_name=image_path.split('/')[-1]
        image_path = funcs.save_image(image_name, image_resized, target_directory_path)
        funcs.add_to_CSV(params.our_images_csv,[image_path])

def create_labels_json():
    labels={0:'airplane',1:'automobile',2:'bird',3:'cat',4:'deer',5:'dog',6:'frog',7:'horse',8:'ship',9:'truck',
            11:'fish',12:'flowers',14:'fruit and vegetables',24:'people',27:'trees'}
    with open(params.labels_json, 'w') as json_file:
        json.dump(labels, json_file)

def define_thresh_json():
    threshes={0:0.2,1:0.1,2:0.15,3:0.2,4:0.2,5:0.25,6:0.12,7:0.2,8:0.3,9:0.2,
            11:0.2,12:0.2,14:0.2,24:0.15,27:0.2}
    with open(params.thresh_json, 'w') as json_file:
        json.dump(threshes, json_file)

def create_dataset(image_csv):
    img_data_array=[]
    class_name=[]
    with open(image_csv,'r') as data:
        next(data)
        for row in data:
            print()
            image= np.array(Image.open(row.split(',')[1]))
            # Normalize the data. Before we need to connvert data type to float for computation.
            image = image.astype('float32')
            image /= 255
            img_data_array.append(image)
            class_name.append(row.split(',')[3])
    return img_data_array , class_name

def savez_images():
    x_train,y_train=create_dataset(params.save_all_directory+"TrainData.csv")
    print("train")
    x_test,y_test=create_dataset(params.save_all_directory+"TestData.csv")
    print("test")
    x_validation,y_validation=create_dataset(params.save_all_directory+"ValidationData.csv")
    print("validation")
    np.savez(params.save_all_directory+"cfar10_modified_1000.npz", train=x_train, ytrain=y_train, test=x_test, ytest=y_test,validation=x_validation, yvalidation=y_validation)

define_thresh_json()