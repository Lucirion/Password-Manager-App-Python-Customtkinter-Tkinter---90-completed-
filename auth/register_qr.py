import pyotp
import json
import qrcode

# Load the existing seed
with open("config/totp_seed.json") as f:
    seed = json.load(f)["seed"]

totp = pyotp.TOTP(seed)
uri = totp.provisioning_uri(name="lucas@lucirion.com", issuer_name="Lucirion Manager")

# Generate and show QR code
img = qrcode.make(uri)
img.show()
