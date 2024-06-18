from typing import Dict, List
from Entities.optimization_instance import OptimizationInstance
from tabulate import tabulate

class OptimizationManager:
    def __init__(self, algorithms):
        self.algorithms = algorithms

    def run_optimization(self, optimization_instance: OptimizationInstance):
        results = []
        for algorithm in self.algorithms:
            print(f"Running {algorithm.name}...")
            result = algorithm.optimize_allocation(optimization_instance)
            results.append((algorithm.name, result))
            print("\n")
        self.print_results(results, optimization_instance)
        return results

    def print_results(self, results, optimization_instance: OptimizationInstance):
        self.print_parameters(optimization_instance)
        for name, result in results:
            self.print_algorithm_results(name, result,optimization_instance)

    def print_parameters(self, optimization_instance: OptimizationInstance):
        print(f"Number of students: {len(optimization_instance.students)}")
        print(f"Number of sockets: {optimization_instance.num_sockets}")
        print(f"Total time (T): {optimization_instance.total_time}")
        print(f"Delta time (ΔT): {optimization_instance.delta_t}")
        print("\n")

    def print_algorithm_results(self, name: str, result: Dict,optimization_instance: OptimizationInstance):
        print(f"Algorithm: {name}")
        if result['status'] == 'optimal':
            print(f"Minimum Usage Time: {result['min_usage_time']}")
            print(f"Percentage {result['min_usage_time']*optimization_instance.delta_t*100/optimization_instance.total_time}%")
            print(f"Optimization Time: {result['optimization_time']} seconds")
            print(f"Model Build Time: {result['model_build_time']} seconds")
            # self.print_matrix(result)
        else:
            print("The algorithm did not find an optimal solution.")
        print("\n")

    def print_matrix(self, result: Dict):
        num_time_slots = len(result['U'][0])
        headers = []
        for t in range(1, num_time_slots + 1):
            headers.extend([f"Bat {t}", f"Y {t}", f"U {t}"])

        table = []
        for i in range(len(result['U'])):
            row = []
            for t in range(num_time_slots):
                row.extend([round(result['B'][i][t]), result['Y'][i][t], result['U'][i][t]])
            table.append(row)

        print(tabulate(table, headers=headers, tablefmt="grid"))
