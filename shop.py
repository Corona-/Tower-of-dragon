#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window
import system_notify

import character_view
import shop_window
import city
import save

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
    
    def __init__(self, game_self):
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
                        
        #setup extra windows
        self.donate_money = None #system_notify.System_notify_window(Rect(200, 120 ,240, 240), system_notify.System_notify_window.DONATE)
        self.remove_curse = None #system_notify.System_notify_window(Rect(150, 120, 340, 240), system_notify.System_notify_window.CURSE )
        self.buy_house = None #system_notify.Confirm_window(Rect(100, 160, 300, 120), system_notify.Confirm_window.HOUSE)

        self.shop_window = None #shop_window.Shop_window(Rect(200, 50, 240, 380))
        self.sell_window = None #system_notify.System_notify_window(Rect(200,120,340, 240), system_notify.System_notify_window.SELL)

        self.music = 0

        #see if temp file exists (before saving)
        #if not, check if saved file exist (after saving)
        #if not, place default shop data

        if game_self.new_game == False:
            try:
                file = "Save/shop_item_temp.dat"
                fp = open(file, "rb")
            except IOError, (errno, msg):

                try:
                    file = "Save/shop_item.dat"
                    fp = open(file, "rb")
                except IOError, (errno, msg):
                    #it stores, item id, number left, ...
                    self.stock = []
                    sword_stock = [Shop_item(100,-1), Shop_item(109, 6), Shop_item(119, 1)]
                    katana_stock = [Shop_item(150, -1), Shop_item(155, 6), Shop_item(164, 1)]
                    blunt_stock = [Shop_item(200, -1), Shop_item(207, 6), Shop_item(212, 1), Shop_item(215, -1), Shop_item(218, 6), Shop_item(225,1)]
                    gun_stock = [Shop_item(250, -1), Shop_item(258, 6), Shop_item(264, 1)]
                    throw_stock = [Shop_item(300, -1), Shop_item(308, 6), Shop_item(316, 1)]
                    shield_stock = [Shop_item(350, -1), Shop_item(354, 6), Shop_item(359, 1)]
                    armor_stock = [Shop_item(400, -1), Shop_item(403, 6), Shop_item(408, 1), Shop_item(426, -1), Shop_item(428, 6)]
                    helmet_stock = [Shop_item(500, -1), Shop_item(504, 6), Shop_item(508, 1)]
                    gauntlet_stock = [Shop_item(550, -1), Shop_item(556, 6), Shop_item(563,1)]
                    accessory_stock = [Shop_item(600,-1), Shop_item(601,1), Shop_item(602,1), Shop_item(603,1), Shop_item(604,1), Shop_item(605,1), Shop_item(606,1)]
                    item_stock = [Shop_item(1,-1), Shop_item(2, 6), Shop_item(4,-1),Shop_item(5,-1), Shop_item(6,-1)]
                    
                    self.stock.append(sword_stock)
                    self.stock.append(katana_stock)
                    self.stock.append(blunt_stock)
                    self.stock.append(gun_stock)
                    self.stock.append(throw_stock)
                    self.stock.append(shield_stock)
                    self.stock.append(armor_stock)
                    self.stock.append(helmet_stock)
                    self.stock.append(gauntlet_stock)
                    self.stock.append(accessory_stock)
                    self.stock.append(item_stock)
                else:
                    save.load_shop_item(self, "Save/shop_item.dat")
            else:
                save.load_shop_item(self, "Save/shop_item_temp.dat")
                print "saved on temp file"
        #if playing in new game, don't read from shop_item.dat
        else:
            try:
                file = "Save/shop_item_temp.dat"
                fp = open(file, "rb")
            except IOError, (errno, msg):

                #it stores, item id, number left, ...
                self.stock = []
                sword_stock = [Shop_item(100,-1), Shop_item(109, 6), Shop_item(119, 1)]
                katana_stock = [Shop_item(150, -1), Shop_item(155, 6), Shop_item(164, 1)]
                blunt_stock = [Shop_item(200, -1), Shop_item(207, 6), Shop_item(212, 1), Shop_item(215, -1), Shop_item(218, 6), Shop_item(225,1)]
                gun_stock = [Shop_item(250, -1), Shop_item(258, 6), Shop_item(264, 1)]
                throw_stock = [Shop_item(300, -1), Shop_item(308, 6), Shop_item(316, 1)]
                shield_stock = [Shop_item(350, -1), Shop_item(354, 6), Shop_item(359, 1)]
                armor_stock = [Shop_item(400, -1), Shop_item(403, 6), Shop_item(408, 1), Shop_item(426, -1), Shop_item(428, 6)]
                helmet_stock = [Shop_item(500, -1), Shop_item(504, 6), Shop_item(508, 1)]
                gauntlet_stock = [Shop_item(550, -1), Shop_item(556, 6), Shop_item(563,1)]
                accessory_stock = [Shop_item(600,-1), Shop_item(601,1), Shop_item(602,1), Shop_item(603,1), Shop_item(604,1), Shop_item(605,1), Shop_item(606,1)]
                item_stock = [Shop_item(1,-1), Shop_item(2, 6), Shop_item(4,-1),Shop_item(5,-1), Shop_item(6,-1)]
                
                self.stock.append(sword_stock)
                self.stock.append(katana_stock)
                self.stock.append(blunt_stock)
                self.stock.append(gun_stock)
                self.stock.append(throw_stock)
                self.stock.append(shield_stock)
                self.stock.append(armor_stock)
                self.stock.append(helmet_stock)
                self.stock.append(gauntlet_stock)
                self.stock.append(accessory_stock)
                self.stock.append(item_stock)
            else:
                save.load_shop_item(self, "Save/shop_item_temp.dat")

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
        if self.donate_money != None:
            self.donate_money.draw(screen, game_self.party.member)
        if self.remove_curse != None:
            self.remove_curse.draw(screen, game_self.party.member)
        if self.buy_house != None:
            self.buy_house.draw(screen, game_self, game_self.party.member)
        if self.sell_window != None:
            self.sell_window.draw(screen, game_self.party.member)

        if self.shop_window != None:
            self.shop_window.draw( screen, game_self)


def shop_handler(self,event):
    """event handler of shop"""

    if self.shop.donate_money != None and self.shop.donate_money.is_visible:
        self.shop.donate_money.system_notify_window_handler( event, self, self.party.member)
        return
    elif self.shop.remove_curse != None and self.shop.remove_curse.is_visible:
        self.shop.remove_curse.system_notify_window_handler( event, self, self.party.member)
        return
    elif self.shop.buy_house != None and self.shop.buy_house.is_visible:
        self.shop.buy_house.confirm_window_handler( self, event, self.party.member)
        return
    elif self.shop.shop_window != None and self.shop.shop_window.is_visible:
        self.shop.shop_window.shop_window_handler( event, self)
        return
    elif self.shop.sell_window != None and self.shop.sell_window.is_visible:
        self.shop.sell_window.system_notify_window_handler( event, self, self.party.member)
        return
    

        
    #moves the cursor up
    if event.type == KEYDOWN and event.key == K_UP:
        self.cursor_se.play()
        self.shop.menu -= 1
        if self.shop.menu < 0:
            self.shop.menu = MENU_MAX
        if self.shop.menu == 4 and self.party.house > 0:
            self.shop.menu -= 1
    #moves the cursor down
    elif event.type == KEYDOWN and event.key == K_DOWN:
        self.cursor_se.play()
        self.shop.menu += 1
        if self.shop.menu > MENU_MAX:
            self.shop.menu = 0
        if self.shop.menu == 4 and self.party.house > 0:
            self.shop.menu += 1
    #select the menu items
    if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
        if self.shop.menu == Shop.BUY:
            self.shop.shop_window = shop_window.Shop_window(Rect(200, 50, 240, 380))
            self.shop.shop_window.is_visible = True
        elif self.shop.menu == Shop.SELL:
            self.shop.sell_window = system_notify.System_notify_window(Rect(200,120,340, 240), system_notify.System_notify_window.SELL)
            self.shop.sell_window.is_visible = True
        elif self.shop.menu == Shop.CURSE:
            self.shop.remove_curse = system_notify.System_notify_window(Rect(150, 120, 340, 240), system_notify.System_notify_window.CURSE )
            self.shop.remove_curse.is_visible = True
        elif self.shop.menu == Shop.DONATE:
            self.shop.donate_money = system_notify.System_notify_window(Rect(200, 120 ,240, 240), system_notify.System_notify_window.DONATE)
            self.shop.donate_money.is_visible = True
        elif self.shop.menu == Shop.BUY_HOUSE:
            self.shop.buy_house = system_notify.Confirm_window(Rect(100, 160, 300, 120), system_notify.Confirm_window.HOUSE)
            self.shop.buy_house.is_visible = True
        elif self.shop.menu == Shop.BACK:
            self.game_state = CITY
            self.shop.menu = Shop.BUY
            self.shop.music = 0
            #save temp shop data
            save.save_shop_item(self, "Save/shop_item_temp.dat")
            self.shop = None
            self.city = city.City()
            self.city.menu = 3
        self.select_se.play()


    if event.type == KEYDOWN and (event.key ==K_x):
        self.game_state = CITY
        self.shop.menu = Shop.BUY
        self.shop.music = 0
        for item_list in self.shop.stock:
            item_list.sort(cmp=lambda x, y: cmp(x.id, y.id), reverse=False)
        save.save_shop_item(self, "Save/shop_item_temp.dat")
        self.shop = None
        self.city = city.City()
        self.city.menu = 3
        self.cancel_se.play()

        

class Shop_item:

    def __init__(self, item_id, stock_number):

        self.id = item_id
        self.stock = stock_number
