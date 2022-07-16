import shutil

import numpy as np
from PIL import Image
import os
import pandas as pd
from os.path import exists
import cv2
import json
from typing import Dict,List

import params


def create_dir(path:str):
    if not exists(path):#if the folder doesn't exist
        os.mkdir(path)# create a folder for the images

def filter_list(list_to_filter:List,filter:List)->List:
    # filtered_list = filter(lambda x: (x >10), list_to_filter)
    filtered_list = [x for x in list_to_filter if x in filter]

    return filtered_list



def resize_to_3x32x32(path:str):# the function gets a path and resizes the image to 3x32x32
    new_image = cv2.imread(path)
    #print(new_image.shape)
    new_image = cv2.resize(new_image, (32, 32))
    #print(new_image.shape)
    return new_image

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

def add_to_CSV(path:str,dfdict:Dict):
    df = pd.DataFrame(data=dfdict)
    df.to_csv(path, mode='a', index=False, header=False)


def add_cifar_to_CSV(df):
    path = params.cifarCSV
    if not exists(path):#if the folder doesn't exist
        df_labels = pd.DataFrame(columns=['image', 'labels','final_labels'])
        df_labels.to_csv(path, mode='a', index=False)
    add_to_CSV(path,df)



def save_images(images,names)->List:
    images_path=[]
    directory_path = params.images_directory
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
    create_dir(params.images_directory)
    path = params.cifarCSV
    df_labels = pd.DataFrame(columns=['image', 'labels', 'final_labels'])
    df_labels.to_csv(path, mode='a', index=False)


def load_all_data(path,selected_classes):#the function gets the path where the cifar10 and the cifar100 are stored
    prepare_files_for_cifar()

    path_cifar10 = params.cifar10_to_execute
    path_cifar100 =params.cifar100_to_execute

    load_cifar10_data_into_CSV(path_cifar10)
    load_cifar100_data_into_CSV(path_cifar100,selected_classes)


def save_image(name,image,path):
    image_path = os.path.join(path,name)
    cv2.imwrite(image_path, image)
    # image.save(path)
    return image_path



def add_our_pictures(directory,target_directory_path=params.our_images_directory):
    create_dir(target_directory_path)
    df=pd.DataFrame(columns=['path','labels'])
    df.to_csv(params.our_images_csv,index=False)
    images_path=[]
    files_list=os.listdir(directory)
    files_list= [x for x in files_list if x.endswith('jpg') or x.endswith('jpeg') or x.endswith('png')]
    for image_name in files_list:
        path=os.path.join(directory, image_name)
        image_resized=resize_to_3x32x32(path)
        image_path=save_image(image_name,image_resized,target_directory_path)
        images_path.append(image_path)
    add_to_CSV(params.our_images_csv,images_path)



def add_one_image(image_path,target_directory_path):
    create_dir(target_directory_path)
    if(image_path.endswith('jpg') or image_path.endswith('jpeg') or image_path.endswith('png')):
        image_resized = resize_to_3x32x32(image_path)
        image_name=image_path.split('\\')[-1]
        image_path = save_image(image_name, image_resized, target_directory_path)
        add_to_CSV(params.our_images_directory,[image_path])

def create_labels_json():
    labels={0:'airplane',1:'automobile',2:'bird',3:'cat',4:'deer',5:'dog',6:'frog',7:'horse',8:'ship',9:'truck',
            11:'fish',12:'flowers',14:'fruit and vegetables',24:'people',27:'trees'}
    with open(params.labels_json, 'w') as json_file:
        json.dump(labels, json_file)

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
def savez_images():#save images in train, test, validation numpy arrays
    x_train,y_train=create_dataset(params.save_all_directory+"TrainData.csv")
    print("train")
    x_test,y_test=create_dataset(params.save_all_directory+"TestData.csv")
    print("test")
    x_validation,y_validation=create_dataset(params.save_all_directory+"ValidationData.csv")
    print("validation")
    np.savez(params.save_all_directory+"cfar10_modified_1000.npz", train=x_train, ytrain=y_train, test=x_test, ytest=y_test,validation=x_validation, yvalidation=y_validation)






