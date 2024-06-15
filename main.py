from Managers.optimizationInstance_manager import OptimizationInstanceManager
from Managers.optimization_manager import OptimizationManager
from Algorithms.gurobi_algorithm import GurobiOptimization
from Algorithms.heuristic_algorithm import HeuristicOptimization

def main():
    manager = OptimizationInstanceManager(1)
    # Assuming N, s, T, and delta_T are given or dynamically decided in the main function
    N = 12
    s = 6
    T = 5
    delta_T = 1

    optimization_instance = manager.create_instance(N, s, T, delta_T)
    algorithms = [GurobiOptimization(),HeuristicOptimization()]
    optimization_manager = OptimizationManager(algorithms)
    optimization_manager.run_optimization(optimization_instance)

if __name__ == "__main__":
    main()
