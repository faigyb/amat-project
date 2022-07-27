import params
import os
import visualize_DB,extract_cifar,create_data,split_and_csv,ruin_data


selected_classes = [1, 2, 4, 14, 17]
# extract_cifar.load_all_data(r'C:\amatProject',selected_classes)

# create_data.create_labels_json()

#we now would like to see our data distrebution.
# visualize_DB.class_samples_number()

#now we need to divide our data into train test and validation
# split_and_csv.split_and_save(params.cifarCSV,params.save_all_directory)

#we can now see how the data distrebutes between the train test and validation
# visualize_DB.pie_chart_split(os.path.join(params.save_all_directory,'TrainData.csv'),os.path.join(params.save_all_directory,'ValidationData.csv'),os.path.join(params.save_all_directory,'TestData.csv'))

#now we take all the data (train, test and validation and insert it (after normolized) to npz file that we can upload to google drive ready for the model
# create_data.savez_images()

#define threashold and create thresh json
# create_data.define_thresh_json()

#here were ruining some of the train data and we want to see how the model will work now
# ruin_data.ruin_data(os.path.join(params.save_all_directory, 'TrainData.csv'))
# ruin_data.savez_images()

