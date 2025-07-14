from os import urandom
from hashlib import pbkdf2_hmac

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    salt_bytes = bytes.fromhex(salt) if salt else urandom(16)
    hashed = pbkdf2_hmac('sha256', password.encode(), salt_bytes, 100000)
    return (hashed.hex(), salt_bytes.hex())