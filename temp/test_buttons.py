import customtkinter as ctk

print("CTk version:", ctk.__version__)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.geometry("300x100")

frame = ctk.CTkFrame(root)
frame.pack(fill="x", padx=10, pady=10)

btn = ctk.CTkButton(
    master=frame,
    text="Test",
    width=100,     # pixels?
    height=40,     # pixels?
    fg_color="#1FA526",
    hover_color="#158A28",
    text_color="white"
)
btn.pack(side="left", expand=True, fill="both", padx=5)

root.mainloop()
