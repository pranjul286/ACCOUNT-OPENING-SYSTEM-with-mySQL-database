# main.py
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from PIL import Image, ImageTk
import database  # Our custom database module

class AccountOpeningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prime Bank - Account Opening System")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Initialize the database
        database.setup_database()

        # Load and set background
        self.bg_image = Image.open("images/background.jpg")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((800, 600), Image.LANCZOS))
        
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create the main welcome screen
        self.create_welcome_screen()

    def create_welcome_screen(self):
        """Creates the widgets for the main welcome screen."""
        # Load and display logo
        self.logo_image = Image.open("images/logo.png")
        self.logo_photo = ImageTk.PhotoImage(self.logo_image.resize((150, 150), Image.LANCZOS))
        
        logo_label = tk.Label(self.root, image=self.logo_photo, bg='#0d1b2a') # Match bg color for better look
        logo_label.pack(pady=50)

        # Main Title
        title_label = tk.Label(self.root, text="Welcome to Prime Bank", 
                               font=("Helvetica", 32, "bold"), fg="white", bg="#0d1b2a")
        title_label.pack(pady=20)
        
        # Sub Title
        subtitle_label = tk.Label(self.root, text="Your Trusted Financial Partner", 
                               font=("Helvetica", 16), fg="lightgray", bg="#0d1b2a")
        subtitle_label.pack(pady=10)

        # Button Frame
        button_frame = tk.Frame(self.root, bg="#0d1b2a")
        button_frame.pack(pady=50)

        # Main Buttons
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 14), padding=10)

        open_account_btn = ttk.Button(button_frame, text="Open New Account", 
                                     style="TButton", command=self.open_account_form)
        open_account_btn.grid(row=0, column=0, padx=20)

    def open_account_form(self):
        """Opens the Toplevel window for the account opening form."""
        self.form_window = Toplevel(self.root)
        self.form_window.title("New Customer Account Form")
        self.form_window.geometry("600x700")
        self.form_window.resizable(False, False)
        self.form_window.configure(bg="#f0f0f0")

        # Create a frame for the form
        form_frame = ttk.LabelFrame(self.form_window, text="Customer Details", padding=20)
        form_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # --- Form Widgets ---
        self.entries = {}
        fields = [
            ("Full Name", "full_name"), ("Gender", "gender"), ("Date of Birth (YYYY-MM-DD)", "dob"),
            ("Email Address", "email"), ("Phone Number", "phone_number"), ("Address", "address"),
            ("Account Type", "account_type"), ("Initial Deposit", "initial_deposit")
        ]

        for i, (text, key) in enumerate(fields):
            label = ttk.Label(form_frame, text=f"{text}:", font=("Helvetica", 12))
            label.grid(row=i, column=0, sticky="w", padx=5, pady=8)

            if key == "gender":
                self.entries[key] = ttk.Combobox(form_frame, values=["Male", "Female", "Other"], font=("Helvetica", 12))
                self.entries[key].grid(row=i, column=1, sticky="ew", padx=5, pady=8)
            elif key == "account_type":
                self.entries[key] = ttk.Combobox(form_frame, values=["Savings", "Current"], font=("Helvetica", 12))
                self.entries[key].grid(row=i, column=1, sticky="ew", padx=5, pady=8)
            else:
                self.entries[key] = ttk.Entry(form_frame, font=("Helvetica", 12))
                self.entries[key].grid(row=i, column=1, sticky="ew", padx=5, pady=8)

        # --- Action Buttons ---
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)

        submit_btn = ttk.Button(button_frame, text="Submit Application", command=self.submit_form)
        submit_btn.pack(side="left", padx=10)

        clear_btn = ttk.Button(button_frame, text="Clear Form", command=self.clear_form)
        clear_btn.pack(side="left", padx=10)

    def clear_form(self):
        """Clears all entry fields in the form."""
        for key in self.entries:
            if isinstance(self.entries[key], ttk.Combobox):
                self.entries[key].set('')
            else:
                self.entries[key].delete(0, tk.END)

    def submit_form(self):
        """Validates and submits the form data to the database."""
        customer_data = {key: entry.get() for key, entry in self.entries.items()}

        # --- Data Validation ---
        for key, value in customer_data.items():
            if not value:
                messagebox.showerror("Validation Error", f"The field '{key.replace('_', ' ').title()}' cannot be empty.")
                return

        if "@" not in customer_data['email'] or "." not in customer_data['email']:
            messagebox.showerror("Validation Error", "Please enter a valid email address.")
            return

        try:
            float(customer_data['initial_deposit'])
        except ValueError:
            messagebox.showerror("Validation Error", "Initial Deposit must be a valid number.")
            return
        
        # --- Add to Database ---
        new_account_number = database.add_customer_to_db(customer_data)

        if new_account_number:
            messagebox.showinfo("Success", f"Account created successfully!\nNew Account Number: {new_account_number}")
            self.clear_form()
            self.form_window.destroy() # Close the form window on success
        else:
            messagebox.showerror("Database Error", "An account with this Email or Phone Number already exists.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AccountOpeningApp(root)
    root.mainloop()
