from typing import List
from Entities.student import Student

class OptimizationInstance:
    def __init__(self, students: List[Student], num_sockets: int, total_time: float, delta_t: float) -> None:
        self.students: List[Student] = students
        self.num_sockets: int = num_sockets
        self.total_time: float = total_time
        self.delta_t: float = delta_t

    def __repr__(self) -> str:
        return (f"OptimizationInstance(num_sockets={self.num_sockets}, total_time={self.total_time}, "
                f"delta_t={self.delta_t}, students={self.students})")
