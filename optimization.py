# optimization.py
from Entities.student import Student
from Entities.optimization_instance import OptimizationInstance
from Managers.optimizationInstance_manager import OptimizationInstanceManager
from Managers.satisfaction_manager import SatisfactionManager
from Algorithms.initial_guess_algorithm import ImprovedInitialGuessAlgorithm
from Algorithms.simulated_annealing import SimulatedAnnealing
from Algorithms.tabu_search_algorithm import TabuSearch
from Algorithms.gurobi_algorithm import ImprovedGurobiOptimization
from Managers.optimization_manager import OptimizationManager

def main():
    instance_manager = OptimizationInstanceManager(seed=10)
    optimization_instance = instance_manager.create_instance()

    students = optimization_instance.students
    num_sockets = optimization_instance.num_sockets
    total_time = optimization_instance.total_time
    total_working_hours = optimization_instance.total_working_hours

    print(f"Number of Students: {len(students)}")
    print(f"Number of Sockets: {num_sockets}")
    print(f"Total Available Time: {total_time:.2f} hours")
    print(f"Total Working Hours: {total_working_hours:.2f} hours")
    print("\nOptimizing allocation...\n")

    algorithms = [
        ImprovedInitialGuessAlgorithm(),
        SimulatedAnnealing(max_iterations=1000, initial_temp=100, cooling_rate=0.003),
        TabuSearch(max_iterations=500, tabu_tenure=5),
        ImprovedGurobiOptimization()
    ]
    manager = OptimizationManager(algorithms)
    results = manager.optimize(optimization_instance)

    for algorithm_name, result in results.items():
        print(f"\nResults from {algorithm_name}:")
        if isinstance(result, str):
            print(result)
        else:
            toos_before_allocation = [SatisfactionManager.calculate_out_of_battery_time(student, 0, total_working_hours) for student in students]
            toos_after_allocation = [SatisfactionManager.calculate_out_of_battery_time(student, time, total_working_hours) for student, time in zip(students, result)]
            total_satisfaction = SatisfactionManager.calculate_total_satisfaction(result, optimization_instance)
            total_out_of_service_hours = sum(toos_after_allocation)

            print(f"{'Student':<10}{'Ch-R':<10}{'Dis-R':<10}{'Init-Bat':<10}{'Alloc-Time':<12}{'TOoS-Before':<12}{'TOoS-After':<12}")
            print("="*76)
            for i, (time, student, toos_before, toos_after) in enumerate(zip(result, students, toos_before_allocation, toos_after_allocation)):
                print(f"{i+1:<10}{student.recharge_rate:<10.2f}{student.discharge_rate:<10.2f}{student.initial_battery:<10.2f}{time:<12.2f}{toos_before:<12.2f}{toos_after:<12.2f}")

            print(f"\nSummary:")
            print(f"Total Satisfaction: {total_satisfaction:.2f}")
            print(f"Total Out of Service Hours: {total_out_of_service_hours:.2f} hours")

if __name__ == "__main__":
    main()
