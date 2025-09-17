from functional_implementation.functional_decision_tree import *
from models.DecisionTree import *
import pandas as pd

# data = pd.read_csv("./data/simple_data.csv", index_col=False)
# data = pd.read_csv("./data/weather.csv", index_col=False)
# data = pd.read_csv('./data/data_example.csv', index_col=False)
data = pd.read_csv('./data/dummy.csv')

# option1:
decision_tree = build_tree(data, {})


#option2:
tree = DesicionTree(data)
result_node = tree.build_tree()

print("\n\n")
print(data)
print("\n")
print("\nDecision Tree Output Structure\n\n")
# print(decision_tree) #option1
print(result_node) #option2




