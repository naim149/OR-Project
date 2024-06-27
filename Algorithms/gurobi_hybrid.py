import numpy as np
from typing import Dict
from Entities.optimization_instance import OptimizationInstance
from Algorithms.heuristic_algorithm import HeuristicOptimization
from Algorithms.gurobi_algorithm import GurobiOptimization

class GurobiHybridOptimization:
    def __init__(self):
        self.name = "Gurobi Hybrid Optimization"

    def optimize_allocation(self, optimization_instance: OptimizationInstance) -> Dict:
        # Step 1: Run the heuristic algorithm
        heuristic_optimizer = HeuristicOptimization()
        heuristic_result = heuristic_optimizer.optimize_allocation(optimization_instance)

        # Step 2: Extract initial guesses from the heuristic results
        initial_guesses = {
            'U': np.array(heuristic_result['U']),
            'Y': np.array(heuristic_result['Y']),
            'B': np.array(heuristic_result['B'])
        }

        # Step 3: Run the Gurobi algorithm with initial guesses
        gurobi_optimizer = GurobiOptimization()
        gurobi_result = gurobi_optimizer.optimize_allocation(optimization_instance, initial_guesses)

        return gurobi_result
