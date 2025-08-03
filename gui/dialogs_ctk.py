# gui/dialogs_ctk.py

import customtkinter as ctk

class LabelPrompt(ctk.CTkToplevel):
    def __init__(self, master, title="Enter Label"):
        super().__init__(master)
        self.title(title)
        self.geometry("300x160")
        self.resizable(False, False)
        self.label_input = None

        ctk.CTkLabel(self, text="Enter a label:").pack(pady=10)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=5)
        self.entry.focus()

        ctk.CTkButton(self, text="Confirm", command=self.confirm).pack(pady=10)
        self.grab_set()

    def confirm(self):
        self.label_input = self.entry.get().strip()
        self.destroy()

class InfoDialog(ctk.CTkToplevel):
    def __init__(self, master, title, message):
        super().__init__(master)
        self.title(title)
        self.geometry("300x140")
        self.resizable(False, False)

        ctk.CTkLabel(self, text=message, wraplength=260).pack(pady=20)
        ctk.CTkButton(self, text="OK", command=self.destroy).pack(pady=10)

        self.grab_set()

