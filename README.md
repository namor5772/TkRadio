# TkRadio
An Internet Radio that uses Python Tinker & Selenium

The main python file is called RadioSelenium-RP4B.py and it implements the internet radio on Windows 11 and Linux and in particular om a Raspberry Pi 4B. Will need to load many additional modules and processed for this will vary depending on the platform. The FireFox browser also needs to be loaded.

It has access to over 100 radio stations mainly available in Australia. It mostly accesses the streams via the stations websites in FireFox using Selenium for automation. When a station is streamed its logo is displayed. In addition the station and program text are displayed together with the program graphic (eg. the record sleeve for the album from which the current song is playing). This program information is automatically refreshed on a regular basis as the stream is playing.

For convenience you can create a playlist for up to 18 stations consisting of buttons that display the station logo. There is an [Add] button which adds/replaces a station to a selected button, while the [Del] button deletes the station from the button, deleting its logo and leaving the button graphic blank. The stations to be added are selected from the combobox which enables all available stations to be selected. You select a station from the combobox, then select a button and then bress the [Add] button.

Occasionally internet/website issues might cause a station to fail to stream or do so without, or not correctly refresh the program text and graphic. This can almost always be resolved by just selecting the station again. 


