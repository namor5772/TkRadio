import tkinter as tk
import RPi.GPIO as GPIO

# --- GPIO Setup ---
GPIO.setmode(GPIO.BCM)  # Using BCM numbering

# Define GPIO pins for the rotary encoder and push button.
CLK_PIN = 16   # Connect to CLK (A) of the encoder
DT_PIN  = 20   # Connect to DT (B) of the encoder
SW_PIN  = 21  # Connect to the push button

# Setup pins with internal pull-ups.
GPIO.setup(CLK_PIN, GPIO.IN)#, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT_PIN, GPIO.IN)#, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW_PIN, GPIO.IN)#, pull_up_down=GPIO.PUD_UP)

# Global counter for rotation steps
counter = 0
# Record the initial state of the CLK pin.
last_clk_state = GPIO.input(CLK_PIN)

# --- Tkinter (GUI) Setup ---
root = tk.Tk()
root.title("Rotary Encoder GUI")

# Create a label to display actions or the counter value.
label = tk.Label(root, text="Counter: 0", font=("Helvetica", 24))
label.pack(padx=20, pady=20)

# To update the label from the GPIO callbacks (which run on a different thread),
# we define a safe update function that uses `after()` to schedule GUI updates.
def safe_update(new_text):
    label.config(text=new_text)

def update_label(new_text):
    # Use root.after to safely update the GUI from outside the main thread.
    root.after(0, safe_update, new_text)

# --- Callback Functions ---
def rotary_callback(channel):
    """Callback for rotary encoder rotation."""
    global counter, last_clk_state
    current_clk = GPIO.input(CLK_PIN)
    current_dt  = GPIO.input(DT_PIN)

    # When the state of CLK changes, determine rotation direction.
    # This simple method checks the state of DT relative to CLK.
    if current_clk != last_clk_state:
        # If DT is different from current CLK state, rotation is clockwise.
        if current_dt != current_clk:
            counter += 1
            update_label("Clockwise: " + str(counter))
        else:
            counter -= 1
            update_label("Counter-clockwise: " + str(counter))
    last_clk_state = current_clk

def button_callback(channel):
    """Callback for push button press."""
    update_label("Button pressed!")

# --- GPIO Event Detection ---
# Detect state changes on the CLK pin for rotational events.
GPIO.add_event_detect(CLK_PIN, GPIO.BOTH, callback=rotary_callback, bouncetime=3)
# Detect a falling edge on the switch pin for button press.
GPIO.add_event_detect(SW_PIN, GPIO.FALLING, callback=button_callback, bouncetime=200)

# --- Start the Tkinter Main Loop ---
try:
    root.mainloop()
finally:
    GPIO.cleanup()  # Clean up the GPIO pins when exiting.
