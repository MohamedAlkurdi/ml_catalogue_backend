import pandas as pd
import sys
import numpy as np
sys.path.append('..')
from knn.models.Point import *
from knn.models.Knn import *
from sklearn.preprocessing import StandardScaler

def process_data(path):
    
    if not path.endswith("csv"):
        raise Exception("Message from developer: provide a csv file.")
    
    data = pd.read_csv(path)
    if 'id' in data.columns:
        data = data.drop('id', axis=1)
    data = data.replace({None: np.nan})
    data = data.dropna()

    features = data.iloc[:, :-1]
    target = data.iloc[:, -1]

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    data_scaled = pd.DataFrame(features_scaled, columns=features.columns)
    data_scaled['target'] = target.reset_index(drop=True)
    
    # print("Data after processing:\n",data_scaled.head())
    
    return data_scaled

def extract_points(table, target_index = -1):
    """
    Convert rows of a Dataframe into Point objects, assuming that the target column is the last column by default.
    You can change the target column index by passing the target_inedex parameter.
    """
    table = table.values.tolist()
    points = []
    for row in table:
        target_value = row[target_index]
        features = row[:target_index] + row[target_index + 1:] if target_index != -1 else row[:-1]
        point = Point(*features,target=target_value)
        points.append(point)
    return points

def is_convertible_to_numeric(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def classes_frequencies(neighbors_labels):
    freqs = {}
    classes = set(neighbors_labels)

    for i in classes:
        freqs[i] = 0

    for i in neighbors_labels:
        freqs[i] += 1

    return freqs

