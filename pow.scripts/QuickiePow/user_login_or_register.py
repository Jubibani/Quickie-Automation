import tkinter as tk
from tkinter import messagebox
import subprocess
import csv
import os

user_csv = 'C:\\Quickie-Automation\\pow.scripts\\QuickiePow\\modules\\auto\\login_sites\\login_user\\user.csv'
file_path = 'C:\\Quickie-Automation\\pow.scripts\\QuickiePow\\modules\\auto\\login_sites\\login_user\\login_for_sites\\login_for_sites.csv'

# Define functions for registration and login for the user
def register_user(username, password):
    # Check if the file exists
    file_exists = os.path.isfile(user_csv)

    # Open the file in append mode
    with open(user_csv, mode='a', newline='') as file:
        writer = csv.writer(file)

        # If the file does not exist or is empty, write the header
        if not file_exists or os.stat(user_csv).st_size == 0:
            writer.writerow(['Username', 'Password'])

        # Write the user data
        writer.writerow([username, password])

    messagebox.showinfo("Success", "User registered successfully!")

def is_user_registered(username, file=user_csv):
    try:
        with open(file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Username'] == username:
                    return True
        return False
    except FileNotFoundError:
        return False

def is_any_user_registered():
    try:
        with open(user_csv, mode='r') as file:
            reader = csv.DictReader(file)
            for _ in reader:
                return True
        return False
    except FileNotFoundError:
        return False

def check_user_credentials(username, password):
    try:
        with open(user_csv, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Username'] == username and row['Password'] == password:
                    return True
        return False
    except FileNotFoundError:
        return False

# Function to store site login data
def store_site_login_data(email, email_password, file_path):
    # Check if the file exists
    file_exists = os.path.isfile(file_path)

    # Open the file in append mode  
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        # If the file does not exist or is empty, write the header
        if not file_exists or os.stat(file_path).st_size == 0:
            writer.writerow(['email', 'email_password'])

        # Write the user data
        writer.writerow([email, email_password])

    print("Site login data stored successfully!")

# Function to validate and register user to the site
def register_to_site():
    global entry_email, entry_email_password, email_login_window  # Declare as global to use these variables
    email = entry_email.get()
    email_password = entry_email_password.get()

    # Basic validation
    if not email or not email_password:
        messagebox.showerror("Error", "All fields are required!")
    else:
        # Check if the email is already registered
        if is_user_registered(email, file_path):
            messagebox.showinfo("Info", "Email already registered!")
        else:
            store_site_login_data(email, email_password, file_path)
            messagebox.showinfo("Success", "Site login credentials registered successfully!")
            email_login_window.destroy()
        entry_email.delete(0, tk.END)
        entry_email_password.delete(0, tk.END)

# Function to open login form
def open_login_form():
    login_window = tk.Toplevel(root)
    login_window.title("Login Form")

    tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=5)
    entry_email = tk.Entry(login_window)
    entry_email.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=5)

    def login():
        username = entry_email.get()
        password = entry_password.get()
        if check_user_credentials(username, password):
            messagebox.showinfo("Success", "Login successful!")
            find_quickielog_and_run_script("quickieLog.py")
            login_window.destroy()  # Close login window
        else:
            messagebox.showerror("Error", "Invalid email or password!")

    tk.Button(login_window, text="Login", command=login).grid(row=2, columnspan=2, pady=10)

# Function to open registration form
def open_registration_form():
    if is_any_user_registered():
        messagebox.showinfo("Existing User Found", "Currently, the program can only accept one local user.")
        return

    registration_window = tk.Toplevel(root)
    registration_window.title("Registration Form")

    tk.Label(registration_window, text="Username:").grid(row=0, column=0, padx=10, pady=5)
    entry_username = tk.Entry(registration_window)
    entry_username.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    entry_password = tk.Entry(registration_window, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=5)

    # Add a label indicating that login details will be saved locally
    tk.Label(registration_window, text="Login details will be saved locally.").grid(row=2, columnspan=2, pady=10)

    def register():
        username = entry_username.get()
        password = entry_password.get()
        if is_user_registered(username):
            messagebox.showinfo("Existing User Found", "Currently, the program can only accept one local user.")
        else:
            register_user(username, password)
            open_email_login_window()
            registration_window.destroy()  # Close registration window

    tk.Button(registration_window, text="Register", command=register).grid(row=3, columnspan=2, pady=10)

# Function to open about window
def open_about_window():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    tk.Label(about_window, text="Quickie Automation is a program developed by Jubibani that is programmed to automate the login to your sites (currently: UC canvas) with the credentials that is saved locally.").pack(padx=20, pady=20)
    tk.Button(about_window, text="Close", command=about_window.destroy).pack(pady=10)

# Function to open email login window
def open_email_login_window():
    global entry_email, entry_email_password, email_login_window  # Declare as global to use these variables
    # Create main window for site registration
    email_login_window = tk.Toplevel(root)
    email_login_window.title("Email Login Form")

    # Create and place the labels and entry widgets for site registration
    tk.Label(email_login_window, text="UC email:").grid(row=0, column=0, padx=10, pady=5)
    entry_email = tk.Entry(email_login_window)
    entry_email.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(email_login_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    entry_email_password = tk.Entry(email_login_window, show="*")
    entry_email_password.grid(row=1, column=1, padx=10, pady=5)

    # Create and place the register button for site registration
    tk.Button(email_login_window, text="Register to UC", command=register_to_site).grid(row=3, columnspan=2, pady=10)

# Function to handle both registration and email login
def open_registration_and_email_login():
    open_registration_form()
    # open_email_login_window()

# Define the function to find and run a script
def find_quickielog_and_run_script(filename): #!! Login Bridge
    # Iterate over all directories and subdirectories
    for root_dir, dirs, files in os.walk("C:\\Quickie-Automation"):
        # Check if the target file is found in the current directory
        if filename in files:
            # Construct the full path to the script
            script_path = os.path.join(root_dir, filename)
            # Run the script as a separate process
            subprocess.Popen(["python", script_path])

# Initialize main Tkinter window
root = tk.Tk()
root.title("Homepage")
root.iconbitmap("C:\\Quickie-Automation\\pow.scripts\\QuickiePow\\logo\\logoAppIco.ico")
root.geometry("800x600")  # Set the window size

# Center frame to hold buttons
center_frame = tk.Frame(root)
center_frame.place(relx=0.5, rely=0.5, anchor='center')

# Main homepage buttons
tk.Button(center_frame, text="Login", command=open_login_form).pack(pady=10)
tk.Button(center_frame, text="Register", command=open_registration_and_email_login).pack(pady=10)
tk.Button(center_frame, text="About", command=open_about_window).pack(pady=10)

# Start the Tkinter event loop
root.mainloop()