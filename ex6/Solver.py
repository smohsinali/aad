import sys
import re
import random

__author__ = 'alis'


class Solver:
    def __init__(self):
        self.random_variable = 0
        self.unsatisfied_clauses = list()

    # Implementation of URW
    def URW(self, cnf, max_steps):
        print("Algo: URW")
        satisfiable = False
        steps = 0
        while satisfiable is False and steps < max_steps:
            self.random_variable = random.randint(1, cnf.total_variables)
            cnf.flip_variable_values([self.random_variable])
            satisfiable = cnf.evaluate_formula()
            if satisfiable is True:
                print("# of Steps:", steps)
                return True
            steps += 1
        print("# of Steps:", steps)
        return False

    # Implementation of TabuSearch. also takes as input tabuLength which tells
    #  until how many next rounds variable shouldnt be updated after its changed.
    def tabuSearch(self, cnf, max_steps, tabuLength):
        print("Algo: Tabu Search")
        steps = 0
        tabu_list = dict()
        satisfiable = False
        variable = None
        for i in cnf.variable_values:
            tabu_list[i] = 0
        if cnf.evaluate_formula() is True:
            return True
        else:
            while satisfiable is False and steps < max_steps:
                variable, tabu_list = self.find_random_best_variable(cnf, tabu_list, tabuLength)
                cnf.flip_variable_values([variable])
                satisfiable = cnf.evaluate_formula()
                if satisfiable is True:
                        print("# of Steps:", steps)
                        return True
                steps += 1
        print("# of Steps:", steps)
        return False

    # Implementation of WalkSAT.
    # Works better when variable 'satisfiable_clauses' is not changed after
    #  initializing it with 'cnf.num_satisfied_clauses'
    def WalkSAT(self, cnf, max_steps):
        print("Algo: WalkSAT")
        steps = 0
        satisfiable_clauses = cnf.num_satisfied_clauses
        satisfiable = False
        if cnf.evaluate_formula() is True:
            print("# of Steps:", steps)
            return True
        else:
            # print("satis", cnf.satisfiable)
            while satisfiable is False and steps < max_steps:
                clause = self.find_random_false_clause(cnf)
                if clause == {}:
                    # print("empty clause")
                    break
                random_literal = random.choice(list(cnf.formula[clause].keys()))
                cnf.flip_variable_values([random_literal])
                cnf.evaluate_formula()

                if cnf.num_satisfied_clauses < satisfiable_clauses:
                    cnf.flip_variable_values([random_literal])
                else:
                    # print("attempt:",steps)
                    # satisfiable_clauses = cnf.num_satisfied_clauses
                    satisfiable = cnf.evaluate_formula()
                    if satisfiable is True:
                        print("# of Steps:", steps)
                        return True
                steps += 1
        print("# of Steps:", steps)
        return False

    # This function is called by TabuSearch.
    # It selects best variable from non-tabu elements and updated tabuList
    @staticmethod
    def find_random_best_variable(cnf, tabu_list, tabuLength):
        best_variable = dict()

        while len(best_variable) == 0:
            for i in cnf.variable_values:
                # print("i in cnf.var:", i)
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


    # This function is called by WalkSAT.
    # It randomly selects a unsatisfied clause.
    @staticmethod
    def find_random_false_clause(cnf):
        unsatisfied_clauses = [i for i, x in enumerate(cnf.clauses_satus) if x is False]
        # print("uc:", unsatisfied_clauses)
        if len(unsatisfied_clauses) == 0:
            return {}
        else:
            return unsatisfied_clauses[random.randint(0, len(unsatisfied_clauses))-1]

if __name__ == "__main__":
    print("Please run 'python3 main.py <filename>'")