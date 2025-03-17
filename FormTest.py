import tkinter as tk

def show_form():
    # Show the form window
    form_window.deiconify()

def hide_form():
    # Hide the form window
    form_window.withdraw()

# Main Window
root = tk.Tk()
root.title("Main GUI")
root.geometry("400x300+0+0")
root.configure(bg="darkgray")

# Create a secondary Toplevel form
form_window = tk.Toplevel(root)
form_window.title("Secondary Form")
form_window.geometry("390x295+13+31")

# Remove the title bar and close buttons
form_window.overrideredirect(True)

# Set the background color of the secondary window
form_window.configure(bg="lightblue")

# Add widgets to the Toplevel form
tk.Label(form_window, text="This is the secondary form!").pack(pady=10)
tk.Button(form_window, text="Close Form", command=hide_form).pack(pady=10)

# Hide the form initially
form_window.withdraw()

# Add widgets to the main window
tk.Label(root, text="Main GUI").pack(pady=10)
tk.Button(root, text="Open Form", command=show_form).pack(pady=10)

root.mainloop()
