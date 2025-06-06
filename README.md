# TkRadio

### **The best way to load this software and build instructions is to Clone this Git Repository using Visual Studio Code.**

Here the building of an Internet Radio will be described in detail.
The software uses Python with tkinter and selenium, while the hardware is based on a Raspberry Pi 5.

As a standalone app (RadioSelenium-Windows11.py) it can also be run under the Windows 11 OS (or other Linux versions). In those cases the installation of additional Python modules and other software setup will be significantly different and not described here (though somewhat in the [Windows setup](#windows-setup) section). The best way to do this in these cases is to try to run it and then correct errors by installing required modules or adjusting settings. Wifi/internet connections and bluetooth speakers have to be managed explicitly through the OS. RadioSelenium-RP5.py is the file for the Raspberry Pi hardware.

The radio software has access to 178 radio stations (currently) with about half from Australia. It accesses these streams via the stations websites via the FireFox browser using selenium for automation. When a station is streamed its logo is displayed. In addition if available the stations program text is displayed together with the programs graphic (eg. the record sleeve for the album from which the current song is playing). The default is for this program information to be refreshed approximately every 22 seconds while the stream is playing.

For convenience you can create a playlist for up to 18 stations consisting of buttons that display the station logo. With a playlist button is selected/in focus pressing the [Delete] key deletes the radio station assigned to that playlist button leaving the graphic blank. Similarily when the [Insert] key is pressed the station that was previously selected from the combobox is assigned to the playlist button overwiting the previous graphic.

Occasionally internet/website issues might cause a station to fail to stream or not correctly refresh the program text and graphic. This can almost always be resolved by just selecting the station again.

Details of the station (from the playlist) currently playing is saved to a file so that if the program is restarted it will automatically start streaming that station. The current playlist is also saved to file after any changes so that it is displayed after restart.

The RadioSelenium-RP5.py python file (or RadioSelenium-Windows11.py) can be launched from any directory as long as it contains the Images subdirectory and its files from the GitHub repository. The playlist.txt, savedRadioStation.txt, bluetooth.txt and pollflag.txt files are assumed to be in the same directory as well.

In the Raspberry Pi case the softwares gui also has a secondary form for pairing/connecting to bluetooth speakers (the default being external speakers attached to the 3.5mm stereo jack of the Raspberry Pi). In addition the connection to the wifi network can also be explicitly made through this apps form. This is necessary since the app is dedicated solely to the Raspberry Pi and is the only interface to the physical internet radio. As such can only use buttons since no mouse or keyboard is assumed to be connected.

Below is an image of the applications main and setup forms.
![app GUI image](ImagesDocs/imageGUI.png)

## Hardware

1. We use a Raspberry Pi 5B with 4GB of memory
1. We use an custom heatsink with  fans since the Raspberry Pi gets hot
1. We use USB powered (by the Raspberry Pi) stereo speakers that are plugged into the USB socket (if the speakers have a 3.5mm plug you must use a converter cable).
1. We use a wireless keyboard and mouse to control the software. The dongle is plugged into a USB port.
1. We use a monitor that is plugged in into the micro HDMI port of the Raspberry Pi. Use an adaptor if the HDMI cable has a standard connector.

*** COMPLETE

## Software Setup

Here we detail ALL the software needed for this project. Starting with the blank micro SD card that will contain all the software running on the Raspberry Pi.

1. Install the OS on a 32GB SanDisk Ultra 10 micro SD card (or equivalent). I used a Windows 11 PC with the **Raspberry Pi Imager v1.8.5** app, selecting the Raspberry Pi OS (64-bit) Debian GNU/Linux 12 (bookworm) OS. In the setup use:

    ```text
    hostname:             rpi
    username:             {username}
    password:             {password}
    SSID:                 {SSID}    password:             {SSID password}
    Wireless LAN country: AU
    locale:               Australia/Sydney
    keyboard:             us
    ```

1. Place the SD card into the Raspberry Pi which is assumed to have a wireless mouse & keyboard connected, a HDMI monitor connected and USB powered stereo speakers connected to the 3.5mm jack. Power up the Raspberry Pi (by plugging in a USB-C 3A rated power pack). If everthing works it should boot into the GUI. Then:
    - Confirm that the system connects to the internet or set it up via the taskbar.
    - Make the system have max volume using the slider available on the taskbar.
    - Open a terminal window and run the following commands:

        ```sh
        sudo apt update
        sudo apt full-upgrade
        sudo apt autoremove
        sudo reboot        
        ```

1. Download the GitHub repository directory TkRadio and all its contents (including subdirectories) to your /**home/{username)/** directory. You can do that via a USB stick or using Visual Studio Code to clone this repository directly to the Raspberry Pi you are using.
1. Install latest versions of Idle & Python
   - Python already installed with OS - Version 3.11.2
   - Install Idle from a terminal window with this command:

        ```sh
        sudo apt-get install idle
        ```

        When you start Idle from the taskbar, the Help => About IDLE menu selection should show you that:

        ```sh
        Python version: 3.11.2
        Tk version: 8.6.13
        IDLE version: 3.11.2
        ```

1. Install the Python Imaging Library (PIL) from the terminal with:

    ```sh
    sudo apt-get update
    sudo apt-get install python3.pil python3.pil.imagetk
    ```

1. Install the Selenium library for Python from the terminal with:

    ```sh
    sudo apt_get install python3_pip
    python3 -m venv selenium_env
    source selenium_env/bin/activate
    pip install selenium
    sudo apt-get install python3-selenium
    ```

1. Install the gekodriver (necessary for selenium to operate with the FireFox browser), Note: FireFox is already installed with the OS:

    From the <https://github.com/mozilla/gekodriver/releases> repository or otherwise (from this repository) download the tar.gz file **gekodriver-v0.36.0-linux-aarch64.tar.gz** file to the **/home/{username}/Downloads** directory and then from a terminal window run:

    ```sh
    cd /
    cd /home/{username}/Downloads
    tar -xvzf gekodriver-v0.36.0-linux-aarch64.tar.gz
    sudo mv gekodriver /usr/local/bin
    gekodriver --version
    ```

1. Open the terminal and use **alsamixer** to adjust the audio level to max. This is needed when using a Bluetooth speaker.

1. Set audio control system to PulseAudio as follows:
    run "sudo raspo-config" from a terminal
    Press Down key 5x to [6 Advanced Options] then press Enter key
    Press Down key 6x to [A7 Audio Config] then press Enter key
    You will be at [1 PulseAudio], press the Enter Key twice.
    Back at the main menu press the Tab key x2 to land on <Finish>
    Press the Enter key to return to the terminal

1. Remove the Bluetooth plugin from the taskbar as follows:
    Right mouse click an unoccupied spot on the taskbar
    A popup appears. Select the [Add / Remove Plugins...] option (with Left mouse click).
    A dialog box titled "Add / Remove Plugins" appears.
    Select the "Bluetooth" entry in either the [Left Side] or [Right Side] columns (with left mouse click)
    Left mouse click the [Remove] button
    Left mouse click the [OK] button

    This prevents popups from appearing on the main window when the app is performing bluetooth
    related actions. They take focus away from the app windows which causes problems and is annoying!

1. NOT NECESSARY: Install the Python pybluez module with:

    ```sh
    sudo apt install bluetooth libbluetooth-dev
    sudo apt autoremove
    sudo apt install python3-bluez
    ```

    In a Python script it is then accessed as: **import bluetooth**

1. NOT NECESSARY: Install the Python pynput module with:

    ``` sh
    cd /
    sudo apt install python3-pynput 
    ```

1. Setup auto-start:
    - create a directory named **autostart** in the directory **/home/{username}/.config** (which is hidden, so you need to use **ls -al** to see its contents from the /home/{username} directory)  
    - in that **autostart** directory use **sudo nano** via a terminal to create a file called **autoRadio.desktop** with the following content:

    ```sh
    [Desktop Entry]
    Type=Application
    Exec=/usr/bin/idle -r /home/{username}/TkRadio/RadioSelenium-RP4B.py
    ```

    You could also just use file available in the repository, but off course you will need to replace {username} with the text relevant to your system.

1. Restart the Raspberry Pi by unplugging power and plugging it back in after a short delay, OR just type **sudo reboot** in a terminal window. If everything was correctly done then after about a minute delay the Radio App should start streaming a station (Make sure the volume is turned up on the speakers!)

1. To make this application more immmersive change the display resolution to 800x600 which matches the size of the apps form and then position the task bar at the bottom of the screen and make its icon size very large (ie. 48x48).

## Windows setup

1. installing the **selenium** Python module:

    In a terminal window type:

    ``` sh
    cd /
    pip install selenium 
    ```

He we describe how to setup the launch of this app through a desktop shortcut.

On GUI Right click mouse to open popup menu, select: New => Shortcut
A dialog box appears. Into the "Type the location of the item:" text box paste the following:

```text
C:\Users\grobl\AppData\Local\Programs\Python\Python312\pythonw.exe "C:\Users\grobl\OneDrive\GitRepos\TkRadio\RadioSelenium-Windows11.py"
```

Press the [Next] button.
In the following text box titled "Type a name for this shortcut" type "RADIO" (replacing "pythonw.exe").
Press the [Finish] button.
This new shortcut then appears on the desktop with the Python icon. This can be changed if you desire. Interestingly when examining the Properties of this shortcut we have (automatically generated) the following properties:

```text
Target location: Python312
Target: C:\Users\grobl\AppData\Local\Programs\Python\Python312\pythonw.exe "C:\Users\grobl\OneDrive\GitRepos\TkRadio\RadioSelenium-Windows11.py"
Start in: C:\Users\grobl\AppData\Local\Programs\Python\Python312
```

Clearly the will vary depending on directories containing the Python script and the Python executable.

## Python Script

The actual gui application that implements the internet radio is the python script [RadioSelenium-RP4B.py](RadioSelenium-RP4B.py) located in the /home/{username}/TkRadio directory. It is displayed below:

```Python
import subprocess
import inspect
import tkinter as tk
import time
import urllib.request
import requests
import os
import csv

from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# START #######################################################
# SETUP VARIOUS GLOBAL VARIABLES AND THE FIREFOX BROWSER OBJECT 

# Get the directory of the current script & then assumed directory for Images
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = script_dir.replace("\\","/")
pathImages = script_dir + "/Images"
print(f"The Images path is: {pathImages}")

# Create the full filepath to the saved radio station file
filename = 'savedRadioStation.txt'
filepath = os.path.join(script_dir, filename)
print(f'The file {filepath} stores the last streamed station before shutdown.')

# Create the full filepath to the saved playlist file
filename2 = 'playlist.txt'
filepath2 = os.path.join(script_dir, filename2)
print(f'The file {filepath2} stores the playlist before shutdown.')

# Open and setup FireFox browser
firefox_options = Options()
# below is the headless width and height, if not headless +15 & 8 respectively
firefox_options.add_argument("--width=1280")
firefox_options.add_argument("--height=917")
#firefox_options.add_argument("-headless")  # Ensure this argument is correct
browser = webdriver.Firefox(options=firefox_options)

# 'cleans' browser between opening station websites
#refresh_http = "http://www.ri.com.au" # use my basic "empty" website
refresh_http = "https://www.blank.org/" # use a basic "empty" website

# global graphis position variables
Ydown = 63
Ygap = 10;  Ygap2 = 110+Ydown; Ygap3 = 110+Ydown
Xgap = 560-70; Xgap2 = 560-70; Xgap3 = 560-70
Xprog = 300

# global variables for combobox selection indexes & button related
numButtons = 18
sizeButton = 62
combobox_index = -1
buttonIndex = -1
addFlag = False
iconSize = 160
eventFlag = True # if on_select & on_select2 are called from event
stopFlag = False
selected_value = "INITIAL"
selected_value_last = "INITIAL"
selected_index = -1
startTime = time.time()
endTime = 0.0
refreshTime = 10.0 # in seconds for program info
stationShort = ""
station = ""
needSleep = 5 # can be less on faster machines
pressButton = True # flag for how stream is started

# END #########################################################
# SETUP VARIOUS GLOBAL VARIABLES AND THE FIREFOX BROWSER OBJECT 


# Define a custom event class
class CustomEvent:
    def __init__(self, event_type, widget, data=None):
        self.type = event_type
        self.widget = widget
        self.data = data


# START ##################################################
# DEFINE VARIOUS CORE FUNCTIONS THAT STREAM RADIO STATIONS
#
# There are 8 of them: Radio1 ... Radio7 & Commercial1. They are needed because the 
# websites used to stream individual radio stations can differ in their layout, but many are
# similar so can use the same code. Radio1...Radio7 are for the ABC stations, while Commercial1
# is for the commercial stations.

def Radio1(br,Num,sPath):
    if eventFlag:
        # use inspect to get the name of the calling function
        # this is used to generate the station name and logo
        stack = inspect.stack()
        global station 
        station = inspect.stack()[1].function
        logo = station + ".png"
        print(logo)
        print("--")

        # go to the station website
        br.get(refresh_http)
        time.sleep(1)
        br.get(sPath)
        time.sleep(needSleep)

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # This where the streaming of the radio station is accomplished
        buttonStream = be.find_element(By.XPATH,'/html/body/div[1]/div/div/div/main/div[1]/div/div/div[1]/div/div[2]/div[12]/div[4]/div/div[1]')
        buttonStream.click()
        time.sleep(1)

        # get station logo
        image_path3 = pathImages
        image_path3 = image_path3 + "/" + logo
        image = Image.open(image_path3)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon if adding station to playlist 
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")

        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    # get program image
    try:
        img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/img')
        img2_url = img2_element.get_attribute("src")
        image2_path = pathImages + "/presenter.jpg"
        urllib.request.urlretrieve(img2_url, image2_path)
    except NoSuchElementException:
        print("Image element not found on the webpage.")            
        # Display a blank image
        image2_path = pathImages + "/Blank.png"

    # Display the program image as given in the scaled_image2
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    crop_box2 = (width2-height2,0,width2,height2)
    cropped_image2 = image2.crop(crop_box2)
    scaled_image2 = cropped_image2.resize((Xprog, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    if station == "ABC_Classic2":
        label2.place(x=Xgap, y=Ygap3)  # Adjust the position
    else:
        label2.place(x=Xgap, y=Ygap2)  # Adjust the position
    
    # get station details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": "view-live-now popup"})
    if fe is not None:
        fe1 = fe.get_text(separator="*", strip=True)
    else:
        fe1 = "None"

    # Remove irrelevant info, starting with [*More]
    sub = "*More"
    pos = fe1.find(sub)
    if pos != -1:
        fe1 = fe1[:pos]
    sub = "More from*"
    fe1 = fe1.replace(sub,"")
    sub = "*."
    fe1 = fe1.replace(sub,"")
        
    # append program details to station details    
    fe = soup.find(attrs={"class": "playingNow"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No specific item playing"
    fe3 = fe1+"*"+fe2
    return fe3


def Radio2(br,Num,sPath):
    if eventFlag:
        # go to the station website
        br.get(refresh_http)
        time.sleep(1)
        br.get(sPath)
        time.sleep(needSleep)

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # Select timezone for stream (specific to this actual ABC radio website)
        for _ in range(3):
            be.send_keys(Keys.TAB)
        be.send_keys(Keys.ENTER)
        for _ in range(4):
            be.send_keys(Keys.UP)
        for _ in range(Num):
            be.send_keys(Keys.DOWN)
        be.send_keys(Keys.ENTER)

        # This where the streaming of the radio station is accomplished
        buttonStream = be.find_element(By.XPATH,'/html/body/div[1]/div/div/div/main/div[1]/div/div/div[2]/div/div[2]/div[12]/div[4]/div/div[1]')
        buttonStream.click()
        time.sleep(1)

        # get station logo
        image_path2 = pathImages + "/ABC_Radio_National.png"
        image = Image.open(image_path2)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon if adding station to playlist 
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")

        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    # get program image
    img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div/div/header/div/div/img')
    img2_url = img2_element.get_attribute("src")
    image2_path = pathImages + "/presenter.jpg"
    urllib.request.urlretrieve(img2_url, image2_path)

    # Display the program image as given in the scaled_image2
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    width = int(Xprog*width2/height2)
    scaled_image2 = image2.resize((width, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap3-(width-Xprog), y=Ygap2)  # Adjust the position
    
    # get station and program details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": "view-live-now popup"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No specific item playing"

    # Remove irrelevant info, starting with [*.*More]
    sub = "*.*More"
    pos = fe2.find(sub)
    if pos != -1:
        fe2 = fe2[:pos]
    return fe2


def Radio3(br,Num,sPath):
    if eventFlag:
        # use inspect to get the name of the calling function
        # this is used to generate the station name and logo
        stack = inspect.stack()
        station = inspect.stack()[1].function
        first_occurrence = station.find("_")
        second_occurrence = station.find("_", first_occurrence+1)
        global station_short
        station_short = station[:second_occurrence]
        logo = station_short + ".png"
        print(logo)
        print("--")

        # go to the station website
        br.get(refresh_http)
        time.sleep(1)
        br.get(sPath)
        time.sleep(needSleep)

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # Select timezone for stream (specific to this actual ABC radio website)
        for _ in range(5):
            be.send_keys(Keys.TAB)
        be.send_keys(Keys.ENTER)
        for _ in range(4):
            be.send_keys(Keys.UP)
        for _ in range(Num):
            be.send_keys(Keys.DOWN)
        be.send_keys(Keys.ENTER)

        # This where the streaming of the radio station is accomplished
        buttonStream = be.find_element(By.XPATH,'/html/body/div[1]/div/div/div/main/div[1]/div/div/div[2]/div/div[2]/div[12]/div[4]/div/div[1]')
        buttonStream.click()
        time.sleep(1)

        # get station logo
        image_path3 = pathImages + "/" + logo
        image = Image.open(image_path3)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon if adding station to playlist 
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")

        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    # get program image
    try:      
        img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div/div/div[3]/div[1]/div/div[2]/div[2]/img')
        img2_url = img2_element.get_attribute("src")
        image2_path = pathImages + "/presenter.jpg"
        urllib.request.urlretrieve(img2_url, image2_path)
    except NoSuchElementException:
        print("Image element not found on the webpage.")            
        # Display a blank image
        image2_path = pathImages + "/Blank.png"

    # Display the program image as given in the scaled_image2
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    crop_box2 = (width2-height2,0,width2,height2)
    cropped_image2 = image2.crop(crop_box2)
    scaled_image2 = cropped_image2.resize((Xprog, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    if station_short == "ABC_Classic":
        label2.place(x=Xgap, y=Ygap3)  # Adjust the position
    else:
        label2.place(x=Xgap, y=Ygap2)  # Adjust the position

    # get station details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": "view-live-now popup"})
    if fe is not None:
        fe1 = fe.get_text(separator="*", strip=True)
    else:
        fe1 = "None"

    # Remove irrelevant info, starting with [*More]
    sub = "*More"
    pos = fe1.find(sub)
    if pos != -1:
        fe1 = fe1[:pos]

    # append program details to station details    
    fe = soup.find(attrs={"class": "playingNow"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No specific item playing"
    fe3 = fe1+"*"+fe2
    return fe3


def Radio4(br,sPath):
    if eventFlag:
        # go to the station website
        br.get(refresh_http)
        time.sleep(1)
        br.get(sPath)
        time.sleep(needSleep)

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # This where the streaming of the radio station is accomplished
        buttonStream = be.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/main/div[1]/div/div/div/div[2]/button')
        buttonStream.click()
        time.sleep(3)
        
        # get station logo
        img_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/main/div[1]/div/div/div/a/div/img')
        img_url = img_element.get_attribute("src")
        image_path = pathImages + "/logo.png"
        urllib.request.urlretrieve(img_url, image_path)
        image = Image.open(image_path)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon if adding station to playlist 
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")
        
        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
       
    # get program image
    try:      
        img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[1]/div/div/div/img')
        img2_url = img2_element.get_attribute("src")
        image2_path = pathImages + "/presenter.jpg"
        print(image2_path)
        urllib.request.urlretrieve(img2_url, image2_path)
    except NoSuchElementException:
        print("Image element not found on the webpage.")            
        # Display a blank image
        image2_path = pathImages + "/ABC_faint.png"

    # Display the program image as given in the scaled_image2
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    crop_box2 = (width2-height2,0,width2,height2)
    cropped_image2 = image2.crop(crop_box2)
    scaled_image2 = cropped_image2.resize((Xprog, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap2, y=Ygap2)  # Adjust the position
    
    # get station details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": "LiveAudioPlayer_body__y6nYe"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No item playing"

    # Remove irrelevant info [*-]
    sub = "*-"
    fe3 = fe2.replace(sub,"")
    
    # append program details to station details    
    fe = soup.find(attrs={"class": "LiveAudioSynopsis_content__DZ6E7"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No Description"
    fe3 = fe3+"* *"+fe2
    return fe3


def Radio5(br,sPath):
    if eventFlag:
        # go to the station website
        br.get(refresh_http)
        time.sleep(1)
        browser.get(sPath)
        time.sleep(needSleep)

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # This where the streaming of the radio station is accomplished
        buttonStream = be.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/main/div[1]/div/div/div/div[2]/button')
        buttonStream.click()
        time.sleep(1)

        # get station logo
        img_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/main/div[1]/div/div/div/a/div/img')
        img_url = img_element.get_attribute("src")
        image_path = pathImages + "/logo.png"
        urllib.request.urlretrieve(img_url, image_path)
        image = Image.open(image_path)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon if adding station to playlist 
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")
        
        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    # get program image
    try:      
        img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[1]/div/div/div/img')
        img2_url = img2_element.get_attribute("src")
        image2_path = pathImages + "/presenter.jpg"
        urllib.request.urlretrieve(img2_url, image2_path)
    except NoSuchElementException:
        print("Image element not found on the webpage.")            
        # Display a blank image
        image2_path = pathImages + "/ABC_faint.png"

    # Display the program image as given in the scaled_image2
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    crop_box2 = (width2-height2,0,width2,height2)
    cropped_image2 = image2.crop(crop_box2)
    scaled_image2 = cropped_image2.resize((Xprog, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap, y=Ygap2)  # Adjust the position

    # get station details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": "LiveAudioPlayer_body__y6nYe"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No item playing"

    # Remove irrelevant info [*-]
    sub = "*-"
    fe3 = fe2.replace(sub,"")
    
    # append program details to station details    
    fe = soup.find(attrs={"class": "LiveAudioSynopsis_content__DZ6E7"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No Description"
    fe3 = fe3+"* *"+fe2
    return fe3


def Radio6(br,sPath):
    if eventFlag:
        # go to the station website
        br.get(refresh_http)
        time.sleep(2)
        br.get(sPath)
        time.sleep(needSleep)

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # This is where the streaming of the radio station is accomplished
        buttonStream = be.find_element(By.XPATH,'/html/body/div[1]/div/div/div/main/div[1]/div/div/div[1]/div/div[2]/div[12]/div[4]/div/div[1]')
        buttonStream.click()
        time.sleep(1)

        # get station logo
        image_path3 = pathImages + "/ABC_Kids_listen.png"
        image = Image.open(image_path3)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon if adding station to playlist 
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")
        
        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    # get program image
    try:      
        img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/img')
        img2_url = img2_element.get_attribute("src")
        image2_path = pathImages + "/presenter.jpg"
        urllib.request.urlretrieve(img2_url, image2_path)
    except NoSuchElementException:
        print("Image element not found on the webpage.")            
        # Display a blank image
        image2_path = pathImages + "/Blank.png"

    # Display the program image as given in the scaled_image2
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    crop_box2 = (width2-height2,0,width2,height2)
    cropped_image2 = image2.crop(crop_box2)
    scaled_image2 = cropped_image2.resize((Xprog, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap, y=Ygap3)  # Adjust the position
    
    # get station details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": "view-live-now popup"})
    if fe is not None:
        fe1 = fe.get_text(separator="*", strip=True)
    else:
        fe1 = "None"

    # Remove irrelevant info, starting with [*More]
    sub = "*More"
    pos = fe1.find(sub)
    if pos != -1:
        fe1 = fe1[:pos]

    # append program details to station details    
    fe = soup.find(attrs={"class": "playingNow"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No specific item playing"
    fe3 = fe1+"*"+fe2
    return fe3


# *************************** FIX FIX FIX ****************************************
def Radio7(br,Num,sPath):
    if eventFlag:
        stack = inspect.stack()
        print("----------")
        station = inspect.stack()[1].function
        logo = station + ".png"
        print(logo)
        print("----------")
        br.get(refresh_http)
        time.sleep(1)
        br.get(sPath)
        time.sleep(needSleep)

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # This where the streaming of the radio station is accomplished
        buttonStream = be.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/main/section[2]/div/section/div/section/section/div[2]/div/div[1]/div/div[2]/button')
        buttonStream.click()
        time.sleep(1)

        # get station logo
        image_path3 = pathImages + "/" + logo
        image = Image.open(image_path3)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")
        
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    # Display a blank program image
    image2_path = pathImages + "/Blank.png"
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    crop_box2 = (width2-height2,0,width2,height2)
    cropped_image2 = image2.crop(crop_box2)
    scaled_image2 = cropped_image2.resize((Xprog, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap, y=Ygap3)  # Adjust the position
        
    # Find program details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    if Num==0:
        xid="abc-:rb:-item-0"
        sName = "ABC SPORT"
    elif Num==1:
        xid="abc-:rb:-item-1"
        sName = "ABC SPORT EXTRA"
    else: # if Num==2
        xid="abc-:rb:-item-2"
        sName = "ABC CRICKET"
    fe = soup.find(attrs={"id": xid})
    if fe is not None:
        feX = fe.find(attrs={"class": "AudioPlayerCard_programMeta__3VqUy"})
        if feX is not None:
            fe2 = feX.get_text(separator="*", strip=True)
    else:
        fe2 = sName

    # Remove irrelevant info, starting with [*.*More]
    sub = "*Stop"
    pos = fe2.find(sub)
    if pos != -1:
        fe2 = fe2[:pos]
    else:
        sub = "*Listen"
        pos = fe2.find(sub)
        if pos != -1:
            fe2 = fe2[:pos]
    return fe2


def Commercial1(br,sPath,sClass,nType):
    if eventFlag:
        # use inspect to get the name of the calling function
        stack = inspect.stack()
        print("----------")
        station = inspect.stack()[1].function
        logo = station + ".png"
        print(logo)
        print("----------")
        
        # go to the station website
        br.get(refresh_http)
        time.sleep(2)
        br.get(sPath)
        time.sleep(needSleep) # bigger on slow machines

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # This where the streaming of the radio station is accomplished
        # the position of the "Listen Live" button depends on he nType integer parameter
        match nType:
            case 0:
                # iHeart stations
                buttonStream = be.find_element(By.XPATH,'/html/body/div[1]/div[4]/div[1]/div/div/div[2]/div/div[1]/button')
                buttonStream.click()
                print("Case 0")
            case 1:
                # Smooth &  Nova Stations
                buttonStream = be.find_element(By.XPATH,'//*[@id="listenLive"]')
                buttonStream.click()
                print("Case 1")
            case _:
                print("Out of bounds")            
        time.sleep(3)

        # get station logo
        if nType==0:
            # for iHeart stations
            img_element = be.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div/div[1]/div/div/img')
            img_url = img_element.get_attribute("src")
            image_path = pathImages + "/logo.png"
            urllib.request.urlretrieve(img_url, image_path)
        else:
            # for Smooth & Nova stations
            image_path = pathImages + "/" + logo

        # Display the station logo as given in the scaled_image
        image = Image.open(image_path)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon if adding station to playlist 
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")

        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    # Display the program image as given in the scaled_image2
    if nType==0: 
        # iHeart stations
        img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div[5]/div/div[1]/div[1]/div/img')
    else:
        # Smooth & Nova stations
        img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div[1]/div[1]/img')
    img2_url = img2_element.get_attribute("src")
    image2_path = pathImages + "/presenter.jpg"
    urllib.request.urlretrieve(img2_url, image2_path)
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"Pic width: {width2}, Pic height: {height2}")
    width = int(Xprog*width2/height2)
    scaled_image2 = image2.resize((width, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap3-(width-Xprog), y=Ygap2)  # Adjust the position
 
    # get station and program details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": sClass})
    if fe is not None:
        fe1 = fe.get_text(separator="*", strip=True)
    else:
        fe1 = "None"
    return fe1


# format used by the radio-australia.org and related stations format
def Commercial2(br,sPath):
    if eventFlag:
        # use inspect to get the name of the calling function
        stack = inspect.stack()
        print("----------")
        station = inspect.stack()[1].function
        logo = station + ".png"
        print(logo)
        print("----------")
        
        # go to the station website
        br.get(refresh_http)
        time.sleep(2)
        br.get(sPath)
        time.sleep(needSleep) # bigger on slow machines

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # press button with virtual mouse to play stream
        window_size = br.get_window_size()
        width = window_size['width']
        height = window_size['height']         
        print(f"Window size: width = {window_size['width']}, height = {window_size['height']}")
        widthPx =280
        heightPx = 390
        print(f"Move size: width = {widthPx}, height = {heightPx}")
        actions = ActionChains(br)
        actions.move_by_offset(widthPx, heightPx).click().perform()
        time.sleep(3)

        # get station logo
        image_path = pathImages + "/" + logo
        image = Image.open(image_path)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon if adding station to playlist 
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")
        
        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    # Stations with program image
    try:
        # try to find a particular image element by path
        img_element = be.find_element(By.XPATH, '/html/body/div[6]/div[1]/div[3]/div/div[1]/div[1]/div[3]/div/div[1]/div/a/img')
        img_url = img_element.get_attribute("src")
        image_path = pathImages + "/presenter.jpg"
        urllib.request.urlretrieve(img_url, image_path)
        image = Image.open(image_path)
        width2, height2 = image.size;
        print(f"Pic width: {width2}, Pic height: {height2}")
        width = int(Xprog*width2/height2)
        scaled_image = image.resize((width, Xprog))  # Adjust the size as needed
        photo = ImageTk.PhotoImage(scaled_image)
        label2.config(image=photo)
        label2.image = photo  # Keep a reference to avoid garbage collection
        label2.place(x=Xgap3-(width-Xprog), y=Ygap2)  # Adjust the position
        print("=====> /div/a/img")
    except NoSuchElementException:
        try:
            # if failed above try a slightly different path
            img_element = be.find_element(By.XPATH, '/html/body/div[6]/div[1]/div[3]/div/div[1]/div[1]/div[3]/div/div[1]/div/img')
            img_url = img_element.get_attribute("src")
            image_path = pathImages + "/presenter.jpg"
            urllib.request.urlretrieve(img_url, image_path)
            image = Image.open(image_path)
            width2, height2 = image.size;
            print(f"Pic width: {width2}, Pic height: {height2}")
            width = int(Xprog*width2/height2)
            scaled_image = image.resize((width, Xprog))  # Adjust the size as needed
            photo = ImageTk.PhotoImage(scaled_image)
            label2.config(image=photo)
            label2.image = photo  # Keep a reference to avoid garbage collection
            label2.place(x=Xgap3-(width-Xprog), y=Ygap2)  # Adjust the position
            print("=====>  /div/img")
        except NoSuchElementException:
            # failed to find image so display a blank image
            image_path = pathImages + "/Blank.png"
            image = Image.open(image_path)
            scaled_image = image.resize((Xprog, Xprog))  # Adjust the size as needed
            photo = ImageTk.PhotoImage(scaled_image)
            label2.config(image=photo)
            label2.image = photo  # Keep a reference to avoid garbage collection
            label2.place(x=Xgap, y=Ygap3)  # Adjust the position
            print("=====> No /img")

    # get station and program details (if available)
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": "history-song"})
    if fe is not None:
        fe1 = fe.get_text(separator="*", strip=True)
    else:
        fe1 = "No program information"
    return fe1



# END ####################################################
# DEFINE VARIOUS CORE FUNCTIONS THAT STREAM RADIO STATIONS


# START **********************************************************
# INDIVIDUAL FUNCTION DEFINITIONS FOR EACH AVAILABLE RADIO STATION
#
# Each one calls a particular core function defined above with specific parameters,
# dependant on the structure of a specific stations website layout

def ABC_Radio_Sydney_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/sydney")
def ABC_Broken_Hill_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/brokenhill")
def ABC_Central_Coast_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/centralcoast")
def ABC_Central_West_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/centralwest")
def ABC_Coffs_Coast_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/coffscoast")
def ABC_Illawarra_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/illawarra")
def ABC_Mid_North_Coast_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/midnorthcoast")
def ABC_New_England_North_West_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/newengland")
def ABC_Newcastle_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/newcastle")
def ABC_North_Coast_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/northcoast")
def ABC_Riverina_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/riverina")
def ABC_South_East_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/southeastnsw")
def ABC_Upper_Hunter_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/upperhunter")
def ABC_Western_Plains_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/westernplains")
def ABC_Radio_Canberra_ACT():
    return Radio4(browser,"https://www.abc.net.au/listen/live/canberra")
def ABC_Radio_Darwin_NT():
    return Radio4(browser,"https://www.abc.net.au/listen/live/darwin")
def ABC_Alice_Springs_NT():
    return Radio4(browser,"https://www.abc.net.au/listen/live/alicesprings")
def ABC_Radio_Melbourne_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/melbourne")
def ABC_Ballarat_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/ballarat")
def ABC_Central_Victoria_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/centralvic")
def ABC_Gippsland_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/gippsland")
def ABC_Goulburn_Murray_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/goulburnmurray")
def ABC_Mildura_Swan_Hill_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/milduraswanhill")
def ABC_Shepparton_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/shepparton")
def ABC_South_West_Victoria_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/southwestvic")
def ABC_Wimmera_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/wimmera")
def ABC_Radio_Adelaide_SA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/adelaide")
def ABC_Eyre_Peninsula_SA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/eyre")
def ABC_North_and_West_SA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/northandwest")
def ABC_Riverland_SA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/riverland")
def ABC_South_East_SA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/southeastsa")
def ABC_Radio_Hobart_TAS():
    return Radio4(browser,"https://www.abc.net.au/listen/live/hobart")
def ABC_Northern_Tasmania_TAS():
    return Radio4(browser,"https://www.abc.net.au/listen/live/northtas")
def ABC_Radio_Brisbane_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/brisbane")
def ABC_Capricornia_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/capricornia")
def ABC_Far_North_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/farnorth")
def ABC_Gold_Coast_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/goldcoast")
def ABC_North_Queensland_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/northqld")
def ABC_North_West_Queensland_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/northwest")
def ABC_Southern_Queensland_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/southqld")
def ABC_Sunshine_Coast_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/sunshine")
def ABC_Tropical_North_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/tropic")
def ABC_Western_Queensland_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/westqld")
def ABC_Wide_Bay_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/widebay")
def ABC_Radio_Perth_WA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/perth")
def ABC_Esperance_WA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/esperance")
def ABC_Goldfields_WA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/goldfields")
def ABC_Great_Southern_WA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/greatsouthern")
def ABC_Kimberley_WA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/kimberley")
def ABC_Midwest_and_Wheatbelt_WA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/wheatbelt")
def ABC_Pilbara_WA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/pilbara")
def ABC_South_West_WA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/southwestwa")
def ABC_NewsRadio():
    return Radio4(browser,"https://www.abc.net.au/listen/live/news")
def ABC_Radio_National_LIVE():
    return Radio2(browser,0,"https://www.abc.net.au/listen/live/radionational")
def ABC_Radio_National_QLD():
    return Radio2(browser,1,"https://www.abc.net.au/listen/live/radionational")
def ABC_Radio_National_WA():
    return Radio2(browser,2,"https://www.abc.net.au/listen/live/radionational")
def ABC_Radio_National_SA():
    return Radio2(browser,3,"https://www.abc.net.au/listen/live/radionational")
def ABC_Radio_National_NT():
    return Radio2(browser,4,"https://www.abc.net.au/listen/live/radionational")
def ABC_SPORT(): # *************************************************************** FIX ****
    return Radio7(browser,0,"https://www.abc.net.au/news/sport/audio")
def ABC_triple_j_LIVE():
    return Radio3(browser,0,"https://www.abc.net.au/listen/live/triplej")
def ABC_triple_j_QLD():
    return Radio3(browser,1,"https://www.abc.net.au/listen/live/triplej")
def ABC_triple_j_WA():
    return Radio3(browser,2,"https://www.abc.net.au/listen/live/triplej")
def ABC_triple_j_SA():
    return Radio3(browser,3,"https://www.abc.net.au/listen/live/triplej")
def ABC_triple_j_NT():
    return Radio3(browser,4,"https://www.abc.net.au/listen/live/triplej")
def ABC_triple_j_Hottest():
    return Radio1(browser,7,"https://www.abc.net.au/triplej/live/triplejhottest")
def ABC_triple_j_Unearthed():
    return Radio1(browser,7,"https://www.abc.net.au/triplej/live/unearthed")
def ABC_Double_j_LIVE():
    return Radio3(browser,0,"https://www.abc.net.au/listen/live/doublej")
def ABC_Double_j_QLD():
    return Radio3(browser,1,"https://www.abc.net.au/listen/live/doublej")
def ABC_Double_j_WA():
    return Radio3(browser,2,"https://www.abc.net.au/listen/live/doublej")
def ABC_Double_j_SA():
    return Radio3(browser,3,"https://www.abc.net.au/listen/live/doublej")
def ABC_Double_j_NT():
    return Radio3(browser,4,"https://www.abc.net.au/listen/live/doublej")
def ABC_Classic_LIVE():
    return Radio3(browser,0,"https://www.abc.net.au/listen/live/classic")
def ABC_Classic_QLD():
    return Radio3(browser,1,"https://www.abc.net.au/listen/live/classic")
def ABC_Classic_WA():
    return Radio3(browser,2,"https://www.abc.net.au/listen/live/classic")
def ABC_Classic_SA():
    return Radio3(browser,3,"https://www.abc.net.au/listen/live/classic")
def ABC_Classic_NT():
    return Radio3(browser,4,"https://www.abc.net.au/listen/live/classic")
def ABC_Classic2():
    return Radio1(browser,7,"https://www.abc.net.au/listen/live/classic2")
def ABC_Jazz():
    return Radio1(browser,7,"https://www.abc.net.au/listen/live/jazz")
def ABC_Country():
    return Radio5(browser,"https://www.abc.net.au/listen/live/country")
def ABC_Kids_listen():
    return Radio6(browser,"https://www.abc.net.au/listenlive/kidslisten")
def ABC_Radio_Australia():
    return Radio5(browser,"https://www.abc.net.au/pacific/live")
def KIIS1065():
    return Commercial1(browser,"https://www.iheart.com/live/kiis-1065-6185/","css-1jnehb1 e1aypx0f0",0)
def GOLD1017():
    return Commercial1(browser,"https://www.iheart.com/live/gold1017-6186/","css-1jnehb1 e1aypx0f0",0)
def CADA():
    return Commercial1(browser,"https://www.iheart.com/live/cada-6179/","css-1jnehb1 e1aypx0f0",0)
def iHeartCountry_Australia():
    return Commercial1(browser,"https://www.iheart.com/live/iheartcountry-australia-7222/","css-1jnehb1 e1aypx0f0",0)
def KIIS_90s():
    return Commercial1(browser,"https://www.iheart.com/live/kiis-90s-10069/","css-1jnehb1 e1aypx0f0",0)
def GOLD_80s():
    return Commercial1(browser,"https://www.iheart.com/live/gold-80s-10073/","css-1jnehb1 e1aypx0f0",0)    
def iHeartRadio_Countdown_AUS():
    return Commercial1(browser,"https://www.iheart.com/live/iheartradio-countdown-aus-6902/","css-1jnehb1 e1aypx0f0",0)
def TikTok_Trending_on_iHeartRadio():
    return Commercial1(browser,"https://www.iheart.com/live/tiktok-trending-on-iheartradio-8876/","css-1jnehb1 e1aypx0f0",0)
def iHeartDance():
    return Commercial1(browser,"https://www.iheart.com/live/iheartdance-6941/","css-1jnehb1 e1aypx0f0",0)
def The_Bounce():
    return Commercial1(browser,"https://www.iheart.com/live/the-bounce-6327/","css-1jnehb1 e1aypx0f0",0)
def iHeartAustralia():
    return Commercial1(browser,"https://www.iheart.com/live/iheartaustralia-7050/","css-1jnehb1 e1aypx0f0",0)
def fbi_radio():
    return Commercial1(browser,"https://www.iheart.com/live/fbiradio-6311/","css-1jnehb1 e1aypx0f0",0)
def _2SER():
    return Commercial1(browser,"https://www.iheart.com/live/2ser-6324/","css-1jnehb1 e1aypx0f0",0)
def _2MBS_Fine_Music_Sydney():
    return Commercial1(browser,"https://www.iheart.com/live/2mbs-fine-music-sydney-6312/","css-1jnehb1 e1aypx0f0",0)
def KIX_Country():
    return Commercial1(browser,"https://www.iheart.com/live/kix-country-9315/","css-1jnehb1 e1aypx0f0",0)
def SBS_Chill():
    return Commercial1(browser,"https://www.iheart.com/live/sbs-chill-7029/","css-1jnehb1 e1aypx0f0",0)
def Vintage_FM():
    return Commercial1(browser,"https://www.iheart.com/live/vintage-fm-8865/","css-1jnehb1 e1aypx0f0",0)
def My88_FM():
    return Commercial1(browser,"https://www.iheart.com/live/my88-fm-8866/","css-1jnehb1 e1aypx0f0",0)
def Hope_103_2():
    return Commercial1(browser,"https://www.iheart.com/live/hope-1032-6314/","css-1jnehb1 e1aypx0f0",0)
def The_90s_iHeartRadio():
    return Commercial1(browser,"https://www.iheart.com/live/the-90s-iheartradio-6793/","css-1jnehb1 e1aypx0f0",0)
def The_80s_iHeartRadio():
    return Commercial1(browser,"https://www.iheart.com/live/the-80s-iheartradio-6794/","css-1jnehb1 e1aypx0f0",0)
def Mix_102_3():
    return Commercial1(browser,"https://www.iheart.com/live/mix1023-6184/","css-1jnehb1 e1aypx0f0",0)
def Cruise_1323():
    return Commercial1(browser,"https://www.iheart.com/live/cruise-1323-6177/","css-1jnehb1 e1aypx0f0",0)
def Mix_80s():
    return Commercial1(browser,"https://www.iheart.com/live/mix-80s-10076/","css-1jnehb1 e1aypx0f0",0)
def Mix_90s():
    return Commercial1(browser,"https://www.iheart.com/live/mix-90s-10072/","css-1jnehb1 e1aypx0f0",0)
def ABC_Sport():
    return Commercial1(browser,"https://www.iheart.com/live/abc-sport-7112/","css-1jnehb1 e1aypx0f0",0)
def ABC_Sport_Extra():
    return Commercial1(browser,"https://www.iheart.com/live/abc-sport-extra-10233/","css-1jnehb1 e1aypx0f0",0)
def Energy_Groove():
    return Commercial1(browser,"https://www.iheart.com/live/energy-groove-6329/","css-1jnehb1 e1aypx0f0",0)
def Vision_Christian_Radio():
    return Commercial1(browser,"https://www.iheart.com/live/vision-christian-radio-9689/","css-1jnehb1 e1aypx0f0",0)
def Starter_FM():
    return Commercial1(browser,"https://www.iheart.com/live/starter-fm-9353/","css-1jnehb1 e1aypx0f0",0)
def _2ME():
    return Commercial1(browser,"https://www.iheart.com/live/2me-10143/","css-1jnehb1 e1aypx0f0",0)
def SBS_PopAsia():
    return Commercial1(browser,"https://www.iheart.com/live/sbs-popasia-7028/","css-1jnehb1 e1aypx0f0",0)
def _3MBS_Fine_Music_Melbourne():
    return Commercial1(browser,"https://www.iheart.com/live/3mbs-fine-music-melbourne-6183/","css-1jnehb1 e1aypx0f0",0)
def Golden_Days_Radio():
    return Commercial1(browser,"https://www.iheart.com/live/golden-days-radio-8676/","css-1jnehb1 e1aypx0f0",0)
def PBS_106_7FM():
    return Commercial1(browser,"https://www.iheart.com/live/pbs-1067fm-6316/","css-1jnehb1 e1aypx0f0",0)
def smoothfm_953_Sydney():
    return Commercial1(browser,"https://smooth.com.au/station/smoothsydney","index_smooth_info-wrapper-desktop__6ZYTT",1)
def smooth_VINTAGE():
    return Commercial1(browser,"https://smooth.com.au/station/smoothvintage","index_smooth_info-wrapper-desktop__6ZYTT",1)
def smooth_relax():
    return Commercial1(browser,"https://smooth.com.au/station/smoothrelax","index_smooth_info-wrapper-desktop__6ZYTT",1)
def smooth_80s():
    return Commercial1(browser,"https://smooth.com.au/station/smooth80s","index_smooth_info-wrapper-desktop__6ZYTT",1)
def smoothfm_Adelaide():
    return Commercial1(browser,"https://smooth.com.au/station/adelaide","index_smooth_info-wrapper-desktop__6ZYTT",1)
def smoothfm_915_Melbourne():
    return Commercial1(browser,"https://smooth.com.au/station/smoothfm915","index_smooth_info-wrapper-desktop__6ZYTT",1)
def smoothfm_Brisbane():
    return Commercial1(browser,"https://smooth.com.au/station/brisbane","index_smooth_info-wrapper-desktop__6ZYTT",1)
def smoothfm_Perth():
    return Commercial1(browser,"https://smooth.com.au/station/smoothfmperth","index_smooth_info-wrapper-desktop__6ZYTT",1)
def nova_969_Sydney():
    return Commercial1(browser,"https://novafm.com.au/station/nova969","index_nova_info-wrapper-desktop__CWW5R",1)
def nova_90s():
    return Commercial1(browser,"https://novafm.com.au/station/nova90s","index_nova_info-wrapper-desktop__CWW5R",1)
def nova_THROWBACKS():
    return Commercial1(browser,"https://novafm.com.au/station/throwbacks","index_nova_info-wrapper-desktop__CWW5R",1)
def nova_FreshCOUNTRY():
    return Commercial1(browser,"https://novafm.com.au/station/novafreshcountry","index_nova_info-wrapper-desktop__CWW5R",1)
def nova_NATION():
    return Commercial1(browser,"https://novafm.com.au/station/novanation","index_nova_info-wrapper-desktop__CWW5R",1)
def nova_919_Adelaide():
    return Commercial1(browser,"https://novafm.com.au/station/nova919","index_nova_info-wrapper-desktop__CWW5R",1)
def nova_100_Melbourne():
    return Commercial1(browser,"https://novafm.com.au/station/nova100","index_nova_info-wrapper-desktop__CWW5R",1)
def nova_1069_Brisbane():
    return Commercial1(browser,"https://novafm.com.au/station/nova1069","index_nova_info-wrapper-desktop__CWW5R",1)
def nova_937_Perth():
    return Commercial1(browser,"https://novafm.com.au/station/nova937","index_nova_info-wrapper-desktop__CWW5R",1)
def _2GB_SYDNEY():
    return Commercial2(browser,"https://www.radio-australia.org/2gb")
def _2GN_GOULBURN():
    return Commercial2(browser,"https://www.radio-australia.org/2gn")
def bbc_radio_1():
    return Commercial2(browser,"https://www.radio-uk.co.uk/bbc-radio-1")
def bbc_radio_2():
    return Commercial2(browser,"https://www.radio-uk.co.uk/bbc-radio-2")
def bbc_radio_3():
    return Commercial2(browser,"https://www.radio-uk.co.uk/bbc-radio-3")
def bbc_radio_4():
    return Commercial2(browser,"https://www.radio-uk.co.uk/bbc-radio-4")
def bbc_radio_5_live():
    return Commercial2(browser,"https://www.radio-uk.co.uk/bbc-radio-5-live")
def _1000_hits_classical_music():
    return Commercial2(browser,"https://www.fmradiofree.com/1000-hits-classical-music")
def classic_fm():
    return Commercial2(browser,"https://www.radio-uk.co.uk/classic-fm")
def klassik_radio():
    return Commercial2(browser,"https://www.internetradio-horen.de/klassik-radio")
def klassik_radio_pure_bach():
    return Commercial2(browser,"https://www.internetradio-horen.de/klassik-radio-pure-bach")
def klassik_radio_pure_beethoven():
    return Commercial2(browser,"https://www.internetradio-horen.de/klassik-radio-pure-beethoven")
def klassik_radio_pure_mozart():
    return Commercial2(browser,"https://www.internetradio-horen.de/klassik-radio-pure-mozart")
def klassik_radio_pure_verdi():
    return Commercial2(browser,"https://www.internetradio-horen.de/klassik-radio-pure-verdi")
def epic_piano_chopin():
    return Commercial2(browser,"https://www.internetradio-horen.de/epic-piano-chopin")


# END ************************************************************
# INDIVIDUAL FUNCTION DEFINITIONS FOR EACH AVAILABLE RADIO STATION


# 2D array of radio station information in [long name, calling function] format
# clearly this can be varied if you wish to listen to different stations
# Currently we Have 83 ABC stations and 108 in total!
aStation = [
    ["ABC Radio Sydney NSW",ABC_Radio_Sydney_NSW],
    ["ABC Broken Hill NSW",ABC_Broken_Hill_NSW],
    ["ABC Central Coast NSW",ABC_Central_Coast_NSW],
    ["ABC Central West NSW",ABC_Central_West_NSW],
    ["ABC Coffs Coast NSW",ABC_Coffs_Coast_NSW],
    ["ABC Illawarra NSW",ABC_Illawarra_NSW],
    ["ABC Mid North Coast NSW",ABC_Mid_North_Coast_NSW],
    ["ABC New England North West NSW",ABC_New_England_North_West_NSW],
    ["ABC Newcastle NSW",ABC_Newcastle_NSW],
    ["ABC North Coast NSW",ABC_North_Coast_NSW],
    ["ABC Riverina NSW",ABC_Riverina_NSW],
    ["ABC South East NSW",ABC_South_East_NSW],
    ["ABC Upper Hunter NSW",ABC_Upper_Hunter_NSW],
    ["ABC Western Plains NSW",ABC_Western_Plains_NSW],
    ["ABC Radio Canberra ACT",ABC_Radio_Canberra_ACT],
    ["ABC Radio Darwin NT",ABC_Radio_Darwin_NT],
    ["ABC Alice Springs NT",ABC_Alice_Springs_NT],
    ["ABC Radio Melbourne VIC",ABC_Radio_Melbourne_VIC],
    ["ABC Ballarat VIC",ABC_Ballarat_VIC],
    ["ABC Central Victoria VIC",ABC_Central_Victoria_VIC],
    ["ABC Gippsland VIC",ABC_Gippsland_VIC],
    ["ABC Goulburn Murray VIC",ABC_Goulburn_Murray_VIC],
    ["ABC Mildura-Swan Hill VIC",ABC_Mildura_Swan_Hill_VIC],
    ["ABC Shepparton VIC",ABC_Shepparton_VIC],
    ["ABC South West Victoria VIC",ABC_South_West_Victoria_VIC],
    ["ABC Wimmera VIC",ABC_Wimmera_VIC],
    ["ABC Radio Adelaide SA",ABC_Radio_Adelaide_SA],
    ["ABC Eyre Peninsula SA",ABC_Eyre_Peninsula_SA],
    ["ABC North and West SA",ABC_North_and_West_SA],
    ["ABC Riverland SA",ABC_Riverland_SA],
    ["ABC South East SA",ABC_South_East_SA],
    ["ABC Radio Hobart TAS",ABC_Radio_Hobart_TAS],
    ["ABC Northern Tasmania TAS",ABC_Northern_Tasmania_TAS],
    ["ABC Radio Brisbane QLD",ABC_Radio_Brisbane_QLD],
    ["ABC Capricornia QLD",ABC_Capricornia_QLD],
    ["ABC Far North QLD",ABC_Far_North_QLD],
    ["ABC Gold Coast QLD",ABC_Gold_Coast_QLD],
    ["ABC North Queensland QLD",ABC_North_Queensland_QLD],
    ["ABC North West Queensland QLD",ABC_North_West_Queensland_QLD],
    ["ABC Southern Queensland QLD",ABC_Southern_Queensland_QLD],
    ["ABC Sunshine Coast QLD",ABC_Sunshine_Coast_QLD],
    ["ABC Tropical North QLD",ABC_Tropical_North_QLD],
    ["ABC Western Queensland QLD",ABC_Western_Queensland_QLD],
    ["ABC Wide Bay QLD",ABC_Wide_Bay_QLD],
    ["ABC Radio Perth WA",ABC_Radio_Perth_WA],
    ["ABC Esperance WA",ABC_Esperance_WA],
    ["ABC Goldfields WA",ABC_Goldfields_WA],
    ["ABC Great Southern WA",ABC_Great_Southern_WA],
    ["ABC Kimberley WA",ABC_Kimberley_WA],
    ["ABC Midwest & Wheatbelt WA",ABC_Midwest_and_Wheatbelt_WA],
    ["ABC Pilbara WA",ABC_Pilbara_WA],
    ["ABC South West WA",ABC_South_West_WA],
    ["ABC NewsRadio",ABC_NewsRadio],
    ["ABC Radio National LIVE",ABC_Radio_National_LIVE],
    ["ABC Radio National QLD",ABC_Radio_National_QLD],
    ["ABC Radio National WA",ABC_Radio_National_WA],
    ["ABC Radio National SA",ABC_Radio_National_SA],
    ["ABC Radio National NT",ABC_Radio_National_NT],
    ["ABC SPORT",ABC_SPORT],
    ["ABC triple j LIVE",ABC_triple_j_LIVE],
    ["ABC triple j QLD",ABC_triple_j_QLD],
    ["ABC triple j WA",ABC_triple_j_WA],
    ["ABC triple j SA",ABC_triple_j_SA],
    ["ABC triple j NT",ABC_triple_j_NT],
    ["ABC triple j Hottest",ABC_triple_j_Hottest],
    ["ABC triple j Unearthed",ABC_triple_j_Unearthed],
    ["ABC Double j LIVE",ABC_Double_j_LIVE],
    ["ABC Double j QLD",ABC_Double_j_QLD],
    ["ABC Double j WA",ABC_Double_j_WA],
    ["ABC Double j SA",ABC_Double_j_SA],
    ["ABC Double j NT",ABC_Double_j_NT],
    ["ABC Classic LIVE",ABC_Classic_LIVE],
    ["ABC Classic QLD",ABC_Classic_QLD],
    ["ABC Classic WA",ABC_Classic_WA],
    ["ABC Classic SA",ABC_Classic_SA],
    ["ABC Classic NT",ABC_Classic_NT],
    ["ABC Classic2",ABC_Classic2],
    ["ABC Jazz",ABC_Jazz],    ["ABC Country",ABC_Country],
    ["ABC Kids listen",ABC_Kids_listen],
    ["ABC Radio Australia",ABC_Radio_Australia],
    ["KIIS 1065",KIIS1065],
    ["GOLD101.7",GOLD1017],
    ["CADA",CADA],
    ["iHeartCountry Australia",iHeartCountry_Australia],
    ["KIIS 90s",KIIS_90s],
    ["GOLD 80s",GOLD_80s],
    ["iHeartRadio Countdown AUS",iHeartRadio_Countdown_AUS],
    ["TikTok Trending on iHeartRadio",TikTok_Trending_on_iHeartRadio],
    ["iHeartDance",iHeartDance],
    ["The Bounce",The_Bounce],
    ["iHeartAustralia",iHeartAustralia],
    ["fbi.radio",fbi_radio],
    ["2SER",_2SER],
    ["2MBS Fine Music Sydney",_2MBS_Fine_Music_Sydney],
    ["KIX Country",KIX_Country],
    ["SBS Chill",SBS_Chill],
    ["Vintage FM",Vintage_FM],
    ["My88 FM",My88_FM],
    ["Hope 103.2",Hope_103_2],
    ["The 90s iHeartRadio",The_90s_iHeartRadio],
    ["The 80s iHeartRadio",The_80s_iHeartRadio],
    ["Mix 102.3",Mix_102_3],
    ["Cruise 1323",Cruise_1323],
    ["Mix 80s",Mix_80s],
    ["ABC Sport",ABC_Sport],
    ["ABC Sport Extra",ABC_Sport_Extra],
    ["Energy Groove",Energy_Groove],
    ["Vision Christian Radio",Vision_Christian_Radio],
    ["Starter FM",Starter_FM],
    ["2ME",_2ME],
    ["SBS PopAsia",SBS_PopAsia],
    ["3MBS Fine Music Melbourne",_3MBS_Fine_Music_Melbourne],
    ["Golden Days Radio",Golden_Days_Radio],
    ["PBS 106.7FM",PBS_106_7FM],
    ["smoothfm 95.3 Sydney",smoothfm_953_Sydney],
    ["smoothfm 91.5 Melbourne",smoothfm_915_Melbourne],
    ["smoothfm Adelaide",smoothfm_Adelaide],
    ["smoothfm Brisbane",smoothfm_Brisbane],
    ["smoothfm Perth",smoothfm_Perth],
    ["smooth 80s",smooth_80s],
    ["smooth relax",smooth_relax],
    ["smooth VINTAGE",smooth_VINTAGE],
    ["nova 969 Sydney",nova_969_Sydney],
    ["nova 100 Melbourne",nova_100_Melbourne],
    ["nova 919 Adelaide",nova_919_Adelaide],
    ["nova 1069 Brisbane",nova_1069_Brisbane],
    ["nova 937 Perth",nova_937_Perth],
    ["nova 90s",nova_90s],
    ["nova THROWBACKS",nova_THROWBACKS],
    ["nova FreshCOUNTRY",nova_FreshCOUNTRY],
    ["nova NATION",nova_NATION],
    ["2GB SYDNEY",_2GB_SYDNEY],
    ["2GN GOULBURN",_2GN_GOULBURN],
    ["bbc radio 1",bbc_radio_1],
    ["bbc radio 2",bbc_radio_2],
    ["bbc radio 3",bbc_radio_3],
    ["bbc radio 4",bbc_radio_4],
    ["bbc radio 5 live",bbc_radio_5_live],
    ["1000 hits classical music",_1000_hits_classical_music],
    ["classic fm",classic_fm],
    ["klassik radio",klassik_radio],
    ["klassik radio pure bach",klassik_radio_pure_bach],
    ["klassik radio pure beethoven",klassik_radio_pure_beethoven],
    ["klassik radio pure mozart",klassik_radio_pure_mozart],
    ["klassik radio pure verdi",klassik_radio_pure_verdi],
    ["epic piano chopin",epic_piano_chopin]
] 

# 2D array of preset radio stations, in long name and index (to aStation[]) format.
# this is the default, but is actually copied from file at statup and saved to file on exit!
aStation2 = []
for i in range(numButtons):
    station = ["-- EMPTY " + str(i) +" --", -1]
    aStation2.append(station)


# does stuff just after gui is initialised and we are running in the root thread
def after_GUI_started():
  # select to stream last station that was streaming just before radio was powered down
    global buttonIndex, buttonFlag; buttonFlag = True
    try:
        with open(filepath, 'r') as file:
            buttonIndex = int(file.read())
    except FileNotFoundError:
        print(f'Error: The file {filepath} does not exist.')
        buttonIndex = 0
    if buttonIndex == -1:
        buttonIndex = 0
    print(f'Index of last station played in playlist is {buttonIndex}')    
    print("")    
    on_select2(CustomEvent("Auto", buttons[buttonIndex], "Auto from GUI start"))


# do this when closing the window/app
def on_closing():
    browser.quit() # close the WebDriver
    root.destroy() # destroy GUI   
    print("Closing the app...")


# do this when a radio station is selected from combobox
def on_select(event):
    # determine the timeInterval between calling on_select() or on_select2()
    global startTime, finishTime
    finishTime = time.time()
    timeInterval = finishTime-startTime
    print("***********************")
    print(f"Time interval: {timeInterval:.2f} seconds")
    print("***********************")
    startTime = time.time()
    print(f"Type: {event.type}")
    print(f"Widget: {event.widget}")
    print(f"Data: {event.data}")
    
    # set various flags and parameters related to starting a station stream or accesing its website
    global eventFlag, stopFlag, selected_value, combobox_index, selected_value_last 
    if event.type=="Auto":
        eventFlag = True # if on_select() is called by selecting a combobox entry
        stopFlag = False # if this call of on_select() should be implemented
      # parameters relating to how this funtion was called
        selected_value_last = selected_value
        selected_value = combobox.get()
        combobox_index = combobox.current()
        print("selected_value:", selected_value)
        print("combobox_index:", combobox_index)

    # setting stop flag, this prevents on_select() from running again
    # "mysterious" code due to timing issues
    if eventFlag:
        stopFlag = False
    else: # if (not eventFlag)   
        if stopFlag:
            stopFlag=False
            print("SECOND STOP FAIL")
        elif (timeInterval < refreshTime-0.5):
            stopFlag = True    
            print("FIRST STOP")
    print("stopFlag:",stopFlag)
    print("eventFlag:",eventFlag)

    if stopFlag==False:
        # run selected radio station stream, and return associated textual information 
        text = aStation[combobox_index][1]() # THIS BIT ACTUALLY STARTS STREAM
        fullStationName = aStation[combobox_index][0] 
        text = fullStationName + "*" + text
        text_rows = text.split("*")
        if len(text_rows)>1:
            if text_rows[0]==text_rows[1]:
                    del text_rows[0]

        # Make text box editable, so contents can be deleted and rewritten
        text_box.config(state=tk.NORMAL)
        text_box.delete('1.0', tk.END)
        print(text_rows)
        # Insert each row of text into the text box
        for row in text_rows:
            text_box.insert(tk.END, row + "\n")
        # Disable the text box to make it read-only
        text_box.config(state=tk.DISABLED)

        # hide the annoying blinking cursor though the fudge
        # of selective focus setting
        combobox.focus_set()
        combobox.selection_clear()
        buttons[buttonIndex].focus_set()
        root.update_idletasks()

        # on_select() schedules itself to run in nominally refreshTime seconds.
        # this updates the program text and grapic while the selected radio station is streaming
        print("JUST ABOUT TO RUN ROOT")
        eventFlag = False
        root.after(int(refreshTime*1000), lambda: on_select(CustomEvent("Manual", combobox, "Manual from combobox")))
        print("FINISHED RUNNING ROOT")
        print("")

    else: #if stopFlag==True
        # Makes the scheduled call to on_select() do nothing if
        # it occurs after another station stream has been started
        stopFlag = False
        print("selected_value:",selected_value_last)
        print("DID STOPPING BIT")
        print("")


# do this when a radio station is selected via playlist buttons,
# similar in structure to on_select(), but the way the radio station stream is called differs.
def on_select2(event):
    global startTime, finishTime
    finishTime = time.time()
    timeInterval = finishTime-startTime
    print("***********************")
    print(f"Time interval: {timeInterval:.2f} seconds")
    print("***********************")
    startTime = time.time()
    print(f"Type: {event.type}")
    print(f"Widget: {event.widget}")
    print(f"Data: {event.data}")

    global eventFlag, stopFlag, selected_value, selected_index, selected_value_last
    if event.type=="Auto":
        eventFlag = True
        selected_value_last = selected_value
        selected_value = aStation2[buttonIndex][0]
        selected_index = int(aStation2[buttonIndex][1])
        print("selected_value:",selected_value)
        print("selected_index:",selected_index)

    # setting stop flag, this prevents on_select2 from running again
    # "mysterious" code due to timing issues
    if eventFlag:
        stopFlag = False
    else: # if (not eventFlag)   
        if stopFlag:
            stopFlag=False
            print("SECOND STOP FAIL")
        elif (timeInterval < refreshTime-0.5):
            stopFlag = True    
            print("FIRST STOP")
    print("stopFlag:",stopFlag)
    print("eventFlag:",eventFlag)

    if stopFlag==False:
        print("Selected:", selected_value)
        print("Index:", selected_index)
        print("Button index:", buttonIndex)

        if selected_index != -1:
            print("selected_index != -1")

            # run selected radio station stream, and return associated textual information 
            text = (aStation[selected_index][1])() # this uses the eventFlag
            fullStationName = aStation[selected_index][0] 
            text = fullStationName + "*" + text
            text_rows = text.split("*")
            if len(text_rows)>1:
                if text_rows[0]==text_rows[1]:
                        del text_rows[0]

            # Make text box editable, so contents can be deleted and rewritten
            text_box.config(state=tk.NORMAL)
            text_box.delete('1.0', tk.END)
            print(text_rows)

            # Insert each row of text into the text box
            for row in text_rows:
                text_box.insert(tk.END, row + "\n")

            # make seleted button synchronize with combobox
            # hide the annoying blinking cursor though the fudge
            # of selective focus setting
            if event.type=="Auto":
                combobox.set(fullStationName)
                combobox.focus_set()
                combobox.selection_clear()
                buttons[buttonIndex].focus_set()
            
            # Disable the text box to make it read-only
            text_box.config(state=tk.DISABLED)
            root.update_idletasks()

            print("JUST ABOUT TO RUN ROOT")
            eventFlag = False
            root.after(int(refreshTime*1000), lambda: on_select2(CustomEvent("Manual", buttons[buttonIndex], "Manual from buttons")))
            print("FINISHED RUNNING ROOT")
            print("")

        else:
            # There is nothing to stream
            browser.get(refresh_http)
            time.sleep(2)
            text = selected_value + "*No station playing"
            text_rows = text.split("*")

            # Make text box editable, so contents can be deleted and rewritten
            text_box.config(state=tk.NORMAL)
            text_box.delete('1.0', tk.END       )
            print(text_rows)

            # Insert each row of text into the text box
            for row in text_rows:
                text_box.insert(tk.END, row + "\n")

            # Disable the text box to make it read-only
            text_box.config(state=tk.DISABLED)
            root.update_idletasks()

            # Display the station logo and program graphic as blank
            image_path = pathImages + "/Blank.png"
            image = Image.open(image_path)
            scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed
            photo = ImageTk.PhotoImage(scaled_image)
            label.config(image=photo)
            label.image = photo  # Keep a reference to avoid garbage collection
            scaled_image2 = image.resize((Xprog, Xprog))  # Adjust the size as needed
            photo2 = ImageTk.PhotoImage(scaled_image2)
            label2.config(image=photo2)
            label2.image = photo2  # Keep a reference to avoid garbage collection
            label2.place(x=Xgap, y=Ygap2)  # Adjust the position
            print("BLANK END")
            print("")

        if event.type=="Auto":
            # save number of last playlist radio station that was played (0,...,9), ie buttonIndex.
            with open(filepath, 'w') as file:
                file.write(str(buttonIndex))

    else: #if stopFlag==True
        print("selected_value:",selected_value_last)
        print("DID STOPPING BIT")
        print("")


# do this when the Add button is pressed.
# it adds the radio station previously selected via the combobox to the playlist button
# that has focus. In particular it displays the station logo on the button and links it to the station.
def on_button_Add_press(event):
    button_Add.config(relief="sunken", bg="lightgray")  # Simulate button press
    button_Add.update_idletasks()  # Force update
    time.sleep(1)
    button_Add.config(relief="raised", bg="gray90")  # Simulate button press
    button_Add.update_idletasks()  # Force update
    print("Add button pressed")
    print("From index:", combobox_index)
    print("To index:", buttonIndex)
    
    # change aStation2[] list to reflect the addition
    global aStation2
    if (combobox_index != -1) and (buttonIndex != -1):
        print("station added")    
        global addFlag
        addFlag = True # so can get and save icon for playlist button

        lastStation = aStation[combobox_index][0]
        aStation2[buttonIndex][0] = lastStation
        aStation2[buttonIndex][1] = combobox_index

        # This will play the newly added station as well as saving the icon
        # to its playlist button number
        on_select2(CustomEvent("Auto", buttons[buttonIndex], "Auto from button_Add"))

        # now need to update the icon on the buttonIndex button
        buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
        image = Image.open(buttonImagePath)
        image_resized = image.resize((sizeButton-5,sizeButton-5), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image_resized)
        buttons[buttonIndex].config(image=photo)
        buttons[buttonIndex].image = photo
        buttons[buttonIndex].update_idletasks()

        # save the playlist to file
        with open(filepath2, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(aStation2)
    else:
        print("No station added")    
    print("")


# do this when the Del button is pressed
# it deletes the radio station linked from the playlist button that currently has focus.
# Its icon is also deleted from the button.
def on_button_Del_press(event):
    button_Del.config(relief="sunken", bg="lightgray")  # Simulate button press
    button_Del.update_idletasks()  # Force update
    time.sleep(1)
    button_Del.config(relief="raised", bg="gray90")  # Simulate button press
    button_Del.update_idletasks()  # Force update
    print("Del button pressed")
    
    # change aStation2[] to reflect the deletion
    global aStation2
    index = aStation2[buttonIndex][1]
    print("deleting station:", index, "with playlist index:", buttonIndex)
    if (buttonIndex != -1) and (index != -1):
        print("station deleted")    

        lastStation = "-- EMPTY " + str(buttonIndex) +" --"
        aStation2[buttonIndex][0] = lastStation
        aStation2[buttonIndex][1] = -1

        # get blank station logo
        image_path = pathImages + "/Blank.png"
        image = Image.open(image_path)

        # saving button icon
        buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
        image.save(buttonImagePath)

        # This will "play" the blank station
        on_select2(CustomEvent("Auto", button_Del, "Auto from button_Del"))

        # now need to update the icon on the buttonIndex button
        image_resized = image.resize((sizeButton-5,sizeButton-5), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image_resized)
        buttons[buttonIndex].config(image=photo)
        buttons[buttonIndex].image = photo
        buttons[buttonIndex].update_idletasks() 

        # save the playlist to file
        with open(filepath2, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(aStation2)
    else:
        print("No station to delete")    
    print("")


# called when playlist button i is pressed.
# visually simulates a physical button press and initiates the station stream by
# calling the on_selec2() function
def on_button_press(event, i):
    buttons[i].config(relief="sunken", bg="lightgray")  # Simulate button press
    buttons[i].update_idletasks()  # Force update
    time.sleep(1)
    buttons[i].config(relief="raised", bg="gray90")  # Simulate button press
    buttons[i].update_idletasks()  # Force update
    print("Button " + str(i) +" pressed")
    global buttonFlag;  buttonFlag = True
    global buttonIndex; buttonIndex = i
    on_select2(CustomEvent("Auto", buttons[buttonIndex], "Auto from buttons[i] press"))    

# called when a playlist button receives focus.
# visually indicates that the button has focus and
# saves the buttonIndex in a global variable
def on_focus(event, i):
    buttons[i].config(relief="raised", bg="darkgray")  # Simulate button press
    buttons[i].update_idletasks()  # Force update
    global buttonIndex; buttonIndex = i
    print(f"on focus: {i}")

# called when a playlist button loses focus.
# returns the button is a visually "unfocused" state. 
def on_focus_out(event, i):
    buttons[i].config(relief="raised", bg="gray90")  # Simulate button press
    buttons[i].update_idletasks()  # Force update
    print(f"on focus out: {i}")

# called when station combobox receives focus.
# makes sure its display is updated.
def on_focus_combobox(event):
    combobox.update_idletasks()  # Force update
    print("on_focus_combobox")

# called when station combobox loses focus.
# makes sure its display is updated.
def on_focus_out_combobox(event):
    combobox.update_idletasks()  # Force update
    print("on_focus_out_combobox")

# called when the Add button receives focus.
# visually indicates that the button has focus and
# makes sure its display is updated.
def on_focus_Add(event):
    button_Add.config(relief="raised", bg="darkgray")  # Simulate button press
    button_Add.update_idletasks()  # Force update
    print("on_focus_Add")

# called when the Add button loses focus.
# makes sure its display is updated.
def on_focus_out_Add(event):
    button_Add.config(relief="raised", bg="gray90")  # Simulate button press
    button_Add.update_idletasks()  # Force update
    print("on_focus_out_Add")

# called when the Del button receives focus.
# visually indicates that the button has focus and
# makes sure its display is updated.
def on_focus_Del(event):
    button_Del.config(relief="raised", bg="darkgray")  # Simulate button press
    button_Del.update_idletasks()  # Force update
    print("on_focus_Del")

# called when the Del button loses focus.
# makes sure its display is updated.
def on_focus_out_Del(event):
    button_Del.config(relief="raised", bg="gray90")  # Simulate button press
    button_Del.update_idletasks()  # Force update
    print("on_focus_out_Del")


####################################
# THIS IS WHERE THE CORE CODE STARTS

# Create the main window
root = tk.Tk()

# Set title, size and position of the main window, and make it non-resizable
strHeightForm = str(int(Xprog + 120 + Ydown))
print(strHeightForm)
root.title("INTERNET RADIO - https://github.com/namor5772/TkRadio")  
root.geometry("800x" + strHeightForm + "+0+0")
root.resizable(False, False)  

# Create a combobox (dropdown list)
# Used to display all avialable radio stations
aStringArray = []
for element in aStation:
    aStringArray.append(element[0])
combobox = ttk.Combobox(root, values=aStringArray, height=20, width=33)
combobox.place(x=130+(sizeButton+5), y=2)  # Adjust the position
combobox.bind("<FocusIn>", on_focus_combobox)
combobox.bind("<FocusOut>", on_focus_out_combobox)
combobox.bind("<<ComboboxSelected>>", lambda e: on_select(CustomEvent("Auto", combobox, "ComboBox Event")))
combobox.config(state="readonly")

# Populate if possible the playlist array aStation2[] from file saved at shutdown
try:
    with open(filepath2, 'r') as file:
        reader = csv.reader(file)
        aStation2 = [row for row in reader]     
except FileNotFoundError:
    # will just use the default aStation2[] array created above
    print(f'Error: The file {filepath2} does not exist.')

# Create a text box, position and size it
# used to display the program and song details
text_box = tk.Text(root)
text_box.place(x=10, y=110+Ydown, width=Xgap-20, height=Xprog)
text_box.config(state=tk.NORMAL) # Enable the text box to insert text
# height=600-110-10

# Create labels used for station logo image (label) and program related image (label2)
# Positioning of latter can vary
label = tk.Label(root)
label.pack()
label.place(x=15, y=2)
label2 = tk.Label(root)
label2.pack()

# Create [Add] button used for adding radio stations to playlist
button_Add = tk.Button(root, text="Add")
button_Add.place(x=400-25-15+70+(sizeButton+5), y=2, width=40, height=20)
button_Add.bind("<ButtonPress>", on_button_Add_press)
button_Add.bind("<Return>", on_button_Add_press)
button_Add.bind("<FocusIn>", on_focus_Add)
button_Add.bind("<FocusOut>", on_focus_out_Add)
    
# Create [Del] button used for deleting radio stations from playlist
button_Del = tk.Button(root, text="Del")
button_Del.place(x=450-25-15+70+(sizeButton+5), y=2, width=40, height=20)
button_Del.bind("<ButtonPress>", on_button_Del_press)
button_Del.bind("<Return>", on_button_Del_press)
button_Del.bind("<FocusIn>", on_focus_Del)
button_Del.bind("<FocusOut>", on_focus_out_Del)

# Create the playlist buttons (fully) and add them to the buttons[] list
buttons = []
for i in range(numButtons):
    # HELP
    button = tk.Button(root, text=f"Button{i}")

    # positioning buttons in 2 rows of 9
    if (i<9):
        button.place(x=128+(sizeButton+5)*(i+1), y=35, width=sizeButton, height=sizeButton)
    else:
        button.place(x=128+(sizeButton+5)*(i-8), y=35+sizeButton+5, width=sizeButton, height=sizeButton)

    button.config(bg="gray90")
    button.bind("<ButtonPress>", lambda event, i=i: on_button_press(event, i))  # Pass the extra parameter (i)
    button.bind("<Return>", lambda event, i=i: on_button_press(event, i))  # Pass the extra parameter (i)
    button.bind("<FocusIn>", lambda event, i=i: on_focus(event, i))
    button.bind("<FocusOut>", lambda event, i=i: on_focus_out(event, i))

    buttonImage = Image.open(pathImages + "/button" + str(i) +".png")
    buttonImage_resized = buttonImage.resize((sizeButton-5,sizeButton-5), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(buttonImage_resized)
    button.config(image=photo)
    button.image = photo
    button.update_idletasks()
    buttons.append(button)

# doing stuff just after the gui is initialised and we are running in the root thread
root.after(1000, after_GUI_started)
print("Radio stream interface")

# Bind the closing event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI loop
root.mainloop()
print("out of GUI loop..")
```

## Parts list

### Core components

Pricing and availability as of 27-Jan-2025. Total cost is $221.47, but clearly some of the items will be usable in many other projects or you will already have them. The pro rata cost is __$138.66__

You will also need a soldering iron and solder, some sellotape and a glue gun with glue sticks. Also some super glue.

| Qty | Product | Description | AUD Cost | Comment | Designator |
| --- | --- | --- | --- | --- | --- |
| 1 | [RP-SC1111](https://raspberry.piaustralia.com.au/products/raspberry-pi-5?variant=44207825617120) | [Raspberry PI 5B](ImagesDocs/RaspberryPI5.png) 4GB | $100.98 | The brains of this project | |
| 1 | [RP-SC1148](https://raspberry.piaustralia.com.au/products/raspberry-pi-active-cooler) | Raspberry Pi [Active Cooler](ImagesDocs/RPI5activeCooler.png) | $8.95 | Absolutely necessary to keep the RPI5 cool | |
| 1 | [XC9024](https://www.jaycar.com.au/p/XC9024) | [5 Inch Touchscreen](ImagesDocs/5inchTouchscreen.png) with HDMI and USB | $119.00 | based on the XPT1046 Touch Controller, see [Manual](Hardware/SR1230_manualMain_94019.pdf) | |
| 1 | [RP-SC1150](https://raspberry.piaustralia.com.au/products/raspberry-pi-27w-usb-c-power-supply?_pos=1&_psq=RP-SC1150&_ss=e&_v=1.0&variant=44207871328480) | Raspberry Pi 27W USB-C [Power Supply](ImagesDocs/PowerSupply.png) | $25.37 | Needed for power hungry Raspberry Pi5 | |
| 1 | [HD-203-0.3M](https://www.amazon.com.au/Thsucords-Micro-Flexible-Supports-18gbps/dp/B0BP29QTJ6/ref=sr_1_1?crid=XOGLPO6XRAKS&dib=eyJ2IjoiMSJ9.5fVBWJr2pX5EGbrBqtl4Rg.0vgcHY3JenNL7yyp8PRcAsHz90e8YfWwQgfYZRkr6tA&dib_tag=se&keywords=hd-203-0.3m&qid=1747122135&sprefix=%2Caps%2C238&sr=8-1&th=1) | Micro HDMI to HDMI [Cable](ImagesDocs/HDMIcable.png) 0.3M | $11.99 | Shortest cable needed for constrained space | |
| 1 | [XC3736](https://www.jaycar.com.au/p/XC3736) | Arduino Compatible Rotary [Encoder Module](ImagesDocs/EncoderModule.png) | $9.95 | Based on model KY-040, see [this](Hardware/XC3736_manualMain_94604.pdf), [this](Hardware/ky-040-datasheet.pdf) and [this](Hardware/KY-040.pdf)| U2 |
| 1 | [HK7011](https://jaycar.com.au/p/HK7011) | 29mm Black Anodised [Knob](ImagesDocs/KnobAnodised.png) | $9.95 | used on above Rotary Encoder Module | |
| 1 | [ZC4821](https://jaycar.com.au/p/ZC4821) | [74HC14](ImagesDocs/74HC14.png) Hex Schmitt trigger Inverter CMOS IC | $1.45 | Used in debouncing circuit, see [datasheet](Hardware/ZC4821_datasheetMain_40327.pdf) | U1 |
| 3 | [RM7125](https://jaycar.com.au/p/RM7125) | 100nF 100VDC MKT Polyester [Capacitor](ImagesDocs/PolyCap.png) | $1.20 | Used in debouncing circuit | C1, C2, C3 |
| 1 | [RC5324](https://jaycar.com.au/p/RC5324) | 100pF 50VDC Ceramic [Capacitors](ImagesDocs/CeramicCap.png) - Pack of 2 | $0.45 | Used in debouncing circuit | C4, $0.23 cost used |

### Other parts

| Qty | Product | Description | AUD Cost | Comment | Designator |
| --- | --- | --- | --- | --- | --- |
| 1 | [WW4030](https://jaycar.com.au/p/WW4030) | Tinned Copper [Wire](Images/CopperWire.png) 22AWG - 100 gram Roll | $19.95 | for wiring up above Vero board | $0.80 cost used|
| 1 | [HM3212](https://jaycar.com.au/p/HM3212) | 40 Pin Header Terminal [Strip](Images/TerminalStrip.png) (used most) | $1.10 | for soldering in sections to boards to attach to veroboard | |
| 1 | [WH3004](https://jaycar.com.au/p/WH3004) | Yellow Light Duty Hook-up [Wire](Images/WireYellow.png) - 25m (less than 30cm needed) | $5.95 | used for miscellaneous connections | $0.08 cost used |
| 1 | [WH3007](https://jaycar.com.au/p/WH3007) | White Light Duty Hook-up [Wire](Images/WireWhite.png) - 25m (less than 30cm needed) | $5.95 | used for miscellaneous connections | $0.08 cost used|
| 1 | [HP0924](https://jaycar.com.au/p/HP0924) | M3 x 12mm Tapped Nylon [Spacers](Images/Spacers.png) - Pk.25 (only need 4x 3mm)| $9.95 | For mounting screen to Jiffy case | $0.80 cost used |
| 1 | [HP0403](https://jaycar.com.au/p/HP0403) | M3 x 10mm Steel [Screws](Images/Screws.png) - Pk.25 (only need 4) | $2.95 | For mounting screen to Jiffy case | $0.48 cost used |
| 1 | [HP0425](https://jaycar.com.au/p/HP0425) | M3 Steel [Nuts](Images/Nuts.png) - Pk.25 (only need 4)| $2.95 | For mounting screen to Jiffy case | $0.48 cost used |
| 1 | [HP0148](https://jaycar.com.au/p/HP0148) | 3mm Nylon [Washers](Images/Washers.png) - Pk.10 (only need 0)| $2.50 | For mounting screen to Jiffy case | $0.00 cost used |
| 1 | [HM3230](https://jaycar.com.au/p/HM3230) | 40 Pin Female Header [Strip](Images/FemaleStrip.png) (only 8 used) | $2.50 | For mounting screen to Jiffy case | $0.50 cost used |
