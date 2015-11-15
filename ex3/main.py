from CNF import CNF
from CSP import CSP
from Solver import Solver
import sys
import re
import random
import json

__author__ = 'alis'

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <file>")
        # sys.exit()
    # file_name = sys.argv[1]

    satisfiable = False

    # file_name = "queens.csp"
    # file_name = "random_ksat1.dimacs"
    # file_name = "factoring2.dimacs"
    file_name = "subsetsum_random.dimacs"
    csp_file = "queens.csp"
    x = 3+1 is not 4
    print(x)

    solver = Solver()
    cnf = CNF()
    csp = CSP()
    #
    csp.read_csp_file(csp_file)
    cnf.read_dimacs_file(file_name)
    #
    # for i in cnf.formula:
    #     print(i)
    # print(cnf.formula)
    # cnf.flip_variable_values([2])

    # print("stra:", cnf.satisfiable)
    # print(random.randint(1,1))
    # satisfiable = solver.URW(cnf, 100000)
    # satisfiable = solver.WalkSAT(cnf, 100)
    # satisfiable = solver.tabuSearch(cnf, 1000, 10)

    # if satisfiable:
    #     print("formula is satisfiable:", cnf.variable_values)
    # else:
    #     print("formula is not satisfiable")
    # print(len(cnf.formula))

    # with open("queens.csp") as fp:
    #     csp = json.load(fp)
    #     print(csp)