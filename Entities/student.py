from typing import List

class Student:
    def __init__(self, recharge_rate: float, discharge_rate: float, initial_battery: float) -> None:
        self.recharge_rate: float = recharge_rate
        self.discharge_rate: float = discharge_rate
        self.initial_battery: float = initial_battery

    def __repr__(self) -> str:
        return (f"Student(recharge_rate={self.recharge_rate}, discharge_rate={self.discharge_rate}, "
                f"initial_battery={self.initial_battery})")