#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

import window
import random

import battle
import codecs
import system_notify
import city
import menu
TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
MENU=12

CHARACTER_MAKE = 10

SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

MENU_MAX = 1



class Dungeon_message(window.Window):

    def __init__(self, rectangle):
        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.coordinate = None
        self.message = None

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        #needs "探しますか？" 
        self.search_window = None

    def update(self):
            
        pass
    def draw(self, game_self, screen):
        window.Window.draw(self, screen)        
        if self.is_visible == False: return

        if self.message != None:
            i = 0
            for message in self.message:
                message_font = self.menu_font.render( message, True, COLOR_WHITE)
                screen.blit( message_font, (self.centerx - message_font.get_width()/2, self.top+15+i*20))
                i += 1


        if self.search_window != None:
            self.search_window.draw(screen, game_self, None)
 

    def dungeon_message_handler(self, game_self, event):
        """event handler for dungeon"""

        if self.search_window != None and self.search_window.is_visible:
            self.search_window.confirm_window_handler(game_self, event, None)
            return

        if event.type == KEYDOWN and (event.key == K_x or event.key ==K_z or event.key == K_SPACE or event.key == K_RETURN):
            #need to close the message
            self.is_visible = False
            self.coordinate = None
            self.message = None
            self.search = None

    def set_coordinate(self, coordinate):

        self.coordinate = coordinate

        #set message
        if self.coordinate == [10,3,1]:
            self.message = [u"部屋の中には、龍の彫像がある。", u"彫像はブロンズで、台座はオニキスで出来ている。"]
            self.search_window = system_notify.Confirm_window(Rect(190, 200, 200, 110), system_notify.Confirm_window.SEARCH)
            self.search_window.is_visible = True
            
        if self.message != None:
            self.is_visible = True

