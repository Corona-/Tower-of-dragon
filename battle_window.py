#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import random

import character
import character_make
import window
import battle
import item

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

        #0 is front enemy, 1 is back enemy
        self.line = 0
        
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
            pygame.draw.rect(screen, COLOR_GLAY, Rect(335, 18, 290, 20 ), 0)
        elif self.menu == self.BACK_2:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(335, 38, 290, 20 ), 0)
        elif self.menu == self.BACK_3:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(335, 58, 290, 20 ), 0)
        elif self.menu == self.BACK_4:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(335, 78, 290, 20 ), 0)

            
        
        pass



    def enemy_select_window_handler( self, game_self, event):

        #not sure it is passing it by...
        #if making change to battle, do it with game_self
        battle_in = game_self.dungeon.battle

        front_length = len(battle_in.enemyList)
        back_length = len(battle_in.enemyListBack)

        

        if event.type == KEYDOWN and event.key == K_DOWN:
            self.menu += 1
            if self.line == 1 and (self.menu > self.BACK_4 or self.menu >= 4+back_length):
                self.menu = self.BACK_1
            if self.line == 0 and (self.menu > self.FRONT_4 or self.menu >= front_length):
                self.menu = self.FRONT_1

        if event.type == KEYDOWN and event.key == K_UP:
            self.menu -= 1
            if self.line == 1 and self.menu < self.BACK_1:
                self.menu += back_length
            if self.line == 0 and self.menu < self.FRONT_1:
                self.menu += front_length

        character = game_self.party.member[ battle_in.selected ]

        if event.type == KEYDOWN and event.key == K_LEFT:
            if self.line == 1:
                self.menu -= 4
                self.line = 0

        if event.type == KEYDOWN and event.key == K_RIGHT:

            if isinstance(character.equip[0], item.Item) and character.equip[0].range > 1 and battle_in.selected < 3:
                if self.line == 0:
                    self.menu += 4
                    self.line = 1



        if event.type == KEYDOWN and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
            if battle_in.menu == battle_in.FIGHT:
                game_self.dungeon.battle.party_movement.append( battle_command.Battle_command( character, battle_in.FIGHT, self.menu, None, None, None, None))
            if battle_in.menu == battle_in.CURSE:
                game_self.dungeon.battle.party_movement.append( battle_command.Battle_command( character, battle_in.CURSE, self.menu, None, None, None, None))                
            self.is_visible = False
            game_self.dungeon.battle.selected += 1
            
            next_character = None
            if game_self.dungeon.battle.selected >= len(game_self.party.member):
                next_character = game_self.party.member[0]
            else:
                next_character = game_self.party.member[ battle_in.selected ]

            #if next character can attack the enemy set command to FIGHT, otherwise set it to DEFEND
            check = battle.character_attackable ( game_self, next_character )

            if check == True:
                game_self.dungeon.battle.menu = battle_in.FIGHT
            else:
                game_self.dungeon.battle.menu = battle_in.DEFEND
       
            self.menu = 0
            self.line = 0



        if event.type == KEYDOWN and event.key == K_x:
            self.menu = self.FRONT_1
            self.is_visible = False
            self.line = 0
        
      
        pass



