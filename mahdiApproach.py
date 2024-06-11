import gurobipy as gp
from gurobipy import GRB
import pandas as pd

# Define your parameters
N = 2  # Number of students
s = 1   # Number of sockets
T = 10  # Total available time
r_i = [5 for _ in range(N)]  # Recharge rates
d_i = [10 for _ in range(N)]  # Discharge rates
b_i = [50 for _ in range(N)]  # Initial battery levels

# Calculate delta_t
def calculate_compatible_delta_t(max_rate: float, total_time: int) -> float:
    delta_t = 1 / max_rate
    ratio = int(total_time / delta_t)
    delta_t = total_time / (ratio + 1)
    return delta_t

max_rate = max(max(r_i), max(d_i))
delta_t = calculate_compatible_delta_t(max_rate, T)

a = T/delta_t
# Create a new model
model = gp.Model("Maximize_Student_Satisfaction")

# Define variables
X = model.addVars(N, int(T // delta_t), vtype=GRB.BINARY, name="X")

# Define the objective function
model.setObjective(
    gp.quicksum(
        b_i[i] + gp.quicksum(X[i, j] * (r_i[i] + d_i[i]) for j in range(int(T // delta_t))) - int(T // delta_t) * d_i[i] 
        + gp.quicksum(X[i, j] for j in range(int(T // delta_t))) * delta_t 
        for i in range(N)
    ),
    GRB.MAXIMIZE)

# Add the total time constraint
model.addConstr(
    gp.quicksum(X[i, j] * delta_t for i in range(N) for j in range(int(T // delta_t))) <= s * T,
    "TotalSocketTime")

# Add the total time constraint
for j in range(int(T // delta_t)):
   model.addConstr(
    gp.quicksum(X[i, j] * delta_t  for i in range(N)) <= s,
    "Total Sockets")

# Add the binary constraints
for i in range(N):
    for j in range(int(T // delta_t)):
        model.addConstr(X[i, j] <= 1, f"BinaryConstr_{i}_{j}")
        model.addConstr(X[i, j] >= 0, f"BinaryConstr_{i}_{j}")

# Optimize the model
model.optimize()

# Print the results in a table format
if model.status == GRB.OPTIMAL:
    print("Optimal Solution Found:")
    
    # Create a DataFrame to display the results
    data = []
    for i in range(N):
        row = []
        for j in range(int(T // delta_t)):
            row.append('Connected' if X[i, j].X == 1 else 'Not Connected')
        data.append(row)
    
    df = pd.DataFrame(data, columns=[f'Time Interval {j}' for j in range(int(T // delta_t))],
                      index=[f'Student {i}' for i in range(N)])
    print(df)
    print("Total Satisfaction:", model.objVal)
    
    # Calculate the matrix B
    B = [[0 for _ in range(int(T // delta_t) + 1)] for _ in range(N)]
    for i in range(N):
        B[i][0] = b_i[i]
        for j in range(int(T // delta_t)):
            if X[i, j].X == 1:
                B[i][j+1] = min(100, B[i][j] + (r_i[i] + d_i[i]) * delta_t - d_i[i] * delta_t)
            else:
                B[i][j+1] = max(0, B[i][j] - d_i[i] * delta_t)

    # Print the matrix B
    B_df = pd.DataFrame(B, columns=[f'Time {t}' for t in range(int(T // delta_t) + 1)],
                        index=[f'Student {i}' for i in range(N)])
    print("Battery Levels (B matrix):")
    print(B_df)
else:
    print("No Optimal Solution Found")
