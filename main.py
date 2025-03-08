from population import genetic_algorithm
from model import calculate_yield
from settings import *
import math

if __name__ == "__main__":
#    best_plant = genetic_algorithm()
#
#    yield_total, results = calculate_yield(
#        days=DAYS,
#        initial_biomass=SEED_MASS,
#        leaf_angle=best_plant.traits[1],
#        grain_params=(FLOWERING_START_DAY, CAPSULE_MASS, GRAIN_FILLING_DURATION)
#    )
#
#    last_day = results[-1]
#    day_num, stage, stem_height, leaf_size, grain_biomass, buds, flowers, capsules, total_biomass, yield_total = last_day
#
#    print("\nРЕЗУЛЬТАТЫ МОДЕЛИРОВАНИЯ:")
#    print(f"Длина стебля: {stem_height:.1f} м")
#    print(f"Площадь листьев: {leaf_size:.2f} м²")
#    print(f"Количество бутонов: {buds}")
#    print(f"Количество цветов: {flowers}")
#    print(f"Количество коробочек: {capsules}")
#    print(f"Общая биомасса: {total_biomass:.2f} г")
#    print(f"Урожайность: {yield_total:.2f} г")
#
    print("_____________________________________________")

    yield_total, results  = calculate_yield(
        days=DAYS,
        initial_leaf_area=0.1,
        leaf_angle=30,
        S_o_values=S_O_VALUES,
        S_total=S_TOTAL,
        grain_params=(FLOWERING_START_DAY, CAPSULE_MASS, GRAIN_FILLING_DURATION),
        conversion_factors=CONVERSION_FACTORS,
        initial_biomass=SEED_MASS
       )

    # Вывод результатов
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