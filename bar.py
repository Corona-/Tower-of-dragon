#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window
import character_view
import system_notify
import city

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
NO_EXTRA, CHARACTER_VIEW, PARTY_REMOVE, CHARACTER_CHECK = 100, 101, 102, 103


SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

MENU_MAX = 6


class Bar:
    #menu items
    ADD, REMOVE, CHECK, SHARE, DONATE, COLLECT, BACK = 0 , 1, 2, 3, 4, 5, 6
    
    
    def __init__(self):
        #initialize menu
        self.menu = self.ADD

        #initialize font
        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.bar_font = self.menu_font.render(u"酒場「超兄貴」", True, COLOR_WHITE)

        self.add_font = self.menu_font.render(u"仲間に入れる", True, COLOR_WHITE)
        self.remove_font = self.menu_font.render(u"仲間から外す", True, COLOR_WHITE)
        self.check_font = self.menu_font.render(u"仲間を見る", True, COLOR_WHITE)
        self.share_font = self.menu_font.render(u"山分けする", True, COLOR_WHITE)
        self.donate_font = self.menu_font.render(u"寄付をする", True, COLOR_WHITE)
        self.collect_font = self.menu_font.render(u"お金を集める", True, COLOR_WHITE)
        self.back_font = self.menu_font.render(u"街に戻る", True, COLOR_WHITE)


        self.no_add_font = self.menu_font.render(u"仲間に入れる", True, COLOR_GLAY)
        self.no_remove_font = self.menu_font.render(u"仲間から外す", True, COLOR_GLAY)
        self.no_check_font = self.menu_font.render(u"仲間を見る", True, COLOR_GLAY)
        self.no_share_font = self.menu_font.render(u"山分けする", True, COLOR_GLAY)
        self.no_donate_font = self.menu_font.render(u"寄付をする", True, COLOR_GLAY)
        self.no_collect_font = self.menu_font.render(u"お金を集める", True, COLOR_GLAY)

        self.music = 0

        # +2 is adjustment between character_view
        self.party_add = None #character_view.Character_view(Rect(80, 60, 480, 360), character_view.Character_view.ADD)
        self.party_remove = None #character_view.Character_view(Rect(80, 60, 480, 360), character_view.Character_view.REMOVE)
        self.character_check = None #character_view.Character_view(Rect(80, 60, 480, 360), character_view.Character_view.CHECK)
        self.status_view = character_view.Status_view_window(Rect(20,20,600, 440))
        self.share_money = None #system_notify.System_notify_window(Rect(220,140,220, 50), system_notify.System_notify.SHARE)
        self.donate_money = None #system_notify.System_notify_window(Rect(200, 120 ,240, 240), system_notify.System_notify.DONATE)
        self.collect_money = None #system_notify.System_notify_window(Rect(200,120,240,240), system_notify.System_notify.COLLECT)
   
    def update(self):
        if self.music == 0:
            pygame.mixer.music.load("BGM/bureikou.mp3")
            pygame.mixer.music.play(-1)
            self.music = 1
        pass
    def draw(self, screen, game_self):

        #draw window for title and menu
        title_window = window.Window(Rect(20,20, 160, 50))
        title_window.draw(screen)
        
        screen.blit(self.bar_font, (35, 35))

        menu_window = window.Window(Rect(320,20,300,240))
        menu_window.draw(screen)

        #set cursors of menu items
        if self.menu == self.ADD:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,35,292,30), 0)
        elif self.menu == self.REMOVE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,65,292,30), 0)
        elif self.menu == self.CHECK:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,95,292,30), 0)
        elif self.menu == self.SHARE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,125,292,30), 0)
        elif self.menu == self.DONATE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,155,292,30), 0)
        elif self.menu == self.COLLECT:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,185,292,30), 0)
        elif self.menu == self.BACK:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,215,292,30), 0)

        #draw the image fonts onto screen
        WINDOW_START_WIDTH = 300
        MENU_CENTER = SCREEN_RECTANGLE.width + WINDOW_START_WIDTH

        if len(game_self.characters) == 0:
            screen.blit(self.no_add_font, ((MENU_CENTER-self.no_add_font.get_width())/2, 40))
        else:
            screen.blit(self.add_font, ((MENU_CENTER-self.add_font.get_width())/2, 40))

        if len(game_self.party.member) == 0:
            screen.blit(self.no_remove_font, ((MENU_CENTER-self.no_remove_font.get_width())/2, 70))            
        else:
            screen.blit(self.remove_font, ((MENU_CENTER-self.remove_font.get_width())/2, 70))

        if len(game_self.party.member) == 0:
            screen.blit(self.no_check_font, ((MENU_CENTER-self.no_check_font.get_width())/2, 100))
        else:    
            screen.blit(self.check_font, ((MENU_CENTER-self.check_font.get_width())/2, 100))

        if len(game_self.party.member) == 0:
            screen.blit(self.no_share_font, ((MENU_CENTER-self.no_share_font.get_width())/2, 130))
        else:
            screen.blit(self.share_font, ((MENU_CENTER-self.share_font.get_width())/2, 130))

        if len(game_self.party.member) == 0:
            screen.blit(self.no_donate_font, ((MENU_CENTER-self.no_donate_font.get_width())/2, 160))
        else:    
            screen.blit(self.donate_font, ((MENU_CENTER-self.donate_font.get_width())/2, 160))

        if len(game_self.party.member) == 0:
            screen.blit(self.no_collect_font, ((MENU_CENTER-self.no_collect_font.get_width())/2, 190))
        else:    
            screen.blit(self.collect_font, ((MENU_CENTER-self.collect_font.get_width())/2, 190))

            
        screen.blit(self.back_font, ((MENU_CENTER-self.back_font.get_width())/2, 220))

        #draw extra window
        if self.party_add != None:
           self.party_add.draw(screen, game_self.characters)
        if self.party_remove != None:
            self.party_remove.draw(screen, game_self.party.member)
        if self.character_check != None:
            self.character_check.draw(screen, game_self.party.member)
        if self.status_view != None:
            self.status_view.draw(screen, game_self.party.member)
        if self.share_money != None:
            self.share_money.draw(screen, game_self.party.member)
        if self.donate_money != None:
            self.donate_money.draw(screen, game_self.party.member)
        if self.collect_money != None:
            self.collect_money.draw(screen, game_self.party.member)

def bar_handler(self, event):
    """event handler of bar"""

    if self.bar.status_view != None and self.bar.status_view.is_visible:
        self.bar.status_view.status_view_window_handler(self, event, self.party.member)
        return
    elif self.bar.party_add != None and self.bar.party_add.is_visible:
        self.bar.party_add.character_view_handler(self, event, self.characters)
        return
    elif self.bar.party_remove != None and self.bar.party_remove.is_visible:
        self.bar.party_remove.character_view_handler(self, event, self.party.member)
        return
    elif self.bar.character_check != None and self.bar.character_check.is_visible:
        self.bar.character_check.character_view_handler(self, event, self.party.member)
        return
    elif self.bar.share_money != None and self.bar.share_money.is_visible:
        self.bar.share_money.system_notify_window_handler(event, self, None)
        return
    elif self.bar.donate_money != None and self.bar.donate_money.is_visible:
        self.bar.donate_money.system_notify_window_handler(event, self, self.party.member)
        return
    elif self.bar.collect_money != None and self.bar.collect_money.is_visible:
        self.bar.collect_money.system_notify_window_handler(event, self, self.party.member)
        return
       
    if event.type == KEYDOWN and event.key == K_UP: #moves the cursor up
        self.cursor_se.play()
        self.bar.menu -= 1
        if self.bar.menu < 0:
            self.bar.menu = MENU_MAX
            
    elif event.type == KEYDOWN and event.key == K_DOWN:
        self.cursor_se.play()
        self.bar.menu += 1
        if self.bar.menu > MENU_MAX:
            self.bar.menu = 0
            
    if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
        if self.bar.menu == Bar.ADD:
            if len(self.characters) > 0:
                self.bar.party_add = character_view.Character_view(Rect(80, 60, 480, 360), character_view.Character_view.ADD)
                self.bar.party_add.is_visible = True
        elif self.bar.menu == Bar.REMOVE:
            if len(self.party.member) > 0:
                self.bar.party_remove = character_view.Character_view(Rect(80, 60, 480, 360), character_view.Character_view.REMOVE)
                self.bar.party_remove.is_visible = True
        elif self.bar.menu == Bar.CHECK:
            if len(self.party.member) > 0:
                self.bar.character_check = character_view.Character_view(Rect(80, 60, 480, 360), character_view.Character_view.CHECK)
                self.bar.character_check.is_visible = True
        elif self.bar.menu == Bar.SHARE:
            if len(self.party.member) > 0:
                self.bar.share_money = system_notify.System_notify_window(Rect(220,140,220, 50), system_notify.System_notify_window.SHARE)
                self.bar.share_money.is_visible = True
        elif self.bar.menu == Bar.DONATE:
            if len(self.party.member) > 0:
                self.bar.donate_money = system_notify.System_notify_window(Rect(200, 120 ,240, 240), system_notify.System_notify_window.DONATE)
                self.bar.donate_money.is_visible = True
        elif self.bar.menu == Bar.COLLECT:
            if len(self.party.member) > 0:
                self.bar.collect_money = system_notify.System_notify_window(Rect(200,120,240,240), system_notify.System_notify_window.COLLECT)
                self.bar.collect_money.is_visible = True
        elif self.bar.menu == Bar.BACK:
            self.game_state = CITY
            self.bar.menu = Bar.ADD
            self.bar.music = 0
            self.city = city.City()
            self.bar = None
        self.select_se.play()

    if event.type == KEYDOWN and (event.key == K_x):
        self.game_state = CITY
        self.bar.menu = Bar.ADD
        self.cancel_se.play()
        self.bar.music = 0
        self.city = city.City()
        self.bar = None

