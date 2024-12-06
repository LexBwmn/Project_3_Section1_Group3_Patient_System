import customtkinter
import openpyxl
from tkinter import messagebox

def create_nurse_section(content_frame):
    def load_nurses():
        try:
            #Load the Excel file
            workbook = openpyxl.load_workbook("Nurses.xlsx")
            sheet = workbook.active  #Select the first sheet
            
            #Display headers
            headers = [cell.value for cell in sheet[1]] 
            for col_index, header in enumerate(headers):
                header_label = customtkinter.CTkLabel(table_frame, text=header, font=("Arial", 12, "bold"))
                header_label.grid(row=0, column=col_index, padx=5, pady=5, sticky="w")
            
            #Add data to the table
            for row_index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=1):
                for col_index, value in enumerate(row):
                    value_label = customtkinter.CTkLabel(table_frame, text=value, font=("Arial", 10))
                    value_label.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="w")
            
            nurse_info_label.configure(text="Nurses Loaded Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load nurses: {str(e)}")

    #Interface for nurse list
    scrollable_frame = customtkinter.CTkScrollableFrame(content_frame, label_text="Nurse List")
    scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

    #Table frame
    table_frame = customtkinter.CTkFrame(scrollable_frame)
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    #Button to load nurses
    load_button = customtkinter.CTkButton(scrollable_frame, text="Load Nurses", command=load_nurses)
    load_button.pack(pady=10)

    #Label for nurse information
    nurse_info_label = customtkinter.CTkLabel(scrollable_frame, text="Nurse Details will appear here.")
    nurse_info_label.pack(pady=10)