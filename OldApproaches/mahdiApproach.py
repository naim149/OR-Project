import gurobipy as gp
from gurobipy import GRB
import numpy as np
import time
import math

# Parameters
N = 5  # Total number of students
s = 1  # Total number of electrical sockets (reduced to 8)
T = 12  # Total available time slots in hours
delta_T = 1  # Time period for charging/discharging in hours

batteryOffset = 0  # Time period for charging/discharging in hours

# Generate random rates and initial battery levels
np.random.seed(0)
r = np.random.randint(10, 20, N)  # Recharge rates (units per hour)
d = np.random.randint(5, 10, N)  # Discharge rates (units per hour)
b0 = np.random.uniform(5, 15, N)  # Initial battery levels

for i in range(N):
    b0[i] += batteryOffset

# Calculate the number of time slots
num_time_slots = math.ceil(T / delta_T)

# Create a new model
m = gp.Model("laptop_charging")

# Decision variables
Y = m.addVars(N, num_time_slots, vtype=GRB.BINARY, name="Y")  # Socket usage
Z = m.addVar(vtype=GRB.CONTINUOUS, name='min_battery')  # Minimum battery level
B = m.addVars(N, num_time_slots + 1,ub= batteryOffset+100, vtype=GRB.CONTINUOUS, name="B")  # Battery levels

# Initial battery levels
for i in range(N):
    m.addConstr(B[i, 0] == b0[i], name=f"init_battery_{i}")

# Ensure minimum battery level Z and upper bound on battery levels
for i in range(N):
    for t in range(num_time_slots + 1):
        m.addConstr(Z <= (B[i, t]), name=f"min_battery_{i}_{t}")

# Ensure minimum battery level Z and upper bound on battery levels
# for i in range(N):
    # m.addConstr(gp.quicksum( B[i, t]  for t in range(num_time_slots))/num_time_slots >=Z , name=f"sum_battery_{i}")
    # for t in range(num_time_slots + 1):
        # m.addConstr(B[i, t] <= batteryOffset+100, name=f"max_battery_{i}_{t}")  # Upper bound constraint
        # m.addConstr(B[i, t] >= batteryOffset, name=f"min_battery_{i}_{t}")  # Lower bound constraint

# Battery dynamics and operational status
for t in range(num_time_slots):
    for i in range(N):
        m.addConstr(B[i, t + 1] == B[i, t] + Y[i, t] * r[i] * delta_T - d[i] * delta_T, name=f"battery_dynamics_{i}_{t}")

# Socket availability constraint
for t in range(num_time_slots):
    m.addConstr(gp.quicksum(Y[i, t] for i in range(N)) <= s, name=f"socket_avail_{t}")

# Set the objective to maximize the minimum battery level
m.setObjective(Z, GRB.MAXIMIZE)

# Optimize the model
start = time.time()
m.optimize()
end = time.time()

# Print results
if m.status == GRB.INFEASIBLE:
    print("The model is infeasible; computing IIS...")
    m.computeIIS()
    m.write("model.ilp")
    print("IIS written to file 'model.ilp'")
elif m.status == GRB.UNBOUNDED:
    print("The model is unbounded.")
else:
    # Print results if the model is feasible
    if m.status == GRB.OPTIMAL:
        # Print the matrix B (battery levels)
        print("Matrix B (Battery Levels):")
        for i in range(N):
            print(f"Student {i}:", [B[i, t].X for t in range(num_time_slots + 1)])

        # Print the matrix Y (socket usage)
        print("\nMatrix Y (Socket Usage):")
        for i in range(N):
            print(f"Student {i}:", [round(Y[i, t].X) for t in range(num_time_slots)])

        # Print the minimum battery level
        print("\nMinimum Battery Level (Z):")
        print(f"Minimum Battery Level: {Z.X}")
    else:
        print("No optimal solution found.")

print(f"Optimization time: {end - start} seconds")
