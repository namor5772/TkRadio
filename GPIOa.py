import RPi.GPIO as GPIO

# Set up GPIO
GPIO.setmode(GPIO.BCM)

TabButton = 21
ShiftTabButton = 20
DownButton = 16
UpButton = 12
EnterButton = 7
DeleteButton = 8
InsertButton = 25
GPIO.setup(TabButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(ShiftTabButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(DownButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(UpButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(EnterButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(DeleteButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(InsertButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

def on_TabButton_press(channel):
    print("TabButton Pressed!")

def on_ShiftTabButton_press(channel):
    print("ShiftTabButton Pressed!")

def on_DownButton_press(channel):
    print("DownButton Pressed!")

def on_UpButton_press(channel):
    print("UpButton Pressed!")

def on_EnterButton_press(channel):
    print("EnterButton Pressed!")

def on_DeleteButton_press(channel):
    print("DeleteButton Pressed!")

def on_InsertButton_press(channel):
    print("INsertButton Pressed!")

GPIO.add_event_detect(TabButton, GPIO.FALLING, callback=on_TabButton_press, bouncetime=300)
GPIO.add_event_detect(ShiftTabButton, GPIO.FALLING, callback=on_ShiftTabButton_press, bouncetime=300)
GPIO.add_event_detect(DownButton, GPIO.FALLING, callback=on_DownButton_press, bouncetime=300)
GPIO.add_event_detect(UpButton, GPIO.FALLING, callback=on_UpButton_press, bouncetime=300)
GPIO.add_event_detect(EnterButton, GPIO.FALLING, callback=on_EnterButton_press, bouncetime=300)
GPIO.add_event_detect(DeleteButton, GPIO.FALLING, callback=on_DeleteButton_press, bouncetime=300)
GPIO.add_event_detect(InsertButton, GPIO.FALLING, callback=on_InsertButton_press, bouncetime=300)


while True:
    pass
'''
def on_button_press(channel):
    """Function to execute when the button is pressed."""
    print("Button Pressed!")  # Replace this with your desired action
    label_var.set("Button Pressed!")  # Update the GUI

# Set up event detection on GPIO21
GPIO.add_event_detect(21, GPIO.FALLING, callback=on_button_press, bouncetime=200)

# Create Tkinter GUI
root = tk.Tk()
root.title("GPIO Button Event Detection")

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
'''
