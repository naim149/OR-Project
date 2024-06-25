import time
import csv
import random
import numpy as np
from datetime import datetime
from Managers.optimizationInstance_manager import OptimizationInstanceManager
from Managers.optimization_manager import OptimizationManager
from Algorithms.heuristic_algorithm import HeuristicOptimization
from Algorithms.gurobi_algorithm import GurobiOptimization  # Assuming GurobiOptimization is implemented similarly

def initialize_instance(seed, N, s, T, delta_T):
    random.seed(seed)
    manager = OptimizationInstanceManager(seed)
    optimization_instance = manager.create_instance(N, s, T, delta_T)
    return optimization_instance

def run_optimization(optimization_instance, algorithm):
    optimization_manager = OptimizationManager([algorithm])
    optimizationResults = optimization_manager.run_optimization(optimization_instance)
    return optimizationResults[0][1]  # Extracting the result of the first (and only) algorithm

def write_results_to_csv(algorithm_name, B, U, Y, T, delta_T, N, s, filename):
    num_intervals = int(T / delta_T)
    header = []
    for i in range(N):
        header.extend([f'Student {i+1} B', f'Student {i+1} U', f'Student {i+1} Y'])

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for t in range(num_intervals):
            row = []
            for i in range(N):
                row.extend([B[i, t], U[i, t], Y[i, t]])
            writer.writerow(row)

def main():
    # Fixed parameters
    seed = 0
    N = 4
    s = 1
    T = 8
    delta_T = 0.5

    algorithms = [
        HeuristicOptimization(),
        # GurobiOptimization()
    ]

    optimization_instance = initialize_instance(seed, N, s, T, delta_T)

    for algorithm in algorithms:
        algorithm_name = algorithm.name
        result = run_optimization(optimization_instance, algorithm)

        B = np.array(result['B'])
        U = np.array(result['U'])
        Y = np.array(result['Y'])

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{algorithm_name}_N{N}_s{s}_T{T}_deltaT{delta_T}_{timestamp}.csv"
        write_results_to_csv(algorithm_name, B, U, Y, T, delta_T, N, s, filename)

if __name__ == "__main__":
    main()
