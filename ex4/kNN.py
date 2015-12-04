"""
class for kNN
"""

import numpy as np
import cmath
from sklearn import preprocessing

class KNN:

    def __init__(self):
        self.true = True

    def kNN_train(self, x_train, y_train, x_test, k = 5, processing = None, distMethod = "Manhattan"):
        """
        returns y_test (prediction on x_test)
        """
        y_test = list()

        if processing == "Scalar":
            # print("Preprocessing = Scalar")
            stdScalar = preprocessing.StandardScaler().fit(x_train)
            x_train = stdScalar.transform(x_train)
            x_test = stdScalar.transform(x_test)

        elif processing == "MinMax":

            # print("Preprocessing = MinMax")
            mmScalar = preprocessing.MinMaxScaler()
            x_train = mmScalar.fit_transform(x_train)
            x_test = mmScalar.fit_transform(x_test)

        elif processing == "None":
            self.true = True
            # print("No Preprocessing")

        else:
            print("wrong processing")
            exit()

        for i in range(0, len(x_test)):
            y_test_temp = list()
            zeroCount = 0
            oneCount = 0

            # find distance of a instance in test test to all instances in training set
            for j in range(0, len(x_train)):
                if distMethod == "Manhattan":
                   y_test_temp.append(self.manhattan(x_train[j], x_test[i]))
                elif distMethod == "Euclidean":
                   y_test_temp.append(self.euclidean(x_train[j], x_test[i]))
                else:
                    print "something wrong with distance calculation"
                    exit()

            # take indices of k nearest points
            # print y_test_temp
            temp = np.asarray(y_test_temp).argsort()[:k]
            # check class of each of k nearest points
            for tmp in temp:
                if y_train[tmp] == 0:
                    zeroCount += 1
                elif y_train[tmp] == 1:
                    oneCount += 1
                else:
                    print("something wrong in counting")

            # classify
            if zeroCount >= oneCount:
                y_test.append(int(0))
            elif oneCount > zeroCount:
                y_test.append(int(1))
            else:
                print("somethign wrong")

        # print y_test
        return y_test

    @staticmethod
    def euclidean(x, y):
        """
        find euclidean dist b/w arrays x & y
        >>> KNN.euclidean(np.array([0, 0]), np.array([3, 4]))
        5.0
        """
        ed = np.sqrt(np.sum((x-y)**2))
        # print ed
        return ed

    @staticmethod
    def manhattan(x, y):
        """
        find manhattn dist b/w arrays x & y
        >>> KNN.manhattan(np.array([-2, 1]), np.array([3, -4]))
        10
        """
        md =  np.sum(abs(x-y))
        # print md
        return md
