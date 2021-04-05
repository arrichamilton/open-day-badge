# open-day-badge

Retropie configuration files for ST7735R

Further testing REQUIRED to ensure complete functionality. 

# Scripts
- mac_handler.py - converts gateway IP to determine MAC address
- location_detector.py - matches MAC to building location_detector
- location_handler.py - combines mac handler and location detector scripts
- pid_kill.py - kills a PID on the RPi
- qr_gen.py - generates, resizes, and outputs a QR code to the RPi

# Config/Boot Files
- config.txt - boot config file for retropie /boot/config.txt
- fbtft.conf - TFT framebuffer configuration file /etc/modprobe.d/fbtft.conf  
- rc.local - Scripts run when device booted /etc/rc.local
- wpa_supplicant.conf - Copy to /boot/ to setup Wi-Fi
- ssh - Copy to /boot/ to enable SSH when flashing an image

# Useful links:
- PiShrink Image Resizer [github](https://github.com/Drewsif/PiShrink)
- 128x160 GU Logo [imgur](https://i.imgur.com/65o2n7P.png)
