from turtle import pd
import numpy as np
from PIL import Image
import imageio
import cv2
from keras.datasets.cifar import load_batch
from keras.utils.data_utils import get_file
import tensorflow

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict


array1=unpickle(r'C:\Users\Efrat\Downloads\cifar-10-python\cifar-10-python~\cifar-10-batches-py\data_batch_1')
array=array1[b'data']

array
ims=np.reshape(array,(10000,3,32,32))
# len(ims[0][0][0])
array1=array1[b'labels'][1]
array1
imgg=ims[537,:,:,:]
imgg=np.transpose(imgg,(1,2,0))
print(imgg.shape)
img=Image.fromarray(imgg)
img.show()


def load_data(path):
    print("vnb")
#first commit
#com2g




































#next commit - racheli


#split funcs:
#uses pandas, and skLearn.model
def my_train_test_split(DataFrameX, y=None, **kwargs):
    # split a df to train and test, or train and validation, depend on the kwargs selection
    if True in kwargs:
        size = 0.18
    else:
        size = 0.15
    if y is None:
        y = DataFrameX['labels']
        DataFrameX = DataFrameX.drop(['labels'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(DataFrameX, y, test_size=size, random_state=42)
    return X_train, X_test, y_train, y_test


# //when data includes labels (but it`s unnecessary):
def my_train_test_split_labeled(DataFrameX, **kwargs):
    # split a df to train and test, or train and validation, depend on the kwargs selection
    if True in kwargs:
        size = 0.18
    else:
        size = 0.15

    X_train, X_test, y_train, y_test = train_test_split(DataFrameX.drop(['labels'], axis=1), DataFrameX['labels'],
                                                        test_size=size, random_state=42)
    return X_train, X_test, y_train, y_test


# merging df func
def merge_dataFrame(A, B):
    return A.append(B)


def save_csv(df, path, fig):
    try:
        df.to_csv(path, sep=fig)
        return True
    except:
        return False


def open_csv(path):
    df = pd.read_csv(path)
    return df
