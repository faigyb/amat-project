# necessary imports:
# from sklearn.model import train_test_split
import pandas as pd
from sklearn.model_selection import train_test_split
import os.path
import params


def my_train_test_split(data_frame_X, y=None, valid=False, columns_to_drop='Labels', columns_to_seperate='Labels'):
    # split a df to train and test, or train and validation, depend on the kwargs selection
    if valid:
        size=params.valid_size
    else:
        size=params.train_size
    if y is None:
        y = data_frame_X[columns_to_drop]
        data_frame_X.drop(columns_to_seperate, axis=1, inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(data_frame_X, y, test_size=size, random_state=42)
    return X_train, X_test, y_train, y_test


# merging df func
def merge_dataFrame(A, B):
    return A.append(B)


def save_csv(df, path, fig=','):
    try:
        df.to_csv(path + '.csv', sep=fig)
        print('we did it bez"h!')
        return True
    except:
        return False


def open_csv(path):
    df = pd.read_csv(path)
    return df


def split_and_save(cifar10_path, prefix):
    df = open_csv(cifar10_path)
    df_temp_X, df_test_X, df_temp_y, df_test_y = my_train_test_split(df, columns_to_drop='labels',
                                                                     columns_to_seperate='labels')
    df_train_X, df_val_X, df_train_y, df_val_y = my_train_test_split(df_temp_X, df_temp_y, True,
                                                                     columns_to_drop='labels',
                                                                     columns_to_seperate='labels')
    df_train_X['labels'] = df_train_y
    df_val_X['labels'] = df_val_y
    df_test_X['labels'] = df_test_y
    save_csv(df_train_X, (prefix + 'TrainData'))
    save_csv(df_val_X, (prefix + 'ValidationData'))
    save_csv(df_test_X, (prefix + 'TestData'))


#split_and_save(params.cifarCSV,"./data.csv/")

