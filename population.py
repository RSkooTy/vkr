from model import calculate_yield
from settings import *
import hashlib
from typing import List, Callable, Tuple

PARAM_RANGES = [
    (0.5, 0.9),   # allocation_ratio
    (0, 180),       # leaf_angle
    (0.1, 1.5),    # photosynthetic_efficiency
    (0, 5)          # temp_tolerance
]

class ParameterConfig:
    def __init__(self, snp_indices: List[int],
                 transform: Callable[[List[int]], float],
                 value_range: Tuple[float, float]):
        self.snp_indices = snp_indices
        self.transform = transform
        self.value_range = value_range

class Plant:
    _hash_cache = {}
    _configs = None

    def __init__(self, genome):
        self.genome = genome
        self._hash = hashlib.sha256(genome.tobytes()).hexdigest()

    @classmethod
    def set_configs(cls, configs: List[ParameterConfig]):
        cls._configs = configs

    def decode_snp(self, idx: int) -> int:

        bits = self.genome[idx * 2: (idx + 1) * 2]
        value = bits[0] * 2 + bits[1]

        return value if value < 3 else 2

    def decode_traits(self) -> List[float]:

        traits = []
        for conf in self._configs:
            snps = [self.decode_snp(i) for i in conf.snp_indices]
            raw = conf.transform(snps)
            trait = float(np.interp(raw, [0, self._max_value(conf)], conf.value_range))
            traits.append(round(trait, 2))

        return traits

    def _max_value(self, conf: ParameterConfig) -> float:

        func_str = str(conf.transform).lower()
        if 'sum' in func_str:
            return 2 * len(conf.snp_indices)
        elif 'prod' in func_str:
            return 3 ** len(conf.snp_indices)
        elif 'max' in func_str:
            return 2
        elif 'len' in func_str or 'count' in func_str:
            return len(conf.snp_indices)

        return 2

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

def generate_configs() -> List[ParameterConfig]:

    configs = []
    all_snps = list(range(200))
    param_settings = [
        (100, np.sum, (0.5, 0.9)),  # allocation_ratio
        (100, np.mean, (0, 180)),  # leaf_angle
        (100, np.max, (0.1, 1.5)),  # photosynthetic_efficiency
        (100, np.median, (0, 5))  # temp_tolerance
    ]

    for n_snps, transform, value_range in param_settings:
        snp_indices = random.sample(all_snps, n_snps)
        configs.append(ParameterConfig(snp_indices, transform, value_range))

    return configs

def create_population(size):
    return [Plant(np.random.randint(0, 2, 400*2)) for _ in range(size)]

def crossover(p1: Plant, p2: Plant) -> Plant:

    pts = sorted(random.sample(range(1, 800), 2))
    child_genome = np.concatenate([
        p1.genome[:pts[0]],
        p2.genome[pts[0]:pts[1]],
        p1.genome[pts[1]:]
    ])

    return Plant(child_genome)

def mutate(ind: Plant, base_rate: float = MUTATION_RATE) -> Plant:

    genome = ind.genome.copy()
    for i in range(0, 800, 2):
        mutation_prob = base_rate * (1 + i / 800)
        if random.random() < mutation_prob:
            genome[i] ^= 1
            genome[i + 1] ^= 1

    return Plant(genome)

def genetic_algorithm_optimized(configs: List[ParameterConfig]):

    Plant.set_configs(configs)
    population = create_population(POPULATION_SIZE)
    hash_table = {}
    elite = None

    for _ in range(ITERATIONS):

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

            child = mutate(child)

            traits = tuple(map(float, child.decode_traits()))
            if traits not in hash_table:
                hash_table[traits] = child.calculate_fitness()

            new_population.append(child)

        if elite not in new_population:
            new_population[-1] = elite

        population = new_population

    return max(population, key=lambda x: hash_table[tuple(map(float, x.decode_traits()))])

def genetic_algorithm_basic(configs: List[ParameterConfig]):

    population = create_population(POPULATION_SIZE)
    best_plant = None
    best_fitness = 0.0

    for _ in range(ITERATIONS):
        new_population = []

        for i in range(POPULATION_SIZE):
            parent1, parent2 = random.sample(population, 2)
            child = crossover(parent1, parent2)

            child = mutate(child, base_rate=MUTATION_RATE)

            new_population.append(child)

        population = new_population

        current_best = max(population, key=lambda x: x.calculate_fitness(use_cache=False))

        if current_best.calculate_fitness(use_cache=False) > best_fitness:
            best_plant = current_best
            best_fitness = current_best.calculate_fitness(use_cache=False)

    return best_plant
