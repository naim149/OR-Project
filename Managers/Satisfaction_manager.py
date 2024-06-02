import numpy as np
from typing import List
from Entities.Student import Student
from Entities.Optimization_Instance import OptimizationInstance

class SatisfactionManager:
    """Stateless class to manage and calculate student satisfaction."""

    @staticmethod
    def calculate_student_satisfaction(allocated_time: float, student: Student, total_working_hours: float) -> float:
        """Calculate satisfaction for a single student based on allocated time."""
        if allocated_time < 0:
            raise ValueError("Allocated time must be non-negative.")
        
        out_of_battery_time = SatisfactionManager.calculate_out_of_battery_time(student, allocated_time, total_working_hours)
        
        if out_of_battery_time == 0:
            return 100  # Maximum satisfaction if battery never runs out
        
        satisfaction = 100 / (1 + np.log10(1 + out_of_battery_time))
        return satisfaction

    @staticmethod
    def calculate_total_satisfaction(allocated_times: List[float], instance: OptimizationInstance) -> float:
        """Calculate total satisfaction for all students."""
        if len(allocated_times) != len(instance.students):
            raise ValueError("Allocated times list length must match number of students.")

        total_satisfaction: float = 0.0
        for allocated_time, student in zip(allocated_times, instance.students):
            total_satisfaction += SatisfactionManager.calculate_student_satisfaction(allocated_time, student, instance.total_working_hours)
        
        # Normalize the total satisfaction to be between 0 and 100
        max_possible_satisfaction = len(instance.students) * 100
        normalized_satisfaction = (total_satisfaction / max_possible_satisfaction) * 100
        
        return normalized_satisfaction

    @staticmethod
    def calculate_out_of_battery_time(student: Student, allocated_time: float, total_working_hours: float) -> float:
        """Calculate the time in hours until the student's laptop runs out of battery after charging during the total working hours."""
        if student.discharge_rate <= 0:
            return 0  # Always in service if discharge rate is zero or negative

        remaining_time = total_working_hours - allocated_time
        final_battery = student.initial_battery + (student.recharge_rate * allocated_time)
        final_battery = max(0, min(100, final_battery))  # Ensure battery stays within 0 to 100%

        time_to_deplete = final_battery / student.discharge_rate
        out_of_service_time = max(0, remaining_time - time_to_deplete)

        return out_of_service_time
