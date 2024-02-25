import tkinter as tk
from tkinter import PhotoImage

def display_image():
    image_path = "mainbackground.png"  # Replace with the actual path to your image
    img = PhotoImage(file=image_path)
    label = tk.Label(root, image=img)
    label.image = img  # To prevent image from being garbage collected
    label.pack()

# Create the main Tkinter window
root = tk.Tk()
root.title("ADVANCE TECHNOLOGY")

# Call the function to display the image
display_image()

# Start the Tkinter event loop
root.mainloop()
