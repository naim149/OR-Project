from typing import List, Dict
from Entities.optimization_instance import OptimizationInstance
import time

class OptimizationManager:
    def __init__(self, algorithms):
        self.algorithms = algorithms

    def run_optimization(self, optimization_instance: OptimizationInstance):
        results = []
        for algorithm in self.algorithms:
            print(f"Running {algorithm.name}...")
            start_time = time.time()
            result = algorithm.optimize_allocation(optimization_instance)
            end_time = time.time()
            
            result_data = {
                'algorithm_name': algorithm.name,
                'result': result,
                'total_time': end_time - start_time,
                'model_build_time': result['model_build_time'],
                'optimization_time': result['optimization_time']
            }
            results.append(result_data)
            print("\n")

        # Print all results after running all algorithms
        self.print_results(optimization_instance, results)

    def print_results(self, optimization_instance: OptimizationInstance, results: List[Dict]):
        print("\n")
        print(f"Parameters: N={len(optimization_instance.students)}, Sockets={optimization_instance.num_sockets}, "
              f"T={optimization_instance.total_time}, delta_T={optimization_instance.delta_t}")
        
        for result in results:
            print(f"Algorithm: {result['algorithm_name']}")
            if result['result']['status'] == 'optimal':
                print(f"Minimum Usage Time: {result['result']['min_usage_time']}")
                print(f"Optimality: {result['result']['min_usage_time']/(optimization_instance.total_time/optimization_instance.delta_t)*100}%")
                print("Matrix U (Laptop Usage):")
                for row in result['result']['U']:
                    print(row)
                print("Matrix Y (Socket Usage):")
                for row in result['result']['Y']:
                    print(row)
            else:
                print("No optimal solution found.")
            print(f"Total Time: {result['total_time']} seconds")
            print(f"Model Build Time: {result['model_build_time']} seconds")
            print(f"Optimization Time: {result['optimization_time']} seconds")
            print("\n")
