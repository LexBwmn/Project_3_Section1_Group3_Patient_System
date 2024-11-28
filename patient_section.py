import customtkinter
import openpyxl
from tkinter import messagebox

def create_patient_section(content_frame):
    def search_patient():
        # Kullanıcıdan alınan arama kriterlerini al
        first_name = first_name_entry.get().strip()
        last_name = last_name_entry.get().strip()
        phone = phone_entry.get().strip()

        try:
            # Excel dosyasını yükle
            file_name = "Patient_Records.xlsx"
            workbook = openpyxl.load_workbook(file_name)
            sheet = workbook.active

            # Eşleşen kayıtları arama
            for row in sheet.iter_rows(min_row=2, values_only=True):  # İlk satır başlık olduğu için atlanır
                if (
                    (not first_name or row[0] == first_name) and
                    (not last_name or row[1] == last_name) and
                    (not phone or row[7] == phone)
                ):
                    # Sonuç bulundu
                    result_label.configure(
                        text=f"Found:\nFirst Name: {row[0]}\nLast Name: {row[1]}\nGender: {row[2]}\n"
                             f"Address: {row[3]}, {row[4]}, {row[5]}, {row[6]}\nPhone: {row[7]}\n"
                             f"Social Security: {row[8]}\nDate of Birth: {row[9]}\nAge: {row[10]}\n"
                             f"Family Doctor: {row[11]}\nEmergency Contact: {row[12]} ({row[13]})"
                    )
                    return

            # Hiçbir sonuç bulunamazsa
            result_label.configure(text="No matching patient found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while searching: {str(e)}")

    # Scrollable Frame
    scrollable_frame = customtkinter.CTkScrollableFrame(content_frame, label_text="Search Patient")
    scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    scrollable_frame.columnconfigure(1, weight=1)

    # Arama Kriterleri
    first_name_label = customtkinter.CTkLabel(scrollable_frame, text="First Name:")
    first_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    first_name_entry = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter First Name")
    first_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    last_name_label = customtkinter.CTkLabel(scrollable_frame, text="Last Name:")
    last_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    last_name_entry = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter Last Name")
    last_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    phone_label = customtkinter.CTkLabel(scrollable_frame, text="Phone Number:")
    phone_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    phone_entry = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter Phone Number")
    phone_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Arama Butonu
    search_button = customtkinter.CTkButton(scrollable_frame, text="Search Patient", command=search_patient)
    search_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Sonuç Alanı
    result_label = customtkinter.CTkLabel(scrollable_frame, text="Patient details will appear here.", wraplength=400)
    result_label.grid(row=4, column=0, columnspan=2, pady=10)