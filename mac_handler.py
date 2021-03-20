# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 22:07:24 2021

@author: Arric Hamilton
"""
import os
import time as ti
from getmac import get_mac_address as gmc
import netifaces as nf
                                           
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

t=0
while(t<14400): #4h
    mac = gmc(ip=list(nf.gateways()['default'].values())[0][0])
    temp = CPUtemp()
    usage = CPUuse()
    ram = freeRAM()
    ti.sleep(3600)
    t+=3600 #10m