import pandas as pd

def execlude_root_feature(data,best_feature):
    features = list(data.columns)
    features.remove(best_feature)
    return features

def detect_feature_data_types(column):
    if isinstance(column, pd.Series):
        column = column.tolist()
    
    classes = list(set(column))
    classes_split = {}
    proportions = []

    for c in classes:
        classes_split[c] = column.count(c)
    for i in classes_split:
        proportions.append(classes_split[i] / len(column))

    return proportions, classes_split

def equivalent_target_values(feature_classes, feature_column, target_column):
    classes_dict = {}
    for j in range(len(feature_classes)):
        classes_dict[feature_classes[j]] = []
    for i in range(len(feature_column)):
        classes_dict[feature_column[i]].append(target_column[i])
    return classes_dict