# gui/entry_view_window.py
import tkinter as tk
import customtkinter as ctk
from entry_manager import EntryManager
from storage.vault import Vault

class EntryDetailsWindow(ctk.CTkToplevel):
    def __init__(self, master, label, entry_data, vault):
        super().__init__(master)
        self.title(f"Details: {label}")
        self.geometry("480x620")
        self.master_window = master
        self.entry_data = entry_data
        self.edit_mode = False
        self.vault = vault
        current = ctk.get_appearance_mode().lower()
        self.bg_color = "#2A2A2A" if current == "dark" else "#FFFFFF"
        self.fg_color = "#F0F0F0" if current == "dark" else "#000000"

        self.fields = {}  # Field name → widget reference

        # Update successful
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            text_color="green",  # success color
            font=("Arial", 14)
        )
        self.status_label.pack(pady=0)  # adjust placement as needed

        # Create all field widgets
        for name, value in {
            "Label": label,
            "Username": entry_data.get("username", ""),
            "E-mail": entry_data.get("email", ""),
            "Password": entry_data.get("password", ""),
            "Notes": entry_data.get("notes", "")
        }.items():
            self.make_field(name, value)

        # Button row
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", pady=(10, 0), padx=10)

        self.edit_button = ctk.CTkButton(
            button_frame,
            text="Edit",
            command=self.toggle_edit_mode,
            width=170
        )
        self.edit_button.pack(side="left", expand=True, padx=5)

        ctk.CTkButton(
            button_frame,
            text="Close",
            command=self.handle_close,
            width=170
        ).pack(side="right", expand=True, padx=5)

        self.protocol("WM_DELETE_WINDOW", self.handle_close)

        self.update_button = ctk.CTkButton(
            button_frame,
            text="Update",
            command=self.save_changes,
            width=170
        )
        self.update_button.pack(side="left", expand=True, padx=5)
        self.update_button.pack_forget()  # Hide it by default


    def make_field(self, name, value):
        ctk.CTkLabel(self, text=f"{name}:", anchor="w") \
            .pack(fill="x", pady=(5, 0))

        if name == "Notes":
            widget = ctk.CTkTextbox(
                self,
                height=150,
                fg_color=self.bg_color,
                text_color=self.fg_color,
                corner_radius=6,
                border_width=1,
                border_color="#555555"
            )
            widget.insert("0.0", value)
        else:
            widget = ctk.CTkEntry(
                self,
                width=360,
                fg_color=self.bg_color,
                text_color=self.fg_color
            )
            widget.insert(0, value)

        widget.configure(state="disabled")
        widget.pack(fill="x", padx=10, pady=(0, 10))
        self.fields[name.lower()] = widget  # store reference

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        new_state = "normal" if self.edit_mode else "disabled"

        for widget in self.fields.values():
            widget.configure(state=new_state)

        if self.edit_mode:
            self.edit_button.pack_forget()
            self.update_button.pack(side="left", expand=True, padx=5)
        else:
            self.update_button.pack_forget()
            self.edit_button.pack(side="left", expand=True, padx=5)

    def handle_close(self):
        self.master_window.deiconify()
        self.destroy()

    def save_changes(self):
        label = self.fields["label"].get().strip()

        updated_data = {
            "username": self.fields["username"].get(),
            "email":    self.fields["e-mail"].get(),
            "password": self.fields["password"].get(),
            "notes":    self.fields["notes"].get("1.0", "end").strip()
        }

        # 🔐 Save to vault
        self.vault.add_entry(
            label,
            updated_data["username"],
            updated_data["password"],
            updated_data["email"],
            updated_data["notes"]
        )

        # 🔁 Reload from vault to reflect saved data
        refreshed = self.vault.get_entry(label)
        if refreshed:
            self.fields["username"].delete(0, "end")
            self.fields["username"].insert(0, refreshed["username"])

            self.fields["e-mail"].delete(0, "end")
            self.fields["e-mail"].insert(0, refreshed["email"])

            self.fields["password"].delete(0, "end")
            self.fields["password"].insert(0, refreshed["password"])

            self.fields["notes"].delete("1.0", "end")
            self.fields["notes"].insert("1.0", refreshed["notes"])

        self.status_label.configure(text="✔️ Entry successfully updated!")
        self.after(3000, lambda: self.status_label.configure(text=""))
        self.toggle_edit_mode()

