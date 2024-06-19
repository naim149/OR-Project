import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
file_path = 'Minimum Optimal Sockets Comparison.csv'  # Replace with your file path
data = pd.read_csv(file_path)

# Extract the data
num_students = data['Number of Students']
gurobi_sockets = data['Gurobi Minimum Required Sockets']
heuristic_sockets = data['Heuristic Minimum Required Sockets']

# Create the histogram
bar_width = 0.35
index = np.arange(len(num_students))

fig, ax = plt.subplots(figsize=(12, 8))

bar1 = ax.bar(index, gurobi_sockets, bar_width, label='Gurobi')
bar2 = ax.bar(index + bar_width, heuristic_sockets, bar_width, label='Heuristic')

ax.set_xlabel('Number of Students')
ax.set_ylabel('Minimum Required Sockets ')
ax.set_title('Minimum Required Sockets to Ensure Continuous laptop Usage by Gurobi and Heuristic Methods')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(num_students)
ax.legend()

# Add grid
ax.grid(False)

# Add legend
ax.legend()

plt.show()
