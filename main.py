from population import genetic_algorithm
from model import calculate_yield
from settings import *
import math

if __name__ == "__main__":

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