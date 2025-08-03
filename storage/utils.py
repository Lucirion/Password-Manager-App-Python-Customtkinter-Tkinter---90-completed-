import os
from cryptography.fernet import Fernet

def load_fernet_key():
    key_path = "vault.key"
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, "wb") as f:
            f.write(key)
        return key
