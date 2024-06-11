from typing import List
import random
from Entities.student import Student
from Entities.optimization_instance import OptimizationInstance

class OptimizationInstanceManager:
    """Manager class to create instances of the optimization problem."""

    def __init__(self, seed: int = None) -> None:
        if seed is not None:
            random.seed(seed)

    @staticmethod
    def create_instance() -> OptimizationInstance:
        """Create and return an instance of the optimization problem."""
        # Number of students
        N: int = random.randint(2, 25)

        # Number of sockets, significantly less than N
        s: int = random.randint(1, N // 4)

        # Total available time for socket usage (e.g., operational hours in a day)
        total_time: int = 12

        # Generate students with their respective rates and battery levels
        students: List[Student] = [
            Student(
                recharge_rate=random.uniform(25, 50),
                discharge_rate=random.uniform(20, 35),
                initial_battery=random.uniform(10, 80),
            ) for _ in range(N)
        ]

        return OptimizationInstance(students, s, total_time)
