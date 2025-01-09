import os
import matplotlib.pyplot as plt

# Base Scheduler class
class Scheduler:
    def __init__(self):
        self.current_time = 0
        self.completed_patients = []

    def add_patient(self, patient):
        raise NotImplementedError

    def schedule(self):
        raise NotImplementedError

    def clear(self):
        self.current_time = 0
        self.completed_patients = []

    def ensure_records_folder(self):
        if not os.path.exists("records"):
            os.makedirs("records")

    def visualize_gantt_chart(self, title, gantt_chart, save_file=None):
        self.ensure_records_folder()

        start_times = [start for start, _, _ in gantt_chart]
        durations = [duration for _, _, duration in gantt_chart]
        labels = [f"Patient {patient_id}" for _, patient_id, _ in gantt_chart]

        plt.barh(labels, durations, left=start_times, color="skyblue")
        plt.xlabel("Time (in minutes)")
        plt.ylabel("Patient IDs")
        plt.title(title)
        plt.grid(axis="x")

        if save_file:
            file_path = os.path.join("records", save_file)
            plt.savefig(file_path)
            print(f"Gantt chart saved to {file_path}")

        plt.show()


# Round Robin Scheduler
class RoundRobinScheduler(Scheduler):
    def __init__(self, time_quantum):
        super().__init__()
        self.time_quantum = time_quantum
        self.patient_queue = []

    def add_patient(self, patient):
        self.patient_queue.append(patient)

    def schedule(self):
        gantt_chart = []

        while self.patient_queue:
            patient = self.patient_queue.pop(0)
            execution_time = min(patient.remaining_time, self.time_quantum)
            gantt_chart.append((self.current_time, patient.patient_id, execution_time))

            self.current_time += execution_time
            patient.remaining_time -= execution_time

            for p in self.patient_queue:
                p.wait_time += execution_time

            if patient.remaining_time > 0:
                self.patient_queue.append(patient)
            else:
                patient.completion_time = self.current_time
                patient.turnaround_time = patient.completion_time - patient.arrival_time
                patient.wait_time = patient.turnaround_time - patient.treatment_time
                self.completed_patients.append(patient)

        self.gantt_chart = gantt_chart
        self.visualize_gantt_chart("Round Robin Scheduler", gantt_chart, "round_robin_gantt_chart.png")

    def clear(self):
        super().clear()
        self.patient_queue = []


# Priority Scheduler
class PriorityScheduler(Scheduler):
    def __init__(self, preemptive=False):
        super().__init__()
        self.patients = []
        self.preemptive = preemptive

    def add_patient(self, patient):
        self.patients.append(patient)

    def schedule(self):
        gantt_chart = []

        while self.patients:
            if self.preemptive:
                self.patients.sort(key=lambda p: (p.priority, p.arrival_time))
            else:
                self.patients.sort(key=lambda p: p.priority)

            patient = self.patients.pop(0)
            execution_time = 1 if self.preemptive and patient.remaining_time > 1 else patient.remaining_time
            gantt_chart.append((self.current_time, patient.patient_id, execution_time))

            self.current_time += execution_time
            patient.remaining_time -= execution_time

            if patient.remaining_time > 0 and self.preemptive:
                self.patients.append(patient)
            else:
                patient.completion_time = self.current_time
                patient.turnaround_time = patient.completion_time - patient.arrival_time
                patient.wait_time = patient.turnaround_time - patient.treatment_time
                self.completed_patients.append(patient)

        title = "Preemptive Priority Scheduler" if self.preemptive else "Priority Scheduler"
        self.gantt_chart = gantt_chart
        self.visualize_gantt_chart(title, gantt_chart, f"{title.lower().replace(' ', '_')}.png")

    def clear(self):
        super().clear()
        self.patients = []


# Shortest Job First Scheduler
class ShortestJobFirstScheduler(Scheduler):
    def __init__(self, preemptive=False):
        super().__init__()
        self.patients = []
        self.preemptive = preemptive

    def add_patient(self, patient):
        self.patients.append(patient)

    def schedule(self):
        gantt_chart = []

        while self.patients:
            if self.preemptive:
                self.patients.sort(key=lambda p: (p.remaining_time, p.arrival_time))
            else:
                self.patients.sort(key=lambda p: p.treatment_time)

            patient = self.patients.pop(0)
            execution_time = 1 if self.preemptive and patient.remaining_time > 1 else patient.remaining_time
            gantt_chart.append((self.current_time, patient.patient_id, execution_time))

            self.current_time += execution_time
            patient.remaining_time -= execution_time

            if patient.remaining_time > 0 and self.preemptive:
                self.patients.append(patient)
            else:
                patient.completion_time = self.current_time
                patient.turnaround_time = patient.completion_time - patient.arrival_time
                patient.wait_time = patient.turnaround_time - patient.treatment_time
                self.completed_patients.append(patient)

        title = "Preemptive SJF Scheduler" if self.preemptive else "SJF Scheduler"
        self.visualize_gantt_chart(title, gantt_chart, f"{title.lower().replace(' ', '_')}.png")

    def clear(self):
        super().clear()
        self.patients = []


# First Come First Serve Scheduler
class FirstComeFirstServeScheduler(Scheduler):
    def __init__(self):
        super().__init__()
        self.patients = []

    def add_patient(self, patient):
        self.patients.append(patient)

    def schedule(self):
        gantt_chart = []
        self.patients.sort(key=lambda p: p.arrival_time)

        for patient in self.patients:
            if self.current_time < patient.arrival_time:
                self.current_time = patient.arrival_time

            patient.wait_time = self.current_time - patient.arrival_time
            gantt_chart.append((self.current_time, patient.patient_id, patient.treatment_time))

            self.current_time += patient.treatment_time
            patient.completion_time = self.current_time
            patient.turnaround_time = self.current_time - patient.arrival_time
            patient.wait_time = patient.turnaround_time - patient.treatment_time
            self.completed_patients.append(patient)

        self.gantt_chart = gantt_chart
        self.visualize_gantt_chart("First Come First Serve Scheduler", gantt_chart, "fcfs_gantt_chart.png")

    def clear(self):
        super().clear()
        self.patients = []

class MultiLevelQueueScheduler(Scheduler):
    def __init__(self, levels):
        super().__init__()
        self.queues = [level[0] for level in levels]
        self.time_quantums = [level[1] for level in levels]  
        self.queue_patients = [[] for _ in levels] 
    def add_patient(self, patient):
      
        queue_index = min(max(patient.priority - 1, 0), len(self.queues) - 1)
        self.queue_patients[queue_index].append(patient)

    def schedule(self):
        gantt_chart = []

        while any(self.queue_patients):
            for i, queue in enumerate(self.queues):
                if not self.queue_patients[i]:
                    continue

                for patient in self.queue_patients[i]:
                    queue.add_patient(patient)

                self.queue_patients[i] = []  

                if self.time_quantums[i]:  
                    start_time = self.current_time
                    quantum = self.time_quantums[i]
                    queue.current_time = start_time

                    while quantum > 0 and queue.patient_queue:
                        patient = queue.patient_queue.pop(0)
                        execution_time = min(patient.remaining_time, quantum)
                        gantt_chart.append((self.current_time, patient.patient_id, execution_time))

                        self.current_time += execution_time
                        patient.remaining_time -= execution_time
                        quantum -= execution_time

                        if patient.remaining_time > 0:
                            queue.patient_queue.append(patient)
                        else:
                            patient.completion_time = self.current_time
                            patient.turnaround_time = patient.completion_time - patient.arrival_time
                            patient.wait_time = patient.turnaround_time - patient.treatment_time
                            self.completed_patients.append(patient)
                else:  
                    queue.schedule()
                    gantt_chart += [
                        (start, pid, duration)
                        for start, pid, duration in getattr(queue, "gantt_chart", [])
                    ]
                    self.current_time = max(self.current_time, getattr(queue, "current_time", 0))

                queue.clear()

     
        self.visualize_gantt_chart(
            "Multi-Level Queue Scheduler", gantt_chart, "multi_level_queue_gantt_chart.png"
        )

    def clear(self):
        super().clear()
        self.queue_patients = [[] for _ in self.queues]
