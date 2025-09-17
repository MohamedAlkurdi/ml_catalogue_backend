import pandas as pd
import numpy as np

def preprocess_dataset(path):
    if not path.endswith("csv"):
        raise Exception("Message from developer: provide a csv file.")
    
    dataset = pd.read_csv(path)
    columns_names = dataset.columns
    for col in columns_names:
        if col.lower() == "id":
            dataset = dataset.drop(columns=[col])
    
    return dataset

def equivalent_target_values(feature_values, feature_column, target_column):
    classes_dict = {}
    for j in range(len(feature_values)):
        classes_dict[feature_values[j]] = []
    for i in range(len(feature_column)):
        classes_dict[feature_column[i]].append(target_column[i])
    for c in classes_dict:
        classes_dict[c] = {x:classes_dict[c].count(x) for x in classes_dict[c]}
    return classes_dict

def target_column(data, index=-1):

    if index < 0:
        target_index = len(data.columns) - 1
    else: target_index = index

    target_column = data.iloc[:, target_index].tolist()
    return target_column

def extract_unique_values(column):
    return list(set(column))

def to_python_type(value):
    if isinstance(value, np.generic):
        return value.item()
    return value

def validate_instance(instance, dataset):

    dataset_columns = dataset.columns
    dataset = dataset.drop(columns=[dataset_columns[-1]])
    dataset_columns = dataset.columns
    
    if len(instance) != len(dataset_columns):
        print("Instance and dataset have different number of columns.")
        return False

    for col in dataset_columns:
        if col in instance.keys():
            if type(instance[col]) != type(to_python_type(dataset[col][0])):
                print("Data types of the instance and the dataset do not match.")
                return False
        else:
            print("Data types of the instance and the dataset do not match.")
            return False

    return True


