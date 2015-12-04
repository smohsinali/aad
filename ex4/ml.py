import sys
import numpy as np
from sklearn import preprocessing
from sklearn import svm
from sklearn import metrics
from sklearn.cross_validation import KFold

if __name__ == "__main__":
    print("ex:4\nSyed Mohsin Ali\nQuestion 4 : ML Competition\n")
    if(len(sys.argv) < 4):
        print "usage: python ml.py x_train.np y_train.np x_test.np"

    print "first arg: ", sys.argv[1]
    print "second arg: ", sys.argv[2]
    print "third arg: ", sys.argv[3]

    trainingDataX = np.loadtxt(sys.argv[1])
    trainingDataY = np.loadtxt(sys.argv[2])
    testDataX = np.loadtxt(sys.argv[3])

    # print("Preprocessing = Scalar")
    stdScalar = preprocessing.StandardScaler().fit(trainingDataX)
    trainingDataX = stdScalar.transform(trainingDataX)
    testDataX = stdScalar.transform(testDataX)

    clf = svm.SVC(kernel="rbf", gamma=.69)
    clf.fit(trainingDataX, trainingDataY)

    y_test = clf.predict(testDataX)
    np.savetxt("y_test.np", y_test, "%d")

    # kf = KFold(len(trainingDataX), 10)
    # score = list()
    # for train, test in kf:
    #     clf.fit(trainingDataX[train], trainingDataY[train])
    #     y_test = clf.predict(trainingDataX[test])
    #     score.append(metrics.accuracy_score(trainingDataY[test], y_test))
