import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

CSV_FILE_NAME = 'gurobi_vs_heuristic_N_39_20240707_163950.csv'

def create_histogram_from_csv():
    CSV_DIRECTORY_PATH = 'Gurobi vs Heuristic Comparison Results/'
    csv_file_path = CSV_DIRECTORY_PATH + CSV_FILE_NAME
    
    df = pd.read_csv(csv_file_path)
    sockets = sorted(df['Sockets'].unique())

    fig, ax1 = plt.subplots(figsize=(12, 6))
    heuristic_color = 'tab:blue'
    gurobi_color = 'tab:orange'

    heuristic_z_avg, heuristic_z_min, heuristic_z_max = [], [], []
    heuristic_u_avg, heuristic_u_min, heuristic_u_max = [], [], []
    gurobi_z_avg, gurobi_z_min, gurobi_z_max = [], [], []
    gurobi_u_avg, gurobi_u_min, gurobi_u_max = [], [], []

    for socket in sockets:
        socket_data = df[df['Sockets'] == socket]

        heuristic_z = socket_data['Heuristic_Z']
        heuristic_u = socket_data['Heuristic_U'] * 32  # Multiply U by 32 to represent the average usage per student

        heuristic_z_avg.append(heuristic_z.mean())
        heuristic_z_min.append(heuristic_z.min())
        heuristic_z_max.append(heuristic_z.max())

        heuristic_u_avg.append(heuristic_u.mean())
        heuristic_u_min.append(heuristic_u.min())
        heuristic_u_max.append(heuristic_u.max())

        gurobi_z = socket_data['Gurobi_Z']
        gurobi_u = socket_data['Gurobi_U'] * 32  # Multiply U by 32 to represent the average usage per student

        gurobi_z_avg.append(gurobi_z.mean())
        gurobi_z_min.append(gurobi_z.min())
        gurobi_z_max.append(gurobi_z.max())

        gurobi_u_avg.append(gurobi_u.mean())
        gurobi_u_min.append(gurobi_u.min())
        gurobi_u_max.append(gurobi_u.max())

    heuristic_z_avg = np.array(heuristic_z_avg)
    heuristic_z_min = np.array(heuristic_z_min)
    heuristic_z_max = np.array(heuristic_z_max)
    heuristic_u_avg = np.array(heuristic_u_avg)
    heuristic_u_min = np.array(heuristic_u_min)
    heuristic_u_max = np.array(heuristic_u_max)
    gurobi_z_avg = np.array(gurobi_z_avg)
    gurobi_z_min = np.array(gurobi_z_min)
    gurobi_z_max = np.array(gurobi_z_max)
    gurobi_u_avg = np.array(gurobi_u_avg)
    gurobi_u_min = np.array(gurobi_u_min)
    gurobi_u_max = np.array(gurobi_u_max)

    heuristic_z_err = [heuristic_z_avg - heuristic_z_min, heuristic_z_max - heuristic_z_avg]
    gurobi_z_err = [gurobi_z_avg - gurobi_z_min, gurobi_z_max - gurobi_z_avg]
    heuristic_u_err = [heuristic_u_avg - heuristic_u_min, heuristic_u_max - heuristic_u_avg]
    gurobi_u_err = [gurobi_u_avg - gurobi_u_min, gurobi_u_max - gurobi_u_avg]

    bar_width = 0.2

    ax1.bar([s - bar_width * 1.5 for s in sockets], heuristic_z_avg, width=bar_width, color=heuristic_color, label='Heuristic Z', align='center')
    ax1.errorbar([s - bar_width * 1.5 for s in sockets], heuristic_z_avg, yerr=heuristic_z_err, fmt='none', ecolor='black', capsize=5)
    
    ax1.bar([s - bar_width * 0.5 for s in sockets], gurobi_z_avg, width=bar_width, color=gurobi_color, label='Gurobi Z', align='center')
    ax1.errorbar([s - bar_width * 0.5 for s in sockets], gurobi_z_avg, yerr=gurobi_z_err, fmt='none', ecolor='black', capsize=5)

    ax1.set_ylabel('Z')
    ax1.set_ylim(0, 35)  

    ax2 = ax1.twinx()

    ax2.bar([s + bar_width * 0.5 for s in sockets], heuristic_u_avg, width=bar_width, color=heuristic_color, label='Heuristic M', align='center', alpha=0.5)
    ax2.errorbar([s + bar_width * 0.5 for s in sockets], heuristic_u_avg, yerr=heuristic_u_err, fmt='none', ecolor='black', capsize=5)
    
    ax2.bar([s + bar_width * 1.5 for s in sockets], gurobi_u_avg, width=bar_width, color=gurobi_color, label='Gurobi M', align='center', alpha=0.5)
    ax2.errorbar([s + bar_width * 1.5 for s in sockets], gurobi_u_avg, yerr=gurobi_u_err, fmt='none', ecolor='black', capsize=5)

    ax2.set_ylabel('M (Average Usage per Student)')
    ax2.set_ylim(0, 35)  

    ax1.set_xticks(sockets)
    ax1.set_xticklabels(sockets)
    ax1.set_xlabel('Sockets')

    heuristic_patch_z = plt.Line2D([0], [0], color=heuristic_color, lw=4, label='Heuristic Z')
    gurobi_patch_z = plt.Line2D([0], [0], color=gurobi_color, lw=4, label='Gurobi Z')
    heuristic_patch_u = plt.Line2D([0], [0], color=heuristic_color, lw=4, label='Heuristic M', alpha=0.5)
    gurobi_patch_u = plt.Line2D([0], [0], color=gurobi_color, lw=4, label='Gurobi M', alpha=0.5)
    plt.legend(handles=[heuristic_patch_z, gurobi_patch_z, heuristic_patch_u, gurobi_patch_u], loc='upper left')

    plt.title('Heuristic vs Gurobi: Z and M for Different Sockets')
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    create_histogram_from_csv()
