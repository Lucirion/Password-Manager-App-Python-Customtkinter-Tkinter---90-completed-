import tkinter    as tk
import customtkinter as ctk
from tkinter import messagebox

class BasicAddEntryWindow(ctk.CTkToplevel):
    def __init__(self, master, entry_manager, on_add_callback):
        super().__init__(master)

        # ── slim context‐menu helper ──────────────────────────
        def add_context_menu(widget):
            menu = tk.Menu(widget, tearoff=False)
            def select_all():
                # if text widget, tag_add exists; else it's an Entry
                if hasattr(widget, "tag_add"):
                    widget.tag_add(tk.SEL, "1.0", "end")
                else:
                    widget.select_range(0, tk.END)
            menu.add_command(label="Select All", command=select_all)
            menu.add_command(label="Copy",       command=lambda: widget.event_generate("<<Copy>>"))
            widget.bind("<Button-3>",  lambda e: menu.tk_popup(e.x_root, e.y_root))
            widget.bind("<Control-a>", lambda e: (select_all(), "break"))

        self.master_window = master
        self.entry_manager = entry_manager
        self.on_add_callback = on_add_callback

        # ── window sizing & centering ─────────────────────────
        self.title("Add New Entry")
        self.geometry("440x580")
        self.update_idletasks()
        w, h = 440, 580
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (sw - w)//2, (sh - h)//2
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.resizable(False, False)

        # ── transparent padding frame ─────────────────────────
        wrapper = ctk.CTkFrame(self, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, padx=20, pady=20)

        self.protocol("WM_DELETE_WINDOW", self.handle_cancel)

        # ── Label field ────────────────────────────────────────
        ctk.CTkLabel(wrapper, text="Label:").pack(anchor="w")
        self.label_var = tk.StringVar()
        label_ent = ctk.CTkEntry(wrapper, textvariable=self.label_var)
        label_ent.pack(fill="x", pady=(10, 25))
        add_context_menu(label_ent)

        # ── Notes field ───────────────────────────────────────┐
        ctk.CTkLabel(wrapper, text="Notes:").pack(anchor="w")
        self.notes_txt = ctk.CTkTextbox(wrapper, height=120)
        self.notes_txt.pack(fill="both", expand=True)
        add_context_menu(self.notes_txt)

        # ── Buttons ────────────────────────────────────────────
        btn_row = ctk.CTkFrame(wrapper, fg_color="transparent")
        btn_row.pack(fill="x", pady=(15, 0))
        ctk.CTkButton(btn_row, text="Add",    command=self.handle_add,    width=170)\
           .pack(side="left", expand=True, padx=5)
        ctk.CTkButton(btn_row, text="Cancel", command=self.handle_cancel, width=170)\
           .pack(side="left", expand=True, padx=5)
        
        self.protocol("WM_DELETE_WINDOW", self.handle_cancel)

    def handle_add(self):
        label = self.label_var.get().strip()
        notes = self.notes_txt.get("1.0", "end").strip()

        if not label:
            messagebox.showwarning("Missing Label", "Label cannot be empty.")
            return

        if label in self.entry_manager.list_entries():
            messagebox.showerror("Duplicate", f"“{label}” already exists.")
            return

        # Persist into vault
        self.entry_manager.add_entry(label, notes)

        # callback will refresh & deiconify the main window
        self.on_add_callback()

        # close this popup
        self.destroy()

    def handle_cancel(self):
        # even on cancel, ensure the main window is shown
        self.on_add_callback()
        self.destroy()
