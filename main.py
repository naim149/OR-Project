from Managers.optimizationInstance_manager import OptimizationInstanceManager
from Managers.optimization_manager import OptimizationManager
from Algorithms.gurobi_algorithm import GurobiOptimization
from Algorithms.heuristic_algorithm import HeuristicOptimization
from Algorithms.gurobi_algorithm_v2 import GurobiOptimizationV2
from Algorithms.gurobi_hybrid import GurobiHybridOptimization
from Algorithms.gurobi_iterative import GurobiIterativeOptimization

def main():
    manager = OptimizationInstanceManager(1)
    # Assuming N, s, T, and delta_T are given or dynamically decided in the main function
    N = 6
    s = 2
    T = 4
    delta_T = 0.5

    optimization_instance = manager.create_instance(N, s, T, delta_T)
    algorithms = []
    algorithms.append(GurobiOptimization())
    algorithms.append(GurobiIterativeOptimization())
    # algorithms.append(GurobiHybridOptimization())

    optimization_manager = OptimizationManager(algorithms)
    optimization_manager.run_optimization(optimization_instance)

if __name__ == "__main__":
    main()
33333