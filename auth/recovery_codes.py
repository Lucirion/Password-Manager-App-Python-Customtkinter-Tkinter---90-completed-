import secrets
import os
import json

BACKUP_CODES_FILE = "config/backup_codes.json"

def generate_backup_codes(n=5):
    codes = [secrets.token_hex(4) for _ in range(n)]
    with open(BACKUP_CODES_FILE, "w") as f:
        json.dump(codes, f)
    return codes

def validate_backup_code(input_code):
    if not os.path.exists(BACKUP_CODES_FILE):
        return False

    with open(BACKUP_CODES_FILE, "r") as f:
        codes = json.load(f)

    if input_code in codes:
        codes.remove(input_code)  # one-time use
        with open(BACKUP_CODES_FILE, "w") as f:
            json.dump(codes, f)
        return True
    return False
