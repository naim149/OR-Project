from typing import List
import random
import numpy as np
from Entities.student import Student
from Entities.optimization_instance import OptimizationInstance

class OptimizationInstanceManager:
    """Manager class to create instances of the optimization problem."""

    def __init__(self, seed: int = None) -> None:
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

    @staticmethod
    def create_instance(N: int, s: int, T: int, delta_T: float) -> OptimizationInstance:
        """Create and return an instance of the optimization problem."""
        # Ensure number of sockets is significantly less than number of students
        assert s <= N, "Number of sockets should be less than the number of students"
        
        # Define the averages
        recharge_rate_avg = 33.33  # Percentage per hour
        discharge_rate_avg = 20.0  # Percentage per hour

        # Define the standard deviations for some variance
        recharge_rate_std = 5.0
        discharge_rate_std = 5.0

        # Generate rates using normal distribution
        recharge_rates = np.random.normal(recharge_rate_avg, recharge_rate_std, N)
        discharge_rates = np.random.normal(discharge_rate_avg, discharge_rate_std, N)

        # Ensure all values are within 0-100%
        recharge_rates = np.clip(recharge_rates, 10, 50)
        discharge_rates = np.clip(discharge_rates, 10, 30)

         # Initial battery levels in percentage
        initial_battery_levels = np.random.uniform(20, 80, N)  # initial battery levels in percentage

        students = [
            Student(recharge_rate, discharge_rate, initial_battery)
            for recharge_rate, discharge_rate, initial_battery in zip(recharge_rates, discharge_rates, initial_battery_levels)
        ]

        return OptimizationInstance(students, s, T, delta_T)

