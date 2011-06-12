#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

import window
import city
import dungeon
import character_view
TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10

DUNGEON = 100

SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

MENU_MAX = 2

class Tower:

    GO, CONTINUE, BACK = 0,1,2
    
    def __init__(self):
        #initualize menu item
        self.menu = self.GO

        #get menu font ready
        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.tower_font = self.menu_font.render(u"天龍の塔入り口", True, COLOR_WHITE)

        self.go_font = self.menu_font.render(u"天龍の塔の探索をする", True, COLOR_WHITE)
        self.continue_font = self.menu_font.render(u"探索を再開する", True, COLOR_WHITE)
        self.back_font = self.menu_font.render(u"街に戻る", True, COLOR_WHITE)

        self.no_go_font = self.menu_font.render(u"天龍の塔の探索をする", True, COLOR_GLAY)
        self.no_continue_font = self.menu_font.render(u"探索を再開する", True, COLOR_GLAY)


        self.character_continue = None

        self.dungeon_alive_characters = []

        self.find_alive_character = False

    def update(self):
        pass
    def draw(self, screen, game_self):

        #draw the window of title and menu
        title_window = window.Window(Rect(20,20, 180, 50))
        title_window.draw(screen)
        

        menu_window = window.Window(Rect(320,20,300,120))
        menu_window.draw(screen)

        #draw the cursor on the menu item
        if self.menu == self.GO:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,35,292,30), 0)
        elif self.menu == self.CONTINUE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,65,292,30), 0)
        elif self.menu == self.BACK:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,95,292,30), 0)

        #draw the font
        WINDOW_START_WIDTH = 300
        MENU_CENTER = SCREEN_RECTANGLE.width + WINDOW_START_WIDTH

        screen.blit(self.tower_font, ( 40, 35))

        #find movable character in the dungeon
        if self.find_alive_character == False:

            self.find_alive_character = True

            for chara in game_self.dungeon_characters:
                if chara.status[4] != 1 and chara.status[5] != 1 and chara.status[6] != 1 and chara.status[7] != 1 and chara.status[8] != 1:
                    self.dungeon_alive_characters.append(chara)

        
        
        if len(game_self.party.member) == 0:
            screen.blit(self.no_go_font, ((MENU_CENTER-self.go_font.get_width())/2, 40))
        else:        
            screen.blit(self.go_font, ((MENU_CENTER-self.go_font.get_width())/2, 40))

        if len(game_self.tower.dungeon_alive_characters) == 0:
            screen.blit(self.no_continue_font, ((MENU_CENTER-self.continue_font.get_width())/2, 70))
        else:
            screen.blit(self.continue_font, ((MENU_CENTER-self.continue_font.get_width())/2, 70))

        screen.blit(self.back_font, ((MENU_CENTER-self.back_font.get_width())/2, 100))

        if self.character_continue != None:
            self.character_continue.draw(screen, game_self.tower.dungeon_alive_characters)


def tower_handler(self, event):
    """event handler of tower"""
    if self.tower.character_continue != None and self.tower.character_continue.is_visible == True:
        self.tower.character_continue.character_view_handler(self, event, self.tower.dungeon_alive_characters)
        return
    
    #moves the cursor up
    if event.type == KEYDOWN and event.key == K_UP:
        self.cursor_se.play()
        self.tower.menu -= 1
        if self.tower.menu < 0:
            self.tower.menu = MENU_MAX
    #moves the cursor down
    elif event.type == KEYDOWN and event.key == K_DOWN:
        self.cursor_se.play()
        self.tower.menu += 1
        if self.tower.menu > MENU_MAX:
            self.tower.menu = 0
    #select the item
    if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
        if self.tower.menu == Tower.GO:
            if len(self.party.member) == 0: return
            self.game_state = DUNGEON
            for character in self.party.member:
                character.coordinate = [9,19,1]
                #character.coordinate = [6,10,4]
            self.dungeon = dungeon.Dungeon(character.coordinate[2])
            self.tower = None
        elif self.tower.menu == Tower.CONTINUE:
            if len(self.tower.dungeon_alive_characters) == 0: return

            self.tower.character_continue = character_view.Character_view(Rect(80,60,480,360), character_view.Character_view.CONTINUE_DUNGEON)
            self.tower.character_continue.is_visible = True

        elif self.tower.menu == Tower.BACK:
            self.game_state = CITY
            self.tower.menu = Tower.GO
            self.tower = None
            self.city = city.City()
            self.city.menu = 6
        self.select_se.play()


    if event.type == KEYDOWN and (event.key ==K_x):
        self.game_state = CITY
        self.tower.menu = Tower.GO
        self.tower = None
        self.city = city.City()
        self.city.menu = 6
        self.cancel_se.play()

