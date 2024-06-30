import math
import numpy as np
import time
from typing import List, Dict
from Entities.optimization_instance import OptimizationInstance

class HeuristicOptimization:
    def __init__(self):
        self.name = "Heuristic Optimization"

    def calculate_current_battery_levels(self, B_matrix, r, d, Y_matrix, U_matrix, t, delta_t):
        if t > 0:
            for i in range(len(B_matrix)):
                B_matrix[i, t] = B_matrix[i, t - 1] + Y_matrix[i, t - 1] * r[i] * delta_t + Y_matrix[i, t - 1] * U_matrix[i, t - 1] * d[i] * delta_t - U_matrix[i, t - 1] * d[i] * delta_t

    def forecast_next_battery_levels(self, B_matrix, d, t, delta_t):
        return B_matrix[:, t] - d * delta_t

    def allocate_sockets(self, forecasted_battery_levels, U_matrix, num_sockets, t, r, d):
        sockets_allocated = np.zeros_like(U_matrix[:, t])
        num_students = len(forecasted_battery_levels)
        
        students_needing_sockets = np.where(forecasted_battery_levels < 0)[0]
        
        if len(students_needing_sockets) <= num_sockets:
            sockets_allocated[students_needing_sockets] = 1
        else:
            sorted_students = sorted(students_needing_sockets, key=lambda i: (np.sum(U_matrix[i, :t]), forecasted_battery_levels[i], r[i] - d[i]))
            sockets_allocated[sorted_students[:num_sockets]] = 1

        for i in range(num_students):
            if sockets_allocated[i] == 1:
                U_matrix[i, t] = 1

        return sockets_allocated

    def distribute_remaining_sockets(self, forecasted_battery_levels, Y_matrix, U_matrix, num_remaining_sockets, r, d, t, delta_t):
        students_without_sockets = np.where(Y_matrix[:, t] == 0)[0]

        if num_remaining_sockets > 0:
            sorted_students = sorted(students_without_sockets, key=lambda i: forecasted_battery_levels[i])
            allocated_sockets = min(int(num_remaining_sockets), len(sorted_students))

            for i in sorted_students[:allocated_sockets]:
                if forecasted_battery_levels[i] + r[i] * delta_t + d[i] * delta_t <= 100:
                    Y_matrix[i, t] = 1
                    if U_matrix[i, t] == 0:
                        U_matrix[i, t] = 1

    def optimize_allocation(self, optimization_instance: OptimizationInstance) -> Dict:
        students = optimization_instance.students
        num_students = len(students)
        total_available_time = optimization_instance.total_time
        delta_t = optimization_instance.delta_t
        num_sockets = optimization_instance.num_sockets

        r = np.array([s.recharge_rate for s in students])
        d = np.array([s.discharge_rate for s in students])
        b0 = np.array([s.initial_battery for s in students])

        num_time_slots = math.ceil(total_available_time / delta_t)

        B_matrix = np.zeros((num_students, num_time_slots + 1))
        B_matrix[:, 0] = b0

        Y_matrix = np.zeros((num_students, num_time_slots))
        U_matrix = np.zeros((num_students, num_time_slots))

        start_time = time.time()

        for t in range(num_time_slots):
            self.calculate_current_battery_levels(B_matrix, r, d, Y_matrix, U_matrix, t, delta_t)
            forecasted_battery_levels = self.forecast_next_battery_levels(B_matrix, d, t, delta_t)
            U_matrix[:, t] = (forecasted_battery_levels >= 0).astype(int)
            Y_matrix[:, t] = self.allocate_sockets(forecasted_battery_levels, U_matrix, num_sockets, t, r, d)

            remaining_sockets = num_sockets - np.sum(Y_matrix[:, t])
            if remaining_sockets > 0:
                self.distribute_remaining_sockets(forecasted_battery_levels, Y_matrix, U_matrix, remaining_sockets, r, d, t, delta_t)

        end_time = time.time()
        A = (np.sum(U_matrix) / (num_time_slots * num_students))
        Z = np.min(np.sum(U_matrix, axis=1))
        result = {
            'fair_maximized_usage_score': ( A+ Z),
            'min_usage_time': Z,
            'A': A,
            'U': U_matrix.tolist(),
            'Y': Y_matrix.tolist(),
            'B': B_matrix[:, :-1].tolist(),  # excluding the last time slot for battery levels
            'optimization_time': end_time - start_time,
            'model_build_time': 0,  # No separate model build time for heuristic
            'status': 'optimal'
        }

        return result
