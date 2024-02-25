from customtkinter import *
from tkinter import *
import subprocess

# wait for 20 seconds

def hand_program():
    window.destroy()
    os.system("HandGesture.py")

def face_program():
    window.destroy()
    os.system("face.py")

def ai_program():
    window.destroy()
    os.system("ai.py")

window = CTk()
window.title("ADVANCE TECHNOLOGY")

# Set window dimensions and position
window_width = 1000
window_height = 610
full_width = window.winfo_screenwidth()
full_height = window.winfo_screenheight()
place_width = int(full_width - full_width / 2 - window_width / 2)
place_height = int(full_height - full_height / 2 - window_height / 2)
window.geometry(f"{window_width}x{window_height}+{place_width}+{place_height}")

window.resizable(False, False)

# Load and display an image
image_path = "mainbackground.png"  # Replace with the actual path to your image
img = PhotoImage(file=image_path)

# Create a label to display the image
image_label = Label(window, image=img)
image_label.pack()

CTkButton(master=window, text="GET START", width=120, height=30, fg_color="#ac74f9", hover_color="#dc85fc", command=face_program).place(relx=0.179, rely=0.7)
CTkButton(master=window, text="GET START", width=120, height=30, fg_color="#ac74f9", hover_color="#dc85fc", command=ai_program).place(relx=0.705, rely=0.7)
CTkButton(master=window, text="GET START", width=140, height=40, fg_color="#ac74f9", hover_color="#dc85fc", command=hand_program).place(relx=0.433, rely=0.73)

window.mainloop()
