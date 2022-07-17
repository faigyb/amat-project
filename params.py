import os

save_all_directory='../'

images_directory=os.path.join(save_all_directory, 'images')
cifarCSV=os.path.join(save_all_directory, 'CIFAR-10.csv')
cifar10_to_execute=os.path.join(save_all_directory, 'cifar-10-batches-py')
cifar100_to_execute=os.path.join(save_all_directory, 'cifar-100-python')
our_images_directory=os.path.join(save_all_directory, 'our_images.csv')
labels_json=os.path.join(save_all_directory, 'labels_names.json')
model_path = 'keras_cifar10_trained_model_1A.h5'
label="tha label is soppused to be here"