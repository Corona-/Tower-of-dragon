#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import random

import character
import character_make
import window

import string

import battle_command

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)


class Enemy_select_window(window.Window):

    FRONT_1, FRONT_2, FRONT_3, FRONT_4 = 0, 1, 2, 3
    BACK_1, BACK_2, BACK_3, BACK_4 = 4, 5, 6, 7

    def __init__(self, rectangle):

        window.Window.__init__(self, rectangle)

        self.menu = self.FRONT_1

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.menu = self.FRONT_1
        
        self.is_visible = False

    def draw(self, screen):
        """draw the window on the screen"""
        window.Window.draw(self, screen)        
        if self.is_visible == False: return


        if self.menu == self.FRONT_1:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(15, 18, 320, 20 ), 0)
        elif self.menu == self.FRONT_2:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(15, 38, 320, 20 ), 0)
        elif self.menu == self.FRONT_3:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(15, 58, 320, 20 ), 0)
        elif self.menu == self.FRONT_4:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(15, 78, 320, 20 ), 0)
        elif self.menu == self.BACK_1:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(495, 18, 320, 20 ), 0)
        elif self.menu == self.BACK_2:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(495, 38, 320, 20 ), 0)
        elif self.menu == self.BACK_3:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(495, 58, 320, 20 ), 0)
        elif self.menu == self.BACK_4:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(495, 78, 320, 20 ), 0)

            
        
        pass



    def enemy_select_window_handler( self, game_self, event):

        #not sure it is passing it by...
        #if making change to battle, do it with game_self
        battle = game_self.dungeon.battle

        front_length = len(battle.enemyList)
        back_length = len(battle.enemyListBack)

        
        character = game_self.party.member[ battle.selected ]

        if event.type == KEYUP and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
            if battle.menu == battle.FIGHT:
                game_self.dungeon.battle.party_movement.append( battle_command.Battle_command( character, battle.FIGHT, self.menu))
            if battle.menu == battle.CURSE:
                game_self.dungeon.battle.party_movement.append( battle_command.Battle_command( character, battle.CURSE, self.menu))                
            self.is_visible = False
            game_self.dungeon.battle.selected += 1


        if event.type == KEYUP and event.key == K_x:
            self.menu = self.FRONT_1
            self.is_visible = False
        
      
        pass



