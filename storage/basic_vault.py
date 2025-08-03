import json
import os
from typing import Optional, Dict, Any, List
from cryptography.fernet import Fernet
from tkinter import simpledialog
from storage.vault import Vault

class BasicVault(Vault):
    def __init__(self, key: bytes, path: Optional[str] = None):
        self.fernet = Fernet(key)

        # 🔧 Define fallback save path inside /storage
        default_folder = os.path.join(os.path.dirname(__file__))  # this should already be /storage
        default_path = os.path.join(default_folder, "basic_vault.data")

        # ✅ Use provided path or fallback
        self.vault_path = os.path.abspath(path or default_path)

        os.makedirs(os.path.dirname(self.vault_path), exist_ok=True)
        self._data = self._load_data()


    def __iter__(self):
        return iter(self._data.values())


    
    def _save_data(self) -> None:
        raw       = json.dumps(self._data).encode("utf-8")
        encrypted = self.fernet.encrypt(raw)
        with open(self.vault_path, "wb") as f:
            f.write(encrypted)

    def _load_data(self) -> Dict[str, Dict[str, Any]]:
        if not os.path.isfile(self.vault_path):
            return {}
        try:
            with open(self.vault_path, "rb") as f:
                encrypted = f.read()
            decrypted = self.fernet.decrypt(encrypted)
            return json.loads(decrypted.decode("utf-8"))
        except Exception:
            return {}

    def add_entry(
        self,
        label: str,
        username: str,
        password: str,
        email: Optional[str] = "",
        notes: Optional[str] = ""
    ) -> None:
        label = label.strip()
        if not label:
            raise ValueError("Entry label cannot be empty")
        self._data[label] = {
            "username": username,
            "password": password,
            "email":    email or "",
            "notes":    notes or ""
        }
        self._save_data()

    def delete_entry(self, label: str) -> bool:
        if label in self._data:
            del self._data[label]
            self._save_data()
            return True
        return False

    def get_entry(self, label: str) -> Optional[Dict[str, Any]]:
        return self._data.get(label)

    def list_entries(self) -> List[str]:
        return sorted(self._data.keys())
    
    def import_txt_entry(self, label: str, file_path: str) -> bool:
        if not label.strip():
            raise ValueError("Entry label cannot be empty")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            return False

        entry_data = {}
        for line in lines:
            if ":" in line:
                key, value = line.strip().split(":", 1)
                key = key.strip().lower()
                if key in {"username", "password", "email", "notes"}:
                    entry_data[key] = value.strip()

        if not entry_data.get("username") or not entry_data.get("password"):
            return False  # required fields missing

        self._data[label] = {
            "username": entry_data.get("username", ""),
            "password": entry_data.get("password", ""),
            "email":    entry_data.get("email", " /n"),
            "notes":    entry_data.get("notes", "")
        }
        self._save_data()
        return True

    def update_entry(self, label: str, updated_data: Dict[str, Any]) -> bool:
        if label not in self._data:
            return False

        self._data[label] = updated_data
        self._save_data()
        return True



# ============ THE REASONS FOR THE DESIGN ============ #
# Encrypted at rest: Nobody can access vault data without a key.

# Modular: You can plug this vault into CLI, GUI, or API.

# Simple & readable: You know how your data flows and where it’s secured.
