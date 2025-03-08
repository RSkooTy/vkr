import math, random
from settings import  CRPAR, LIGHT_INTENSITY, SEEDS_PER_CAPSULE

GROWTH_STAGES = {
    1: (1, 10),   #семя
    2: (11, 30),  #рост стебля и листьев
    3: (31, 45),  #ветвление
    4: (46, 60),  #новые листья
    5: (61, 70),  #формирование бутона
    6: (71, 80),  #продолжение роста
    7: (81, 90),  #бутонизация
    8: (91, 95),  #цветение
    9: (96, 105), #созревание
    10: (106, 115),#формирование семян
    11: (116, 120)#урожай
}

CONVERSION_FACTORS = {
    'leaf': 0.023,
    'stem': 0.851,
    'grain': 1.0
}
def get_growth_stage(t):
    for stage, (start, end) in GROWTH_STAGES.items():
        if start <= t <= end:
            return stage
    return 11

#Расчет поглощенной PAR на основе угла листа и интенсивности света
def calculate_absorbed_PAR(leaf_area, leaf_angle, light_intensity):
    angle_impact = math.cos(math.radians(leaf_angle)) ** 2
    absorption_factor = 2.0 * angle_impact
    return leaf_area * light_intensity * absorption_factor * CRPAR

#Расчет фотосинтетической продукции
def calculate_photosynthetic_production(*args):
    return 10

#Расчет затрат на поддержание дыхания
def calculate_maintenance_respiration(total_biomass):
    return 0.014 * total_biomass

#Расчет роста размера органа на основе прироста биомассы
def calculate_organ_size_growth(biomass_increment, conversion_factor):
    return biomass_increment * conversion_factor

#Расчет общего ассимилята
def calculate_cap(CAP_prev, P_t, C_mr):
    return CAP_prev + P_t - C_mr

#Расчет роста биомассы органа
def calculate_biomass_increment(S_o, S_total, CAP_t):
    return min(S_o, (S_o / S_total) * CAP_t)

#Обновление биомассы органа
def update_biomass(previous_biomass, increment):
    return previous_biomass + increment

#Расчет урожайности
def calculate_grain_yield(D_grain_values, n_grain):
    return sum(D_grain_values[:n_grain])

def calculate_yield(days, initial_leaf_area, leaf_angle, S_o_values, S_total, grain_params, conversion_factors, initial_biomass):
    CAP = 0
    yield_total = 0
    total_biomass = initial_biomass
    D_grain_values = []

    t_grain_start, D_flower, t_grain_duration = grain_params
    t_grain_end = t_grain_start + t_grain_duration

    results = []

    organs = {
        'seed': {
            'biomass': initial_biomass,
        },
        'leaf': {
            'biomass': 0.0,
            'size': 0.0,
            'count': 0
        },
        'stem': {
            'biomass': 0.0,
            'height': 0.0,
            'branches': 0
        },
        'grain': {
            'biomass': 0.0,
            'capsules': []
        },
        'buds':[],
        'flowers': []
    }

    sink_strength = {
        'seed': 5.0,
        'leaf': 0.0,
        'stem': 0.0,
        'grain': 0.0,
        'buds': 0.0,
        'flowers': 0.0
    }

    for t in range(1, days + 1):
        stage = get_growth_stage(t)

        if stage == 1:
            P_t = 0.0
            C_mr = calculate_maintenance_respiration(organs['seed']['biomass'])
            CAP = max(0, CAP + P_t - C_mr)

            allocation = min(sink_strength['seed'], CAP)
            organs['seed']['biomass'] += allocation
            CAP -= allocation

            organs['seed']['size'] = organs['seed']['biomass'] * 1.0

            total_biomass = organs['seed']['biomass']

            results.append((
                t, stage, 0.0, 0, 0, total_biomass, 0.0
            ))
            continue

        if stage == 2:
            if organs['leaf']['count'] == 0:
                transfer = organs['seed']['biomass'] * 0.7
                organs['seed']['biomass'] -= transfer
                organs['leaf']['biomass'] = transfer * 0.6
                organs['stem']['biomass'] = transfer * 0.4
                organs['leaf']['count'] = 2
                organs['leaf']['size'] = organs['leaf']['biomass'] * CONVERSION_FACTORS['leaf']

            if random.random() < 0.25 and organs['leaf']['count'] < 15:
                organs['leaf']['count'] += 1
                organs['leaf']['biomass'] += 0.2
                organs['leaf']['size'] = organs['leaf']['biomass'] * CONVERSION_FACTORS['leaf']

            sink_strength.update({'leaf': 15.0, 'stem': 10.0, 'seed': 0.0})



        elif stage == 3 and t == GROWTH_STAGES[3][0]:
            organs['stem']['branches'] = random.randint(2, 4)
            sink_strength['branch'] = 8.0
            # Рост ветвей
            organs['stem']['biomass'] += 0.3 * organs['stem']['branches']


        elif stage == 4:
            sink_strength['leaf'] = 20.0

            if random.random() < 0.25 and organs['leaf']['count'] < 15:
                organs['leaf']['count'] += 1
                organs['leaf']['biomass'] += 0.2
                organs['leaf']['size'] = organs['leaf']['biomass'] * CONVERSION_FACTORS['leaf']

        elif stage == 5:
            if not organs['buds']:
                num_buds = random.randint(1, 5)
                organs['buds'] = [{'size': 0.1, 'biomass': 0.01} for _ in range(num_buds)]
            sink_strength['buds'] = 12.0

        elif stage == 6:
            sink_strength.update({
                'leaf': 10.0,
                'stem': 15.0,
                'branch': 5.0,
                'buds': 12.0
            })
            organs['stem']['biomass'] += 0.5

        elif stage == 7:
            sink_strength.update({
                'buds': 15.0,
                'flowers': 5.0
            })
            if t == GROWTH_STAGES[7][0]:
                organs['flowers'] = [{'size': 0.5, 'biomass': 0.0} for _ in organs['buds']]

        elif stage == 8:
            sink_strength.update({
                'flower': 20.0,
                'grain': 5.0
            })

        elif stage == 9:
            sink_strength.update({
                'grain': 25.0,
                'flower': 0.0,
                'buds': 0.0
            })
            organs['grain']['capsules'] = [
                {'seeds': SEEDS_PER_CAPSULE}
                for f in organs['flowers']
                if f.get('pollinated', False)
            ]
            organs['flowers'] = []


        elif stage == 10:
            sink_strength['grain'] = 30.0
            for capsule in organs['grain']['capsules']:
                capsule['size'] = min(1.0, capsule.get('size', 0.0) + 0.05)

        elif stage == 11:
            yield_total = sum(
                capsule.get('size', 0.0) * capsule['seeds']
                for capsule in organs['grain']['capsules']
            )

        leaf_area = organs['leaf']['size'] * organs['leaf']['count']
        absorbed_PAR = calculate_absorbed_PAR(leaf_area,leaf_angle,LIGHT_INTENSITY)
        P_t = calculate_photosynthetic_production(absorbed_PAR)
        C_mr = calculate_maintenance_respiration(total_biomass)
        CAP = max(0, calculate_cap(CAP, P_t, C_mr))

        active_sinks = {k: v for k, v in sink_strength.items() if v > 0}
        S_total = sum(active_sinks.values())

        allocations = {}
        if S_total > 0:
            for organ in sink_strength:
                S_o = sink_strength[organ]
                G_o = calculate_biomass_increment(S_o,S_total,CAP) if S_total > 0 else 0
                allocations[organ] = G_o
                CAP -= G_o

        for organ in ['leaf', 'stem', 'grain', 'buds', 'flowers']:
            if organ in allocations:
                if organ == 'buds':
                    if organs['buds']:
                        allocation_per_bud = allocations[organ] / len(organs['buds'])
                        for bud in organs['buds']:
                            bud['biomass'] += allocation_per_bud
                elif organ == 'flowers':
                    if organs['flowers']:
                        allocation_per_flower = allocations[organ] / len(organs['flowers'])
                        for flower in organs['flowers']:
                            flower['biomass'] += allocation_per_flower
                else:
                    organs[organ]['biomass'] += allocations.get(organ, 0)

        organs['leaf']['size'] = organs['leaf']['biomass'] * CONVERSION_FACTORS['leaf']
        organs['stem']['height'] = organs['stem']['biomass'] * CONVERSION_FACTORS['stem']

        if t == t_grain_start:
            n_gmax = CAP / D_flower if D_flower != 0 else 0
        if t_grain_start <= t <= t_grain_end:
            grain_alloc = allocations.get('grain', 0)
            D_grain_values.append(grain_alloc)

        total_biomass = sum([
            organs['seed']['biomass'],
            organs['leaf']['biomass'],
            organs['stem']['biomass'],
            organs['grain']['biomass'],
            sum(bud['biomass'] for bud in organs['buds']),  # Бутоны
            sum(flower['biomass'] for flower in organs['flowers'])
        ])

        yield_total = sum(D_grain_values) if t > t_grain_start else 0

        results.append((
            t, stage,
            round(organs['stem']['height'], 1),  #высота
            organs['leaf']['count'],  #листья
            len(organs['buds']),  #бутоны
            total_biomass,  #биомасса
            round(yield_total, 2)  #урожай
        ))

    return yield_total, results


