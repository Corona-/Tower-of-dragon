#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window
import system_notify
import temple_window
import city

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
NO_EXTRA, CHARACTER_VIEW, PARTY_REMOVE, CHARACTER_CHECK = 100, 101, 102, 103


SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_BLACK = (0,0,0)
COLOR_GLAY = (128,128,128)
COLOR_WHITE = (255,255,255)

MENU_MAX = 2
class Temple:

    CURE, DONATE, BACK = 0, 1, 2
    
    def __init__(self):
        #set the menu item
        self.menu = self.CURE

        #set the menu font ready
        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.temple_font = self.menu_font.render(u"トート寺院", True, COLOR_WHITE)

        self.cure_font = self.menu_font.render(u"治療する", True, COLOR_WHITE)
        self.donate_font = self.menu_font.render(u"寄付をする", True, COLOR_WHITE)
        self.back_font = self.menu_font.render(u"街に戻る", True, COLOR_WHITE)
  
        self.cursor = self.menu_font.render(u"⇒", True, COLOR_WHITE)

        self.music = 0

        #initialize extra window
        self.temple_cure_window = None #temple_window.Temple_window( Rect(60, 50, 520, 360))
        self.donate_money = None #system_notify.System_notify_window(Rect(200, 120 ,240, 240), system_notify.System_notify_window.DONATE)

    def update(self):
        if self.music == 0:
            pygame.mixer.music.load("BGM/istanbul_no_rakuen.mp3")
            pygame.mixer.music.play(-1)
            self.music = 1
        pass
    def draw(self, screen, game_self):

        #draw window for title and menu
        title_window = window.Window(Rect(20,20, 135, 50))
        title_window.draw(screen)
        
        screen.blit(self.temple_font, (35, 35))

        menu_window = window.Window(Rect(320,20,300,120))
        menu_window.draw(screen)

        #set cursor on menu items
        if self.menu == self.CURE:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,35,292,30), 0)
        elif self.menu == self.DONATE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,65,292,30), 0)
        elif self.menu == self.BACK:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,95,292,30), 0)

        #draw image font on the screen
        WINDOW_START_WIDTH = 300
        MENU_CENTER = SCREEN_RECTANGLE.width + WINDOW_START_WIDTH

        screen.blit(self.cure_font, ((MENU_CENTER-self.cure_font.get_width())/2, 40))
        screen.blit(self.donate_font, ((MENU_CENTER-self.donate_font.get_width())/2, 70))
        screen.blit(self.back_font, ((MENU_CENTER-self.back_font.get_width())/2, 100))

        #draw extra window
        if self.donate_money != None:
            self.donate_money.draw(screen, game_self.party.member)
        if self.temple_cure_window != None:
            self.temple_cure_window.draw(screen, game_self)


def temple_handler(self, event):
    """event handler of temple"""
    if self.temple.donate_money != None and self.temple.donate_money.is_visible:
        self.temple.donate_money.system_notify_window_handler(event, self,self.party.member)
        return
    elif self.temple.temple_cure_window != None and self.temple.temple_cure_window.is_visible:
        self.temple.temple_cure_window.temple_window_handler(event, self)
        return
    
    if event.type == KEYDOWN and event.key == K_UP: #moves the cursor up
        self.cursor_se.play()
        self.temple.menu -= 1
        if self.temple.menu < 0:
            self.temple.menu = MENU_MAX
    elif event.type == KEYDOWN and event.key == K_DOWN:
        self.cursor_se.play()
        self.temple.menu += 1
        if self.temple.menu > MENU_MAX:
            self.temple.menu = 0

    if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
        if self.temple.menu == Temple.CURE:
            self.temple.temple_cure_window = temple_window.Temple_window( Rect(60, 50, 520, 360))
            self.temple.temple_cure_window.is_visible = True
        elif self.temple.menu == Temple.DONATE:
            self.temple.donate_money = system_notify.System_notify_window(Rect(200, 120 ,240, 240), system_notify.System_notify_window.DONATE)
            self.temple.donate_money.is_visible = True
        elif self.temple.menu == Temple.BACK:
            self.game_state = CITY
            self.temple.menu = Temple.CURE
            self.temple.music = 0
            self.temple = None
            self.city = city.City()
        self.select_se.play()




    if event.type == KEYDOWN and (event.key ==K_x):
        self.game_state = CITY
        self.temple.menu = Temple.CURE
        self.temple.music = 0
        self.temple = None
        self.city = city.City()
        self.cancel_se.play()
        

