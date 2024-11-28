import customtkinter
import openpyxl
from openpyxl import Workbook
from tkinter import messagebox
import os

# NEW PATIENT REGISTER
def create_new_patient_form(content_frame):
    def enter_data():
        # Formdan alınan bilgileri kontrol et
        accepted = accept_var.get()
        if accepted == "Accepted":
            firstname = first_name_entry.get()
            lastname = last_name_entry.get()
            if firstname and lastname:
                # Diğer bilgileri oku
                gender = gender_combobox.get()
                address = address_entry.get()
                city = city_entry.get()
                state = state_entry.get()
                zip_code = zip_code_entry.get()
                phone = phone_entry.get()
                social_security = social_security_entry.get()
                dob = dob_entry.get()
                age = age_entry.get()
                family_doctor = family_doctor_entry.get()
                emergency_contact = emergency_contact_entry.get()
                relationship = relationship_entry.get()

                # Excel dosyasına yazdır
                file_name = "Patient_Records.xlsx"
                if not os.path.exists(file_name):  # Eğer dosya yoksa başlıklarla yeni bir dosya oluştur
                    workbook = Workbook()
                    sheet = workbook.active
                    sheet.title = "Patients"
                    sheet.append([
                        "First Name", "Last Name", "Gender", "Address", "City", 
                        "State", "Zip Code", "Phone", "Social Security", 
                        "Date of Birth", "Age", "Family Doctor", 
                        "Emergency Contact", "Relationship"
                    ])
                    workbook.save(file_name)

                # Mevcut dosyaya verileri ekle
                workbook = openpyxl.load_workbook(file_name)
                sheet = workbook.active
                sheet.append([
                    firstname, lastname, gender, address, city, state, zip_code, 
                    phone, social_security, dob, age, family_doctor, 
                    emergency_contact, relationship
                ])
                workbook.save(file_name)

                messagebox.showinfo("Success", "Patient data saved successfully!")
                # Formu temizle
                first_name_entry.delete(0, "end")
                last_name_entry.delete(0, "end")
                gender_combobox.set("")
                address_entry.delete(0, "end")
                city_entry.delete(0, "end")
                state_entry.delete(0, "end")
                zip_code_entry.delete(0, "end")
                phone_entry.delete(0, "end")
                social_security_entry.delete(0, "end")
                dob_entry.delete(0, "end")
                age_entry.delete(0, "end")
                family_doctor_entry.delete(0, "end")
                emergency_contact_entry.delete(0, "end")
                relationship_entry.delete(0, "end")
            else:
                messagebox.showwarning("Error", "First name and last name are required.")
        else:
            messagebox.showwarning("Error", "You have not accepted the terms.")

    # Scrollable Frame
    scrollable_frame = customtkinter.CTkScrollableFrame(content_frame, label_text="New Patient Register")
    scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    scrollable_frame.columnconfigure(1, weight=1)

    # Form Alanları
    first_name_label = customtkinter.CTkLabel(scrollable_frame, text="First Name:")
    first_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    first_name_entry = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter First Name")
    first_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    last_name_label = customtkinter.CTkLabel(scrollable_frame, text="Last Name:")
    last_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    last_name_entry = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter Last Name")
    last_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    gender_label = customtkinter.CTkLabel(scrollable_frame, text="Gender:")
    gender_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    gender_combobox = customtkinter.CTkComboBox(scrollable_frame, values=["", "Male", "Female"])
    gender_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    address_label = customtkinter.CTkLabel(scrollable_frame, text="Address:")
    address_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    address_entry = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter Address")
    address_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    city_label = customtkinter.CTkLabel(scrollable_frame, text="City:")
    city_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    city_entry = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter City")
    city_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    state_label = customtkinter.CTkLabel(scrollable_frame, text="State:")
    state_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    state_entry = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter State")
    state_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

    zip_code_label = customtkinter.CTkLabel(scrollable_frame, text="Zip Code:")
    zip_code_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
    zip_code_entry = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter Zip Code")
    zip_code_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

    phone_label = customtkinter.CTkLabel(scrollable_frame, text="Phone#:")
    phone_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
    phone_entry = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter Phone#")
    phone_entry.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

    social_security_label = customtkinter.CTkLabel(scrollable_frame, text="Social Security:")
    social_security_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
    social_security_entry = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter SSN")
    social_security_entry.grid(row=8, column=1, padx=10, pady=5, sticky="ew")

    dob_label = customtkinter.CTkLabel(scrollable_frame, text="Date of Birth:")
    dob_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")
    dob_entry = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter DOB")
    dob_entry.grid(row=9, column=1, padx=10, pady=5, sticky="ew")

    age_label = customtkinter.CTkLabel(scrollable_frame, text="Age:")
    age_label.grid(row=10, column=0, padx=10, pady=5, sticky="w")
    age_entry = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter Age")
    age_entry.grid(row=10, column=1, padx=10, pady=5, sticky="ew")

    family_doctor_label = customtkinter.CTkLabel(scrollable_frame, text="Family Doctor:")
    family_doctor_label.grid(row=11, column=0, padx=10, pady=5, sticky="w")
    family_doctor_entry = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter Family Doctor")
    family_doctor_entry.grid(row=11, column=1, padx=10, pady=5, sticky="ew")

    emergency_contact_label = customtkinter.CTkLabel(scrollable_frame, text="Emergency Contact:")
    emergency_contact_label.grid(row=12, column=0, padx=10, pady=5, sticky="w")
    emergency_contact_entry = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter Emergency Contact")
    emergency_contact_entry.grid(row=12, column=1, padx=10, pady=5, sticky="ew")

    relationship_label = customtkinter.CTkLabel(scrollable_frame, text="Relationship:")
    relationship_label.grid(row=13, column=0, padx=10, pady=5, sticky="w")
    relationship_entry = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter Relationship")
    relationship_entry.grid(row=13, column=1, padx=10, pady=5, sticky="ew")
    
    # Şartlar ve Gönder Butonu
    terms_frame = customtkinter.CTkFrame(scrollable_frame)
    terms_frame.grid(row=14, column=0, columnspan=2, pady=10, sticky="ew")

    accept_var = customtkinter.StringVar(value="Not Accepted")
    terms_check = customtkinter.CTkCheckBox(terms_frame, text="I accept the terms and conditions.",
                                            variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
    terms_check.pack(padx=10, pady=5)

    submit_button = customtkinter.CTkButton(scrollable_frame, text="Submit", command=enter_data)
    submit_button.grid(row=15, column=0, columnspan=2, pady=20)