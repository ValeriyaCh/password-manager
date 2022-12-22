import hashlib
import hmac
import os

# server-side
def verify_password(salt: str, password_hash: str, password: str):
    return hmac.compare_digest(password_hash, hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 10000))

def hash_data_salt(plaintext: str):
    salt = os.urandom(32)
    hash = hashlib.pbkdf2_hmac('sha256', plaintext.encode(), salt, 10000)
    return salt, hash
