import gurobipy as gp
from gurobipy import GRB
from typing import List, Dict
from Entities.optimization_instance import OptimizationInstance
import numpy as np
import time
import math

class GurobiOptimization:
    def __init__(self):
        self.name = "Gurobi Optimization"

    def optimize_allocation(self, optimization_instance: OptimizationInstance) -> Dict:
        students = optimization_instance.students
        num_students = len(students)
        total_available_time = optimization_instance.total_time
        delta_t = optimization_instance.delta_t

        r = np.array([s.recharge_rate for s in students]) 
        d = np.array([s.discharge_rate for s in students])
        b0 = np.array([s.initial_battery for s in students])

        num_time_slots = math.ceil(total_available_time / delta_t)

        model_build_start_time = time.time()
        model = gp.Model("laptop_charging")
        model.Params.OutputFlag=0
        model.Params.LogToConsole=0
        Y = model.addVars(num_students, num_time_slots, vtype=GRB.BINARY, name="Y")
        U = model.addVars(num_students, num_time_slots, vtype=GRB.BINARY, name="U")
        Z = model.addVar(vtype=GRB.INTEGER, name='min_battery')
        B = model.addVars(num_students, num_time_slots + 1,lb = 0, ub=100, vtype=GRB.CONTINUOUS, name="B")

        for i in range(num_students):
            model.addConstr(B[i, 0] == b0[i], name=f"init_battery_{i}")

        for i in range(num_students):
            model.addConstr(gp.quicksum(U[i, t] for t in range(num_time_slots)) >= Z, name=f"sum_of_usage_{i}")

        for t in range(num_time_slots):
            for i in range(num_students):
                model.addConstr(B[i, t + 1] == B[i, t] + Y[i, t] * r[i] * delta_t + Y[i, t] * U[i, t] * d[i] * delta_t - U[i, t] * d[i] * delta_t, name=f"battery_dynamics_{i}_{t}")

        for t in range(num_time_slots):
            model.addConstr(gp.quicksum(Y[i, t] for i in range(num_students)) <= optimization_instance.num_sockets, name=f"socket_avail_{t}")

        model.setObjective(Z, GRB.MAXIMIZE)
        model_build_end_time = time.time()

        optimization_start_time = time.time()
        model.optimize()
        optimization_end_time = time.time()

        if model.status == GRB.OPTIMAL:
            U_matrix = [[round(U[i, t].X) for t in range(num_time_slots)] for i in range(num_students)]
            Y_matrix = [[round(Y[i, t].X) for t in range(num_time_slots)] for i in range(num_students)]
            B_matrix = [[round(B[i, t].X) for t in range(num_time_slots + 1)] for i in range(num_students)]

            result = {
                'min_usage_time': Z.X,
                'U': U_matrix,
                'Y': Y_matrix,
                'B': B_matrix,
                'model_build_time': model_build_end_time - model_build_start_time,
                'optimization_time': optimization_end_time - optimization_start_time,
                'status': 'optimal'
            }
            return result
        else:
            result = {
                'min_usage_time': None,
                'U': None,
                'Y': None,
                'B': None,
                'model_build_time': model_build_end_time - model_build_start_time,
                'optimization_time': optimization_end_time - optimization_start_time,
                'status': 'not_optimal'
            }
            return result
