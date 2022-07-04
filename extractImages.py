import numpy as np
from PIL import Image
import os
import pandas as pd
from os.path import exists
import cv2

def resize_to_3x32x32(path):# the function gets a path and resizes the image to 3x32x32
    new_image = cv2.imread(path)
    #print(new_image.shape)
    new_image = cv2.resize(new_image, (32, 32))
    #print(new_image.shape)
    #cv2.imshow("resized", new_image)
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

def add_to_CSV(df):
    path = os.path.join('../', 'CIFAR-10.csv')
    if not exists(path):#if the folder doesn't exist
        df_labels = pd.DataFrame(columns=['image', 'labels', 'names','final_labels'])
        df_labels.to_csv(path, mode='a', index=False)

    df=pd.DataFrame(data=df)
    df.to_csv(r'../CIFAR-10.csv',mode='a', index=False , header=False)


def save_images(images,names):
    images_path=[]
    path = os.path.join('../', 'images')
    if not exists(path):#if the folder doesn't exist
        os.mkdir(path)# create a folder for the images
    images = np.reshape(images, (len(names), 3, 32, 32))
    for image,image_name in zip(images,names):
        fixed_image = np.transpose(image, (1, 2, 0))
        fixed_image = Image.fromarray(fixed_image)
        path='../images/'+image_name.decode("utf-8")
        fixed_image.save(path)
        images_path.append(path)
    return images_path


def map_classes(images,  coarse_labels,  names,final_labels,selected_classes):
    df= {'image': images, 'labels': coarse_labels, 'names': names,'final_labels':final_labels}
    df=pd.DataFrame(data=df)

    df=df[df['labels'].isin( selected_classes)]
    for i in range(len(selected_classes)):#replace label's names to prevent duplicates
        df['labels']=df['labels'].replace(selected_classes[i],10+i)
    print('map_classes')
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
    df = {'image': image_path, 'labels': labels, 'names': names}
    add_to_CSV(df)

def load_cifar100_data_into_CSV(directory,selected_classes):
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
    df = {'image': image_path, 'labels': coarse_labels, 'names': names, 'final_labels': final_labels}
    add_to_CSV(df)

def load_all_data(path,selected_classes):#the function gets the path where the cifar10 and the cifar100 are stored
    #  ולעשות פונקציה למיפוי הקלאסים שאני רוצה.
    path_cifar10 = os.path.join(path, 'cifar-10-batches-py')
    path_cifar100 = os.path.join(path, 'cifar-100-python')

    load_cifar10_data_into_CSV(path_cifar10)
    load_cifar100_data_into_CSV(path_cifar100,selected_classes)
    #try merging