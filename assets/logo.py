import os
from PIL import Image, ImageTk

def load_logo(size=(120, 120)):
    """
    Load and resize the app logo image for Tkinter.
    Returns an ImageTk.PhotoImage object.
    """
    logo_path = os.path.join(os.path.dirname(__file__), "bank_logo.png")

    if not os.path.exists(logo_path):
        print("Logo image not found in assets folder.")
        return None

    try:
        image = Image.open(logo_path)
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error loading logo: {e}")
        return None

