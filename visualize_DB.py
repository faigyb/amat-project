import pandas as pd
import seaborn as sns
import matplotlib
import json
import matplotlib.pyplot as plt
import numpy as np
import h5py
from PIL import Image
from PIL._imaging import display
import matplotlib.image as mpimg
import cv2


def class_samples_number():
    df = pd.read_csv()
    with open(r'../labels_names.json', 'r') as f:
        classes_names = json.load(f) #load classes names
    ax=sns.countplot(x='labels',data=df, palette = "CMRmap_r")
    ax.set_xticklabels(classes_names.values(), rotation=40, ha="right")
    ax.set_title('disturbution of classes')
    ax.set_xlabel('Classes')
    plt.show()

def image_examples():
    df = pd.read_csv(r'../CIFAR-10.csv')
    help_list = df[df['labels'].isin([1])].head()['image']
    fig= plt.figure(figsize=(15,10))
    images=list()
    rows = 15
    columns = 5
    with open(r'../labels_names.json', 'r') as f:
        classes_names = json.load(f)
    print(classes_names)
    arr=[0,1,2,3,4,5,6,7,8,9,11,12,14,24,27]
    for j in classes_names:
        print(j)
        help_list = df[df['labels'].isin([int(j)])].head()['image']
        print(help_list)
        for i in help_list:
            images.append(cv2.imread(i))
        for i in range(len(images)):
            fig.add_subplot(rows, columns,i+1)
            plt.imshow(images[i])
            plt.axis('off')
            plt.title(i)
    plt.show()

def open_csv(path):
    df = pd.read_csv(path)
    return df

def pie_chart_split(tr,val,tst):
    myValues=[len(tr),len(val),len(tst)]
    mylabels = [f"Train\n{myValues[0]/sum(myValues)}%", f"valid\n{myValues[1]/sum(myValues)}%", f"test\n{myValues[2]/sum(myValues)}%"]
    plt.pie(myValues, labels = mylabels,colors=['y','k','c'])
    plt.legend(title = "Our split:",loc=1)
    plt.show()

