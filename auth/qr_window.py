import tkinter as tk
from PIL import ImageTk, Image
import qrcode
from totp import get_provisioning_uri


def show_qr_window():
    # Initialize Tkinter root
    base_root = tk.Tk()
    base_root.withdraw() # Hide the main root window

    uri = get_provisioning_uri()
    qr_img = qrcode.make(uri)

    # Create a popup window
    global root
    root = tk.Toplevel()
    root.title("📲 Register Authenticator")
    root.geometry("600x650")
    root.resizable(False, False)

    def on_close():
        print("Window closed")  # Optional: Add cleanup logic or logging
        root.destroy()
        base_root.destroy()

    tk.Label(root, text="Scan this QR with your app:").pack(pady=10)

    # Convert PIL image to Tkinter-compatible image
    qr_tk = ImageTk.PhotoImage(qr_img)
    qr_label = tk.Label(root, image=qr_tk)
    qr_label.image = qr_tk  # Keep a reference
    qr_label.pack(pady=10)

    tk.Button(root, text="Close", command=on_close).pack(pady=10)
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Start the loop
    base_root.mainloop()

show_qr_window()
