import customtkinter
import openpyxl
from tkinter import Label, Toplevel, messagebox
from Modules import OxygenSaturationMonitoringDevice, OxygenSaturationController
import random

class OxygenSaturationMonitorApp:
    def __init__(self, root, monitor):
        self.monitor = monitor  # Instance of OxygenSaturationMonitoringDevice
        self.root = root
        self.content_frame = customtkinter.CTkFrame(root, width=400, height=300, corner_radius=10)
        self.content_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title label
        self.title_label = customtkinter.CTkLabel(
            self.content_frame,
            text="Oxygen Saturation Monitor",
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

        # Oxygen Flow Control buttons
        self.button_start_oxygen = customtkinter.CTkButton(
            self.content_frame,
            text="Start Oxygen Flow",
            command=lambda: self.start_oxygen_flow(),
            fg_color="#2E8B57",
            hover_color="#3CB371",
            text_color="white",
            height=35,
            corner_radius=5,
            width=200
        )
        self.button_start_oxygen.pack(pady=10, padx=20, fill="x")

        self.button_stop_oxygen = customtkinter.CTkButton(
            self.content_frame,
            text="Stop Oxygen Flow",
            command=lambda: self.stop_oxygen_flow(),
            fg_color="#D9534F",
            hover_color="#C9302C",
            text_color="white",
            height=35,
            corner_radius=5,
            width=200
        )
        self.button_stop_oxygen.pack(pady=10, padx=20, fill="x")

        # Status label to display messages below buttons
        self.status_label = Label(self.content_frame, text="", bg="white", fg="black", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def start_monitoring(self):
        """Triggers monitoring of random patient data."""
        self.monitor.monitor_patient_data(self.display_alert)

    def display_alert(self, alert_message):
        """Displays an alert in the GUI."""
        create_alert(content_frame=self.content_frame, alert_message=alert_message)

    def start_oxygen_flow(self):
        """Start oxygen flow."""
        oxygen_controller = OxygenSaturationController()
        oxygen_controller.adjust_oxygen_flow(True)  # Start oxygen flow
        self.status_label.config(text="Oxygen flow started.")  # Update GUI message

    def stop_oxygen_flow(self):
        """Stop oxygen flow."""
        oxygen_controller = OxygenSaturationController()
        oxygen_controller.adjust_oxygen_flow(False)  # Stop oxygen flow
        self.status_label.config(text="Oxygen flow stopped.")  # Update GUI message

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


# Extend OxygenSaturationMonitoringDevice class
class OxygenSaturationMonitoringDeviceExtended(OxygenSaturationMonitoringDevice):
    def monitor_patient_data(self, display_alert_callback):
        if not self.patients:
            display_alert_callback("No patient data available to monitor.")
            return

        # Simulate random patient monitoring
        random_index = random.randint(0, len(self.patients) - 1)
        random_patient = self.patients[random_index]

        if random_patient.oxygenSaturation < self.oxygenSaturationLowerThreshold:
            alert_message = (f"ALERT: Patient ID {random_patient.id} in Room {random_patient.roomNumber} "
                             f"\nhas oxygen saturation below threshold! \nOxygen Saturation: {random_patient.oxygenSaturation}% \nThreshold range: "
                            f"{self.oxygenSaturationLowerThreshold}% - {self.oxygenSaturationUpperThreshold}%)\n")
            display_alert_callback(alert_message)
        elif random_patient.oxygenSaturation > self.oxygenSaturationUpperThreshold:
            alert_message = (f"ALERT: Patient ID {random_patient.id} in Room {random_patient.roomNumber} "
                             f"\nhas oxygen saturation above threshold! \nOxygen Saturation: {random_patient.oxygenSaturation}%\nThreshold range: "
                            f"{self.oxygenSaturationLowerThreshold}% - {self.oxygenSaturationUpperThreshold}%)\n")
            display_alert_callback(alert_message)
        else:
            display_alert_callback(f"Patient ID {random_patient.id} in Room {random_patient.roomNumber} "
                                    f"\nhas oxygen saturation within acceptable limits.")


if __name__ == "__main__":
    # Create a monitor object and load data
    monitor = OxygenSaturationMonitoringDeviceExtended()
    monitor.load_patient_data("Patient_Dat.csv")  # Make sure the CSV exists

    # Create the GUI application
    root = customtkinter.CTk()
    root.title("Oxygen Saturation Monitoring System")
    root.geometry("500x400")

    app = OxygenSaturationMonitorApp(root, monitor)
    root.mainloop()