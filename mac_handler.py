# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 22:07:24 2021

@author: Arric Hamilton
"""

import time as ti
from getmac import get_mac_address as gmc
import netifaces
      
t=0
while(t<14400): #4h
    gw=netifaces.gateways() #refreshes gateways
    mac=gmc(ip=list(gw['default'].values())[0][0])
    ti.sleep(3600)
    t+=3600 #10m