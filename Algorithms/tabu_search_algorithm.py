# Algorithms/tabu_search_algorithm.py
import numpy as np
from typing import List, Tuple
from Entities.Optimization_Instance import OptimizationInstance
from Managers.Satisfaction_manager import SatisfactionManager
from Entities.optimization_algorithm import OptimizationAlgorithm

class TabuSearch(OptimizationAlgorithm):
    def __init__(self, max_iterations: int, tabu_tenure: int):
        self.max_iterations = max_iterations
        self.tabu_tenure = tabu_tenure

    @staticmethod
    def objective_function(allocated_times: np.array, optimization_instance: OptimizationInstance) -> float:
        """Objective function to minimize the negative of total satisfaction."""
        allocated_times = np.maximum(allocated_times, 0)  # Ensure no negative values due to numerical issues
        satisfaction = SatisfactionManager.calculate_total_satisfaction(allocated_times.tolist(), optimization_instance)
        return -satisfaction

    def generate_neighbor(self, current_solution: np.array) -> np.array:
        """Generate a neighbor solution by slightly adjusting the current solution."""
        neighbor = current_solution.copy()
        idx = np.random.randint(0, len(current_solution))
        change = np.random.uniform(-0.1, 0.1)  # Adjust this range as needed
        neighbor[idx] = max(0, neighbor[idx] + change)
        return neighbor

    def optimize_allocation(self, optimization_instance: OptimizationInstance) -> List[float]:
        students = optimization_instance.students
        num_students = len(students)
        total_available_time = optimization_instance.num_sockets * optimization_instance.total_time

        # Initial solution (equal distribution)
        current_solution = np.array([total_available_time / num_students] * num_students)
        best_solution = current_solution.copy()
        best_satisfaction = -self.objective_function(current_solution, optimization_instance)

        tabu_list = np.zeros((num_students, self.tabu_tenure))

        for iteration in range(self.max_iterations):
            neighbors = [self.generate_neighbor(current_solution) for _ in range(10)]  # Generate multiple neighbors
            neighbors = [neighbor for neighbor in neighbors if sum(neighbor) <= total_available_time]  # Feasible neighbors
            neighbors_satisfaction = [-self.objective_function(neighbor, optimization_instance) for neighbor in neighbors]

            best_neighbor_idx = np.argmax(neighbors_satisfaction)
            best_neighbor = neighbors[best_neighbor_idx]
            best_neighbor_satisfaction = neighbors_satisfaction[best_neighbor_idx]

            if best_neighbor_satisfaction > best_satisfaction:
                best_solution = best_neighbor
                best_satisfaction = best_neighbor_satisfaction

            # Update tabu list
            for i in range(num_students):
                tabu_list[i] = np.roll(tabu_list[i], 1)
                tabu_list[i][0] = current_solution[i]

            current_solution = best_neighbor

        return np.maximum(best_solution, 0).tolist()  # Ensure no negative values due to numerical issues
