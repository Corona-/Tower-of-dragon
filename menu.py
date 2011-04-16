#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window
import system_notify

import character_view
import item
import shop
import easygui

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
SCREEN_RECTANGLE = Rect(0,0,640,480)

DUNGEON = 100


COLOR_BLACK = (0,0,0)
COLOR_GLAY = (128,128,128)
COLOR_WHITE = (255,255,255)

class Menu:

    ITEM, MAGIC, STATUS, CHANGE, SETTINGS, BACK = 0, 1, 2, 3, 4, 5
    MENU_MAX = 5


    def __init__(self):

        self.menu = self.ITEM

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.item_font = self.menu_font.render(u"アイテムを使う", True, COLOR_WHITE)
        self.magic_font = self.menu_font.render(u"魔法を使う", True, COLOR_WHITE)
        self.status_font = self.menu_font.render(u"状態を見る", True, COLOR_WHITE)
        self.change_font = self.menu_font.render(u"隊列を変更する", True, COLOR_WHITE)
        self.setting_font = self.menu_font.render(u"パーティの名前を変更する", True, COLOR_WHITE)
        self.back_font = self.menu_font.render(u"戻る", True, COLOR_WHITE)

        self.no_item_font = self.menu_font.render(u"アイテムを使う", True, COLOR_GLAY)
        self.no_magic_font = self.menu_font.render(u"魔法を使う", True, COLOR_GLAY)
        self.no_status_font = self.menu_font.render(u"状態を見る", True, COLOR_GLAY)
        self.no_change_font = self.menu_font.render(u"隊列を変更する", True, COLOR_GLAY)

        self.item_window = system_notify.System_notify_window(Rect(200,120,340, 240), 9)
        self.magic_window = system_notify.System_notify_window(Rect(200,120,340, 240), 10)
        self.status_window = system_notify.System_notify_window(Rect(200,120,340, 240), 11)
        self.change_window = system_notify.System_notify_window(Rect(200,120,340, 240), 12)

        self.temp_party1 = []
        self.temp_party2 = []

    def update(self):
        pass

    def draw(self, screen, game_self):

        menu_title_font = self.menu_font.render( game_self.party.party_name, True, COLOR_WHITE)


        #draw window for title and menu
        title_window = window.Window(Rect(20,20, menu_title_font.get_width()+40, 50))
        title_window.draw(screen)
        
        screen.blit(menu_title_font, (35, 35))


        menu_window = window.Window(Rect(160,80,320,200))
        menu_window.draw(screen)

        #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
        #the height depends on the size of font
        pygame.draw.rect(screen, COLOR_GLAY, Rect(164,95+self.menu*30,312,30), 0)

        if len(game_self.party.member) > 0:
            screen.blit(self.item_font, (320-self.item_font.get_width()/2, 100))
            screen.blit(self.magic_font, (320-self.magic_font.get_width()/2, 130))
            screen.blit(self.status_font, (320-self.status_font.get_width()/2, 160))
            screen.blit(self.change_font, (320-self.change_font.get_width()/2, 190))
        else:
            screen.blit(self.no_item_font, (320-self.no_item_font.get_width()/2, 100))
            screen.blit(self.no_magic_font, (320-self.no_magic_font.get_width()/2, 130))
            screen.blit(self.no_status_font, (320-self.no_status_font.get_width()/2, 160))
            screen.blit(self.no_change_font, (320-self.no_change_font.get_width()/2, 190))
            
        screen.blit(self.setting_font, (320-self.setting_font.get_width()/2, 220))
        screen.blit(self.back_font, (320-self.back_font.get_width()/2, 250))
    
        self.item_window.draw(screen, game_self)
        self.magic_window.draw(screen, game_self) 
        self.status_window.draw(screen, game_self.party.member)
        self.change_window.draw(screen, self.temp_party1)
 

    def menu_handler(self, event, game_self):

        if self.item_window.is_visible == True:
            self.item_window.system_notify_window_handler(event, game_self, game_self.party.member)
            return
        elif self.magic_window.is_visible == True:
            self.magic_window.system_notify_window_handler(event, game_self, game_self.party.member)
            return
        elif self.status_window.is_visible == True:
            self.status_window.system_notify_window_handler(event, game_self, game_self.party.member)
            return
        elif self.change_window.is_visible == True:
            self.change_window.system_notify_window_handler(event, game_self, self.temp_party1)
            return
        

        #moves the cursor up
        if event.type == KEYUP and event.key == K_UP:
            game_self.cursor_se.play()
            self.menu -= 1
            if self.menu < 0:
                self.menu = self.MENU_MAX
 
        #moves the cursor up
        if event.type == KEYUP and event.key == K_DOWN:
            game_self.cursor_se.play()
            self.menu += 1
            if self.menu > self.MENU_MAX:
                self.menu = 0
    
        if event.type == KEYUP and (event.key ==K_x):
            game_self.cancel_se.play()
            self.menu = self.ITEM
            if game_self.party.member[0].coordinate != [-1,-1,-1]:
                game_self.game_state = DUNGEON
            else:
                game_self.game_state = CITY


      
        if event.type == KEYUP and (event.key ==K_z or event.key == K_SPACE or event.key == K_RETURN):
            game_self.select_se.play()
            if self.menu == self.ITEM:
                if len(game_self.party.member) > 0:
                    self.item_window.is_visible = True
            if self.menu == self.MAGIC:
                if len(game_self.party.member) > 0:
                    self.magic_window.is_visible = True
            if self.menu == self.STATUS:
                if len(game_self.party.member) > 0:
                    self.status_window.is_visible = True
            if self.menu == self.CHANGE:
                if len(game_self.party.member) > 0:
                    for character in game_self.party.member:
                        self.temp_party1.append(character)
                    self.change_window.is_visible = True
            if self.menu == self.SETTINGS:

                character_name_message = u"パーティ名を入力してください"
                message_title = u"パーティ名入力"
                fieldnames = [u"パーティ名"]
                fieldvalues = []
                
                fieldvalues = easygui.multenterbox(character_name_message, message_title, fieldnames)

                if (fieldvalues != None):
                    #if empty string, then re-enter
                    if len(fieldvalues[0]) == 0:
                        return
                    #if it includes spaces at front, then also re-enter
                    if fieldvalues[0][0] == " ":
                        return
                if fieldvalues == None: return
                game_self.party.party_name = u""+ fieldvalues[0]

            if self.menu == self.BACK:
                self.menu = self.ITEM
                if game_self.party.member == []:
                    game_self.game_state = CITY
                    return
                if game_self.party.member[0].coordinate != [-1,-1,-1]:
                    game_self.game_state = DUNGEON
                else:
                    game_self.game_state = CITY
