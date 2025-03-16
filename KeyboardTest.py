import tkinter as tk
from tkinter import ttk
import keyboard

# Create a Tkinter window
root = tk.Tk()
root.title("Keyboard with Combobox")
root.geometry("400x300")  # Set window size (width x height)

# Add a Combobox
values = ["Option 1", "Option 2", "Option 3"]
combobox = ttk.Combobox(root, values=values)
combobox.pack(pady=20)

def select_next_option():
    # Focus on the combobox
    combobox.focus_set()
    # Simulate pressing "Down" to move through combobox options
    keyboard.press_and_release("down")

def select_option_and_submit():
    # Simulate pressing "Return" to select an option
    combobox.event_generate("<Return>")

# Simulate selecting the next option on button click
button_next = tk.Button(root, text="Next Option", command=select_next_option)
button_next.pack(pady=40)

# Simulate submitting the selected option
button_submit = tk.Button(root, text="Submit Option", command=select_option_and_submit)
button_submit.pack()

# Run the Tkinter main loop
root.mainloop()
