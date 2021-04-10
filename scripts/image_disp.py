# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 22:55:06 2021

@author: Arric Hamilton
"""
import pygame
import os

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ['SDL_VIDEODRIVER']="fbcon"

global screen
pygame.init()
size = width,height = 128,160
screen = pygame.display.set_mode(size)
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0)) #hide cur
screen.fill((1,53,99))
pygame.display.flip()

image = pygame.image.load('test.png')
screen.fill((0,0,0))
screen.blit(image, (110,110))
pygame.display.flip()