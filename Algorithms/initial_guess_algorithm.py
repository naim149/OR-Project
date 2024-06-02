import numpy as np
from scipy.optimize import minimize
from typing import List
from Entities.Optimization_Instance import OptimizationInstance
from Managers.Satisfaction_manager import SatisfactionManager
from Entities.optimization_algorithm import OptimizationAlgorithm

class ImprovedInitialGuessAlgorithm(OptimizationAlgorithm):
    @staticmethod
    def objective_function(allocated_times: np.array, optimization_instance: OptimizationInstance) -> float:
        """Objective function to minimize the negative of total satisfaction."""
        allocated_times = np.maximum(allocated_times, 0)  # Ensure no negative values due to numerical issues
        satisfaction = SatisfactionManager.calculate_total_satisfaction(allocated_times.tolist(), optimization_instance)
        return -satisfaction

    def optimize_allocation(self, optimization_instance: OptimizationInstance) -> List[float]:
        """Optimize the allocation of charging time to maximize total satisfaction."""
        students = optimization_instance.students
        num_students = len(students)
        total_available_time = optimization_instance.num_sockets * optimization_instance.total_time

        # Improved initial guess based on specific rule:
        # Proportional to discharging rate, inversely proportional to charging time, and inversely proportional to initial battery
        total_weights = sum(student.discharge_rate / (student.recharge_rate * (100 - student.initial_battery)) for student in students)
        initial_guess_1 = np.array([total_available_time * (student.discharge_rate / (student.recharge_rate * (100 - student.initial_battery))) / total_weights for student in students])

        # Alternate initial guess (e.g., equal distribution)
        initial_guess_2 = np.array([total_available_time / num_students] * num_students)

        initial_guesses = [initial_guess_1, initial_guess_2]

        best_result = None
        best_satisfaction = -np.inf

        for initial_guess in initial_guesses:
            # Constraints: sum of allocated times <= total_available_time and allocated times >= 0
            constraints = [
                {'type': 'eq', 'fun': lambda x: np.sum(x) - total_available_time},  # Total time constraint
                {'type': 'ineq', 'fun': lambda x: x}  # Non-negative allocation
            ]

            # Optimize
            result = minimize(
                ImprovedInitialGuessAlgorithm.objective_function,
                initial_guess,
                args=(optimization_instance,),
                constraints=constraints,
                method='SLSQP'
            )

            if result.success and -result.fun > best_satisfaction:
                best_satisfaction = -result.fun
                best_result = result

        if best_result is None:
            raise ValueError("Optimization failed: No successful optimization result found.")

        return np.maximum(best_result.x, 0).tolist()  # Ensure no negative values due to numerical issues
