# storage/vault.py

import json
import os
from typing import Optional, Dict, Any, List
from cryptography.fernet import Fernet

class Vault():
    def __init__(self, key: bytes, path: Optional[str] = None):
        """
        key: Fernet key bytes
        path: optional override for data file location
        """
        self.fernet = Fernet(key)
        # default vault path is next to this file
        self.vault_path = path or os.path.join(
            os.path.dirname(__file__), "vault.data"
        )
        self._ensure_storage()
        self._data: Dict[str, Dict[str, Any]] = self._load_data()

    def _ensure_storage(self):
        # make parent folder if needed
        dir_path = os.path.dirname(self.vault_path)
        os.makedirs(dir_path, exist_ok=True)

    def _save_data(self) -> None:
        """Encrypt and write self._data to disk."""
        raw = json.dumps(self._data).encode("utf-8")
        encrypted = self.fernet.encrypt(raw)
        with open(self.vault_path, "wb") as f:
            f.write(encrypted)

    def _load_data(self) -> Dict[str, Dict[str, Any]]:
        """Read, decrypt, and return vault dict; on error, return empty."""
        if not os.path.isfile(self.vault_path):
            return {}
        try:
            with open(self.vault_path, "rb") as f:
                encrypted = f.read()
            decrypted = self.fernet.decrypt(encrypted)
            return json.loads(decrypted.decode("utf-8"))
        except Exception as e:
            print(f"Vault load failed: {e!r}")
            return {}


    def add_entry(self, label, username, password, email, notes):
        self._data[label] = {
            "username": username,
            "password": password,
            "email": email,
            "notes": notes
        }
        self._save_data()  # encrypt and write to disk


    def delete_entry(self, label: str) -> bool:
        """
        Remove an entry if it exists.
        Returns True on success, False if the label wasn't found.
        """
        if label in self._data:
            del self._data[label]
            self._save_data()
            return True
        return False

    def get_entry(self, label: str) -> Optional[Dict[str, Any]]:
        """Return the full entry dict (including notes), or None if missing."""
        return self._data.get(label)

    def list_entries(self) -> List[str]:
        """Return a sorted list of all labels."""
        return sorted(self._data.keys())


# ============ THE REASONS FOR THE DESIGN ============ #
# Encrypted at rest: Nobody can access vault data without a key.

# Modular: You can plug this vault into CLI, GUI, or API.

# Simple & readable: You know how your data flows and where it’s secured.
