# TkRadio

### **The best way to load this software and build instructions is to Clone this Git Repository using Visual Studio Code.**

Here the building of an Internet Radio will be described in detail.
The software uses Python with tkinter and selenium, while the hardware is based on a Raspberry Pi 5.

As a standalone app (RadioSelenium.py) it can also be run under the Windows 11 OS (or other Linux versions). In those cases the installation of additional Python modules and other software setup will be significantly different and not described here (though somewhat in the [Windows setup](#windows-setup) section). The best way to do this in these cases is to try to run it and then correct errors by installing required modules or adjusting settings. Wifi/internet connections and bluetooth speakers have to be managed explicitly through the OS. RadioSelenium.py is also the file for the Raspberry Pi hardware.

The radio software has access to about 79500 radio stations with about 132 from Australia. It accesses these streams via the stations websites via the FireFox browser using selenium for automation. When a station is streamed its logo is displayed. In addition if available the stations program text is displayed together with the programs graphic (eg. the record sleeve for the album from which the current song is playing). The default is for this program information to be refreshed approximately every 12 seconds while the stream is playing.

For convenience you can create a playlist for up to 54 stations (Raspberry Pi or 108 for Windows) consisting of a matrix of buttons that display the station logos. With a playlist button selected/in focus, pressing the [Delete] key deletes the radio station assigned to that playlist button leaving the graphic blank. Similarily when the [Insert] key is pressed the station that was previously selected from the combobox is assigned to the playlist button overwiting the previous graphic.

Occasionally internet/website issues might cause a station to fail to stream or not correctly refresh the program text and graphic. This can almost always be resolved by just selecting the station again. Rarely you might need to restart the radio.

Details of the station (from the playlist) currently playing is saved to a file so that if the program is restarted it will automatically start streaming that station. The current playlist is also saved to file after any changes so that it is displayed after restart.

The RadioSelenium.py python file can be launched from any directory as long as it contains the Images subdirectory and its files from the GitHub repository. The playlist.txt, savedRadioStation.txt, bluetooth.txt, pollflag.txt, AllRadioStations.csv and StationLogs.txt files are assumed to be in the same directory as well.

When run on a Raspberry Pi the softwares gui also has a secondary form for pairing/connecting to bluetooth speakers (the default being external speakers attached to a USB port of the Raspberry Pi). In addition the connection to the wifi network can also be explicitly made through this apps form when running on a Raspberry Pi. This is necessary since when running on a Raspberry Pi, interfacing is only available through buttons with no mouse or keyboard assumed to be connected.

In the Windows case of the software we also have a text box at the bottom of the main form that can display ai generated information about the currently playing radio station. To enable this you will need to have an OpenAI account and an API Key. 

Main and only form when run on a windows PC, with ai station summary available on bottom text panel.
![app GUI image1a](ImagesDocs/imageGUI1a.png)
![app GUI image1b](ImagesDocs/imageGUI1b.png)

Main and secondary forms when run on a Raspberry Pi with PRi.GPIO module available, but no ai.
![app GUI image2a](ImagesDocs/imageGUI2a.png)
![app GUI image2b](ImagesDocs/imageGUI2b.png)
![app GUI image2c](ImagesDocs/imageGUI2c.png)

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
    Exec=/usr/bin/idle -r /home/{username}/TkRadio/RadioSelenium.py
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
C:\Users\grobl\AppData\Local\Programs\Python\Python312\pythonw.exe "C:\Users\grobl\OneDrive\GitRepos\TkRadio\RadioSelenium.py"
```

Press the [Next] button.
In the following text box titled "Type a name for this shortcut" type "RADIO" (replacing "pythonw.exe").
Press the [Finish] button.
This new shortcut then appears on the desktop with the Python icon. This can be changed if you desire. Interestingly when examining the Properties of this shortcut we have (automatically generated) the following properties:

```text
Target location: Python312
Target: C:\Users\grobl\AppData\Local\Programs\Python\Python312\pythonw.exe "C:\Users\grobl\OneDrive\GitRepos\TkRadio\RadioSelenium.py"
Start in: C:\Users\grobl\AppData\Local\Programs\Python\Python312
```

Clearly the will vary depending on which directories containing the Python script and the Python executable.

## Python Script

Here we describe the design and use of the python script [RadioSelenium.py](RadioSelenium.py) that implements the gui interface to this web radio.

The core purpose of this python script is to stream a selected internet radio station, as well as displaying and refreshing any program details and graphics approximately every 12 seconds (while the station is streaming). The station Logo is also displayed.
The details of the available approximately 79500 stations are maintained in the [TkRadio\AllRadioStations.csv](AllRadioStations.csv) file that is assumed to be in the same directory as the python script (ie. \TkRadio). 

Below are a sample 4 rows from this csv file

```text
smoothfm Brisbane,smoothfm_Brisbane,Commercial1,0,https://smooth.com.au/station/brisbane,index_smooth_info-wrapper-desktop__6ZYTT,1
smoothfm Perth,smoothfm_Perth,Commercial1,0,https://smooth.com.au/station/smoothfmperth,index_smooth_info-wrapper-desktop__6ZYTT,1
ab 101.6 Marites FM Radio,ab_101-6_Marites_FM_Radio,Commercial2,0,https://www.radioarabic.org/sa/1016-marites-fm-radio,Arabic,0
ab 101.8artysfm,ab_101-8artysfm,Commercial2,0,https://www.radioarabic.org/sa/rm-heart-fm,Arabic,0
```

Each row consists of 7 comma deliminated entries as follows:

1. The unique name of the station
2. The name of the stations logo.png file (which is stored in the \TkRadio\Images directory)
3. Name of the python function that actually accesses the station website and runs the stream etc. (all have same arguments)
4. 1st arg, integer, value depends on function and station (often 0)
5. 2nd arg, radio stations website url
6. 3rd arg, string argument, value depends on function and station (often empty)
7. 4th arg, integer, value depends on function and station (usually 0 or 1) 

The core functions that actually stream a radio station are on_select(event) and on_select2(event). The first is called when a radio station is selected from the main combobox. The second is called when a radio station is called by pressing a playlist button. They could/should be made into the same function. They also obtain the station and program details and image if available. A crucial feature is that if the PollFlag==True the on_select() or on_select2() functions are scheduled to run again repeatedly after refreshTime seconds (about 12 seconds) until a new station is selected to stream. This refreshes the program details and image of the stream if any is available.

The PollFlag is toggled by a button. In the Windows case it is in the top right hand corner of the main (and only screen) and has the text [ON] or [OFF]. In the Raspberry Pi case this button is on the secondary setup screen and has the text [Polling is ON] or [Polling is OFF]. The state of the PollFlag is maintained in the \TkRadio\pollflag.txt file, and enables it to be restored after the application is restarted.

Even thought the script runs a gui it has been designed to be interfaced purely using the keyboard (no mouse necessary, in the Windows case and via a virtual keyboard in the Raspberry Pi case). This is to facilitate the Raspberry Pi version with its hardware setup. The [Tab] and [Shift-Tab] (also called [ISO_Left_Tab]) keys can be used to navigate focus among all available gui elements like comboboxes, comboboxes, textboxes or buttons. Below what what can be done in the gui is described in detail in terms of key presses:

**With focus on a combobox** the dropdown list can be displayed by pressing the [Down] key, thereafter you can navigate up and down this list by pressing the [Up] or [Down] keys. To enable "faster" movement you can also press the [PgUp] or [PgDn] keys. If you want to exit out of the dropdown without doing anything just press [Tab] or [Shift-Tab].
There are at most three comboboxes available:

1. The most important one is on the main form. It is used to select any of the available radio stations for streaming. Once you are on a desired Radio Station you start it by pressing the [Enter] key.
2. The leftmost one on the setup screen. Press [Enter] to select a Blue Tooth speaker to pair to.
3. The rightmost one on the setup screen. Press [Enter] to select a Wifi network to connect to. Each one has a signal strength score, with Q70 being the strongest (go figure).

**With focus on textboxes** there are two cases:

1. The textboxes on the main form. These are for information only and as such they can get focus by using the [Tab] or [Shift-Tab] keys, in which case their background will be light blue. Once "inside" you can scroll up or down if necessary to see any text that does not fit in the textbox by pressing the [PgUp] or [PgDn] keys. As usual you can exit the textbox by pressing the [Tab] or [Shift-Tab] keys. One textbox is used to display station and program information. While another one (only available in the Windows version) displays detailed AI generated information about the currently streaming station.
2. The "password" textbox on the setup page. it only available when running the script on a Raspberry Pi. It is used to input the password for a WIFI network that has not previously been used. You type the password in the usual way and then press the [Enter] key when finished.

**With focus on buttons** we can move focus from them by pressing the [Tab] or [Shift-Tab] keys:

1. The [RND] button. When the [Enter] key is pressed a random station from the available list (\TkRadio\AllRadioStations.csv) is streamed.
2. The [DEL] button. When tthe [Delete] key is pressed the currently "streaming" station is permanently deleted from the available list (\TkRadio\AllRadioStations.csv). Any necessary adjustments are made to the playlist buttons. The [Enter] key is not used to cause action, because it might cause deletion by mistake!
3. The [SAVE] button. When the [Enter] key is pressed details about the currently streaming station are appended to the [tkRadio\StationLogs.txt](StationLogs.txt) file. If Running under Windows this might include AI generated content.
4. The [AI] button. Only available when running under Windows. When the [Enter] key is pressed detailed information about the currently streaming station are generated by AI and placed in the lower textbox.
5. The [View] button. When the [Enter] key is pressed toggling occurs between a partial or complete view of playlist buttons. The partial view shows a 2 row by 9 column matrix of 18 playlist buttons. The complete view shows a 6 row by 9 column matrix of 54 buttons in the Raspberry Pi case but a 12 row by 9 column matrix of 108 buttons in the Winbdows case. The complete view obscures any information about the radio station currently streaming, except for the stations logo visible in the top left hand corner of the main screen.
6. The PollFlag button. In the Windows case it is in the in the top right hand corner of the main screen and displays [ON] with a green background or [OFF] with a red background. In the Raspberry Pi case this button is on at the top of the right hand side of the setup screen and displays [Polling is ON] with a green background of [Polling is OFF] with a red background. Pressing the [Enter] key toggles between the two states as discussed previously.
7. The [+] buttons. Only available in the Raspberry Pi case. They are located at the top right hand corner of the main and setup displays. When the [Enter] key is pressed on the button in the main screen, the setup screen becomes visible and focus is shifted to the button on the setup screen. Similarily when the [Enter] key is pressed on the button in the setup screen, the main screen becomes visible and focus is shifted to button on the mainm screen.
8. **The matrix of playlist buttons.** If populated they display a logo for a particular radio station. For convenience on can traverse focusing among these buttons by using the [Up], [Down], [Left] and [Right] keys. This works in the obvious way, however if you press the [Down] key on a playlist button which is in the lowest row then nothing happens, similarily if you press the [Left] key on a button in the leftmost column or if you press the [Right] key on a button in the rightmost column. If you press the [Up] key on a button in the top row focus will pass to............................

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
