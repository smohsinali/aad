from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.cross_validation import KFold
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("Exercise 5\nSyed Mohsin Ali")

    dataSet = "set1"
    trainingDataX = np.loadtxt(dataSet + "/x_train.np")
    trainingDataY = np.loadtxt(dataSet + "/y_train.np")
    testData = np.loadtxt(dataSet + "/x_test.np")

    kf = KFold(len(trainingDataX), 10)
    fold = 0
    for train, test in kf:
        fold += 1
        print
        print("fold:", fold)
        clf = RandomForestClassifier(n_estimators=1, criterion="gini", max_features="auto", warm_start=True)
        # clf = RandomForestClassifier(n_estimators=20, criterion="entropy", max_features=None, warm_start=True)
        for n_trees in range(1, 21):
            clf.set_params(n_estimators=n_trees)
            clf.fit(trainingDataX[train], trainingDataY[train])
            y_test = clf.predict(trainingDataX[test])
            accuracy = metrics.accuracy_score(trainingDataY[test], y_test)
            print("n_estiamtor:", n_trees, "accuracy:",accuracy)
