#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

import window
TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10

DUNGEON = 100

SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

MENU_MAX = 1

class Tower:

    GO, BACK = 0,1
    
    def __init__(self):
        #initualize menu item
        self.menu = self.GO

        #get menu font ready
        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.tower_font = self.menu_font.render(u"天龍の塔入り口", True, COLOR_WHITE)

        self.go_font = self.menu_font.render(u"天龍の塔の探索をする", True, COLOR_WHITE)
        self.back_font = self.menu_font.render(u"街に戻る", True, COLOR_WHITE)

        self.cursor = self.menu_font.render(u"⇒", True, (255,255,255))


    def update(self):
        pass
    def draw(self, screen):

        #draw the window of title and menu
        title_window = window.Window(Rect(20,20, 180, 50))
        title_window.draw(screen)
        

        menu_window = window.Window(Rect(320,20,300,90))
        menu_window.draw(screen)

        #draw the cursor on the menu item
        if self.menu == self.GO:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,35,292,30), 0)
        elif self.menu == self.BACK:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,65,292,30), 0)

        #draw the font
        WINDOW_START_WIDTH = 300
        MENU_CENTER = SCREEN_RECTANGLE.width + WINDOW_START_WIDTH

        screen.blit(self.tower_font, ( 40, 35))
        
        screen.blit(self.go_font, ((MENU_CENTER-self.go_font.get_width())/2, 40))
        screen.blit(self.back_font, ((MENU_CENTER-self.back_font.get_width())/2, 70))



def tower_handler(self, event):
    """event handler of tower"""
    #moves the cursor up
    if event.type == KEYUP and event.key == K_UP:
        self.cursor_se.play()
        self.tower.menu -= 1
        if self.tower.menu < 0:
            self.tower.menu = MENU_MAX
    #moves the cursor down
    elif event.type == KEYUP and event.key == K_DOWN:
        self.cursor_se.play()
        self.tower.menu += 1
        if self.tower.menu > MENU_MAX:
            self.tower.menu = 0
    #select the item
    if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
        if self.tower.menu == Tower.GO:
            self.game_state = DUNGEON
            for character in self.party.member:
                character.coordinate = [8,19,1]
        elif self.tower.menu == Tower.BACK:
            self.game_state = CITY
            self.tower.menu = Tower.GO
        self.select_se.play()


    if event.type == KEYUP and (event.key ==K_x):
        self.game_state = CITY
        self.tower.menu = Tower.GO
        self.cancel_se.play()

