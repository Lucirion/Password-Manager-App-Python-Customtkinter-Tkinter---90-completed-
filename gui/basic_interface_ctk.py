import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, simpledialog, messagebox
from typing import Union
from gui.basic_entry_view_window import BasicEntryDetailsWindow
from gui.basic_add_entry_window  import BasicAddEntryWindow
from shared_functions import BasicEntryManager

# ── Appearance ─────────────────────────────────────────
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ── Centering helper ───────────────────────────────────
def center_window(win, width, height):
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw - width) // 2
    y = (sh - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

# ── Main Interface Class ───────────────────────────────
class BasicInterfaceWindow(ctk.CTkToplevel):
    def __init__(self, master: Union[tk.Tk, ctk.CTk]):
        super().__init__(master)
        self._master_root = master
        master.withdraw()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.title("🔐 Lucirion Basic Password Manager Version")
        self.geometry("600x520")
        center_window(self, 600, 520)
        self.resizable(False, False)

        # ── Header Frame ───────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(10, 5))

        # Dark/Light toggle on the left
        self.appearance_var = ctk.IntVar(value=1)
        self.theme_switch = ctk.CTkSwitch(
            master=header,
            text="🌙 Dark Mode",
            variable=self.appearance_var,
            command=self.toggle_appearance,
            switch_width=34,
            switch_height=18,
            font=ctk.CTkFont(size=12, weight="bold"),
            progress_color="light blue",
            button_color="light blue",
            text_color="#969696"
        )
        self.theme_switch.pack(side="left")

        # Settings dropdown on the right
        self.dropdown_var = ctk.StringVar(value="Settings")
        self.dropdown = ctk.CTkOptionMenu(
            master=header,
            variable=self.dropdown_var,
            values=["Import", "Export", "Return"],
            command=self._on_dropdown_change,
            width=120,
            font=ctk.CTkFont(size=13, weight="bold"),
            dropdown_font=ctk.CTkFont(size=12),
            fg_color="#444444",
            text_color="#DDDDDD",
            button_color="#666666",
            button_hover_color="#777777",
        )
        self.dropdown.pack(side="right")
        
        # ── Core Logic & UI Build ────────────────────────────
        self.entry_manager = BasicEntryManager()
        self.search_var = ctk.StringVar()
        self.selected_label = ctk.StringVar()
        self._build_ui()
        self.search_var.trace_add("write", lambda *_: self.refresh_entries())
        self.refresh_entries()

    def _on_close(self):
        # self.master.deiconify()
        self.destroy()
        self._master_root.destroy()

    def _build_ui(self):
        # Search bar
        ctk.CTkLabel(self, text="Search Labels:", anchor="w")\
            .pack(fill="x", padx=20, pady=(20, 5))

        ctk.CTkEntry(
            self,
            textvariable=self.search_var,
            placeholder_text="Type to filter…"
        ).pack(fill="x", padx=20)

        # Scrollable list of entries
        self.entry_list_frame = ctk.CTkScrollableFrame(self, width=560, height=300)
        self.entry_list_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Action buttons
        btn_frame = ctk.CTkFrame(master=self)
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        for action in ["Add", "View", "Delete"]:
            ctk.CTkButton(
                btn_frame,
                text=action,
                width=170,
                command=lambda a=action: self.handle_action(a)
            ).pack(side="left", expand=True, padx=5)

    def refresh_entries(self):
        # clear existing buttons
        for w in self.entry_list_frame.winfo_children():
            w.destroy()

        term = self.search_var.get().lower().strip()
        for label in self.entry_manager.list_entries():
            if term in label.lower():
                ctk.CTkRadioButton(
                    master=self.entry_list_frame,
                    text=label,
                    variable=self.selected_label,
                    value=label
                ).pack(fill="x", padx=10, pady=4)

    def handle_action(self, action):
        if action == "Add":
            self.withdraw()
            BasicAddEntryWindow(self, self.entry_manager, self._on_popup_close)

        elif action == "View":
            self.view_entry()

        elif action == "Delete":
            self.delete_entry()

    def _on_popup_close(self):
        self.refresh_entries()
        self.deiconify()

    def view_entry(self):
        label = self.selected_label.get().strip()
        if not label:
            messagebox.showwarning("No selection", "Please select an entry first.")
            return
        data = self.entry_manager.get_entry(label)
        if not data:
            messagebox.showerror("Not found", f"No data found for “{label}”.")
            return
        data = self.entry_manager.get_entry(label)
        self.withdraw()
        popup = BasicEntryDetailsWindow(root=self.master, master=self, label=label, entry_data=data, editable=True)
        center_window(popup, 500, 600)

    def delete_entry(self):
        label = self.selected_label.get().strip()
        if not label:
            messagebox.showwarning("No selection", "Please select an entry first.")
            return
        if messagebox.askyesno("Confirm Delete", f"Delete “{label}”?"):
            if self.entry_manager.delete_entry(label):
                self.selected_label.set("")
                self.refresh_entries()
            else:
                messagebox.showerror("Error", f"Could not delete “{label}”.")
                pass

    # ── dropdown handler ───────────────────────────────────
    
    def _on_dropdown_change(self, choice):
        if choice == "Import":
            self._basic_import()
        elif choice == "Export":
            self._basic_export()
        elif choice == "Return":
            self._return_to_main()
        self.dropdown_var.set("Settings")

    # ── Menu Actions ──────────────────────────────────────
    def _basic_import(self):

        # 1) Ask the user to pick a file
        fname = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json")]
        )
        if not fname:
            return

        # 2) Prompt for the label before importing
        label = simpledialog.askstring(
            "Import Label",
            "Enter a label for this imported entry:"
        )
        if label is None or not label.strip():
            messagebox.showerror(
                "Import Error",
                "You must provide a non-empty label."
            )
            return
        label = label.strip()

        # 3) Delegate to your manager, passing file path + label
        success = self.entry_manager.import_entries(fname, label)

        # 4) Refresh UI and give feedback
        if success:
            self.refresh_entries()
            messagebox.showinfo(
                "Import Successful",
                f"Entry “{label}” added to vault."
            )
        else:
            messagebox.showerror(
                "Import Failed",
                "Could not import—check file format or required fields."
            )

    def _basic_export(self):
        fname = filedialog.asksaveasfilename(
            title="Export Entries",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if fname:
            exported_count = self.entry_manager.export_as_text(fname)
            if exported_count:
                messagebox.showinfo("Export Successful", f"{exported_count} entries saved to:\n{fname}")

            else:
                messagebox.showerror("Export Failed", "There was a problem saving entries.")

    def _return_to_main(self):
        self._master_root.deiconify()
        self.destroy()

    # ── Theme toggle handler ─────────────────────────────────
    def toggle_appearance(self):
        # Flip between Dark (1) and Light (0)
        mode = "Dark" if self.appearance_var.get() == 1 else "Light"
        ctk.set_appearance_mode(mode)
        # Update the switch text to match
        self.theme_switch.configure(
            text="🌙 Dark Mode" if mode == "Dark" else "🌞 Light Mode"
        )
# ── Standalone Launch (for testing) ──────────────────────
if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    app = BasicInterfaceWindow(root)
    app.mainloop()
