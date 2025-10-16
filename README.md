## 🏦 SwiftBank — Modern GUI Banking System (Tkinter + Python)

### ⚡ Overview

**SwiftBank** is a modern **graphical banking system** built with **Python** and **Tkinter**.
It allows users to create accounts, log in securely, manage balances, and perform transactions — all through a sleek, intuitive interface.

The project simulates real-world banking operations, combining **user-friendly design**, **modular architecture**, and **clean code structure**.

---

### ✨ Key Features

✅ **User Account Creation** — Register new accounts with automatic account number generation.
✅ **Secure Login System** — PIN-based authentication for privacy and data protection.
✅ **Admin Panel** — Special access for administrators to manage users.
✅ **Deposit, Withdraw, and Transfer Funds** — Full simulation of core banking operations.
✅ **Balance Inquiry** — Instant view of available balance.
✅ **PIN Reset System** — Generate new PINs securely.
✅ **Data Persistence** — All data stored locally via JSON file (no external database needed).
✅ **Custom Logo Support** — Add your own brand logo (`SwiftBank` logo included).
✅ **Modern UI** — Simple and neat Tkinter interface optimized for clarity.

---

### 🏗️ Project Structure

```
swiftbank/
│
├── core/
│   ├── account_manager.py      # Core account logic
│   ├── data_handler.py         # Handles data saving/loading
│   ├── utils.py                # Utility functions
│
├── gui/
│   ├── login_window.py         # Login screen
│   ├── register_window.py      # Registration form
│   ├── dashboard_window.py     # User dashboard
│   ├── admin_window.py         # Admin management window
│
├── assets/
│   ├── logo.py                 # Logo loader utility
│   ├── bank_logo.png           # SwiftBank logo
│
├── main.py                     # Entry point to launch the app
├── README.md                   # Project documentation
└── data.json                   # Local storage file for users
```

---

### 🧠 How It Works

1. **Start the app** → Users see a login window.
2. **Login or Register** → Existing users enter credentials; new users create accounts.
3. **Dashboard Access** → Upon login, users can:

   * View balance
   * Deposit/withdraw funds
   * Transfer to other accounts
   * Logout securely
4. **Admin Panel** → If logged in as `admin`, you gain access to manage all users.

---

### ⚙️ Installation & Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/swiftbank.git
cd swiftbank
```

#### 2. Install Required Dependencies

SwiftBank uses only built-in Python libraries, but you’ll need **Pillow** for image support:

```bash
pip install pillow
```

#### 3. Run the Application

```bash
python main.py
```

---

### 🖼️ Screenshot (Optional)

You can include your logo or app UI preview here:

![SwiftBank Logo](assets/bank_logo.png)

---

### 👨‍💻 Tech Stack

* **Python 3.10+**
* **Tkinter** — GUI framework
* **Pillow (PIL)** — Image handling
* **JSON** — Local data storage

---

### 🧩 Modular Design

Each major part of the project is isolated in its own module:

* `core/` handles logic and data
* `gui/` manages all Tkinter interfaces
* `assets/` stores branding and images

This makes SwiftBank **easy to maintain**, **extend**, or **integrate** with databases or APIs later.

---

### 🚀 Future Improvements

* Add SQLite or MySQL database support
* Implement transaction history logging
* Include email notifications for PIN reset
* Add responsive themes and light/dark mode
* Support multiple currencies

---

### 📜 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

### 💡 Author

**Bashir Rabiu**
💻 Aspiring Data Scientist | Python Developer | Tech Enthusiast
📧 [bashirrabiu308@gmail.com]

---
