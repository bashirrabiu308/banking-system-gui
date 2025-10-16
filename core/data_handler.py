import json
import os

# Paths to your data files
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

USERS_FILE = os.path.join(DATA_DIR, "users.json")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.json")


# USERS
def load_data():
    """Load all user data from users.json"""
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_data(data):
    """Save all user data to users.json"""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)


# TRANSACTIONS
def load_transactions():
    """Load transaction history"""
    if not os.path.exists(TRANSACTIONS_FILE):
        return []
    with open(TRANSACTIONS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_transactions(data):
    """Save transaction history"""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump(data, f, indent=4)
