import random
from core.data_handler import load_data, save_data


# CREATE ACCOUNT
def create_account(full_name: str, pin: str):
    """
    Create a new bank account with a unique account number.
    Automatically assigns admin privileges if the full name is 'admin'.
    """
    users = load_data()

    # Ensure 10-digit unique account number
    while True:
        account_number = str(random.randint(1000000000, 9999999999))
        if not any(u["account_number"] == account_number for u in users):
            break

    new_user = {
        "full_name": full_name.strip(),
        "pin": str(pin).strip(),
        "balance": 0.0,
        "account_number": account_number,
        "is_admin": full_name.strip().lower() == "admin"
    }

    users.append(new_user)
    save_data(users)
    return True, account_number


# LOGIN USER
def login(account_number: str, pin: str):
    """
    Verify login credentials.
    Returns (True, user_dict) if success, else (False, error_message).
    """
    users = load_data()

    for user in users:
        if str(user["account_number"]) == str(account_number) and str(user["pin"]) == str(pin):
            return True, user

    return False, "Invalid account number or PIN."


# RETRIEVE USER BY ACCOUNT
def get_user_by_account(account_number: str):
    """Retrieve a single user's data by their account number."""
    users = load_data()
    for user in users:
        if str(user["account_number"]) == str(account_number):
            return user
    return None


# UPDATE USER DATA
def update_user_data(updated_user: dict):
    """
    Update an existing user's data (e.g., after deposit or withdrawal).
    """
    users = load_data()
    for i, user in enumerate(users):
        if str(user["account_number"]) == str(updated_user["account_number"]):
            users[i] = updated_user
            save_data(users)
            return True
    return False


# GET ALL USERS
def get_all_users():
    """Return a list of all user records."""
    return load_data()


# DELETE USER
def delete_user(account_number: str):
    """Delete a user by account number."""
    users = load_data()
    new_users = [u for u in users if str(u["account_number"]) != str(account_number)]
    save_data(new_users)
    return len(new_users) < len(users)


# RESET USER PIN
def reset_user_pin(account_number: str):
    """
    Generate a new random 4-digit PIN for the given user.
    Returns (True, new_pin) if successful, else (False, None).
    """
    users = load_data()
    for user in users:
        if str(user["account_number"]) == str(account_number):
            new_pin = str(random.randint(1000, 9999))
            user["pin"] = new_pin
            save_data(users)
            return True, new_pin
    return False, None
