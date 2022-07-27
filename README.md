# imagesProject
recognizing images project for amat

our goal:

use cnn/vgg model in order to classified
cifar10 dataset images and some cifar100 superclasses as well.
as one could add any desired super-class to classified.

In order to use our code,

first of all you have to change the 'params.py' customize.
so, you have to download the cifar10 both cifar100 datasets,
and then you can extract and save the images locally using our code - in 'extract_cifar.py'
(beforehand you should extract one level manually)

`load_all_data(path,selected_classes)`

//the function gets the path where the cifar10 and the cifar100 are stored

now, all you have to do toward model training is split the data to 3 csv files and upload to your google drive(now the training will carry out at the google-colab) 
so please execute this func:
`split_and_save(params.cifarCSV,"./data.csv/")
` from the 'split_and_csv.py' 

after training and saving the model, and update its path in params,
you just left to run the GUI - 
#your project is all prepared!