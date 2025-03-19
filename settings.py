import random

DAYS = 103

S_O_VALUES = [0.1, 0.4, 0.5]
S_TOTAL = sum(S_O_VALUES)

CONVERSION_FACTORS = {
    'leaf': 0.023,
    'stem': 0.851,
    'grain': 1.0
}

PP_PARAMS = {
    'Pc': 14,
    'ppsen': 0.0085,
    'CPP': 16
}

STAGE_PARAMS = {
    1: {'Tb': 10, 'To': 19, 'Tc': 36},  # Прорастание
    2: {'Tb': 10, 'To': 18, 'Tc': 36},  # Рост стебля
    3: {'Tb': 10, 'To': 18, 'Tc': 36},  # Ветвление
    4: {'Tb': 10, 'To': 18, 'Tc': 36},  # Ветвление
    5: {'Tb': 10, 'To': 18, 'Tc': 36},  # Ветвление
    6: {'Tb': 10, 'To': 18, 'Tc': 36},  # Ветвление
    7: {'Tb': 10, 'To': 23, 'Tc': 36},  # Цветение
    8: {'Tb': 10, 'To': 23, 'Tc': 36},  # Созревание
    9: {'Tb': 10, 'To': 23, 'Tc': 36},  # Формирование семян
    10: {'Tb': 10, 'To': 23, 'Tc': 36},  # Ветвление
    11: {'Tb': 10, 'To': 23, 'Tc': 36},  # Ветвление

}

GROWTH_STAGES_BD = {
    1: (0, 10),
    2: (10.001, 21),
    3: (21.001, 22),
    4: (22.001, 34),
    5: (34.001, 35),
    6: (35.001, 44),
    7: (44.001, 50),
    8: (50.001, 55),
    9: (55.001, 60),
    10: (60.001, 70),
    11: (70.001, float('inf'))
}

SEEDS_PER_CAPSULE = random.randint(5, 10)

GRAIN_PARAMS = (1, 0.05, 150)
POPULATION_SIZE = 20
CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.08
ITERATIONS = 120

CRPAR = 0.48
LEAF_ANGLES = [30, 45, 60]

SEED_MASS = 0.5
FLOWERING_START_DAY = 75
GRAIN_FILLING_DURATION = 40
CAPSULE_MASS = 0.5

SOLAR_CONSTANT = 1368
