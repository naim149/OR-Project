import gurobipy as gp
from gurobipy import GRB
from typing import List, Dict, Optional
from Entities.optimization_instance import OptimizationInstance
import numpy as np
import time
import math

class GurobiOptimization:
    def __init__(self):
        self.name = "Gurobi Optimization"

    def optimize_allocation(self, optimization_instance: OptimizationInstance, initial_guesses: Optional[Dict[str, np.ndarray]] = None) -> Dict:
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
        # Set the acceptable optimality gap (e.g., 0.0001 for 99.99% optimality)
        # model.setParam('MIPGap', 0.001)

        if optimization_instance.time_limit > 0:
            model.setParam('TimeLimit', optimization_instance.time_limit)

        model.Params.OutputFlag = 0
        model.Params.LogToConsole = 0
        Y = model.addVars(num_students, num_time_slots, vtype=GRB.BINARY, name="Y")
        U = model.addVars(num_students, num_time_slots, vtype=GRB.BINARY, name="U")
        Z = model.addVar(vtype=GRB.INTEGER, name='min_usage_time')
        B = model.addVars(num_students, num_time_slots + 1, lb=0, ub=100, vtype=GRB.CONTINUOUS, name="B")
        A = model.addVar(vtype=GRB.CONTINUOUS, name='average_usage_time')

        if initial_guesses:
            for i in range(num_students):
                for t in range(num_time_slots):
                    Y[i, t].start = initial_guesses['Y'][i, t]
                    U[i, t].start = initial_guesses['U'][i, t]
                for t in range(num_time_slots + 1):
                    if t < initial_guesses['B'].shape[1]:
                        B[i, t].start = initial_guesses['B'][i, t]

        for i in range(num_students):
            model.addConstr(B[i, 0] == b0[i], name=f"init_battery_{i}")

        for i in range(num_students):
            model.addConstr(gp.quicksum(U[i, t] for t in range(num_time_slots)) >= Z, name=f"sum_of_usage_{i}")

        for t in range(num_time_slots):
            for i in range(num_students):
                model.addConstr(B[i, t + 1] == B[i, t] + Y[i, t] * r[i] * delta_t + Y[i, t] * U[i, t] * d[i] * delta_t - U[i, t] * d[i] * delta_t, name=f"battery_dynamics_{i}_{t}")

        for t in range(num_time_slots):
            model.addConstr(gp.quicksum(Y[i, t] for i in range(num_students)) <= optimization_instance.num_sockets, name=f"socket_avail_{t}")

        model.addConstr(gp.quicksum((U[i, t] / (num_students * num_time_slots)) for t in range(num_time_slots) for i in range(num_students)) == A, name=f"average_usage")

        for t in range(num_time_slots):
            for i in range(num_students):
                model.addConstr(U[i, t] >= Y[i, t])

        model.setObjective(Z+A , GRB.MAXIMIZE)
        model_build_end_time = time.time()

        optimization_start_time = time.time()
        model.optimize()
        optimization_end_time = time.time()

        if model.status == GRB.TIME_LIMIT or model.status == GRB.OPTIMAL:
            U_matrix = [[round(U[i, t].X) for t in range(num_time_slots)] for i in range(num_students)]
            Y_matrix = [[round(Y[i, t].X) for t in range(num_time_slots)] for i in range(num_students)]
            B_matrix = [[round(B[i, t].X) for t in range(num_time_slots + 1)] for i in range(num_students)]

            result = {
                'fair_maximized_usage_score': Z.X + A.X,
                'min_usage_time': Z.X,
                'A': A.X,
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
                'fair_maximized_usage_score': None,
                'U': None,
                'Y': None,
                'B': None,
                'model_build_time': model_build_end_time - model_build_start_time,
                'optimization_time': optimization_end_time - optimization_start_time,
                'status': 'not_optimal'
            }
            return result
