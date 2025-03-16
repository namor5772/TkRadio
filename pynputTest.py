from tkinter import Tk, Button
from tkinter.ttk import Combobox
import time

def simulate_combobox_navigation():
    # Set focus to the combobox
    combobox.focus()
    # Simulate pressing the <Down> key to open the dropdown
    combobox.event_generate("<Down>")

    # Allow time for the dropdown to open, then navigate to the next item
    root.after(1000, lambda: combobox.event_generate("<Down>"))

    # Allow time for the dropdown to open, then navigate to the next item
    root.after(2000, lambda: combobox.event_generate("<Down>"))

    # Allow time for the dropdown to open, then navigate to the next item
    root.after(3000, lambda: combobox.event_generate("<Down>"))

    # Allow time for the dropdown to open, then navigate to the next item
    root.after(4000, lambda: combobox.event_generate("<Down>"))
    
    # Allow time for the dropdown to open, then navigate to the next item
    root.after(5000, lambda: combobox.event_generate("<Up>"))
    
    # Allow time for the dropdown to open, then navigate to the next item
    root.after(6000, lambda: combobox.event_generate("<Up>"))
    
    # Allow time for the dropdown to open, then navigate to the next item
    root.after(7000, lambda: combobox.event_generate("<Up>"))

    # Allow time for the dropdown to open, then navigate to the next item
    root.after(9000, lambda: combobox.event_generate("<Return>"))

# Tkinter setup
root = Tk()
root.title("Simulate Combobox Navigation")
root.geometry("300x150")

# Create a combobox
combobox = Combobox(root)
combobox.pack(pady=20)
combobox['values'] = ("Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "Option 6")

# Button to trigger simulation
#simulate_button = Button(root, text="Simulate Navigation", command=simulate_combobox_navigation)
#simulate_button.pack(pady=30)

# Schedule the function to run after 3000 milliseconds (3 seconds)
root.after(5000, simulate_combobox_navigation)



root.mainloop()
