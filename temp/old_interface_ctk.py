# gui/interface_ctk.py

import sys
import os

# Ensure project root is on the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import customtkinter as ctk
from tkinter import messagebox
from cryptography.fernet import Fernet
from storage.main_vault import Vault
from auth.qr_window import show_qr_window


print("CustomTkinter version:", ctk.__version__)

# Theme setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Load Fernet key
with open("config/fernet_key.key", "rb") as key_file:
    KEY = key_file.read()


def launch_gui(vault: Vault):
    root = ctk.CTk()
    root.title("🔐 Lucirion Password Manager")
    root.geometry("500x500")
    root.resizable(False, False)

    mode_var = ctk.StringVar(value=ctk.get_appearance_mode())

    mode_switch = ctk.CTkSwitch(
        master=root,
        text=f"{mode_var.get().capitalize()} Mode",
        variable=mode_var,
        onvalue="light",
        offvalue="dark",
        command=lambda: (
            ctk.set_appearance_mode(mode_var.get()),        # flip CTk theme
            mode_switch.configure(                           # update switch text
                text=f"{mode_var.get().capitalize()} Mode"
            )
        )
    )    
    mode_switch.pack(anchor="ne", padx=20, pady=10)

    if mode_var.get() == "dark":
        mode_switch.select()
    else:
        mode_switch.deselect()

    def toggle_appearance():
        # flip mode
        new_mode = "light" if ctk.get_appearance_mode() == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)
        # update switch text
        mode_switch.configure(text=f"{new_mode.capitalize()} Mode")
    
    # Search field label
    ctk.CTkLabel(
        master=root,
        text="Search Password Labels:",
        anchor="w"
    ).pack(fill="x", padx=20, pady=(20, 0))

    # Search field
    search_var = ctk.StringVar()
    search_entry = ctk.CTkEntry(
        master=root,
        placeholder_text="🔍 Search entries…",
        textvariable=search_var,
        width=460
    )
    search_entry.pack(padx=20, pady=(5, 10))

    # Scrollable entry list
    frame = ctk.CTkScrollableFrame(master=root, width=460, height=300)
    frame.pack(padx=20, pady=(0, 10))

    def refresh_entries():
        term = search_var.get().lower().strip()
        # clear out old labels
        for widget in frame.winfo_children():
            widget.destroy()

        # repopulate with only matching labels
        for label in vault.list_entries():
            if term in label.lower():
                ctk.CTkLabel(
                    master=frame,
                    text=label,
                    anchor="w"
                ).pack(fill="x", padx=10, pady=2)
    # re-filter every time the user types
    search_var.trace_add("write", lambda *_: refresh_entries())

    # — Handlers

    def add_entry():
        popup = ctk.CTkToplevel(root)
        popup.title("Add Entry")
        popup.geometry("440x580")
        popup.resizable(False, False)

        # Use a wrapper frame for neat vertical layout
        wrapper = ctk.CTkFrame(master=popup)
        wrapper.pack(fill="both", expand=True, padx=20, pady=20)

        # Label
        ctk.CTkLabel(wrapper, text="Label:").pack(anchor="w")
        label_ent = ctk.CTkEntry(wrapper)
        label_ent.pack(fill="x", pady=(5, 15))

        # Username
        ctk.CTkLabel(wrapper, text="Username:").pack(anchor="w")
        user_ent = ctk.CTkEntry(wrapper)
        user_ent.pack(fill="x", pady=(5, 15))

        # E-mail
        ctk.CTkLabel(wrapper, text="E-mail:").pack(anchor="w")
        email_ent = ctk.CTkEntry(wrapper)
        email_ent.pack(fill="x", pady=(5, 15))

        # Password
        ctk.CTkLabel(wrapper, text="Password:").pack(anchor="w")
        pwd_ent = ctk.CTkEntry(wrapper, show="*")
        pwd_ent.pack(fill="x", pady=(5, 15))

        # Notes (multiline)
        ctk.CTkLabel(wrapper, text="Notes:").pack(anchor="w")
        notes_txt = ctk.CTkTextbox(wrapper, height=120)
        notes_txt.pack(fill="both", pady=(5, 20))

        def save():
            vault.add_entry(
                label_ent.get().strip(),
                user_ent.get().strip(),
                pwd_ent.get().strip(),
                email=email_ent.get().strip(),
                notes=notes_txt.get("1.0", "end-1c").strip()
            )
            refresh_entries()
            popup.destroy()

        # Save button at bottom of popup
        ctk.CTkButton(
            master=popup,
            text="Save",
            command=save
        ).pack(pady=10, padx=20, fill="x")

    def view_entry():
        children = frame.winfo_children()
        if not children:
            return
        selected = children[0].cget("text")
        entry = vault.get_entry(selected)
        if not entry:
            return
        info = (
            f"Label: {selected}\n"
            f"Username: {entry.get('username')}\n"
            f"E-mail: {entry.get('email')}\n"
            f"Password: {entry.get('password')}\n\n"
            f"Notes:\n{entry.get('notes')}"
        )
        messagebox.showinfo("Entry Details", info)

    def delete_entry():
        children = frame.winfo_children()
        if not children:
            return
        selected = children[0].cget("text")
        vault.delete_entry(selected)
        refresh_entries()

    # — Bottom action buttons — inside launch_gui(), after your handlers —

    # — Bottom action buttons via place() — 
    btn_frame = ctk.CTkFrame(master=root, height=50)
    btn_frame.pack(fill="x", padx=20, pady=20)
    btn_frame.pack_propagate(False)   # lock in that 50px height

    btn_frame.pack(fill="x", padx=20, pady=20)
    btn_frame.configure(height=60)             # <- force minimum height
    btn_frame.pack_propagate(False) 

    actions = [("Add", add_entry),
               ("View", view_entry),
               ("Delete", delete_entry),
               ("Quit", root.quit)]
    n = len(actions)
    for i, (txt, cmd) in enumerate(actions):
        btn = ctk.CTkButton(
            master=btn_frame,
            text=txt,
            command=cmd,
            corner_radius=8,
            fg_color="#1FA526",
            hover_color="#158A28",
            text_color="white"
        )
        # position each button evenly across the width
        btn.place(
            relx = i/n + 0.01,                     # slight padding from edge
            rely = 0.1,                            # 10% from top
            relwidth = 1/n - 0.02,                 # equal slices
            relheight = 0.8                        # stretch to 80% height
        )

    # Initial population
    refresh_entries()
    root.mainloop()


if __name__ == "__main__":
    vault = Vault(KEY)
    launch_gui(vault)
