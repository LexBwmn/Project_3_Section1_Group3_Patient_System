import customtkinter
import openpyxl
from tkinter import Toplevel, messagebox

def create_alert(content_frame, alert_message):
    """Creates a closable alert widget."""
    alert_window = Toplevel(content_frame)
    alert_window.title("Alert")
    alert_window.geometry("300x150")
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

def create_bed_section_temperature(content_frame):
    def on_slider_change(slider_value, slider_label, bed_type):
        """Updates the label with the current slider value and checks for alerts."""
        slider_label.configure(text=f"{slider_value:.1f}°C")
        create_alert(content_frame, slider_value, bed_type)  # Check if temperature is too high

    # 
    I_label = customtkinter.CTkLabel(
        content_frame, text="Increase Bed Temperature", font=("Arial", 14)
    )
    I_label.pack(pady=10)

    I_slider_label = customtkinter.CTkLabel(content_frame, text="36.0°C")
    I_slider_label.pack()

    I_slider = customtkinter.CTkSlider(
        content_frame,
        from_=30.0,
        to=40.0,
        number_of_steps=100,
        command=lambda value: on_slider_change(value, I_slider_label, "Fowler")
    )
    I_slider.set(36.0)  # Set default value for the Fowler bed
    I_slider.pack(pady=10, padx=20, fill="x")

    # Supine bed temperature section
    L_label = customtkinter.CTkLabel(
        content_frame, text="Lower Bed Temperature", font=("Arial", 14)
    )
    L_label.pack(pady=10)

    L_slider_label = customtkinter.CTkLabel(content_frame, text="36.0°C")
    L_slider_label.pack()

    L_slider = customtkinter.CTkSlider(
        content_frame,
        from_=30.0,
        to=40.0,
        number_of_steps=100,
        command=lambda value: on_slider_change(value, L_slider_label, "Supine")
    )
    L_slider.set(36.0)  # Set default values
    L_slider.pack(pady=10, padx=20, fill="x")
