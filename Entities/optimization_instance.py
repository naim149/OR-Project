from typing import List
from Entities.student import Student

class OptimizationInstance:
    def __init__(self, students: List[Student], num_sockets: int, total_time: int):
        self.students = students
        self.num_sockets = num_sockets
        self.total_time = total_time
        
        # Calculate compatible ∆T
        max_rate = max(max(student.recharge_rate for student in students),
                       max(student.discharge_rate for student in students))
        self.delta_t = self.calculate_compatible_delta_t(max_rate, total_time)

    def calculate_compatible_delta_t(self, max_rate: float, total_time: int) -> float:
        delta_t = 1 / max_rate
        ratio = int(total_time / delta_t)
        delta_t = total_time / (ratio + 1)
        return delta_t
