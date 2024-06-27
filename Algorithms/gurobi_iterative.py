import gurobipy as gp
from gurobipy import GRB
from typing import List, Dict
from Entities.optimization_instance import OptimizationInstance
from Algorithms.gurobi_algorithm import GurobiOptimization
import numpy as np
import time
import math

class GurobiIterativeOptimization:
    def __init__(self):
        self.name = "Gurobi Iterative Optimization"

    def optimize_allocation(self, optimization_instance: OptimizationInstance) -> Dict:
        students = optimization_instance.students
        num_students = len(students)
        total_available_time = optimization_instance.total_time
        delta_t = optimization_instance.delta_t
        num_sockets = optimization_instance.num_sockets

        r = np.array([s.recharge_rate for s in students])
        d = np.array([s.discharge_rate for s in students])
        b0 = np.array([s.initial_battery for s in students])

        num_total_time_slots = math.ceil(total_available_time / delta_t)
        num_segments = 2
        segment_time = total_available_time / num_segments
        num_segment_time_slots = math.ceil(segment_time / delta_t)

        final_U_matrix = np.zeros((num_students, num_total_time_slots))
        final_Y_matrix = np.zeros((num_students, num_total_time_slots))
        final_B_matrix = np.zeros((num_students, num_total_time_slots + 1))
        final_B_matrix[:, 0] = b0

        current_battery_levels = b0.copy()
        start_time = time.time()

        gurobi_optimizer = GurobiOptimization()

        for segment in range(num_segments):
            segment_start_time = segment * num_segment_time_slots

            # Update the initial battery levels for the current segment
            for i in range(num_students):
                students[i].initial_battery = current_battery_levels[i]

            # Create a new OptimizationInstance for the current segment
            partial_instance = OptimizationInstance(
                students=students,
                total_time=segment_time,
                delta_t=delta_t,
                num_sockets=num_sockets
            )

            gurobi_result = gurobi_optimizer.optimize_allocation(partial_instance)

            if gurobi_result['status'] == 'optimal':
                U_matrix = np.array(gurobi_result['U'])
                Y_matrix = np.array(gurobi_result['Y'])
                B_matrix = np.array(gurobi_result['B'])

                final_U_matrix[:, segment_start_time:segment_start_time + num_segment_time_slots] = U_matrix
                final_Y_matrix[:, segment_start_time:segment_start_time + num_segment_time_slots] = Y_matrix
                final_B_matrix[:, segment_start_time:segment_start_time + num_segment_time_slots + 1] = B_matrix

                current_battery_levels = B_matrix[:, -1]
            else:
                print(f"Segment {segment} did not converge.")
                result = {
                    'min_usage_time': None,
                    'U': None,
                    'Y': None,
                    'B': None,
                    'optimization_time': time.time() - start_time,
                    'model_build_time': 0,
                    'status': 'not_optimal'
                }
                return result

        end_time = time.time()

        result = {
            'min_usage_time': np.min(np.sum(final_U_matrix, axis=1)),
            'U': final_U_matrix.tolist(),
            'Y': final_Y_matrix.tolist(),
            'B': final_B_matrix.tolist(),
            'optimization_time': end_time - start_time,
            'model_build_time': 0,  # Model build time not separately tracked for iterative approach
            'status': 'optimal'
        }

        return result
