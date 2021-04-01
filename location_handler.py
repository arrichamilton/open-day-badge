# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 00:27:55 2021

@author: TDP4 Team 3 2021
"""

import os
from os import path
from getmac import get_mac_address as gmc
import netifaces as nf
import board #Adafruit Blinka
import digitalio #RPi GPIO
import time #optional include

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
        '80:72:15:ef:aa:21': 'Self Test '      
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
        
def locationTiming(i):
    loc_int.append(location_conv(getMAC()))
    if loc_int[i] != loc_int[i - 1]:
        loc.append(loc_int[i])
        if loc[-1] == 'User Travelling':
            z = 1
        else:
            print('Do you like this place?')
            if button.value == 'Yes':
                info_conv(loc[-1])
                print(info_conv(loc[-1]))
    else:
        print("same location")
    
    if path.exists("C://Users/Arric/Documents/test_loc.txt") == True:
        with open("C://Users/Arric/Documents/test_loc.txt", "a") as locSave:
            locSave.write(loc[-1])
    else:
         with open("test_loc.txt", "a") as locSave:
             locSave.write(loc[-1])
    i+=1
    #temp = CPUtemp() #optional CPU temp
    #usage = CPUuse() #CPU usage
    #ram = freeRAM() #RAM usage
    
#Raspberry Pi GPIO setup 
button = digitalio.DigitalInOut(board.D18)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN

loc_int = []
loc = []
loc_int.append(location_conv(getMAC())) #start locations
loc.append(location_conv(getMAC())) 
i=0

for k in range(0,10,1):
    locationTiming(i)

    

