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
import item
TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
MENU=12

CHARACTER_MAKE = 10

SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

MENU_MAX = 1


class Party_encount_message(window.Window):

    INFO, ITEM, BUY, HEAL, BATTLE, END = 0,1,2,3,4,5

    GOOD, NEUTRAL, EVIL , WORST= 1, 0, -1, -2

    def __init__(self, rectangle, instruction, game_self):

        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.instruction = instruction
        

        self.message = None

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.buy_window = None

        self.key_press = False

        self.message_number = 0
        self.more_message = False

        self.get_item = None

        self.price = 0

        self.relation = game_self.dungeon.party_encounter_window.relation
            
        #to get item
        if self.instruction == self.ITEM:
            self.get_item = dungeon.party_encount_item( True, game_self.party.member[0].coordinate[2])

            self.price = self.get_item[1]
            self.get_item = item.Item( game_self.item_data[self.get_item[0]])
        elif self.instruction == self.BUY:
            self.get_item = dungeon.party_encount_item( False, game_self.party.member[0].coordinate[2])

            self.price = self.get_item[1]
            self.get_item = item.Item( game_self.item_data[self.get_item[0]])
            

        #if point is higher:
        #gives better info
        #at least 3 points needed on item given, then if point difference is > 3 that is point needed
        #price down on buy
        #higher probability of premitive attack, and less prob of enemy first

        if self.instruction == self.INFO:
            #select information to give
            
            self.message = [u"まだ情報はありません"]
            pass
        elif self.instruction == self.ITEM:

            self.ok = False

            if self.relation == self.GOOD:
                if game_self.dungeon.party_encounter_window.use_points < 4:
                    good_probability = int(100*game_self.dungeon.party_encounter_window.use_points/4)
                    probability = random.randint(1,100)
                    if probability < good_probability:
                        self.ok = True
                else:
                    self.ok = True
                        
            elif self.relation == self.NEUTRAL:
                if game_self.dungeon.party_encounter_window.use_points < 8:
                    good_probability = int(100*game_self.dungeon.party_encounter_window.use_points/8)
                    probability = random.randint(1,100)
                    if probability < good_probability:
                        self.ok = True
                else:
                    self.ok = True
            elif self.relation == self.EVIL:
                if game_self.dungeon.party_encounter_window.use_points < 16:
                    good_probability = int(100*game_self.dungeon.party_encounter_window.use_points/16)
                    probability = random.randint(1,100)
                    if probability < good_probability:
                        self.ok = True
                else:
                    self.ok = True

            #select receiving item
            if self.ok == True:
                self.message = [u"目の前の冒険者達は荷物からアイテムを取り出すと、", u"冒険者達に差し出してきた。", "", u"冒険者達は"+ self.get_item.name +u"を手に入れた！"]
            else:
                self.message = [u"目の前の冒険者達は静かに首を横に振った。", "",u"アイテムを貰えなかった。"]

        elif self.instruction == self.BUY:


            if self.relation == self.GOOD:
                self.price = self.price-int(self.price*game_self.dungeon.party_encounter_window.use_points*5/100)
            elif self.relation == self.NEUTRAL:
                self.price*=2
                self.price = self.price-int(self.price*game_self.dungeon.party_encounter_window.use_points*3.5/100)
            elif self.relation == self.EVIL:
                self.price*=4
                self.price = self.price-int(self.price*game_self.dungeon.party_encounter_window.use_points*1.5/100)

            

            #select buying item
            self.message = [u"目の前の冒険者達はアイテムを取り出すと", u"冒険者達に値段を告げた。", "", u"アイテムを" + str(self.price) + u"TGで購入しますか?"]

            self.buy_window = system_notify.Confirm_window( Rect(160, 150, 380, 110) , system_notify.Confirm_window.BUY_ITEM)
            self.buy_window.is_visible = True
            pass
        elif self.instruction == self.HEAL:

            self.heal_percent = 0
            self.price = 0

            if self.relation == self.GOOD:
                self.heal_percent = game_self.dungeon.party_encounter_window.use_points*25
            elif self.relation == self.NEUTRAL:
                self.heal_percent = game_self.dungeon.party_encounter_window.use_points*10                
            elif self.relation == self.EVIL:
                self.heal_percent = game_self.dungeon.party_encounter_window.use_points*5

            for chara in game_self.party.member:

                if chara.status[5] == 1 or chara.status[6] == 1 or chara.status[7] == 1:
                    continue

                
                chara.hp += random.randint(0, int(math.ceil((self.heal_percent/100.0)*chara.max_hp)))

                if chara.hp > chara.max_hp:
                    chara.hp = chara.max_hp
                
            self.message = [u"冒険者達は傷を治してもらった！"]

    
    def draw( self, screen, game_self):
        if self.is_visible == False: return        
        window.Window.draw(self, screen)


        if self.message != None:
            i=0
            for message in self.message:
                if message == "change":
                    self.message_number = i+1
                    self.more_message = True
                    break
                message_font = self.menu_font.render(message, True, COLOR_WHITE)
                screen.blit( message_font, (self.centerx - message_font.get_width()/2, self.top+15+i*20))
                i+=1

        if self.instruction == self.HEAL:
            game_self.party.draw(screen, game_self)

        if self.buy_window != None:
            self.buy_window.draw(screen, game_self, None)
            

   

    def party_encount_message_handler( self, event, game_self):

        if self.buy_window != None and self.buy_window.is_visible:
            self.buy_window.confirm_window_handler( game_self, event, None)
            return

        if event.type == KEYDOWN and (event.key == K_x or event.key ==K_z or event.key == K_SPACE or event.key == K_RETURN):

            if self.more_message == True:
                del self.message[0:self.message_number]
                self.more_message = False
                return

        
            #need to close the message
            self.is_visible = False
            self.coordinate = None
            self.message = None
            self.search_window = None
            self.press_window = None
            self.key_press = False
       
