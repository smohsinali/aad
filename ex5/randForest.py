from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.cross_validation import KFold
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    print("Exercise 5\nSyed Mohsin Ali")

    np.set_printoptions(formatter={"float": lambda x: "%0.4f" % x})

    dataSet = "set4"
    trainingDataX = np.loadtxt("ml_set/" + dataSet + "/x_train.np")
    trainingDataY = np.loadtxt("ml_set/" + dataSet + "/y_train.np")
    testData = np.loadtxt("ml_set/" + dataSet + "/x_test.np")
    # a = np.array([1,2,3,4])

    kf = KFold(len(trainingDataX), 10)
    fold = 0
    max_trees = 20
    for train, test in kf:
        fold += 1
        print
        print("fold:", fold)
        clf = RandomForestClassifier(n_estimators=1, criterion="gini", max_features="auto", warm_start=True)
        # clf = RandomForestClassifier(n_estimators=20, criterion="entropy", max_features=None, warm_start=True)
        scores = np.zeros(max_trees)
        # print("initialize scores:", scores)
        for n_tree in range(1, max_trees+1):
            clf.set_params(n_estimators=n_tree)
            clf.fit(trainingDataX[train], trainingDataY[train])
            y_test = clf.predict(trainingDataX[test])
            accuracy = metrics.accuracy_score(trainingDataY[test], y_test)
            scores[n_tree-1] = accuracy
            print("n_estiamtor:", n_tree, "accuracy:", accuracy, "avg.:", np.mean(scores[0: n_tree]), "stdDev:", np.std(scores[0: n_tree]))
        print("scores:", scores)

