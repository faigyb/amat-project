import shutil

import pandas as pd
import os

import params

import extractImages
import visualize_DB
selected_classes = [1, 2, 4, 14, 17]
#extractImages.load_cifar100_data_into_CSV(r'C:\amatProject\cifar-100-python',[0,12])
# extractImages.load_cifar10_data_into_CSV(r'C:\amatProject\cifar-10-batches-py')

# extractImages.load_all_data(r'C:\amatProject',selected_classes)
# extractImages.add_our_pictures(r'C:\Users\biali\Pictures\Camera Roll',r'C:\amatProject\our_resized_images')
# extractImages.add_one_image(r'C:\faigy bootcamp\basic-original.png',r'C:\amatProject\our_resized_images')

#extractImages.create_labels_json()
# visualize_DB.class_samples_number()
import split_and_csv
# split_and_csv.split_and_save(params.cifarCSV,params.save_all_directory)
# visualize_DB.image_examples()