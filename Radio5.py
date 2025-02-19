# all part of the Python standard libraries, with RPI.GPIO pre installed as part of the Raspian os
import subprocess
import time
import RPi.GPIO as GPIO
import os;    

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Create the full filepath to the saved radio station file
filename = 'savedRadioStation.txt'
filepath = os.path.join(script_directory, filename)
print(f'The file {filepath} stores the last streamed station number.')

# Use BCM GPIO numbering 
GPIO.setmode(GPIO.BCM)

# Define Raspberry Pi pins that go to the interface circuit board
button_pin = 26
led0_pin = 19
led1_pin = 13
led2_pin = 6

# Setup the pins
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(False)
GPIO.setup(led0_pin, GPIO.OUT)
GPIO.setup(led1_pin, GPIO.OUT)
GPIO.setup(led2_pin, GPIO.OUT)

# setup the leds to be initially all off
GPIO.output(led0_pin,GPIO.LOW)
GPIO.output(led1_pin,GPIO.LOW)
GPIO.output(led2_pin,GPIO.LOW)

# 2D array of radio station information in [short name, long name, url] format
# clearly this can be varied if you wish to listen to different 7 stations
aStation = [
    ["2LRW","ABC Radio Sydney","https://live-radio01.mediahubaustralia.com/2LRW/mp3/"],
    ["5LRW","ABC Radio National","https://live-radio01.mediahubaustralia.com/2RNW/mp3/"],
    ["PBW","ABC NewsRadio","https://live-radio01.mediahubaustralia.com/PBW/mp3/"],
    ["2FMW","ABC Classic Sydney","https://live-radio01.mediahubaustralia.com/2FMW/mp3/"],
    ["FM2W","ABC Classic 2","https://live-radio01.mediahubaustralia.com/FM2W/mp3/"],
    ["WSFM","GOLD 101.7","https://playerservices.streamtheworld.com/api/livestream-redirect/ARN_WSFM.mp3"],
    ["SMOOTH953","Smooth FM Sydney 95.3","https://playerservices.streamtheworld.com/api/livestream-redirect/SMOOTH953.mp3"]
]

# some utility global variables
vlc_path = "/usr/bin/cvlc" # full path to cvlc
Running = False # flag True if radio station is streaming
nStation = 0 # station number (0 is the "no radio streaming" station)
startup = True # True when radio initially powered up 

print("Radio stream interface")

while True:

    if ((GPIO.input(button_pin) == GPIO.LOW) or (startup)):
        time.sleep(0.2) # pathetic debouncing code

        if (startup):
            # load saved station number from file when radio powered up
            try:
                with open(filepath, 'r') as file:
                    nStation = int(file.read())
            except FileNotFoundError:
                print(f'Error: The file {filepath} does not exist.')
                nStation = 0
        else:
            # increment station number modulo 8 when button pressed
            if nStation == 7:
                nStation = 0
            else:
                nStation = nStation +1

            # save station number to file (if radio powered off when playing this station)
            with open(filepath, 'w') as file:
                file.write(str(nStation))

        # display the station number in binary
        bit0 = (nStation >> 0) & 1 # LSB
        bit1 = (nStation >> 1) & 1 # middle bit
        bit2 = (nStation >> 2) & 1 # MSB
        GPIO.output(led0_pin,bit0)
        GPIO.output(led1_pin,bit1)
        GPIO.output(led2_pin,bit2)
        print("Button pressed, Station: ",nStation)    

        if nStation > 0:
            stream_url = aStation[nStation-1][2]
            stream_longName = aStation[nStation-1][1]

        if nStation == 0:
            if Running:    
                process.terminate()
            Running = False
            print("No streaming")

        elif nStation == 1:
            # started new process, but no need to terminate previous one since already terminated
            process = subprocess.Popen([vlc_path, stream_url])
            Running = True
            print("Started streaming radio station: " + stream_longName)

        else:
            if (not startup):
                # need to terminate current process, before starting new one
                process.terminate()
                
            process = subprocess.Popen([vlc_path, stream_url])
            Running = True
            print("Started streaming radio station: " + stream_longName)

        startup = False    

