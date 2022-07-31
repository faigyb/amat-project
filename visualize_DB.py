import pandas as pd
import seaborn as sns
import json
import matplotlib.pyplot as plt
import cv2
import params


def class_samples_number():
    df = pd.read_csv(params.cifarCSV)
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
    for j in classes_names:
        help_list = df[df['labels'].isin([int(j)])].head()['image']
        for i in help_list:
            images.append(cv2.imread(i))
        for i in range(len(images)):
            fig.add_subplot(rows, columns,i+1)
            plt.imshow(images[i])
            plt.axis('off')
    plt.show()

def open_csv(path:str):
    df = pd.read_csv(path)
    return df

def pie_chart_split(train_path,validation_path,test_path):
    train=open_csv(train_path)
    validation=open_csv(validation_path)
    test=open_csv(test_path)

    myValues=[len(train),len(validation),len(test)]
    mylabels = [f"Train\n{myValues[0]/sum(myValues)}%", f"valid\n{myValues[1]/sum(myValues)}%", f"test\n{myValues[2]/sum(myValues)}%"]
    plt.pie(myValues, labels = mylabels,colors=['y','k','c'])
    plt.legend(title = "Our split:",loc=1)
    plt.show()
