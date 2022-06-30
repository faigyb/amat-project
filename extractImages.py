import numpy as np
from PIL import Image
import os
import pandas as pd
# import imageio
import cv2

def resize_to_3x32x32(path):# the function get path and resize the image to 3x32x32
    new_image = cv2.imread(path)
    #print(new_image.shape)
    new_image = cv2.resize(x, (32, 32))
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
    labels=data[b'labels']
    images=data[b'data']
    names=data[b'filenames']
    return labels,images,names

def add_to_CSV(images,labels,names,batch):
    df = {'image': images, 'labels':labels,'names':names,'batch':batch}
    df=pd.DataFrame(data=df)
    df.to_csv(r'../CIFAR-10.csv',mode='a')


def save_images(images,names):
    images_path=[]
    path = os.path.join('../', 'images')
    os.mkdir(path)# create a folder for the images

    images = np.reshape(images, (60000, 3, 32, 32))
    for image,image_name in zip(images,names):
        fixed_image = np.transpose(image, (1, 2, 0))
        fixed_image = Image.fromarray(fixed_image)
        path='../images/'+image_name.decode("utf-8")
        fixed_image.save(path)
        images_path.append(path)
    return images_path


def load_cifar10_data_into_CSV(directory):
    images=[]
    labels=[]
    names=[]
    batch=[]
    for filename in os.listdir(directory):
        if filename.startswith("data_batch") or filename.startswith("test_batch"):
            path = os.path.join(directory,  filename)  # Adding file name at the end of the address
            data=unpickle(path)
            batch_labels,batch_images,batch_names=divide_data(data)
            labels+=batch_labels
            images = [*images, *batch_images]
            names+=batch_names
            batch+=[filename]*len(batch_labels)

    image_path=save_images(images,names)
    # im = Image.open(image_path[1])
    # im.show()
    add_to_CSV(image_path,labels,names,batch)