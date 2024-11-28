import customtkinter
from tkinter import messagebox
import random

# Patient Data Read from CSV File
def read_patient_data_from_csv():
    patient_data = []
    try:
        patient_file = "patientData.csv"
        with open(patient_file, mode="r") as file:
            lines = file.readlines()[1:]  # Skip header
            for line in lines:
                parts = line.strip().split(",")
                patient = {
                    "patientID": int(parts[0]),
                    "age": int(parts[1]),
                    "gender": parts[2],
                    "thresholdLow": int(parts[3]),
                    "thresholdHigh": int(parts[4])
                }
                patient_data.append(patient)
        return patient_data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load patient data: {str(e)}")
        return []

# Function to display specific patient's data based on ID
def search_patient_by_id(content_frame, patient_data):
    def search_patient():
        patient_id = patient_id_entry.get()

        if patient_id.isdigit():
            patient_id = int(patient_id)
            found_patient = None
            for patient in patient_data:
                if patient['patientID'] == patient_id:
                    found_patient = patient
                    break

            if found_patient:
                patient_info_label.configure(text=f"Patient ID: {found_patient['patientID']}\n"
                                                 f"Age: {found_patient['age']}\n"
                                                 f"Gender: {found_patient['gender']}\n"
                                                 f"Threshold Low: {found_patient['thresholdLow']}\n"
                                                 f"Threshold High: {found_patient['thresholdHigh']}")
                showSubMenu(content_frame, found_patient)  # Show the submenu after displaying patient info
            else:
                messagebox.showwarning("Not Found", f"No patient found with ID {patient_id}")
        else:
            messagebox.showwarning("Invalid Input", "Please enter a valid patient ID.")

    # Creating the UI for Patient Search
    search_frame = customtkinter.CTkFrame(content_frame)
    search_frame.pack(pady=10, padx=20, fill="both", expand=True)

    patient_id_label = customtkinter.CTkLabel(search_frame, text="Enter Patient ID:")
    patient_id_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    patient_id_entry = customtkinter.CTkEntry(search_frame, placeholder_text="Enter Patient ID")
    patient_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    search_button = customtkinter.CTkButton(search_frame, text="Search", command=search_patient)
    search_button.grid(row=1, column=0, columnspan=2, pady=10)

    patient_info_label = customtkinter.CTkLabel(search_frame, text="Patient info will be displayed here.")
    patient_info_label.grid(row=2, column=0, columnspan=2, pady=10)

# Function to display the submenu
def showSubMenu(content_frame, patient):
    submenu_frame = customtkinter.CTkFrame(content_frame)
    submenu_frame.pack(pady=10, padx=20, fill="both", expand=True)

    submenu_label = customtkinter.CTkLabel(submenu_frame, text="Submenu Options:", font=("Arial", 16))
    submenu_label.grid(row=0, column=0, pady=5)

    def show_patient_info():
        patient_info_label.configure(text=f"Patient ID: {patient['patientID']}\n"
                                         f"Age: {patient['age']}\n"
                                         f"Gender: {patient['gender']}\n"
                                         f"Threshold Low: {patient['thresholdLow']}\n"
                                         f"Threshold High: {patient['thresholdHigh']}")

    def show_heart_rate():
        heart_rate, range_name = generate_heart_rate(patient)
        heart_rate_label.configure(text=f"Current Heart Rate: {heart_rate} bpm ({range_name})")
        # Call function to update heart rate continuously
        update_heart_rate(patient)

    def show_abnormalities():
        # Check if abnormalities exist
        abnormalities = check_abnormalities(patient)
        abnormalities_label.configure(text=abnormalities)

    options = [("Patient Information", show_patient_info),
               ("Show Current Heart Rate", show_heart_rate),
               ("Display Abnormalities", show_abnormalities)]  # Placeholder for "Return to Main Menu"

    # Adding buttons for submenu options
    row = 1
    for option_text, command in options:
        button = customtkinter.CTkButton(submenu_frame, text=option_text, command=command)
        button.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        row += 1

    # Labels for dynamic data display
    patient_info_label = customtkinter.CTkLabel(submenu_frame, text="Patient info will be displayed here.")
    patient_info_label.grid(row=row, column=0, padx=10, pady=10)
    heart_rate_label = customtkinter.CTkLabel(submenu_frame, text="Heart rate will be displayed here.")
    heart_rate_label.grid(row=row + 1, column=0, padx=10, pady=10)
    abnormalities_label = customtkinter.CTkLabel(submenu_frame, text="Abnormalities will be displayed here.")
    abnormalities_label.grid(row=row + 2, column=0, padx=10, pady=10)

    # Define the function to continuously update heart rate
    def update_heart_rate(patient):
        heart_rate, range_name = generate_heart_rate(patient)
        heart_rate_label.configure(text=f"Current Heart Rate: {heart_rate} bpm ({range_name})")
        submenu_frame.after(1000, update_heart_rate, patient)  # Update heart rate every 1 second

def generate_heart_rate(patient):
    """
    Generate a heart rate based on the patient's thresholds.
    Returns the heart rate and its range (Low, Normal, High).
    """
    range_type = random.choice(["Low", "Normal", "High"])
    if range_type == "Low":
        heart_rate = random.randint(patient['thresholdLow'] - 10, patient['thresholdLow'] - 1)
    elif range_type == "Normal":
        heart_rate = random.randint(patient['thresholdLow'], patient['thresholdHigh'])
    else:  # High
        heart_rate = random.randint(patient['thresholdHigh'] + 1, patient['thresholdHigh'] + 10)

    return heart_rate, range_type

def check_abnormalities(patient):
    """
    Check if the patient's heart rate is within the acceptable range.
    If it's out of bounds, return an alert message.
    """
    heart_rate, range_name = generate_heart_rate(patient)
    if range_name == "Low" or range_name == "High":
        return f"ALERT: Heart rate is out of normal range! Current Heart Rate: {heart_rate} bpm"
    else:
        return "Abnormalities: None detected."

# Main function to call heart rate monitor and display patient data
def heart_rate_monitor(content_frame):
    patient_data = read_patient_data_from_csv()

    search_patient_by_id(content_frame, patient_data)