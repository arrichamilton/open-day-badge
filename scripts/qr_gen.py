# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 16:33:35 2021

@author: Arric Hamilton
"""

import os
import sys
import time
import qrcode
import pygame
from PIL import Image

qr = qrcode.QRCode(version=1,box_size=10,border=5) #QR class
qr.add_data("123test") #Configurable QR text
qr.make(fit=True)
img = qr.make_image(fill='black', back_color='white')
img.save('qr_demo.png')
im = Image.open('qr_demo.png')
im_resized=im.resize((128,160)) #resize to display
im_resized.save('qr_demo.png') 

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ['SDL_VIDEODRIVER']="fbcon"

qrCode = pygame.image.load('qr_demo.png')

def qr(x,y):
    screen.fill((0,0,0))
    screen.blit(qrCode, (x,y))

def main():
    global screen
    pygame.init()
    size = width,height = 128,160
    screen = pygame.display.set_mode(size)
    x,y=0,0

    while True:
        qr(x,y)
        pygame.display.flip()
        time.sleep(1)

if __name__ == '__main__':
    main()