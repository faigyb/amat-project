#necessary imports:
#from sklearn.model import train_test_split
import pandas as pd
from sklearn.model_selection import train_test_split
import os.path

#from extractImages import create_labels_json
from visualize_DB import pie_chart_split, class_samples_number


def my_train_test_split(DataFrameX, y=None, valid=False,columnsToDrop='Labels',columnsToseperate='Labels'):
    # split a df to train and test, or train and validation, depend on the kwargs selection
    if valid:
        size = 0.18
    else:
        size = 0.15
    if y is None:
        y = DataFrameX[columnsToDrop]
        DataFrameX.drop(columnsToseperate, axis=1,inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(DataFrameX, y, test_size=size, random_state=42)
    return X_train, X_test, y_train, y_test


# //when data includes labels (but it`s unnecessary):
# def my_train_test_split_labeled(DataFrameX, **kwargs):
#     # split a df to train and test, or train and validation, depend on the kwargs selection
#     if True in kwargs:
#         size = 0.18
#     else:
#         size = 0.15
#
#     X_train, X_test, y_train, y_test = train_test_split(DataFrameX.drop(['Longitude'], axis=1), DataFrameX['labels'],
#                                                         test_size=size, random_state=42)
#     return X_train, X_test, y_train, y_test


# merging df func
def merge_dataFrame(A, B):
    return A.append(B)


def save_csv(df, path, fig=','):
    try:
        df.to_csv(path+'.csv', sep=fig)
        print('we did it bez"h!')
        return True
    except:
        return False


def open_csv(path):
    df = pd.read_csv(path)
    return df
def split_and_save(path,prefix):
    df=open_csv(path)
    dfTempX,dfTestX,dfTempy,dfTesty=my_train_test_split(df,columnsToDrop='labels',columnsToseperate='labels')
    dfTrainX,dfValX,dfTrainy,dfValy=my_train_test_split(dfTempX,dfTempy,True,columnsToDrop='labels',columnsToseperate='labels')
    dfTrainX['labels']=dfTrainy
    dfValX['labels'] = dfValy
    dfTestX['labels']=dfTesty
    save_csv(dfTrainX,(prefix+'TrainData'))
    save_csv(dfValX, (prefix+'ValidationData'))
    save_csv(dfTestX,(prefix+'TestData'))
#split_and_save("C:/Users/1/Downloads/CIFAR-10.csv","./data.csv")
import matplotlib.pyplot as plt
#import numpy as np

#y = np.array([35, 25, 25, 15])

# train=open_csv('../data.csv/TrainData.csv')
# val=open_csv('../data.csv/ValidationData.csv')
# test=open_csv('../data.csv/TestData.csv')
# pie_chart_split(train,val,test)
