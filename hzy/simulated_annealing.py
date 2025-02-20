import random
import math

def algorithm(structs):
    # 获取所有变量编号
    vars_set = {abs(var) for clause in structs for var in clause}
    # 随机初始化赋值
    assignment = {var: random.randint(0, 1) for var in vars_set}

    def count_satisfied(assignment):
        return sum(
            any((var > 0 and assignment[var] == 1) or (var < 0 and assignment[-var] == 0) for var in clause)
            for clause in structs
        )

    # 初始温度
    T = 10.0
    # 退火率
    alpha = 0.99
    # 迭代次数
    max_iters = 1000

    # 计算初始可满足子句数
    best_assignment = assignment.copy()
    best_satisfied = count_satisfied(assignment)

    for _ in range(max_iters):
        # 随机选择一个变量翻转其值
        flip_var = random.choice(list(vars_set))
        assignment[flip_var] ^= 1

        new_satisfied = count_satisfied(assignment)
        delta = new_satisfied - best_satisfied

        # 根据模拟退火准则决定是否接受新的状态
        if delta > 0 or random.random() < math.exp(delta / T):
            best_satisfied = new_satisfied
            best_assignment = assignment.copy()
        else:
            # 回溯
            assignment[flip_var] ^= 1

        # 降低温度
        T *= alpha
        if T < 1e-3:
            break

    return best_satisfied