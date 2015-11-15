import sys
import re
import random

__author__ = 'alis'

class Solver:
    def __init__(self):
        self.random_variable = 0
        self.unsatisfied_clauses = list()

    def URW(self, cnf, max_steps):
        satisfiable = False
        steps = 0
        print("sat;", cnf.satisfiable)
        while satisfiable is False and steps < max_steps:
            self.random_variable = random.randint(1, cnf.total_variables)
            print(steps, self.random_variable)
            cnf.flip_variable_values([self.random_variable])
            satisfiable = cnf.evaluate_formula()
            if satisfiable is True:
                return True
            steps += 1
        return False

    def tabuSearch(self, cnf, max_steps, tabuLength):
        print("tabu search")
        steps = 0
        tabu_list = dict()
        satisfiable = False
        variable = None
        for i in cnf.variable_values:
            tabu_list[i] = 0
        # print(tabu_list)
        if cnf.evaluate_formula() is True:
            return True
        else:
            while satisfiable is False and steps < max_steps:
                variable, tabu_list = self.find_random_best_variable(cnf, tabu_list, tabuLength)
                print("variable:", variable, "tabuList:", tabu_list)
                cnf.flip_variable_values([variable])
                satisfiable = cnf.evaluate_formula()
                if satisfiable is True:
                        return True

                print("attempt:", steps)
                print()
                steps += 1

        return False


    @staticmethod
    def find_random_best_variable(cnf, tabu_list, tabuLength):
        best_variable = dict()

        for i in cnf.variable_values:
            print("i in cnf.var:", i)
            if tabu_list[i] != 0:
                tabu_list[i] -= 1
            else:
                cnf.flip_variable_values([i])
                cnf.evaluate_formula()
                best_variable[i] = cnf.num_satisfied_clauses
                cnf.flip_variable_values([i])

        maxx = max(best_variable.values())
        keys = [x for x, y in best_variable.items() if y == maxx]

        # print("keys:", keys)
        key = random.choice(keys)
        tabu_list[key] = tabuLength
        return key, tabu_list


    def WalkSAT(self, cnf, max_steps):
        steps = 0
        satisfiable_clauses = cnf.num_satisfied_clauses
        satisfiable = False
        if cnf.evaluate_formula() is True:
            return True
        else:
            print("satis", cnf.satisfiable)
            while satisfiable is False and steps < max_steps:
                clause = self.find_random_false_clause(cnf)
                if clause == {}:
                    print("empty clause")
                    break
                # print("clause:", clause, cnf.formula[clause], random.choice(list(cnf.formula[clause].keys())))
                random_literal = random.choice(list(cnf.formula[clause].keys()))
                cnf.flip_variable_values([random_literal])
                cnf.evaluate_formula()
                # print()
                if cnf.num_satisfied_clauses < satisfiable_clauses:
                    cnf.flip_variable_values([random_literal])
                else:
                    print("attempt:",steps)
                    satisfiable_clauses = cnf.num_satisfied_clauses
                    satisfiable = cnf.evaluate_formula()
                    if satisfiable is True:
                        return True
                steps += 1
        return False

    @staticmethod
    def find_random_false_clause(cnf):
        unsatisfied_clauses = [i for i, x in enumerate(cnf.clauses_satus) if x is False]
        # print("uc:", unsatisfied_clauses)
        if len(unsatisfied_clauses) == 0:
            return {}
        else:
            return unsatisfied_clauses[random.randint(0, len(unsatisfied_clauses))-1]

