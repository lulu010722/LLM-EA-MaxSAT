import random


class Literal:
    def __init__(self, var_index: int, negated: bool):
        self.var_index = var_index
        self.negated = negated

    def __str__(self):
        return f"{'-' if self.negated else ''}{self.var_index}"


class Clause:
    def __init__(self, literals: list[Literal]):
        self.literals = literals

    def __str__(self):
        return f"{' '.join([str(literal.var_index) for literal in self.literals])}"


class MaxSATProblem:
    def __init__(self, clauses: list[Clause]):
        self.clauses = clauses
        self.num_variables = max([
            literal.var_index
            for clause in clauses
            for literal in clause.literals
        ])
        self.num_clauses = len(clauses)

        self.optimal_assignment = []
        self.optimal_count = 0
        self.solution()

    def evaluate(self, assignment: list[bool]):
        satisfied_count = 0
        for clause in self.clauses:
            satisfied = False
            for literal in clause.literals:
                if (not literal.negated and assignment[literal.var_index - 1]) or (literal.negated and not assignment[literal.var_index - 1]):
                    satisfied = True
                    break
            if satisfied:
                satisfied_count += 1
        return satisfied_count

    # 暴力求最优解
    def solution(self):
        for i in range(2 ** self.num_variables):
            assignment = [int(bit) for bit in bin(i)[2:].zfill(self.num_variables)]
            count = self.evaluate(assignment)
            if count == self.optimal_count:
                self.optimal_assignment += [assignment]
            elif count > self.optimal_count:
                self.optimal_assignment = [assignment]
                self.optimal_count = count


class MaxSATProblemFactory:
    @staticmethod
    def create_maxsat_problem(num_variables: int, num_clauses: int, num_literals_per_clause: int):
        clauses = [
            Clause([
                Literal(var_index, random.choice([False, True]))
                for var_index in random.sample(
                    range(1, num_variables + 1), num_literals_per_clause
                )
            ])
            for _ in range(num_clauses)
        ]

        return MaxSATProblem(clauses)

    @staticmethod
    def create_n_maxsat_problem(num_variables: int, num_clauses: int, num_literals_per_clause: int, n=1):
        return [MaxSATProblemFactory.create_maxsat_problem(num_variables, num_clauses, num_literals_per_clause) for _ in range(n)]
