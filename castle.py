#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window
import character_view
import system_notify

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
NO_EXTRA, CHARACTER_VIEW, PARTY_REMOVE, CHARACTER_CHECK = 100, 101, 102, 103

SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

MENU_MAX = 5

class Castle:

    NEW, DELETE, NAME_CHANGE, JOB_CHANGE, DONATE, BACK = 0, 1, 2, 3 ,4 ,5

    
    
    def __init__(self):
        self.menu = self.NEW

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.castle_font = self.menu_font.render(u"ジークフロント城", True, COLOR_WHITE)

        self.new_font = self.menu_font.render(u"冒険者を募集する", True, COLOR_WHITE)
        self.delete_font = self.menu_font.render(u"冒険者を追放する", True, COLOR_WHITE)
        self.name_change_font = self.menu_font.render(u"名前を変える", True, COLOR_WHITE)
        self.job_change_font = self.menu_font.render(u"転職する", True, COLOR_WHITE)
        self.donate_font = self.menu_font.render(u"寄付をする", True, COLOR_WHITE)
        self.back_font = self.menu_font.render(u"街に戻る", True, COLOR_WHITE)

        self.no_delete_font = self.menu_font.render(u"冒険者を追放する", True, COLOR_GLAY)
        self.no_name_change_font = self.menu_font.render(u"名前を変える", True, COLOR_GLAY)
        self.no_job_change_font = self.menu_font.render(u"転職する", True, COLOR_GLAY)
        self.no_donate_font = self.menu_font.render(u"寄付をする", True, COLOR_GLAY)

        self.music = 0


        #extra windows initialization
        #-1 to adjust with view.
        self.character_delete = character_view.Character_view(Rect(80, 60, 480, 360), self.DELETE - 1)
        self.delete_confirm = character_view.Delete_confirm_window(Rect(200, 160, 240, 120))
        self.character_rename = character_view.Character_view(Rect(80, 60, 480, 360), self.NAME_CHANGE - 1)
        self.donate_money = system_notify.System_notify_window(Rect(200,120,240,240), self.DONATE - 3)
        
    def update(self):
        if self.music == 0:
            pygame.mixer.music.load("BGM/sakusen_kaigi.mp3")
            pygame.mixer.music.play(-1)
            self.music = 1
        pass
    def draw(self, screen, game_self, characters):

        #draw window for title and menu
        title_window = window.Window(Rect(20,20, 190, 50))
        title_window.draw(screen)
        
        screen.blit(self.castle_font, (35, 35))

        menu_window = window.Window(Rect(320,20,300,210))
        menu_window.draw(screen)

        #set cursors for menu item
        if self.menu == self.NEW:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,35,292,30), 0)
        elif self.menu == self.DELETE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,65,292,30), 0)
        elif self.menu == self.NAME_CHANGE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,95,292,30), 0)
        elif self.menu == self.JOB_CHANGE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,125,292,30), 0)
        elif self.menu == self.DONATE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,155,292,30), 0)
        elif self.menu == self.BACK:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,185,292,30), 0)


        #draw the image fonts onto screen
        WINDOW_START_WIDTH = 300
        MENU_CENTER = SCREEN_RECTANGLE.width + WINDOW_START_WIDTH

        screen.blit(self.new_font, ((MENU_CENTER-self.new_font.get_width())/2, 40))

        if len(game_self.characters) == 0:
            screen.blit(self.no_delete_font, ((MENU_CENTER-self.no_delete_font.get_width())/2, 70))
        else:
            screen.blit(self.delete_font, ((MENU_CENTER-self.delete_font.get_width())/2, 70))

        if len(game_self.characters) == 0:
            screen.blit(self.no_name_change_font, ((MENU_CENTER-self.no_name_change_font.get_width())/2, 100))
        else:
            screen.blit(self.name_change_font, ((MENU_CENTER-self.name_change_font.get_width())/2, 100))

        if len(game_self.party.member) == 0:
            screen.blit(self.no_job_change_font, ((MENU_CENTER-self.no_job_change_font.get_width())/2, 130))
        else:
            screen.blit(self.job_change_font, ((MENU_CENTER-self.job_change_font.get_width())/2, 130))

        if len(game_self.party.member) == 0:
            screen.blit(self.no_donate_font, ((MENU_CENTER-self.no_donate_font.get_width())/2, 160))
        else:
            screen.blit(self.donate_font, ((MENU_CENTER-self.donate_font.get_width())/2, 160))

        screen.blit(self.back_font, ((MENU_CENTER-self.back_font.get_width())/2, 190))


        #draw the extra window
        self.character_delete.draw(screen, characters)
        self.delete_confirm.draw(screen)
        self.character_rename.draw(screen, characters)
        self.donate_money.draw(screen, game_self.party.member)

def castle_handler(self, event):
    """event handler of castle"""

    if self.castle.delete_confirm.is_visible:
        self.castle.delete_confirm.delete_confirm_window_handler(self, event, self.characters)
        return
    elif self.castle.character_rename.is_visible:
        self.castle.character_rename.character_view_handler( self, event, self.characters)
        return
    elif self.castle.character_delete.is_visible:
        self.castle.character_delete.character_view_handler( self, event, self.characters)
        return
    elif self.castle.donate_money.is_visible:
        self.castle.donate_money.system_notify_window_handler( event, self, self.party.member)
        return
    
    
    if event.type == KEYUP and event.key == K_UP: #moves the cursor up
        self.cursor_se.play()
        self.castle.menu -= 1
        if self.castle.menu < 0:
            self.castle.menu = MENU_MAX
    elif event.type == KEYUP and event.key == K_DOWN:
        self.cursor_se.play()
        self.castle.menu += 1
        if self.castle.menu > MENU_MAX:
            self.castle.menu = 0

    if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
        if self.castle.menu == Castle.NEW:
            self.game_state = CHARACTER_MAKE
        elif self.castle.menu == Castle.DELETE:
            if len(self.characters) > 0:
                self.castle.character_delete.is_visible = True
        elif self.castle.menu == Castle.NAME_CHANGE:
            if len(self.characters) > 0:
                self.castle.character_rename.is_visible = True
        elif self.castle.menu == Castle.JOB_CHANGE:
            if len(self.party.member) > 0:
                pass
        elif self.castle.menu == Castle.DONATE:
            if len(self.party.member) > 0:
                self.castle.donate_money.is_visible = True
        elif self.castle.menu == Castle.BACK:
            self.game_state = CITY
            self.castle.menu = Castle.NEW
            self.castle.music = 0
        self.select_se.play()

    if event.type == KEYUP and (event.key ==K_x):
        self.game_state = CITY
        self.castle.menu = Castle.NEW
        self.castle.music = 0
        self.cancel_se.play()
