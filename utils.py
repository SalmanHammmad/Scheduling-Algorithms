import os
import json
from patient import Patient


def ensure_records_folder():
    """Ensure that the 'records' folder exists."""
    if not os.path.exists("records"):
        os.makedirs("records")


def load_patient_data(file_name):
    """Load patient data from a JSON file."""
    patients = []
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            for entry in data:
                try:
                    patients.append(
                        Patient(
                            patient_id=entry["patient_id"],
                            treatment_time=int(entry["treatment_time"]),
                            priority=int(entry["priority"]),
                            doctor=entry["doctor"],
                            department=entry["department"],
                            arrival_time=int(entry["arrival_time"])
                        )
                    )
                except (ValueError, KeyError) as e:
                    print(f"Skipping invalid patient entry: {entry} ({e})")
        print(f"{len(patients)} patients successfully loaded.")
        if len(patients) < len(data):
            print(f"Warning: {len(data) - len(patients)} entries were skipped due to invalid data.")
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from file '{file_name}'.")
    return patients


def save_results(patients, file_name="results.json"):
    """Save scheduling results to a JSON file in the 'records' folder."""
    ensure_records_folder()  

    file_name = os.path.basename(file_name)  
    file_path = os.path.join("records", file_name)

    try:
        data = [
            {
                "patient_id": p.patient_id,
                "wait_time": p.wait_time,
                "completion_time": p.completion_time,
                "turnaround_time": p.turnaround_time,
            }
            for p in patients
        ]
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Results saved successfully to {file_path}")
    except Exception as e:
        print(f"Error saving results: {e}")
