import math
from settings import  CRPAR, LIGHT_INTENSITY

def calculate_absorbed_PAR(leaf_area, leaf_angle, light_intensity):
    """Расчет поглощенной PAR на основе угла листа и интенсивности света."""
    # Упрощенная модель: поглощение зависит от косинуса угла падения света
    absorption_factor = math.cos(math.radians(leaf_angle))
    absorbed_PAR = leaf_area * light_intensity * absorption_factor * CRPAR
    return absorbed_PAR

#Расчет фотосинтетической продукции
def calculate_photosynthetic_production(absorbed_PAR, temperature=25, CO2=400):
    """Модель LEAFC3 (упрощенная версия)."""
    # Параметры модели из статьи (примерные значения)
    alpha = 0.05  # Квантовая эффективность
    beta = 0.1     # Коэффициент дыхания
    photosynthesis = alpha * absorbed_PAR - beta * temperature
    return max(0, photosynthesis)

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


def calculate_yield(days, initial_leaf_area, leaf_angle, S_o_values, S_total, grain_params, conversion_factors):
    CAP = 0
    yield_total = 0
    total_biomass = 0
    leaf_area = initial_leaf_area
    organ_biomass = {i: 0 for i in range(len(S_o_values))}
    organ_sizes = {i: 0 for i in range(len(S_o_values))}
    D_grain_values = []

    t_grain_start, D_flower, t_grain_duration = grain_params
    t_grain_end = t_grain_start + t_grain_duration
    n_gmax = 0

    results = []

    for t in range(1, days + 1):
        absorbed_PAR = calculate_absorbed_PAR(leaf_area, leaf_angle, LIGHT_INTENSITY)

        P_t = calculate_photosynthetic_production(absorbed_PAR)
        C_mr = calculate_maintenance_respiration(total_biomass)
        CAP = calculate_cap(CAP, P_t, C_mr)

        for i, S_o in enumerate(S_o_values):
            biomass_increment = calculate_biomass_increment(S_o, S_total, CAP)
            CAP -= biomass_increment
            organ_biomass[i] = update_biomass(organ_biomass[i], biomass_increment)
            organ_size_increment = calculate_organ_size_growth(biomass_increment, conversion_factors[i])
            organ_sizes[i] += organ_size_increment

        total_biomass = sum(organ_biomass.values())
        leaf_area = organ_sizes[0]

        if t >= t_grain_start:
            grain_growth = calculate_biomass_increment(S_o_values[-1], S_total, CAP)
            CAP -= grain_growth
            D_grain_values.append(grain_growth / D_flower)
            n_gmax = max(n_gmax, len(D_grain_values))

        if t <= t_grain_end:
            yield_total = calculate_grain_yield(D_grain_values, len(D_grain_values))
        else:
            yield_total = calculate_grain_yield(D_grain_values, n_gmax)

        results.append((t, leaf_area, total_biomass, yield_total))

    return yield_total, results