#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

import window

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
HOUSE = 11

CHARACTER_MAKE = 10
NO_EXTRA, CHARACTER_VIEW, PARTY_REMOVE, CHARACTER_CHECK = 100, 101, 102, 103


SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

MENU_MAX = 6

class City:

    #menu items
    BAR, INN, HOUSE, SHOP, TEMPLE, CASTLE, TOWER = 0, 1, 2, 3, 4, 5, 6

    def __init__(self):
        self.menu = self.BAR

        #initialize font
        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        #set menu fonts
        self.city_font = self.menu_font.render(u"城郭都市ジークフロント", True, COLOR_WHITE)

        self.bar_font = self.menu_font.render(u"酒場「超兄貴」", True, COLOR_WHITE)
        self.inn_font = self.menu_font.render(u"宿屋「ローゼンメイデン」", True, COLOR_WHITE)
        self.house_font = self.menu_font.render(u"自宅", True, COLOR_WHITE)       
        self.shop_font = self.menu_font.render(u"ベストバル商店街", True, COLOR_WHITE)    
        self.temple_font = self.menu_font.render(u"トート寺院", True, COLOR_WHITE)
        self.castle_font = self.menu_font.render(u"ジークフロント城", True, COLOR_WHITE)
        self.tower_font = self.menu_font.render(u"天龍の塔", True, COLOR_WHITE)

        self.no_shop_font = self.menu_font.render(u"ベストバル商店街", True, COLOR_GLAY)    
        self.no_temple_font = self.menu_font.render(u"トート寺院", True, COLOR_GLAY)
        self.no_tower_font = self.menu_font.render(u"天龍の塔", True, COLOR_GLAY)
        

        self.music = 0

        self.cursor_se = pygame.mixer.Sound("SE/decide.wav")
        self.select_se = pygame.mixer.Sound("SE/select.wav")
        

    def update(self):
        if self.music == 0:
            pygame.mixer.music.load("BGM/Spring walk.mp3")
            pygame.mixer.music.play(-1)
            self.music = 1
        pass
    def draw(self, screen, game_self):
        
        #draw window for title and menu
        title_window = window.Window(Rect(20,20, 250, 50))
        title_window.draw(screen)
        
        screen.blit(self.city_font, (35, 35))

        if game_self.party.house == 0:
            menu_window = window.Window(Rect(320,20,300,210))
            menu_window.draw(screen)
        else: 
            menu_window = window.Window(Rect(320,20,300,240))
            menu_window.draw(screen)

        #set cursors of menu items
        if self.menu == self.BAR:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,35,292,30), 0)
        elif self.menu == self.INN:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,65,292,30), 0)
        elif self.menu == self.HOUSE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,95,292,30), 0)            
        elif self.menu == self.SHOP:
            if game_self.party.house > 0:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(324,125,292,30), 0)
            else:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(324,95,292,30), 0)
        elif self.menu == self.TEMPLE:
            if game_self.party.house > 0:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(324,155,292,30), 0)
            else:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(324,125,292,30), 0)
        elif self.menu == self.CASTLE:
            if game_self.party.house > 0:            
                pygame.draw.rect(screen, COLOR_GLAY, Rect(324,185,292,30), 0)
            else:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(324,155,292,30), 0)
        elif self.menu == self.TOWER:
            if game_self.party.house > 0:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(324,215,292,30), 0)
            else:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(324,185,292,30), 0)


        #draw the image fonts onto screen
        WINDOW_START_WIDTH = 300
        MENU_CENTER = SCREEN_RECTANGLE.width + WINDOW_START_WIDTH

        house_diff = 0
        if game_self.party.house > 0:
            house_diff = 30
            screen.blit(self.house_font, ((MENU_CENTER-self.house_font.get_width())/2, 100))

        screen.blit(self.bar_font, ((MENU_CENTER-self.bar_font.get_width())/2, 40))
        screen.blit(self.inn_font, ((MENU_CENTER-self.inn_font.get_width())/2, 70))

        if len(game_self.party.member) == 0:
            screen.blit(self.no_shop_font, ((MENU_CENTER-self.no_shop_font.get_width())/2, 100 + house_diff))            
        else:
            screen.blit(self.shop_font, ((MENU_CENTER-self.shop_font.get_width())/2, 100 + house_diff))

        if len(game_self.party.member) == 0:
            screen.blit(self.no_temple_font, ((MENU_CENTER-self.no_temple_font.get_width())/2, 130 + house_diff))
        else:    
            screen.blit(self.temple_font, ((MENU_CENTER-self.temple_font.get_width())/2, 130 + house_diff))
            
        screen.blit(self.castle_font, ((MENU_CENTER-self.castle_font.get_width())/2, 160 + house_diff))

        if len(game_self.party.member) == 0:
            screen.blit(self.no_tower_font, ((MENU_CENTER-self.no_tower_font.get_width())/2, 190 + house_diff))
        else:    
            screen.blit(self.tower_font, ((MENU_CENTER-self.tower_font.get_width())/2, 190 + house_diff))   



#what to do on city menu
def city_handler(self, event):
    """event handler of city"""
    #moves between menu items
    
    if event.type == KEYUP and event.key == K_UP: #moves the cursor up
        self.cursor_se.play()
        self.city.menu -= 1
        if self.city.menu < 0:
            self.city.menu = MENU_MAX
        if self.city.menu == 2 and self.party.house == 0:
            self.city.menu -= 1

    elif event.type == KEYUP and event.key == K_DOWN:
        self.cursor_se.play()
        self.city.menu += 1
        if self.city.menu > MENU_MAX:
            self.city.menu = 0
        if self.city.menu == 2 and self.party.house == 0:
            self.city.menu += 1

    #move to each menu item
    if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):

        self.select_se.play()

        self.city.music = 0
        
        if self.city.menu == City.BAR:
            self.game_state = BAR
        elif self.city.menu == City.INN:
            self.game_state = INN
        elif self.city.menu == City.HOUSE:
            self.game_state = HOUSE
        elif self.city.menu == City.SHOP:
            if len(self.party.member) == 0:
                #if it cannot be selected, continue music
                self.city.music = 1
            else:
                self.game_state = SHOP
        elif self.city.menu == City.TEMPLE:
            if len(self.party.member) == 0:
                self.city.music = 1
            else:
                self.game_state = TEMPLE
        elif self.city.menu == City.CASTLE:
            self.game_state = CASTLE
        elif self.city.menu == City.TOWER:
            if len(self.party.member) == 0:
                self.city.music = 1
            else:
                self.game_state = TOWER




