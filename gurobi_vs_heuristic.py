import time
import csv
import random
from datetime import datetime
from Managers.optimizationInstance_manager import OptimizationInstanceManager
from Managers.optimization_manager import OptimizationManager
from Algorithms.heuristic_algorithm import HeuristicOptimization
from Algorithms.gurobi_algorithm import GurobiOptimization
import numpy as np
import math

def main():
    # Fixed parameters
    T = 16
    delta_T = 0.5
    results = []

    # Define ranges and step sizes
    ranges = [ (150, 201, 50)] #, (150, 201, 50) (1, 16, 1),

    optimal_s = 1  # Start with the minimum possible value of s

    for start, end, step in ranges:
        for N in range(start, end, step):
            print(f"Testing for N = {N}")
            found_optimal_s = False
            for s in range(math.ceil(N/3), N + 1):
                heuristic_min_usage_times = []
                heuristic_optimization_times = []
                gurobi_min_usage_times = []
                gurobi_optimization_times = []
                gurobi_model_build_times = []
                consistent = True

                for seed in range(10):
                    random.seed(seed)
                    manager = OptimizationInstanceManager(seed)
                    optimization_instance = manager.create_instance(N, s, T, delta_T)

                    # Heuristic Optimization
                    heuristic = HeuristicOptimization()
                    start_time = time.time()
                    heuristic_result = heuristic.optimize_allocation(optimization_instance)
                    heuristic_optimization_time = time.time() - start_time

                    if heuristic_result['min_usage_time'] < (T / delta_T):
                        consistent = False
                        break

                    heuristic_min_usage_times.append(heuristic_result['min_usage_time'])
                    heuristic_optimization_times.append(heuristic_optimization_time)

                    # Gurobi Optimization
                    gurobi = GurobiOptimization()
                    start_time = time.time()
                    gurobi_result = gurobi.optimize_allocation(optimization_instance)
                    gurobi_optimization_time = time.time() - start_time
                    gurobi_model_build_time = gurobi_result.get('model_build_time', 0)

                    if gurobi_result['min_usage_time'] < (T / delta_T):
                        consistent = False
                        break

                    gurobi_min_usage_times.append(gurobi_result['min_usage_time'])
                    gurobi_optimization_times.append(gurobi_optimization_time)
                    gurobi_model_build_times.append(gurobi_model_build_time)

                if consistent:
                    optimal_s = s
                    results.append({
                        'N': N,
                        's': optimal_s,
                        'heuristic_min_usage_time': np.mean(heuristic_min_usage_times),
                        'heuristic_optimization_time': np.mean(heuristic_optimization_times),
                        'gurobi_min_usage_time': np.mean(gurobi_min_usage_times),
                        'gurobi_optimization_time': np.mean(gurobi_optimization_times),
                        'gurobi_model_build_time': np.mean(gurobi_model_build_times)
                    })
                    found_optimal_s = True
                    break

            if not found_optimal_s:
                print(f"No optimal s found for N = {N}")

    # Get the current time for the filename
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'comparison_results_{current_time}.csv'

    # Write results to CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['N', 's', 'heuristic_min_usage_time', 'heuristic_optimization_time',
                         'gurobi_min_usage_time', 'gurobi_optimization_time', 'gurobi_model_build_time'])
        for result in results:
            writer.writerow([result['N'], result['s'], result['heuristic_min_usage_time'],
                             result['heuristic_optimization_time'], result['gurobi_min_usage_time'],
                             result['gurobi_optimization_time'], result['gurobi_model_build_time']])

if __name__ == "__main__":
    main()
