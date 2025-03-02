import string
import secrets

def get_secret_code(length):
    digits = list(string.digits + string.ascii_uppercase + string.ascii_lowercase)
    return ''.join(secrets.choice(digits) for _ in range(length))