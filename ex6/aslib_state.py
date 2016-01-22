import arff
import os
import numpy as np
from argparse import ArgumentParser


if __name__ == "__main__":
    print("Ex6 Q1\nSyed Mohsin Ali\n")
    parser = ArgumentParser()
    parser.add_argument("-a", "--algoruns", dest="scenario",
                        default="SAT11-INDU/algorithm_runs.arff", help="specify algorithm_runs.arff file")
    args, unknown = parser.parse_known_args()

    np.set_printoptions(formatter={"float": lambda x: "%0.0f" % x})
    scenarios = ["SAT11-INDU", "SAT11-RAND"]
    set = 1
    # scenario = scenarios[set]
    scenario = args.scenario
    print("DataSet:%s\n" % scenario)

    ar = args.scenario
    # print(ar, cv, fv)
    results = arff.load(open(ar, "rb"))
    data = results["data"]

    num_algos = 0
    algos = list()
    for i, d in enumerate(data):
        # print("here:", i)
        if data[i][2] not in algos:
            algos.append(data[i][2])
        else:
            break

    num_algos = len(algos)
    num_instances = len(data) / num_algos

    runtime_matrix = np.zeros((num_instances, num_algos))

    for i in range(num_instances):
        for j in range(num_algos):
            if data[i * num_algos + j][3] == 5000:
                runtime_matrix[i][j] = data[i * num_algos + j][3] * 10
            else:
                runtime_matrix[i][j] = data[i * num_algos + j][3]

    oracle_time = np.zeros(num_instances)
    oracle_time = np.amin(runtime_matrix, axis=1)
    ot = np.average(oracle_time)

    seq_time = np.zeros(num_instances)
    seq_time = np.amin(runtime_matrix, axis=1) * num_algos
    np.clip(seq_time, 0, 50000, seq_time)
    st = np.average(seq_time)

    single_best = np.zeros(num_algos)
    single_best = np.average(runtime_matrix, axis=0)
    sbt = np.amin(single_best)
    # print(single_best)

    print("Oracle:", ot)
    print("SB:", sbt)
    # print("Seq. Time:", st)
    # np.savetxt("matrix.txt", runtime_matrix, fmt='%.2f')

