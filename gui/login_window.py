import tkinter as tk
from tkinter import messagebox
from core.account_manager import login
from gui.dashboard_window import DashboardWindow
from assets.logo import load_logo


class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("SwiftBank - Login")
        self.center_window(400, 500)
        self.master.resizable(False, False)

        # --- Logo ---
        logo_image = load_logo((100, 100))
        if logo_image:
            logo_label = tk.Label(master, image=logo_image)
            logo_label.image = logo_image  # prevent garbage collection
            logo_label.pack(pady=10)

        # --- Title ---
        tk.Label(master, text="🏦 SwiftBank", font=("Arial", 20, "bold")).pack(pady=5)
        tk.Label(master, text="Login to your account", font=("Arial", 12)).pack(pady=5)

        # --- Account Number ---
        tk.Label(master, text="Account Number:", font=("Arial", 11)).pack(pady=(20, 5))
        self.account_entry = tk.Entry(master, width=30, font=("Arial", 11))
        self.account_entry.pack(pady=5)

        # --- PIN Entry ---
        tk.Label(master, text="4-Digit PIN:", font=("Arial", 11)).pack(pady=5)
        pin_frame = tk.Frame(master)
        pin_frame.pack(pady=5)

        self.pin_entry = tk.Entry(pin_frame, width=25, font=("Arial", 11), show="*")
        self.pin_entry.pack(side="left", padx=(0, 5))

        # --- Show/Hide PIN ---
        self.show_pin = tk.BooleanVar(value=False)
        toggle_btn = tk.Checkbutton(pin_frame, text="Show", variable=self.show_pin,
                                    command=self.toggle_pin_visibility)
        toggle_btn.pack(side="right")

        # --- Buttons ---
        tk.Button(master, text="Login", width=25, bg="green", fg="white",
                  font=("Arial", 11, "bold"), command=self.handle_login).pack(pady=15)

        tk.Button(master, text="Create New Account", width=25, bg="blue", fg="white",
                  font=("Arial", 11, "bold"), command=self.open_register_window).pack(pady=5)

        # --- Bind Enter key to login ---
        master.bind("<Return>", lambda event: self.handle_login())

    # Toggle PIN Visibility
    def toggle_pin_visibility(self):
        if self.show_pin.get():
            self.pin_entry.config(show="")
        else:
            self.pin_entry.config(show="*")

    # Handle Login
    def handle_login(self):
        account_number = self.account_entry.get().strip()
        pin = self.pin_entry.get().strip()

        if not account_number or not pin:
            messagebox.showwarning("Error", "Please fill all fields.")
            return

        if not pin.isdigit() or len(pin) != 4:
            messagebox.showwarning("Error", "PIN must be a 4-digit number.")
            return

        success, result = login(account_number, pin)

        if success:
            messagebox.showinfo("Success", f"Welcome, {result['full_name']}!")
            self.master.withdraw()
            new_window = tk.Toplevel(self.master)

            if result.get("is_admin"):
                from gui.admin_window import AdminWindow
                AdminWindow(new_window, result)
            else:
                DashboardWindow(new_window, result)
        else:
            messagebox.showerror("Login Failed", result)

    # Open Registration Window
    def open_register_window(self):
        from gui.register_window import RegisterWindow
        self.master.withdraw()
        new_window = tk.Toplevel(self.master)
        RegisterWindow(new_window)

    # Utility - Center Window
    def center_window(self, width, height):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.master.geometry(f"{width}x{height}+{x}+{y}")
