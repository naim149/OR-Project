import gurobipy as gp
from gurobipy import GRB
from typing import List
from Entities.optimization_instance import OptimizationInstance
import numpy as np

class ImprovedGurobiOptimization:
    def __init__(self):
        self.name = "ImprovedGurobiOptimization"

    def optimize_allocation(self, optimization_instance: OptimizationInstance) -> List[float]:
        students = optimization_instance.students
        num_students = len(students)
        total_available_time = optimization_instance.num_sockets * optimization_instance.total_time
        total_working_hours = optimization_instance.total_working_hours
        epsilon = 1e-10  # Small value to prevent invalid log inputs

        try:
            model = gp.Model("allocation_optimization")

            allocated_times = model.addVars(num_students, lb=0, ub=total_available_time, name="allocated_time")

            # Build the objective function using piecewise linear approximation for the log function
            for i, s in enumerate(students):
                y_pts = []
                initial_outOfServiceTime = (s.initial_battery / 100.0) * total_available_time / s.discharge_rate
                x_pts = np.linspace(0, initial_outOfServiceTime, 101)  # 101 points for piecewise linear approximation
                for x in x_pts:
                    remaining_battery_time = (s.initial_battery / 100.0) * total_available_time / s.discharge_rate - x
                    time_out_of_service = max(0, total_working_hours - remaining_battery_time)
                    if time_out_of_service <= epsilon:
                        y = 0  # If the value is too small or invalid, set satisfaction to zero
                    else:
                        y = 100 / (1 + np.log(1 + time_out_of_service))
                    y_pts.append(y)
                model.setPWLObj(allocated_times[i], x_pts.tolist(), y_pts)

            # Add constraints
            model.addConstr(allocated_times.sum() <= total_available_time, "total_time_constraint")

            # Optimize
            model.optimize()

            if model.status == GRB.OPTIMAL:
                allocated_times_values = [t.X for t in allocated_times.values()]
                return allocated_times_values
            else:
                print(f"Optimization not optimal. Status: {model.status}")
                return [0.0] * num_students

        except gp.GurobiError as e:
            print(f"Gurobi error: {e}")
            return [0.0] * num_students
        except AttributeError as e:
            print(f"Attribute error: {e}")
            return [0.0] * num_students
