import params
import pandas as pd
import numpy as np
from random import shuffle
import os

def ruin_data(train_csv_path:str):
    df = pd.read_csv(train_csv_path)
    labels=df['labels']
    shuffle(labels[:len(labels)//10])
    df['labels']=labels
    #save to csv ruin_TestData
    ruined_TrainData_csv=os.path.join(params.save_all_directory, 'ruined_TrainData.csv')
    df.to_csv(ruined_TrainData_csv)