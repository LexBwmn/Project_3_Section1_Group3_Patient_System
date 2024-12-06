import customtkinter
from tkinter import messagebox
from new_patient import create_new_patient_form
from doctor_section import create_doctor_section
from patient_section import create_patient_section
from nurse_section import create_nurse_section
from bed_temperature_section import BedTemperatureApp, BedTemperatureMonitorExtended
from glucose_section import GlucoseLevelMonitorApp, GlucoseLevelMonitorExtended
from oxygen_section import OxygenSaturationMonitorApp, OxygenSaturationMonitoringDeviceExtended
from heart_rate_monitor_section import create_heartRate_section
from medication_control_monitor_section import create_medication_section  # Added import for medication section
from BW_PM import BodyWeightPressureMonitorExtended, GUIApp 
from BP import BloodPressureApp

# Theme settings
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

# Main screen
root = customtkinter.CTk()
root.title("Hospital Management System")
root.geometry("800x600")

# Right side
content_frame = customtkinter.CTkFrame(root)
content_frame.pack(side="right", fill="both", expand=True)

def show_content(content):
    for widget in content_frame.winfo_children():
        widget.destroy()  # Clear content

    if content == "New Patient Register":
        create_new_patient_form(content_frame)
    elif content == "Doctor":
        create_doctor_section(content_frame)
    elif content == "Patient":
        create_patient_section(content_frame)
    elif content == "Nurse":
        create_nurse_section(content_frame)
    elif content == "Heart Rate Monitor":
        create_heartRate_section(content_frame)
    elif content == "Bed Temperature Monitor":
        monitor = BedTemperatureMonitorExtended() # Create the monitor instance
        monitor.load_threshold_data("C:/Users/navje/OneDrive - Conestoga College/Desktop/PROJECTWORK/Project_3_Section1_Group3_Patient_System/Bed_Temperature.csv")
        monitor.load_patient_data("Patient_Dat.csv")  # Load the patient data (example)
        app = BedTemperatureApp(content_frame, monitor) # Initialize the GUI app with the monitor
    elif content == "Glucose Level Monitor":
        monitor = GlucoseLevelMonitorExtended()  # Create an instance of the monitor class
        monitor.load_patient_data("Patient_Dat.csv")  # Load the patient data
        app = GlucoseLevelMonitorApp(content_frame, monitor)  # Initialize the GUI app for Glucose Level Monitor
    elif content == "Oxygen Saturation Monitor":
        monitor = OxygenSaturationMonitoringDeviceExtended()  # Create an instance of the monitor class
        monitor.load_patient_data("Patient_Dat.csv")  # Load the patient data
        app = OxygenSaturationMonitorApp(content_frame, monitor)
    elif content == "Body Weight and Pressure Monitor":
        monitor = BodyWeightPressureMonitorExtended()  # Create the monitor instance
        monitor.loadThresholdData("BodyWeight.csv")  # Load the threshold data (example)
        monitor.loadPatientData("Patient_Dat.csv")  # Load the patient data (example)
        app = GUIApp(content_frame, monitor)  # Initialize the GUI app with the monitor
    elif content == "Medicine Monitoring":  # New case for Medicine Monitoring
        create_medication_section(content_frame)
    elif content == "Blood Pressure Monitoring":
        application = BloodPressureApp(content_frame)
    else:
        label = customtkinter.CTkLabel(content_frame, text=f"{content} Content", font=("Arial", 20))
        label.pack(pady=20)

# Left side menu
menu_frame = customtkinter.CTkFrame(root, fg_color="#2E8B57")
menu_frame.pack(side="left", fill="y")

# Menu buttons
menu_buttons = [
    {"name": "New Patient Register", "command": lambda: show_content("New Patient Register")},
    {"name": "Doctor", "command": lambda: show_content("Doctor")},
    {"name": "Patient", "command": lambda: show_content("Patient")},
    {"name": "Nurse", "command": lambda: show_content("Nurse")},
    {"name": "Heart Rate Monitor", "command": lambda: show_content("Heart Rate Monitor")},
    {"name": "Medicine Monitoring", "command": lambda: show_content("Medicine Monitoring")},  # Added button for Medicine Monitoring
    {"name": "Blood Pressure Monitoring", "command": lambda: show_content("Blood Pressure Monitoring")},
    {"name": "Body Weight and Pressure Monitor", "command": lambda: show_content("Body Weight and Pressure Monitor")},
    {"name": "Glucose Level Monitor", "command": lambda: show_content("Glucose Level Monitor")},
    {"name": "Oxygen Saturation Monitor", "command": lambda: show_content("Oxygen Saturation Monitor")},
    {"name": "Bed Temperature Monitor", "command": lambda: show_content("Bed Temperature Monitor")},
]

# Create menu buttons and add to left side
for button_info in menu_buttons:
    menu_button = customtkinter.CTkButton(
        menu_frame,
        text=button_info["name"],
        command=button_info["command"],
        fg_color="#2E8B57",
        hover_color="#3CB371",
        text_color="white",
        anchor="w",
        height=35,
        corner_radius=5,
        width=200
    )
    menu_button.pack(pady=2, padx=3, fill="x")

# Window is open
root.mainloop()