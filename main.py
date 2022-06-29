import numpy as np
from PIL import Image
import imageio
import cv2
from keras.datasets.cifar import load_batch
from keras.utils.data_utils import get_file
# import tensorflow

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict
print("hello")

array1=unpickle(r'C:\amatProject\cifar-10-batches-py\data_batch_1')
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
