from typing import List
import random
from Entities.Student import Student
from Entities.Optimization_Instance import OptimizationInstance



class OptimizationInstanceManager:
    """Manager class to create instances of the optimization problem."""

    def __init__(self, seed: int = None) -> None:
        if seed is not None:
            random.seed(seed)

    @staticmethod
    def create_instance() -> OptimizationInstance:
        """Create and return an instance of the optimization problem."""
        # Number of students
        N: int = random.randint(10, 30)

        # Number of sockets, significantly less than N
        s: int = random.randint(1, N // 2)

        # Total available time for socket usage (e.g., operational hours in a day)
        T: float = random.uniform(5, 10)

        # Generate students with their respective rates and battery levels
        students: List[Student] = [
            Student(
                recharge_rate=random.uniform(5, 20),
                discharge_rate=random.uniform(1, 5),
                initial_battery=random.uniform(10, 80),
            ) for _ in range(N)
        ]

        return OptimizationInstance(students, s, T)
