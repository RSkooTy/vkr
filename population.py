import numpy as np
from model_2 import calculate_yield2
from settings import *

class Plant:
    def __init__(self, traits):
        self.traits = traits

    def calculate_fitness(self):
        yield_result, _ = calculate_yield2(
            days=DAYS,
            grain_params=(FLOWERING_START_DAY, CAPSULE_MASS, GRAIN_FILLING_DURATION),
            initial_biomass=SEED_MASS,
            temperatures=temperatures,
            latitude=55.7,
            traits=self.traits
        )
        return yield_result


def create_population(size):
    return [Plant([
        np.random.uniform(0.7, 0.95),  # allocation_ratio
        np.random.choice(LEAF_ANGLES),  # leaf_angle
        np.random.uniform(0.01, 0.2),  # photosynthetic_efficiency
        np.random.uniform(0, 5)         # temp_tolerance
    ]) for _ in range(size)]

def crossover(parent1, parent2):
    return Plant([
        random.choice([parent1.traits[0], parent2.traits[0]]),
        random.choice([parent1.traits[1], parent2.traits[1]]),
        random.choice([parent1.traits[2], parent2.traits[2]]),
        random.choice([parent1.traits[3], parent2.traits[3]])
    ])
    return None


def mutate(individual):
    traits = individual.traits
    if np.random.rand() < MUTATION_RATE:
        traits[0] = np.clip(traits[0] + np.random.normal(0, 0.03), 0.7, 0.95)
    if np.random.rand() < MUTATION_RATE:
        traits[1] = np.random.choice(LEAF_ANGLES)
    if np.random.rand() < MUTATION_RATE:
        traits[2] = np.clip(traits[2] + np.random.normal(0, 0.005), 0.02, 0.05)
    if np.random.rand() < MUTATION_RATE:
        traits[3] = np.clip(traits[3] + np.random.normal(0, 0.5), 0, 3)
    return individual


def genetic_algorithm():
    population = create_population(POPULATION_SIZE)
    best_plant = None
    best_fitness = 0.0

    for iteration in range(ITERATIONS):
        new_population = []

        current_best = max(population, key=lambda x: x.calculate_fitness())
        current_fitness = current_best.calculate_fitness()

        if current_fitness > best_fitness:
            best_plant = current_best
            best_fitness = current_fitness

        random.shuffle(population)

        num_pairs = len(population) // 2
        for i in range(num_pairs):
            parent1 = population[2 * i]
            parent2 = population[2 * i + 1]

            child = crossover(parent1, parent2)
            if child:
                child = mutate(child)
                candidates = [parent1, parent2, child]
            else:
                candidates = [parent1, parent2]

            best_candidate = max(candidates, key=lambda x: x.calculate_fitness())
            new_population.append(best_candidate)

        if len(population) % 2 != 0:
            new_population.append(population[-1])

        population = new_population

        if len(population) > (len(new_population) + 1):
            population.remove(random.choice(population))

        print(f"Iteration {iteration + 1} | Pop size: {len(population)} | Best yield: {best_fitness:.2f}")

        if len(population) <= 1:
            break

    return best_plant if best_plant else population[0]

