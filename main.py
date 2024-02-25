import tkinter as tk
from tkinter import PhotoImage

def display_image():
    image_path = "mainbackground.png"  # Replace with the actual path to your image
    img = PhotoImage(file=image_path)
    label = tk.Label(window, image=img)
    label.image = img  # To prevent image from being garbage collected
    label.pack()

# Create the main Tkinter window
window = tk.Tk()
window.title("Youtube Video Downloader")

# Set window size and position
window_width = 1248
window_height = 768
full_width = window.winfo_screenwidth()
full_height = window.winfo_screenheight()
place_width = int(full_width - full_width / 2 - window_width / 2)
place_height = int(full_height - full_height / 2 - window_height / 2) - 40
window.geometry(f"{window_width}x{window_height}+{place_width}+{place_height}")

# Call the function to display the image
display_image()

# Start the Tkinter event loop
window.mainloop()
