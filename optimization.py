import numpy as np
from scipy.optimize import minimize

# Define the objective function
def objective(x):
    return x[0]**2 + x[1]**2 + x[2]**2

# Initial guess
x0 = [1, 1, 1]

# Optimize
result = minimize(objective, x0)

# Print the result
print("Optimal value:", result.fun)
print("Optimal solution:", result.x)