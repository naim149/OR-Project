import random
from typing import List
from Entities.Student import Student
from Entities.Optimization_Instance import OptimizationInstance
from Managers.OptimizationInstance_manager import OptimizationInstanceManager
from Managers.Satisfaction_manager import SatisfactionManager




def calculate_out_of_battery_time(student: Student) -> float:
    """Calculate the time in hours until the student's laptop runs out of battery."""
    if student.discharge_rate <= 0:
        return float('inf')  # Infinite time if discharge rate is zero or negative
    return student.initial_battery / student.discharge_rate

def main():
    # Create an instance of the optimization problem using the OptimizationInstanceManager
    instance_manager = OptimizationInstanceManager(seed=1022)
    optimization_instance = instance_manager.create_instance()

    # Extract necessary parameters from the optimization instance
    students = optimization_instance.students
    num_sockets = optimization_instance.num_sockets
    total_time = optimization_instance.total_time

    print(f"Number of Students: {len(students)}")
    print(f"Number of Sockets: {num_sockets}")
    print(f"Total Available Time: {total_time:.2f} hours")
    print("\nStudents:")
    for i, student in enumerate(students):
        out_of_battery_time = calculate_out_of_battery_time(student)
        print(f"Student {i+1}: Recharge Rate = {student.recharge_rate:.2f}, Discharge Rate = {student.discharge_rate:.2f}, Initial Battery = {student.initial_battery:.2f}%")
        print(f" -> Time Until Out of Battery = {out_of_battery_time:.2f} hours")

    # Initialize variables for allocated times
    allocated_times = [0.0] * len(students)
    total_available_time = num_sockets * total_time

    # Allocate times to students (this is a simple heuristic, you can improve this with a more complex algorithm)
    for i in range(len(students)):
        if total_available_time <= 0:
            break
        max_time_for_student = min(total_time, total_available_time)
        allocated_time = random.uniform(0, max_time_for_student)
        allocated_times[i] = allocated_time
        total_available_time -= allocated_time

    # Calculate total satisfaction using the SatisfactionManager
    total_satisfaction = SatisfactionManager.calculate_total_satisfaction(allocated_times, optimization_instance)

    # Print allocated times and total satisfaction
    for i, time in enumerate(allocated_times):
        print(f"Student {i+1}: Allocated Time = {time:.2f} hours")

    print(f"Total Satisfaction: {total_satisfaction:.2f}")

if __name__ == "__main__":
    main()
