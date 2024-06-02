# Entities/optimization_algorithm.py
from abc import ABC, abstractmethod
from typing import List
from Entities.Optimization_Instance import OptimizationInstance

class OptimizationAlgorithm(ABC):
    @abstractmethod
    def optimize_allocation(self, optimization_instance: OptimizationInstance) -> List[float]:
        pass
