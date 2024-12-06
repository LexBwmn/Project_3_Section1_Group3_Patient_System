import customtkinter
import openpyxl
from tkinter import Label, Toplevel, messagebox
from Modules import GlucoseLevelMonitor, GlucoseLevelController
import random

class GlucoseLevelMonitorApp:
    def __init__(self, root, monitor):
        self.monitor = monitor  # Instance of GlucoseLevelMonitor
        self.root = root
        self.content_frame = customtkinter.CTkFrame(root, width=400, height=300, corner_radius=10)
        self.content_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title label
        self.title_label = customtkinter.CTkLabel(
            self.content_frame,
            text="Glucose Level Monitor",
            text_color="black",
            font=("Arial", 18)
        )
        self.title_label.pack(pady=10)

        # Start Monitoring button
        self.start_monitor_button = customtkinter.CTkButton(
            self.content_frame,
            text="Start Monitoring",
            command=self.start_monitoring,
            fg_color="#007BFF",
            hover_color="#0056b3",
            text_color="white",
            height=40,
            corner_radius=5,
            width=200
        )
        self.start_monitor_button.pack(pady=10)

        # Alert Buttons for Glucose Flow
        self.button_start_glucose = customtkinter.CTkButton(
            self.content_frame,
            text="Start Glucose Flow",
            command=lambda: self.start_glucose_flow(),
            fg_color="#2E8B57",
            hover_color="#3CB371",
            text_color="white",
            height=35,
            corner_radius=5,
            width=200
        )
        self.button_start_glucose.pack(pady=10, padx=20, fill="x")

        self.button_stop_glucose = customtkinter.CTkButton(
            self.content_frame,
            text="Stop Glucose Flow",
            command=lambda: self.stop_glucose_flow(),
            fg_color="#D9534F",
            hover_color="#C9302C",
            text_color="white",
            height=35,
            corner_radius=5,
            width=200
        )
        self.button_stop_glucose.pack(pady=10, padx=20, fill="x")

        # Status label to display messages below buttons
        self.status_label = Label(self.content_frame, text="", bg="white", fg="black", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def start_monitoring(self):
        """Triggers glucose level monitoring of random patient data."""
        self.monitor.monitor_patient_data(self.display_alert)

    def display_alert(self, alert_message):
        """Displays an alert in the GUI."""
        create_alert(self.content_frame, alert_message)

    def start_glucose_flow(self):
        """Handles glucose flow adjustment."""
        glucose_controller = GlucoseLevelController()
        glucose_controller.adjust_glucose_flow(True)
        self.status_label.config(text="Glucose flow started")
    
    def stop_glucose_flow(self):
        """Handles glucose flow adjustment."""
        glucose_controller = GlucoseLevelController()
        glucose_controller.adjust_glucose_flow(False)
        self.status_label.config(text="Glucose flow stopped")

def create_alert(content_frame, alert_message):
    """Creates a closable alert widget."""
    alert_window = Toplevel(content_frame)
    alert_window.title("Alert")
    alert_window.geometry("400x250")
    alert_window.configure(bg="white")

    # Add a label with the alert message
    alert_label = customtkinter.CTkLabel(
        alert_window,
        text=alert_message,
        text_color="black",
        font=("Arial", 14)
    )
    alert_label.pack(pady=20)

    # Add a Close button to dismiss the alert
    close_button = customtkinter.CTkButton(
        alert_window,
        text="Close",
        command=alert_window.destroy,
        fg_color="#D9534F",
        hover_color="#C9302C",
        text_color="white",
        height=30,
        corner_radius=5,
        width=100
    )
    close_button.pack(pady=10)


# Extend the GlucoseLevelMonitor class for the GUI app
class GlucoseLevelMonitorExtended(GlucoseLevelMonitor):
    def monitor_patient_data(self, display_alert_callback):
        if not self.is_data_loaded():
            display_alert_callback("No patient data loaded.")
            return

        # Simulate random patient monitoring
        random_patient = random.choice(self.patients)

        if random_patient.glucoseLevel < self.glucose_level_lower_threshold:
            alert_message = (f"ALERT: Patient ID {random_patient.id} in Room {random_patient.roomNumber} "
                             f"\nhas a glucose level of {random_patient.glucoseLevel}, \nwhich is below the threshold!\n"
                             "Threshold range: "f"{self.glucose_level_lower_threshold} - {self.glucose_level_upper_threshold})\n")
            display_alert_callback(alert_message)
        elif random_patient.glucoseLevel > self.glucose_level_upper_threshold:
            alert_message = (f"ALERT: Patient ID {random_patient.id} in Room {random_patient.roomNumber} "
                             f"\nhas a glucose level of {random_patient.glucoseLevel}, \nwhich is above the threshold!\n"
                             "Threshold range: "f"{self.glucose_level_lower_threshold} - {self.glucose_level_upper_threshold})\n")
            display_alert_callback(alert_message)
        else:
            display_alert_callback(f"Patient ID {random_patient.id} in Room {random_patient.roomNumber} "
                                   f"\nhas a glucose level within acceptable limits.")

    

if __name__ == "__main__":
    monitor = GlucoseLevelMonitorExtended()
    monitor.load_patient_data("Patient_Dat.csv")

    root = customtkinter.CTk()
    root.title("Patient Glucose Monitoring System")
    root.geometry("500x400")

    app = GlucoseLevelMonitorApp(root, monitor)
    root.mainloop()