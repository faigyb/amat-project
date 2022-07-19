import shutil

import numpy as np
from PIL import Image
import os
import pandas as pd
from os.path import exists
import cv2
import json
from typing import Dict,List

import params,funcs


def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict    #return a dict that has the data-images labels and names


def divide_data(data:Dict,type):#divide batch into labels, data and names
    images=data[b'data']
    names=data[b'filenames']
    if type==10:
        labels=data[b'labels']
        return labels,images,names
    if type==100:
        coarse_labels=data[b'coarse_labels']
        final_labels = data[b'fine_labels']
        return images,names,coarse_labels,final_labels
    print("error")


def map_classes(images,  coarse_labels,  names,final_labels,selected_classes):
    dfdict= {'image': images, 'labels': coarse_labels, 'names': names,'final_labels':final_labels}
    df=pd.DataFrame(data=dfdict)
    df=df[df['labels'].isin( selected_classes)]
    for i in selected_classes:#replace label's names to prevent duplicates
        df['labels']=df['labels'].replace(i,i+10)
    return df['image'].tolist(),df['labels'],df['names'],df['final_labels']
    #take only the classes we want from cifar100

def add_cifar_to_CSV(df):
    path = params.cifarCSV
    if not exists(path):#if the folder doesn't exist
        df_labels = pd.DataFrame(columns=['image', 'labels','final_labels'])
        df_labels.to_csv(path, mode='a', index=False)
    funcs.add_to_CSV(path,df)



def save_images(images,names)->List:
    images_path=[]
    directory_path = params.images_directory
    funcs.create_dir(directory_path)
    images = np.reshape(images, (len(names), 3, 32, 32))
    for image,image_name in zip(images,names):
        fixed_image = np.transpose(image, (1, 2, 0))
        fixed_image = Image.fromarray(fixed_image)
        path=f'{directory_path}/{image_name.decode("utf-8")}'
        fixed_image.save(path)
        images_path.append(path)
    return images_path

def load_cifar10_data_into_CSV(directory):
    images=[]
    labels=[]
    names=[]
    files_list = os.listdir(directory)
    files_list = [x for x in files_list if x.startswith("data_batch") or x.startswith("test_batch")]
    for filename in files_list:
        path = os.path.join(directory,  filename)  # Adding file name at the end of the address
        data=unpickle(path)
        batch_labels,batch_images,batch_names=divide_data(data,10)
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
    files_list= os.listdir(directory)
    files_list= [x for x in files_list if x.startswith("test") or x.startswith("train")]
    for filename in files_list:
        path = os.path.join(directory, filename)  # Adding file name at the end of the address
        data = unpickle(path)
        batch_images, batch_names, batch_coarse_labels, batch_final_labels=divide_data(data,100)
        coarse_labels+=batch_coarse_labels
        images = [*images, *batch_images]
        names+=batch_names
        final_labels+=batch_final_labels
    images,  coarse_labels,  names,final_labels=map_classes(images,  coarse_labels,  names,final_labels,selected_classes)
    image_path=save_images(images,names)
    df = {'image': image_path, 'labels': coarse_labels, 'final_labels': final_labels}
    add_cifar_to_CSV(df)

def prepare_files_for_cifar():
    try:
        shutil.rmtree(params.images_directory)
    except:
        print('was not')
    try:
        os.remove(params.cifarCSV)
    except:
        print('was not')
    funcs.create_dir(params.images_directory)
    path = params.cifarCSV
    df_labels = pd.DataFrame(columns=['image', 'labels', 'final_labels'])
    df_labels.to_csv(path, mode='a', index=False)


def load_all_data(path,selected_classes):#the function gets the path where the cifar10 and the cifar100 are stored
    prepare_files_for_cifar()

    path_cifar10 = params.cifar10_to_execute
    path_cifar100 =params.cifar100_to_execute

    load_cifar10_data_into_CSV(path_cifar10)
    load_cifar100_data_into_CSV(path_cifar100,selected_classes)