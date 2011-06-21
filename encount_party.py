#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

import window
import random

import battle
import codecs
import system_notify
import city
import menu
import dungeon_message
import tower
import dungeon_search
import math
import dungeon
import encount_party_message
TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
MENU=12

CHARACTER_MAKE = 10

SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

MENU_MAX = 1

class Encount_party(window.Window):

    INIT, COMMAND = 0, 1

    INFO, ITEM, BUY, HEAL, BATTLE, END = 0,1,2,3,4,5

    MENU_MAX = 5

    GOOD, NEUTRAL, EVIL , WORST= 1, 0, -1, -2

    def __init__(self, rectangle, floor, game_self):

        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx        
        
        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.encount_font = self.menu_font.render(u"何者かが現れた！", True, COLOR_WHITE)

        self.select_font = self.menu_font.render(u"何をしますか？", True, COLOR_WHITE)

        self.info_font = self.menu_font.render(u"情報を貰う", True, COLOR_WHITE)
        self.item_font = self.menu_font.render(u"アイテムを貰う", True, COLOR_WHITE)
        self.buy_font = self.menu_font.render(u"アイテムを買う", True, COLOR_WHITE)
        self.heal_font = self.menu_font.render(u"回復してもらう", True, COLOR_WHITE)
        #if alignment is neutral or evil only
        self.battle_font = self.menu_font.render(u"襲う", True, COLOR_WHITE)
        self.end_font = self.menu_font.render(u"立ち去る", True, COLOR_WHITE)

        self.trade_font = self.menu_font.render(u"交渉値", True, COLOR_WHITE)
        #calculate merchant level
        self.left_font = self.menu_font.render(u"残り:", True, COLOR_WHITE)

        self.not_enough_point_font = self.menu_font.render(u"交渉値が足りません！", True, COLOR_WHITE)


        self.merchant_point = 0

        self.menu = self.INFO

        self.state = self.INIT

        self.first = 0
        self.encount_window = window.Window(Rect(210, 120, 190, 60))

        self.use_points = 0

        self.message_window = None

        self.party_alignment = random.randint(-6,6)


        self.alignment_difference = int(math.fabs(self.party_alignment-game_self.party.alignment))

        self.relation = self.NEUTRAL

        if self.alignment_difference <= 2:
            self.relation = self.GOOD
        elif self.alignment_difference <=4:
            self.relation = self.NEUTRAL
        elif self.alignment_difference <=5:
            self.relation = self.EVIL
        else:
            self.relation = self.WORST
            
    
    def draw( self, screen, game_self):
        if self.is_visible == False: return        

        if self.state == self.INIT:
            if self.first == 0:
                encount_se = pygame.mixer.Sound("SE/thunder.wav")
                encount_se.play()
                pygame.mixer.music.stop()
                self.first = 1
                self.merchant_point = dungeon.calculate_merchant_level(game_self)


            self.encount_window.draw(screen)
            screen.blit(self.encount_font, (230, 140))
    

        elif self.state == self.COMMAND:

            window.Window.draw(self, screen)


            pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+45 + 30*self.menu,(self.right-self.left)-8,30), 0)

            if self.menu != self.END:
                points_font = self.menu_font.render( str(self.use_points), True, COLOR_WHITE)
                screen.blit(  points_font, (  self.right-60, self.top+50+self.menu*30 ))



            screen.blit( self.select_font, (self.left+20, self.top+20))
            screen.blit( self.info_font, (self.left+20, self.top+50))
            screen.blit( self.item_font, (self.left+20, self.top+80))
            screen.blit( self.buy_font, (self.left+20, self.top+110))
            screen.blit( self.heal_font, (self.left+20, self.top+140))
            screen.blit( self.battle_font, (self.left+20, self.top+170))
            screen.blit( self.end_font, (self.left+20, self.top+200))

            self.points_window = window.Window(Rect(310, 320, 200, 60))
            self.points_window.draw(screen)

            screen.blit( self.left_font, (330, 340))
            total_points = self.menu_font.render( str(self.merchant_point), True, COLOR_WHITE)
            screen.blit( total_points, (350 + self.left_font.get_width(), 340))
        

            if self.message_window != None:
                self.message_window.draw( screen, game_self)
        
        pass

    def encount_party_handler( self, event, game_self):

        if self.message_window != None and self.message_window.is_visible == True:
            self.message_window.party_encount_message_handler( event, game_self)
            return

        if self.state == self.INIT:
            if event.type == KEYDOWN and (event.key ==K_z or event.key == K_SPACE or event.key == K_RETURN):
                self.state = self.COMMAND
            return


        if event.type == KEYDOWN and event.key == K_x:
            coordinate = game_self.party.member[0].coordinate
            x = coordinate[0]
            y = coordinate[1]

            game_self.dungeon.object[y][x] = 0

            self.menu = 0
            self.is_visible = False
            self.state = 0

            self.first = 0
            self.merchant_point = 0
            self.use_points = 0

        elif event.type == KEYDOWN and event.key == K_UP:
            self.menu -= 1
            if self.menu < 0:
                self.menu = self.MENU_MAX
            
        elif event.type == KEYDOWN and event.key == K_DOWN:
            self.menu += 1
            if self.menu > self.MENU_MAX:
                self.menu = 0

        elif event.type == KEYDOWN and event.key == K_RIGHT:
            self.use_points += 1
            if self.use_points > self.merchant_point:
                self.use_points = self.merchant_point
        elif event.type == KEYDOWN and event.key == K_LEFT:
            self.use_points -= 1
            if self.use_points < 0:
                self.use_points = 0
                               

                
        elif event.type == KEYDOWN and (event.key ==K_z or event.key == K_SPACE or event.key == K_RETURN):

            if self.menu == self.INFO:
                if self.use_points > 0:
                    self.merchant_point -= self.use_points
                    self.message_window = encount_party_message.Party_encount_message( Rect(10, 10, 620, 200), self.INFO, game_self)
                    self.use_points = 0
                    self.message_window.is_visible = True

            elif self.menu == self.ITEM:
                if self.use_points > 0:
                    self.merchant_point -= self.use_points
                    self.message_window = encount_party_message.Party_encount_message( Rect(10, 10, 620, 200), self.ITEM, game_self)
                    self.use_points = 0
                    self.message_window.is_visible = True

            elif self.menu == self.BUY:
                if self.use_points > 0:
                    self.merchant_point -= self.use_points
                    self.message_window = encount_party_message.Party_encount_message( Rect(10, 10, 620, 200), self.BUY, game_self)
                    self.use_points = 0
                    self.message_window.is_visible = True

            elif self.menu == self.HEAL:
                if self.use_points > 0:
                    self.merchant_point -= self.use_points
                    self.message_window = encount_party_message.Party_encount_message( Rect(10, 10, 620, 200), self.HEAL, game_self)
                    self.use_points = 0
                    self.message_window.is_visible = True
            elif self.menu == self.BATTLE:
                if self.use_points > 0:
                    self.merchant_point -= self.use_points
                    self.use_points = 0
            elif self.menu == self.END:

                coordinate = game_self.party.member[0].coordinate
                x = coordinate[0]
                y = coordinate[1]

                game_self.dungeon.object[y][x] = 0

                self.is_visible = False
                self.menu = 0
                self.state = 0

                self.first = 0
                self.merchant_point = 0
                self.use_points = 0
                pass


