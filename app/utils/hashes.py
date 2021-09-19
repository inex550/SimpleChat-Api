import hashlib


def get_password_hash(password: str):
    return hashlib.sha256(password.encode()).hexdigest()