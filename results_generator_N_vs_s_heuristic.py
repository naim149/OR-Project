import time
import csv
import random
import numpy as np
from datetime import datetime
from Managers.optimizationInstance_manager import OptimizationInstanceManager
from Managers.optimization_manager import OptimizationManager
from Algorithms.heuristic_algorithm import HeuristicOptimization

def main():
    # Fixed parameters
    T = 16
    delta_T = 0.5
    results = []
    algorithms = [HeuristicOptimization()]

    # Define ranges and step sizes
    ranges = [(1, 101, 1),(100, 1001, 10), (1000, 10001, 100)]
    
    optimal_s = 1  # Start with the minimum possible value of s

    for start, end, step in ranges:
        for N in range(start, end, step):
            print(f"Testing for N = {N}")
            found_optimal_s = False
            for s in range(optimal_s, N + 1):
                consistent = True
                execution_times = []
                for seed in range(10):
                    random.seed(seed)
                    manager = OptimizationInstanceManager(seed)
                    optimization_instance = manager.create_instance(N, s, T, delta_T)
                    optimization_manager = OptimizationManager(algorithms)
                    
                    start_time = time.time()
                    optimizationResults = optimization_manager.run_optimization(optimization_instance)
                    end_time = time.time()
                    
                    result = optimizationResults[0][1]
                    if result['fair_maximized_usage_score'] < 1+ (T / delta_T):
                        consistent = False
                        break
                    execution_times.append(end_time - start_time)
                
                if consistent:
                    optimal_s = s
                    average_execution_time = np.mean(execution_times)
                    results.append({
                        'N': N,
                        's': optimal_s,
                        'average_execution_time': average_execution_time,
                        'execution_times': execution_times
                    })
                    found_optimal_s = True
                    break
            
            if not found_optimal_s:
                print(f"No optimal s found for N = {N}")

    # Write results to CSV file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'N vs s Results\\results_{timestamp}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['N', 's', 'Average Execution Times', 'Execution Times'])
        for result in results:
            writer.writerow([result['N'], result['s'], result['average_execution_time'], *result['execution_times']])

if __name__ == "__main__":
    main()
