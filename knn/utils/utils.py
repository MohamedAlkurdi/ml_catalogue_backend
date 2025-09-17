import math

def areSimiliar(point1,point2):
    print("brother brother brother what you do dooooingg")
    print(point1.arguments)
    print(point2.arguments)
    return len(point1.arguments) == len(point2.arguments)

def manhattan(vector1, vector2):
    distance = 0
    for i in range(len(vector1)):
        # Skip non-numeric values
        if not isinstance(vector1[i], (int, float)) or not isinstance(vector2[i], (int, float)):
            continue
        iteration = abs(vector1[i]-vector2[i])
        distance += iteration
    return distance

def eucledean(vector1, vector2):
    distance = 0
    for i in range(len(vector1)):
        # Skip non-numeric values
        if not isinstance(vector1[i], (int, float)) or not isinstance(vector2[i], (int, float)):
            continue
        difference_square = math.pow(vector1[i] - vector2[i],2)
        distance += difference_square
    return math.sqrt(distance)

def calculate_distance(point1,point2,method="eucledean"):
    if areSimiliar(point1,point2):
        vector1 = point1.arguments
        vector2 = point2.arguments
        if method.lower() == "eucledean":
            return eucledean(vector1,vector2)
        elif method.lower() == "manhattan":
            return manhattan(vector1,vector2)
        else: 
            return eucledean(vector1,vector2)
    raise Exception("Message from develeoper: check the input point, they should be two DIMENSIONALLY IDENTICAL points.")

def initial_k(length):
    root = math.sqrt(length)
    k = int(root)
    if k % 2 == 0: 
        k = k+1
    return k
