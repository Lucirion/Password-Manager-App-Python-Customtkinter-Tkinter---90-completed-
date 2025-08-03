import customtkinter as ctk
from storage.vault import Vault
from cryptography.fernet import Fernet

import os
from storage.vault import Vault
from storage.basic_vault import BasicVault

# ── Config constants ────────────────────────────────────
BASE_DIR          = os.path.dirname(__file__)
BASIC_VAULT_FILE  = os.path.join(BASE_DIR, "vaults", "basic_vault.data")
BASIC_KEY_FILE    = os.path.join(BASE_DIR, "vaults", "fernet_key.key")


def load_key() -> bytes:
    """Read your Fernet key from disk."""
    with open("config/fernet_key.key", "rb") as f:
        return f.read()

def clean_empty_entries(vault_obj: Vault) -> None:
    """
    Remove any entries whose label is just whitespace.
    """
    deleted = []
    for lbl in vault_obj.list_entries():
        if not lbl.strip():
            vault_obj.delete_entry(lbl)
            deleted.append(lbl)
    if deleted:
        print("Removed ghost entries:", deleted)


class CustomDialog(ctk.CTkToplevel):
    def __init__(self, master, title, message):
        super().__init__(master)
        self.title(title)
        self.geometry("320x160")
        self.resizable(False, False)
        self.response = None

        label = ctk.CTkLabel(self, text=message, wraplength=280)
        label.pack(pady=20)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        yes_button = ctk.CTkButton(button_frame, text="Yes", command=self.yes)
        yes_button.pack(side="left", padx=10)

        no_button = ctk.CTkButton(button_frame, text="No", command=self.no)
        no_button.pack(side="left", padx=10)

        self.grab_set()  # Makes it modal

    def yes(self):
        self.response = True
        self.destroy()

    def no(self):
        self.response = False
        self.destroy()


class BasicEntryManager:  
    """Only label+notes, stored in basic_vault.data."""
    def __init__(self):
        key = load_key()
        self.vault = BasicVault(key, path="config/basic_vault.data")
        clean_empty_entries(self.vault)

    def list_entries(self) -> list[str]:
        return self.vault.list_entries()

    def get_entry(self, label: str) -> dict:
        return self.vault.get_entry(label) or {}

    def add_entry(self, label: str, notes: str, master=None) -> bool:
        label = label.strip()
        if not label:
            CustomDialog(master=master, title="Missing Label", message="Label cannot be empty.")
            return False

        if label in self.vault.list_entries():
            dialog = CustomDialog(master=master, title="Overwrite?", message=f"“{label}” exists. Overwrite?")
            dialog.update_idletasks()
            dialog.wait_window()

            if not dialog.response:
                return False

        # empty creds + your notes
        self.vault.add_entry(label, "", "", "", notes)
        return True

    def delete_entry(self, label: str) -> bool:
        return self.vault.delete_entry(label)
    
    def export_as_text(self, file_path: str) -> int:
        print(self.vault)
        try:
            count = 0
            with open(file_path, "w", encoding="utf-8") as file:
                for label, entry in self.vault._data.items():
                    file.write(f"Label: {label}\n")
                    file.write(f"Username: {entry.get('username', '')}\n")
                    file.write(f"Password: {entry.get('password', '')}\n")
                    file.write(f"Notes: {entry.get('notes', '')}\n")
                    file.write("-----\n")
                    count += 1
            return count
        except Exception as e:
            print(f"❌ Error exporting to .txt: {e}")
            return 0


    def import_entries(self, filepath, label):
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read().strip()

            if not content:
                return False  # Empty file

            clean_label = label.strip() if label and label.strip() else "Imported Entry"

            self.vault.add_entry(
                label=clean_label,
                username="",
                password="",
                email="",
                notes=content
            )
            return True

        except Exception as e:
            print(f"Import failed: {e}")
            return False

        
class FullEntryManager:
    """Username/password/email/notes, stored in vault.data."""
    def __init__(self):
        key = load_key()
        self.vault = Vault(key)  # default path -> vault.data
        clean_empty_entries(self.vault)

    def list_entries(self) -> list[str]:
        return self.vault.list_entries()

    def get_entry(self, label: str) -> dict:
        return self.vault.get_entry(label) or {}

    def add_entry(
        self, label: str, username: str, password: str,
        email: str = "", notes: str = ""
    ) -> None:
        self.vault.add_entry(label, username, password, email, notes)

    def delete_entry(self, label: str) -> bool:
        return self.vault.delete_entry(label)    
    
    def import_entries(self, filepath, label):
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                lines = file.readlines()

            # Map various capitalizations to canonical field names
            key_map = {
                "username": "username",
                "user name": "username",
                "password": "password",
                "pass": "password",
                "email": "email",
                "e-mail": "email",
                "mail": "email",
                "notes": "notes",
                "note": "notes"
            }

            fields = {v: "" for v in set(key_map.values())}

            for line in lines:
                line = line.strip()
                if not line or ":" not in line:
                    continue  # Skip empty or malformed lines
                key, value = line.split(":", 1)
                key, value = key.strip().lower(), value.strip()

                if key in key_map:
                    canonical = key_map[key]
                    fields[canonical] = value



            use_label = label.strip() if label and label.strip() else "Imported Entry"

            self.vault.add_entry(
                label=use_label,
                username=fields["username"],
                password=fields["password"],
                email=fields["email"],
                notes=fields["notes"]
            )
            return True

        except Exception as e:
            print(f"Import failed: {e}")
            return False
