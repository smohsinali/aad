from CNF import CNF
from CSP import CSP
from Solver import Solver
import sys
import time

__author__ = 'alis'

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
        print("Usage: python3 main.py <file>")
        # sys.exit()
    # file_name = sys.argv[1]

    satisfiable = False

    # class Solver contain algorithms URW, WalkSAT, TabuSearch and their helper functions
    solver = Solver()
    # class CNF handles files, create datastructures for CNFs and provide function to check if formula is satisfied
    cnf = CNF()

    csp = CSP()

    if len(sys.argv) == 2:
        file_name = sys.argv[1]

        solver = Solver()
        cnf = CNF()
        cnf.read_dimacs_file(file_name)

        start = time.time()
        satisfiable = solver.URW(cnf, 100000)
        end = time.time()

        if satisfiable:
            print("s SATISFIABLE:")
            print("v", *format_output(cnf.variable_values), sep=" " )
        else:
            print("formula is not satisfiable")

        print("Time taken:", end - start, "secs")

        del cnf
        del solver
        satisfiable = False
        print()

        solver = Solver()
        cnf = CNF()
        cnf.read_dimacs_file(file_name)

        start = time.time()
        satisfiable = solver.WalkSAT(cnf, 100000)
        end = time.time()

        if satisfiable:
            print("s SATISFIABLE:")
            print("v", *format_output(cnf.variable_values), sep=" " )
        else:
            print("formula is not satisfiable")

        print("Time taken:", end - start, "secs")

        del cnf
        del solver
        satisfiable = False
        print()

        solver = Solver()
        cnf = CNF()
        cnf.read_dimacs_file(file_name)

        start = time.time()
        satisfiable = solver.tabuSearch(cnf, 100000, 5)
        end = time.time()

        if satisfiable:
            print("s SATISFIABLE:")
            print("v", *format_output(cnf.variable_values), sep=" " )
        else:
            print("formula is not satisfiable")

        print("Time taken:", end - start, "secs")

        del cnf
        del solver
        satisfiable = False
        print()

        sys.exit()

    # if no filename given in argument run on all files
    else:
        file_names = ["random_ksat1.dimacs", "random_ksat2.dimacs", "random_ksat3.dimacs",
                      "factoring1.dimacs", "factoring2.dimacs",
                      "subsetsum_random.dimacs"]

        csp_file = "queens.csp"

        print()
        # Following sequence of 20 lines calls URW on all given dimacs files and prints their solution and times
        for i in file_names:
            print ("DataSet:", i)
            solver = Solver()
            cnf = CNF()
            cnf.read_dimacs_file(i)

            start = time.time()
            satisfiable = solver.URW(cnf, 100000)
            end = time.time()

            if satisfiable:
                print("s SATISFIABLE:")
                print("v", *format_output(cnf.variable_values), sep=" " )
            else:
                print("formula is not satisfiable")

            print("Time taken:", end - start, "secs")
            del cnf
            del solver
            satisfiable = False
            print()

        print()
        # Following sequence of 20 lines calls WalkSAT on all given dimacs files and prints their solution and times
        for i in file_names:
            print ("DataSet:", i)
            solver = Solver()
            cnf = CNF()
            cnf.read_dimacs_file(i)

            start = time.time()
            satisfiable = solver.WalkSAT(cnf, 100000)
            end = time.time()

            if satisfiable:
                print("s SATISFIABLE:")
                print("v", *format_output(cnf.variable_values), sep=" " )
            else:
                print("formula is not satisfiable")

            print("Time taken:", end - start, "secs")
            del cnf
            del solver
            satisfiable = False
            print()

        print()
        # Following sequence of 20 lines calls TabuSearch on all given dimacs files and prints their solution and times
        for i in file_names:
            print ("DataSet:", i)
            solver = Solver()
            cnf = CNF()
            cnf.read_dimacs_file(i)

            start = time.time()
            satisfiable = solver.tabuSearch(cnf, 100000, 5)
            end = time.time()

            if satisfiable:
                print("s SATISFIABLE:")
                print("v", *format_output(cnf.variable_values), sep=" " )
            else:
                print("formula is not satisfiable")

            print("Time taken:", end - start, "secs")
            del cnf
            del solver
            satisfiable = False
            print()

