import numpy as np

from population import genetic_algorithm
from model import calculate_yield
from model_2 import calculate_yield2
from settings import *
from plot import *

if __name__ == "__main__":

    print("_____________________________________________")
    print("Температура на протяжении дней:")
    print(temperatures)

    yield_total, results = calculate_yield(
        days=DAYS,
        grain_params=(FLOWERING_START_DAY, CAPSULE_MASS, GRAIN_FILLING_DURATION),
        initial_biomass=SEED_MASS,
        temperatures=temperatures,
        latitude=55.7

    )

    print(f"Общая урожайность: {yield_total:.2f} г")
    print("\nДинамика роста:")
    print("{:<5} {:<7} {:<12} {:<8} {:<8} {:<12} {:<10}".format(
    "День", "Стадия", "Высота, см", "Листья", "Бутоны", "Биомасса, г", "Урожай, г"
    ))

    for day_data in results:
        day, stage, stem_h, leaves, buds, biomass, yield_t = day_data
        print("{:<5} {:<7} {:<12.1f} {:<8} {:<8} {:<12.2f} {:<10.2f}".format(
            day, stage, stem_h, leaves, buds, biomass, yield_t
        ))

    print("Запуск генетического алгоритма...")
    best_plant = genetic_algorithm()

    yield_total, results = calculate_yield2(
        days=DAYS,
        grain_params=(FLOWERING_START_DAY, CAPSULE_MASS, GRAIN_FILLING_DURATION),
        initial_biomass=SEED_MASS,
        temperatures=temperatures,
        latitude=55.7,
        traits=best_plant.traits
    )

    max_height = max([r[2] for r in results])
    max_biomass = max([r[5] for r in results])
    final_yield = results[-1][6]

    print("\nРезультаты работы алгоритма:")
    print(f"Лучшая особь с параметрами:")
    print(f"• Распределение биомассы: {best_plant.traits[0]:.2f}")
    print(f"• Угол листьев: {best_plant.traits[1]}°")
    print(f"• Эффективность фотосинтеза: {best_plant.traits[2]:.3f}")
    print(f"• Термоустойчивость: ±{best_plant.traits[3]:.1f}°C")
    print(f"• Максимальная высота: {max_height:.1f} см")
    print(f"• Максимальная биомасса: {max_biomass:.2f} г")
    print(f"• Итоговая урожайность: {final_yield:.2f} г")

    num_simulations = 20
    all_heights = []
    real_height = 78.97

    print("\nПроведение множественных симуляций...")
    for _ in range(num_simulations):
        yield_total, results = calculate_yield(
            days=DAYS,
            grain_params=(FLOWERING_START_DAY, CAPSULE_MASS, GRAIN_FILLING_DURATION),
            initial_biomass=SEED_MASS,
            temperatures=temperatures,
            latitude=55.7
        )
        heights = [r[2] for r in results]
        all_heights.append(heights)

    days = [r[0] for r in results]
    final_heights = [h[-1] for h in all_heights]

    plot_growth_dynamics(days, all_heights, real_height)
    plot_final_heights_comparison(final_heights, real_height)
    plot_statistical_analysis(days, all_heights, real_height)