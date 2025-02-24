import numpy as np
from model import calculate_yield
from settings import *


class Plant:
    def __init__(self, traits):
        self.traits = traits

    def calculate_fitness(self):
        yield_result, _ = calculate_yield(
            days=DAYS,
            initial_leaf_area=self.traits[0],
            leaf_angle=self.traits[1],
            S_o_values=S_O_VALUES,
            S_total=S_TOTAL,
            grain_params=GRAIN_PARAMS,
            conversion_factors=CONVERSION_FACTORS
        )
        return yield_result


def create_population(size):
    return [Plant([np.random.uniform(0.05, 0.2), np.random.choice(LEAF_ANGLES)]) for _ in range(size)]

def crossover(parent1, parent2):
    if np.random.rand() < CROSSOVER_RATE:
        split_point = np.random.randint(1, len(parent1.traits))
        child_traits = parent1.traits[:split_point] + parent2.traits[split_point:]
        return Plant(child_traits)
    return None


def mutate(individual):
    for i in range(len(individual.traits)):
        if np.random.rand() < MUTATION_RATE:
            individual.traits[i] += np.random.normal(0, 0.1)
    return individual


def genetic_algorithm():
    population = create_population(POPULATION_SIZE)

    for iteration in range(ITERATIONS):
        population.sort(key=lambda x: -x.calculate_fitness())
        new_population = []

        for i in range(0, len(population), 2):
            if i + 1 >= len(population):
                new_population.append(population[i])
                break

            parent1, parent2 = population[i], population[i + 1]

            child = crossover(parent1, parent2)

            if child:
                child = mutate(child)
                candidates = [parent1, parent2, child]
            else:
                candidates = [parent1, parent2]

            best = max(candidates, key=lambda x: x.calculate_fitness())
            new_population.append(best)

        population = new_population
        print(f"Iteration {iteration + 1}: Population size = {len(population)}")

        if len(population) == 1:
            break

    return max(population, key=lambda x: x.calculate_fitness())