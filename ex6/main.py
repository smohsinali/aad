import arff
import os
import numpy as np

if __name__ == "__main__":
    print("Ex6 Q1\nSyed Mohsin Ali\n")
    np.set_printoptions(formatter={"float": lambda x: "%0.5f" % x})
    scenarios = ["SAT11-INDU", "SAT11-RANDU"]
    set = 0
    ar = os.path.join(scenarios[set], "algorithm_runs.arff")
    cv = os.path.join(scenarios[set], "cv.arff")
    fv = os.path.join(scenarios[set], "features_values.arff")

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
    seq_time = np.zeros(num_instances)
    seq_time = np.amin(runtime_matrix, axis=1) * num_algos
    np.clip(seq_time, 0, 50000, seq_time)

    ot = np.average(oracle_time)
    st = np.average(seq_time)
    print("Oracle:", ot)
    print("SB:", st)
