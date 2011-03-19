#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

import window
import enemy
import random
import battle_command

import battle_window
TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10

SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

MENU_MAX = 5


class Battle:

    INIT, COMMAND, BATTLE, END = 0, 1, 2, 3

    FIGHT, DEFEND, ITEM, CURSE, MAGIC, ESCAPE = 0, 1, 2 ,3 ,4, 5

    def __init__(self, enemy_data, floor):
        #initialize font
        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.battle_start_font = self.menu_font.render(u"何者かが現れた！", True, COLOR_WHITE)

        self.select_font = self.menu_font.render(u"行動：", True, COLOR_WHITE)

        self.battle_font = self.menu_font.render(u"戦う", True, COLOR_WHITE)
        self.defend_font = self.menu_font.render(u"防御", True, COLOR_WHITE)
        self.magic_font = self.menu_font.render(u"呪いを解く", True, COLOR_WHITE)
        self.curse_font = self.menu_font.render(u"呪文", True, COLOR_WHITE)
        self.item_font = self.menu_font.render(u"アイテム", True, COLOR_WHITE)
        self.escape_font = self.menu_font.render(u"逃げる", True, COLOR_WHITE)

        self.encount_window = window.Window(Rect(210, 120, 190, 60))
        self.command_window = window.Window(Rect(360, 120, 260, 170))
        self.enemy_window = window.Window(Rect(10, 10, 620, 100))
        self.message_window = window.Window(Rect(210, 120, 190, 60))

        self.enemy_select_window = battle_window.Enemy_select_window(Rect(10, 10, 620, 100))
        
        self.first = 0

        self.state = self.INIT

        self.music = 0

        self.menu = self.FIGHT

        self.enemy_data = enemy_data

        #has all enemies in a group
        #stores until four groups and Back stores enemy in back row
        self.enemy_encount = select_enemy( self.enemy_data, floor)
        self.enemyList = self.enemy_encount[0]
        self.enemyListBack = self.enemy_encount[1]


        self.enemy_font = pygame.font.Font("ipag.ttf", 15)

        self.selected = 0

        self.party_movement = []
     
    def update(self):
        if self.state == self.COMMAND:
            if self.music == 0:
                pygame.mixer.music.load("BGM/hisyou.mp3")
                pygame.mixer.music.play(-1)
                self.music = 1

    def draw(self, game_self, screen):

        if self.state == self.INIT:
            if self.first == 0:
                encount_se = pygame.mixer.Sound("SE/thunder.wav")
                encount_se.play()
                self.first = 1
                pygame.mixer.music.stop()
                


            self.encount_window.draw(screen)
            
            screen.blit(self.battle_start_font, (230, 140))

        if self.state == self.COMMAND:
            game_self.party.draw(screen)
            self.command_window.draw(screen)
            self.enemy_window.draw(screen)

            self.enemy_select_window.draw(screen)

            if self.menu == self.FIGHT:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(370,185,100,30), 0)
            elif self.menu == self.DEFEND:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(370,215,100,30), 0)
            elif self.menu == self.ITEM:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(370,245,100,30), 0)            
            elif self.menu == self.CURSE:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(490,185,120,30), 0)            
            elif self.menu == self.MAGIC:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(490,215,120,30), 0)            
            elif self.menu == self.ESCAPE:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(490,245,120,30), 0)            

            if self.selected < len(game_self.party.member):
                character_font = self.menu_font.render( game_self.party.member[self.selected].name, True, COLOR_WHITE)     
                screen.blit(character_font, ( 440, 140))



            screen.blit(self.select_font, (380, 140))
            screen.blit(self.battle_font, (380, 190))
            screen.blit(self.defend_font, (380, 220))
            screen.blit(self.item_font, (380, 250))
            screen.blit(self.magic_font, (500, 190))
            screen.blit(self.curse_font, (500, 220))
            screen.blit(self.escape_font, (500, 250))
    
            #display the enemies names
            count = 0
            for group in self.enemyList:
                movable_count = count_movable( group)
                group_font = self.enemy_font.render( str(len(group))+group[0].name + " ("+str(movable_count)+")", True, COLOR_WHITE)
                screen.blit(group_font, (20, 20+count*20))
                count+=1
                
            count = 0
            for group in self.enemyListBack:
                movable_count = count_movable( group)
                group_font = self.enemy_font.render( str(len(group))+group[0].name + " ("+str(movable_count)+")", True, COLOR_WHITE)
                screen.blit(group_font, (340, 20+count*20))
                count+=1

    
             

    def battle_handler(self, game_self, event):
        
        if self.enemy_select_window.is_visible == True:
            self.enemy_select_window.enemy_select_window_handler( game_self, event)
            if self.selected == len(game_self.party.member):
                self.state = self.BATTLE
            return
        

        if self.state == self.INIT:
            if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN or event.key == K_x):
                self.state = self.COMMAND

            return



        elif self.state == self.COMMAND:

            if event.type == KEYUP and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):

                game_self.select_se.play()
                
                character = game_self.party.member[ self.selected ]
                
                if self.menu == self.FIGHT:
                    self.enemy_select_window.is_visible = True
                if self.menu == self.DEFEND:
                    self.party_movement.append( battle_command.Battle_command( character, self.DEFEND, 0))
                    self.selected += 1
                if self.menu == self.ITEM:
                    pass
                if self.menu == self.CURSE:
                    self.enemy_select_window.is_visible = True
                if self.menu == self.MAGIC:
                    pass
                if self.menu == self.ESCAPE:
                    probability = random.randint(1, 100)
                    if probability < 50:
                        game_self.dungeon.battle_flag = 0
                        game_self.dungeon.battle = None
                        game_self.dungeon.music = 0
                    else:
                        self.state = self.BATTLE
                        

                if self.selected == len(game_self.party.member):
                    self.state = self.BATTLE
                    return

            if event.type == KEYUP and event.key == K_UP: #moves the cursor up
                game_self.cursor_se.play()
                self.menu -= 1
                if self.menu == self.ITEM:
                    self.menu = MENU_MAX
                if self.menu < 0:
                    self.menu = self.ITEM

            elif event.type == KEYUP and event.key == K_DOWN:
                game_self.cursor_se.play()
                self.menu += 1
                if self.menu % 3 == 0:
                    self.menu -= 3

            elif event.type == KEYUP and event.key == K_LEFT:
                game_self.cursor_se.play()
                self.menu -= 3
                if self.menu < 0:
                    self.menu += MENU_MAX+1

            elif event.type == KEYUP and event.key == K_RIGHT:
                game_self.cursor_se.play()
                self.menu += 3
                if self.menu > MENU_MAX:
                    self.menu = self.menu % (MENU_MAX+1)


            if event.type == KEYUP and event.key == K_x:
                if self.selected > 0:
                    self.selected -= 1
                    count = len(self.party_movement)
                    del (self.party_movement[count-1])
                else:
                    #to end battle
                    game_self.dungeon.battle_flag = 0
                    game_self.dungeon.battle = None
                    game_self.dungeon.music = 0


        elif self.state == self.BATTLE:

            if event.type == KEYUP and event.key == K_x:
                game_self.dungeon.battle_flag = 0
                game_self.dungeon.battle = None
                game_self.dungeon.music = 0






def count_movable( enemy_group ):

    movable_count = 0
    for enemy_status in enemy_group:
        if enemy_status.status == "OK":
            movable_count += 1
    return movable_count


def select_enemy( enemy_data, floor ):

    enemy_total = []
    enemy_front = []
    enemy_back = []
    
    if floor == 1:

        enemy_id = random.randint(1,3)

        enemy_count = random.randint(1,3)

        #has enemies of a group
        enemy_group = []

        for i in range(enemy_count):
            enemy_group.append( enemy.Enemy(enemy_data[ enemy_id ] ) )

        enemy_front.append(enemy_group)

        enemy_total.append(enemy_front)
        enemy_total.append(enemy_back)


    return enemy_total
            
