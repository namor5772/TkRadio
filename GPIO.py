import tkinter as tk
import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Configure GPIO21 with a pull-up resistor

def on_button_press(channel):
    """Function to execute when the button is pressed."""
    print("Button Pressed!")  # Replace this with your desired action
    label_var.set("Button Pressed!")  # Update the GUI
    time.sleep(2)  # Pause for a second
    label_var.set("Waiting for Button Press...")  # Update the GUI    


# Set up event detection on GPIO21
GPIO.add_event_detect(21, GPIO.FALLING, callback=on_button_press, bouncetime=200)

# Create Tkinter GUI
root = tk.Tk()
root.title("GPIO Button Event Detection")
root.geometry("400x200")

label_var = tk.StringVar()
label_var.set("Waiting for Button Press...")

label = tk.Label(root, textvariable=label_var, font=("Arial", 16))
label.pack(pady=20)

# Graceful exit on closing the GUI
def on_close():
    GPIO.cleanup()  # Clean up GPIO resources
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
