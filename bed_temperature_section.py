import customtkinter
import openpyxl
from tkinter import Label, Toplevel, messagebox
from Modules import BedTemperatureMonitor
import random

# Define the GUIApp class
class BedTemperatureApp:
    def __init__(self, root, monitor):
        self.monitor = monitor  # Instance of BedTemperatureMonitor
        self.root = root
        self.content_frame = customtkinter.CTkFrame(root, width=400, height=300, corner_radius=10)
        self.content_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title label
        self.title_label = customtkinter.CTkLabel(
            self.content_frame,
            text="Bed Temperature Monitor",
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

        def on_slider_change(slider_value, slider_label, bed_type=None):
            """Updates the label with the current slider value and checks for alerts."""
            slider_label.configure(text=f"{slider_value:.1f}°C")
            self.update_status(f"Bed temperature changed to {slider_value:.1f}°C")

        # Fowler bed temperature section
        I_label = customtkinter.CTkLabel(
            self.content_frame, text="Change Bed Temperature", font=("Arial", 14)
        )
        I_label.pack(pady=10)

        I_slider_label = customtkinter.CTkLabel(self.content_frame, text="36.0°C")
        I_slider_label.pack()

        I_slider = customtkinter.CTkSlider(
            self.content_frame,
            from_=30.0,
            to=40.0,
            number_of_steps=100,
            command=lambda value: on_slider_change(value, I_slider_label)
        )
        I_slider.set(36.0)  # Set default value for the Fowler bed
        I_slider.pack(pady=10, padx=20, fill="x")


        # Status label to display messages
        self.status_label = Label(self.content_frame, text="", bg="white", fg="black", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def start_monitoring(self):
        """Triggers monitoring of random patient data."""
        self.monitor.monitor_random_patient_data(self.display_alert)

    def display_alert(self, alert_message):
        """Displays an alert in the GUI."""
        create_alert(self.content_frame, alert_message)
    
    def update_status(self, message):
        """Updates the status label with the message."""
        self.status_label.config(text=message)


# Function to create an alert popup
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

def create_alert(content_frame, alert_message, bed_type=None):
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

# Extend the BedTemperatureMonitor class
class BedTemperatureMonitorExtended(BedTemperatureMonitor):
    def monitor_random_patient_data(self, display_alert_callback):
        if not self.patients:
            print("No patient data available to monitor.")
            return

        # Select a random patient
        random_index = random.randint(0, len(self.patients) - 1)
        random_patient = self.patients[random_index]

        print(f"Monitoring bed temperature for Patient ID {random_patient.id} in Room {random_patient.roomNumber}...")

        threshold_exceeded = False
        matched_threshold = False

        # Iterate through the threshold data to find a match
        for threshold in self.thresholds:
            if random_patient.age == threshold.ageGroup and random_patient.disease == threshold.disease:
                matched_threshold = True

                # Check if temperature is outside the acceptable range
                if random_patient.temperature < threshold.minimumTemperature:
                    alert_message = (f"ALERT: Patient ID {random_patient.id} \n"
                                    f"has low temperature ({random_patient.temperature}).\n"
                                    f"Action required.\n"
                                    f"Normal Range: {threshold.minimumTemperature} - {threshold.maximumTemperature}")
                    display_alert_callback(alert_message)  # Show alert in GUI
                    break
                elif random_patient.temperature > threshold.maximumTemperature:
                    alert_message = (f"ALERT: Patient ID {random_patient.id} \n"
                                    f"has high temperature ({random_patient.temperature}).\n"
                                    f"Action required.\n"
                                    f"Normal Range: {threshold.minimumTemperature} - {threshold.maximumTemperature}")
                    display_alert_callback(alert_message)  # Show alert in GUI
                    break
                else:
                   display_alert_callback(f"Patient ID {random_patient.id} in Room {random_patient.roomNumber}\n is within safe limits.")

        if not matched_threshold:
            print(f"No matching threshold found for Patient ID {random_patient.id}.")

if __name__ == "__main__":
    monitor = BedTemperatureMonitorExtended()
    monitor.load_threshold_data("Bed_Temperature.csv")
    monitor.load_patient_data("Patient_data.csv")

    root = customtkinter.CTk()
    root.title("Patient Monitoring System")
    root.geometry("500x400")

    app = BedTemperatureApp(root, monitor)
    root.mainloop()    