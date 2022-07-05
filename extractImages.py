import numpy as np
from PIL import Image
import os
import pandas as pd
from os.path import exists
import cv2
import json
from typing import Dict,List

def create_dir(path):
    if not exists(path):#if the folder doesn't exist
        os.mkdir(path)# create a folder for the images

def resize_to_3x32x32(path):# the function gets a path and resizes the image to 3x32x32
    new_image = cv2.imread(path)
    #print(new_image.shape)
    new_image = cv2.resize(new_image, (32, 32))
    #print(new_image.shape)
    cv2.imshow("resized", new_image)
    #cv2.waitKey(0)
    return new_image

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict    #return a dict that has the data-images labels and names


def divide_data(data):#divide batch into labels, data and names
    images=data[b'data']
    names=data[b'filenames']
    if len(data)==4:
        labels=data[b'labels']
        return labels,images,names
    coarse_labels=data[b'coarse_labels']
    final_labels = data[b'fine_labels']
    return images,names,coarse_labels,final_labels

def add_to_CSV(path:str,dfdict:Dict):
    df = pd.DataFrame(data=dfdict)
    df.to_csv(path, mode='a', index=False, header=False)


def add_cifar_to_CSV(df):
    path = os.path.join('../', 'CIFAR-10.csv')
    if not exists(path):#if the folder doesn't exist
        df_labels = pd.DataFrame(columns=['image', 'labels','final_labels'])
        df_labels.to_csv(path, mode='a', index=False)
    add_to_CSV(path,df)



def save_images(images,names)->List:
    images_path=[]
    directory_path = os.path.join('../', 'images')
    create_dir(directory_path)
    images = np.reshape(images, (len(names), 3, 32, 32))
    for image,image_name in zip(images,names):
        fixed_image = np.transpose(image, (1, 2, 0))
        fixed_image = Image.fromarray(fixed_image)
        path=f'{directory_path}/{image_name.decode("utf-8")}'
        fixed_image.save(path)
        images_path.append(path)
    return images_path


def map_classes(images,  coarse_labels,  names,final_labels,selected_classes):
    dfdict= {'image': images, 'labels': coarse_labels, 'names': names,'final_labels':final_labels}
    df=pd.DataFrame(data=dfdict)
    df=df[df['labels'].isin( selected_classes)]
    for i in selected_classes:#replace label's names to prevent duplicates
        df['labels']=df['labels'].replace(i,i+10)
    return df['image'].tolist(),df['labels'],df['names'],df['final_labels']
    #take only the classes we want from cifar100

def load_cifar10_data_into_CSV(directory):
    images=[]
    labels=[]
    names=[]
    for filename in os.listdir(directory):
        if filename.startswith("data_batch") or filename.startswith("test_batch"):
            path = os.path.join(directory,  filename)  # Adding file name at the end of the address
            data=unpickle(path)
            batch_labels,batch_images,batch_names=divide_data(data)
            labels+=batch_labels
            images = [*images, *batch_images]
            names+=batch_names

    image_path=save_images(images,names)
    dfdict = {'image': image_path, 'labels': labels}
    add_cifar_to_CSV(dfdict)

def load_cifar100_data_into_CSV(directory,selected_classes):
    selected_classes.sort(reverse=True)
    images=[]
    coarse_labels=[]
    final_labels=[]
    names=[]
    for filename in os.listdir(directory):
        if filename.startswith("test") or filename.startswith("train"):
            path = os.path.join(directory, filename)  # Adding file name at the end of the address
            data = unpickle(path)
            batch_images, batch_names, batch_coarse_labels, batch_final_labels=divide_data(data)
            coarse_labels+=batch_coarse_labels
            images = [*images, *batch_images]
            names+=batch_names
            final_labels+=batch_final_labels
    images,  coarse_labels,  names,final_labels=map_classes(images,  coarse_labels,  names,final_labels,selected_classes)
    image_path=save_images(images,names)
    df = {'image': image_path, 'labels': coarse_labels, 'final_labels': final_labels}
    add_cifar_to_CSV(df)

def load_all_data(path,selected_classes):#the function gets the path where the cifar10 and the cifar100 are stored
    path_cifar10 = os.path.join(path, 'cifar-10-batches-py')
    path_cifar100 = os.path.join(path, 'cifar-100-python')

    load_cifar10_data_into_CSV(path_cifar10)
    load_cifar100_data_into_CSV(path_cifar100,selected_classes)
    #try merging

def save_image(name,image,path):
    create_dir(path)
    image_path = os.path.join(path,name)
    cv2.imwrite(image_path, image)
    # image.save(path)
    return image_path



def add_our_pictures(directory,directory_path):
    images_path=[]
    for image_name in os.listdir(directory):
        if not image_name.startswith("desktop"):
            path=os.path.join(directory, image_name)
            image_resized=resize_to_3x32x32(path)
            image_path=save_image(image_name,image_resized,directory_path)
            images_path.append(image_path)
    add_to_CSV(r'../our_images.csv',images_path)


def add_one_image(image_path,target_directory_path):
    image_resized = resize_to_3x32x32(image_path)
    image_name=image_path.split('\\')[-1]
    image_path = save_image(image_name, image_resized, target_directory_path)
    add_to_CSV(r'../our_images.csv',[image_path])

def create_labels_json():
    labels={0:'airplane',1:'automobile',2:'bird',3:'cat',4:'deer',5:'dog',6:'frog',7:'horse',8:'ship',9:'truck',
            11:'fish',12:'flowers',14:'fruit and vegetables',24:'people',27:'trees'}
    with open(r'../labels_names.json', 'w') as json_file:
        json.dump(labels, json_file)








