import sys
import re
import random

__author__ = 'alis'

class CNF:

    def __init__(self):
        self.formula = list()
        self.clauses = dict()
        self.lines = list()
        self.total_variables = int();
        self.variable_values = dict();
        self.satisfiable = True
        self.clauses_satus = list()
        self.total_clauses = 0
        self.num_satisfied_clauses = 0

    def read_dimacs_file(self, file_name):
        with open(file_name) as file:
            self.lines = file.readlines()
            # print (self.lines)
            for line in self.lines:
                if re.match(r"[a-z]", line[0]) is None:
                    line = re.findall(r'(?<!\S)[+-]?\d+(?!\S)', line)
                    # print(line)
                    # print("end")
                    for variable in line[0:-1]:
                        # print(variable)
                        if int(variable) > 0:
                            self.clauses[int(variable)] = True
                        elif int(variable) < 0:
                            self.clauses[int(variable[1:])] = False
                    # print(self.clauses)
                    self.formula.append(self.clauses)
                    self.clauses = dict()
                if re.match(r"[p]", line[0]):
                    self.total_variables = int(line.split()[2])
                    self.total_clauses = int(line.split()[3])
            for i in range(1, self.total_variables + 1):
                self.variable_values[i] = True

                self.clauses_satus = [None] * self.total_clauses

    def evaluate_formula(self):
        print("var values", self.variable_values)
        evaluation = False
        clause_num = 0
        for clause in self.formula:
            # print(clause)
            for variable in clause:
                # print(clause[variable], self.variable_values[variable], " ",self.truth_value(clause[variable], self.variable_values[variable]))
                # print(evaluation, self.truth_value(clause[variable], self.variable_values[variable]))
                evaluation = evaluation or self.truth_value(clause[variable], self.variable_values[variable])
            # print(clause_num)
            self.clauses_satus[clause_num] = evaluation
            # print("eval:", evaluation, self.satisfiable)
            self.satisfiable = self.satisfiable and evaluation
            evaluation = False
            clause_num += 1

        self.num_satisfied_clauses = self.clauses_satus.count(True)
        print(self.clauses_satus)
        print("nsc:", self.num_satisfied_clauses)
        if self.satisfiable is True:
            return True
        else:
            self.satisfiable = True
            return False
            # print(self.satisfiable)
        # print(self.satisfiable)

    @staticmethod
    def truth_value(bit1, bit2):
        if bit1 == True and bit2 == True:
            return True
        elif bit1 == True and bit2 == False:
            return False
        elif bit1 == False and bit2 == True:
            return False
        elif bit1 == False and bit2 == False:
            return True

    def update_variable_values(self, variable, value):
        self.variable_values[variable] = value

    def flip_variable_values(self, variable):
        for i in variable:
            self.variable_values[i] = not self.variable_values[i]


