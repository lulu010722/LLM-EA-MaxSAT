import random
import plotly.graph_objects as go


from maxsat import MaxSATProblemFactory, MaxSATProblem


class Individual:
    def __init__(self, chromosome: list[int], problem: MaxSATProblem, mutation_rate: float):
        self.chromosome = chromosome
        self.problem = problem
        self.mutation_rate = mutation_rate
        self.fitness = self.calculate_fitness()

    @classmethod
    def create_gnome(cls, num_variables: int):
        return [random.randint(0, 1) for _ in range(num_variables)]

    def mate(self, partner: 'Individual'):
        child_chromosome = []
        for gnome1, gnome2 in zip(self.chromosome, partner.chromosome):
            prob = random.random()
            if prob < 0.5:
                child_chromosome.append(gnome1)
            else:
                child_chromosome.append(gnome2)
        return Individual(child_chromosome, self.problem, self.mutation_rate)

    def mutate(self):
        for i in range(len(self.chromosome)):
            if random.random() < self.mutation_rate:
                self.chromosome[i] = 1 - self.chromosome[i]
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        return self.problem.evaluate(self.chromosome)


class GeneticAlgorithm:
    def __init__(self, problem: MaxSATProblem, population_size: int,  mutation_rate: float, generations: int):
        self.problem = problem
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations

        self.solution = {
            "optimal_chromosome": [],
            "optimal_fitness": 0,
        }
        self.evolution_process = []

        self.population = self.generate_population()

    def generate_population(self):
        return [Individual(Individual.create_gnome(self.problem.num_variables), self.problem, self.mutation_rate) for _ in range(self.population_size)]

    def evolve(self):
        for i in range(self.generations):
            new_population = self.population
            for i in range(0, self.population_size, 2):
                child1 = self.population[i].mate(self.population[i + 1])
                child2 = self.population[i + 1].mate(self.population[i])
                child1.mutate()
                child2.mutate()
                new_population.extend([child1, child2])
            new_population.sort(key=lambda x: x.fitness, reverse=True)
            self.population = new_population[:self.population_size]

        self.solution["optimal_chromosome"] = [self.population[0].chromosome]
        self.solution["optimal_fitness"] = self.population[0].fitness

    def cumulative_evolution_process(self):
        for i in range(self.generations):
            self.evolution_process.append({
                "chromosome": self.population[0].chromosome,
                "fitness": self.population[0].fitness,
            })
            new_population = self.population
            for i in range(0, self.population_size, 2):
                child1 = self.population[i].mate(self.population[i + 1])
                child2 = self.population[i + 1].mate(self.population[i])
                child1.mutate()
                child2.mutate()
                new_population.extend([child1, child2])
            new_population.sort(key=lambda x: x.fitness, reverse=True)
            self.population = new_population[:self.population_size]
            if self.population[0].fitness == self.problem.optimal_count:
                break
        while len(self.evolution_process) < self.generations:
            self.evolution_process.append({
                "chromosome": self.population[0].chromosome,
                "fitness": self.population[0].fitness,
            })


# 研究遗传算法的表现随着迭代次数的变化，对于每个迭代次数，进化过程是独立的
def with_respect_to_generations(generations_range: range):
    results = []
    problem = MaxSATProblemFactory.create_maxsat_problem(NUM_VARIABLES, NUM_CLAUSES, NUM_LITERALS_PER_CLAUSE)
    for generations in generations_range:
        ga = GeneticAlgorithm(problem, POPULATION_SIZE, MUTATION_RATE, generations)
        ga.evolve()
        results.append((generations, ga.solution["optimal_fitness"]))
    return results, problem.optimal_count


# 研究遗传算法的表现随着迭代次数的变化，只进化一次，进化过程中记录每一代的最优解
def with_respect_to_generations_cumulative(generations):
    results = []
    problem = MaxSATProblemFactory.create_maxsat_problem(NUM_VARIABLES, NUM_CLAUSES, NUM_LITERALS_PER_CLAUSE)
    ga = GeneticAlgorithm(problem, POPULATION_SIZE, MUTATION_RATE, generations)
    ga.cumulative_evolution_process()
    return ga.evolution_process, problem.optimal_count


POPULATION_SIZE = 100
MUTATION_RATE = 0.1
GENERATIONS = 20

NUM_VARIABLES = 10
NUM_CLAUSES = 500
NUM_LITERALS_PER_CLAUSE = 3

GENERATIONS_RANGE = range(10, 101, 10)


if __name__ == "__main__":

    # 1. 研究遗传算法的表现随着迭代次数的变化，对于每个迭代次数，进化过程是独立的
    results, optimal_count = with_respect_to_generations(GENERATIONS_RANGE)
    x = list(GENERATIONS_RANGE)
    y1 = [result[1] for result in results]
    y2 = [optimal_count for _ in GENERATIONS_RANGE]

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=x, y=y1, mode='lines+markers', name="遗传算法"))
    fig1.add_trace(go.Scatter(x=x, y=y2, mode='lines+markers', name="最优解"))
    
    fig1.update_layout(
        title=f"算法表现与最大进化轮数的关系(变量个数={NUM_VARIABLES}, 子句个数={NUM_CLAUSES}, 每个子句中的文字个数={NUM_LITERALS_PER_CLAUSE})",
        xaxis_title="迭代次数",
        yaxis_title="最优解",
    )
    fig1.show()

    # 2. 研究遗传算法的表现随着迭代次数的变化，只进化一次，进化过程中记录每一代的最优解
    evolution_process, optimal_count = with_respect_to_generations_cumulative(GENERATIONS)
    x = list(range(GENERATIONS))
    y1 = [process["fitness"] for process in evolution_process]
    y2 = [optimal_count for _ in range(GENERATIONS)]
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=x, y=y1, mode='lines+markers', name="遗传算法"))
    fig2.add_trace(go.Scatter(x=x, y=y2, mode='lines+markers', name="最优解"))

    fig2.update_layout(
        title=f"单次进化过程中，最优解随着迭代次数的变化(变量个数={NUM_VARIABLES}, 子句个数={NUM_CLAUSES}, 每个子句中的文字个数={NUM_LITERALS_PER_CLAUSE})",
        xaxis_title="迭代次数",
        yaxis_title="最优解",
    )
    fig2.show()
