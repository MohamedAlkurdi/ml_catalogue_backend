import pandas as pandas
import sys
sys.path.append('..')
from utils.utils import *
from utils.c45Utils import *

class DesicionTree:
    def __init__(self, dataset="missing dataset"):
        self.dataset = dataset
        self.target_index = 0
        if isinstance(dataset, str) or dataset is None:
            raise Exception("MESSAGE FROM DEVELOPER: PROVIDE A VALID DATASET (pandas DataFrame)")

    def build_tree(self):
        dataset = self.dataset
        print("========== DATA ==========")
        print(dataset)
        print("========== ==== ==========")

        continuous_features = check_continuous_columns(dataset)
        if continuous_features: 
            categorized_columns = handle_continuous_table(dataset)
            dataset = merge_categorized_columns(categorized_columns, dataset)

        current_node = {
        'feature':None,
        'prediction':None,
        "children":{}
        }
        
        next_layer_nodes = {}
        
        self.target_index = len(dataset.columns) - 1
        dataset_processing_output = process_table(dataset)
        is_leaf = dataset_processing_output.get('is_leaf')
        
        if is_leaf:
            target_values = dataset.iloc[:,self.target_index]
            majority_class = target_values.mode()[0] 
            print(f"Reached leaf node ... Prediction: {majority_class}")
            current_node["prediction"] = majority_class
            current_node["feature"] = None
            current_node['children']={}
            return majority_class
        
        table_processing_output_value = dataset_processing_output.get('value')
        current_node["feature"] = table_processing_output_value

        ROOT_COLUMN = dataset[table_processing_output_value]
        ROOT_COLUMN = list(ROOT_COLUMN)
        ROOT_CLASSES = list(set(ROOT_COLUMN))
        
        print("\n\n\n\n\n THE FEATURE THAT SHOULD BE EXECLUDED: ",table_processing_output_value," \n\n\n\n\n")
        other_features = execlude_root_feature(dataset, table_processing_output_value)
        
        current_tree_state = {}
        
        print("!!!!!!!!!!!splitting the data table depending on ",table_processing_output_value," columns as the Root!!!!!!!!!!!")
        
        for i in range(len(ROOT_CLASSES)):
            current_tree_state[ROOT_CLASSES[i]] = {}
        
        for c in current_tree_state:
            for f in other_features:
                current_tree_state[c][f] = []
        print("current_tree_state version 1: ", current_tree_state)
        
        for feature in other_features:
            for j in range(len(ROOT_COLUMN)):
                current_tree_state[ROOT_COLUMN[j]][str(feature)].append(list(dataset[feature])[j])

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
            
            self.dataset = next_layer_nodes.get(table)
            current_node["children"][table] = self.build_tree()
        return current_node



