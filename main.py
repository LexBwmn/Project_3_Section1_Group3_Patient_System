import customtkinter
from tkinter import messagebox
from new_patient import create_new_patient_form
from doctor_section import create_doctor_section
from patient_section import create_patient_section
from nurse_section import create_nurse_section
from bed_position_section import create_bed_section
from bed_temperature_section import create_bed_section_temperature
from glucose_section import create_glucose_section
from oxygen_section import create_oxygen_section
from heart_rate_monitor_section import heart_rate_monitor, showSubMenu  # Importing functions from heart_rate_monitor_section
from BW_PM import create_section_BWPM


# Tema ayarları
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

# Ana pencereyi oluşturma
root = customtkinter.CTk()
root.title("Hospital Management System")
root.geometry("800x600")

# Sağ kısım için içerik alanı
content_frame = customtkinter.CTkFrame(root)
content_frame.pack(side="right", fill="both", expand=True)

def show_content(content):
    for widget in content_frame.winfo_children():
        widget.destroy()
    if content == "New Patient Register":
        create_new_patient_form(content_frame)
    elif content == "Doctor":
        create_doctor_section(content_frame)
    elif content == "Patient":
        create_patient_section(content_frame)
    elif content == "Nurse":
        create_nurse_section(content_frame)
    elif content == "Heart Rate Monitor":
        heart_rate_monitor(content_frame)  # Heart Rate Monitor bölümünü çağırıyoruz
        showSubMenu(content_frame)  # Alt menüyü ekliyoruz
    elif content == "Bed Position Monitor":
        create_bed_section(content_frame)
    elif content == "Bed Temperature Monitor":
        create_bed_section_temperature(content_frame)
    elif content == "Glucose Level Monitor":
        create_glucose_section(content_frame)
    elif content == "Oxygen Saturation Monitor":
        create_oxygen_section(content_frame)
    elif content == "Body Weight and Pressure Monitor":
        create_section_BWPM(content_frame)
    else:
        label = customtkinter.CTkLabel(content_frame, text=f"{content} Content", font=("Arial", 20))
        label.pack(pady=20)

# Sol kısım için menü alanı
menu_frame = customtkinter.CTkFrame(root, fg_color="#2E8B57")
menu_frame.pack(side="left", fill="y")

# Menü butonları
menu_buttons = [
    {"name": "New Patient Register", "command": lambda: show_content("New Patient Register")},
    {"name": "Doctor", "command": lambda: show_content("Doctor")},
    {"name": "Patient", "command": lambda: show_content("Patient")},
    {"name": "Nurse", "command": lambda: show_content("Nurse")},
    {"name": "Heart Rate Monitor", "command": lambda: show_content("Heart Rate Monitor")},
    {"name": "Medicine Monitoring", "command": lambda: show_content("Medicine Monitoring")},
    {"name": "Blood Pressure Monitoring", "command": lambda: show_content("Blood Pressure Monitoring")},
    {"name": "Bed Position Monitor", "command": lambda: show_content("Bed Position Monitor")},
    {"name": "Body Weight and Pressure Monitor", "command": lambda: show_content("Body Weight and Pressure Monitor")},
    {"name": "Glucose Level Monitor", "command": lambda: show_content("Glucose Level Monitor")},
    {"name": "Oxygen Saturation Monitor", "command": lambda: show_content("Oxygen Saturation Monitor")},
    {"name": "Bed Temperature Monitor", "command": lambda: show_content("Bed Temperature Monitor")},
]

# Menü butonlarını oluştur ve sol tarafa ekle
for button_info in menu_buttons:
    menu_button = customtkinter.CTkButton(
        menu_frame,
        text=button_info["name"],
        command=button_info["command"],
        fg_color="#2E8B57",
        hover_color="#3CB371",
        text_color="white",
        anchor="w",
        height=35,
        corner_radius=5,
        width=200
    )
    menu_button.pack(pady=2, padx=3, fill="x")

# Pencereyi açık tutan döngü
root.mainloop()

