from typing import List
from Entities.Student import Student
from Entities.Optimization_Instance import OptimizationInstance


class SatisfactionManager:
    """Stateless class to manage and calculate student satisfaction."""

    @staticmethod
    def calculate_student_satisfaction(allocated_time: float, student: Student) -> float:
        """Calculate satisfaction for a single student based on allocated time."""
        if allocated_time < 0:
            raise ValueError("Allocated time must be non-negative.")
        # For demonstration, satisfaction is directly proportional to allocated time
        return allocated_time

    @staticmethod
    def calculate_total_satisfaction(allocated_times: List[float], instance: OptimizationInstance) -> float:
        """Calculate total satisfaction for all students."""
        if len(allocated_times) != len(instance.students):
            raise ValueError("Allocated times list length must match number of students.")

        total_satisfaction: float = 0.0
        for allocated_time, student in zip(allocated_times, instance.students):
            total_satisfaction += SatisfactionManager.calculate_student_satisfaction(allocated_time, student)

        return total_satisfaction
