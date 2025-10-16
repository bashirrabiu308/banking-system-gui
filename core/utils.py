import random
import hashlib
import time


def generate_account_number():
    """Generate a unique 10-digit account number."""
    return str(random.randint(10**9, (10**10) - 1))


def get_timestamp():
    """Return the current time in a readable format."""
    return time.strftime("%Y-%m-%d %H:%M:%S")


def hash_pin(pin):
    """Encrypt the user's 4-digit PIN using SHA-256."""
    return hashlib.sha256(pin.encode()).hexdigest()


def verify_pin(pin, hashed_pin):
    """Verify a PIN against its hashed version."""
    return hash_pin(pin) == hashed_pin
