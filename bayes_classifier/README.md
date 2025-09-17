# Naive Bayes Classifier

This project is a simple implementation of the **Naive Bayes Classification Algorithm** written in Python from scratch. It works on categorical datasets (like the weather dataset) and uses probability theory to predict a class label based on feature values.

---

## What is Naive Bayes?

Naive Bayes is a probabilistic classifier based on Bayes’ Theorem, assuming feature independence:

```

P(Class | Features) ∝ P(Class) × Π P(Feature\_i | Class)

```

This algorithm is widely used for text classification, spam filtering, and many basic decision-making systems.

---

## Functions Overview

### In `datalab.py` (Data Preprocessing)

- **`preprocess_dataset(path)`**  
  Loads CSV, drops ID columns if present.

- **`equivalent_target_values(feature_values, feature_column, target_column)`**  
  Builds a dictionary showing how often each target value appears for every feature value.

- **`target_column(data, index=-1)`**  
  Extracts the target column from the dataset (default is the last column).

- **`extract_unique_values(column)`**  
  Returns unique values in a list.

- **`to_python_type(value)`**  
  Converts NumPy types to native Python types for comparison.

- **`validate_instance(instance, dataset)`**  
  Checks if a prediction instance has matching format and data types with the dataset.

---

### In `algorithm.py` (Naive Bayes Logic)

- **`target_values_share(target_column)`**  
  Counts how many times each target class appears.

- **`calculate_prior_probs(data, target_index=-1)`**  
  Calculates P(feature | class) probabilities using the dataset.

- **`calculate_probs(instance, data)`**  
  Computes final probabilities P(class | instance) for each class.

- **`classify(probs)`**  
  Returns the class label with the highest probability.

---

## How to Run

1. Place your dataset in the `data/` folder.
2. Adjust the instance you want to classify in `client.py`.
3. Run the project:

```bash
python client.py
````

---

## Example Output

```
root current prob: 0.6428571428571429
root current prob: 0.35714285714285715
final probs dict: {'Yes': 0.00352, 'No': 0.0411}
classification output: No
```

---

## Notes

* Assumes all features are categorical.
* Handles only classification problems with discrete classes.
* Code is written and structured for learning purposes — clear and modular.

---