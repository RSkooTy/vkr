
from population import genetic_algorithm_basic, genetic_algorithm_optimized, generate_configs, Plant
from model import calculate_yield
from settings import *
from plot import *

configs = generate_configs()
Plant.set_configs(configs)


def print_results(results, title):
    print(f"\n{title}:")
    print("{:<5} {:<7} {:<12} {:<8} {:<8} {:<12} {:<10}".format(
        "День", "Стадия", "Высота, см", "Листья", "Бутоны", "Биомасса, г", "Урожай, г"
    ))
    for day_data in results:
        day, stage, stem_h, leaves, buds, biomass, yield_t = day_data
        print("{:<5} {:<7} {:<12.1f} {:<8} {:<8} {:<12.2f} {:<10.2f}".format(
            day, stage, stem_h, leaves, buds, biomass, yield_t
        ))


if __name__ == "__main__":

    random.seed(42)
    np.random.seed(42)

    configs = generate_configs()

    print("_____________________________________________")
    print("Температура на протяжении дней:")
    print(temperatures)
    best_optimized = genetic_algorithm_optimized(configs)
    traits_optimized = best_optimized.decode_traits()

    yield_total, results, growth_times = calculate_yield(
        days=DAYS,
        grain_params=(FLOWERING_START_DAY, CAPSULE_MASS, GRAIN_FILLING_DURATION),
        initial_biomass=SEED_MASS,
        temperatures=temperatures,
        latitude=55.7,
        traits=traits_optimized

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

    num_simulations = 20
    all_heights = []
    real_height = 78.97

    for _ in range(num_simulations):
        yield_total, results, growth_times = calculate_yield(
            days=DAYS,
            grain_params=(FLOWERING_START_DAY, CAPSULE_MASS, GRAIN_FILLING_DURATION),
            initial_biomass=SEED_MASS,
            temperatures=temperatures,
            latitude=55.7,
            traits=traits_optimized
        )
        heights = [r[2] for r in results]
        all_heights.append(heights)

    days = [r[0] for r in results]
    final_heights = [h[-1] for h in all_heights]

    plot_final_heights_comparison(final_heights, real_height)


    random.seed(42)
    np.random.seed(42)

    print("=" * 50)
    print("Начало работы генетического алгоритма оптимизации растений")
    print(f"Параметры среды:\n- Дней роста: {DAYS}\n- Размер популяции: {POPULATION_SIZE}")
    print(f" - Мутация: {MUTATION_RATE * 100} %\n - Итераций: {ITERATIONS}")

    print("\n" + "=" * 50)
    print("Запуск базовой версии алгоритма...")
    best_basic = genetic_algorithm_basic(configs)
    traits_basic = best_basic.decode_traits()
    yield_basic, results_basic, growth_time_basic = calculate_yield(
        days=DAYS,
        grain_params=(FLOWERING_START_DAY, CAPSULE_MASS, GRAIN_FILLING_DURATION),
        initial_biomass=SEED_MASS,
        temperatures=temperatures,
        latitude=55.7,
        traits=traits_basic
    )

    print("\n" + "=" * 50)
    print("Запуск оптимизированной версии алгоритма...")
    best_optimized = genetic_algorithm_optimized(configs)
    traits_optimized = best_optimized.decode_traits()
    yield_optimized, results_optimized, growth_time_optimized = calculate_yield(
        days=DAYS,
        grain_params=(FLOWERING_START_DAY, CAPSULE_MASS, GRAIN_FILLING_DURATION),
        initial_biomass=SEED_MASS,
        temperatures=temperatures,
        latitude=55.7,
        traits=traits_optimized
    )

    print("\n" + "=" * 50)
    print("Итоговые результаты оптимизации:")
    print(f"{'Параметр':<25} | {'Базовая версия':<15} | {'Оптимизированная':<15}")
    print("-" * 65)
    print(f"{'Урожайность (г)':<25} | {yield_basic:<15.2f} | {yield_optimized:<15.2f}")
    print(f"{'Прирост (%)':<25} | {'-':<15} | {(yield_optimized / yield_basic - 1) * 100:<15.1f}")
    print("\nОптимизированные параметры растения:")
    print(f"- Коэффициент аллокации: {traits_optimized[0]:.2f}")
    print(f"- Угол листьев: {traits_optimized[1]:.1f}°")
    print(f"- Эффективность фотосинтеза: {traits_optimized[2]:.3f}")
    print(f"- Термотолерантность: {traits_optimized[3]:.1f}°C")

    print_results(results_basic, "Базовый алгоритм - динамика роста")
    print_results(results_optimized, "Оптимизированный алгоритм - динамика роста")

    plot_yield_growth(results_basic, results_optimized)






