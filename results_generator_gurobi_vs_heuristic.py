import time
import csv
import random
from datetime import datetime
from Managers.optimizationInstance_manager import OptimizationInstanceManager
from Algorithms.heuristic_algorithm import HeuristicOptimization
from Algorithms.gurobi_algorithm import GurobiOptimization
import numpy as np
import math

def main():
    # Fixed parameters
    T = 16
    delta_T = 0.5
    num_time_slots = math.ceil(T / delta_T)

    ranges = [9]  # Define the range of N values to investigate
    timeout = 5

    for N in ranges:
        results = []
        print(f" Generating for Number of students: {N}")
        for s in range(1, N + 1):
            print(f" Generating for sockets: {s}")
            optimal = True
            heuristic_u_scores = []
            heuristic_optimization_times = []
            heuristic_min_usage_times = []
            gurobi_u_scores = []
            gurobi_optimization_times = []
            gurobi_model_build_times = []
            gurobi_min_usage_times = []

            for seed in range(10):
                print(f" Generating for seed: {seed}")
                manager = OptimizationInstanceManager(seed)
                optimization_instance = manager.create_instance(N, s, T, delta_T,timeout)

                # Heuristic Optimization
                print(f" Started Heuristic")
                heuristic = HeuristicOptimization()
                start_time = time.time()
                heuristic_result = heuristic.optimize_allocation(optimization_instance)
                heuristic_optimization_time = time.time() - start_time

                if heuristic_result['fair_maximized_usage_score'] < 1 + (num_time_slots):
                    optimal = False

                heuristic_u_scores.append(heuristic_result['A'])
                heuristic_optimization_times.append(heuristic_optimization_time)
                heuristic_min_usage_times.append(heuristic_result['min_usage_time'])

                # Gurobi Optimization
                print(f" Started Gurobi")
                gurobi = GurobiOptimization()
                start_time = time.time()
                gurobi_result = gurobi.optimize_allocation(optimization_instance)
                gurobi_optimization_time = time.time() - start_time
                gurobi_model_build_time = gurobi_result.get('model_build_time', 0)

                if gurobi_result['fair_maximized_usage_score'] < 1 + (num_time_slots):
                    optimal = False

                gurobi_u_scores.append(gurobi_result['A'])
                gurobi_optimization_times.append(gurobi_optimization_time)
                gurobi_model_build_times.append(gurobi_model_build_time)
                gurobi_min_usage_times.append(gurobi_result['min_usage_time'])

            for seed in range(10):
                results.append({
                    'N': N,
                    's': s,
                    'heuristic_z': heuristic_min_usage_times[seed],
                    'heuristic_u': heuristic_u_scores[seed],
                    'heuristic_optimization_time': heuristic_optimization_times[seed],
                    'gurobi_z': gurobi_min_usage_times[seed],
                    'gurobi_u': gurobi_u_scores[seed],
                    'gurobi_model_build_time': gurobi_model_build_times[seed],
                    'gurobi_optimization_time': gurobi_optimization_times[seed]
                })

            if optimal:
               print(f" Optimal was found for socket: {s}")
               break

        # Get the current time for the filename
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'Gurobi vs Heuristic Comparison Results\\gurobi_vs_heuristic_N_{N}_{current_time}.csv'

        # Write results to CSV file
        print(f" Starting Data Export")
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Students', 'Sockets', 'Heuristic_Z', 'Heuristic_U', 'Heuristic_Optimization_Time',
                             'Gurobi_Z', 'Gurobi_U', 'Gurobi_model_build_time', 'Gurobi_optimization_time'])
            for result in results:
                writer.writerow([result['N'], result['s'], result['heuristic_z'], result['heuristic_u'],
                                 result['heuristic_optimization_time'], result['gurobi_z'], result['gurobi_u'],
                                 result['gurobi_model_build_time'], result['gurobi_optimization_time']])

if __name__ == "__main__":
    main()
