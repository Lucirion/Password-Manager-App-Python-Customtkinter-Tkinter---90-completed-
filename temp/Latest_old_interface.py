# gui/interface_ctk.py

import json
import sys, os
import tkinter as tk
import customtkinter as ctk

# make project root importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tkinter import filedialog
from tkinter import messagebox
from cryptography.fernet import Fernet
from storage.main_vault import Vault
from gui.entry_view_window import EntryDetailsWindow
from alternative_interface_ctk import ImportEntryWindow

# load key & vault
with open("config/fernet_key.key", "rb") as f:
    KEY = f.read()
vault = Vault(KEY)

def launch_gui():

    def center_window(win, w, h):
        win.update_idletasks()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width // 2) - (w // 2)
        y = (screen_height // 2) - (h // 2)
        win.geometry(f"{w}x{h}+{x}+{y}")

    def clean_empty_entries():
        deleted = []
        for label in vault.list_entries():
            if not label.strip():
                vault.delete_entry(label)
                deleted.append(label)
        if deleted:
            print(f"Removed ghost entries: {deleted}")

    clean_empty_entries()

    # ── Root & Theme ──────────────────────────────
    root = ctk.CTk()
    root.title("🔐 Lucirion Password Manager")
    root.geometry("500x550")
    root.resizable(False, False)
    center_window(root, 500, 550)
    
    # ── Dark / Light mode ──────────────────────────────
    appearance_var = ctk.IntVar(value=1)  # 1 = Dark, 0 = Light

    def toggle_appearance():
        mode = "Dark" if appearance_var.get() == 1 else "Light"
        ctk.set_appearance_mode(mode)
        theme_switch.configure(text="🌙 Dark Mode" if mode == "Dark" else "🌞 Light Mode")
    
    theme_switch = ctk.CTkSwitch(
        master=root,
        text="🌙 Dark Mode",
        variable=appearance_var,
        command=toggle_appearance,
        switch_width=34,
        switch_height=18,
        font=ctk.CTkFont(size=12),
        progress_color="light blue",
        button_color="light blue",
        text_color="#969696"
    )
    theme_switch.pack(padx=10, pady=(0, 15), anchor="w")

    # ── Dropdown Menu ──────────────────────────────

    dropdown_var = ctk.StringVar(value="Settings")
    dropdown_menu = ctk.CTkOptionMenu(
        master=root,
        variable=dropdown_var,
        values=["Import", "Export", "Simpler import"],
        width=100,
        anchor="w",
        font=ctk.CTkFont(size=13),
        dropdown_font=ctk.CTkFont(size=12),
        fg_color="#444444",
        text_color="#DDDDDD",
        button_color="#666666",
        button_hover_color="#777777",
    )
    dropdown_menu.pack(padx=30, pady=(0), anchor="e")

    def on_dropdown_change(*_):
        choice = dropdown_var.get()
        if choice == "Export":
            export_data()
        elif choice == "Import":
            pass
        elif choice == "Simpler import":
            import_entry()

        dropdown_var.set("Settings")
    
    dropdown_var.trace_add("write", on_dropdown_change)

    # ── Export function ───────────────────────────────────

    def export_data():
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Export Vault"
        )
        if not filepath:
            return # user cancelled
        
        data = []
        for label in vault.list_entries():
            entry = vault.get_entry(label)
            if entry is None:
                print(f"Skipped export for label '{label}' (entry not found)")
                continue
            ordered_entry = {
                "Label": label,
                "Email": entry.get("email", ""),
                "Username": entry.get("username", ""),
                "Password": entry.get("password", ""),
                "Notes": entry.get("notes", "")
            }
            data.append(ordered_entry)

        try:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Export Successful", f"{len(data)} entries saved.")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    # ── Select button ──────────────────────────────

    def on_entry_select(entry_label):
        selected_var.set(entry_label)

    # ── Search Bar ────────────────────────────────
    search_var = ctk.StringVar()
    ctk.CTkLabel(root, text="Search Labels:", anchor="w") \
        .pack(fill="x", padx=20, pady=(20, 5))
    ctk.CTkEntry(
        master=root,
        textvariable=search_var
    ).pack(fill="x", padx=20, pady=(0, 10))

    # ── Scrollable List ───────────────────────────
    list_frame = ctk.CTkScrollableFrame(root, width=460, height=300)
    list_frame.pack(padx=20, pady=(0, 10))

    selected_var = ctk.StringVar(value="")

    def refresh_entries():
        term = search_var.get().lower().strip()
        for w in list_frame.winfo_children():
            w.destroy()

        for label in vault.list_entries():
            if term in label.lower():
                ctk.CTkRadioButton(
                    master=list_frame,
                    text=label,
                    variable=selected_var,
                    value=label
                ).pack(fill="x", padx=10, pady=2)

    search_var.trace_add("write", lambda *_: refresh_entries())
    refresh_entries()

    # ── Handlers ───────────────────────────────────

    def add_entry():
        popup = ctk.CTkToplevel(root)
        popup.title("Add Entry")
        popup.geometry("440x580")
        popup.resizable(False, False)
        center_window(popup, 440, 580)

        root.withdraw()  # hide main window

        wrapper = ctk.CTkFrame(popup)
        wrapper.pack(fill="both", expand=True, padx=20, pady=20)


        # ─── right-click / Ctrl+A context menu helper ───────────────
        def add_context_menu(widget, is_text=False):
            menu = tk.Menu(widget, tearoff=0)
            if is_text:
                menu.add_command(
                    label="Select All",
                    command=lambda: widget.tag_add(tk.SEL, "1.0", "end")
                )
            else:
                menu.add_command(
                    label="Select All",
                    command=lambda: widget.select_range(0, tk.END)
                )
            menu.add_command(
                label="Copy",
                command=lambda: widget.event_generate("<<Copy>>")
            )
            widget.bind(
                "<Button-3>",
                lambda e: menu.tk_popup(e.x_root, e.y_root)
            )
            widget.bind(
                "<Control-a>",
                lambda e: ("break",
                           widget.tag_add(tk.SEL, "1.0", "end")
                           if is_text
                           else widget.select_range(0, tk.END))
            )

        ctk.CTkLabel(wrapper, text="Label:").pack(anchor="w")
        label_ent = ctk.CTkEntry(wrapper)
        label_ent.pack(fill="x", pady=(5, 15))
        label_ent.configure(state="normal")
        add_context_menu(label_ent)

        ctk.CTkLabel(wrapper, text="Username:").pack(anchor="w")
        user_ent = ctk.CTkEntry(wrapper)
        user_ent.pack(fill="x", pady=(5, 15))
        user_ent.configure(state="normal")
        add_context_menu(user_ent)

        ctk.CTkLabel(wrapper, text="E-mail:").pack(anchor="w")
        email_ent = ctk.CTkEntry(wrapper)
        email_ent.pack(fill="x", pady=(5, 15))
        email_ent.configure(state="normal")
        add_context_menu(email_ent)

        ctk.CTkLabel(wrapper, text="Password:").pack(anchor="w")
        pwd_ent = ctk.CTkEntry(wrapper, show="")
        pwd_ent.pack(fill="x", pady=(5, 15))
        pwd_ent.configure(state="normal")
        add_context_menu(pwd_ent)

        ctk.CTkLabel(wrapper, text="Notes:").pack(anchor="w")
        # styled multiline textbox
        mode = ctk.get_appearance_mode().lower()
        notes_bg = "#2A2A2A" if mode == "dark" else "#FFFFFF"
        notes_fg = "#F0F0F0" if mode == "dark" else "#000000"
        

        notes_txt = ctk.CTkTextbox(
            wrapper,
            height=120,
            fg_color=notes_bg,
            text_color=notes_fg,
            corner_radius=6,
            border_width=1,
            border_color="#555555"
        )
        notes_txt.pack(fill="both", pady=(5, 20))
        add_context_menu(notes_txt, is_text=True)

        # Save callback has access to label_ent, user_ent, etc.
        def on_save():

            label = label_ent.get().strip()
            if not label:
                messagebox.showwarning("Missing Label", "You must enter a Label to save an entry.")
                return

            vault.add_entry(
                label_ent.get().strip(),
                user_ent.get().strip(),
                pwd_ent.get().strip(),
                email=email_ent.get().strip(),
                notes=notes_txt.get("1.0", "end-1c").strip()
            )
            refresh_entries()
            popup.destroy()
            root.deiconify() # show main window again
            
        # Handle closing manually
        def on_close():
            root.deiconify()
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)
        ctk.CTkButton(popup, text="Save", command=on_save)\
            .pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            master=popup,
            text="Save",
            command=on_save
        ).pack(fill="x", padx=20, pady=10)

    # ── Entry view window ──────────────────────
    def view_entry():
        sel = selected_var.get()
        if not sel:
            messagebox.showwarning("No selection", "Select an entry first.")
            return
        
        data = vault.get_entry(sel)
        if not data:
            messagebox.showerror("Not found", f"No data for “{sel}”.")
            return

        root.withdraw() # hide main window

        popup = EntryDetailsWindow(root, sel, data)
        center_window(popup, 400, 500)

        # Ensure the main window comes back when view closes
        def on_close():
            root.deiconify()
            popup.destroy()
        popup.protocol("WM_DELETE_WINDOW", on_close)

    def delete_entry():
        sel = selected_var.get().strip()
        if not sel:
            messagebox.showwarning("No selection", "Please select an entry to delete.")
            return

        if sel not in vault.list_entries():
            messagebox.showerror("Invalid Entry", f"No vault entry named “{sel}”.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", f"Delete entry “{sel}”?")
        if confirm:
            vault.delete_entry(sel)
            selected_var.set("")
            refresh_entries()
    
    # ── Alternative interface window ──────────────────────
    def import_entry():
        ImportEntryWindow(root)

    # ── Bottom Action Buttons ──────────────────────
    btn_frame = ctk.CTkFrame(master=root)
    btn_frame.pack(fill="x", padx=0, pady=20)

    for txt, cmd in [
        ("Add",    add_entry),
        ("View",   view_entry),
        ("Delete", delete_entry)
    ]:
        ctk.CTkButton(
            master=btn_frame,
            text=txt,
            command=cmd
        ).pack(side="left", expand=True, fill="x", padx=5)

    root.mainloop()


if __name__ == "__main__":
    launch_gui()
