import time
import csv
import random
from datetime import datetime
from Managers.optimizationInstance_manager import OptimizationInstanceManager
from Managers.optimization_manager import OptimizationManager
from Algorithms.heuristic_algorithm import HeuristicOptimization
from Algorithms.gurobi_algorithm import GurobiOptimization

def main():
    # Fixed parameters
    T = 2
    delta_T = 1
    results = []

    # Define ranges for N and s
    N_range = range(1, 16)
    
    for N in N_range:
        print(f"Testing for N = {N}")
        for s in range(1, N + 1):
            for seed in range(10):
                random.seed(seed)
                manager = OptimizationInstanceManager(seed)
                optimization_instance = manager.create_instance(N, s, T, delta_T)
                
                # Heuristic Optimization
                heuristic = HeuristicOptimization()
                start_time = time.time()
                heuristic_result = heuristic.optimize_allocation(optimization_instance)
                heuristic_optimization_time = time.time() - start_time

                # Gurobi Optimization
                gurobi = GurobiOptimization()
                start_time = time.time()
                gurobi_result = gurobi.optimize_allocation(optimization_instance)
                gurobi_optimization_time = time.time() - start_time
                gurobi_model_build_time = gurobi_result.get('model_build_time', 0)

                results.append({
                    'N': N,
                    's': s,
                    'seed': seed,
                    'heuristic_min_usage_time': heuristic_result['min_usage_time'],
                    'heuristic_optimization_time': heuristic_optimization_time,
                    'gurobi_min_usage_time': gurobi_result['min_usage_time'],
                    'gurobi_optimization_time': gurobi_optimization_time,
                    'gurobi_model_build_time': gurobi_model_build_time
                })

    # Get the current time for the filename
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'comparison_results_{current_time}.csv'

    # Write results to CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['N', 's', 'seed', 'heuristic_min_usage_time', 'heuristic_optimization_time',
                         'gurobi_min_usage_time', 'gurobi_optimization_time', 'gurobi_model_build_time'])
        for result in results:
            writer.writerow([result['N'], result['s'], result['seed'], result['heuristic_min_usage_time'],
                             result['heuristic_optimization_time'], result['gurobi_min_usage_time'],
                             result['gurobi_optimization_time'], result['gurobi_model_build_time']])

if __name__ == "__main__":
    main()
