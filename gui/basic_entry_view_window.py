# gui/entry_view_window.py
import tkinter as tk
import customtkinter as ctk
from storage.basic_vault import BasicVault
from tkinter import messagebox
from customtkinter import CTkTextbox
from typing import cast

class BasicEntryDetailsWindow(ctk.CTkToplevel):
    def __init__(self, root, master, label, entry_data, basic_vault, editable=False):
        super().__init__(master)
        self.title("Details")
        self.master_window = master # Store reference to root
        self.vault = basic_vault
        self.label = label

        # Attaches a context menu to a widget
        def add_context_menu(widget):
            menu = tk.Menu(widget, tearoff=0)
            menu.add_command(
                label="Select All",
                command=lambda: widget.select_range(0, tk.END)
            )
            
            menu.add_command(
                label="Copy",
                command=lambda: widget.event_generate("<<Copy>>")
            )
            # right-click popup
            widget.bind(
                "<Button-3>",
                lambda e: menu.tk_popup(e.x_root, e.y_root)
            )
            # optional Ctrl+A shortcut
            widget.bind(
                "<Control-a>",
                lambda e: (widget.select_range(0, tk.END), "break")
            )
        
        # Theme-aware style constants
        current = ctk.get_appearance_mode().lower()    # e.g. "dark" or "light"
        bg_color = "#2A2A2A" if current == "dark" else "#FFFFFF"
        fg_color = "#F0F0F0" if current == "dark" else "#000000"

        # Field‐display helper
        def make_field(name, value, editable=False):
            ctk.CTkLabel(self, text=f"{name}:", anchor="w").pack(fill="x", pady=(5, 0))

            if name == "Notes":
                
                widget = ctk.CTkTextbox(
                    self,
                    height=150,
                    fg_color=bg_color,
                    text_color=fg_color,
                    corner_radius=6,
                    border_width=1,
                    border_color="#555555"
                )
                widget.insert("1.0", value)  # 💬 Insert initial text

                if not editable:
                    widget.configure(state="disabled")  # better to disable textbox fully

                widget.pack(fill="both", expand=True, pady=(0, 10))
                self.notes_entry = widget
            else:
                widget = ctk.CTkEntry(
                    self,
                    width=360,
                    fg_color=bg_color,
                    text_color=fg_color,
                    textvariable=ctk.StringVar(value=value)
                )
                if not editable:
                    widget.configure(state="readonly")
                widget.pack(fill="x", pady=(0, 10))

            add_context_menu(widget)
            return widget
        
        # Render each field

        self.editable = editable
        self.notes_entry = make_field("Notes", entry_data.get("notes", ""), editable=self.editable)

        self.button_row = ctk.CTkFrame(self)
        self.button_row.pack(pady=(10, 10), fill="x")

        # Edit button (initially visible)
        self.edit_button = ctk.CTkButton(
            self.button_row,
            text="Edit",
            command=self.handle_edit
        )
        self.edit_button.pack(side="left", padx=5, expand=True, fill="x")

        # Update button (initially hidden)
        self.update_button = ctk.CTkButton(
            self.button_row,
            text="Update",
            command=self.handle_update
        )
        self.update_button.pack_forget()

        # Close button (always visible on the right)
        self.close_button = ctk.CTkButton(
            self.button_row,
            text="Close",
            command=self.handle_close
        )
        self.close_button.pack(side="right", padx=5, expand=True, fill="x")

        # Edit button - visible
        ctk.CTkButton(
            self,
            text="Edit",
            command=self.handle_edit
        )
        self.edit_button.pack(pady=(0, 5), fill="x")

        # Update button - invisible
        ctk.CTkButton(
            self,
            text="Update",
            command=self.handle_update
        )
        self.update_button.pack_forget()
        
        # Close button
        ctk.CTkButton(
            self,
            text="Close",
            command=self.handle_close
        )
        # Handle [X] window close
        self.protocol("WM_DELETE_WINDOW", self.handle_close)

    # Edit and update buttons functions    
    def handle_edit(self):
        self.notes_entry.configure(state="normal")

        self.edit_button.pack_forget()
        self.update_button.pack(side="left", padx=5, expand=True, fill="x")
    
    def handle_update(self):
        updated_notes = self.notes_entry.get("1.0", "end-1c").strip()
        
        # Confirm label still exists before update
        if self.label in self.vault._data:
            self.vault._data[self.label]["notes"] = updated_notes
            self.vault._save_data()
            messagebox.showinfo("Updated", f"Notes for '{self.label}' have been saved.")
        else:
            messagebox.showerror("Error", f"Entry '{self.label}' not found in vault.")

    def handle_close(self):
        self.master_window.deiconify()  # Show main window again
        self.destroy() # Close view window

