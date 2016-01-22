import arff
import os
import numpy as np
import random
import operator
from argparse import ArgumentParser


def cost(runtime_matrix, runtimes, permutation, cutoff):
    time = 0
    time_outs = len(runtime_matrix)

    for i in range(len(runtime_matrix)):
        if np.average(runtime_matrix[i]) == 50000:
            time += 50000
        else:
            for j in range(len(permutation)):
                if runtime_matrix[i, j] <= runtimes[j]:
                    time += runtime_matrix[i, j]
                    time_outs -= 1
                    break
                else:
                    time += runtimes[j]

    return time, time_outs


def find_min_timeouts(runtime_matrix, runtimes, permutation, steps, cutoff, number_of_permutations):
    num_perms = number_of_permutations
    time, score = cost(runtime_matrix, runtimes, permutation, cutoff)
    # print("timeouts before opt:%s" % score)
    for i in range(num_perms):
        old_permutation = np.copy(permutation)
        time, old_perm_score = cost(runtime_matrix, runtimes, old_permutation, cutoff)

        permutation = swap(permutation, 3)
        for i in range(steps):
            change = random.randint(100, 1000)
            old_runtimes = np.copy(runtimes)
            runtimes = change_time(runtimes, change, cutoff)
            time, new_score = cost(runtime_matrix, runtimes, permutation, cutoff)
            if new_score > score:
                runtimes = np.copy(old_runtimes)
            time, score = cost(runtime_matrix, runtimes, permutation, cutoff)

        if score > old_perm_score:
            permutation = np.copy(old_perm_score)

    return runtimes, permutation


def swap(permutation, num_times):
    for i in range(num_times):
        first_index = random.randint(0, len(permutation) - 1)
        second_index = random.randint(0, len(permutation) - 1)
        temp = permutation[first_index]
        permutation[first_index] = permutation[second_index]
        permutation[second_index] = temp

    return permutation


def change_time(runtimes, change, cutoff):
    first_index = random.randint(0, len(runtimes) - 1)
    second_index = random.randint(0, len(runtimes) - 1)
    # print
    # print(runtimes)
    indexes = [first_index, second_index]
    inc = random.randint(0, 1)
    dec = 1 - inc
    runtimes[indexes[inc]] += change
    runtimes[indexes[dec]] -= change

    if runtimes[indexes[inc]] > cutoff:
        runtimes[indexes[inc]] -= change
        runtimes[indexes[dec]] += change

    if runtimes[indexes[dec]] < 0:
        runtimes[indexes[inc]] -= change
        runtimes[indexes[dec]] += change
    # print(runtimes)
    return runtimes


if __name__ == "__main__":
    print("Ex6 Q3\nSyed Mohsin Ali\n")

    parser = ArgumentParser()
    parser.add_argument("-a", "--algoruns", dest="scenario",
                        default="SAT11-INDU", help="specify algorithm_runs.arff file")
    parser.add_argument("-f", "--features", dest="features",
                        default="SAT11-INDU", help="specify features.arff file")
    parser.add_argument("-c", "--cv", dest="cv",
                        default="SAT11-INDU", help="specify cv.arff file")
    args, unknown = parser.parse_known_args()

    np.set_printoptions(formatter={"float": lambda x: "%0.0f" % x})
    scenarios = ["SAT11-INDU", "SAT11-RAND"]
    set = 1
    # scenario = scenarios[set]
    scenario = args.scenario
    print("DataSet:%s" % scenario)
    cvr = args.cv
    fer = args.features

    ar = os.path.join(scenario, "algorithm_runs.arff")
    cv = os.path.join(scenario, "cv.arff")
    fv = os.path.join(scenario, "features_values.arff")

    results = arff.load(open(ar, "rb"))
    data = results["data"]

    folds_info = arff.load(open(cv, "rb"))
    folds_info = folds_info["data"]

    # print(folds_info)

    folds_dict = dict()
    for i in range(len(folds_info)):
        folds_dict[folds_info[i][0]] = folds_info[i][2]

    folds_dict = sorted(folds_dict.items(), key=operator.itemgetter(1))
    print(len(folds_dict))

    cutoff = 5000
    steps = 100
    number_of_permutations = 10

    num_algos = 0
    algos = dict()
    for i, d in enumerate(data):
        if data[i][2] not in algos.values():
            algos[i] = data[i][2]
        else:
            break

    instances = dict()
    # print(data)
    k = 0
    for i, d in enumerate(data):
        if data[i][0] not in instances:
            instances[data[i][0]] = k
            k += 1

    print(len(instances))

    num_algos = len(algos)
    num_instances = len(data) / num_algos
    # print(len(algos))
    # print(num_instances)
    runtime_matrix = np.zeros((num_instances, num_algos))

    for i in range(num_instances):
        for j in range(num_algos):
            if data[i * num_algos + j][3] == cutoff:
                runtime_matrix[i][j] = data[i * num_algos + j][3] * 10
            else:
                runtime_matrix[i][j] = data[i * num_algos + j][3]



    best_algos = list()
    differences = list()
    for i in range(num_instances):
        for j in range(num_algos):
            # taking pairwise difference
            differences.append(runtime_matrix[i, j] * num_algos - np.sum(runtime_matrix[i]))
        # print(differences)
        best_algos.append(differences.index(min(differences)))
        differences = list()
    best_algos = np.array(best_algos)
    print("best algos:", best_algos)

    # now prepare train_x and train_y matrices for ML
    train_x = np.zeros((num_instances, num_algos))
    train_y = np.zeros(num_instances)
    k = 0
    for name, fold_id in folds_dict:
        index = instances[name]
        # print(index, fold_id)
        train_x[k] = runtime_matrix[index]
        train_y[k] = best_algos[index]
        k += 1
        # print(index)

    print(k)



