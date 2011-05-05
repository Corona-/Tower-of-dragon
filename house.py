#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

import window
import system_notify
import save
import city

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
NO_EXTRA, CHARACTER_VIEW, PARTY_REMOVE, CHARACTER_CHECK = 100, 101, 102, 103


SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

class House:

    REST, ITEM_OUT, ITEM_IN, SAVE, LOAD, REFORM, BACK = 0, 1, 2, 3, 4, 5, 6
    MENU_MAX = 6


    def __init__(self):

        self.menu = self.REST

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.house_font = self.menu_font.render(u"自宅", True, COLOR_WHITE)

        self.rest_font = self.menu_font.render(u"休息を取る", True, COLOR_WHITE)
        self.item_out_font = self.menu_font.render(u"アイテムを預ける", True, COLOR_WHITE)
        self.item_in_font = self.menu_font.render(u"アイテムを引き出す", True, COLOR_WHITE)
        self.save_font = self.menu_font.render(u"セーブする", True, COLOR_WHITE)
        self.load_font = self.menu_font.render(u"ロードする", True, COLOR_WHITE)
        self.reform_font = self.menu_font.render(u"家を改装する", True, COLOR_WHITE)
        self.back_font = self.menu_font.render(u"街に戻る", True, COLOR_WHITE)

        self.no_rest_font = self.menu_font.render(u"休息を取る", True, COLOR_GLAY)
        self.no_item_out_font = self.menu_font.render(u"アイテムを預ける", True, COLOR_GLAY)
        self.no_item_in_font = self.menu_font.render(u"アイテムを引き出す", True, COLOR_GLAY)
        self.no_reform_font = self.menu_font.render(u"家を改装する", True, COLOR_GLAY)


        #create extra window for rest
        self.who_rest = None #system_notify.System_notify_window(Rect(240, 80 ,240, 240), system_notify.System_notify_window.REST)
        self.house_change = None #system_notify.Confirm_window(Rect(180, 80 ,360, 110), system_notify.Confirm_window.HOUSE_CHANGE)
        self.save_confirm = None #system_notify.Confirm_window(Rect(150, 150, 200, 110), system_notify.Confirm_window.SAVE)
        self.load_confirm = None #system_notify.Confirm_window(Rect(150, 150, 200, 110), system_notify.Confirm_window.LOAD)

        self.item_out_window = None #system_notify.System_notify_window(Rect(200,120,340, 240), system_notify.System_notify_window.ITEM_OUT)
        self.item_in_window = None #system_notify.System_notify_window(Rect(200,120,340, 240), system_notify.System_notify_window.ITEM_IN)

 

    def update(self):
        pass
    def draw(self, screen, game_self):

        #draw window for title and menu
        title_window = window.Window(Rect(20,20, self.house_font.get_width()+40, 50))
        title_window.draw(screen)

        screen.blit(self.house_font, (35, 35))

        if game_self.party.house == 5:
            menu_window = window.Window(Rect(320,20,300,210))
            menu_window.draw(screen)
        else:    
            menu_window = window.Window(Rect(320,20,300,240))
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
        elif self.menu == self.REFORM:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,185,292,30), 0)
        elif self.menu == self.BACK:
            if game_self.party.house == 5:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(324,185,292,30), 0)
            else:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(324,215,292,30), 0)
        #draw the image fonts onto screen
        WINDOW_START_WIDTH = 300
        MENU_CENTER = SCREEN_RECTANGLE.width + WINDOW_START_WIDTH

        house_diff = 0
        if game_self.party.house == 5:
            house_diff = -30
        else:
            if len(game_self.party.member) == 0:
                screen.blit(self.no_reform_font, ((MENU_CENTER-self.no_reform_font.get_width())/2, 190))
            else:    
                screen.blit(self.reform_font, ((MENU_CENTER-self.reform_font.get_width())/2, 190))


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
        screen.blit(self.back_font, ((MENU_CENTER-self.back_font.get_width())/2, 220+house_diff))


        #draws extra window
        if self.who_rest != None:
            self.who_rest.draw(screen,game_self.party.member)
        if self.house_change != None:
            self.house_change.draw(screen, game_self, game_self.party.member)
        if self.save_confirm != None:
            self.save_confirm.draw(screen, game_self, None)
        if self.load_confirm != None:
            self.load_confirm.draw(screen, game_self, None)

        if self.item_out_window != None:
            self.item_out_window.draw(screen,game_self)
        if self.item_in_window != None:
            self.item_in_window.draw(screen,game_self)

    
    def house_handler(self, game_self, event):
        """event handler for house"""

        if self.who_rest != None and self.who_rest.is_visible:
            self.who_rest.system_notify_window_handler( event, game_self, game_self.party.member)
            return
        elif self.house_change != None and self.house_change.is_visible:
            self.house_change.confirm_window_handler( game_self, event, game_self.party.member)
            return
        elif self.save_confirm != None and self.save_confirm.is_visible:
            self.save_confirm.confirm_window_handler(game_self, event, None)
            return
        elif self.load_confirm != None and self.load_confirm.is_visible:
            self.load_confirm.confirm_window_handler(game_self, event, None)
            return
        elif self.item_out_window != None and self.item_out_window.is_visible:
            self.item_out_window.system_notify_window_handler(event, game_self, game_self.party.member)
            return
        elif self.item_in_window != None and self.item_in_window.is_visible:
            self.item_in_window.system_notify_window_handler(event, game_self, game_self.party.member)
            return


 

  
        #moves the cursor up
        if event.type == KEYDOWN and event.key == K_UP:
            game_self.cursor_se.play()
            self.menu -= 1
            if self.menu < 0:
                self.menu = self.MENU_MAX
            if game_self.party.house == 5 and self.menu == 5:
                self.menu -= 1
        #moves the cursor down
        elif event.type == KEYDOWN and event.key == K_DOWN:
            game_self.cursor_se.play()
            self.menu += 1
            if self.menu > self.MENU_MAX:
                self.menu = 0
            if game_self.party.house == 5 and self.menu == 5:
                self.menu += 1

        if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):

            game_self.select_se.play()

            if self.menu == self.REST:
                if len(game_self.party.member) > 0:
                    self.who_rest = system_notify.System_notify_window(Rect(240, 80 ,240, 240), system_notify.System_notify_window.REST)
                    self.who_rest.is_visible = True
            elif self.menu == self.ITEM_OUT:
                if len(game_self.party.member) > 0:
                    self.item_out_window = system_notify.System_notify_window(Rect(200,120,340, 240), system_notify.System_notify_window.ITEM_OUT)
                    self.item_out_window.is_visible = True
            elif self.menu == self.ITEM_IN:
                if len(game_self.party.member) > 0:
                    self.item_in_window = system_notify.System_notify_window(Rect(200,120,340, 240), system_notify.System_notify_window.ITEM_IN)
                    self.item_in_window.is_visible = True
            elif self.menu == self.SAVE:
                self.save_confirm = system_notify.Confirm_window(Rect(150, 150, 200, 110), system_notify.Confirm_window.SAVE)
                self.save_confirm.is_visible = True
            elif self.menu == self.LOAD:
                self.load_confirm = system_notify.Confirm_window(Rect(150, 150, 200, 110), system_notify.Confirm_window.LOAD)
                self.load_confirm.is_visible = True
            elif self.menu == self.REFORM:
                if len(game_self.party.member) > 0:
                    self.house_change = system_notify.Confirm_window(Rect(180, 80 ,360, 110), system_notify.Confirm_window.HOUSE_CHANGE)
                    self.house_change.is_visible = True
            elif self.menu == self.BACK:
                game_self.game_state = CITY
                self.menu = self.REST
                game_self.city = city.City()
                game_self.house = None





        if event.type == KEYDOWN and (event.key ==K_x):
            game_self.game_state = CITY
            self.menu = self.REST 
            game_self.city = city.City()
            game_self.house = None

            

