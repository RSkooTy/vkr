import numpy as np
from matplotlib import pyplot as plt

#Расчет затрат на поддержание дыхания
def calculate_maintenance_respiration(total_biomass):
    return 0.014 * total_biomass

#Расчет фотосинтетической продукции на основе площади листа и скорости
def calculate_photosynthetic_production(area, rate):
    return area * rate

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

#Расчет урожайности как суммы значений массы зерна от 1 до n_grain
def calculate_grain_yield(D_grain_values, n_grain):
    return sum(D_grain_values[:n_grain])

def plot_results(results, param_name, param_values, ylabel=""):
    days = [res[0] for res in results[0]]
    plt.figure(figsize=(18, 6))

    for i, res in enumerate(results):
        values = [day[-1] for day in res]
        plt.plot(days, values, label=f'{param_name}={param_values[i]}')

    plt.title(f"Динамика показателей при изменении {param_name}")
    plt.xlabel("Дни")
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def calculate_yield(days, initial_leaf_area, photosynthesis_rate, S_o_values, S_total, grain_params, conversion_factors):
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
        P_t = calculate_photosynthetic_production(leaf_area, photosynthesis_rate)
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

if __name__ == "__main__":
    days = 100
    photosynthesis_rate = 10
    S_o_values = [0.1, 0.2, 0.3]
    S_total = sum(S_o_values)
    grain_params = (1, 0.05, 40)
    conversion_factors = [0.023, 0.851, 1.0]

    photosynthesis_rates = [5, 10, 15]
    results_photosynthesis = []
    for rate in photosynthesis_rates:
        yield_result, res = calculate_yield(days, 0.1, rate, S_o_values, S_total, grain_params, conversion_factors)
        print(f"Результаты для скорости фотосинтеза {rate} г/м²:")
        for day, leaf_area, biomass, yield_total in res:
            print(f"День {day}: площадь листа={leaf_area:.2f} м², биомасса={biomass:.2f} г, урожайность={yield_total:.2f} г")
        results_photosynthesis.append(res)

    initial_leaf_areas = [0.05, 0.1, 0.2]
    results_leaf_area = []
    for area in initial_leaf_areas:
        yield_result, res = calculate_yield(days, area, photosynthesis_rate, S_o_values, S_total, grain_params, conversion_factors)
        print(f"Результаты для начальной площади листа {area} м²:")
        for day, leaf_area, biomass, yield_total in res:
            print(f"День {day}: площадь листа={leaf_area:.2f} м², биомасса={biomass:.2f} г, урожайность={yield_total:.2f} г")
        results_leaf_area.append(res)

    # Графики
    plot_results(results_photosynthesis, "Скорость фотосинтеза", photosynthesis_rates, "Урожайность (г)")
    plot_results(results_leaf_area, "Начальная площадь листа", initial_leaf_areas, "Урожайность (г)")
