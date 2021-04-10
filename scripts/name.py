# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 14:38:31 2021

@author: TDP4 Team 3 
"""
import pygame
import os
import board #Adafruit Blinka
import digitalio #RPi GPIO
import time

#GPIO setup 
startB = digitalio.DigitalInOut(board.D5) #START button
startB.direction = digitalio.Direction.INPUT
startB.pull = digitalio.Pull.UP

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ['SDL_VIDEODRIVER']="fbcon"

def killPID(pid):
    if pid=='None':
        print("fbcp not running!")
    else:
        os.kill(pid, 9)
        
def openPID(pid):
    if pid!='None':
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
            pid='None'        
    return pid
   
def displayText(text,size,line,color,clearscreen):
   if clearscreen:
       screen.fill((1,53,99))

   font = pygame.font.Font(None,size)
   text = font.render(text,0,color)
   rotated = pygame.transform.rotate(text,270)
   textpos = rotated.get_rect()
   textpos.centery = 80
   if line == 2:
        textpos.centerx = 20
        screen.blit(rotated,textpos)
   elif line == 1:
        textpos.centerx = 80
        screen.blit(rotated,textpos)
   elif line == 3:
        textpos.centerx = 72
        screen.blit(rotated,textpos)
    
global screen
killPID(checkPID())
pygame.init()
size = width,height = 128,160
screen = pygame.display.set_mode(size)
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
bg = pygame.image.load('/home/pi/scripts/bg.png')
pygame.display.flip()

for o in range(2):
    loading="Loading"
    for p in range(3):
        loading=loading+"."
        displayText(loading,30,3,(100,100,255),True)
        pygame.display.flip()
        time.sleep(0.5)

i=0
START=startB.value
while(START==True):
    username="Arric"
    displayText(username,50,1,(255,255,255),True)
    displayText("Press START to exit",15,2,(255,255,255),False)
    screen.blit(bg, (80,125))
    pygame.display.flip()
    time.sleep(0.5)
    if not(i%5): #5s
        killPID(checkPID())
    i+=1
    if startB.value==False:
        openPID(checkPID())
        exit()