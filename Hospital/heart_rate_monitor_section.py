import customtkinter
import threading
import csv
import time
from tkinter import messagebox
from heartRate import simulate_heart_rate

def create_heartRate_section(content_frame):
    def load_patients():
        show_frame(table_frame)
        hide_frame(search_frame)

        try:
            with open("Patient_Data.csv", mode="r", encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file)

                headers = next(csv_reader)
                for col_index, header in enumerate(headers):
                    header_label = customtkinter.CTkLabel(table_frame, text=header, font=("Arial", 12, "bold"))
                    header_label.grid(row=0, column=col_index, padx=5, pady=5, sticky="w")

                for row_index, row in enumerate(csv_reader, start=1):
                    for col_index, value in enumerate(row):
                        value_label = customtkinter.CTkLabel(table_frame, text=value, font=("Arial", 10))
                        value_label.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="w")

            doctor_info_label.configure(text="Loaded Successfully!")
        except Exception as e:
            doctor_info_label.configure(text="Error: Failed to load data.")
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
        finally:
            doctor_info_label.pack(side="bottom", pady=10)

    def show_search():
        show_frame(search_frame)
        hide_frame(table_frame)
        doctor_info_label.configure(text="")

    def search_patient():
        first_name = first_name_entry.get().strip().lower()
        last_name = last_name_entry.get().strip().lower()

        try:
            with open("Patient_Data.csv", mode="r", encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file)
                headers = next(csv_reader)

                for row in csv_reader:
                    csv_first_name = row[1].strip().lower()
                    csv_last_name = row[2].strip().lower()

                    if (
                        (not first_name or csv_first_name == first_name) and
                        (not last_name or csv_last_name == last_name)
                    ):
                        result_label.configure(
                            text=f"Found:\nPatient ID: {row[0]}\nName: {row[1]}\nSurname: {row[2]}\n"
                                 f"Age: {row[3]}\nGender: {row[4]}\nThreshold Low: {row[5]}\nThreshold High: {row[6]}"
                        )
                        add_submenu_buttons(row)
                        return

                result_label.configure(text="No matching patient found.")
                clear_submenu_buttons()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while searching: {str(e)}")

    def add_submenu_buttons(patient_data):
        #Adds submenu buttons and aligns them horizontally
        clear_submenu_buttons()

        submenu_frame = customtkinter.CTkFrame(search_frame)
        submenu_frame.pack(pady=10, padx=35, fill="x")

        # Show Current Heart Rate Butonu
        heart_rate_button = customtkinter.CTkButton(
            submenu_frame, text="Show Current Heart Rate",
            command=lambda: start_heart_rate_monitor(patient_data)
        )
        heart_rate_button.pack(side="left", padx=35, pady=5)
        submenu_buttons.append(heart_rate_button)

        # Display Abnormalities Butonu
        abnormalities_button = customtkinter.CTkButton(
            submenu_frame, text="Display Abnormalities",
            command=lambda: display_abnormalities(patient_data)
        )
        abnormalities_button.pack(side="left", padx=10, pady=5)
        submenu_buttons.append(abnormalities_button)

    def start_heart_rate_monitor(patient_data):
        #Starts the heart rate monitor
        if hasattr(start_heart_rate_monitor, "monitor_frame"):
            start_heart_rate_monitor.monitor_frame.pack_forget()

        monitor_frame = customtkinter.CTkFrame(search_frame)
        monitor_frame.pack(pady=20, padx=20, fill="x")
        start_heart_rate_monitor.monitor_frame = monitor_frame

        monitor_label = customtkinter.CTkLabel(monitor_frame, text="Heart Rate: Initializing...", font=("Arial", 14))
        monitor_label.pack(pady=10)

        alert_label = customtkinter.CTkLabel(monitor_frame, text="", font=("Arial", 14, "bold"), fg_color="red")
        alert_label.pack(pady=10)
        alert_label.pack_forget()

        stop_event = threading.Event()

        def stop_monitor():
            stop_event.set()
            monitor_frame.pack_forget()

        stop_button = customtkinter.CTkButton(monitor_frame, text="Stop", command=stop_monitor)
        stop_button.pack(pady=10)

        def update_heart_rate(heart_rate, range_type, is_abnormal, range_info):
            #Updates the heart rate and status
            if is_abnormal:
                monitor_label.configure(text=f"Heart Rate: {heart_rate} bpm ({range_type}) [Abnormal]", fg_color="red")
                start_alert_signal(alert_label, "ALERT: Immediate intervention required!")
            else:
                monitor_label.configure(text=f"Heart Rate: {heart_rate} bpm ({range_type})", fg_color="green")
                stop_alert_signal(alert_label)

        def start_alert_signal(label, message):
            #Starts the blinking alert signal
            def blink():
                while not stop_event.is_set():
                    label.configure(text=message) 
                    label.pack()
                    time.sleep(0.5)
                    label.pack_forget()
                    time.sleep(0.5)

            threading.Thread(target=blink, daemon=True).start()

        def stop_alert_signal(label):
            #Stops the blinking alert signal
            label.pack_forget()
            label.configure(text="") 

        def monitor_task():
            patient_info = {
                "id": patient_data[0],
                "name": patient_data[1],
                "surname": patient_data[2],
                "gender": patient_data[4],
                "thresholdLow": int(patient_data[5]),
                "thresholdHigh": int(patient_data[6])
            }
            simulate_heart_rate(patient_info, update_heart_rate, stop_event)

        threading.Thread(target=monitor_task, daemon=True).start()
        
    def display_abnormalities(patient_data):
        #Displays abnormalities for the specified patient
        try:
            with open("abnormalHeart.csv", mode="r", encoding="utf-8") as file:
                csv_reader = csv.DictReader(file)
                
                abnormalities = []
                for row in csv_reader:
                    if row["Patient ID"] == patient_data[0]: 
                        abnormalities.append(
                            f"Timestamp: {row['Timestamp']}\n"
                            f"Measured Range: {row['Measured Range']}\n"
                            f"Measured Value: {row['Measured Value']}\n\n"
                        )
                        
                if abnormalities:
                    messagebox.showinfo(
                        "Abnormalities",
                        f"Abnormal Data Found for Patient ID {patient_data[0]}:\n\n" + "".join(abnormalities) 
                    )
                else:
                    messagebox.showinfo("Abnormalities", "No abnormalities found for this patient.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Abnormalities file not found.")
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

    scrollable_frame = customtkinter.CTkScrollableFrame(content_frame, label_text="HeartRate Monitor")
    scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

    button_frame = customtkinter.CTkFrame(scrollable_frame)
    button_frame.pack(pady=10, padx=35, fill="x")

    loadAllPatientsData = customtkinter.CTkButton(button_frame, text="Display All Current Patient Information", command=load_patients)
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

    doctor_info_label = customtkinter.CTkLabel(scrollable_frame, text="")
    doctor_info_label.pack(side="bottom", pady=10)

    submenu_buttons = []

