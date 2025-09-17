from decision_tree.utils.utils import *
from decision_tree.utils.c45Utils import *
import pandas as pd


def build_tree(data_set, latest_tree_state, target_index=-1):
    print("========== DATA ==========")
    print(data_set)
    print(type(data_set))
    print("========== ==== ==========")

    #logic for handling continuous columns
    continuous_features = check_continuous_columns(data_set)
    if continuous_features: 
        categorized_columns = handle_continuous_table(data_set)
        data_set = merge_categorized_columns(categorized_columns, data_set)

    current_node = {
        'feature':None,
        'prediction':None,
        "children":{}
    }
    next_layer_nodes = {}

    target_index = len(data_set.columns) - 1
    dataset_processing_output = process_table(data_set, target_index)
    is_leaf = dataset_processing_output.get("is_leaf")
    
    if is_leaf:
        target_values = data_set.iloc[:, target_index]
        majority_class = target_values.mode()[0] 
        print(f"Reached leaf node ... Prediction: {majority_class}")
        current_node["prediction"] = majority_class
        current_node["feature"] = None
        current_node['children']={}
        return majority_class
    
    table_processing_output_value = dataset_processing_output.get('value')
    current_node["feature"] = table_processing_output_value
    
    ROOT_COLUMN = data_set[table_processing_output_value]
    ROOT_COLUMN = list(ROOT_COLUMN)  # converting dataFrame to list
    feature_classes = list(set(ROOT_COLUMN))  # extracting all the value classes that Root column has

    other_features = execlude_root_feature(data_set,table_processing_output_value)  # extracting the feature from the dataset and execluding the best featre, which is the current Root column

    current_tree_state = {}  # creating a subset starts from here

    print("!!!!!!!!!!!splitting the data table depending on ",table_processing_output_value," columns as the Root!!!!!!!!!!!")

    for j in range(len(feature_classes)):
        current_tree_state[feature_classes[j]] = {} # assiging an empty object to each value class in the root column
    print("current_tree_state version 1: ", current_tree_state)

    for c in current_tree_state:
        for k in other_features:
            current_tree_state[c][k] = [] # assiging an empty list that will contain a feature data for each value class
    print("current_tree_state version 2: ", current_tree_state)


    for feature in other_features:
        for i in range(len(ROOT_COLUMN)):
            current_tree_state[ROOT_COLUMN[i]][str(feature)].append(list(data_set[feature])[i])  # filling the data
            

    for key in current_tree_state:
        next_layer_nodes[key] = pd.DataFrame(current_tree_state[key]) 

    print("new table under each root value class ====>", current_tree_state)
    for table in next_layer_nodes:
        print("branch ", table, ":")
        print(next_layer_nodes.get(table))
    print("\n\n\n\n")
    print("STARTING TO BUILD A NEW LAYER IN THE TREE, EACH BRANCH WILL BE PROCESSES SEPERATELY:")
    print("\n\n\n\n")

    for table in next_layer_nodes:
        print("stats of the branch ", table, ":")
        print("########## RECURSION MAGIC ##########")
        current_node["children"][table] = build_tree(next_layer_nodes.get(table),latest_tree_state)
    return current_node
    