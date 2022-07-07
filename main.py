import pandas as pd
from tensorflow import keras
from keras.datasets import cifar10

import extractImages
import visualize_DB
selected_classes = [1, 2, 4, 14, 17]
# extractImages.load_cifar100_data_into_CSV(r'C:\amatProject\cifar-100-python',selected_classes)

# extractImages.load_all_data(r'C:\amatProject',selected_classes)
# extractImages.add_our_pictures(r'C:\Users\biali\Pictures\Camera Roll',r'C:\amatProject\our_resized_images')
# extractImages.add_one_image(r'C:\faigy bootcamp\basic-original.png',r'C:\amatProject\our_resized_images')

#extractImages.create_labels_json()


(x_train, y_train), (x_test, y_test) = cifar10.load_data()
print('x_train shape:', x_train.shape)
print('y_train shape:', y_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')
visualize_DB.class_samples_number()

