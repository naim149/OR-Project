from typing import List
from concurrent.futures import ThreadPoolExecutor
from Entities.Optimization_Instance import OptimizationInstance
from Entities.optimization_algorithm import OptimizationAlgorithm

class OptimizationManager:
    def __init__(self, algorithms: List[OptimizationAlgorithm]):
        self.algorithms = algorithms

    def optimize(self, optimization_instance: OptimizationInstance):
        results = {}
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(algorithm.optimize_allocation, optimization_instance): algorithm for algorithm in self.algorithms}
            for future in futures:
                algorithm = futures[future]
                try:
                    results[algorithm.__class__.__name__] = future.result()
                except Exception as exc:
                    results[algorithm.__class__.__name__] = f"Algorithm failed with exception: {exc}"

        return results
