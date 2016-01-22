import arff
import os
import numpy as np
import random
from argparse import ArgumentParser


def cost(runtime_matrix, runtimes, permutation, cutoff):
    # returns number of timeouts and total time taken by given schedule deefined by runtimes and permutation
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
    # this is implementation of walkSAT
    # there are two loops, outer loop changes permutations and inner loop changes runtimes
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

    # print("timeouts after opt:%s" % (cost(runtime_matrix, runtimes, permutation, cutoff)[1]))
    return runtimes, permutation


def swap(permutation, num_times):
    # this function is used to find random permutations of schedule by swapping any two random indexes
    # run this multiple times to find different permutations with large variance
    for i in range(num_times):
        first_index = random.randint(0, len(permutation) - 1)
        second_index = random.randint(0, len(permutation) - 1)
        temp = permutation[first_index]
        permutation[first_index] = permutation[second_index]
        permutation[second_index] = temp

    return permutation


def change_time(runtimes, change, cutoff):
    # this function randomly selects two inxes and change their times by increasing one value and decreasing other
    # it also takes care of keeping runtimes within bounds
    first_index = random.randint(0, len(runtimes) - 1)
    second_index = random.randint(0, len(runtimes) - 1)
    # print
    # print(runtimes)
    indexes = [first_index, second_index]
    inc = random.randint(0, 1)
    dec = 1 - inc
    # print("indexes getting their times changed:[%s, %s]" % (first_index, second_index))
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
    print("Ex6 Q2\nSyed Mohsin Ali\n")

    parser = ArgumentParser()
    parser.add_argument("-a", "--algoruns", dest="scenario",
                        default="SAT11-RAND/algorithm_runs.arff", help="specify algorithm_runs.arff file")
    args, unknown = parser.parse_known_args()

    np.set_printoptions(formatter={"float": lambda x: "%0.0f" % x})
    scenarios = ["SAT11-INDU", "SAT11-RAND"]
    set = 1
    # scenario = scenarios[set]
    scenario = args.scenario
    print("DataSet:%s" % scenario)

    ar = args.scenario
    cv = os.path.join(scenario, "cv.arff")
    fv = os.path.join(scenario, "features_values.arff")

    results = arff.load(open(ar, "rb"))
    data = results["data"]

    cutoff = 5000
    steps = 100
    number_of_permutations = 10

    num_algos = 0
    # finding names of all algorithms
    algos = dict()
    for i, d in enumerate(data):
        # print("here:", i)
        if data[i][2] not in algos.values():
            algos[i] = data[i][2]
        else:
            break

    num_algos = len(algos)
    num_instances = len(data) / num_algos
    # print(len(algos))
    # print(num_instances)
    runtime_matrix = np.zeros((num_instances, num_algos))

    # creating runtime matrix as shown in lecture slides
    for i in range(num_instances):
        for j in range(num_algos):
            if data[i * num_algos + j][3] == cutoff:
                runtime_matrix[i][j] = data[i * num_algos + j][3] * 10
            else:
                runtime_matrix[i][j] = data[i * num_algos + j][3]

    runtimes = np.zeros(len(algos))
    runtimes.fill(cutoff/len(algos))
    permutation = np.arange(len(algos))

    # calling a implementation of WalkSAT
    runtimes, permutation = find_min_timeouts(runtime_matrix, runtimes, permutation, steps, cutoff, number_of_permutations)

    assignment = dict()
    perm = list()
    for i in range(num_algos):
        assignment[algos[i]] = runtimes[i]
        perm.append(algos[permutation[i]])
    print
    print("assignment:", assignment)
    print("permutation:", perm)
    time, score = cost(runtime_matrix, runtimes, permutation, cutoff)
    print("average time ater optimization:", time/num_instances)