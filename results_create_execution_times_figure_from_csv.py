import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

CSV_FILE_NAME = 'gurobi_vs_heuristic_N_39_20240707_163950.csv'

def create_execution_time_histogram_from_csv():
    CSV_DIRECTORY_PATH = 'Gurobi vs Heuristic Comparison Results/'
    csv_file_path = CSV_DIRECTORY_PATH + CSV_FILE_NAME

    df = pd.read_csv(csv_file_path)
    sockets = sorted(df['Sockets'].unique())

    fig, ax1 = plt.subplots(figsize=(12, 6))
    heuristic_color = 'tab:blue'
    gurobi_build_color = 'tab:green'
    gurobi_opt_color = 'tab:orange'

    heuristic_time_avg, heuristic_time_min, heuristic_time_max = [], [], []
    gurobi_build_time_avg, gurobi_build_time_min, gurobi_build_time_max = [], [], []
    gurobi_opt_time_avg, gurobi_opt_time_min, gurobi_opt_time_max = [], [], []

    for socket in sockets:
        socket_data = df[df['Sockets'] == socket]

        heuristic_time = socket_data['Heuristic_Optimization_Time']

        heuristic_time_avg.append(heuristic_time.mean())
        heuristic_time_min.append(heuristic_time.min())
        heuristic_time_max.append(heuristic_time.max())

        gurobi_build_time = socket_data['Gurobi_model_build_time']

        gurobi_build_time_avg.append(gurobi_build_time.mean())
        gurobi_build_time_min.append(gurobi_build_time.min())
        gurobi_build_time_max.append(gurobi_build_time.max())

        gurobi_opt_time = socket_data['Gurobi_optimization_time']

        gurobi_opt_time_avg.append(gurobi_opt_time.mean())
        gurobi_opt_time_min.append(gurobi_opt_time.min())
        gurobi_opt_time_max.append(gurobi_opt_time.max())

    heuristic_time_avg = np.array(heuristic_time_avg)
    heuristic_time_min = np.array(heuristic_time_min)
    heuristic_time_max = np.array(heuristic_time_max)
    gurobi_build_time_avg = np.array(gurobi_build_time_avg)
    gurobi_build_time_min = np.array(gurobi_build_time_min)
    gurobi_build_time_max = np.array(gurobi_build_time_max)
    gurobi_opt_time_avg = np.array(gurobi_opt_time_avg)
    gurobi_opt_time_min = np.array(gurobi_opt_time_min)
    gurobi_opt_time_max = np.array(gurobi_opt_time_max)

    heuristic_time_err = [heuristic_time_avg - heuristic_time_min, heuristic_time_max - heuristic_time_avg]
    gurobi_build_time_err = [gurobi_build_time_avg - gurobi_build_time_min, gurobi_build_time_max - gurobi_build_time_avg]
    gurobi_opt_time_err = [gurobi_opt_time_avg - gurobi_opt_time_min, gurobi_opt_time_max - gurobi_opt_time_avg]

    bar_width = 0.2

    ax1.bar([s - bar_width * 1.5 for s in sockets], heuristic_time_avg, width=bar_width, color=heuristic_color, label='Heuristic Optimization Time', align='center')
    ax1.errorbar([s - bar_width * 1.5 for s in sockets], heuristic_time_avg, yerr=heuristic_time_err, fmt='none', ecolor='black', capsize=5)
    
    ax1.bar([s - bar_width * 0.5 for s in sockets], gurobi_build_time_avg, width=bar_width, color=gurobi_build_color, label='Gurobi Model Build Time', align='center')
    ax1.errorbar([s - bar_width * 0.5 for s in sockets], gurobi_build_time_avg, yerr=gurobi_build_time_err, fmt='none', ecolor='black', capsize=5)
    
    ax1.bar([s + bar_width * 0.5 for s in sockets], gurobi_opt_time_avg, width=bar_width, color=gurobi_opt_color, label='Gurobi Optimization Time', align='center')
    ax1.errorbar([s + bar_width * 0.5 for s in sockets], gurobi_opt_time_avg, yerr=gurobi_opt_time_err, fmt='none', ecolor='black', capsize=5)

    ax1.set_ylabel('Time (seconds)')
    ax1.set_yscale('log')
    ax1.set_xlabel('Sockets')

    ax1.set_xticks(sockets)
    ax1.set_xticklabels(sockets)

    heuristic_patch_time = plt.Line2D([0], [0], color=heuristic_color, lw=4, label='Heuristic Optimization Time')
    gurobi_patch_build = plt.Line2D([0], [0], color=gurobi_build_color, lw=4, label='Gurobi Model Build Time')
    gurobi_patch_opt = plt.Line2D([0], [0], color=gurobi_opt_color, lw=4, label='Gurobi Optimization Time')
    plt.legend(handles=[heuristic_patch_time, gurobi_patch_build, gurobi_patch_opt], loc='upper left')

    plt.title('Heuristic vs Gurobi: Execution Times for Different Sockets')
    plt.grid(True, which="both", ls="--")

    plt.show()

if __name__ == "__main__":
    create_execution_time_histogram_from_csv()
