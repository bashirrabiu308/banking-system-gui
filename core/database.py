import json
import os

# Paths to your data files
USER_FILE = os.path.join("data", "users.json")
TRANSACTION_FILE = os.path.join("data", "transactions.json")


def load_data(file_path):
    """Load data safely from a JSON file."""
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_data(file_path, data):
    """Save data safely to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_users():
    return load_data(USER_FILE)


def save_users(users):
    save_data(USER_FILE, users)


def load_transactions():
    """Load transactions from file."""
    if not os.path.exists("data/transactions.json"):
        return []
    with open("data/transactions.json", "r") as f:
        return json.load(f)


def save_transactions(transactions):
    save_data(TRANSACTION_FILE, transactions)
