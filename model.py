import math, random, numpy as np
from settings import  CRPAR,  SEEDS_PER_CAPSULE, SOLAR_CONSTANT, CONVERSION_FACTORS, PP_PARAMS, STAGE_PARAMS, GROWTH_STAGES_BD

random.seed(42)
np.random.seed(42)

def calculate_solar_declination(day_of_year):
    return math.radians(23.45 * math.sin(2 * math.pi * (284 + day_of_year) / 365))

def calculate_sin_beta(latitude, day_of_year):
    lat_rad = math.radians(latitude)
    delta = calculate_solar_declination(day_of_year)
    return math.sin(lat_rad) * math.sin(delta) + math.cos(lat_rad) * math.cos(delta)

def calculate_earth_sun_distance_factor(day_of_year):
    return 1 + 0.033 * math.cos(2 * math.pi * (day_of_year - 10) / 365)

def get_growth_stage_bd(sum_bd):
    for stage, (start, end) in GROWTH_STAGES_BD.items():
        if start <= sum_bd <= end:
            return stage
    return 11

def calculate_tempfun(T, Tb, To, Tc):
    if T <= Tb or T >= Tc:
        return 0.0
    return ((Tc - T)/(Tc - To)) * (((T - Tb)/(To - Tb))**((To - Tb)/(Tc - To)))

def calculate_day_length(day_of_year, latitude):
    lat_rad = math.radians(latitude)
    theta = 0.2163108 + 2 * math.atan(0.9671396 * math.tan(0.00860 * (day_of_year - 186)))
    P = math.asin(0.39795 * math.cos(theta))

    sin_term = math.sin(lat_rad) * math.sin(P)
    cos_term = math.cos(lat_rad) * math.cos(P)
    hour_angle = math.acos(sin_term / cos_term)

    return 24 - (24 / math.pi) * math.acos(math.sin(math.sin(math.radians(0.833)))) + hour_angle

def calculate_ppfun(PP):
    if PP >= PP_PARAMS['Pc']:
        return 1.0
    return 1 - PP_PARAMS['ppsen'] * (PP_PARAMS['CPP'] - PP) ** 2

#Расчет поглощенной PAR на основе угла листа и интенсивности света
def calculate_absorbed_PAR(leaf_area, leaf_angle, E_dir, E_dif):
    if not leaf_angle or leaf_area <= 0:
        return 0.0

    num_leaves = len(leaf_angle)
    area_per_leaf = leaf_area / num_leaves
    total_absorbed = 0.0

    for angle in leaf_angle:
        angle_rad = math.radians(angle)
        angle_impact = math.sin(angle_rad)
        absorption_factor = angle_impact
        leaf_PAR = (E_dir + E_dif) * CRPAR
        total_absorbed += area_per_leaf * leaf_PAR * absorption_factor

    return total_absorbed

def calculate_photosynthetic_production(absorbed_PAR, photosynthetic_efficiency):
    if absorbed_PAR <= 0:
        return 0.0
    epsilon = photosynthetic_efficiency
    P_t = absorbed_PAR * epsilon
    return min(P_t, 12.1)

#Расчет затрат на поддержание дыхания
def calculate_maintenance_respiration(total_biomass):
    return 0.014 * total_biomass

#Расчет общего ассимилята
def calculate_cap(CAP_prev, P_t, C_mr):
    return CAP_prev + P_t - C_mr

#Расчет роста биомассы органа
def calculate_biomass_increment(S_o, S_total, CAP_t):
    return min(S_o, (S_o / S_total) * CAP_t)

def calculate_yield(days, grain_params, initial_biomass, temperatures, latitude, traits):
    CAP = 0
    yield_total = 0
    total_biomass = initial_biomass
    D_grain_values = []

    sum_BD = 0.0
    current_stage = 1
    BD_history = []

    leaf_angles = [traits[1]] * 12

    t_grain_start, D_flower, t_grain_duration = grain_params
    t_grain_end = t_grain_start + t_grain_duration

    results = []

    organs = {
        'seed': {'biomass': initial_biomass, 'size': 0.0},
        'leaf': {'biomass': 0.0, 'size': 0.0, 'count': 0, 'scale': 1.0, 'angles': leaf_angles},
        'stem': {'biomass': 0.0, 'height': 0.0, 'branches': 0, 'diameter': 0.0},
        'grain': {'biomass': 0.0, 'capsules': []},
        'buds': [],
        'flowers': [],
        'fruits': []
    }

    sink_strength = {
        'seed': 5.0,
        'leaf': 0.0,
        'stem': 0.0,
        'grain': 0.0,
        'buds': 0.0,
        'flowers': 0.0,
        'fruits': 0.0
    }

    allocation_ratio = traits[0]
    photosynthetic_efficiency = traits[2]
    temp_tolerance = traits[3]

    To = 16 + temp_tolerance
    Tc = 36 - temp_tolerance

    for t in range(1, days + 1):
        previous_stage = current_stage

        day_of_year = t
        r_factor = calculate_earth_sun_distance_factor(day_of_year)
        sin_beta = calculate_sin_beta(latitude, day_of_year)

        E_dir = 0.85 * SOLAR_CONSTANT * r_factor * max(sin_beta, 0)
        E_dif = 0.15 * SOLAR_CONSTANT * r_factor * max(sin_beta, 0)

        PP = calculate_day_length(t, latitude)
        ppf = calculate_ppfun(PP)
        T = temperatures[t - 1] if t <= len(temperatures) else 10

        stage_params = STAGE_PARAMS.get(current_stage, {'Tb': 10, 'To': To, 'Tc': 36})
        Tb = stage_params['Tb']
        tempf = calculate_tempfun(T, Tb, To, Tc)
        werf = 1.0
        wsf = 1.0

        growth_coeff = tempf

        BD_day = max(0.0, tempf * ppf * werf * wsf)
        sum_BD += BD_day
        BD_history.append(BD_day)

        new_stage = get_growth_stage_bd(sum_BD)
        if new_stage != current_stage:
            current_stage = new_stage
            stage_params = STAGE_PARAMS[current_stage]
            Tb = stage_params['Tb']
            To = stage_params['To']

        if current_stage == 1:

            if organs['seed']['biomass'] > 0:
                transfer = organs['seed']['biomass'] * 0.9
                organs['seed']['biomass'] -= transfer
                organs['leaf']['biomass'] = transfer * 0.7
                organs['stem']['biomass'] = transfer * 0.3
                organs['leaf']['count'] = 0
                organs['leaf']['size'] = organs['leaf']['biomass'] * CONVERSION_FACTORS['leaf']
                organs['stem']['diameter'] = 0.1


        elif current_stage == 2:

            if random.random() < 0.5 and organs['leaf']['count'] < 85:
                organs['leaf']['count'] = 12
                organs['leaf']['angles'].append(random.uniform(0, 90))
                organs['leaf']['biomass'] = transfer * allocation_ratio
                organs['leaf']['size'] = organs['leaf']['biomass'] * CONVERSION_FACTORS['leaf']
                organs['stem']['biomass'] = transfer * (1 - allocation_ratio)
                organs['stem']['diameter'] += 0.02
                organs['stem']['biomass'] += 0.2 * growth_coeff
            sink_strength.update({'leaf': 15.0, 'stem': 10.0, 'seed': 0.0})


        elif current_stage == 3:

            organs['stem']['branches'] = np.random.randint(2, 5)
            organs['buds'] = [{'biomass': 0.01, 'maturity': 0.0} for _ in range(5)]
            sink_strength['buds'] = 8.0
            organs['stem']['height'] += 1.2 * growth_coeff
            organs['stem']['diameter'] += 0.03


        elif current_stage == 4:

            if random.random() < 0.25 and organs['leaf']['count'] < 85:
                organs['leaf']['count'] += 1
                organs['leaf']['angles'].append(random.uniform(0, 90))
                organs['leaf']['biomass'] += 0.2 * growth_coeff
                if sum_BD <= 36:
                    organs['leaf']['scale'] = 1.2
                elif 36 < sum_BD <= 45:
                    organs['leaf']['scale'] = 1.0
                organs['leaf']['size'] = organs['leaf']['biomass'] * CONVERSION_FACTORS['leaf'] * organs['leaf']['scale']
            sink_strength['leaf'] = 20.0


        elif current_stage == 5:

            if not organs['buds']:
                num_buds = random.randint(3, 5)
                for bud in organs['buds']:
                    bud['biomass'] += 0.01 * growth_coeff
                organs['buds'] = [{'size': 0.1, 'biomass': 0.01, 'maturity': 0.0} for _ in range(num_buds)]
            organs['stem']['diameter'] += 0.03
            sink_strength['buds'] = 12.0


        elif current_stage == 7:

            if not organs['flowers']:
                num_flowers = random.randint(3, 5)
                organs['flowers'] = [{
                    'size': 0.5,
                    'biomass': 0.0,
                    'pollinated': True,
                    'maturity': 0.0
                } for _ in range(num_flowers)]
            for flower in organs['flowers']:
                flower['biomass'] += 0.02 * growth_coeff

            organs['leaf']['scale'] *= 0.8
            sink_strength.update({'buds': 15.0, 'flowers': 5.0})


        elif current_stage == 8:

            for flower in organs['flowers']:
                flower['size'] = min(1.0, flower['size'] + 0.05)
                flower['biomass'] += 0.02 * growth_coeff
            sink_strength['flowers'] = 20.0


        elif current_stage == 9:
            if previous_stage != 9:
                organs['grain']['capsules'] = [
                    {
                        'seeds': SEEDS_PER_CAPSULE if f['pollinated'] else 0,
                        'size': 0.001,
                        'biomass': 0.0001,
                        'maturity': 0.0
                    } for f in organs['flowers'] if f['pollinated']
                ]
                organs['flowers'] = []

            for capsule in organs['grain']['capsules']:
                capsule['biomass'] += 0.04 * growth_coeff
                capsule['maturity'] += 0.35 * growth_coeff
            sink_strength['grain'] = 25.0

        elif current_stage == 10:

            for capsule in organs['grain']['capsules']:
                capsule['size'] = min(1.0, capsule['size'] + 0.05 * growth_coeff)
                capsule['biomass'] += 0.03 * growth_coeff
                capsule['maturity'] += 0.25 * growth_coeff
            sink_strength['grain'] = 30.0

        elif current_stage == 11:

            yield_total = sum(
                capsule['size'] * capsule['seeds'] * CONVERSION_FACTORS['grain']
                for capsule in organs['grain']['capsules']
                if capsule['maturity'] >= 1.0 or current_stage == 11
            )

        leaf_area = organs['leaf']['size'] * organs['leaf']['count']
        leaf_angle = organs['leaf']['angles']

        absorbed_PAR = calculate_absorbed_PAR(leaf_area, leaf_angle, E_dir, E_dif)
        P_t = calculate_photosynthetic_production(absorbed_PAR, photosynthetic_efficiency)
        C_mr = calculate_maintenance_respiration(total_biomass)
        CAP = max(0, calculate_cap(CAP, P_t, C_mr))

        active_sinks = {k: v for k, v in sink_strength.items() if v > 0}
        S_total = sum(active_sinks.values())

        allocations = {}
        if S_total > 0:
            for organ in active_sinks:
                S_o = active_sinks[organ]
                G_o = calculate_biomass_increment(S_o, S_total, CAP)
                allocations[organ] = G_o
                CAP -= G_o

        for organ in ['leaf', 'stem', 'grain', 'buds', 'flowers']:
            if organ in allocations:
                if organ == 'buds' and organs['buds']:
                    allocation_per = allocations[organ] / len(organs['buds'])
                    for bud in organs['buds']:
                        bud['biomass'] += allocation_per
                elif organ == 'flowers' and organs['flowers']:
                    allocation_per = allocations[organ] / len(organs['flowers'])
                    for flower in organs['flowers']:
                        flower['biomass'] += allocation_per
                else:
                    if isinstance(organs.get(organ, {}), dict):
                        organs[organ]['biomass'] += allocations.get(organ, 0)

        organs['leaf']['size'] = organs['leaf']['biomass'] * CONVERSION_FACTORS['leaf'] * organs['leaf']['scale']
        organs['stem']['height'] = organs['stem']['biomass'] * CONVERSION_FACTORS['stem']
        organs['stem']['diameter'] = max(0.1, organs['stem']['diameter'])

        if t_grain_start <= t <= t_grain_end:
            grain_alloc = allocations.get('grain', 0)
            D_grain_values.append(grain_alloc)

        yield_total = sum(
            capsule['biomass'] * capsule['seeds'] * CONVERSION_FACTORS['grain']
            for capsule in organs['grain']['capsules']
            if capsule['maturity'] >= 0.9
        )

        total_biomass = sum([
            organs['seed']['biomass'],
            organs['leaf']['biomass'],
            organs['stem']['biomass'],
            organs['grain']['biomass'],
            sum(bud['biomass'] for bud in organs['buds']),
            sum(flower['biomass'] for flower in organs['flowers'])
        ])

        results.append((
            t,
            current_stage,
            round(organs['stem']['height'], 1),
            organs['leaf']['count'],
            len(organs['buds']),
            total_biomass,
            round(yield_total, 2)
        ))

        growth_time = days
        for day_data in results:
            if day_data[1] == 11:
                growth_time = day_data[0]
                break

    return yield_total, results, growth_time