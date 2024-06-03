from typing import List
from Entities.student import Student

class OptimizationInstance:
    """Class representing an instance of the optimization problem."""

    def __init__(self, students: List[Student], num_sockets: int, total_time: float, total_working_hours: float) -> None:
        if num_sockets <= 0:
            raise ValueError("Number of sockets must be positive.")
        if total_time <= 0:
            raise ValueError("Total available time must be positive.")
        if not (12 <= total_working_hours <= 18):
            raise ValueError("Total working hours must be between 12 and 18.")

        self.students: List[Student] = students
        self.num_sockets: int = num_sockets
        self.total_time: float = total_time
        self.total_working_hours: float = total_working_hours
