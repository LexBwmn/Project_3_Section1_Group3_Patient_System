import customtkinter
from tkinter import messagebox, PhotoImage
import subprocess  # Required to run main.py

# Create the login screen
def login_screen():
    def signin():
        # Function to handle the sign-in process
        username = user.get()
        password = code.get()

        if username == 'admin' and password == "12345":
            # If credentials are correct, close the login screen and run main.py
            login_window.destroy()  
            try:
                # Run the main.py file
                subprocess.run(['python', 'main.py'], check=True)
            except Exception as e:
                # Show an error message if main.py fails to run
                messagebox.showerror("Error", f"Failed to launch main.py: {str(e)}")
        else:
            # Show an error message for invalid credentials
            messagebox.showerror("Invalid", "Invalid username or password!")

    # Initialize the login window
    login_window = customtkinter.CTk()
    login_window.title('Login')
    login_window.geometry('800x600')
    customtkinter.set_appearance_mode("light")  # Set the light theme
    customtkinter.set_default_color_theme("blue")  # Set the default color theme
    login_window.resizable(False, False)  # Prevent resizing of the window

    # Main frame (contains the logo on the left and the login form on the right)
    main_frame = customtkinter.CTkFrame(login_window, fg_color="white")  # White background
    main_frame.pack(fill="both", expand=True)

    # Left frame (for the logo)
    left_frame = customtkinter.CTkFrame(main_frame, fg_color="white", width=300)
    left_frame.pack(side="left", fill="y", padx=20, pady=20)

    # Right frame (for login fields)
    right_frame = customtkinter.CTkFrame(main_frame, fg_color="white")
    right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # Heading for the login form
    heading = customtkinter.CTkLabel(
        right_frame, text='Sign In', 
        font=('Microsoft YaHei UI Light', 24, 'bold'), 
        fg_color="white", text_color="black"
    )
    heading.pack(pady=20)

    # Username input field
    user = customtkinter.CTkEntry(
        right_frame, placeholder_text="Username", 
        fg_color="white", text_color="black"
    )
    user.pack(pady=10)

    # Password input field
    code = customtkinter.CTkEntry(
        right_frame, placeholder_text="Password", 
        show="*", fg_color="white", text_color="black"
    )
    code.pack(pady=10)

    # Sign In button
    signin_button = customtkinter.CTkButton(right_frame, text="Sign In", command=signin)
    signin_button.pack(pady=20)

    # Start the main loop
    login_window.mainloop()

