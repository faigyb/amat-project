import pandas as pd
def class_samples_number():
    df = pd.read_csv(r'../CIFAR-10.csv')
    print(df.tail())
