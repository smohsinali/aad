"""
script for running auto sklearn in Question 3
"""

import autosklearn
import numpy as np

if __name__ == "__main__":

    trainingDataX = np.loadtxt("mload_ml_sets/set1/x_train.np")
    trainingDataY = np.loadtxt("mload_ml_sets/set1/y_train.np")

    classifier = autosklearn.AutoSklearnClassifier()
    classifier.fit(trainingDataX, trainingDataY)
    print(classifier.show_models())