class Patient:
    def __init__(self, patient_id, treatment_time, priority, doctor, department, arrival_time):
        self.patient_id = str(patient_id)  
        self.treatment_time = int(treatment_time)  
        self.priority = int(priority)  
        self.doctor = doctor
        self.department = department
        self.arrival_time = int(arrival_time) 
        self.remaining_time = self.treatment_time  
        self.wait_time = 0  
        self.turnaround_time = 0  
        self.completion_time = 0 
