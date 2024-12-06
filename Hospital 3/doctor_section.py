import customtkinter
import openpyxl
from tkinter import messagebox

def create_doctor_section(content_frame):
    def load_doctors():
        try:
            #Load data from the file
            workbook = openpyxl.load_workbook("Doctors.xlsx")
            sheet = workbook.active  #Select the first sheet
            
            #Add table headers
            headers = [cell.value for cell in sheet[1]]  
            for col_index, header in enumerate(headers):
                header_label = customtkinter.CTkLabel(table_frame, text=header, font=("Arial", 12, "bold"))
                header_label.grid(row=0, column=col_index, padx=5, pady=5, sticky="w")
            
            #Add data to the table
            for row_index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=1):  # İlk satırı atla
                for col_index, value in enumerate(row):
                    value_label = customtkinter.CTkLabel(table_frame, text=value, font=("Arial", 10))
                    value_label.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="w")
            
            doctor_info_label.configure(text="Doctors Loaded Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load doctors: {str(e)}")

    #Interface for the doctor list
    scrollable_frame = customtkinter.CTkScrollableFrame(content_frame, label_text="Doctor List")
    scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

    #Frame for the table
    table_frame = customtkinter.CTkFrame(scrollable_frame)
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    #Button to load doctors
    load_button = customtkinter.CTkButton(scrollable_frame, text="Load Doctors", command=load_doctors)
    load_button.pack(pady=10)

    #Label for doctor information
    doctor_info_label = customtkinter.CTkLabel(scrollable_frame, text="Doctor Details will appear here.")
    doctor_info_label.pack(pady=10)