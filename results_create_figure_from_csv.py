import pandas as pd
import matplotlib.pyplot as plt

# Define the fixed path to the CSV file directory
CSV_DIRECTORY_PATH = 'Gurobi vs Heuristic Comparison Results/'

# Variable to hold the file name (change this before running the script)
CSV_FILE_NAME = 'gurobi_vs_heuristic_N_8_20240701_114232.csv'

def create_figure_from_csv():
    # Construct the full file path
    csv_file_path = CSV_DIRECTORY_PATH + CSV_FILE_NAME
    
    # Read the data from the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Extract unique sockets and sort them
    sockets = sorted(df['Sockets'].unique())

    # Prepare the figure
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Colors for the different algorithms
    heuristic_color = 'tab:blue'
    gurobi_color = 'tab:orange'

    # Iterate over each socket value to plot the candle charts
    for i, socket in enumerate(sockets):
        # Filter data for the current socket
        socket_data = df[df['Sockets'] == socket]

        # Heuristic data
        heuristic_z = socket_data['Heuristic_Z']
        heuristic_u = socket_data['Heuristic_U']

        # Gurobi data
        gurobi_z = socket_data['Gurobi_Z']
        gurobi_u = socket_data['Gurobi_U']

        # Offset to avoid overlapping
        pos_h_z = socket - 0.3
        pos_g_z = socket - 0.1
        pos_h_u = socket + 0.1
        pos_g_u = socket + 0.3

        # Box plot for Heuristic Z
        ax1.boxplot(heuristic_z, positions=[pos_h_z], widths=0.1, patch_artist=True,
                    boxprops=dict(facecolor=heuristic_color), medianprops=dict(color='black'))
        
        # Box plot for Gurobi Z
        ax1.boxplot(gurobi_z, positions=[pos_g_z], widths=0.1, patch_artist=True,
                    boxprops=dict(facecolor=gurobi_color), medianprops=dict(color='black'))

        # Adding labels for Z axis (left y-axis)
        ax1.set_ylabel('Z')
        ax1.set_ylim(0, 35)  # Ensure the Z axis shows up to 32

        # Creating another y-axis for U
        ax2 = ax1.twinx()

        # Box plot for Heuristic U
        ax2.boxplot(heuristic_u, positions=[pos_h_u], widths=0.1, patch_artist=True,
                    boxprops=dict(facecolor=heuristic_color, alpha=0.5), medianprops=dict(color='black'))
        
        # Box plot for Gurobi U
        ax2.boxplot(gurobi_u, positions=[pos_g_u], widths=0.1, patch_artist=True,
                    boxprops=dict(facecolor=gurobi_color, alpha=0.5), medianprops=dict(color='black'))

        # Adding labels for U axis (right y-axis)
        ax2.set_ylabel('U')
        ax2.set_ylim(0, 1.1)  # Ensure the U axis goes slightly above 1 for clarity

    # Setting the x-axis labels
    ax1.set_xticks(sockets)
    ax1.set_xticklabels(sockets)
    ax1.set_xlabel('Sockets')

    # Adding legend
    heuristic_patch_z = plt.Line2D([0], [0], color=heuristic_color, lw=4, label='Heuristic Z')
    gurobi_patch_z = plt.Line2D([0], [0], color=gurobi_color, lw=4, label='Gurobi Z')
    heuristic_patch_u = plt.Line2D([0], [0], color=heuristic_color, lw=4, label='Heuristic U', alpha=0.5)
    gurobi_patch_u = plt.Line2D([0], [0], color=gurobi_color, lw=4, label='Gurobi U', alpha=0.5)
    plt.legend(handles=[heuristic_patch_z, gurobi_patch_z, heuristic_patch_u, gurobi_patch_u], loc='upper left')

    # Title and grid
    plt.title('Heuristic vs Gurobi: Z and U for Different Sockets')
    plt.grid(True)

    # Show the plot
    plt.show()

if __name__ == "__main__":
    create_figure_from_csv()
