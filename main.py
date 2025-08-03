# from gui.interface import launch_gui
# from auth.totp import validate_code
from auth.login_screen import show_login
# from auth.qr_window import show_qr_window

# Calls the function from inside login_screen.py
if __name__ == "__main__":
    show_login()

# show_qr_window()

# ============ BELOW USED FOR TESTING ============ #

# print("🔐 Welcome to Lucirion Password Manager 🔐")
# code = input("Enter 6-digit TOTP code: ")

# if validate_code(code):
#     print("✅ Code valid! Launching vault...")
#     from storage.vault import Vault
#     from cryptography.fernet import Fernet
    
# ⚠️ Use a generated key from the generate_key.py or store this securely
#     key = b'...'
#     vault = Vault(key)

#     from gui.interface import launch_gui
#     launch_gui()
# else:
#     print("❌ Invalid code. Access denied.")




# ✅ Test: Add an entry
# vault.add_entry("GitHub", "lucas_dev", "MySuperSecretPassword123")

# ✅ Test: List entries
# print("Stored Entries:", vault.list_entries())

# ✅ Test: Retrieve an entry
# entry = vault.get_entry("GitHub")
# print("Retrieved Entry:", entry)

# ✅ Test: Delete entry
# vault.delete_entry("GitHub")
# print("After Deletion:", vault.list_entries())


