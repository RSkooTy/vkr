import numpy as np
import matplotlib.pyplot as plt

def plot_final_heights_comparison(final_heights, real_height):
    plt.figure(figsize=(10, 6))
    simulation_numbers = np.arange(1, len(final_heights) + 1)

    plt.scatter(simulation_numbers, final_heights,
                c='#2ecc71', s=100, edgecolor='black',
                alpha=0.8, label='Результаты симуляций')

    plt.axhline(real_height, color='#e74c3c', linestyle='--',
                linewidth=2.5, label='Эталонное значение')

    for x, y in zip(simulation_numbers, final_heights):
        plt.plot([x, x], [y, real_height], color='#3498db',
                 alpha=0.4, linestyle=':', linewidth=1.5)

    plt.xticks(simulation_numbers)
    plt.xlim(0.5, len(final_heights) + 0.5)
    plt.ylim(min(final_heights + [real_height]) - 5,
             max(final_heights + [real_height]) + 5)

    for i, h in enumerate(final_heights):
        plt.text(i + 1, h + 0.5, f'{h:.1f} см', ha='center',
                 va='bottom', fontsize=9, color='#2c3e50')

    plt.xlabel('Номер симуляции', fontsize=12)
    plt.ylabel('Финальная высота (см)', fontsize=12)
    plt.title('Сравнение с эталоном', fontsize=14)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15))
    plt.grid(True, axis='y', alpha=0.2)
    plt.tight_layout()
    plt.show()

def plot_yield_growth(results_before, results_after):
    plt.figure(figsize=(12, 6))

    def find_first_yield_day(results):
        for day_data in results:
            if day_data[6] > 0:
                return day_data[0]
        return 0

    start_day_before = find_first_yield_day(results_before)
    start_day_after = find_first_yield_day(results_after)

    filtered_before = [d for d in results_before if d[0] >= start_day_before]
    filtered_after = [d for d in results_after if d[0] >= start_day_after]

    days_before = [d[0] - start_day_before + 1 for d in filtered_before]
    yield_before = [d[6] for d in filtered_before]

    days_after = [d[0] - start_day_after + 1 for d in filtered_after]
    yield_after = [d[6] for d in filtered_after]

    plt.plot(days_before, yield_before,
             label='До оптимизации',
             color='blue')

    plt.plot(days_after, yield_after,
             label='После оптимизации',
             color='red')

    plt.xlabel('Дни с начала роста урожайности', fontsize=12)
    plt.ylabel('Урожайность (г)', fontsize=12)
    plt.title('Динамика урожайности с момента её начала', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(alpha=0.2)
    plt.xticks(np.arange(0, max(max(days_before), max(days_after)) + 1, 5))
    plt.tight_layout()
    plt.show()


