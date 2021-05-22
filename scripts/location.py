# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 00:27:55 2021
@author: TDP4 Team 3 2021
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
        'Rankine ': 'r ',
        'Library ': 'l',
        'James Watt School of Engineering ': 'j',
        'Glasgow University Union ': 'g',
        'Fraser Building ': 'f',
        'Boyd Orr ': 'b',
        'Queen Margaret Union ': 'q',
    }
    return information.get(place, 'None')

def location_conv(name):
    address = {
        '00:2A:10:57:35:31': 'Rankine ',
        '00:2A:10:9B:8A:B1': 'Library ',
        'F8:4F:57:3A:21:11': 'James Watt School of Engineering ',
        'D4:6D:50:F3:11:21': 'Glasgow University Union ',
        '84:78:AC:F0:22:A1': 'Fraser Building ',
        'EC:E1:A9:6E:BE:81': 'Boyd Orr ',
        '00:2A:10:93:BF:F1': 'Queen Margaret Union ',
        #'70:79:B3:2D:6F:A1': 'East ',
        #'B8:62:1F:AC:60:81': 'West ',
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

    best_cell_num = 0
    cellBest = cell[0].q
    for i in range(cell_count):
        if cellBest < cell[i].q:
            cellBest = cell[i].q
            best_cell_num = i
    mac = cell[best_cell_num].addr
    print("Best quality:", mac)
    return mac

def qrGen(data):
    x = "https://prospectusgla.000webhostapp.com/?buildings=" + data
    qr = qrcode.QRCode(version=1, box_size=10, border=5)  # QR class
    qr.add_data(x)  # Configurable QR text
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
                z = 1  #do nothing
        else:
            print("Same Location")
            
        if i > 120:
            if pidFlag == True:
                #additional GPIO setup
                aB = digitalio.DigitalInOut(board.D22) #A button
                aB.direction = digitalio.Direction.INPUT
                aB.pull = digitalio.Pull.UP
                rightB = digitalio.DigitalInOut(board.D15) #RIGHT button
                rightB.direction = digitalio.Direction.INPUT
                rightB.pull = digitalio.Pull.UP
                upB = digitalio.DigitalInOut(board.D14) #UP button
                upB.direction = digitalio.Direction.INPUT
                upB.pull = digitalio.Pull.UP
                downB = digitalio.DigitalInOut(board.D18) #DOWN button
                downB.direction = digitalio.Direction.INPUT
                downB.pull = digitalio.Pull.UP
                
                strt=startB.value
                sel=selB.value
                a=aB.value
                r=rightB.value
                up=upB.value
                down=downB.value
                
                bcounter=0
                
                while True == (sel or strt or a or r or up or down):
                    if not(startB.value or selB.value or aB.value or rightB.value or upB.value or downB.value):
                        print("button detected")
                        bcounter=0
                    else:
                        bcounter+=1
                    time.sleep(1)
                    
                    if bcounter==30:
                        killPID(checkPID())
                        break
                
            pygameInit()
            displaytext("Like to know more", 20, 3, (255, 255, 255), True)
            displaytext("about your visits?", 20, 2, (255, 255, 255), False)
            displaytext("START (Y) / SEL (N)", 20, 1, (255, 255, 255), False)
            pygame.display.flip()

            strt = startB.value
            sel = selB.value
            while True == (sel or strt):
                if not (startB.value):
                    print("START: Printing QR")
                    
                    strQR=[]
                    data=""
                    for i in range(len(loc)):
                        strQR.append(info_conv(''.join(loc[i])))
                        data = data+strQR[i]   
                        
                    qrGen(data)
                    qrDisp()
                    pygame.display.flip()
                    strt = startB.value
                    while True == strt:
                        print("waiting for strt")
                        if not (startB.value):
                            break
                    break

                elif not (selB.value):
                    print("SEL: Not Printing QR")
                    if pidFlag == True:
                        openPID(checkPID())
                    break
                else:
                    time.sleep(1)  # update for button
                    print("Waiting")

            # text file save 
            with open("/home/pi/scripts/loc.txt", "a") as locSave:
                locSave.write(strLoc + "\n")
            
    if i == 0:
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
        print("Initial Run")
        i = 0
        loc_int.append(location_conv(getMAC())) # start locations
        loc.append(location_conv(getMAC()))

    locationInput(loc, loc_int, i, pidFlag)

if __name__ == '__main__':
    main()