import math
import pandas as pd
from .datalab import *


def entropy(column):
    """
    The main job if this function is to calculate the entropy,
    but it also can be used to calculate the Split Inormation,
    because "computationally" they are the same.
    """
    proportions = detect_feature_data_types(column)[0]
    entropy = 0

    for p in proportions:
        if p > 0:
            entropy += abs(p * math.log2(p))

    return entropy

def information_gain(target_column, feature_column):
    if isinstance(target_column, pd.Series):
        target_column = target_column.tolist()
    if isinstance(target_column, pd.Series):
        target_column = target_column.tolist()

    target_entropy = entropy(target_column)
    sum_of_feature_classes_entropy = 0
    feature_classes = list(set(feature_column))
    classes_dict = equivalent_target_values(feature_classes, feature_column, target_column)
    print("column values VS target values:", classes_dict)

    for c in classes_dict:
        length_of_class = len(classes_dict[c])
        entropy_of_class = entropy(classes_dict[c])
        weghited_entropy_of_class = (
            length_of_class / len(target_column) * entropy_of_class
        )
        # print("weighted entropy of class ", c, ": ", weghited_entropy_of_class)
        sum_of_feature_classes_entropy += weghited_entropy_of_class
    print("sum of weighted entropies:", sum_of_feature_classes_entropy)
    print("information gain:", target_entropy - sum_of_feature_classes_entropy)
    return target_entropy - sum_of_feature_classes_entropy


def gain_ratio(target_column, column):
    information_gain = information_gain(target_column, column)
    split_information = entropy(column)
    return information_gain / split_information


def process_table(data, target_index=-1):
    """by default, target column is the last columns.
    you can't change that though.
    """
    columns = data.columns
    if target_index == -1:
        target_index = len(columns) -1
    # continuous_tables = check_continuous_columns(data)
    
    # print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC\n")
    # print("continuous tables:", continuous_tables)
    # print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC\n")
    
    
    print("target_index: ", target_index)
    print("===data table features(columns) processing operation starting===")
    
    target_column = data.iloc[:, target_index].tolist()
    target_entropy = entropy(target_column)
    print("Target Entropy:", target_entropy)
    coulmns_information_gain = {}
    coulmns_gain_ratios = {}
    data = data.drop(columns=[columns[target_index]])
    
    if(target_entropy == 0.0):
        print("\n\n\n")
        print(">>>>>>>>>>>>> LEAF NODE <<<<<<<<<<<<")
        print("\n\n\n")
        return {"is_leaf":True,"value":target_column[0]}
    else:
        for i in range(len(data.columns)):
            column_label = columns[i]
            print("COLUMN:",column_label)
            column = data.iloc[:, i].tolist()
            information_gain_value = information_gain(target_column, column)
            gain_ratio_value = 0 if entropy(column) == 0 else information_gain_value / entropy(column)
            coulmns_information_gain[columns[i]] = information_gain_value
            coulmns_gain_ratios[column_label] = gain_ratio_value
            print("======================================")
        
        #check for empty dictionary before calling max()
        if not coulmns_information_gain:
            # if there are no features with information gain, treat as a leaf node
            majority_class = max(set(target_column), key=target_column.count)
            return {"is_leaf":True,"value":majority_class}
            
        print("max information gain column: ",max(coulmns_information_gain, key=coulmns_information_gain.get))
        return {"is_leaf":False,"value":max(coulmns_information_gain, key=coulmns_information_gain.get)}
