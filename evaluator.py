import time
import numpy as np
from typing import Any
import Retrospective_method #以其中一种maxsat启发式算法为例

class MaxSatEvaluator:

    def __init__(self, algorithm: Any, test_instance: str, timeout_seconds: int = 60, quality_weight: float = 1.0,
                 time_weight: float = 1.0):

        self.algorithm = algorithm  # MaxSAT求解算法
        self.test_instance = test_instance  # CNF测试实例
        self.timeout_seconds = timeout_seconds  # 运行算法的超时限制
        self.quality_weight = quality_weight  # 质量（满足的子句数量）的权重
        self.time_weight = time_weight  # 运行时间的权重

    def parse_cnf(self, instance: str) -> list:
        #解析CNF文件，返回子句列表，每个子句是字面量的列表
        clauses = []
        with open(instance, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith("c") or not line:
                    continue
                if line.startswith("p"):
                    continue
                literals = list(map(int, line.split()))[:-1]
                clauses.append(literals)
        return clauses

    def run_algorithm(self, clauses) -> tuple[Any, float]:
        #运行算法并测量执行时间
        start_time = time.time()
        satisfied,assignment = self.algorithm(clauses)
        elapsed_time = time.time() - start_time
        return satisfied, assignment, elapsed_time

    def calculate_score(self,quality, time, stability) -> float:
        #计算综合评分
        score = (self.quality_weight * quality) / (self.time_weight * time) * stability
        return score

    def evaluate(self,num_trials) -> None:
        clauses = self.parse_cnf(test_instance)
        # 运行算法num_trials次并获取运算结果
        satisfied_list = []
        time_list = []
        for i in range(num_trials):
            satisfied, _, elapsed_time = self.run_algorithm(clauses)
            satisfied_list.append(satisfied)
            time_list.append(elapsed_time)

        avg_satisfied = np.mean(satisfied_list)
        avg_time = np.mean(time_list)
        if avg_time > self.timeout_seconds:
            print(f"Algorithm on instance {self.test_instance} timed out")
            return  # 超时则不继续评估
        # 计算满足子句数量的稳定性（离散系数：标准差/平均值）
        if avg_satisfied != 0:
            stability = np.std(satisfied_list) / avg_satisfied
        else:
            stability = 0 # 如果满足的子句数量为0，稳定性为0

        quality, time_taken = avg_satisfied, avg_time
        score = self.calculate_score(quality, time_taken, stability)
        self.save_results(quality, time_taken, stability, score)

    def save_results(self, quality: int, time_taken: float, stability: float, score: float) -> None:
        #示例将评估结果保存到文件，后续可调整为算法库等
        with open('E:/MaxSat/evaluation_results.txt', "w") as file:
            file.write(f"quality (satisfied clauses): {quality}\n")
            file.write(f"time: {time_taken}s\n")
            file.write(f"stability: {stability}\n")
            file.write(f"score: {score}\n")

# 测试实例
test_instance = 'E:/MaxSat/maxsat-instances/flush_reload_min.cnf'
evaluator = MaxSatEvaluator(algorithm=Retrospective_method.algorithm, test_instance=test_instance, quality_weight=1.0,
                            time_weight=0.5)
evaluator.evaluate(10)