class Student:
    """Class representing a student with battery and usage parameters."""

    def __init__(self, recharge_rate: float, discharge_rate: float, initial_battery: float) -> None:
        if not (0 <= initial_battery <= 100):
            raise ValueError("Initial battery level must be between 0 and 100.")
        if recharge_rate <= 0 or discharge_rate <= 0 :
            raise ValueError("Rates must be positive.")

        self.recharge_rate: float = recharge_rate
        self.discharge_rate: float = discharge_rate
        self.initial_battery: float = initial_battery
