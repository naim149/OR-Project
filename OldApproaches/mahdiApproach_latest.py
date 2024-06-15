import gurobipy as gp
from gurobipy import GRB
import numpy as np
import time
import math

# Parameters
N = 6  # Total number of students
s = 3  # Total number of electrical sockets
T = 10  # Total available time slots in hours
delta_T = 1  # Time period for charging/discharging in hours
batteryOffset = 0  # Time period for charging/discharging in hours

# Generate random data for each student's battery capacity, recharge, and discharge rates
battery_capacity_mean, battery_capacity_std = 60, 10
battery_capacities = np.random.normal(battery_capacity_mean, battery_capacity_std, N)

r_watts_mean, r_watts_std = 37.5, 5
r_watts = np.random.normal(r_watts_mean, r_watts_std, N)

d_watts_mean, d_watts_std = 10, 2
d_watts = np.random.normal(d_watts_mean, d_watts_std, N)

# Conversion to battery percentage per hour based on individual battery capacities
r = (r_watts / battery_capacities) * 100
d = (d_watts / battery_capacities) * 100

# Initial battery levels in percentage
b0 = np.random.uniform(5, 15, N)

# Ensure values are within acceptable ranges
r_min, r_max = (30 / battery_capacity_mean) * 100, (45 / battery_capacity_mean) * 100
d_min, d_max = (5 / battery_capacity_mean) * 100, (15 / battery_capacity_mean) * 100

r = np.clip(r, r_min, r_max)
d = np.clip(d, d_min, d_max)

print("Battery capacities (Wh):", battery_capacities)
print("Recharge rates (r) in percentage per hour:", r)
print("Discharge rates (d) in percentage per hour:", d)
print("Initial battery levels (b0):", b0)

# Calculate the number of time slots
num_time_slots = math.ceil(T / delta_T)
# Create a new model
m = gp.Model("laptop_charging")

# Decision variables
Y = m.addVars(N, num_time_slots, vtype=GRB.BINARY, name="Y")  # Socket usage
U = m.addVars(N, num_time_slots, vtype=GRB.BINARY, name="U")  # Laptop usage
Z = m.addVar(vtype=GRB.INTEGER, name='min_battery')  # Minimum battery level
B = m.addVars(N, num_time_slots + 1, ub=100, vtype=GRB.CONTINUOUS, name="B")  # Battery levels

# Initial battery levels
for i in range(N):
    m.addConstr(B[i, 0] == b0[i], name=f"init_battery_{i}")

# Ensure minimum battery level Z and upper bound on battery levels
for i in range(N):
    m.addConstr(gp.quicksum( U[i, t]  for t in range(num_time_slots))>=Z , name=f"sum of usage {i}")

# Ensure battery levels are within bounds
for i in range(N):
    for t in range(num_time_slots + 1):
        m.addConstr(B[i, t] <= 100, name=f"max_battery_{i}_{t}")  # Upper bound constraint
        m.addConstr(B[i, t] >= 0, name=f"min_battery_{i}_{t}")  # Lower bound constraint

# Battery dynamics and operational status
for t in range(num_time_slots):
    for i in range(N):
        m.addConstr(B[i, t + 1] == B[i, t] + Y[i, t] * r[i] * delta_T +  Y[i, t] * U[i, t] * d[i] * delta_T - U[i, t] * d[i] * delta_T, name=f"battery_dynamics_{i}_{t}")

# Socket availability constraint
for t in range(num_time_slots):
    m.addConstr(gp.quicksum((Y[i, t] for i in range(N)) ) <= s, name=f"socket_avail_{t}")

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

        # Print the matrix U (laptop usage)
        print("\nMatrix U (Laptop Usage):")
        for i in range(N):
            print(f"Student {i}:", [round(U[i, t].X) for t in range(num_time_slots)])

        # Print the minimum battery level
        print(f"Minimum Usage Times: {Z.X} of {num_time_slots}")
    else:
        print("No optimal solution found.")

print(f"Optimization time: {end - start} seconds")
