from knn.models import Point
from knn.utils.datalab import *
from knn.utils.utils import *

class KNN:
    def __init__(self, path, target_index = -1, method="eucledean"):
        self.dataset = process_data(path)
        self.target_index = target_index
        self.method = method
        self.distances = []
    
    def compute_distances(self,input=Point()):
        other_points = extract_points(self.dataset, self.target_index)
        distances = []
        for point in other_points:
            distance = calculate_distance(input, point,self.method)
            point_informations = {
                "distance": distance,
                "target": point.target,
            }
            distances.append(point_informations)
        distances.sort(key=lambda x: x["distance"])
        self.distances = distances
        return distances

    def __classification(self,K):
        neighbors_lables = []
        max_freq = {"value": 0, "target": None}
        
        for i in range(K):
            neighbors_lables.append(self.distances[i].get("target"))
        
        freqs = classes_frequencies(neighbors_lables)
        
        for i in freqs:
            if freqs[i] > max_freq["value"]:
                max_freq["value"] = freqs[i]
                max_freq["target"] = i
        
        return max_freq["target"]

    def __regression(self, K):
        neighbors_values = []
        
        for i in range(K):
            neighbors_values.append(self.distances[i].get("target"))
        
        regression = 0
        
        for value in neighbors_values:
            regression += value
        
        return regression / K
    
    def predict(self,input, K):
        self.compute_distances(input)
        
        if len(self.distances) == 0:
            raise Exception("Message from developer: dataset is empty.")
        
        if K > len(self.distances):
            print("Message from developer: K is larger than the number of points, automatically set K to the number of points.")
            K = len(self.distances)
        
        if is_convertible_to_numeric(self.distances[0].get("target")):
            return self.__regression(K)
        else:
            return self.__classification(K)

    def evalute(self, test_fraction=0.3):
        
        error_rate = 0
        K = initial_k(len(self.dataset))
        print("inital K:", K)
        print("fraction:", test_fraction)
        
        best_k_candidates = [K, K+2 ,K+4 ,K+6]
        stats = []
        temp_K = K
        for i in range(3):
            if temp_K-2 > 0:
                temp_K = temp_K-2
                best_k_candidates.append(temp_K)
        
        test_set = self.dataset.sample(frac=test_fraction, random_state=1)
        test_points = extract_points(test_set)
        train_set = self.dataset.drop(test_set.index)

        original_dataset = self.dataset
        self.dataset = train_set

        for candidate in best_k_candidates:
            error_rate = 0
            for point in test_points:
                prediction = self.predict(point,candidate)
                if prediction != point.target:
                    error_rate +=1
            stats.append({candidate:(error_rate*100)/len(test_points)})
        self.dataset = original_dataset
        # you can return the stats as well if you want, I didn't to keep it simple.
        best_k = min(stats, key = lambda x: list(x.values())[0])
        return list(best_k.keys())[0]