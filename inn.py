#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window

import inn_window
import system_notify

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
NO_EXTRA, CHARACTER_VIEW, PARTY_REMOVE, CHARACTER_CHECK = 100, 101, 102, 103


SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

MENU_MAX = 5


class Inn:

    REST, ITEM_OUT, ITEM_IN, SAVE, LOAD, BACK = 0, 1, 2, 3, 4, 5
    HORSE, EASY, ECONOMY, SUITE, ROYAL, DONATE= 10, 11, 12, 13, 14, 15
    
    def __init__(self):

        self.menu = self.REST

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.inn_font = self.menu_font.render(u"宿屋「ローゼンメイデン」", True, COLOR_WHITE)

        self.rest_font = self.menu_font.render(u"休息を取る", True, COLOR_WHITE)
        self.item_out_font = self.menu_font.render(u"アイテムを預ける", True, COLOR_WHITE)
        self.item_in_font = self.menu_font.render(u"アイテムを引き出す", True, COLOR_WHITE)
        self.save_font = self.menu_font.render(u"セーブする", True, COLOR_WHITE)
        self.load_font = self.menu_font.render(u"ロードする", True, COLOR_WHITE)
        self.back_font = self.menu_font.render(u"街に戻る", True, COLOR_WHITE)

        self.no_rest_font = self.menu_font.render(u"休息を取る", True, COLOR_GLAY)
        self.no_item_out_font = self.menu_font.render(u"アイテムを預ける", True, COLOR_GLAY)
        self.no_item_in_font = self.menu_font.render(u"アイテムを引き出す", True, COLOR_GLAY)



        #initialize extra window
        self.inn_window = inn_window.Inn_window(Rect(80, 100, 340, 200))
        self.save_confirm = system_notify.Confirm_window(Rect(150, 150, 200, 110), 100)
        self.load_confirm = system_notify.Confirm_window(Rect(150, 150, 200, 110), 101)

        self.item_out_window = system_notify.System_notify_window(Rect(200,120,340, 240), 6)
        self.item_in_window = system_notify.System_notify_window(Rect(200,120,340, 240), 7)

                
        self.music = 0

    def update(self):
        if self.music == 0:
            pygame.mixer.music.load("BGM/hidamari_no_hana.mp3")
            pygame.mixer.music.play(-1)
            self.music = 1
        pass
    def draw(self, screen, game_self):

        #draw window for title and menu
        title_window = window.Window(Rect(20,20, 260, 50))
        title_window.draw(screen)
        
        screen.blit(self.inn_font, (35, 35))

        menu_window = window.Window(Rect(320,20,300,210))
        menu_window.draw(screen)

        #set cursor on menu items
        if self.menu == self.REST:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,35,292,30), 0)
        elif self.menu == self.ITEM_OUT:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,65,292,30), 0)
        elif self.menu == self.ITEM_IN:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,95,292,30), 0)
        elif self.menu == self.SAVE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,125,292,30), 0)
        elif self.menu == self.LOAD:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,155,292,30), 0)
        elif self.menu == self.BACK:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,185,292,30), 0)


        #draw the image fonts onto screen
        WINDOW_START_WIDTH = 300
        MENU_CENTER = SCREEN_RECTANGLE.width + WINDOW_START_WIDTH

        if len(game_self.party.member) == 0:
            screen.blit(self.no_rest_font, ((MENU_CENTER-self.no_rest_font.get_width())/2, 40))
        else:
            screen.blit(self.rest_font, ((MENU_CENTER-self.rest_font.get_width())/2, 40))

        if len(game_self.party.member) == 0:
            screen.blit(self.no_item_out_font, ((MENU_CENTER-self.no_item_out_font.get_width())/2, 70))
        else:
            screen.blit(self.item_out_font, ((MENU_CENTER-self.item_out_font.get_width())/2, 70))

        if len(game_self.party.member) == 0:
            screen.blit(self.no_item_in_font, ((MENU_CENTER-self.no_item_in_font.get_width())/2, 100))
        else:    
            screen.blit(self.item_in_font, ((MENU_CENTER-self.item_in_font.get_width())/2, 100))

        screen.blit(self.save_font, ((MENU_CENTER-self.save_font.get_width())/2, 130))
        screen.blit(self.load_font, ((MENU_CENTER-self.load_font.get_width())/2, 160))
        screen.blit(self.back_font, ((MENU_CENTER-self.back_font.get_width())/2, 190))

        #draw extra window
        self.inn_window.draw(screen, game_self.party.member)
        self.save_confirm.draw(screen, game_self, None)
        self.load_confirm.draw(screen, game_self, None)

        self.item_out_window.draw(screen, game_self)
        self.item_in_window.draw(screen, game_self)
                

def inn_handler(self, event):
    """event handler of inn"""

    if self.inn.inn_window.is_visible:
        self.inn.inn_window.inn_window_handler(event, self, self.party.member)
        return
    elif self.inn.save_confirm.is_visible:
        self.inn.save_confirm.confirm_window_handler(self, event, None)
        return
    elif self.inn.load_confirm.is_visible:
        self.inn.load_confirm.confirm_window_handler(self, event, None)
        return
    elif self.inn.item_out_window.is_visible:
        self.inn.item_out_window.system_notify_window_handler( event, self, self.party.member)
        return
    elif self.inn.item_in_window.is_visible:
        self.inn.item_in_window.system_notify_window_handler(event, self, self.party.member)
        return

    
    #moves the cursor up
    if event.type == KEYUP and event.key == K_UP:
        self.cursor_se.play()
        self.inn.menu -= 1
        if self.inn.menu < 0:
            self.inn.menu = MENU_MAX
    #moves the cursor down
    elif event.type == KEYUP and event.key == K_DOWN:
        self.cursor_se.play
        self.inn.menu += 1
        if self.inn.menu > MENU_MAX:
            self.inn.menu = 0

    if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
        if self.inn.menu == Inn.REST:
            if len(self.party.member) > 0:
                self.inn.inn_window.is_visible = True
        elif self.inn.menu == Inn.ITEM_OUT:
            if len(self.party.member) > 0:
                self.inn.item_out_window.is_visible = True
        elif self.inn.menu == Inn.ITEM_IN:
            if len(self.party.member) > 0:
                self.inn.item_in_window.is_visible = True
        elif self.inn.menu == Inn.SAVE:
            self.inn.save_confirm.is_visible = True
        elif self.inn.menu == Inn.LOAD:
            self.inn.load_confirm.is_visible = True
        elif self.inn.menu == Inn.BACK:
            self.game_state = CITY
            self.inn.menu = Inn.REST
            self.inn.music = 0
        self.select_se.play()

    if event.type == KEYUP and (event.key ==K_x):
        self.cancel_se.play()
        self.game_state = CITY
        self.inn.menu = Inn.REST
        self.inn.music = 0
        
       

