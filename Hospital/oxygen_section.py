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

def create_oxygen_section(content_frame):
    """Function to load beds and add buttons to the screen."""
    def load_oxygen():
        # Create first button
        button1 = customtkinter.CTkButton(
            content_frame,
            text="Start Oxygen Flow",
            command=lambda: trigger_alert_o("Start o Selected"),
            fg_color="#2E8B57",
            hover_color="#3CB371",
            text_color="white",
            height=35,
            corner_radius=5,
            width=200
        )
        button1.pack(pady=10, padx=20, fill="x")  # Add the button to the frame

        # Create second button
        button2 = customtkinter.CTkButton(
            content_frame,
            text="Stop Oxygen Flow",
            command=lambda: trigger_alert_o("Stop o Selected"),
            fg_color="#2E8B57",
            hover_color="#3CB371",
            text_color="white",
            height=35,
            corner_radius=5,
            width=200
        )
        button2.pack(pady=10, padx=20, fill="x")  # Add the button to the frame

    def trigger_alert_o(selection):
        """Checks a condition and triggers an alert."""
        if selection == "Start o Selected":  # Example condition
            create_alert(content_frame, "Start condition triggered!")
        elif selection == "Stop o Selected":  # Example condition
            create_alert(content_frame, "Stop condition triggered!")

    # Call the load_beds function to add buttons when the section is created
    load_oxygen()