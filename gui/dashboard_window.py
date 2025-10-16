import tkinter as tk
from tkinter import messagebox, ttk
from core.transaction_manager import deposit, withdraw, transfer, get_user_transactions
from core.account_manager import get_user_by_account
from assets.logo import load_logo


class DashboardWindow:
    def __init__(self, master, user):
        self.master = master
        self.user = user
        self.master.title(f"SwiftBank Dashboard - {user['full_name']}")
        self.master.geometry("600x550")
        self.master.resizable(False, False)

        # Display SwiftBank logo
        logo_image = load_logo((90, 90))
        if logo_image:
            logo_label = tk.Label(master, image=logo_image)
            logo_label.image = logo_image  # Keep reference
            logo_label.pack(pady=10)

        # Welcome message
        tk.Label(master, text=f"Welcome, {user['full_name']}", font=("Arial", 16, "bold")).pack(pady=5)
        tk.Label(master, text=f"Account Number: {user['account_number']}", font=("Arial", 10)).pack()

        # Balance
        self.balance_label = tk.Label(
            master,
            text=f"Current Balance: ₦{self.user['balance']:,.2f}",
            font=("Arial", 14, "bold"),
            fg="green"
        )
        self.balance_label.pack(pady=15)

        # Buttons Frame
        frame = tk.Frame(master)
        frame.pack(pady=10)

        tk.Button(frame, text="Deposit", width=12, bg="green", fg="white", command=self.deposit_money).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Withdraw", width=12, bg="orange", fg="white", command=self.withdraw_money).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Transfer", width=12, bg="blue", fg="white", command=self.transfer_money).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Transactions", width=16, bg="purple", fg="white", command=self.show_transactions).grid(row=0, column=3, padx=5)

        tk.Button(master, text="Logout", bg="red", fg="white", width=15, command=self.logout).pack(pady=20)

    # Deposit
    def deposit_money(self):
        amount = self.get_amount_popup("Deposit Amount (₦)")
        if amount is None:
            return

        success, msg = deposit(self.user["account_number"], amount)
        messagebox.showinfo("Deposit", msg)
        if success:
            self.refresh_balance()

    # Withdraw
    def withdraw_money(self):
        amount = self.get_amount_popup("Withdraw Amount (₦)")
        if amount is None:
            return

        success, msg = withdraw(self.user["account_number"], amount)
        messagebox.showinfo("Withdraw", msg)
        if success:
            self.refresh_balance()

    # Transfer
    def transfer_money(self):
        popup = tk.Toplevel(self.master)
        popup.title("Transfer Money")
        popup.geometry("300x250")
        popup.resizable(False, False)

        tk.Label(popup, text="Receiver Account Number:").pack(pady=5)
        self.receiver_entry = tk.Entry(popup, width=30)
        self.receiver_entry.pack(pady=5)

        tk.Label(popup, text="Amount (₦):").pack(pady=5)
        self.amount_entry = tk.Entry(popup, width=30)
        self.amount_entry.pack(pady=5)

        tk.Button(popup, text="Transfer", bg="blue", fg="white", width=15,
                  command=lambda: self.confirm_transfer(popup)).pack(pady=10)

    def confirm_transfer(self, popup):
        receiver_acc = self.receiver_entry.get().strip()
        amount = self.amount_entry.get().strip()

        if not receiver_acc or not amount:
            messagebox.showerror("Error", "All fields are required.")
            return

        if receiver_acc == self.user["account_number"]:
            messagebox.showerror("Error", "You cannot transfer to your own account.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for amount.")
            return

        success, msg = transfer(self.user["account_number"], receiver_acc, amount)
        if success:
            messagebox.showinfo("Success", msg)
            self.refresh_balance()
            popup.destroy()
        else:
            messagebox.showerror("Error", msg)

    # Transaction History
    def show_transactions(self):
        transactions = get_user_transactions(self.user["account_number"])

        popup = tk.Toplevel(self.master)
        popup.title("Transaction History")
        popup.geometry("600x400")

        columns = ("Type", "Amount", "Description", "Timestamp")
        tree = ttk.Treeview(popup, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        tree.pack(fill="both", expand=True)

        for t in transactions:
            tree.insert("", "end", values=(t["type"], f"₦{t['amount']:.2f}", t["description"], t["timestamp"]))

    # Utility Functions
    def get_amount_popup(self, title):
        popup = tk.Toplevel(self.master)
        popup.title(title)
        popup.geometry("300x150")
        popup.resizable(False, False)

        tk.Label(popup, text=title, font=("Arial", 12)).pack(pady=10)
        amount_entry = tk.Entry(popup, width=25)
        amount_entry.pack(pady=5)

        result = {"amount": None}

        def confirm():
            try:
                result["amount"] = float(amount_entry.get().strip())
                popup.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount.")

        tk.Button(popup, text="Confirm", bg="green", fg="white", command=confirm).pack(pady=10)
        popup.wait_window()
        return result["amount"]

    def refresh_balance(self):
        user = get_user_by_account(self.user["account_number"])
        self.user = user
        self.balance_label.config(text=f"Current Balance: ₦{self.user['balance']:,.2f}")

    # Logout
    def logout(self):
        from gui.login_window import LoginWindow
        self.master.withdraw()
        messagebox.showinfo("Logout", "You have been logged out successfully.")
        new_window = tk.Toplevel(self.master)
        LoginWindow(new_window)
