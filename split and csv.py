#necessary imports:
#from sklearn.model import train_test_split
import pandas as pd
from sklearn.model_selection import train_test_split
import os.path

def my_train_test_split(DataFrameX, y=None, valid=False):
    # split a df to train and test, or train and validation, depend on the kwargs selection
    if valid:
        size = 0.18
    else:
        size = 0.15
    if y is None:
        y = DataFrameX['Labels']
        DataFrameX = DataFrameX.drop(['Labels'], axis=1)
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
        return True
    except:
        return False


def open_csv(path):
    df = pd.read_csv(path)
    return df
def split_and_save(path,prefix):
    df=open_csv(path)
    dfTempX,dfTestX,dfTempy,dfTesty=my_train_test_split(df)
    dfTrainX,dfValX,dfTrainy,dfValy=my_train_test_split(dfTempX,dfTempy,True)
    dfTrainX['labels']=dfTrainy
    dfValX['labels'] = dfValy
    dfTestX['labels']=dfTesty
    save_csv(dfTrainX,(prefix+'TrainData'))
    save_csv(dfValX, (prefix+'ValidationData'))
    save_csv(dfTestX,(prefix+'TestData'))
split_and_save("../Covid-19_data.csv","./")
