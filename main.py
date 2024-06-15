from Managers.optimizationInstance_manager import OptimizationInstanceManager
from Managers.optimization_manager import OptimizationManager
from Algorithms.gurobi_algorithm import GurobiOptimization

def main():
    manager = OptimizationInstanceManager(3)
    # Assuming N, s, T, and delta_T are given or dynamically decided in the main function
    N = 5
    s = 2
    T = 5
    delta_T = 0.5

    optimization_instance = manager.create_instance(N, s, T, delta_T)
    algorithms = [GurobiOptimization()]
    optimization_manager = OptimizationManager(algorithms)
    optimization_manager.run_optimization(optimization_instance)

if __name__ == "__main__":
    main()
