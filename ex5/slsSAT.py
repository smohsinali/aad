from CNF import CNF
from Solver import Solver
import sys
import time


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
                "cnf_exercise5/random_ksat(13).dimacs",
                "cnf_exercise5/random_ksat(14).dimacs",
                ]
    # class Solver contain algorithms URW, WalkSAT, TabuSearch and their helper functions
    solver = Solver()
    # class CNF handles files, create datastructures for CNFs and provide function to check if formula is satisfied
    cnf = CNF()

    for dataSet in dataSets:
        file_name = dataSet
        print "For dataset:", dataSet

        solver = Solver()
        cnf = CNF()
        cnf.read_dimacs_file(file_name)

        start = time.time()
        satisfiable = solver.WalkSAT(cnf, 200)
        end = time.time()

        if satisfiable:
            print "s SATISFIABLE:"
            print "v", format_output(cnf.variable_values)
        else:
            print "Cannot find Solution"

        print "Time taken:", end - start, "secs"

        del cnf
        del solver
        satisfiable = False
        print

