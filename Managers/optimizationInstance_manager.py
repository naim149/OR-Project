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
    def create_instance(N: int, s: int, T: int, delta_t: float) -> OptimizationInstance:
        """Create and return an instance of the optimization problem."""
        # Ensure number of sockets is significantly less than number of students
        assert s <= N, "Number of sockets should be less than the number of students"
        
        # # Generate random data for each student's battery capacity, recharge, and discharge rates
        # battery_capacity_mean, battery_capacity_std = 60, 10
        # battery_capacities = np.random.normal(battery_capacity_mean, battery_capacity_std, N)

        # r_watts_mean, r_watts_std = 40, 5  #37.5, 5
        # r_watts = np.random.normal(r_watts_mean, r_watts_std, N)

        # d_watts_mean, d_watts_std = 30, 5 #10, 2
        # d_watts = np.random.normal(d_watts_mean, d_watts_std, N)

        # # Conversion to battery percentage per hour based on individual battery capacities
        # r = (r_watts / battery_capacities) * 100 * delta_t
        # d = (d_watts / battery_capacities) * 100 * delta_t

        # # Initial battery levels in percentage
        # b0 = np.random.uniform(5, 100, N)

        # # # Ensure values are within acceptable ranges
        # # r_min, r_max = (30 / battery_capacity_mean) * 100, (45 / battery_capacity_mean) * 100
        # # d_min, d_max = (5 / battery_capacity_mean) * 100, (15 / battery_capacity_mean) * 100

        # r = np.clip(r, 2, 100)
        # d = np.clip(d, 2, 100)

        r = np.random.randint(10, 20, N)  # Recharge rates
        d = np.random.randint(5, 10, N)  # Discharge rates
        b0 = np.random.uniform(5, 10, N)  # Initial battery levels
        # Generate students with their respective rates and battery levels
        students: List[Student] = [
            Student(recharge_rate=r[i], discharge_rate=d[i], initial_battery=b0[i])
            for i in range(N)
        ]

        return OptimizationInstance(students, s, T, delta_t)

