import numpy as np
import matplotlib.pyplot as plt
from kNN import KNN
from sklearn import metrics
from sklearn.cross_validation import KFold


def call_kNN(set, k, processing, distMethod):
    """
    used for calling kNN with all possible configs
    """

    trainingDataX = np.loadtxt("mload_ml_sets/" + set + "/x_train.np")
    trainingDataY = np.loadtxt("mload_ml_sets/" + set + "/y_train.np")
    testData = np.loadtxt("mload_ml_sets/" + set + "/x_test.np")

    kNN = KNN()

    score = list()
    kf = KFold(len(trainingDataX), 10)

    for train, test in kf:
        y_test = kNN.kNN_train(trainingDataX[train], trainingDataY[train], trainingDataX[test], k, processing, distMethod)
        acc = metrics.accuracy_score(trainingDataY[test], y_test)
        score.append(acc)

    avgScore = sum(score)/len(score)
    print ("k = %s : avg. score = %s" %(k, avgScore))

    return k, avgScore
    # np.savetxt("mload_ml_sets/" + set + "/y_test.np", y_test, "%d")

if __name__ == "__main__":
    print("ex:4\nSyed Mohsin Ali\n")

    k = 1
    processing = ["MinMax", "Scalar", "None"]
    distMethod = ["Euclidean", "Manhattan"]

    # processing = ["MinMax"]
    # distMethod = ["Euclidean"]

    print
    sets = ["set2"]

    # looping over all possible configs
    for set in sets:
        plot_k = list()
        plot_score = list()
        print "set:", set
        for pro in processing:
            print "Preprocessing = ", pro
            for dist in distMethod:
                print "Distance Metric = ", dist
                for k in range(1,34):
                    t_k, t_score = call_kNN(set, k, pro, dist)
                    plot_k.append(t_k)
                    plot_score.append(t_score)
        plt.plot(plot_k, plot_score)
        plt.ylabel("score")
        plt.xlabel("k")
        plt.show()

        raw_input('press return to continue')

