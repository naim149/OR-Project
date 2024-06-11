import gurobipy as gp
from gurobipy import GRB
import numpy as np

# Parameters
N = 1 # Total number of students
s = 0  # Total number of electrical sockets
T = 2  # Total available time slots
delta_T = 1  # Time period for charging/discharging

# Generate random data for rates and initial battery levels
np.random.seed(0)
r = np.random.randint(10, 20, N)  # Recharge rates
d = np.random.randint(5, 10, N)  # Discharge rates
b0 = np.random.uniform(0, 10, N)  # Initial battery levels

# Create a new model
m = gp.Model("laptop_charging")

# Decision variables
Y = m.addVars(N, T, vtype=GRB.BINARY, name="Y")  # Socket usage
O = m.addVars(N, T, vtype=GRB.BINARY, name="O")  # Operational status
B = m.addVars(N, T+1, vtype=GRB.CONTINUOUS, name="B")  # Battery levels
Z = m.addVars(N, vtype=GRB.CONTINUOUS, name="Z")  # Operational time ratios

# Initial battery levels
for i in range(N):
    m.addConstr(B[i, 0] == b0[i])

# Battery dynamics and operational status
for t in range(T):
    for i in range(N):
        m.addConstr(B[i, t+1] - B[i, t] == Y[i, t] *( r[i] * delta_T +  d[i] * delta_T) - d[i] * delta_T )
        # m.addConstr(B[i, t+1] <= 100)  # Clip battery level at 100
        # m.addConstr(B[i, t+1] >= 0)    # Clip battery level at 0
        # m.addConstr(O[i, t] >= Y[i, t])
        # m.addConstr(O[i, t] >= B[i, t]/100)

# Socket availability constraint
for t in range(T):
    m.addConstr(gp.quicksum(Y[i, t] for i in range(N)) <= s)

# Compute Z_i for each student
for i in range(N):
    m.addConstr(Z[i] == gp.quicksum(O[i, t] * delta_T/ T for t in range(T)) )

# Compute sum of Z_i and sum of Z_i squared
# sum_Z_sq = gp.quicksum(Z[i] * Z[i] for i in range(N))

# Set the objective to maximize the variance
m.setObjective(gp.quicksum(Z[i] for i in range(N)), GRB.MINIMIZE)

# Optimize the model
m.optimize()

# Print results
# If the model is infeasible, compute the IIS
if m.status == GRB.INFEASIBLE:
    print("The model is infeasible; computing IIS...")
    m.computeIIS()
    m.write("model.ilp")
    print("IIS written to file 'model.ilp'")
else:
    # Print results if the model is feasible
    if m.status == GRB.OPTIMAL:
        # Print the matrix B (battery levels)
        print("Matrix B (Battery Levels):")
        for i in range(N):
            print(f"Student {i}:", [B[i, t].X for t in range(T + 1)])

        print("Operational Time O:")
        for i in range(N):
            print(f"Student {i}:", [O[i, t].X for t in range(T )])

        # Print the matrix Y (socket usage)
        print("\nMatrix Y (Socket Usage):")
        for i in range(N):
            print(f"Student {i}:", [Y[i, t].X for t in range(T)])

        # Print the operational time ratios
        print("\nOperational Time Ratios (Z):")
        for i in range(N):
            print(f"Student {i}: Z_i = {Z[i].X}")
    else:
        print("No optimal solution found.")