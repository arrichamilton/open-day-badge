# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 00:27:55 2021

@author: TDP4 Team 3 2021

To-Do List:
    1) Process check against emulation station
"""
import os
from os import path
from getmac import get_mac_address as gmc
import netifaces as nf
import time
import qrcode
import pygame
from PIL import Image
import board #Adafruit Blinka
import digitalio #RPi GPIO

#GPIO setup 
startB = digitalio.DigitalInOut(board.D5) #START button
startB.direction = digitalio.Direction.INPUT
startB.pull = digitalio.Pull.UP
selB = digitalio.DigitalInOut(board.D23) #SEL button
selB.direction = digitalio.Direction.INPUT
selB.pull = digitalio.Pull.UP

#display drivers
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ['SDL_VIDEODRIVER']="fbcon"

def killPid():
    import subprocess
    subprocess = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    output, error = subprocess.communicate()
    
    target_process = "fbcp"
    for line in output.splitlines():
        if target_process in str(line):
            pid = int(line.split(None, 1)[0])
            os.kill(pid, 9)

def openPID():
    import subprocess
    subprocess.Popen([r'fbcp'])

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
        '80:72:15:ef:aa:21': 'Self Test'
    }
    return address.get(name, 'User Travelling ')

def CPUtemp():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def freeRAM():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(int(line.split()[3])/1024)
            
def CPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))

def freeDisk():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(int(line.split()[3]))

def getMAC():
    return gmc(ip=list(nf.gateways()['default'].values())[0][0])

def qrGen(data):
    qr = qrcode.QRCode(version=1,box_size=10,border=5) #QR class
    qr.add_data(data) #Configurable QR text
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('qr.png')
    im = Image.open('qr.png')
    im_resized=im.resize((128,160)) #resize to display
    im_resized.save('qr.png') 

def qrDisp():
    qrCode = pygame.image.load('qr.png')
    screen.fill((0,0,0))
    screen.blit(qrCode, (0,0))
    
def displaytext(text,size,line,color,clearscreen):
   if clearscreen:
       screen.fill((1,53,99))

   font = pygame.font.Font(None,size)
   text = font.render(text,0,color)
   rotated = pygame.transform.rotate(text,90)
   textpos = rotated.get_rect()
   textpos.centery = 80
   if line == 1:
        textpos.centerx = 99
        screen.blit(rotated,textpos)
   elif line == 2:
        textpos.centerx = 61
        screen.blit(rotated,textpos)
   elif line == 3:
        textpos.centerx = 40
        screen.blit(rotated,textpos)

def locationInput(loc,loc_int,i):
    loc_int.append(location_conv(getMAC()))
    """#TEST FUNCTION
    if i == 4:
        loc_int[i] = 'East '
    """
    if loc_int[i] != loc_int[i-1]:
        loc.append(loc_int[i])
        if loc[-1] == 'User Travelling':
            z=1
        else:
            killPid()
            displaytext("Like to know more",20,3,(255,255,255),True)
            displaytext("about this location?",20,2,(255,255,255),False)
            displaytext("START (Y) / SEL (N)",20,1,(255,255,255),False)
            pygame.display.flip()
            
            strt = startB.value
            sel = selB.value
            while True =(sel or strt):
                if startB.value:
                    print("START, Printing QR")
                    x=info_conv(loc[-1])
                    qrGen(x)
                    qrDisp()
                    pygame.display.flip()
                    time.sleep(10)
                    load=True
                    break
                    
                elif selB.value:
                    print("SEL")
                    load=True
                    break
                else: 
                    time.sleep(2)
                    print("Waiting")
                    
    else:
        load = False
        openPID()
        print("Same Location")
    
    #Loading screen
    if load:
        loading="Loading"
        for p in range(3):
            loading=loading+"."
            displaytext(loading,30,2,(100,100,255),True)
            pygame.display.flip()
            time.sleep(0.5)
    
    #text file save + self test
    if path.exists("C://Users/Arric/Documents/test_loc.txt") == True:
        with open("C://Users/Arric/Documents/test_loc.txt", "a") as locSave:
            locSave.write(loc[-1])
    else:
         with open("loc.txt", "a") as locSave:
             locSave.write(loc[-1])
    #temp = CPUtemp() #optional CPU temp
    #usage = CPUuse() #CPU usage
    #ram = freeRAM() #RAM usage

def main():
    global screen
    pygame.init()
    pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0)) #hides cursor
    size = width,height = 128,160
    screen = pygame.display.set_mode(size)
    
    #start loc needs fixed
    loc_int = []
    loc = []
    loc_int.append(location_conv(getMAC())) #start locations
    loc.append(location_conv(getMAC())) 
    i=0
    
    #main loop
    for k in range(0,10,1):
        locationInput(loc,loc_int,i)
        time.sleep(1)
        i+=1

if __name__ == '__main__':
    main()