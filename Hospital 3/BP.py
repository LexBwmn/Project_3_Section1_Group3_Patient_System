import customtkinter
from tkinter import Toplevel, Label, messagebox
import random
import csv

# Blood Pressure Monitoring System Class
class BloodPressureMonitoring:
    class Range:
        def __init__(self, systolic_min, systolic_max, diastolic_min, diastolic_max):
            self.systolic_min = systolic_min
            self.systolic_max = systolic_max
            self.diastolic_min = diastolic_min
            self.diastolic_max = diastolic_max

    def __init__(self):
        self.normal_ranges = {}

    def generate_key(self, age, gender):
        return f"{age}_{gender.lower()}"

    def load_csv(self, csv_file):
        try:
            with open(csv_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row if present
                for row in reader:
                    age, gender, systolic_min, systolic_max, diastolic_min, diastolic_max = row
                    key = self.generate_key(int(age), gender)
                    self.normal_ranges[key] = self.Range(
                        int(systolic_min), int(systolic_max), int(diastolic_min), int(diastolic_max)
                    )
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def is_blood_pressure_normal(self, systolic, diastolic, age, gender):
        key = self.generate_key(age, gender)
        if key not in self.normal_ranges:
            return False

        range_data = self.normal_ranges[key]
        return (range_data.systolic_min <= systolic <= range_data.systolic_max and
                range_data.diastolic_min <= diastolic <= range_data.diastolic_max)

    def evaluate_patient_status(self, systolic, diastolic):
        if systolic < 90 or diastolic < 60:
            return "Low"
        elif systolic <= 120 and diastolic <= 80:
            return "Normal"
        elif systolic <= 139 or diastolic <= 89:
            return "Slightly High"
        else:
            return "High"

    def generate_report_bp(self, systolic, diastolic, age, gender):
        normal = self.is_blood_pressure_normal(systolic, diastolic, age, gender)
        status = self.evaluate_patient_status(systolic, diastolic)
        return f"Systolic: {systolic}, Diastolic: {diastolic}\nAge: {age}, Gender: {gender}\nNormal Range: {'Yes' if normal else 'No'}\nStatus: {status}"

# Create Blood Pressure App GUI
class BloodPressureApp:
    def __init__(self, parent):
        self.parent = parent
      
        self.systolic_label = customtkinter.CTkLabel(self.parent, text="Systolic:")
        self.systolic_label.pack(pady=5)
        self.systolic_entry = customtkinter.CTkEntry(self.parent)
        self.systolic_entry.pack(pady=5)

        self.diastolic_label = customtkinter.CTkLabel(self.parent, text="Diastolic:")
        self.diastolic_label.pack(pady=5)
        self.diastolic_entry = customtkinter.CTkEntry(self.parent)
        self.diastolic_entry.pack(pady=5)

        self.age_label = customtkinter.CTkLabel(self.parent, text="Age:")
        self.age_label.pack(pady=5)
        self.age_entry = customtkinter.CTkEntry(self.parent)
        self.age_entry.pack(pady=5)

        self.gender_label = customtkinter.CTkLabel(self.parent, text="Gender (Male/Female):")
        self.gender_label.pack(pady=5)
        self.gender_entry = customtkinter.CTkEntry(self.parent)
        self.gender_entry.pack(pady=5)

        # Start Monitoring button
        self.start_monitor_button = customtkinter.CTkButton(
            self.parent,
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

        # Alert Buttons for Blood Pressure
        self.button_alert_low = customtkinter.CTkButton(
            self.parent,
            text="Alert for Low BP",
            command=self.alert_low_bp,
            fg_color="#D9534F",
            hover_color="#C9302C",
            text_color="white",
            height=35,
            corner_radius=5,
            width=200
        )
        self.button_alert_low.pack(pady=10, padx=20, fill="x")

        self.button_alert_high = customtkinter.CTkButton(
            self.parent,
            text="Alert for High BP",
            command=self.alert_high_bp,
            fg_color="#FF5733",
            hover_color="#C9302C",
            text_color="white",
            height=35,
            corner_radius=5,
            width=200
        )
        self.button_alert_high.pack(pady=10, padx=20, fill="x")

        # Status label to display messages
        self.status_label = customtkinter.CTkLabel(self.parent, text="", wraplength=350)
        self.status_label.pack(pady=10)

        # Initialize Blood Pressure Monitoring
        self.monitoring_system = BloodPressureMonitoring()
        self.monitoring_system.load_csv("blood_pressure_ranges.csv")

    def start_monitoring(self):
        """Triggers blood pressure monitoring of random patient data."""
        try:
            systolic = int(self.systolic_entry.get())
            diastolic = int(self.diastolic_entry.get())
            age = int(self.age_entry.get())
            gender = self.gender_entry.get().lower()

            # Generate the report based on the inputs
            report = self.monitoring_system.generate_report_bp(systolic, diastolic, age, gender)
            self.status_label.configure(text=report)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid values for systolic, diastolic, age, and gender.")

    def alert_low_bp(self):
        """Displays an alert for low blood pressure."""
        self.status_label.config(text="Low BP alert triggered!")
        alert_message = "ALERT: Blood pressure is too low! Immediate action required."
        create_alert(self.parent, alert_message)

    def alert_high_bp(self):
        """Displays an alert for high blood pressure."""
        self.status_label.config(text="High BP alert triggered!")
        alert_message = "ALERT: Blood pressure is too high! Immediate action required."
        create_alert(self.parent, alert_message)


# Function to create alert windows
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


# Main application window
if __name__ == "__main__":
    root = customtkinter.CTk()
    root.title("Blood Pressure Monitoring System")
    root.geometry("500x400")

    app = BloodPressureApp(root)
    root.mainloop()
