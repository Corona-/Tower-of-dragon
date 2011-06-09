#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

import window
import enemy
import random
TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10

SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

MENU_MAX = 5

class Battle_command:

    def __init__(self, character, movement, target, magic_target, magic_level, magic_number, item_number):

        self.character = character
        self.movement = movement
        self.target = target

        #for enemy's extra attack,
        #magic_target would be same as party
        #magic_level would be name of the extra attack

        #string of target ex. "ENEMY_ONE"
        self.magic_target = magic_target
        #if level < 8 it is magician, and else priest?
        self.magic_level = magic_level
        self.magic_number = magic_number

        self.item_number = item_number

        self.speed = random.randint(1,character.agility)

        

