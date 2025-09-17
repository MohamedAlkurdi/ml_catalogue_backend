from .utils import entropy, information_gain
import pandas as pd

def is_convertible_to_numeric(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def is_continuous(table):
    continuous = False
    columns = table.columns
    for key in columns:
        column = table[key]
        if is_convertible_to_numeric(column[0]):
            continuous=True
    return continuous

def check_continuous_columns(table,continuity_threshold=15):
    columns = table.columns
    continuous_features = []

    for key in columns:
        column = table[key]
        number_of_rows = len(column)
        values_frequency = len(set(column))
        length_over_frequency = number_of_rows/values_frequency
        continuity_value = (100*length_over_frequency)/number_of_rows
        print("\ncolumn:",key)
        print("number_of_rows:",number_of_rows)
        print("values_frequency:",values_frequency)
        print("length_over_frequency:",length_over_frequency)
        print("continuity_value:",continuity_value)
        if continuity_value <= continuity_threshold :
            if is_convertible_to_numeric(column[0]):
                continuous_features.append(key)
                print(key,"column is continuous.\n" )
    return continuous_features

def continuous_column_thresholds(data):
    features = data.columns
    data = data.sort_values(by=features[0], ascending=True)

    column = data[features[0]]
    target = data[features[1]]
    thresholds = []
    current_value = None
    previous_value = None
    latest_target_value = None
    current_target_value = None
    
    if not column.empty:
        previous_value = float(column.iloc[0])
        latest_target_value = target.iloc[0]
        
        for i in range(1, len(column)):
            current_value = float(column.iloc[i])
            current_target_value = target.iloc[i]
            
            if current_target_value != latest_target_value:
                latest_target_value = current_target_value
                new_threshold = (previous_value + current_value) / 2
                thresholds.append(new_threshold)
                
            previous_value = current_value
            
    return thresholds

def cetegorize_value(x,T):
    if x < T: return f"<{T}"
    else: return f">={T}"

def split_columns_using_threshols(thresholds, data):
    candidates = {}
    columns = data.columns
    column = data[columns[0]]
    for T in thresholds:
        candidate = pd.DataFrame()
        candidate[columns[0]] = column.apply(lambda x: cetegorize_value(x, T))
        for col in columns[1:]:
            candidate[col] = data[col]
        candidates[T]=candidate
    return candidates

def categorize_continuous_column(column_target_dataset):
    thresholds = continuous_column_thresholds(column_target_dataset)
    candidates = split_columns_using_threshols(thresholds, column_target_dataset)

    # If there are no thresholds or candidates, return None
    if not candidates:
        return None

    target_column = column_target_dataset[column_target_dataset.columns[1]]

    candidate_informations = {}
    for key in candidates.keys():
        candidate_df = candidates.get(key)
        feature_column = candidate_df[candidate_df.columns[0]]
        IG = information_gain(target_column, feature_column)
        split_information = entropy(feature_column)
        gain_ratio_value =0 if split_information == 0 else  IG/split_information
        candidate_informations[key] = gain_ratio_value
        max_key = max(candidate_informations,key=candidate_informations.get)
    return candidates.get(max_key)

def extract_continuous_columns(data):
    continuous_features = check_continuous_columns(data)
    
    target_column = data.columns[-1]
    
    sub_datasets = {}
    for feature in continuous_features:
        sub_dataset = pd.DataFrame()
        sub_dataset["feature"] = data[feature]
        sub_dataset["target"] = data[target_column]
        
        sub_datasets[feature] = sub_dataset
    return sub_datasets

def handle_continuous_table(data):
    continuous_columns_subdatasets = extract_continuous_columns(data)

    categorized_columns = {}
    for subdataset in continuous_columns_subdatasets:
        result = categorize_continuous_column(continuous_columns_subdatasets[subdataset])
        if result is not None:  # Only add to categorized_columns if result is not None
            categorized_columns[subdataset] = result['feature']
    return categorized_columns

def merge_categorized_columns(columns, data):
    data_copy = data.copy()
    for key in columns:
        data_copy[key] = columns[key]
    return data_copy