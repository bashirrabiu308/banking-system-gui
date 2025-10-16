import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from core.account_manager import get_all_users, delete_user, reset_user_pin
from core.database import load_transactions


class AdminWindow:
    def __init__(self, master, admin_user):
        self.master = master
        self.admin_user = admin_user
        self.master.title("Admin Dashboard")
        self.center_window(700, 500)
        self.master.resizable(False, False)

        # --- Header ---
        tk.Label(master, text=f"Welcome, {admin_user['full_name']} (Admin)",
                 font=("Arial", 16, "bold")).pack(pady=10)

        # --- Search Section ---
        search_frame = tk.Frame(master)
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5)
        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.grid(row=0, column=1)
        tk.Button(search_frame, text="Search", bg="green", fg="white",
                  command=self.search_user).grid(row=0, column=2, padx=5)
        tk.Button(search_frame, text="Refresh", bg="gray", fg="white",
                  command=self.load_users).grid(row=0, column=3, padx=5)

        # --- Users Table ---
        table_frame = tk.Frame(master)
        table_frame.pack(fill="both", expand=True, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("Account", "Full Name", "Balance"), show="headings")
        self.tree.heading("Account", text="Account Number")
        self.tree.heading("Full Name", text="Full Name")
        self.tree.heading("Balance", text="Balance (₦)")
        self.tree.column("Account", width=150)
        self.tree.column("Full Name", width=200)
        self.tree.column("Balance", width=120)

        # Scrollbar
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll_y.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        # --- Buttons ---
        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="View Transactions", bg="purple", fg="white", width=18,
                  command=self.view_transactions).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Reset PIN", bg="blue", fg="white", width=15,
                  command=self.reset_pin).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Delete User", bg="red", fg="white", width=15,
                  command=self.delete_user).grid(row=0, column=2, padx=10)
        tk.Button(btn_frame, text="Logout", bg="gray", fg="white", width=15,
                  command=self.logout).grid(row=0, column=3, padx=10)

        self.load_users()

    # ===================================================
    # Load All Users
    # ===================================================
    def load_users(self):
        self.tree.delete(*self.tree.get_children())
        users = get_all_users()
        for u in users:
            self.tree.insert("", "end", values=(u["account_number"],
                                                u["full_name"],
                                                f"₦{u['balance']:,.2f}"))

    # ===================================================
    # Search User
    # ===================================================
    def search_user(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showinfo("Search", "Please enter a name or account number.")
            return

        self.tree.delete(*self.tree.get_children())
        users = get_all_users()
        for u in users:
            if query in u["full_name"].lower() or query in u["account_number"]:
                self.tree.insert("", "end", values=(u["account_number"],
                                                    u["full_name"],
                                                    f"₦{u['balance']:,.2f}"))

    # ===================================================
    # Reset User PIN
    # ===================================================
    def reset_pin(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to reset PIN.")
            return

        user_data = self.tree.item(selected, "values")
        account_number = user_data[0]
        success, new_pin = reset_user_pin(account_number)

        if success:
            messagebox.showinfo("Success", f"PIN reset successfully!\nNew PIN: {new_pin}")
        else:
            messagebox.showerror("Error", "Failed to reset PIN.")

    # ===================================================
    # Delete User
    # ===================================================
    def delete_user(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to delete.")
            return

        user_data = self.tree.item(selected, "values")
        account_number = user_data[0]

        confirm = messagebox.askyesno("Confirm Delete",
                                      f"Are you sure you want to delete account {account_number}?")
        if not confirm:
            return

        success = delete_user(account_number)
        if success:
            messagebox.showinfo("Deleted", "User account deleted successfully.")
            self.load_users()
        else:
            messagebox.showerror("Error", "Failed to delete account.")

    # ===================================================
    # View All Transactions
    # ===================================================
    def view_transactions(self):
        transactions = load_transactions()

        popup = tk.Toplevel(self.master)
        popup.title("All Transactions")
        self.center_popup(popup, 750, 450)

        # --- Search Frame ---
        search_frame = tk.Frame(popup)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search by Account Number:").grid(row=0, column=0, padx=5)
        search_entry = tk.Entry(search_frame)
        search_entry.grid(row=0, column=1, padx=5)

        # --- Table ---
        columns = ("Account", "Type", "Amount", "Description", "Timestamp")
        tree = ttk.Treeview(popup, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)

        scroll_y = ttk.Scrollbar(popup, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scroll_y.set)
        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scroll_y.pack(side="right", fill="y")

        # --- Populate ---
        def populate(data):
            tree.delete(*tree.get_children())
            for t in data:
                tree.insert("", "end", values=(
                    t["account_number"],
                    t["type"],
                    f"₦{t['amount']:,.2f}",
                    t["description"],
                    t["timestamp"]
                ))

        populate(transactions)

        # --- Search ---
        def search():
            acc_num = search_entry.get().strip()
            if acc_num == "":
                populate(transactions)
            else:
                filtered = [t for t in transactions if acc_num in t["account_number"]]
                populate(filtered)

        # --- Export CSV ---
        def export_csv():
            file = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv")])
            if file:
                with open(file, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Account", "Type", "Amount", "Description", "Timestamp"])
                    for t in transactions:
                        writer.writerow([
                            t["account_number"],
                            t["type"],
                            t["amount"],
                            t["description"],
                            t["timestamp"]
                        ])
                messagebox.showinfo("Export", "Transactions exported successfully!")

        # --- Buttons ---
        tk.Button(search_frame, text="Search", bg="green", fg="white",
                  command=search).grid(row=0, column=2, padx=5)
        tk.Button(search_frame, text="Clear", bg="gray", fg="white",
                  command=lambda: populate(transactions)).grid(row=0, column=3, padx=5)
        tk.Button(search_frame, text="Export CSV", bg="blue", fg="white",
                  command=export_csv).grid(row=0, column=4, padx=5)

    # ===================================================
    # Logout
    # ===================================================
    def logout(self):
        self.master.withdraw()
        messagebox.showinfo("Logout", "You have been logged out successfully.")

        from gui.login_window import LoginWindow
        new_window = tk.Toplevel(self.master)
        LoginWindow(new_window)

    # ===================================================
    # Utility Functions
    # ===================================================
    def center_window(self, width, height):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def center_popup(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
