from population import genetic_algorithm_basic_1, genetic_algorithm_optimized_1, generate_configs_1, Plant_1
from model import calculate_yield
from settings import *
from plot import *
from population_2 import generate_configs_2, Plant_2, genetic_algorithm_optimized_2, genetic_algorithm_basic_2


configs = generate_configs_1()
Plant_1.set_configs(configs)


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

    configs = generate_configs_1()

    print("_____________________________________________")
    print("Температура на протяжении дней:")
    print(temperatures)
    best_optimized_1,fitness_history_1, diversity_history_1, snp_history_1, snapshot_1 = genetic_algorithm_optimized_1(configs)
    traits_optimized_1 = best_optimized_1.decode_traits()

    yield_total_1, results_1, growth_times_1, cap_hist_1, leaf_hist_1, stem_hist_1, grain_hist_1 = calculate_yield(
        days=DAYS,
        grain_params=(FLOWERING_START_DAY, CAPSULE_MASS, GRAIN_FILLING_DURATION),
        initial_biomass=SEED_MASS,
        temperatures=temperatures,
        latitude=55.7,
        traits=traits_optimized_1

    )

    print(f"Общая урожайность: {yield_total_1:.2f} г")
    print("\nДинамика роста:")
    print("{:<5} {:<7} {:<12} {:<8} {:<8} {:<12} {:<10}".format(
    "День", "Стадия", "Высота, см", "Листья", "Бутоны", "Биомасса, г", "Урожай, г"
    ))

    for day_data in results_1:
        day, stage, stem_h, leaves, buds, biomass, yield_t = day_data
        print("{:<5} {:<7} {:<12.1f} {:<8} {:<8} {:<12.2f} {:<10.2f}".format(
            day, stage, stem_h, leaves, buds, biomass, yield_t
        ))


    num_simulations = 20
    all_heights = []
    real_height = 78.97
    all_yields = []
    all_yield_curves = []
    start_days = []
    all_simulations_data = []

    for _ in range(num_simulations):
        yield_total_2, results_2, growth_times_2, cap_hist_2, leaf_hist_2, stem_hist_2, grain_hist_2 = calculate_yield(
            days=DAYS,
            grain_params=(FLOWERING_START_DAY, CAPSULE_MASS, GRAIN_FILLING_DURATION),
            initial_biomass=SEED_MASS,
            temperatures=temperatures,
            latitude=55.7,
            traits=traits_optimized_1
        )

        all_simulations_data.append(results_2)

        first_yield_day = next((i for i, r in enumerate(results_2) if r[6] > 0), None)
        if first_yield_day is not None:

            trimmed_days = [r[0] - results_2[first_yield_day][0] for r in results_2[first_yield_day:]]
            trimmed_yield = [r[6] for r in results_2[first_yield_day:]]

            all_yield_curves.append((trimmed_days, trimmed_yield))
            start_days.append(results_2[first_yield_day][0])

        heights = [r[2] for r in results_2]
        all_heights.append(heights)

    final_heights = [h[-1] for h in all_heights]


    plot_final_heights_comparison(final_heights, real_height)
    plot_yield_simulations(all_yield_curves, start_days)

    print("\n" + "=" * 50)
    print("Статистика по 20 симуляциям:")
    print("{:<6} {:<8} {:<8} {:<8} {:<10} {:<10}".format(
        "Симуляция", "Высота", "Листья", "Бутоны", "Биомасса", "Урожай"
    ))

    total_height = 0
    total_leaves = 0
    total_buds = 0
    total_biomass = 0
    total_yield = 0

    for i in range(num_simulations):
        last_day_data = all_simulations_data[i][-1]
        height = last_day_data[2]
        leaves = last_day_data[3]
        buds = last_day_data[4]
        biomass = last_day_data[5]
        yield_t = last_day_data[6]

        print("{:<8} {:<8.1f} {:<8} {:<8} {:<10.2f} {:<10.2f}".format(
            i + 1, height, leaves, buds, biomass, yield_t
        ))

        total_height += height
        total_leaves += leaves
        total_buds += buds
        total_biomass += biomass
        total_yield += yield_t

    print("\nСредние значения:")
    print("{:<8} {:<8.1f} {:<8.1f} {:<8.1f} {:<10.2f} {:<10.2f}".format(
        "",
        total_height / num_simulations,
        total_leaves / num_simulations,
        total_buds / num_simulations,
        total_biomass / num_simulations,
        total_yield / num_simulations
    ))


    random.seed(42)
    np.random.seed(42)
    
    print("=" * 50)
    print("Population - v1")
    print("Начало работы генетического алгоритма оптимизации растений")
    print(f"Параметры среды:\n- Дней роста: {DAYS}\n- Размер популяции: {POPULATION_SIZE}")
    print(f" - Мутация: {MUTATION_RATE * 100} %\n - Итераций: {ITERATIONS}")

    print("\n" + "=" * 50)
    print("Запуск базовой версии алгоритма...")
    best_basic, diversity_history_basic = genetic_algorithm_basic_1(configs)
    traits_basic = best_basic.decode_traits()
    yield_basic, results_basic, growth_time_basic, cap_hist_basic, leaf_hist_basic, stem_hist_basic, grain_hist_basic = calculate_yield(
        days=DAYS,
        grain_params=(FLOWERING_START_DAY, CAPSULE_MASS, GRAIN_FILLING_DURATION),
        initial_biomass=SEED_MASS,
        temperatures=temperatures,
        latitude=55.7,
        traits=traits_basic
    )

    print("\n" + "=" * 50)
    print("Запуск оптимизированной версии алгоритма...")
    best_optimized, fitness_history, diversity_history_optimize, snp_history, snapshots = genetic_algorithm_optimized_1(configs)
    traits_optimized = best_optimized.decode_traits()
    yield_optimized, results_optimized, growth_time_optimized, cap_hist_opt, leaf_hist_opt, stem_hist_opt, grain_hist_opt = calculate_yield(
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

    plot_fitness_and_diversity(diversity_history_optimize, "Оптимизированная версия")
    plot_fitness_and_diversity(diversity_history_basic, "Базовая версия")

    days_list = list(range(1, DAYS + 1 ))
    plot_unified_biomass(days_list, cap_hist_opt, leaf_hist_opt, stem_hist_opt, grain_hist_opt,title = "Оптимизированная версия")
    plot_unified_biomass(days_list, cap_hist_basic, leaf_hist_basic, stem_hist_basic, grain_hist_basic, title = "Базовая версия")

    param_names = [
        'Коэффициент аллокации',
        'Угол листьев',
        'Эффективность фотосинтеза',
        'Термотолерантность'
    ]
    plot_snp_evolution(snp_history, param_names)

    plot_optimized_convergence(fitness_history)

    iteration_names = ['Инициализация', 'Середина', 'Финал']
    plot_snp_distribution(snapshots)
    plot_snp_mosaic(snapshots)

    #-----------------------------------------------------
    #Версия алгоритма оптимизации с 100 SNP
    #-----------------------------------------------------
    print("----------------------------------------------------------------------------------------------------------")
    print("----------------------------------------------------------------------------------------------------------")
    print("Версия алгоритма оптимизации с 100 SNP")
    print("----------------------------------------------------------------------------------------------------------")
    print("----------------------------------------------------------------------------------------------------------")

    configs_2 = generate_configs_2()
    Plant_2.set_configs(configs_2)

    print("=" * 50)
    print("Population - v2")
    print("Начало работы генетического алгоритма оптимизации растений")
    print(f"Параметры среды:\n- Дней роста: {DAYS}\n- Размер популяции: {POPULATION_SIZE}")
    print(f" - Мутация: {MUTATION_RATE * 100} %\n - Итераций: {ITERATIONS}")

    print("\n" + "=" * 50)
    print("Запуск базовой версии алгоритма...")
    best_basic_2, diversity_history_basic_2 = genetic_algorithm_basic_2(configs_2)
    traits_basic_2 = best_basic_2.decode_traits()
    yield_basic_2, results_basic_2, growth_time_basic_2, cap_hist_basic_2, leaf_hist_basic_2, stem_hist_basic_2, grain_hist_basic_2 = calculate_yield(
        days=DAYS,
        grain_params=(FLOWERING_START_DAY, CAPSULE_MASS, GRAIN_FILLING_DURATION),
        initial_biomass=SEED_MASS,
        temperatures=temperatures,
        latitude=55.7,
        traits=traits_basic_2
    )

    print("\n" + "=" * 50)
    print("Запуск оптимизированной версии алгоритма...")
    best_optimized_2, fitness_history_2, diversity_history_optimize_2, snp_history_2, snapshots_2 = genetic_algorithm_optimized_2(
        configs_2)
    traits_optimized_2 = best_optimized_2.decode_traits()
    yield_optimized_2, results_optimized_2, growth_time_optimized_2, cap_hist_opt_2, leaf_hist_opt_2, stem_hist_opt_2, grain_hist_opt_2 = calculate_yield(
        days=DAYS,
        grain_params=(FLOWERING_START_DAY, CAPSULE_MASS, GRAIN_FILLING_DURATION),
        initial_biomass=SEED_MASS,
        temperatures=temperatures,
        latitude=55.7,
        traits=traits_optimized_2
    )

    print("\n" + "=" * 50)
    print("Итоговые результаты оптимизации:")
    print(f"{'Параметр':<25} | {'Базовая версия':<15} | {'Оптимизированная':<15}")
    print("-" * 65)
    print(f"{'Урожайность (г)':<25} | {yield_basic_2:<15.2f} | {yield_optimized_2:<15.2f}")
    print(f"{'Прирост (%)':<25} | {'-':<15} | {(yield_optimized_2 / yield_basic_2 - 1) * 100:<15.1f}")
    print("\nОптимизированные параметры растения:")
    print(f"- Коэффициент аллокации: {traits_optimized_2[0]:.2f}")
    print(f"- Угол листьев: {traits_optimized_2[1]:.1f}°")
    print(f"- Эффективность фотосинтеза: {traits_optimized_2[2]:.3f}")
    print(f"- Термотолерантность: {traits_optimized_2[3]:.1f}°C")

    print_results(results_basic_2, "Базовый алгоритм - динамика роста")
    print_results(results_optimized_2, "Оптимизированный алгоритм - динамика роста")

    plot_yield_growth(results_basic_2, results_optimized_2)

    plot_fitness_and_diversity(diversity_history_optimize_2, "Оптимизированная версия")
    plot_fitness_and_diversity(diversity_history_basic_2, "Базовая версия")

    days_list = list(range(1, DAYS + 1))
    plot_unified_biomass(days_list, cap_hist_opt_2, leaf_hist_opt_2, stem_hist_opt_2, grain_hist_opt_2,
                         title="Оптимизированная версия")
    plot_unified_biomass(days_list, cap_hist_basic_2, leaf_hist_basic_2, stem_hist_basic_2, grain_hist_basic_2,
                         title="Базовая версия")

    param_names = [
        'Коэффициент аллокации',
        'Угол листьев',
        'Эффективность фотосинтеза',
        'Термотолерантность'
    ]
    plot_snp_evolution(snp_history_2, param_names)

    plot_optimized_convergence(fitness_history_2)

    plot_snp_distribution(snapshots_2)
    plot_snp_mosaic_v2(snapshots_2)
    plt.show()




