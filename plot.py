import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


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

    plt.xlabel('Дни', fontsize=12)
    plt.ylabel('Урожайность (г)', fontsize=12)
    plt.title('Динамика урожайности', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(alpha=0.2)
    plt.xticks(np.arange(0, max(max(days_before), max(days_after)) + 1, 5))
    plt.tight_layout()


def plot_fitness_and_diversity(diversity_history, title=""):
    plt.figure(figsize=(12, 6))

    plt.plot(diversity_history, color='blue')
    plt.xlabel('Итерация')
    plt.ylabel('Стандартное отклонение')
    plt.title(f'Разнообразие популяции: {title}')
    plt.grid(alpha=0.3)

    plt.tight_layout()


def plot_unified_biomass(days, cap_data, leaf_data, stem_data, grain_data, title=""):
    plt.figure(figsize=(12, 6))

    scale_factor = 25 / max(cap_data + leaf_data + stem_data + grain_data)

    cap_norm = [x * scale_factor for x in cap_data]
    leaf_norm = [x * scale_factor for x in leaf_data]
    stem_norm = [x * scale_factor for x in stem_data]
    grain_norm = [x * scale_factor for x in grain_data]

    plt.plot(days, cap_norm,
             label='Центральный ассимиляционный пул',
             color='#e74c3c',
             linewidth=3,
             linestyle='-')

    plt.plot(days, leaf_norm,
             label='Биомасса листьев',
             color='#2ecc71',
             linestyle='--',
             alpha=0.8)

    plt.plot(days, stem_norm,
             label='Биомасса стебля',
             color='#3498db',
             linestyle='-.',
             alpha=0.8)

    plt.plot(days, grain_norm,
             label='Биомасса зерен',
             color='#9b59b6',
             linestyle=':',
             alpha=0.8)

    plt.xlabel('Время роста (дни)', fontsize=12)
    plt.ylabel('Биомасса', fontsize=12)
    plt.title(f'Динамика биомассы органов: {title}', fontsize=14)
    plt.legend(loc='upper left', ncol=2, frameon=False)


    plt.grid(True, alpha=0.2)
    plt.xticks(np.arange(0, max(days) + 1, 20))
    plt.xlim(0, max(days))
    plt.ylim(0, 25)
    plt.tight_layout()


def plot_yield_simulations(all_yield_curves, start_days):
    plt.figure(figsize=(12, 6))

    all_yields = []
    max_length = 0
    for days, yields in all_yield_curves:
        if len(yields) > max_length:
            max_length = len(yields)
        all_yields.append(yields)

    min_values = []
    max_values = []
    mean_values = []

    for day_idx in range(max_length):
        daily_values = []
        for curve in all_yields:
            if day_idx < len(curve):
                daily_values.append(curve[day_idx])
        min_values.append(np.min(daily_values) if daily_values else 0)
        max_values.append(np.max(daily_values) if daily_values else 0)
        mean_values.append(np.mean(daily_values) if daily_values else 0)

    days = range(len(mean_values))

    plt.fill_between(
        days,
        min_values,
        max_values,
        color='#3498db',
        alpha=0.2,
        label='Диапазон'
    )

    plt.plot(
        days,
        mean_values,
        color='#e74c3c',
        linewidth=2,
        label='Средняя урожайность'
    )

    plt.xlabel('Дни', fontsize=12)
    plt.ylabel('Урожайность, г', fontsize=12)
    plt.title('Динамика урожайности', fontsize=14)
    plt.legend()
    plt.grid(alpha=0.2)
    plt.xticks(np.arange(0, max_length + 1, 5))
    plt.xlim(0, max_length)
    plt.tight_layout()


def plot_snp_evolution(snp_history, param_names):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    styles = [
        {'color': '#E64A19', 'lw': 2, 'ls': '-'},
        {'color': '#1976D2', 'lw': 2, 'ls': '-'},
        {'color': '#388E3C', 'lw': 2, 'ls': '-'},
        {'color': '#7B1FA2', 'lw': 2, 'ls': '-'}
    ]

    for i, (name, style) in enumerate(zip(param_names, styles)):
        ax = axes[i // 2, i % 2]
        param_key = f'param_{i}'
        values = [gen_data[param_key] for gen_data in snp_history]

        ax.plot(values, **style, markersize=6, markevery=15, alpha=0.8)

        ax.set_title(name, fontsize=12, pad=10)
        ax.set_xlabel('Итерация', fontsize=10)
        ax.set_ylabel('Значение', fontsize=10)
        ax.grid(alpha=0.2)

    fig.suptitle('Эволюция параметров растения по поколениям')

    plt.tight_layout()


def plot_optimized_convergence(fitness_history):
    plt.figure(figsize=(12, 6))

    plt.plot(fitness_history,
             color='#2ecc71',
             linewidth=2.5,
             marker='o',
             markersize=8,
             markevery=5,
             markerfacecolor='white',
             markeredgecolor='#27ae60')

    plt.title('Кривая сходимости оптимизированного алгоритма', fontsize=14)
    plt.xlabel('Номер итерации ГА', fontsize=12)
    plt.ylabel('Лучшее значение целевой функции', fontsize=12)
    plt.grid(alpha=0.2)
    plt.xticks(np.arange(0, len(fitness_history) + 1, 5))


    plt.tight_layout()


import matplotlib.pyplot as plt
import numpy as np


def plot_snp_distribution(snapshots, stage_names=('Начало', 'Середина', 'Финал')):
    colors = {'0': '#FF6B6B', '1': '#4D96FF', 'best': '#82CD47'}
    BIN_SIZE = 10

    for i, snapshot in enumerate(snapshots):
        if not snapshot:
            continue

        genomes = [ind[0] for ind in snapshot]
        fitness = [ind[1] for ind in snapshot]
        best_idx = np.argmax(fitness)
        best_genome = genomes[best_idx]
        population = np.array(genomes)
        genome_len = population.shape[1]

        trimmed_len = (genome_len // BIN_SIZE) * BIN_SIZE
        population = population[:, :trimmed_len]
        best_genome = best_genome[:trimmed_len]
        genome_len = trimmed_len

        if population.size == 0 or best_genome.size == 0:
            continue

        n_bins = genome_len // BIN_SIZE
        binned_population = np.array([
            ind.reshape(-1, BIN_SIZE).mean(axis=1)
            for ind in population
        ])
        freq_1 = binned_population.mean(axis=0)
        freq_0 = 1 - freq_1

        best_binned = best_genome.reshape(-1, BIN_SIZE).mean(axis=1)

        x = np.arange(n_bins) * BIN_SIZE + BIN_SIZE / 2

        plt.figure(figsize=(12, 8), dpi=120)
        ax = plt.gca()

        ax.bar(
            x, freq_0,
            width=BIN_SIZE * 0.8,
            color=colors['0'],
            edgecolor='white',
            label='0'
        )
        ax.bar(
            x, freq_1,
            width=BIN_SIZE * 0.8,
            bottom=freq_0,
            color=colors['1'],
            edgecolor='white',
            label='1'
        )

        ax.plot(
            x, best_binned,
            color=colors['best'],
            linewidth=3,
            marker='o',
            markersize=8,
            label='Лучший результат'
        )

        ax.set_title(f"{stage_names[i]}")
        ax.set_xlabel('SNP')
        ax.set_xticks(np.arange(0, genome_len + 1, 200))
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()


def plot_snp_mosaic(snapshots, stage_names=('Начало', 'Середина', 'финал')):

    cmap = ListedColormap(['#FF6B6B','#4D96FF'])

    for i, snapshot in enumerate(snapshots):
        if not snapshot:
            continue

        genomes = np.array([ind[0] for ind in snapshot])
        n_individuals, genome_len = genomes.shape

        block_size = genome_len // 100
        grouped = genomes.reshape(n_individuals, 100, block_size)
        mosaic = np.mean(grouped, axis=2)

        plt.figure(figsize=(12, 8))
        plt.imshow(mosaic, cmap=cmap, vmin=0, vmax=1, aspect='auto')

        plt.title(f"{stage_names[i]} |", fontsize=14)
        plt.xlabel('SNP', fontsize=12)
        plt.ylabel('число индивидов в популяции', fontsize=12)

        cbar = plt.colorbar(ticks=[0, 1])
        cbar.set_label('0:  Red| 1: Blue ', rotation=270, labelpad=20)

        plt.tight_layout()


def plot_snp_distribution_v2(snapshots, stage_names=('Начало v2', 'Середина v2', 'Финал v2')):
    colors = {'0': '#FF6B6B', '1': '#4D96FF', 'best': '#82CD47'}

    for i, snapshot in enumerate(snapshots):
        if not snapshot:
            continue

        genomes = [ind[0] for ind in snapshot]
        fitness = [ind[1] for ind in snapshot]
        best_idx = np.argmax(fitness)
        best_genome = genomes[best_idx]
        population = np.array(genomes)

        genome_len = 100
        n_bins = genome_len

        freq_1 = population.mean(axis=0)
        freq_0 = 1 - freq_1

        best_binned = best_genome

        x = np.arange(n_bins)

        plt.figure(figsize=(15, 6), dpi=100)
        ax = plt.gca()

        ax.bar(x, freq_0, width=0.8, color=colors['0'], edgecolor='white', label='0')
        ax.bar(x, freq_1, width=0.8, bottom=freq_0, color=colors['1'], edgecolor='white', label='1')

        ax.scatter(x, best_binned, color=colors['best'], s=30, zorder=3,
                   label='Лучший результат', edgecolor='black', linewidth=0.5)

        ax.set_title(f"Распределение SNP ({stage_names[i]})", fontsize=14)
        ax.set_xlabel('Номер SNP', fontsize=12)
        ax.set_ylabel('Частота аллелей', fontsize=12)
        ax.set_xticks(np.arange(0, 100, 10))
        ax.set_xlim(-0.5, 99.5)
        ax.grid(axis='y', alpha=0.3)
        ax.legend(loc='upper right')

        plt.tight_layout()


def plot_snp_mosaic_v2(snapshots, stage_names=('Начало v2', 'Середина v2', 'Финал v2')):
    cmap = ListedColormap(['#FF6B6B', '#4D96FF'])

    for i, snapshot in enumerate(snapshots):
        if not snapshot:
            continue

        genomes = np.array([ind[0] for ind in snapshot])
        n_individuals = len(genomes)

        plt.figure(figsize=(18, 8))
        plt.imshow(genomes, cmap=cmap, aspect='auto', vmin=0, vmax=1)

        plt.title(f"Мозаика SNP ({stage_names[i]})", fontsize=14)
        plt.xlabel('Номер SNP (0-99)', fontsize=12)
        plt.ylabel('Особи популяции', fontsize=12)

        cbar = plt.colorbar(ticks=[0, 1])
        cbar.set_label('0: Красный | 1: Синий', rotation=270, labelpad=20)

        plt.xticks(np.arange(0, 100, 5), np.arange(0, 100, 5))
        plt.yticks(np.arange(0, n_individuals, 5))

        plt.tight_layout()
