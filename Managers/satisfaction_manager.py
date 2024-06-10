import numpy as np
from typing import List
from Entities.student import Student
from Entities.optimization_instance import OptimizationInstance

class SatisfactionManager:
    @staticmethod
    def calculate_satisfaction(time_out_of_service):
        epsilon = 1e-10
        if time_out_of_service <= epsilon:
            return 0
        return 100 / (1 + np.log(1 + time_out_of_service))
