import os
from patient import Patient
from schedulers import (
    RoundRobinScheduler,
    PriorityScheduler,
    ShortestJobFirstScheduler,
    FirstComeFirstServeScheduler,
    MultiLevelQueueScheduler,
)
from utils import load_patient_data, save_results
import matplotlib.pyplot as plt


def ensure_records_folder():
    if not os.path.exists("records"):
        os.makedirs("records")


def display_menu():
    print("\n===== Patient Scheduling System =====")
    print("1. Load Patient Data from File")
    print("2. Choose and Run Scheduling Algorithm")
    print("3. Find Optimized Scheduling Algorithm")
    print("4. Exit")


def display_scheduler_menu():
    print("\n===== Choose Scheduling Algorithm =====")
    print("1. Round Robin")
    print("2. Priority Scheduling (Non-Preemptive)")
    print("3. Priority Scheduling (Preemptive)")
    print("4. Shortest Job First (Non-Preemptive)")
    print("5. Shortest Job First (Preemptive)")
    print("6. First Come First Serve")
    print("7. Multi-Level Queue")



def run_scheduler(scheduler, patients, scheduler_name):
    try:
        patients_copy = [Patient(
            p.patient_id, p.treatment_time, p.priority, p.doctor, p.department, p.arrival_time
        ) for p in patients]

        for patient in patients_copy:
            scheduler.add_patient(patient)

        print(f"\nRunning {scheduler_name}...")
        scheduler.schedule()

        print("\nSchedule Results:")
        print(f"{'Patient ID':<10}{'Wait Time (mins)':<20}{'Turnaround Time (mins)':<25}{'Completion Time (HH:MM)':<25}")
        print("-" * 80)
        for patient in scheduler.completed_patients:
            print(f"{patient.patient_id:<10}{patient.wait_time:<20}{patient.turnaround_time:<25}{format_time(patient.completion_time):<25}")

        results_file = f"records/{scheduler_name.lower().replace(' ', '_')}_results.json"
        save_results(scheduler.completed_patients, results_file)
        print(f"\nResults saved to {results_file}")

        scheduler.clear()
    except Exception as e:
        print(f"Error during scheduling: {e}")


def find_optimized_algorithm(patients):
    try:
        print("\nFinding Optimized Scheduling Algorithm...")
        schedulers = {
            "Round Robin": RoundRobinScheduler(5),
            "Priority Scheduling (Non-Preemptive)": PriorityScheduler(preemptive=False),
            "Priority Scheduling (Preemptive)": PriorityScheduler(preemptive=True),
            "Shortest Job First (Non-Preemptive)": ShortestJobFirstScheduler(preemptive=False),
            "Shortest Job First (Preemptive)": ShortestJobFirstScheduler(preemptive=True),
            "First Come First Serve": FirstComeFirstServeScheduler(),
        }

        best_scheduler_name = None

        best_avg_wait_time = float("inf")

        for name, scheduler in schedulers.items():
            patients_copy = [Patient(
                p.patient_id, p.treatment_time, p.priority, p.doctor, p.department, p.arrival_time
            ) for p in patients]

            for patient in patients_copy:
                scheduler.add_patient(patient)
            scheduler.schedule()

            avg_wait_time = sum(p.wait_time for p in scheduler.completed_patients) / len(patients)
            scheduler.clear()

            if avg_wait_time < best_avg_wait_time:
                best_avg_wait_time = avg_wait_time
                best_scheduler_name = name

        print(f"\nOptimized Algorithm: {best_scheduler_name} (Average Wait Time: {best_avg_wait_time:.2f} mins)")
    except Exception as e:
        print(f"Error in optimization: {e}")


def format_time(minutes):
    from datetime import timedelta, datetime
    base_time = datetime.strptime("00:00", "%H:%M")
    return (base_time + timedelta(minutes=minutes)).strftime("%H:%M")


def main():
    ensure_records_folder()
    patients = []
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            file_name = input("Enter file name: ")
            try:
                patients = load_patient_data(file_name)
                print(f"{len(patients)} patients loaded!")
            except Exception as e:
                print(f"Error loading patient data: {e}")
        elif choice == "2":
            if patients:
                display_scheduler_menu()
                scheduler_choice = input("Enter your choice: ")
                scheduler = None
                scheduler_name = None

                if scheduler_choice == "1":
                    time_quantum = int(input("Enter Time Quantum for Round Robin: "))
                    scheduler = RoundRobinScheduler(time_quantum)
                    scheduler_name = "Round Robin"
                elif scheduler_choice == "2":
                    scheduler = PriorityScheduler(preemptive=False)
                    scheduler_name = "Priority Scheduling (Non-Preemptive)"
                elif scheduler_choice == "3":
                    scheduler = PriorityScheduler(preemptive=True)
                    scheduler_name = "Priority Scheduling (Preemptive)"
                elif scheduler_choice == "4":
                    scheduler = ShortestJobFirstScheduler(preemptive=False)
                    scheduler_name = "Shortest Job First (Non-Preemptive)"
                elif scheduler_choice == "5":
                    scheduler = ShortestJobFirstScheduler(preemptive=True)
                    scheduler_name = "Shortest Job First (Preemptive)"
                elif scheduler_choice == "6":
                    scheduler = FirstComeFirstServeScheduler()
                    scheduler_name = "First Come First Serve"
                elif scheduler_choice == "7":
                    levels = [(RoundRobinScheduler(5), 5),(PriorityScheduler(preemptive=True), None), (FirstComeFirstServeScheduler(), None),]
                    scheduler = MultiLevelQueueScheduler(levels)
                    scheduler_name = "Multi-Level Queue"
                    
                else:
                    print("Invalid choice!")
                    continue

                run_scheduler(scheduler, patients, scheduler_name)
            else:
                print("No patient data available.")
        elif choice == "3":
            if patients:
                find_optimized_algorithm(patients)
            else:
                print("No patient data available.")
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
