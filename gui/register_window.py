import tkinter as tk
from tkinter import messagebox
from core.account_manager import create_account


class RegisterWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Create New Account")
        self.master.geometry("400x400")
        self.master.resizable(False, False)

        tk.Label(master, text="🏦 Create Account", font=("Arial", 18, "bold")).pack(pady=20)

        # Full name
        tk.Label(master, text="Full Name:").pack(pady=(10, 5))
        self.name_entry = tk.Entry(master, width=30)
        self.name_entry.pack()

        # PIN
        tk.Label(master, text="4-Digit PIN:").pack(pady=5)
        self.pin_entry = tk.Entry(master, width=30, show="*")
        self.pin_entry.pack()

        # Register button
        tk.Button(master, text="Register", width=20, bg="green", fg="white",
                  command=self.handle_register).pack(pady=15)

        # Back to login
        tk.Button(master, text="Back to Login", width=20, bg="blue", fg="white",
                  command=self.back_to_login).pack()

    def handle_register(self):
        full_name = self.name_entry.get().strip()
        pin = self.pin_entry.get().strip()

        if not full_name or not pin:
            messagebox.showwarning("Error", "Please fill all fields.")
            return

        success, msg = create_account(full_name, pin)
        if success:
            messagebox.showinfo("Success", msg)
            self.back_to_login()
        else:
            messagebox.showerror("Error", msg)

    def back_to_login(self):
        # Delayed import to avoid circular import
        from gui.login_window import LoginWindow
        self.master.withdraw()
        new_window = tk.Toplevel(self.master)
        LoginWindow(new_window)
