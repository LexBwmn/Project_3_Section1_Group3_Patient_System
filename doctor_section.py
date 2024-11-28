import customtkinter
import openpyxl
from tkinter import messagebox

def create_doctor_section(content_frame):
    def load_doctors():
        try:
            # Excel dosyasını yükleme
            workbook = openpyxl.load_workbook("Doctors.xlsx")
            sheet = workbook.active  # İlk sayfayı seç
            
            # Başlıkları görüntüleme
            headers = [cell.value for cell in sheet[1]]  # İlk satırı başlık olarak al
            for col_index, header in enumerate(headers):
                header_label = customtkinter.CTkLabel(table_frame, text=header, font=("Arial", 12, "bold"))
                header_label.grid(row=0, column=col_index, padx=5, pady=5, sticky="w")
            
            # Verileri tabloya ekleme
            for row_index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=1):  # İlk satırı atla
                for col_index, value in enumerate(row):
                    value_label = customtkinter.CTkLabel(table_frame, text=value, font=("Arial", 10))
                    value_label.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="w")
            
            doctor_info_label.configure(text="Doctors Loaded Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load doctors: {str(e)}")

    # Doktor listesi için arayüz
    scrollable_frame = customtkinter.CTkScrollableFrame(content_frame, label_text="Doctor List")
    scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Tablo çerçevesi
    table_frame = customtkinter.CTkFrame(scrollable_frame)
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Doktorları yükleme düğmesi
    load_button = customtkinter.CTkButton(scrollable_frame, text="Load Doctors", command=load_doctors)
    load_button.pack(pady=10)

    # Doktor bilgisi
    doctor_info_label = customtkinter.CTkLabel(scrollable_frame, text="Doctor Details will appear here.")
    doctor_info_label.pack(pady=10)