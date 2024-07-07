# Project Overview
This project focuses on optimizing socket-student allocation using various algorithms, specifically Gurobi and a heuristic method. It includes generating results, comparing different algorithms, and visualizing data through figures.

## Main Components
1. **main.py**: Entry point for running optimizations using different algorithms.
2. **results_generator_N_vs_s_heuristic.py**: Generates results comparing the number of students (N) versus the number of sockets (s) using heuristic optimization.
3. **results_generator_gurobi_vs_heuristic.py**: Compares the performance of Gurobi and heuristic algorithms.
4. **results_generator_allocations.py**: Generates allocation results and visualizes them.
5. **results_create_performance_comparison_figure_from_csv.py**: Creates figures from CSV data comparing heuristic and Gurobi optimization results.
6. **results_create_execution_times_figure_from_csv.py**: Creates figures from CSV data to compare the execution times of heuristic and Gurobi algorithms.

## Algorithms
We currently have three optimization algorithms implemented:

1. **HeuristicOptimization**: A custom heuristic algorithm.
2. **GurobiOptimization**: Directly uses the Gurobi optimizer.
3. **GurobiHybridOptimization**: Combines the heuristic and Gurobi methods by using the heuristic as an initial guess for Gurobi.

## Usage

### 1. main.py
This script is the main entry point for running various optimizations using different algorithms. It allows you to specify parameters such as the number of students, total time, time step.(Seed can be specified)

#### Parameters:
- **N_values**: Number of students to investigate.
- **T**: Total time.
- **delta_T**: Time step.
- **num_time_slots**: Number of time slots, calculated as the ceiling of T divided by delta_T.
- **seed**: Seed for generating instance.
- **timeout**: Timeout limit for each algorithm execution.
- **Algorithms**: List of algorithms that will be used to generate the socket allocations.

### 2. results_generator_N_vs_s_heuristic.py
This script searches for the minimum number of sockets (s) needed to guarantee continous usage for the number of students (N).

#### Parameters:
- **ranges**: Ranges of number of students to investigate.
- **T**: Total time.
- **delta_T**: Time step.

### 3. results_generator_gurobi_vs_heuristic.py
This script compares the performance of Gurobi and heuristic algorithms. It allows you to specify parameters similar to the main script and includes a timeout.

#### Parameters:
- **ranges**: Ranges of number of students to investigate.
- **T**: Total time.
- **delta_T**: Time step.
- **timeout**: Timeout limit for each algorithm execution.

### 4. results_generator_allocations.py
This script generates student-socket allocation results and visualizes them using a figure. It allows you to specify parameters similar to the other scripts.

#### Parameters:
- **N**: Number of students.
- **s**: number of sockets.
- **T**: Total time.
- **delta_T**: Time step.
- **seed**: Seed for generating instance.
- **Algorithms**: List of algorithms that will be used to generate the socket allocations.

### 5. results_create_performance_comparison_figure_from_csv.py
This script creates figures from CSV data comparing heuristic and Gurobi optimization results. You can specify the directory path where the CSV files are stored and the name of the CSV file to read and generate the figure from.

#### Parameters:
- **CSV_FILE_NAME**: The name of the CSV file to read and generate the figure from.

### 6. results_create_execution_times_figure_from_csv.py
This script creates figures from CSV data to compare the execution times of heuristic and Gurobi algorithms. It allows you to specify the directory path where the CSV files are stored and the name of the CSV file to read and generate the figure from.

#### Parameters:
- **CSV_FILE_NAME**: The name of the CSV file to read and generate the figure from.

## Installation
1. Clone the repository:
```sh
git clone https://github.com/mahdi-assaf/OR_Aula_Studio-main.git

```
2. Run the setup batch script:
```sh
./setup.bat
```