import numpy as np
from model import calculate_yield
from settings import *
import hashlib
from typing import List, Callable, Tuple
import random

PARAM_RANGES = [
    (0.5, 0.9),  # allocation_ratio
    (0, 180),  # leaf_angle
    (0.1, 1.5),  # photosynthetic_efficiency
    (0, 5)  # temp_tolerance
]


class ParameterConfig:
    def __init__(self, snp_indices: List[int],
                 transform: Callable[[List[int]], float],
                 value_range: Tuple[float, float],
                 min_raw: float = None,
                 max_raw: float = None):
        self.snp_indices = snp_indices
        self.transform = transform
        self.value_range = value_range
        self.min_raw = min_raw
        self.max_raw = max_raw


class Plant_2:
    _hash_cache = {}
    _configs = None

    def __init__(self, genome):
        self.genome = genome
        self._hash = hashlib.sha256(genome.tobytes()).hexdigest()

    @classmethod
    def set_configs(cls, configs: List[ParameterConfig]):
        cls._configs = configs

    def decode_snp(self, idx: int) -> int:
        return self.genome[idx]

    def decode_traits(self) -> List[float]:
        traits = []
        for conf in self._configs:
            snps = [self.decode_snp(i) for i in conf.snp_indices]
            raw = conf.transform(snps)
            trait = np.interp(raw, [conf.min_raw, conf.max_raw], conf.value_range)
            traits.append(round(trait, 2))
        return traits

    def calculate_fitness(self, use_cache=False):
        params_hash = hashlib.md5(str(self.decode_traits()).encode()).hexdigest()
        if params_hash in self._hash_cache:
            return self._hash_cache[params_hash]

        traits = self.decode_traits()

        yield_result = calculate_yield(
            days=DAYS,
            grain_params=(FLOWERING_START_DAY, CAPSULE_MASS, GRAIN_FILLING_DURATION),
            initial_biomass=SEED_MASS,
            temperatures=temperatures,
            latitude=55.7,
            traits=traits
        )[0]

        return yield_result


def generate_configs_2() -> List[ParameterConfig]:
    configs = []
    all_snps = list(range(100))

    for value_range in PARAM_RANGES:
        weights = np.random.randn(100)
        min_raw = sum(min(0 * w, 1 * w) for w in weights)
        max_raw = sum(max(0 * w, 1 * w) for w in weights)

        configs.append(ParameterConfig(
            snp_indices=all_snps,
            transform=lambda snps, w=weights.copy(): sum(s * wi for s, wi in zip(snps, w)),
            value_range=value_range,
            min_raw=min_raw,
            max_raw=max_raw
        ))

    return configs


def create_population(size):
    return [Plant_2(np.random.randint(0, 2, 100)) for _ in range(size)]


def crossover(p1: Plant_2, p2: Plant_2) -> Plant_2:
    pts = sorted(random.sample(range(1, 100), 2))
    child_genome = np.concatenate([
        p1.genome[:pts[0]],
        p2.genome[pts[0]:pts[1]],
        p1.genome[pts[1]:]
    ])
    return Plant_2(child_genome)


def mutate(ind: Plant_2, base_rate: float = MUTATION_RATE) -> Plant_2:
    genome = ind.genome.copy()
    for i in range(100):
        mutation_prob = base_rate * (1 + i / 100)
        if random.random() < mutation_prob:
            genome[i] ^= 1
    return Plant_2(genome)

def genetic_algorithm_optimized_2(configs: List[ParameterConfig]):

    Plant_2.set_configs(configs)
    population = create_population(POPULATION_SIZE)
    hash_table = {}
    elite = None
    fitness_history = []
    diversity_history = []
    snp_history = []
    snapshots = []

    for iteration in range(ITERATIONS):

        current_gen_snps = {f'param_{i}': [] for i in range(len(configs))}
        for ind in population:
            traits = ind.decode_traits()
            for i, trait in enumerate(traits):
                current_gen_snps[f'param_{i}'].append(trait)

        avg_snps = {}
        for param in current_gen_snps:
            avg = np.mean(current_gen_snps[param])
            avg_snps[param] = avg
        snp_history.append(avg_snps)

        for ind in population:
            traits = tuple(map(float, ind.decode_traits()))
            if traits not in hash_table:
                hash_table[traits] = ind.calculate_fitness()

        sorted_pop = sorted(population, key=lambda x: -hash_table[tuple(map(float, x.decode_traits()))])
        elite_size = int(POPULATION_SIZE * 0.1)
        elite = sorted_pop[0] if (elite is None or hash_table[tuple(map(float, sorted_pop[0].decode_traits()))] > hash_table[tuple(map(float, elite.decode_traits()))]) else elite
        new_population = sorted_pop[:elite_size].copy()

        parents_pool = sorted_pop[:int(POPULATION_SIZE * 0.4)]

        while len(new_population) < POPULATION_SIZE:

            p1, p2 = random.choices(parents_pool, k=2)
            child = crossover(p1, p2)

            child = mutate(child, base_rate=MUTATION_RATE)

            traits = tuple(map(float, child.decode_traits()))
            if traits not in hash_table:
                hash_table[traits] = child.calculate_fitness()

            new_population.append(child)

        if elite not in new_population:
            new_population[-1] = elite

        population = new_population

        current_fitness = hash_table[tuple(map(float, sorted_pop[0].decode_traits()))]
        fitness_history.append(current_fitness)

        fitness_values = [hash_table[tuple(map(float, ind.decode_traits()))] for ind in population]
        diversity = np.std(fitness_values)/ np.mean(fitness_values)
        diversity_history.append(diversity)

        if iteration == 0 or iteration == ITERATIONS // 2 or iteration == ITERATIONS - 1:
            current_snapshot = []
            for ind in population:
                fitness = hash_table[tuple(map(float, ind.decode_traits()))]
                current_snapshot.append((ind.genome.copy(), fitness))
            snapshots.append(current_snapshot)

    return max(population, key=lambda x: hash_table[tuple(map(float, x.decode_traits()))]), fitness_history, diversity_history, snp_history, snapshots

def genetic_algorithm_basic_2(configs: List[ParameterConfig]):

    population = create_population(POPULATION_SIZE)
    best_plant = None
    best_fitness = 0.0
    diversity_history = []
    fitness_history = []

    for _ in range(ITERATIONS):
        new_population = []
        fitness_values = [ind.calculate_fitness(use_cache=False) for ind in population]

        current_best = max(population, key=lambda x: x.calculate_fitness(use_cache=False))
        current_fitness = current_best.calculate_fitness(use_cache=False)
        fitness_history.append(current_fitness)

        for i in range(POPULATION_SIZE):
            parent1, parent2 = random.sample(population, 2)
            child = crossover(parent1, parent2)

            child = mutate(child, base_rate=MUTATION_RATE)

            new_population.append(child)

        population = new_population

        if current_best.calculate_fitness(use_cache=False) > best_fitness:
            best_plant = current_best
            best_fitness = current_best.calculate_fitness(use_cache=False)

        diversity = np.std(fitness_values) / np.mean(fitness_values) if np.mean(fitness_values) != 0 else 0
        diversity_history.append(diversity)

    return best_plant, diversity_history