import sys, os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_root)

# gui/interface_ctk.py
from dialogs_ctk import LabelPrompt, InfoDialog

import tkinter as tk
import customtkinter as ctk
import pyotp
from auth.totp import validate_code
from auth.totp import get_or_generate_seed, get_provisioning_uri
import qrcode
import uuid

from tkinter import filedialog, simpledialog, messagebox
from cryptography.fernet import Fernet
from tkinter import simpledialog
import tkinter.messagebox as mbox

from gui.entry_view_window import EntryDetailsWindow
from gui.basic_interface_ctk import BasicInterfaceWindow
from shared_functions import FullEntryManager
from storage.vault import Vault
from storage.utils import load_fernet_key

from auth.recovery_codes import generate_backup_codes

KEY = load_fernet_key()
vault = Vault(KEY)

def get_device_id():
    device_file = "config/device_id.txt"
    if not os.path.exists(device_file):
        device_id = str(uuid.uuid4())
        with open(device_file, "w") as f:
            f.write(device_id)
        return device_id
    else:
        with open(device_file, "r") as f:
            return f.read()

def is_first_time():
    return not os.path.exists("config/totp_seed.json")

# def register_totp_if_first_time():
#     if is_first_time():
#         seed = get_or_generate_seed()
#         uri = get_provisioning_uri()
#         qr_img = qrcode.make(uri)

#         # Show QR code to the user (e.g., via GUI window or save to file)
#         qr_img.show()  # or launch a dedicated QR window
#         print("Scan this QR code using your authenticator app.")

def register_totp_if_first_time():
    if is_first_time():
        seed = get_or_generate_seed()
        uri = get_provisioning_uri()
        qr_img = qrcode.make(uri)

        # Show QR for pairing with TOTP app
        qr_img.show()
        print("Scan this QR code using your authenticator app.")

        # 🎯 Then generate backup codes
        backup_codes = generate_backup_codes()
        print("📦 Your backup codes (save securely):")
        for code in backup_codes:
            print(f"- {code}")

def show_login():
    root = tk.Tk()
    root.title("🔐 Lucirion Login 🔐")
    root.geometry("400x220")
    root.resizable(False, False)

    tk.Label(root, text="Enter 6-digit code:").pack(pady=10)
    code_entry = tk.Entry(root, font=("Courier", 14), justify="center")
    code_entry.pack()

    def validate():
        code = code_entry.get().strip()
        if validate_code(code):
            root.destroy()
            vault = Vault(KEY)
            launch_gui()
        else:
            messagebox.showerror("Access Denied", "Invalid code.")

    tk.Button(root, text="Unlock Vault", command=validate).pack(pady=10)
    root.mainloop()


def show_backup_codes_gui(codes):
    backup_window = tk.Toplevel()
    backup_window.title("Your Backup Codes")
    backup_window.geometry("400x300")

    label = tk.Label(backup_window, text="Save these codes securely!", font=("Courier", 12))
    label.pack(pady=5)

    text_box = tk.Text(backup_window, wrap="word", height=10, font=("Courier", 12))
    text_box.pack(padx=10, pady=5, fill="both", expand=True)

    for code in codes:
        text_box.insert("end", code + "\n")

    text_box.config(state="disabled")

    def copy_to_clipboard():
        backup_window.clipboard_clear()
        backup_window.clipboard_append("\n".join(codes))
        backup_window.update()

    copy_button = tk.Button(backup_window, text="📋 Copy All Codes", command=copy_to_clipboard)
    copy_button.pack(pady=10)

def launch_gui():
    key = load_fernet_key()
    vault = Vault(key)
   
    def center_window(win, w, h):
        win.update_idletasks()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width // 2) - (w // 2)
        y = (screen_height // 2) - (h // 2)
        win.geometry(f"{w}x{h}+{x}+{y}")
    entry_manager = FullEntryManager()

    # ── Root & Theme ──────────────────────────────
    root = ctk.CTk()
    root.title("🔐 Lucirion Password Manager")
    root.geometry("600x520")
    root.resizable(False, False)
    center_window(root, 600, 550)
    
    # ── Generate new codes ──────────────────────────────
    def regenerate_backup_codes_with_confirmation():
        confirm = messagebox.askyesno(
            "Regenerate Backup Codes",
            "This will invalidate your existing backup codes and generate new ones.\nDo you want to continue?"
        )
        if confirm:
            new_codes = generate_backup_codes()
            show_backup_codes_gui(new_codes)

    # ── Dark / Light mode ──────────────────────────────
    
    header = ctk.CTkFrame(root, fg_color="transparent")
    header.pack(fill="x", padx=20, pady=(10, 5))
    appearance_var = ctk.IntVar(value=1)  # 1 = Dark, 0 = Light
    
    def toggle_appearance():
        mode = "Dark" if appearance_var.get() == 1 else "Light"
        ctk.set_appearance_mode(mode)
        theme_switch.configure(text="🌙 Dark Mode" if mode == "Dark" else "🌞 Light Mode")
    
    theme_switch = ctk.CTkSwitch(
        master=header,
        text="🌙 Dark Mode",
        variable=appearance_var,
        command=toggle_appearance,
        switch_width=34,
        switch_height=18,
        font=ctk.CTkFont(size=12, weight="bold"),
        progress_color="light blue",
        button_color="light blue",
        text_color="#969696"
    )
    theme_switch.pack(side="left")

    # ── Dropdown Menu ──────────────────────────────
    def on_main_select(choice):
        if choice == "Export":
            export_data()
        elif choice == "Import":
        # full‐featured import
            root.withdraw()
            import_data()      # <- make sure this function exists
            root.deiconify()
        elif choice == "Simpler import":
            root.withdraw()
            import_entry()
        # elif choice == "Regenerate backup codes":
        #     regenerate_backup_codes_with_confirmation()

        dropdown_menu.set("Settings")    
    dropdown_var = ctk.StringVar(value="Settings")
    dropdown_menu = ctk.CTkOptionMenu(
        master=header,
        variable=dropdown_var,
        values=["Settings", "Import", "Export", "Simpler import", "Regenerate backup codes"],
        command=on_main_select,
        width=100,
        anchor="w",
        font=ctk.CTkFont(size=13, weight="bold"),
        dropdown_font=ctk.CTkFont(size=12),
        fg_color="#444444",
        text_color="#DDDDDD",
        button_color="#666666",
        button_hover_color="#777777",
    )
    dropdown_menu.pack(side="right")
    
    # ── Import function ───────────────────────────────────
    
    def import_data():
        # 1) Pick file
        fname = filedialog.askopenfilename(
            title="Import Entry",
            filetypes=[("Text files", "*.txt")]
        )
        if not fname:
            return

        # 2) Label input via customtkinter
        prompt = LabelPrompt(master=root)
        root.wait_window(prompt)
        label = prompt.label_input

        if not label:
            InfoDialog(master=root, title="Import Error", message="Label cannot be empty.")
            return

        # 3) Import call
        success = entry_manager.import_entries(fname, label)

        # 4) If successful, sync to vault
        if success:
            entry = entry_manager.get_entry(label)
            if entry:
                vault.add_entry(
                    label,
                    entry.get("username", ""),
                    entry.get("password", ""),
                    entry.get("email", ""),
                    entry.get("notes", "")
                )

            InfoDialog(master=root, title="Import Successful", message=f"Entry “{label}” added.")
            refresh_entries()
        else:
            InfoDialog(
                master=root,
                title="Import Failed",
                message="Could not import—check file format or required fields."
            )

        def modal_window(win, width, height):
            win.geometry(f"{width}x{height}")
            win.resizable(False, False)
            win.grab_set()
            win.focus()


    # ── Export function ───────────────────────────────────

    def export_data():
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Export Vault"
        )
        if not filepath:
            return  # user cancelled

        try:
            with open(filepath, "w", encoding="utf-8") as file:
                exported_count = 0
                for label in entry_manager.list_entries():
                    entry = entry_manager.get_entry(label)
                    if entry is None:
                        print(f"Skipped export for label '{label}' (entry not found)")
                        continue

                    file.write(f"Label: {label}\n")
                    file.write(f"Email: {entry.get('email', '')}\n")
                    file.write(f"Username: {entry.get('username', '')}\n")
                    file.write(f"Password: {entry.get('password', '')}\n")
                    file.write(f"Notes: {entry.get('notes', '')}\n")
                    file.write("-----\n")
                    exported_count += 1

            messagebox.showinfo("Export Successful", f"{exported_count} entries saved to:\n{filepath}")
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
    list_frame = ctk.CTkScrollableFrame(root, width=560, height=300)
    list_frame.pack(padx=20, pady=(0, 10))

    selected_var = ctk.StringVar(value="")

    def refresh_entries():
        term = search_var.get().lower().strip()
        for w in list_frame.winfo_children():
            w.destroy()

        for label in entry_manager.list_entries():
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

        wrapper = ctk.CTkFrame(popup, fg_color="transparent")
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
        notes_txt.pack(fill="both", pady=(0, 0))
        add_context_menu(notes_txt, is_text=True)

        # Save callback has access to label_ent, user_ent, etc.
        def on_save():

            label = label_ent.get().strip()
            if not label:
                messagebox.showwarning("Missing Label", "You must enter a Label to save an entry.")
                return

            entry_manager.add_entry(
                label_ent.get().strip(),
                user_ent.get().strip(),
                pwd_ent.get().strip(),
                email=email_ent.get().strip(),
                notes=notes_txt.get("1.0", "end-1c").strip()
            )

            refresh_entries()
            popup.destroy()
            root.deiconify() # show main window again
            
            entry = entry_manager.get_entry(label)
            if entry:
                vault.add_entry(
                    label,
                    entry.get("username", ""),
                    entry.get("password", ""),
                    entry.get("email", ""),
                    entry.get("notes", "")
                )
                        
        # Handle closing manually
        def on_close():
            root.deiconify()
            popup.destroy()

        # ── Buttons ────────────────────────────────────────────
        btn_row = ctk.CTkFrame(wrapper, fg_color="transparent")
        btn_row.pack(fill="x", pady=(15, 0))
        ctk.CTkButton(btn_row, text="Add",    command=on_save,    width=170)\
           .pack(side="left", expand=True, padx=5)
        ctk.CTkButton(btn_row, text="Cancel", command=on_close, width=170)\
           .pack(side="left", expand=True, padx=5)
        
    # ── Entry view window ──────────────────────
    def view_entry():
        sel = selected_var.get()
        if not sel:
            messagebox.showwarning("No selection", "Select an entry first.")
            return

        entry_data = entry_manager.get_entry(sel)
        if not entry_data:
            messagebox.showerror("Not found", f"No data for “{sel}”.")
            return

        handle_edit(sel)  # launch the popup

    def handle_edit(label):
        entry_data = vault.get_entry(label)
        if entry_data:
            popup = EntryDetailsWindow(root, label, entry_data, vault)
            popup.grab_set()
            root.withdraw()
            center_window(popup, 400, 580)

            def on_close():
                root.deiconify()
                popup.destroy()
            popup.protocol("WM_DELETE_WINDOW", on_close)

    edit_button = ctk.CTkButton(root, text="Edit", command=view_entry)
    
    def delete_entry():
        sel = selected_var.get().strip()
        if not sel:
            messagebox.showwarning("No selection", "Please select an entry to delete.")
            return

        if sel not in entry_manager.list_entries():
            messagebox.showerror("Invalid Entry", f"No vault entry named “{sel}”.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", f"Delete entry “{sel}”?")
        if confirm:
            entry_manager.delete_entry(sel)
            selected_var.set("")
            refresh_entries()
    
    # ── Basic interface window ──────────────────────
    def import_entry():
        BasicInterfaceWindow(root)

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
    # register_totp_if_first_time()
    # show_login()


