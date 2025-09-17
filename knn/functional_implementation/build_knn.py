from knn.utils.utils import *
from knn.utils.datalab import *
from knn.models.Point import *


def compute_distances(input, dataset, target_index = -1, method="eucledean"):
    other_points = extract_points(dataset, target_index)
    distances = []
    for point in other_points:
        distance = calculate_distance(input, point,method)
        point_informations = {
            "distance": distance,
            "target": point.target,
        }
        distances.append(point_informations)
    distances.sort(key=lambda x: x["distance"])
    return distances

def classification(distances, K):
    neighbors_lables = []
    max_freq = {"value": 0, "target": None}

    for i in range(K):
        neighbors_lables.append(distances[i].get("target"))
    
    freqs = classes_frequencies(neighbors_lables)
    
    for i in freqs:
        if freqs[i] > max_freq["value"]:
            max_freq["value"] = freqs[i]
            max_freq["target"] = i

        
    # print("Classification Result:", max_freq["target"])
    return max_freq["target"]

def regression(distances, K):
    neighbors_values = []

    for i in range(K):
        neighbors_values.append(distances[i].get("target"))

    regression = 0

    for value in neighbors_values:
        regression += value

    # print("Regression Result:", regression)
    return regression / K 

def predict(input, dataset, K, target_index = -1, method="eucledean"):
    
    distances = compute_distances(input, dataset, target_index, method)

    if len(distances) == 0:
        raise Exception("Message from developer: dataset is empty.")
    
    if K > len(distances):
        print("Message from developer: K is larger than the number of points, automatically set K to the number of points.")
        K = len(distances)
    
    if is_convertible_to_numeric(distances[0].get("target")):
        return {"operation_type":"regression", "result":regression(distances, K)}
    else:
        return {"operation_type":"classification", "result":classification(distances ,K)}

def evaluate(dataset, test_fraction=0.3):
    """
    This function returns the best K value and the error rates of a set of K candidates.
    """
    error_rate = 0
    K = initial_k(len(dataset))
    print("inital K:", K)
    print("fraction:", test_fraction)
    
    best_k_candidates = [K, K+2 ,K+4 ,K+6]
    stats = []
    temp_K = K
    for i in range(3):
        if temp_K-2 > 0:
            temp_K = temp_K-2
            best_k_candidates.append(temp_K)

    print("best K candidates:", best_k_candidates)

    test_set = dataset.sample(frac=test_fraction, random_state=1)
    test_points = extract_points(test_set)
    train_set = dataset.drop(test_set.index)
    for candidate in best_k_candidates:
        error_rate = 0
        for point in test_points:
            prediction = predict(point,train_set,candidate)
            if prediction != point.target:
                error_rate +=1
        stats.append({candidate:(error_rate*100)/len(test_points)})
    print("\nError rate stats:",stats)
    best_k = min(stats, key = lambda x: list(x.values())[0])
    print("\nbest k:", best_k)
    # you can return the stats as well if you want, I didn't to keep it simple.
    return list(best_k.keys())[0]

