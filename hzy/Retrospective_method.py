import sys


def score_variables(clauses):
    #计算变量出现的频率并排序
    score = {}
    for clause in clauses:
        for var in clause:
            score[abs(var)] = score.get(abs(var), 0) + 1
    return sorted(score.keys(), key=lambda x: -score[x])  # 按出现次数降序排列

def is_satisfied(clause, assignment):
    #判断子句是否满足
    return any((var > 0 and assignment.get(var, None) == 1) or
               (var < 0 and assignment.get(abs(var), None) == 0) for var in clause)

def count_satisfied(clauses, assignment):
    #计算当前赋值下满足的子句数
    return sum(is_satisfied(clause, assignment) for clause in clauses)


def backtrack(clauses, variables, assignment, index, best_satisfied, best_assignment):
    # 回溯法求解 MAXSAT，记录最优解
    if index == len(variables):
        satisfied_count = count_satisfied(clauses, assignment)
        if satisfied_count > best_satisfied[0]:  # 仅当找到更优解时更新
            best_satisfied[0] = satisfied_count
            best_assignment[0] = assignment.copy()
        return

    var = variables[index]

    for value in [1, 0]:
        assignment[var] = value
        backtrack(clauses, variables, assignment, index + 1, best_satisfied, best_assignment)

    del assignment[var]  # 回溯时删除该变量


def algorithm(clauses):
    variables = score_variables(clauses)  # 变量排序
    assignment = {}

    best_satisfied = [0]  # 记录最优解
    best_assignment = [{}]  # 记录最优赋值方案

    backtrack(clauses, variables, assignment, 0, best_satisfied, best_assignment)

    print(f"\n最大满足子句数: {best_satisfied[0]}")
    print(f"变量赋值方案: {best_assignment[0]}")
    return best_satisfied[0], best_assignment[0]


if __name__ == "__main__":
    clauses = []
    while True:
        line = input().strip()
        if not line:
            break
        if line.startswith('c') or line.startswith('p'):
            continue
        clause = list(map(int, line.split()))[:-1]
        clauses.append(clause)
    algorithm(clauses)