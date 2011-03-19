#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window
import system_notify

import character_view

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
NO_EXTRA, CHARACTER_VIEW, PARTY_REMOVE, CHARACTER_CHECK = 100, 101, 102, 103


SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_BLACK = (0,0,0)
COLOR_GLAY = (128,128,128)
COLOR_WHITE = (255,255,255)

MENU_MAX = 5

class Shop:

    BUY, SELL, CURSE, DONATE, BUY_HOUSE, BACK = 0, 1, 2, 3, 4, 5
    ITEM, WEAPON, ARMOR, HAT, GLOVE, ACCESSORY = 0, 1, 2, 3, 4, 5
    
    def __init__(self):
        #set the menu item
        self.menu = self.BUY

        #set the menu fonts to be ready
        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.shop_font = self.menu_font.render(u"ベストバル商店街", True, COLOR_WHITE)

        self.buy_font = self.menu_font.render(u"アイテムを購入する", True, COLOR_WHITE)
        self.sell_font = self.menu_font.render(u"アイテムを売却する", True, COLOR_WHITE)
        self.curse_font = self.menu_font.render(u"アイテムの呪いを解く", True, COLOR_WHITE)
        self.donate_font = self.menu_font.render(u"寄付をする", True, COLOR_WHITE)
        self.buy_house_font = self.menu_font.render(u"家を購入する", True, COLOR_WHITE)
        self.back_font = self.menu_font.render(u"街に戻る", True, COLOR_WHITE)
                        
        self.weapon_font = self.menu_font.render(u"武器", True, COLOR_WHITE)
        self.armor_font = self.menu_font.render(u"鎧", True, COLOR_WHITE)
        self.hat_font = self.menu_font.render(u"兜", True, COLOR_WHITE)
        self.glove_font = self.menu_font.render(u"篭手", True, COLOR_WHITE)
        self.accessory_font = self.menu_font.render(u"アクセサリー", True, COLOR_WHITE)
        self.item_font = self.menu_font.render(u"アイテム", True, COLOR_WHITE)

        self.cursor = self.menu_font.render(u"⇒", True, COLOR_WHITE)

        #setup extra windows
        self.donate_money = system_notify.System_notify_window(Rect(200, 120 ,240, 240), self.DONATE - 2)
        self.remove_curse = system_notify.System_notify_window(Rect(150, 120, 340, 240), self.CURSE )
        self.buy_house = system_notify.Confirm_window(Rect(100, 160, 300, 120), self.BUY_HOUSE - 4)

        self.music = 0

    def update(self):
        if self.music == 0:
            pygame.mixer.music.load("BGM/hirusagari_no_waltz.mp3")
            pygame.mixer.music.play(-1)
            self.music = 1
        pass
    def draw(self, screen, game_self):

        #draw window for title and menu
        title_window = window.Window(Rect(20,20, 190, 50))
        title_window.draw(screen)
        
        screen.blit(self.shop_font, (35, 35))

        if game_self.party.house == 0:
            menu_window = window.Window(Rect(320,20,300,210))
            menu_window.draw(screen)
        else:
            menu_window = window.Window(Rect(320,20,300,180))
            menu_window.draw(screen)            

        #draws the cursor on the screen
        if self.menu == self.BUY:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,35,292,30), 0)
        elif self.menu == self.SELL:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,65,292,30), 0)
        elif self.menu == self.CURSE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,95,292,30), 0)
        elif self.menu == self.DONATE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,125,292,30), 0)
        elif self.menu == self.BUY_HOUSE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,155,292,30), 0)
        elif self.menu == self.BACK:
            if game_self.party.house > 0:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(324,155,292,30), 0)
            else:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(324,185,292,30), 0)
 
        #draws the font image onto screen
        WINDOW_START_WIDTH = 300
        MENU_CENTER = SCREEN_RECTANGLE.width + WINDOW_START_WIDTH

        house_diff = 0
        if game_self.party.house > 0:
            house_diff = -30
        else:
            screen.blit(self.buy_house_font, ((MENU_CENTER-self.buy_house_font.get_width())/2, 160))

            
        screen.blit(self.buy_font, ((MENU_CENTER-self.buy_font.get_width())/2, 40))
        screen.blit(self.sell_font, ((MENU_CENTER-self.sell_font.get_width())/2, 70))
        screen.blit(self.curse_font, ((MENU_CENTER-self.curse_font.get_width())/2, 100))
        screen.blit(self.donate_font, ((MENU_CENTER-self.donate_font.get_width())/2, 130))
        screen.blit(self.back_font, ((MENU_CENTER-self.back_font.get_width())/2, 190+house_diff))

        #draw extra window
        self.donate_money.draw(screen, game_self.party.member)
        self.remove_curse.draw(screen, game_self.party.member)
        self.buy_house.draw(screen, game_self, game_self.party.member)


def shop_handler(self,event):
    """event handler of shop"""

    if self.shop.donate_money.is_visible:
        self.shop.donate_money.system_notify_window_handler( event, self, self.party.member)
        return
    elif self.shop.remove_curse.is_visible:
        self.shop.remove_curse.system_notify_window_handler( event, self, self.party.member)
        return
    elif self.shop.buy_house.is_visible:
        self.shop.buy_house.confirm_window_handler( self, event, self.party.member)
        return
    
    #moves the cursor up
    if event.type == KEYUP and event.key == K_UP:
        self.cursor_se.play()
        self.shop.menu -= 1
        if self.shop.menu < 0:
            self.shop.menu = MENU_MAX
        if self.shop.menu == 4 and self.party.house > 0:
            self.shop.menu -= 1
    #moves the cursor down
    elif event.type == KEYUP and event.key == K_DOWN:
        self.cursor_se.play()
        self.shop.menu += 1
        if self.shop.menu > MENU_MAX:
            self.shop.menu = 0
        if self.shop.menu == 4 and self.party.house > 0:
            self.shop.menu += 1
    #select the menu items
    if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
        if self.shop.menu == Shop.BUY:
            pass
        elif self.shop.menu == Shop.SELL:
            pass
        elif self.shop.menu == Shop.CURSE:
            self.shop.remove_curse.is_visible = True
        elif self.shop.menu == Shop.DONATE:
            self.shop.donate_money.is_visible = True
        elif self.shop.menu == Shop.BUY_HOUSE:
            self.shop.buy_house.is_visible = True
        elif self.shop.menu == Shop.BACK:
            self.game_state = CITY
            self.shop.menu = Shop.BUY
            self.shop.music = 0
        self.select_se.play()

    if event.type == KEYUP and (event.key ==K_x):
        self.game_state = CITY
        self.shop.menu = Shop.BUY
        self.shop.music = 0
        self.cancel_se.play()
        
