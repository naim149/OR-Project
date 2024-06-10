from Algorithms.gurobi_algorithm import ImprovedGurobiOptimization
from Managers.optimizationInstance_manager import OptimizationInstanceManager
import time

def main():
    # Create an instance manager
    manager = OptimizationInstanceManager(seed=42)
    optimization_instance = manager.create_instance()

    # Initialize the optimizer
    optimizer = ImprovedGurobiOptimization()

    # Run the optimization
    result = optimizer.optimize_allocation(optimization_instance)

    print(f"Optimal allocation: {result}")
    print(f"Objective function value: {optimizer.objective_value}")
    print(f"Model build time: {optimizer.model_build_time} seconds")
    print(f"Total execution time: {optimizer.execution_time} seconds")

if __name__ == "__main__":
    main()
