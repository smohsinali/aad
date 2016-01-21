import arff
import os
import numpy as np
import random


def cost(runtime_matrix, runtimes, permutation, cutoff):
    time = 0
    time_outs = len(runtime_matrix)

    # print(len(runtime_matrix))
    for i in range(len(runtime_matrix)):
        # print(np.average(runtime_matrix[i]))
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
        # if time >= cutoff:
        #     time_outs += 1

    # print(runtimes, time_outs)
    # print("time:%s", time)
    return time, time_outs


def find_min_timeouts(runtime_matrix, runtimes, permutation):
    steps = 100
    cutoff = 50000
    change = 1
    num_perms = 10
    time, score = cost(runtime_matrix, runtimes, permutation, cutoff)
    print("timeouts before opt:%s" % score)
    for i in range(num_perms):
        old_permutation = np.copy(permutation)
        time, old_perm_score = cost(runtime_matrix, runtimes, old_permutation, cutoff)

        permutation = swap(permutation, 3)
        for i in range(steps):
            change = random.randint(100, 1000)
            old_runtimes = np.copy(runtimes)
            # print("old runtimes:%s" % old_runtimes)
            runtimes = change_time(runtimes, change, cutoff)
            time, new_score = cost(runtime_matrix, runtimes, permutation, cutoff)
            if new_score > score:
                # print("im here")
                # print(runtimes)
                # print(old_runtimes)
                runtimes = np.copy(old_runtimes)
                # print(runtimes)
                # print("exit")
            time, score = cost(runtime_matrix, runtimes, permutation, cutoff)
            # print(permutation, runtimes, score)

        if score > old_perm_score:
            permutation = np.copy(old_perm_score)

    print("timeouts after opt:%s" % (cost(runtime_matrix, runtimes, permutation, cutoff)[1]))
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
    np.set_printoptions(formatter={"float": lambda x: "%0.0f" % x})
    scenarios = ["SAT11-INDU", "SAT11-RAND"]
    set = 1
    print("DataSet:%s" % scenarios[set])
    # random.seed(5)
    # ar = os.path.join(scenarios[set], "testing.arff")
    ar = os.path.join(scenarios[set], "algorithm_runs.arff")
    cv = os.path.join(scenarios[set], "cv.arff")
    fv = os.path.join(scenarios[set], "features_values.arff")

    # print(ar, cv, fv)
    results = arff.load(open(ar, "rb"))
    data = results["data"]

    cutoff = 5000
    num_algos = 0
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

    for i in range(num_instances):
        for j in range(num_algos):
            if data[i * num_algos + j][3] == cutoff:
                runtime_matrix[i][j] = data[i * num_algos + j][3] * 10
            else:
                runtime_matrix[i][j] = data[i * num_algos + j][3]

    oracle_time = np.zeros(num_instances)
    oracle_time = np.amin(runtime_matrix, axis=1)
    ot = np.average(oracle_time)

    seq_time = np.zeros(num_instances)
    seq_time = np.amin(runtime_matrix, axis=1) * num_algos
    np.clip(seq_time, 0, cutoff * 10, seq_time) # cutoff * 10
    # print((seq_time == 50000).sum())
    st = np.average(seq_time)

    single_best = np.zeros(num_algos)
    single_best = np.average(runtime_matrix, axis=0)
    sbt = np.amin(single_best)
    # print(single_best)

    print("Oracle:", ot)
    print("SB:", sbt)
    print("Seq. Time:", st)
    # np.savetxt("matrix.txt", runtime_matrix, fmt='%.2f')
    print("cutoff:%s*10" % cutoff)
    # print("avg runtime:%s" % (cutoff/num_algos))
    runtimes = np.zeros(len(algos))
    runtimes.fill(cutoff/len(algos))
    permutation = np.arange(len(algos))

    # runtimes = np.array([1, 7, 2])
    # permutation = np.array([0, 2, 1])

    print("\nruntime_matrix:\n%s" % runtime_matrix)
    print("initialize all runtimes to average:%s" % runtimes)

    # cost = score(runtime_matrix, runtimes, permutation, cutoff)
    # print(cost)
    #
    # first_index = random.randint(0, len(algos) - 1)
    # second_index = random.randint(0, len(algos) - 1)
    # print(first_index, second_index)
    # print(permutation)
    # permutation = swap(permutation)
    # print(permutation)
    #
    # change_time(runtimes, 2, cutoff)
    # print((np.average(runtime_matrix, axis=1) == 50000).sum())
    runtimes, permutation = find_min_timeouts(runtime_matrix, runtimes, permutation)

    print("\nResults:")
    print("algos:", algos)
    print("runtimes:%s" % (runtimes))
    print("permutation in numeric form:%s" % permutation)
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