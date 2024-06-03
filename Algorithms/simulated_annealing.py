import numpy as np
from typing import List
from Entities.optimization_instance import OptimizationInstance
from Managers.satisfaction_manager import SatisfactionManager
from Entities.optimization_algorithm import OptimizationAlgorithm

class SimulatedAnnealing(OptimizationAlgorithm):
    def __init__(self, max_iterations=1000, initial_temp=100, cooling_rate=0.003):
        self.max_iterations = max_iterations
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate

    @staticmethod
    def objective_function(allocated_times: np.array, optimization_instance: OptimizationInstance) -> float:
        allocated_times = np.maximum(allocated_times, 0)
        satisfaction = SatisfactionManager.calculate_total_satisfaction(allocated_times.tolist(), optimization_instance)
        return -satisfaction

    def optimize_allocation(self, optimization_instance: OptimizationInstance) -> List[float]:
        students = optimization_instance.students
        num_students = len(students)
        total_available_time = optimization_instance.num_sockets * optimization_instance.total_time

        total_weights = sum(student.discharge_rate / (student.recharge_rate * (100 - student.initial_battery)) for student in students)
        initial_guess = np.array([total_available_time * (student.discharge_rate / (student.recharge_rate * (100 - student.initial_battery))) / total_weights for student in students])

        current_solution = np.copy(initial_guess)
        best_solution = np.copy(initial_guess)
        current_temp = self.initial_temp
        best_satisfaction = -SimulatedAnnealing.objective_function(current_solution, optimization_instance)

        for i in range(self.max_iterations):
            new_solution = np.copy(current_solution)
            perturbation = np.random.normal(0, 0.1, len(new_solution))
            new_solution += perturbation

            new_solution = np.maximum(new_solution, 0)
            if np.sum(new_solution) > total_available_time:
                new_solution *= total_available_time / np.sum(new_solution)

            current_satisfaction = -SimulatedAnnealing.objective_function(current_solution, optimization_instance)
            new_satisfaction = -SimulatedAnnealing.objective_function(new_solution, optimization_instance)

            if new_satisfaction > current_satisfaction or np.random.rand() < np.exp((new_satisfaction - current_satisfaction) / current_temp):
                current_solution = new_solution

            if new_satisfaction > best_satisfaction:
                best_satisfaction = new_satisfaction
                best_solution = new_solution

            current_temp *= (1 - self.cooling_rate)

        return np.maximum(best_solution, 0).tolist()
