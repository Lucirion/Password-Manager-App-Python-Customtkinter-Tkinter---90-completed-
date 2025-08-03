# import customtkinter as ctk
# from storage.vault import Vault
# from auth.qr_window import show_qr_window

# # 1) Global style setup
# ctk.set_appearance_mode("dark")           # “light” or “dark”
# ctk.set_default_color_theme("blue")       # themes: blue, dark-blue, green

# def launch_gui(vault):
#     # 2) Root window
#     root = ctk.CTk()
#     root.title("🔐 Lucirion Password Manager")
#     root.geometry("500x500")
#     root.resizable(False, False)

#     # 3) Menu bar (still tk.Menu under the hood)
#     menu = ctk.CTkOptionMenu(master=root, values=["Add Entry", "Setup Auth", "Quit"],
#                              command=lambda choice: {
#                                "Add Entry": add_entry,
#                                "Setup Auth": lambda: show_qr_window(root),
#                                "Quit": root.quit
#                              }[choice]())
#     menu.pack(pady=10)

#     # 4) Entry list as a CTkScrollableFrame + Labels
#     frame = ctk.CTkScrollableFrame(master=root, width=460, height=300)
#     frame.pack(pady=(0,20))
#     def refresh_entries():
#         for widget in frame.winfo_children(): widget.destroy()
#         for label in vault.list_entries():
#             ctk.CTkLabel(master=frame, text=label, anchor="w").pack(fill="x", padx=10, pady=2)
#     refresh_entries()

#     # 5) Bottom action buttons
#     btn_frame = ctk.CTkFrame(master=root)
#     btn_frame.pack(fill="x", pady=10, padx=20)

#     def add_entry():
#         popup = ctk.CTkToplevel(root)
#         popup.title("Add Entry")
#         popup.geometry("300x300")

#         # Input fields
#         lbl  = ctk.CTkLabel(master=popup, text="Label:")
#         lbl.pack(pady=(20,5))
#         ent1 = ctk.CTkEntry(master=popup)
#         ent1.pack(pady=5, padx=20)
#         ctk.CTkLabel(master=popup, text="Username:").pack(pady=(10,5))
#         ent2 = ctk.CTkEntry(master=popup)
#         ent2.pack(pady=5, padx=20)
#         ctk.CTkLabel(master=popup, text="Password:").pack(pady=(10,5))
#         ent3 = ctk.CTkEntry(master=popup, show="*")
#         ent3.pack(pady=5, padx=20)

#         def save():
#             vault.add_entry(ent1.get(), ent2.get(), ent3.get())
#             refresh_entries()
#             popup.destroy()

#         ctk.CTkButton(master=popup, text="Save", command=save).pack(pady=20)

#     def view_entry():
#         sel = frame.winfo_children()[0]  # just example; replace with real selection logic
#         # …show details…

#     def delete_entry():
#         # implement deletion & refresh
#         pass

#     for txt, cmd in [("Add", add_entry), ("View", view_entry),
#                      ("Delete", delete_entry), ("Quit", root.quit)]:
#         ctk.CTkButton(master=btn_frame, text=txt, command=cmd).pack(side="left", expand=True, padx=5)

#     root.mainloop()


# if __name__ == "__main__":
#     from cryptography.fernet import Fernet
#     key = b'6tLqQ-lqwz0QO-GU0UxLd5ZgoJH_YU9dMm3jxYUtVSo=' 
#     vault = Vault(key)
#     launch_gui(vault)

