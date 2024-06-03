import gurobipy as gp
from gurobipy import GRB
from typing import List
from Entities.student import Student
from Entities.optimization_instance import OptimizationInstance
from Managers.satisfaction_manager import SatisfactionManager
import math

class ImprovedGurobiOptimization:
    @staticmethod
    def optimize_allocation(optimization_instance: OptimizationInstance) -> List[float]:
        students = optimization_instance.students
        num_students = len(students)
        total_available_time = optimization_instance.num_sockets * optimization_instance.total_time

        try:
            model = gp.Model("improved_allocation_optimization")

            # Add variables for allocated times
            allocated_times = model.addVars(num_students, lb=0, name="allocated_time")

            # Compute out-of-battery times before charging
            total_working_hours = optimization_instance.total_working_hours
            out_of_battery_times_before = [(s.initial_battery / 100.0) * total_working_hours / s.discharge_rate for s in students]

            # Add variables for the time out of service after charging
            time_out_of_service_after = model.addVars(num_students, lb=0, name="toos_after")

            # Set objective: Minimize the sum of time out of service after charging
            model.setObjective(gp.quicksum(time_out_of_service_after[i] for i in range(num_students)), GRB.MINIMIZE)

            # Add constraint: sum of allocated times <= total available time
            model.addConstr(gp.quicksum(allocated_times[i] for i in range(num_students)) <= total_available_time, "time_constraint")

            # Add constraints for time out of service after charging
            for i in range(num_students):
                model.addConstr(time_out_of_service_after[i] >= (1 - (students[i].initial_battery / 100.0) - allocated_times[i] / total_working_hours) * total_working_hours / students[i].discharge_rate, f"toos_constraint_{i}")

            # Optimize the model
            model.optimize()

            # Check if the optimization was successful
            if model.status == GRB.OPTIMAL:
                return [allocated_times[i].X for i in range(num_students)]
            else:
                print(f"Optimization not optimal. Status: {model.status}")
                return [0.0] * num_students

        except gp.GurobiError as e:
            print(f"Gurobi error: {e}")
            return [0.0] * num_students
        except Exception as e:
            print(f"General error: {e}")
            return [0.0] * num_students