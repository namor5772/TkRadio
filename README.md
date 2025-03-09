# TkRadio
An Internet Radio that uses Python with tkinter & selenium

The main python file is called RadioSelenium-RP4B.py and it implements the internet radio on Windows 11 and Linux and in particular on a Raspberry Pi 4B (although loading streams can sometimes be a bit slow). You will need to load many additional modules and the process for this will vary depending on the platform. The FireFox browser also needs to be loaded.

It has access to over 100 radio stations mainly available in Australia. It accesses the streams via the stations websites in FireFox using selenium for automation. When a station is streamed its logo is displayed. In addition the station and program text are displayed together with the program graphic (eg. the record sleeve for the album from which the current song is playing). This program information is refreshed about every 12 seconds as the stream is playing.

For convenience you can create a playlist for up to 18 stations consisting of buttons that display the station logo. There is an [Add] button which adds/replaces a station to a selected button, while the [Del] button deletes the station from the button/playlist, deleting its logo and leaving the button graphic blank. The stations to be added are selected from the combobox which enables all available stations to be streamed. You select a station from the combobox, then select a button and then press the [Add] button.

Occasionally internet/website issues might cause a station to fail to stream or or not correctly refresh the program text and graphic. This can almost always be resolved by just selecting the station again.

The currently playing station from the playlist is saved to file so that if the program is restarted it will automatically start streaming that station. The current playlist is also saved to file after any changes so that it is displayed after restart.

The RadioSelenium-RP4B.py python file can be launched from any directory as long as it contains the Images subdirectory and its files from the GitHub repository. The playlist and last streaming station files are assumed to be in the same directory.

Here we will describe in detail how to implement this radio as a dedicated app on a Raspberry Pi, in particular the hardware and software setup.

Below are two images of the applications GUI:
![alt text](image.png)

![alt text](image-1.png)

## Hardware

We use a Raspberry Pi 4B with 4GB of memory

## Software

Here we detail ALL the software needed for this project. Starting with the blank micro SD card that will contain all the software running on the Raspberry Pi.

1. Install the OS on a 32GB SanDisk Ultra 10 micro SD card (or equivalent). I used a Windows 11 PC with the Raspberry Pi Imager v1.8.5 app, selecting the Raspberry Pi OS (64-bit) Debian GNU/Linux 12 (bookworm). In the setup use:
    ```
    hostname:             rpi
    username:             {username}
    password:             {password}
    SSID:                 {SSID}
    password:             {SSID password}
    Wireless LAN country: AU
    locale:               Australia/Sydney
    keyboard:             us
    ```   
1. Place the SD card into the Raspberry Pi which is assumed to have a wireless mouse & keyboard connected, a HDMI monitor connected and USB powered stereo speakers connected to the 3.5mm jack. Power up the Raspberry Pi (by plugging in a USB-C 3A rated power pack). If everthing works it should boot into the GUI. Then:
    - Confirm that system connects to the internet or set it up via the taskbar.
    - Make the system have max volume using the slider available on the taskbar.
    - Open a terminal window and run the following commands:
        ```    
        sudo apt update
        sudo apt full-upgrade
        sudo apt autoremove
        sudo reboot        
        ```
1. Download the GitHub repository directory TkRadio and all its contents (including subdirectories) to your /__home/{username)/__ directory. You can do that via a USB stick or using Visual Studio Code directly from the Raspberry Pi you are using.
1. Install latest versions of Idle & Python
   - Python already installed with OS - Version 3.11.2
   - Install Idle from a terminal window with this command:
        ```
        sudo apt-get install idle
        ```
        When you start Idle from the taskbar, the Help => About IDLE menu selection should tell you that:
        ```
        Python version: 3.11.2
        Tk version: 8.6.13
        IDLE version: 3.11.2
        ```
1. Install the Python Imaging Library (PIL) from the terminal with:
    ```
    sudo apt-get update
    sudo apt-get install python3.pil python3.pil.imagetk
    ```
1. Install the Selenium library for Python from the terminal with:
    ```
    sudo apt_get install python3_pip
    python3 -m venv selenium_env
    source selenium_env/bin/activate
    pip install selenium
    sudo apt-get install python3-selenium
    ```
1. Install the gekodriver (necessary for selenium to operate with the FireFox browser):
    - From the https://github.com/mozilla/gekodriver/releases repository or otherwise download the tar.gz file __gekodriver-v0.36.0-linux-aarch64.tar.gz__ file to the __/home/{username}/Downloads__ directory and then from a terminal window run:
    ```
    cd /
    cd /home/{username}/Downloads
    tar -xvzf gekodriver-v0.36.0-linux-aarch64.tar.,gz
    sudo mv gekodriver /usr/local/bin
    gekodriver --version
    ```
1. Setup auto-start for this internet Radio app.
    - create a directory named autostart in the directory __/home/{username}/.config__ (it is hidden, so you need to use __ls -al__ to see it from the /home/{username} directory)  
    - in that autostart directory use __sudo nano__ via a terminal to create a file called __autoRadio.desktop__ with the following content:
    ```
    [Desktop Entry]
    Type=Application
    Exec=/usr/bin/idle -r /home/{username}/TkRadio/RadioSelenium-RP4B.py
    ```
1. Restart the Raspberry Pi, by unplugging power and plugging it back in after a short delay, OR just type __sudo reboot__ in a terminal window. If everything was correctly done then after about a minute delay the Radio App should start streaming a station (Make sure the volume is turned up on the speakers!)
     