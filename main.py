import pandas as pd

import extractImages
extractImages.load_cifar10_data_into_CSV(r'C:\amatProject\cifar-10-batches-py')
df = {'image': [23526,7458], 'labels': ['fb','fhmn '],'names': [5,3], 'batch':[00,1]}
df = pd.DataFrame(data=df)
df.to_csv(r'../CIFAR-10.csv',mode='a')