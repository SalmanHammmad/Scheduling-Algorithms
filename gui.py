import tkinter as tk
from tkinter import filedialog, messagebox
from utils import load_patient_data

def start_gui():
    def load_file():
        file_name = filedialog.askopenfilename(
            title="Select Patient Data File",
            filetypes=[("JSON Files", "*.json")],
        )
        if file_name:
            try:
                patients = load_patient_data(file_name)
                messagebox.showinfo("Success", f"{len(patients)} patients loaded!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {e}")

    root = tk.Tk()
    root.title("Patient Scheduling System")

    load_button = tk.Button(root, text="Load Patient Data", command=load_file)
    load_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
