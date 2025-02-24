from openalea.plantgl.all import *
from population import genetic_algorithm



if __name__ == "__main__":
    best_plant = genetic_algorithm()
    print(f"Лучшие признаки: площадь листа(cm): {best_plant.traits[0]}, угол поворота листа:  {best_plant.traits[1]}, Урожайность: {best_plant.calculate_fitness()}")

