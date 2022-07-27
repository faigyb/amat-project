import shutil
import params
import pandas as pd
import os
import visualize_DB,extract_cifar,create_data,split_and_csv,ruin_data
import numpy as np
selected_classes = [1, 2, 4, 14, 17]
# extract_cifar.load_all_data(r'C:\amatProject',selected_classes)

# create_data.create_labels_json()

#'we now would like to see our data distrebution.
# visualize_DB.class_samples_number()

#now we need to divide our data into train test and validation
# split_and_csv.split_and_save(params.cifarCSV,params.save_all_directory)

#we can now see how the data distrebutes between the train test and validation
# visualize_DB.pie_chart_split(os.path.join(params.save_all_directory,'TrainData.csv'),os.path.join(params.save_all_directory,'ValidationData.csv'),os.path.join(params.save_all_directory,'TestData.csv'))

# extractImages.add_our_pictures(r'C:\Users\biali\Pictures\Camera Roll',r'C:\amatProject\our_resized_images')
# extractImages.add_one_image(r'C:\faigy bootcamp\basic-original.png',r'C:\amatProject\our_resized_images')

#now we take all the data (train, test and validation and insert it (after normolized) to npz file that we can upload to google drive
# create_data.savez_images()
# ruin_data.ruin_data(os.path.join(params.save_all_directory, 'TrainData.csv'))
# ruin_data.savez_images()

