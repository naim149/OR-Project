import csv
import random
import numpy as np
from datetime import datetime
from Managers.optimizationInstance_manager import OptimizationInstanceManager
from Managers.optimization_manager import OptimizationManager
from Algorithms.heuristic_algorithm import HeuristicOptimization  
from Algorithms.gurobi_algorithm import GurobiOptimization  
from Algorithms.gurobi_hybrid import GurobiHybridOptimization  
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Flags
remove_axis_numbering = True
hide_values_in_table = True
hide_results_in_header = False

def main():
    # Fixed parameters
    seed = 0
    N = 200
    s = 65
    T = 16
    delta_T = 0.5

    algorithms = []
    algorithms.append(GurobiHybridOptimization())
    # algorithms.append(HeuristicOptimization())

    if not os.path.exists('Allocations Results'):
        os.makedirs('Allocations Results')

    optimization_instance = initialize_instance(seed, N, s, T, delta_T)

    fig, axs = plt.subplots(len(algorithms), 1, figsize=(10, 8), gridspec_kw={'hspace': 0.5})

    if len(algorithms) == 1:
        axs = [axs]

    for i, algorithm in enumerate(algorithms):
        algorithm_name = algorithm.name
        result = run_optimization(optimization_instance, algorithm)

        B = np.array(result['B'])
        U = np.array(result['U'])
        Y = np.array(result['Y'])
        Z = result['min_usage_time']

        create_colored_heatmap(axs[i], B, U, Y, T, delta_T, N, s, algorithm_name, Z)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Allocations_Results_Compiled_{timestamp}.png"
    plt.savefig(f'Allocations Results/{filename}', bbox_inches='tight')
    plt.close()

def initialize_instance(seed, N, s, T, delta_T):
    random.seed(seed)
    manager = OptimizationInstanceManager(seed)
    optimization_instance = manager.create_instance(N, s, T, delta_T)
    return optimization_instance

def run_optimization(optimization_instance, algorithm):
    optimization_manager = OptimizationManager([algorithm])
    optimizationResults = optimization_manager.run_optimization(optimization_instance)
    return optimizationResults[0][1]  

def create_colored_heatmap(ax, B, U, Y, T, delta_T, N, s, algorithm_name, Z):
    num_intervals = int(T / delta_T)
    num_students = N
    avg_usage = np.mean(U)*num_intervals

    data = np.round(B[:, :num_intervals]).astype(float) 

    mask_green = (Y[:, :num_intervals] == 1)
    mask_yellow = (Y[:, :num_intervals] == 0) & (U[:, :num_intervals] == 1)
    mask_red = (Y[:, :num_intervals] == 0) & (U[:, :num_intervals] == 0)

    data_green = data.copy()
    data_yellow = data.copy()
    data_red = data.copy()

    cmap_green = sns.color_palette(["#006400"], as_cmap=True)
    cmap_yellow = sns.color_palette(["#FFD700"], as_cmap=True)
    cmap_red = sns.color_palette(["#8B0000"], as_cmap=True)

    # Apply masks
    data_green[~mask_green] = np.nan
    data_yellow[~mask_yellow] = np.nan
    data_red[~mask_red] = np.nan

    annot = not hide_values_in_table

    sns.heatmap(data_green, annot=annot, fmt=".0f" if annot else "", linewidths=.5, ax=ax, cmap=cmap_green, cbar=False, center=50)
    sns.heatmap(data_yellow, annot=annot, fmt=".0f" if annot else "", linewidths=.5, ax=ax, cmap=cmap_yellow, cbar=False, center=50)
    sns.heatmap(data_red, annot=annot, fmt=".0f" if annot else "", linewidths=.5, ax=ax, cmap=cmap_red, cbar=False, center=50)

    if hide_results_in_header:
        ax.set_title(algorithm_name, fontsize=14, pad=10)
    else:
        ax.set_title(f"{algorithm_name} (Z: {Z}, Avg Usage Per Student: {avg_usage:.2f})", fontsize=14, pad=10)

    if not remove_axis_numbering:
        ax.set_xlabel('Time Interval')
        ax.set_ylabel('Student')
        ax.set_xticks(np.arange(num_intervals) + 0.5)
        ax.set_xticklabels([f'T-{t+1}' for t in range(num_intervals)], rotation=45)
        ax.set_yticks(np.arange(num_students) + 0.5)
        ax.set_yticklabels([f'Std-{i+1}' for i in range(num_students)], rotation=0)
    else:
        ax.set_xticks([])
        ax.set_yticks([])


if __name__ == "__main__":
    main()
