# visualization.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


def plot_growth_dynamics(days, all_heights, real_height):
    plt.figure(figsize=(15, 6))

    for i, heights in enumerate(all_heights):
        plt.plot(days, heights, alpha=0.5, linewidth=1.5,
                 label=f'Симуляция {i + 1}' if i < 3 else None)

    plt.axhline(y=real_height, color='#e74c3c', linestyle='--',
                linewidth=2.5, label=f'Реальное значение ({real_height} см)')

    plt.xlabel('Дни роста', fontsize=12)
    plt.ylabel('Высота растения (см)', fontsize=12)
    plt.title('Динамика роста растения', fontsize=14)
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.2)
    plt.show()


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


def plot_statistical_analysis(days, all_heights, real_height):
    heights_matrix = np.array(all_heights)
    mean_heights = np.mean(heights_matrix, axis=0)
    std_heights = np.std(heights_matrix, axis=0)
    median_heights = np.median(heights_matrix, axis=0)

    plt.figure(figsize=(18, 6))

    plt.fill_between(days, mean_heights - std_heights, mean_heights + std_heights,
                     color='#3498db', alpha=0.2)
    plt.plot(days, mean_heights, color='#2980b9', linewidth=2,
             label='Среднее значение')
    plt.plot(days, median_heights, color='#e67e22', linestyle=':',
             linewidth=2, label='Медиана')
    plt.axhline(real_height, color='#e74c3c', linestyle='--',
                linewidth=2, label='Эталон')
    plt.title('Средняя динамика с отклонениями')
    plt.grid(alpha=0.1)
    plt.legend()

    plt.tight_layout()
    plt.show()