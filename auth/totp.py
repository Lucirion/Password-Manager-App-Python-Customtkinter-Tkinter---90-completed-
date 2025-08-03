import pyotp
import json # Converts Python dictionaries to strings and vice versa. AKA Data serialization
import os # Helps checking file existence

SEED_PATH = "config/totp_seed.json"

def get_or_generate_seed():
    if not os.path.exists(SEED_PATH):
        seed = pyotp.random_base32()
        with open(SEED_PATH, "w") as f:
            json.dump({"seed": seed}, f)
    else:
        with open(SEED_PATH, "r") as f:
            seed = json.load(f)["seed"]
    return seed

def get_provisioning_uri(account="PMA", issuer="D.K Secret Banana Vault"):
    seed = get_or_generate_seed()
    totp = pyotp.TOTP(seed)
    return totp.provisioning_uri(name=account, issuer_name=issuer)

def generate_seed():
    if not os.path.exists(SEED_PATH):
        seed = pyotp.random_base32()
        with open(SEED_PATH, "w") as f:
            json.dump({"seed": seed}, f)
        print("TOTP seed generated and saved.")
    else:
        print("Seed already exists.")

def load_seed():
    with open(SEED_PATH, "r") as f:
        data = json.load(f)
    return data["seed"]
    
def validate_code(user_code):
    seed = load_seed()
    totp = pyotp.TOTP(seed)
    return totp.verify(user_code)

if __name__ == "__main__":
    generate_seed()