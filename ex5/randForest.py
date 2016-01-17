from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.cross_validation import KFold
import numpy as np
import copy
import matplotlib.pyplot as plt


def plot_learningcurve(scores):
    n_iters = scores.shape[1]
    max_trees = scores.shape[0]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range(1, max_trees + 1), np.mean(scores, axis=1))
    ax.axis([1, max_trees, 0.65, 0.85])
    plt.xlabel("n_estimators")
    plt.ylabel("Accuracy")
    plt.title("Training Accuracy")
    ax.fill_between(range(1, max_trees + 1),
                    np.mean(scores, axis=1) + np.std(scores, axis=1),
                    np.mean(scores, axis=1) - np.std(scores, axis=1),
                    facecolor="yellow",
                    alpha=0.2)
    ax.set_yticks(np.arange(0.65, 0.85, 0.01))
    ax.set_yticklabels(np.arange(0.65, 0.85, 0.01))

    ax.set_xticks(np.arange(1, max_trees, 1))
    ax.set_xticklabels(np.arange(1, max_trees, 1))
    print(np.arange(1, max_trees, 1))
    plt.savefig('learningcurve.png')


def plot_qrd(scores):
    n_iters = scores.shape[1]
    max_trees = scores.shape[0]
    probs = np.zeros(max_trees)

    for i in range(max_trees):
        print("i:", i, "prob:", np.where(scores[i] >= 0.76)[0])
        probs[i] = len(np.where(scores[i] >= 0.76)[0])/float(n_iters)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.xlabel("n_estimators")
    plt.ylabel("p(x)<0.76")
    # ax.axis([1, 20, 0.60, 0.95])
    ax.plot(range(1, max_trees + 1), probs)
    plt.savefig('qrd.png')

    print(probs)


def train_forest(classifier, trainingDataX, trainingDataY, testDataX, testDataY, num_iterations, max_trees):
    scores_train = np.zeros((max_trees, num_iterations))
    scores_test = np.zeros((max_trees, num_iterations))
    train = 4000
    for i in range(num_iterations):
        clf = copy.deepcopy(classifier)
        for n_tree in range(1, max_trees+1):
            # print(i, n_tree)
            clf.set_params(n_estimators=n_tree)
            clf.fit(trainingDataX[0:train], trainingDataY[0:4000])
            y_test = clf.predict(testDataX)
            x_test = clf.predict(trainingDataX[4000:])

            accuracy = metrics.accuracy_score(testDataY, y_test)
            scores_test[n_tree-1][i] = accuracy
            accuracy = metrics.accuracy_score(trainingDataY[4000:], x_test)
            scores_train[n_tree-1][i] = accuracy
    return scores_train,scores_test

if __name__ == "__main__":
    print("Exercise 5\nSyed Mohsin Ali")

    np.set_printoptions(formatter={"float": lambda x: "%0.4f" % x})
    dataSet = "set4"
    trainingDataX = np.loadtxt("ml_set/" + dataSet + "/x_train.np")
    trainingDataY = np.loadtxt("ml_set/" + dataSet + "/y_train.np")
    testDataX = np.loadtxt("ml_set/" + dataSet + "/x_test.np")
    testDataY = np.loadtxt("ml_set/" + dataSet + "/y_test.np")
    # a = np.array(([1, 2, 3, 4],[2, 4, 5]))
    # print("sum a:", sum(a[1]))
    num_iterations = 3
    max_trees = 20

    #clf = RandomForestClassifier(n_estimators=1, criterion="gini", max_features="auto", warm_start=True)
    clf = RandomForestClassifier(n_estimators=20, criterion="entropy", max_features=None, warm_start=True)

    scores_train,scores_test = train_forest(clf, trainingDataX, trainingDataY, testDataX, testDataY, num_iterations, max_trees)

    print(scores_train)
    print(scores_test)

    # plot_learningcurve(scores_train)
    # plot_learningcurve(scores_test)
    # plot_qrd(scores_train)
    plot_qrd(scores_test)


