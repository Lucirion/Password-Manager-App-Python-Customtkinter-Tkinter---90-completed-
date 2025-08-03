import tkinter as tk
from tkinter import messagebox
from auth.totp import validate_code
from storage.vault import Vault
from cryptography.fernet import Fernet
from gui.interface_ctk import launch_gui


KEY = b'24LAJ4YSYMKMKMR3NTT5P5QZIAI5HVWK'

def show_login():
    root = tk.Tk()
    root.title("🔐 Lucirion Login 🔐")
    root.geometry("500x350")
    root.resizable(False, False)

    root.lift()
    root.attributes("-topmost", True)
    root.after(100, lambda: root.attributes("-topmost", False))

    tk.Label(root, text="Enter 6-digit code:").pack(pady=10)
    code_entry = tk.Entry(root, justify="center", font=("Courier", 14), width=10)
    code_entry.pack()

    def validate():
        code = code_entry.get().strip()
        if validate_code(code):
            vault = Vault(KEY)
            root.destroy()
            launch_gui(vault)
        else:
            messagebox.showerror("Access denied", "Invalid code.")  # Also: typo fixed from "Invalide"

    tk.Button(root, text="Unlock vault", command=validate).pack(pady=10)  # ⬅️ This belongs outside validate()

    root.mainloop()

if __name__ == "__main__":
    show_login()
