#hear me out, more than 95% of the code is written by me, the rest was generated using LLMs.

from utils.datalab import *
from logic.algorithm import *

data_path = "./data/weather.csv"
data = preprocess_dataset(data_path)
instance = {"Outlook": "Sunny", "Temperature": "Hot", "Humidity": "High", "Windy": True}

probs = calculate_probs(instance,data,target_index=-1)

print("final probs dict:", probs)
print("classification output:", classify(probs))