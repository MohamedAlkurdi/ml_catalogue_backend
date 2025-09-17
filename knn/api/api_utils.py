from fastapi import HTTPException
import pandas as pd
import io
from knn.utils.datalab import *
from knn.models.Point import *
from knn.models.Knn import *
from knn.functional_implementation.build_knn import *

def ensure_str_categoricals(df):
    # convert all object, bool, and category columns to string
    for col in df.columns:
        if df[col].dtype == 'bool' or df[col].dtype == 'object' or str(df[col].dtype).startswith('category'):
            df[col] = df[col].astype(str)
    return df

def preprocess_test_point(test_point, features_df):
    for col in features_df.columns:
        if col in test_point:
            dtype = features_df[col].dtype
            if dtype == 'bool' or dtype == 'object' or str(dtype).startswith('category'):
                test_point[col] = str(test_point[col])
    return test_point

def preprocess_data(file_content):
    data = pd.read_csv(io.StringIO(file_content))
    if "id" in data.columns:
        data = data.drop('id', axis=1)
    data = data.replace({None: np.nan})
    data = data.dropna()
    return data

def extract_target_column(data, target_index):
    if target_index == -1:
        target_index = len(data.columns) - 1

    if target_index < 0 or target_index >= len(data.columns):
        raise HTTPException(status_code=400, detail="Invalid target index")
    
    target = data.iloc[:, target_index]
    return target
