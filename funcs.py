import os
import pandas as pd
from os.path import exists
import cv2
from typing import Dict,List


def create_dir(path:str):
    if not exists(path):#if the folder doesn't exist
        os.mkdir(path)# create a folder for the images

def resize_to_3x32x32(path:str):# the function gets a path and resizes the image to 3x32x32
    new_image = cv2.imread(path)
    new_image = cv2.resize(new_image, (32, 32))
    return new_image

def add_to_CSV(path:str,dfdict:Dict):
    df = pd.DataFrame(data=dfdict)
    df.to_csv(path, mode='a', index=False, header=False)


def save_image(name:str,image,path:str)->str:
    # image_path = os.path.join(path,name)
    image_path = f'{path}/{name}'
    cv2.imwrite(image_path, image)
    return image_path