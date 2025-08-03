import time
import pyotp
import qrcode
import PIL
import base64

# Step 1: Use a single consistent key
key = "H64MM44A3CJTDWS43HXM37IXRTTLKHOB"

totp = pyotp.TOTP(key)

# Step 2: Create QR code with saved key
#uri = totp.provisioning_uri(name="", issuer_name="D.K Secret Banana Vault")
#qrcode.make(uri).save("totp.png")
#print("Scan this QR code to set up.")

# Step 3: Verify input using same key
while True:
    code = input("Enter code: ")
    print(totp.verify(code))

# ================================================================== #
# Nedan foer koden
# key = pyotp.random_base32()
# totp = pyotp.TOTP(key)

# print(totp.now())

# input_code = input("Enter 2FA Code:")

# print(totp.verify(input_code))


