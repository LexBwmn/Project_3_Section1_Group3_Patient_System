import customtkinter
import openpyxl
from tkinter import Label, Toplevel, messagebox
from Modules import BodyWeightPressureMonitor
import random

class GUIApp:
    def __init__(self, root, monitor):
        self.monitor = monitor  # Instance of BodyWeightPressureMonitor
        self.root = root
        self.content_frame = customtkinter.CTkFrame(root, width=400, height=300, corner_radius=10)
        self.content_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title label
        self.title_label = customtkinter.CTkLabel(
            self.content_frame,
            text="Body Weight and Pressure Monitor",
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

        # Bed position buttons
        self.button_fowler = customtkinter.CTkButton(
            self.content_frame,
            text="Fowler",
            command=lambda: self.change_bed_position("Fowler"),
            fg_color="#2E8B57",
            hover_color="#3CB371",
            text_color="white",
            height=35,
            corner_radius=5,
            width=200
        )
        self.button_fowler.pack(pady=10, padx=20, fill="x")

        self.button_supine = customtkinter.CTkButton(
            self.content_frame,
            text="Supine",
            command=lambda: self.change_bed_position("Supine"),
            fg_color="#2E8B57",
            hover_color="#3CB371",
            text_color="white",
            height=35,
            corner_radius=5,
            width=200
        )
        self.button_supine.pack(pady=10, padx=20, fill="x")

        # Status label to display messages below buttons
        self.status_label = Label(self.content_frame, text="", bg="white", fg="black", font=("Arial", 12))
        self.status_label.pack(pady=10)

    monitor = BodyWeightPressureMonitor

    def start_monitoring(self):
        """Triggers monitoring of random patient data."""
        self.monitor.monitorRandomPatientData(self.display_alert)

    def display_alert(self, alert_message):
        """Displays an alert in the GUI."""
        create_alert_BWPM(self.content_frame, alert_message)

    def change_bed_position(self, position):
        """Handles bed position change."""
        self.monitor.changeBedPosition(position)  # Perform backend action
        self.status_label.config(text=f"Bed position changed to {position}.")  # Update GUI message


def create_alert_BWPM(content_frame, alert_message):
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


# Extend the BodyWeightPressureMonitor class
class BodyWeightPressureMonitorExtended(BodyWeightPressureMonitor):
    def monitorRandomPatientData(self, display_alert_callback):
        if not self.patients:
            display_alert_callback("No patient data available to monitor.")
            return

        # Simulate random patient monitoring
        random_index = random.randint(0, len(self.patients) - 1)
        random_patient = self.patients[random_index]

        for threshold in self.thresholds:
            if (random_patient.age == threshold.age and
                random_patient.gender == threshold.gender and
                abs(random_patient.weight - threshold.weight) < self.WEIGHT_TOLERANCE):
                if random_patient.currentPressure > threshold.thresholdPressure:
                    alert_message = (f"ALERT: Patient ID {random_patient.id} in Room {random_patient.roomNumber}"
                                     f"\nexceeds the pressure threshold with \ncurrent pressure {random_patient.currentPressure} Pa.")
                    display_alert_callback(alert_message)
                    return
        display_alert_callback(f"Patient ID {random_patient.id} in Room {random_patient.roomNumber} is within safe limits.")


if __name__ == "__main__":
    monitor = BodyWeightPressureMonitorExtended()
    monitor.loadThresholdData("BodyWeight.csv")
    monitor.loadPatientData("Patient_Dat.csv")

    root = customtkinter.CTk()
    root.title("Patient Monitoring System")
    root.geometry("500x400")

    app = GUIApp(root, monitor)
    root.mainloop()