from CNF import CNF
from Solver import Solver
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import plot_scatter as ps

def format_output(variables):
    vals = list()

    for i in variables:
        if variables[i] == False:
            vals.append(-i)
        else:
            vals.append(i)

    return vals

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <file>")
        # sys.exit()
    # file_name = sys.argv[1]
    np.set_printoptions(formatter={"float": lambda x: "%0.4f" % x})
    satisfiable = False
    dataSets = ["cnf_exercise5/random_ksat(1).dimacs",
                "cnf_exercise5/random_ksat(2).dimacs",
                "cnf_exercise5/random_ksat(3).dimacs",
                "cnf_exercise5/random_ksat(4).dimacs",
                "cnf_exercise5/random_ksat(5).dimacs",
                "cnf_exercise5/random_ksat(6).dimacs",
                "cnf_exercise5/random_ksat(7).dimacs",
                "cnf_exercise5/random_ksat(8).dimacs",
                "cnf_exercise5/random_ksat(9).dimacs",
                "cnf_exercise5/random_ksat(10).dimacs",
                "cnf_exercise5/random_ksat(11).dimacs",
                "cnf_exercise5/random_ksat(12).dimacs",
                # "cnf_exercise5/random_ksat(13).dimacs",
                # "cnf_exercise5/random_ksat(14).dimacs",
                ]
    # dataSets = ["cnf_exercise5/random_ksat(6).dimacs"]
    # class Solver contain algorithms URW, WalkSAT, TabuSearch and their helper functions
    solver = Solver()
    # class CNF handles files, create datastructures for CNFs and provide function to check if formula is satisfied
    cnf = CNF()
    num_runs = 20
    time_matrix1= np.zeros((len(dataSets), num_runs))
    time_matrix2= np.zeros((len(dataSets), num_runs))

    for j, dataSet in enumerate(dataSets):
        print("\nFor dataset:", dataSet)
        for run in range(num_runs):

            print("\nRun#:",run, "For dataset:",dataSet)
            file_name = dataSet

            solver = Solver()
            cnf = CNF()
            cnf.read_dimacs_file(file_name)

            start = time.clock()
            satisfiable = solver.WalkSAT(cnf, 200)
            end = time.clock()

            if satisfiable:
                print("s SATISFIABLE:")
                print("v", format_output(cnf.variable_values))
            else:
                print("Cannot find Solution")

            print("Time taken:%2.4f" % (end - start), "secs")
            time_matrix1[j][run] = end - start
            del cnf
            del solver
            satisfiable = False

    for j, dataSet in enumerate(dataSets):
        print("\nFor dataset:", dataSet)
        for run in range(num_runs):

            print("\nRun#:",run, "For dataset:",dataSet)
            file_name = dataSet

            solver = Solver()
            cnf = CNF()
            cnf.read_dimacs_file(file_name)

            start = time.clock()
            satisfiable = solver.tabuSearch(cnf, 200, 5)
            end = time.clock()

            if satisfiable:
                print("s SATISFIABLE:")
                print("v", format_output(cnf.variable_values))
            else:
                print("Cannot find Solution")

            print("Time taken:%2.4f" % (end - start), "secs")
            time_matrix2[j][run] = end - start
            del cnf
            del solver
            satisfiable = False

    print("\nRuntimes, each columns show timetaken on one of iterations and row shows datasets.\n"
          "Eg. row 0 column 3 show time taken to solve first dataset on 4th iteration\n")
    print(time_matrix1)
    print(time_matrix2)
    tm1_avg = np.mean(time_matrix1, axis=1)
    tm2_avg = np.mean(time_matrix2, axis=1)

    print(tm1_avg)
    print(tm2_avg)
    plt.hist(time_matrix1[0], bins=40, normed=True, cumulative=True, histtype='step', color='b', label='WalkSAT')
    plt.hist(time_matrix2[0], bins=40, normed=True, cumulative=True, histtype='step', color='r', label='TabuSearch')
    plt.title("WalkSat vs TabuSearch")
    plt.xlabel("TimeTaken in Secs")
    plt.ylabel("Probability")
    plt.legend()
    plt.savefig('sls_runtime.png')
    ps.plot_scatter_plot(tm1_avg, tm2_avg,labels=["WalkSat", "Tabu"], title="WalkSat vs TabuSearch",
                         save="ps.png", debug=False, min_val=0, max_val=0.6, grey_factor=1,
                         linefactors=None, user_fontsize=20, dpi=200)
    data = [tm1_avg, tm2_avg]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.ylabel("Runtime Ratio")
    ax.boxplot(data)
    ax.set_xticklabels(["WalkSat", "Tabu"])
    plt.savefig("boxplot.png")


