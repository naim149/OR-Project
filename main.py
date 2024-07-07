from Managers.optimizationInstance_manager import OptimizationInstanceManager
from Managers.optimization_manager import OptimizationManager
from Algorithms.gurobi_algorithm import GurobiOptimization
from Algorithms.heuristic_algorithm import HeuristicOptimization
from Algorithms.gurobi_hybrid import GurobiHybridOptimization

def main():
    #Parameters
    N = 9
    s = 3
    T = 16
    delta_T = 0.5
    seed = 4
    timeout = 10

    algorithms = []
    algorithms.append(HeuristicOptimization())
    algorithms.append(GurobiOptimization())
    # algorithms.append(GurobiHybridOptimization())

    manager = OptimizationInstanceManager(seed)
    optimization_instance = manager.create_instance(N, s, T, delta_T,timeout)

    optimization_manager = OptimizationManager(algorithms)
    optimization_manager.run_optimization(optimization_instance)

if __name__ == "__main__":
    main()