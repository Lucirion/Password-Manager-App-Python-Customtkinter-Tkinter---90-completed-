# import tkinter as tk
# from tkinter import messagebox
# from storage.vault import Vault
# from auth.qr_window import show_qr_window

# def launch_gui(vault):
#     root = tk.Tk()
#     root.title("🔐 Lucirion Password Manager 🔐")
#     root.geometry("400x400")
#     root.resizable(False, False)

#     # Entry list
#     entry_listbox = tk.Listbox(root, height=15, width=50)
#     entry_listbox.pack(pady=10)

#     # Handlers
#     def refresh_entries():
#         entry_listbox.delete(0, tk.END)
#         for label in vault.list_entries():
#             entry_listbox.insert(tk.END, label)

#     def add_entry():
#         def save():
#             label = label_entry.get()
#             user = user_entry.get()
#             pwd = pwd_entry.get()
#             vault.add_entry(label, user, pwd)
#             refresh_entries()
#             popup.destroy()

#         popup = tk.Toplevel(root)
#         popup.title("Add Entry")
#         tk.Label(popup, text="Label:").pack(pady=(10, 0))
#         label_entry = tk.Entry(popup)
#         label_entry.pack(padx=10, pady=5)
        
#         tk.Label(popup, text="Username:").pack(pady=(10, 0))
#         user_entry = tk.Entry(popup, show="*")
#         user_entry.pack(padx=10, pady=5)

#         tk.Label(popup, text="Password:").pack(pady=(10, 0))
#         pwd_entry = tk.Entry(popup, show="*")
#         pwd_entry.pack(padx=10, pady=5)

#         tk.Button(popup, text="Save", command=save).pack(pady=(10, 15))

#     def view_entry():
#         selected = entry_listbox.get(tk.ACTIVE)
#         entry = vault.get_entry(selected)
#         if entry:
#             msg = f"Username: {entry['username']}\nPassword: {entry['password']}"
#             messagebox.showinfo("Entry Details", msg)

#     def delete_entry():
#         selected = entry_listbox.get(tk.ACTIVE)
#         if selected:
#             vault.delete_entry(selected)
#             refresh_entries()

#     # Menu bar
#     vault_menu = tk.Menu(root)
#     root.config(menu=vault_menu)
#     vault_menu.add_command(label="🔐 Add Entry", command=add_entry)
#     vault_menu.add_command(label="📲 Setup Authenticator", command=lambda: show_qr_window(root))
#     vault_menu.add_command(label="🚪 Quit", command=root.quit)

#     # Action buttons
#     btn_frame = tk.Frame(root)
#     btn_frame.pack(fill="x", pady=10)
#     tk.Button(btn_frame, text="Add",    command=add_entry).pack(side=tk.LEFT, padx=10)
#     tk.Button(btn_frame, text="View",   command=view_entry).pack(side=tk.LEFT, padx=10)
#     tk.Button(btn_frame, text="Delete", command=delete_entry).pack(side=tk.LEFT, padx=10)
#     tk.Button(btn_frame, text="Quit",   command=root.quit).pack(side=tk.RIGHT, padx=10)

#     # Initial population
#     refresh_entries()
#     root.mainloop()


# if __name__ == "__main__":
#     # For quick testing without the login flow
#     from cryptography.fernet import Fernet
#     key = b'6tLqQ-lqwz0QO-GU0UxLd5ZgoJH_YU9dMm3jxYUtVSo='  # replace with your secure key
#     vault = Vault(key)
#     launch_gui(vault)
