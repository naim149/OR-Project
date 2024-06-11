import gurobipy as gp
from gurobipy import GRB
from typing import List
from Entities.optimization_instance import OptimizationInstance
import numpy as np
import time

class ImprovedGurobiOptimization:
    def __init__(self):
        self.name = "ImprovedGurobiOptimization"
        self.objective_value = None
        self.execution_time = None
        self.model_build_time = None

    def optimize_allocation(self, optimization_instance: OptimizationInstance) -> List[float]:
        # Start measuring the total execution time
        total_execution_start_time = time.time()

        students = optimization_instance.students
        num_students = len(students)
        num_sockets = optimization_instance.num_sockets
        total_time = optimization_instance.total_time
        delta_t = optimization_instance.delta_t

        # Initialize the model
        model = gp.Model("laptop_charging")

        # Calculate number of time slots
        num_time_slots = int(total_time / delta_t)

        # Decision variables
        Y = model.addVars(num_students, num_time_slots, vtype=GRB.BINARY, name="Y")
        O = model.addVars(num_students, num_time_slots, vtype=GRB.BINARY, name="O")
        B = model.addVars(num_students, num_time_slots + 1, vtype=GRB.CONTINUOUS, name="B")
        Z = model.addVars(num_students, name="Z")

        # Initial battery levels
        for i, student in enumerate(students):
            model.addConstr(B[i, 0] == student.initial_battery)

        # Battery dynamics and operational status
        for t in range(num_time_slots):
            for i, student in enumerate(students):
                model.addConstr(B[i, t + 1] == B[i, t] + Y[i, t] * student.recharge_rate * delta_t - (1 - Y[i, t]) * student.discharge_rate * delta_t)
                model.addConstr(O[i, t] <= B[i, t] + Y[i, t])
                model.addConstr(O[i, t] <= 1)

        # Socket availability constraint
        for t in range(num_time_slots):
            model.addConstr(gp.quicksum(Y[i, t] for i in range(num_students)) <= num_sockets)

        # Time allocation constraint
        for i in range(num_students):
            model.addConstr(gp.quicksum(Y[i, t] for t in range(num_time_slots)) <= 1)

        # Compute Z_i for each student
        for i in range(num_students):
            model.addConstr(Z[i] == gp.quicksum(O[i, t] * delta_t for t in range(num_time_slots)) / total_time)

        # Compute sum of Z_i and sum of Z_i squared
        sum_Z = gp.quicksum(Z[i] for i in range(num_students))
        sum_Z_sq = gp.quicksum(Z[i] * Z[i] for i in range(num_students))

        # Set the objective to maximize the variance
        model.setObjective(sum_Z_sq - (sum_Z * sum_Z / num_students), GRB.MAXIMIZE)

        # Measure the model build time
        model_build_start_time = time.time()
        model.optimize()
        model_build_end_time = time.time()

        self.model_build_time = model_build_end_time - model_build_start_time

        # Measure the total execution time
        total_execution_end_time = time.time()
        self.execution_time = total_execution_end_time - total_execution_start_time

        if model.status == GRB.OPTIMAL:
            self.objective_value = model.ObjVal
            allocated_times_values = [Z[i].X for i in range(num_students)]
            return allocated_times_values
        else:
            print(f"Optimization not optimal. Status: {model.status}")
            return [0.0] * num_students
