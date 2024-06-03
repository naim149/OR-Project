import gurobipy as gp
from gurobipy import GRB
from typing import List
from Entities.optimization_instance import OptimizationInstance
import numpy as np
import math

class GurobiAlgorithmNotWorking:
    def __init__(self):
        self.name = "GurobiAlgorithmNotWorking"

    def optimize_allocation(self, optimization_instance: OptimizationInstance) -> List[float]:
        students = optimization_instance.students
        num_students = len(students)
        total_available_time = optimization_instance.num_sockets * optimization_instance.total_time
        total_working_hours = optimization_instance.total_working_hours

        try:
            model = gp.Model("allocation_optimization")

            allocated_times = model.addVars(num_students, lb=0, ub=total_available_time, name="allocated_time")

            # Build the objective function using Gurobi functions

            expression = (100 / (1 + math.log(1 + (s.initial_battery / 100.0) * total_available_time / s.discharge_rate - allocated_times[i])) for i, s in enumerate(students))

            obj_expr = gp.quicksum(
                expression
            )
            model.setObjective(obj_expr, gp.GRB.MAXIMIZE)

            # Add constraints
            model.addConstr(allocated_times.sum() <= total_available_time, "total_time_constraint")

            model.optimize()

            if model.status == GRB.OPTIMAL:
                return [t.X for t in allocated_times.values()] 
            else:
                print(f"Optimization not optimal. Status: {model.status}")
                return [0.0] * num_students

        except gp.GurobiError as e:
            print(f"Gurobi error: {e}")
            return [0.0] * num_students
        except AttributeError as e:
            print(f"Attribute error: {e}")
            return [0.0] * num_students
