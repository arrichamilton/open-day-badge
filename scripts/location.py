# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 00:27:55 2021
@author: TDP4 Team 3 2021
To-Do List:
    1) Process check against emulation station
    2) Change timings for QR Display 
    3) Capitalize MAC addresses
"""
import os
from os import path
import rssi
import time
import qrcode
from PIL import Image
import board  # Adafruit Blinka
import digitalio  # RPi GPIO

# GPIO setup
startB = digitalio.DigitalInOut(board.D5)  # START button
startB.direction = digitalio.Direction.INPUT
startB.pull = digitalio.Pull.UP
selB = digitalio.DigitalInOut(board.D23)  # SEL button
selB.direction = digitalio.Direction.INPUT
selB.pull = digitalio.Pull.UP

# display drivers
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ['SDL_VIDEODRIVER'] = "fbcon"  # error with current config

#RSSI config
interface = 'wlan0'
rssi_scanner = rssi.RSSI_Scan(interface)
info=rssi_scanner.getRawNetworkScan()

def killPID(pid):
    if pid == 'None':
        print("fbcp not running!")
    else:
        os.kill(pid, 9)

def openPID(pid):
    if pid != 'None':
        print("fbcp already running!")
    else:
        import subprocess
        subprocess.Popen([r'fbcp'])

def checkPID():
    import subprocess
    subprocess = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    output, error = subprocess.communicate()

    target_process = "fbcp"
    for line in output.splitlines():
        if target_process in str(line):
            pid = int(line.split(None, 1)[0])
            break
        else:
            pid = 'None'
    return pid

def info_conv(place):
    information = {
        'Rankine ': 'https://universitystory.gla.ac.uk/building/?id=18 ',
        'Library ': 'https://universitystory.gla.ac.uk/building/?id=69 ',
        'James Watt School of Engineering ': 'https://universitystory.gla.ac.uk/building/?id=112',
        'Glasgow University Union ': 'https://universitystory.gla.ac.uk/building/?id=50',
        'Fraser Building ': 'https://universitystory.gla.ac.uk/building/?id=71',
        'Boyd Orr ': 'https://universitystory.gla.ac.uk/building/?id=40',
        'Queen Margaret Union ': 'https://universitystory.gla.ac.uk/building/?id=19',
        'East ': 'https://en.wikipedia.org/wiki/University_of_Glasgow',
        'West ': 'https://en.wikipedia.org/wiki/University_of_Glasgow',
        'Self Test ': 'Self Test',
    }
    return information.get(place, 'None')

def location_conv(name):
    address = {
        '00:2a:10:57:35:31': 'Rankine ',
        '00:2a:10:9b:8a:b1': 'Library ',
        'f8:4f:57:3a:21:11': 'James Watt School of Engineering ',
        'd4:6d:50:f3:11:21': 'Glasgow University Union ',
        '84:78:ac:f0:22:a1': 'Fraser Building ',
        'ec:e1:a9:6e:be:81': 'Boyd Orr ',
        '00:2a:10:93:bf:f1': 'Queen Margaret Union ',
        '70:79:b3:2d:6f:a1': 'East ',
        'b8:62:1f:ac:60:81': 'West ',
        '80:72:15:EF:AA:22': 'Self Test'
    }
    return address.get(name, 'User Travelling ')

def CPUtemp():
    res = os.popen('vcgencmd measure_temp').readline()
    return (res.replace("temp=", "").replace("'C\n", ""))

def freeRAM():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return (int(line.split()[3]) / 1024)

def CPUuse():
    return (str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip( \
        )))

def freeDisk():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return (int(line.split()[3]))

def getMAC():
    class Cells:
        def __init__(self):
            self.addr = 0
            self.q = 0

    cell_count = str(info).count("Cell")  # counts the number of times "Cell" occurs in the text above
    cell = [Cells() for i in range(cell_count)]  # creates instances of the class for each cell
    jmac = 0  # counters to maintain cell count
    kmac = 0

    text = str(info).split("                    ")  # splits text into multiple lines according to breaks in spacing

    for i in range(len(text)):  # runs through all lines of text
        if "Cell" in text[i]:  # checks if the string contains "cell"
            cell[jmac].addr = text[i].split('Address: ')[1].split('\\n')[0]  # sets the class address to the text without the information around it
            jmac += 1
        if "Quality" in text[i]:
            cell[kmac].q = text[i].split('Quality=')[1].split(' Signal')[0]
            kmac += 1

    """for i in range(cell_count): #troubleshooting ONLY
        print(cell[i].addr)
        print(cell[i].q)"""

    best_cell_no = 0
    cellBest = cell[0].q
    for i in range(cell_count):
        if cellBest < cell[i].q:
            cellBest = cell[i].q
            best_cell_no = i
    mac = cell[best_cell_no].addr
    print("Best quality:", mac)
    return mac

def qrGen(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)  # QR class
    qr.add_data(data)  # Configurable QR text
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('/home/pi/scripts/qr.bmp')
    im = Image.open('/home/pi/scripts/qr.bmp')
    im_resized = im.resize((128, 160))  # resize to display
    im_resized.save('/home/pi/scripts/qr.bmp')

def qrDisp():
    qrCode = pygame.image.load('/home/pi/scripts/qr.bmp')
    screen.fill((0, 0, 0))
    screen.blit(qrCode, (0, 0))

def pygameInit():  # efficient init
    global pygame
    import pygame
    global screen
    pygame.init()
    size = width, height = 128, 160
    screen = pygame.display.set_mode(size)
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))

def displaytext(text, size, line, color, clearscreen):
    if clearscreen:
        screen.fill((1, 53, 99))

    font = pygame.font.Font(None, size)
    text = font.render(text, 0, color)
    rotated = pygame.transform.rotate(text, 270)
    textpos = rotated.get_rect()
    textpos.centery = 80
    if line == 3:
        textpos.centerx = 99
        screen.blit(rotated, textpos)
    elif line == 2:
        textpos.centerx = 72
        screen.blit(rotated, textpos)
    elif line == 1:
        textpos.centerx = 20
        screen.blit(rotated, textpos)

def locationInput(loc, loc_int, i, pidFlag):
    loc_int.append(location_conv(getMAC()))

    with open("/home/pi/scripts/loc_int.txt", "a") as locSave:  # write new value
        locSave.write(loc_int[-1] + "\n")

    # create str from list
    strInt = ''.join(loc_int[-1])
    strIntPre = ''.join(loc_int[i - 1])
    strLoc = ''.join(loc[-1])

    if i > 0:  # avoids start run
        if strInt != strIntPre:
            loc.append(strInt)
            if strLoc == 'User Travelling':
                z = 1  # do nothing
            else:
                if pidFlag == True:
                    killPID(checkPID())
                pygameInit()
                displaytext("Like to know more", 20, 3, (255, 255, 255), True)
                displaytext("about this location?", 20, 2, (255, 255, 255), False)
                displaytext("START (Y) / SEL (N)", 20, 1, (255, 255, 255), False)
                pygame.display.flip()

                strt = startB.value
                sel = selB.value
                while True == (sel or strt):
                    if not (startB.value):
                        print("START: Printing QR")
                        x = info_conv(strLoc)
                        qrGen(x)
                        qrDisp()
                        pygame.display.flip()
                        time.sleep(10)
                        load = 1
                        break

                    elif not (selB.value):
                        print("SEL")
                        load = 1
                        break
                    else:
                        time.sleep(2)  # update for button
                        print("Waiting")

        else:
            load = 0
            print("Same Location")

        # Loading screen
        if load:
            loading = "Loading"
            for p in range(3):
                loading = loading + "."
                displaytext(loading, 30, 2, (100, 100, 255), True)
                pygame.display.flip()
                time.sleep(0.5)

    if pidFlag == True:
        openPID(checkPID())

    # text file save + self test
    if path.exists("C://Users/Arric/Documents/test_loc.txt") == True:
        with open("C://Users/Arric/Documents/test_loc.txt", "a") as locSave:
            locSave.write(strLoc + "\n")
    else:
        with open("/home/pi/scripts/loc.txt", "a") as locSave:
            locSave.write(strLoc + "\n")
    # temp = CPUtemp() #optional CPU temp
    # usage = CPUuse() #CPU usage
    # ram = freeRAM() #RAM usage

def main():
    print("Succesfully loaded script")
    if checkPID() == 'None':
        pidFlag = False
    else:
        pidFlag = True

    loc_int = []
    loc = []

    if path.exists("/home/pi/scripts/loc_int.txt") == True:
        with open('/home/pi/scripts/loc_int.txt') as f:
            for line in f:
                inner = [elt.strip() for elt in line.split(',')]
                loc_int.append(inner)

        if path.exists("/home/pi/scripts/loc.txt") == True:
            with open('/home/pi/scripts/loc.txt') as f:
                for line in f:
                    inner = [elt.strip() for elt in line.split(',')]
                    loc.append(inner)
        i = len(loc_int)
    else:
        print("Start Detected")
        i = 0
        loc_int.append(location_conv(getMAC()))  # start locations
        loc.append(location_conv(getMAC()))

    locationInput(loc, loc_int, i, pidFlag)

if __name__ == '__main__':
    main()