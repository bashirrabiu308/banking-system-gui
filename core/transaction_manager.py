from core.database import load_transactions, save_transactions
from core.account_manager import get_user_by_account, update_user_data
from core.utils import get_timestamp


def record_transaction(account_number, type_, amount, description):
    """Record a transaction in transactions.json"""
    transactions = load_transactions()

    transaction = {
        "account_number": account_number,
        "type": type_,  # deposit, withdraw, transfer
        "amount": amount,
        "description": description,
        "timestamp": get_timestamp()
    }

    transactions.append(transaction)
    save_transactions(transactions)


def deposit(account_number, amount):
    """Add money to an account."""
    user = get_user_by_account(account_number)
    if not user:
        return False, "Account not found."

    if amount <= 0:
        return False, "Deposit amount must be positive."

    user["balance"] += amount
    update_user_data(user)
    record_transaction(account_number, "deposit", amount, "Deposit successful")

    return True, f"₦{amount:.2f} deposited successfully."


def withdraw(account_number, amount):
    """Withdraw money from an account."""
    user = get_user_by_account(account_number)
    if not user:
        return False, "Account not found."

    if amount <= 0:
        return False, "Withdrawal amount must be positive."

    if user["balance"] < amount:
        return False, "Insufficient balance."

    user["balance"] -= amount
    update_user_data(user)
    record_transaction(account_number, "withdraw", amount, "Withdrawal successful")

    return True, f"₦{amount:.2f} withdrawn successfully."


def transfer(sender_account, receiver_account, amount):
    """Transfer money between accounts."""
    sender = get_user_by_account(sender_account)
    receiver = get_user_by_account(receiver_account)

    if not sender:
        return False, "Sender account not found."
    if not receiver:
        return False, "Receiver account not found."
    if amount <= 0:
        return False, "Transfer amount must be positive."
    if sender["balance"] < amount:
        return False, "Insufficient balance."

    # Perform the transfer
    sender["balance"] -= amount
    receiver["balance"] += amount

    update_user_data(sender)
    update_user_data(receiver)

    record_transaction(sender_account, "transfer", amount, f"Transfer to {receiver_account}")
    record_transaction(receiver_account, "transfer", amount, f"Transfer from {sender_account}")

    return True, f"₦{amount:.2f} transferred to account {receiver_account} successfully."


def get_user_transactions(account_number):
    """Retrieve all transactions belonging to a specific user."""
    transactions = load_transactions()
    return [t for t in transactions if t["account_number"] == account_number]
