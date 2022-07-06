import pandas as pd
import seaborn as sns
import matplotlib
import json
import matplotlib.pyplot as plt


def class_samples_number():
    df = pd.read_csv(r'../CIFAR-10.csv')
    with open(r'../labels_names.json', 'r') as f:
        classes_names = json.load(f) #load classes names
    ax=sns.countplot(x='labels',data=df, palette = "CMRmap_r")
    ax.set_xticklabels(classes_names.values(), rotation=40, ha="right")
    ax.set_title('disturbution of classes')
    ax.set_xlabel('Classes')
    plt.show()
