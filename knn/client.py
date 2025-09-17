from utils.datalab import *
from models.Point import *
from models.Knn import *
from functional_implementation.build_knn import *

# test_point = Point(13.08,15.71,85.63,520,0.1075,0.127,0.04568,0.0311,0.1967,0.06811,0.1852,0.7477,1.383,14.67,0.004097,0.01898,0.01698,0.00649,0.01678,0.002425,14.5,20.49,96.09,630.5,0.1312,0.2776,0.189,0.07283,0.3184,0.08183, target="target")
test_point = Point(110,1,0.3,0.1, target="genre")


# ===== functional implementation demo ===== #
# data = process_data('./demo.csv')
data = process_data('./data.csv')
best_k = evaluate(data)
prediction = predict(test_point, data, best_k)

print("\ninput point:\n",test_point.arguments)
print("\ndiagnosis prediction:",prediction)


# ===== OOP demo ===== #
# knn = KNN('./demo.csv')
# best_k = knn.evalute()
# prediction = knn.predict(test_point, best_k)

#Note: best_k variable can be replaced with any value, but using it ensures good results.
