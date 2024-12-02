import customtkinter
import threading
import csv
from tkinter import messagebox, Toplevel
import tkinter as tk
import time

class MedicationMonitor:
    #Piston Animation for Medication Monitoring
    def __init__(self, root, medication_name):
        self.root = root
        self.canvas = tk.Canvas(root, width=300, height=200, bg="white")
        self.canvas.pack(pady=20)

        self.canvas.create_text(150, 20, text=f"Monitoring: {medication_name}", font=("Arial", 16, "bold"))

        self.piston1 = self.canvas.create_rectangle(50, 50, 100, 100, fill="green")
        self.piston2 = self.canvas.create_rectangle(200, 100, 250, 150, fill="blue")
        self.text_status = self.canvas.create_text(150, 180, text="Status: Normal", fill="green", font=("Arial", 14, "bold"))

        self.is_abnormal = False
        self.running = True

    def update_status(self, status):
        #Updates status text and piston colors
        if status == "normal":
            self.is_abnormal = False
            self.canvas.itemconfig(self.text_status, text="Status: Normal", fill="green")
            self.canvas.itemconfig(self.piston1, fill="green")
            self.canvas.itemconfig(self.piston2, fill="blue")
        else:
            self.is_abnormal = True
            self.canvas.itemconfig(self.text_status, text="Status: Abnormal", fill="red")
            self.canvas.itemconfig(self.piston1, fill="red")
            self.canvas.itemconfig(self.piston2, fill="orange")

    def animate(self):
        #Handles piston movement
        direction = 1
        while self.running:
            self.canvas.move(self.piston1, 0, direction * 5)
            coords1 = self.canvas.coords(self.piston1)
            if coords1[1] <= 50 or coords1[3] >= 150:
                direction *= -1

            self.canvas.move(self.piston2, 0, -direction * 5)
            self.root.update()
            time.sleep(0.1)

    def stop(self):
        #Stops animation
        self.running = False

def create_medication_section(content_frame):
    def load_patients():
        show_frame(table_frame)
        hide_frame(search_frame)

        try:
            with open("medicationData.csv", mode="r", encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file)

                headers = next(csv_reader)
                for col_index, header in enumerate(headers):
                    header_label = customtkinter.CTkLabel(table_frame, text=header, font=("Arial", 12, "bold"))
                    header_label.grid(row=0, column=col_index, padx=5, pady=5, sticky="w")

                for row_index, row in enumerate(csv_reader, start=1):
                    for col_index, value in enumerate(row):
                        value_label = customtkinter.CTkLabel(table_frame, text=value, font=("Arial", 10))
                        value_label.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="w")

            info_label.configure(text="Loaded Successfully!")
        except Exception as e:
            info_label.configure(text="Error: Failed to load data.")
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
        finally:
            info_label.pack(side="bottom", pady=10)

    def show_search():
        show_frame(search_frame)
        hide_frame(table_frame)
        info_label.configure(text="")

    def search_patient():
        #Searches for all patients matching the name and surname
        first_name = first_name_entry.get().strip().lower()
        last_name = last_name_entry.get().strip().lower()

        try:
            with open("medicationData.csv", mode="r", encoding="utf-8") as csv_file:
                csv_reader = csv.DictReader(csv_file)

                matching_records = []
                medications = []

                for row in csv_reader:
                    csv_first_name = row.get("name", "").strip().lower()
                    csv_last_name = row.get("surname", "").strip().lower()

                    if (not first_name or csv_first_name == first_name) and \
                       (not last_name or csv_last_name == last_name):
                        matching_records.append(row)
                        medications.append(row.get("medication", "Unknown"))

                if matching_records:
                    patient_info = matching_records[0]  
                    result_label.configure(
                        text=f"Found Patient:\nPatient ID: {patient_info.get('patientID', 'Unknown')}\n"
                             f"Name: {patient_info.get('name', 'Unknown')}\n"
                             f"Surname: {patient_info.get('surname', 'Unknown')}\n"
                             f"Age: {patient_info.get('age', 'Unknown')}\n"
                             f"Gender: {patient_info.get('gender', 'Unknown')}\n"
                    )
                    add_submenu_buttons(medications, patient_info) 
                else:
                    result_label.configure(text="No matching patient found.")
                    clear_submenu_buttons()

        except FileNotFoundError:
            messagebox.showerror("Error", "The file medicationData.csv was not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while searching: {str(e)}")

    def add_submenu_buttons(medications, patient_info):
        clear_submenu_buttons()

        submenu_frame = customtkinter.CTkFrame(search_frame)
        submenu_frame.pack(pady=10, padx=35, fill="x")

        for medication in medications:
            #Create a button for each medication
            medication_button = customtkinter.CTkButton(
                submenu_frame,
                text=f"{medication}",
                command=lambda med=medication: display_monitor(med)
            )
            medication_button.pack(pady=5, padx=10, fill="x")
            submenu_buttons.append(medication_button)

        #Add a single button to show abnormalities for the current patient
        abnormalities_button = customtkinter.CTkButton(
            submenu_frame,
            text=f"Show Abnormalities for {patient_info.get('name', 'Unknown')}",
            command=lambda: show_abnormalities(patient_info)
        )
        abnormalities_button.pack(pady=5, padx=10, fill="x")
        submenu_buttons.append(abnormalities_button)

    def display_monitor(medication_name):
        #Displays the medication monitor for a specific medication
        monitor_window = Toplevel()
        monitor_window.title(f"Monitoring: {medication_name}")

        monitor = MedicationMonitor(monitor_window, medication_name)

        def simulate_status():
            statuses = ["normal", "abnormal", "normal"]
            for status in statuses:
                time.sleep(5)
                monitor.update_status(status)

        threading.Thread(target=monitor.animate, daemon=True).start()
        threading.Thread(target=simulate_status, daemon=True).start()

    def show_abnormalities(patient_info):
        #Displays the abnormalities for a specific patient
        try:
            abnormalities = display_abnormalities("abnormalMedicine.csv", patient_info.get("patientID"))
            if abnormalities:
                abnormalities_text = "\n".join(abnormalities)
                messagebox.showinfo(
                    "Abnormalities",
                    f"Abnormal Data Found for Patient {patient_info.get('name')} (ID: {patient_info.get('patientID')}):\n\n" + abnormalities_text
                )
            else:
                messagebox.showinfo("Abnormalities", f"No abnormalities found for Patient {patient_info.get('name')}.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_submenu_buttons():
        for button in submenu_buttons:
            button.pack_forget()
        submenu_buttons.clear()

    def show_frame(frame):
        frame.pack(pady=10, padx=20, fill="both", expand=True)

    def hide_frame(frame):
        frame.pack_forget()

    #Main content frame
    scrollable_frame = customtkinter.CTkScrollableFrame(content_frame, label_text="Medication Control Monitor")
    scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

    #Top button frame
    button_frame = customtkinter.CTkFrame(scrollable_frame)
    button_frame.pack(pady=10, padx=35, fill="x")

    loadAllPatientsData = customtkinter.CTkButton(button_frame, text="Display All Patient Information", command=load_patients)
    loadAllPatientsData.pack(side="left", padx=10, pady=5)

    accessSpecificData = customtkinter.CTkButton(button_frame, text="Access Specific Patient Data", command=show_search)
    accessSpecificData.pack(side="right", padx=10, pady=5)

    table_frame = customtkinter.CTkFrame(scrollable_frame)
    search_frame = customtkinter.CTkFrame(scrollable_frame)

    first_name_label = customtkinter.CTkLabel(search_frame, text="First Name:")
    first_name_label.pack(pady=5, anchor="w")
    first_name_entry = customtkinter.CTkEntry(search_frame, placeholder_text="Enter First Name")
    first_name_entry.pack(pady=5, fill="x")

    last_name_label = customtkinter.CTkLabel(search_frame, text="Last Name:")
    last_name_label.pack(pady=5, anchor="w")
    last_name_entry = customtkinter.CTkEntry(search_frame, placeholder_text="Enter Last Name")
    last_name_entry.pack(pady=5, fill="x")

    search_button = customtkinter.CTkButton(search_frame, text="Search Patient", command=search_patient)
    search_button.pack(pady=10)

    result_label = customtkinter.CTkLabel(search_frame, text="Patient details will appear here.", wraplength=400)
    result_label.pack(pady=10)

    info_label = customtkinter.CTkLabel(scrollable_frame, text="")
    info_label.pack(side="bottom", pady=10)

    submenu_buttons = []


def display_abnormalities(filename, patient_id):
    #Displays abnormalities from the CSV file
    abnormalities = []
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row["Patient ID"] == str(patient_id):
                    abnormalities.append(
                        f"Medication: {row['Medication']}, Time: {row['Time']}, Issue: {row['Issue']}"
                    )
    except FileNotFoundError:
        print("Error: File not found.")
    return abnormalities