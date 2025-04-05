import matplotlib.pyplot as plt
from settings import DAYS


def plot_results(results, param_name, param_values, ylabel):
    plt.figure(figsize=(10, 6))

    for i, res in enumerate(results):
        days = [r[0] for r in res]
        yield_values = [r[3] for r in res]
        plt.plot(days, yield_values,
                 label=f'{param_name}={param_values[i]}',
                 linewidth=2,
                 alpha=0.7)

    plt.xlabel('Дни', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title('Динамика урожайности', fontsize=14)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlim(0, DAYS)
    plt.xticks(range(0, DAYS + 1, 10))
    plt.tight_layout()
    plt.show()

def print_growth_report(growth_data):
        """Печать детального отчета о росте растения"""
        print("\nДетальный отчет о росте лучшего растения:")
        print(f"{'День':<5} {'Стадия роста':<25} {'Площадь листа (см²)':<20} {'Биомасса (г)':<15} {'Урожай (г)':<10}")
        for day in growth_data[::7]:  # Выводим каждую неделю
            print(
                f"{day['day']:<5} {day['stage']:<25} {day['leaf_area']:<20.2f} {day['total_biomass']:<15.2f} {day['yield']:<10.2f}")

def plot_evolution(fitness_history):
        """Визуализация прогресса эволюции"""
        plt.figure(figsize=(10, 6))
        plt.plot(fitness_history, marker='o', linestyle='-', color='b')
        plt.title('Прогресс эволюционного алгоритма')
        plt.xlabel('Поколение')
        plt.ylabel('Максимальная урожайность (г)')
        plt.grid(True)
