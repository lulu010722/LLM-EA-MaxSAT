import random


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
            "optimal_fitness": 0
        }
        self.population = self.generate_population()

    def generate_population(self):
        return [Individual(Individual.create_gnome(self.problem.num_variables), self.problem, self.mutation_rate) for _ in range(self.population_size)]

    def evolve(self):
        for i in range(self.generations):
            if i % 10 == 0:
                print(f"Generation: {i}")
            self.population.sort(key=lambda x: x.fitness, reverse=True)
            new_population = []
            # 让适应度相邻的两个个体交配（门当户对）
            for i in range(0, self.population_size, 2):
                child1 = self.population[i].mate(self.population[i + 1])
                child2 = self.population[i + 1].mate(self.population[i])
                child1.mutate()
                child2.mutate()
                new_population.extend([child1, child2])
            self.population = new_population

        self.solution["optimal_chromosome"] = [self.population[0].chromosome]
        self.solution["optimal_fitness"] = self.population[0].fitness


POPULATION_SIZE = 100
MUTATION_RATE = 0.01
GENERATIONS = 100

NUM_VARIABLES = 12
NUM_CLAUSES = 100
NUM_LITERALS_PER_CLAUSE = 2


def with_respect_to_generations():
    results = []
    problem = MaxSATProblemFactory.create_maxsat_problem(NUM_VARIABLES, NUM_CLAUSES, NUM_LITERALS_PER_CLAUSE)
    for generations in range(10, 101, 10):
        ga = GeneticAlgorithm(problem, POPULATION_SIZE, MUTATION_RATE, generations)
        ga.evolve()
        results.append((generations, ga.solution["optimal_fitness"]))
        print(f"Generations: {generations}, Optimal Fitness: {ga.solution['optimal_fitness']}")
    return results


if __name__ == "__main__":
    results = with_respect_to_generations()

    
    
    
