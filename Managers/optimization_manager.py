from typing import List
from concurrent.futures import ThreadPoolExecutor
from Entities.optimization_instance import OptimizationInstance

class OptimizationManager:
    def __init__(self, algorithms):
        self.algorithms = algorithms

    def run_optimization(self, optimization_instance):
        for algorithm in self.algorithms:
            print(f"Running {algorithm.name}...")
            result = algorithm.optimize_allocation(optimization_instance)
            print(f"Result from {algorithm.name}: {result}")
            print("\n")
