import params
import pandas as pd
import numpy as np
from random import shuffle
import os
import create_data

def ruin_data(train_csv_path:str):
    df = pd.read_csv(train_csv_path)
    print(df)
    labels=df['labels']
    shuffle(labels[:len(labels)//10])
    df['labels']=labels
    #save to csv ruin_TestData
    ruined_TrainData_csv=os.path.join(params.save_all_directory, 'ruined_TrainData.csv')
    df.to_csv(ruined_TrainData_csv,index=False)


def savez_images():
    x_train,y_train=create_data.create_dataset(params.save_all_directory+"ruined_TrainData.csv")
    print("train")
    x_test,y_test=create_data.create_dataset(params.save_all_directory+"TestData.csv")
    print("test")
    x_validation,y_validation=create_data.create_dataset(params.save_all_directory+"ValidationData.csv")
    print("validation")
    np.savez(params.save_all_directory+"cfar10_ruined_data.npz", train=x_train, ytrain=y_train, test=x_test, ytest=y_test,validation=x_validation, yvalidation=y_validation)
