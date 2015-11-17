import sys
import re
import random
import json

__author__ = 'alis'


class CSP:

    def __init__(self):
        self.variables = dict()
        self.formula = list()
        self.clauses = dict()

    def read_csp_file(self, file_name):
        with open(file_name) as fp:
            csp = json.load(fp)
            for line in csp:
                if line[0] == "int":
                    self.variables[line[1]] = range(line[2], line[3] + 1)
                elif line[0] == "alldifferent":
                    print(line)
                    for i in range(1, len(line) - 1):
                        print(i)
                        print(line[1])
                        self.clauses[line[i]] = random.choice(self.variables[line[i]])
                        self.clauses[line[i + 1]] = random.choice(self.variables[line[i + 1]])
                        self.formula.append(self.clauses)
                        self.clauses = dict()

if __name__ == "__main__":
    print("Please run 'python3 main.py <filename>'")

