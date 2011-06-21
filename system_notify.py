#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window
import rest

import save
import shop_window
import item
import character_view
import random
import temple_window
import tower
import dungeon
import string
import battle
import battle_command
import item_view

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
HOUSE = 11
MENU = 12
DUNGEON = 100

class System_notify_window(window.Window):

    SHARE, DONATE, CURSE, PAY, REST = 0, 1, 2, 3, 4
    SELL = 5
    ITEM_OUT, ITEM_IN = 6, 7
    COLLECT = 8
    USE_ITEM = 9
    USE_MAGIC = 10
    VIEW_STATUS = 11
    CHANGE_PARTY = 12
    TEMPLE_PAY = 13
    
    def __init__(self, rectangle, instruction):
        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.menu = 0

        self.instruction = instruction

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        #initialize extra windows
        self.donate_window = None #Donate_window(Rect(150, 160 ,300, 150))
        self.inn_not_enough = None #Donate_finish_window(Rect(150, 160 ,300, 50), Donate_finish_window.NOT_ENOUGH)
        self.resting_window = None #Rest_window(Rect(100, 160 ,400, 50), Rest_window.REST)
        self.house_buy_message = None #Donate_finish_window(Rect(170, 160, 300, 50), Donate_finish_window.BUY_HOUSE)                
        self.house_reform_message = None #Donate_finish_window(Rect(170, 160, 300, 50), Donate_finish_window.REFORM_HOUSE)
        self.character_sell_window = None #shop_window.Sell_window(Rect(120, 50, 400, 360))
        self.collect_message = None #Donate_finish_window(Rect(150, 160, 300, 50), Donate_finish_window.COLLECT)


        self.item_hold_window = None #Item_select_window( Rect(120, 50, 400, 360), Item_select_window.ITEM_OUT)
        self.item_receive_window = None #Item_select_window( Rect(120, 50, 400, 360), Item_select_window.ITEM_IN) 

        self.status_view = None #character_view.Status_view_window(Rect(20, 20, 600, 440))

        self.item_view = None #Item_view(Rect(120, 50, 400, 360))
        self.magic_all_view = None #Magic_all_view(Rect(80, 50, 280 ,120))

        self.temple_not_enough = None #Donate_finish_window(Rect(150,160,300,50), Donate_finish_window.TEMPLE_NOT_ENOUGH)
        self.temple_not_movable = None #Donate_finish_window(Rect(150,160,300,50), Donate_finish_window.TEMPLE_NOT_MOVABLE)
        self.temple_curing = None #temple_window.Curing_window(Rect(60, 40, 520, 400))
        self.cured = False

        #if not movable, can't use shop
        self.shop_not_movable = None
        self.inn_not_movable = None
        
    def draw(self, screen, character):
            """draw the window on the screen"""
            
            window.Window.draw(self, screen)        
            if self.is_visible == False: return

            if self.instruction == self.SHARE:
                top_font = self.menu_font.render( u"*山分けしました*", True, COLOR_WHITE)      
                screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+15))

                #check in other class if there is people in party or not.
                #character should be party members
                total_money = 0
                for chara in character:
                    total_money += chara.money
                for chara in character:
                    chara.money = (int)(total_money/len(character))
                #share the remaining
                if len(character) != 0:
                    money_left = total_money % len(character)
                    for chara in character:
                        if money_left > 0:
                            chara.money += 1
                            money_left -= 1

            if self.instruction == self.DONATE or self.instruction == self.CURSE or self.instruction == self.PAY or self.instruction == self.REST or self.instruction == self.SELL or self.instruction == self.COLLECT or self.instruction == self.USE_ITEM or self.instruction == self.USE_MAGIC or self.instruction == self.VIEW_STATUS or self.instruction == self.CHANGE_PARTY or self.instruction == self.TEMPLE_PAY:

                if self.instruction == self.DONATE:
                    top_font = self.menu_font.render( u"誰が寄付をしますか？", True, COLOR_WHITE)      
                    screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+15))
                elif self.instruction == self.CURSE:
                    top_font = self.menu_font.render( u"誰のアイテムの呪いを解きますか？", True, COLOR_WHITE)      
                    screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+15))
                elif self.instruction == self.PAY:
                    top_font = self.menu_font.render( u"誰が支払いますか？", True, COLOR_WHITE)      
                    screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+15))
                elif self.instruction == self.REST:
                    top_font = self.menu_font.render( u"誰が泊まりますか？", True, COLOR_WHITE)      
                    screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+15))
                elif self.instruction == self.SELL:
                    top_font = self.menu_font.render( u"誰が売ってくれるんだい？", True, COLOR_WHITE)      
                    screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+15))                    
                elif self.instruction == self.COLLECT:
                    top_font = self.menu_font.render( u"誰にお金を集めますか？", True, COLOR_WHITE)      
                    screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+15))                    
                elif self.instruction == self.USE_ITEM:
                    top_font = self.menu_font.render( u"誰のアイテムを見ますか？", True, COLOR_WHITE)      
                    screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+15))
                    game_self = character
                    character = game_self.party.member
                elif self.instruction == self.USE_MAGIC:
                    top_font = self.menu_font.render( u"誰の魔法を使いますか？", True, COLOR_WHITE)      
                    screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+15))
                    game_self = character
                    character = game_self.party.member
                elif self.instruction == self.VIEW_STATUS:
                    top_font = self.menu_font.render( u"誰の状態を見ますか？", True, COLOR_WHITE)      
                    screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+15))                    
                elif self.instruction == self.CHANGE_PARTY:
                    top_font = self.menu_font.render( u"順番に並べ替えてください", True, COLOR_WHITE)      
                    screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+15))                    
                elif self.instruction == self.TEMPLE_PAY:
                    top_font = self.menu_font.render( u"誰が寄付金を納めますか？", True, COLOR_WHITE)      
                    screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+15))
                    game_self = character
                    character = game_self.party.member


                #set cursors of menu items
                if len(character) > 0:
                    pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4, self.top+45+30*self.menu, self.right-self.left-8,30), 0)

                i = 0
                for chara in character:
                    name_font =  self.menu_font.render( chara.name , True, COLOR_WHITE) 
                    screen.blit(name_font, (self.centerx - name_font.get_width()/2, self.top+50+i*30))
                    i+= 1

                if len(character) > 0:
                    if self.donate_window != None:
                        self.donate_window.draw(screen, character[self.menu])
                    if self.resting_window != None:
                        self.resting_window.draw(screen, character[self.menu])
                if self.inn_not_enough != None:
                    self.inn_not_enough.draw(screen)
                if self.house_buy_message != None:
                    self.house_buy_message.draw(screen)
                if self.house_reform_message != None:
                    self.house_reform_message.draw(screen)
                if self.character_sell_window != None:
                    self.character_sell_window.draw(screen, character[self.menu])
                if self.collect_message != None:
                    self.collect_message.draw(screen)
                if self.temple_not_enough != None:
                    self.temple_not_enough.draw(screen)
                if self.temple_not_movable != None:
                    self.temple_not_movable.draw(screen)

                if self.status_view != None:
                    self.status_view.draw(screen, character)

                if self.shop_not_movable != None:
                    self.shop_not_movable.draw(screen)
                if self.inn_not_movable != None:
                    self.inn_not_movable.draw(screen)


                if self.instruction == self.TEMPLE_PAY:
                    if self.temple_curing != None:
                        self.temple_curing.draw(screen, game_self)

                if self.instruction == self.USE_ITEM:
                    if self.item_view != None:
                        self.item_view.draw(screen, game_self)

                if self.instruction == self.USE_MAGIC:
                    if self.magic_all_view != None:
                        self.magic_all_view.draw(screen, game_self)

            elif self.instruction == self.ITEM_OUT or self.instruction == self.ITEM_IN:

                game_self = character
                character = character.party.member
    
                if self.instruction == self.ITEM_OUT:
                    top_font = self.menu_font.render( u"誰のアイテムを預かればいいんだ？", True, COLOR_WHITE)      
                    screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+15))
                elif self.instruction == self.ITEM_IN:
                    top_font = self.menu_font.render( u"誰が引き出すんだ？", True, COLOR_WHITE)      
                    screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+15))


                #set cursors of menu items
                if len(character) > 0:
                    pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4, self.top+45+30*self.menu, self.right-self.left-8,30), 0)

                i = 0
                for chara in character:
                    name_font =  self.menu_font.render( chara.name , True, COLOR_WHITE) 
                    screen.blit(name_font, (self.centerx - name_font.get_width()/2, self.top+50+i*30))
                    i+= 1


                #for items it passes game_self for character
                if self.item_hold_window != None:
                    self.item_hold_window.draw(screen, game_self)
                if self.item_receive_window != None:
                    self.item_receive_window.draw(screen, game_self) 
                       



    def system_notify_window_handler(self, event, game_self, character):

        if self.donate_window != None and self.donate_window.is_visible:
            self.donate_window.donate_window_handler(event, game_self, character[self.menu])
            return
        elif self.inn_not_enough != None and self.inn_not_enough.is_visible:
            self.inn_not_enough.donate_finish_window_handler(event, game_self)
            return
        elif self.resting_window != None and self.resting_window.is_visible:
            self.resting_window.resting_window_handler(event, game_self)
            return
        elif self.house_buy_message != None and self.house_buy_message.is_visible:
            self.house_buy_message.donate_finish_window_handler(event, game_self)
            return
        elif self.house_reform_message != None and self.house_reform_message.is_visible:
            self.house_reform_message.donate_finish_window_handler(event, game_self)
            return
        elif self.character_sell_window != None and self.character_sell_window.is_visible:
            self.character_sell_window.character_sell_window_handler( event, game_self)
            return
        elif self.item_hold_window != None and self.item_hold_window.is_visible:
            self.item_hold_window.item_select_window_handler( event, game_self)
            return
        elif self.item_receive_window != None and self.item_receive_window.is_visible:
            self.item_receive_window.item_select_window_handler( event, game_self)
            return
        elif self.collect_message != None and self.collect_message.is_visible:
            self.collect_message.donate_finish_window_handler(event, game_self)
            return
        elif self.status_view != None and self.status_view.is_visible:
            self.status_view.status_view_window_handler(game_self, event, game_self.party.member)
            return
        elif self.item_view != None and self.item_view.is_visible:
            self.item_view.item_view_handler(event, game_self)
            return
        elif self.magic_all_view != None and self.magic_all_view.is_visible:
            self.magic_all_view.magic_all_view_handler(event, game_self)
            return
        elif self.temple_not_enough != None and self.temple_not_enough.is_visible:
            self.temple_not_enough.donate_finish_window_handler(event, game_self)
            return
        elif self.temple_not_movable != None and self.temple_not_movable.is_visible:
            self.temple_not_movable.donate_finish_window_handler(event, game_self)
            return
        elif self.temple_curing != None and self.temple_curing.is_visible:
            self.temple_curing.curing_window_handler(event, game_self)
            return
        elif self.shop_not_movable != None and self.shop_not_movable.is_visible:
            self.shop_not_movable.donate_finish_window_handler(event, game_self)
            return
        elif self.inn_not_movable != None and self.inn_not_movable.is_visible:
            self.inn_not_movable.donate_finish_window_handler(event, game_self)
            return
        
        if self.instruction == self.SHARE:        
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
                self.is_visible = False






        elif self.instruction == self.DONATE or self.instruction == self.CURSE or self.instruction == self.PAY or self.instruction == self.REST or self.instruction == self.SELL or self.instruction == self.ITEM_OUT or self.instruction == self.ITEM_IN or self.instruction == self.COLLECT or self.instruction == self.USE_ITEM or self.instruction == self.USE_MAGIC or self.instruction == self.VIEW_STATUS or self.instruction == self.CHANGE_PARTY or self.instruction == self.TEMPLE_PAY:
            
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
                #if game_self.party.member[self.menu].status != "OK" and self.instruction != self.VIEW_STATUS:
                #    return

                
                if self.instruction == self.DONATE:
                    if len(character) > 0:
                        self.donate_window = Donate_window(Rect(150, 160 ,300, 150))
                        self.donate_window.is_visible = True
                elif self.instruction == self.CURSE:
                    pass
                elif self.instruction == self.PAY:

                    #reform the house
                    if game_self.game_state == HOUSE:
                        payment = 0
                        if game_self.party.house == 1:
                            payment = 50000
                        if game_self.party.house == 2:
                            payment = 100000
                        if game_self.party.house == 3:
                            payment = 200000
                        if game_self.party.house == 4:
                            payment = 500000
                        if game_self.party.member[self.menu].money > payment:
                            game_self.party.house += 1
                            game_self.party.member[self.menu].money -= payment
                            self.house_reform_message = Donate_finish_window(Rect(170, 160, 300, 50), Donate_finish_window.REFORM_HOUSE)
                            game_self.house.house_change.who_pay_window.house_reform_message.is_visible = True
                        else:
                            self.inn_not_enough = Donate_finish_window(Rect(150, 160 ,300, 50), Donate_finish_window.NOT_ENOUGH)
                            self.inn_not_enough.is_visible = True
                        return
                    # buy a house with 10000                    
                    if game_self.party.member[self.menu].money > 10000:
                        game_self.party.house = 1
                        game_self.party.member[self.menu].money -= 10000
                        self.house_buy_message = Donate_finish_window(Rect(170, 160, 300, 50), Donate_finish_window.BUY_HOUSE)                

                        game_self.shop.buy_house.who_pay_window.house_buy_message.is_visible = True
                    else:
                        self.inn_not_enough = Donate_finish_window(Rect(150, 160 ,300, 50), Donate_finish_window.NOT_ENOUGH)
                        self.inn_not_enough.is_visible = True
                elif self.instruction == self.REST and len(game_self.party.member) > 0:
                    #get the item chosen to rest for and if money is not enough, open inn_not_enough window
                    #else check exp points and rests

                    #if character is not movable cannot rest
                    if game_self.party.member[self.menu].status != [0,0,0,0,0,0,0,0,0]:
                        self.inn_not_movable = Donate_finish_window(Rect(150,160,300,50), Donate_finish_window.TEMPLE_NOT_MOVABLE)
                        self.inn_not_movable.is_visible = True
                        return


                    if game_self.game_state == INN:
                        rest.rest(self, game_self, game_self.inn.inn_window.menu, 1)
                    elif game_self.game_state == HOUSE:
                        rest.rest(self, game_self, game_self.party.house, 0)                         
                        
                    if self.inn_not_enough != None and self.inn_not_enough.is_visible:
                        return

                    #check exp and lv up
                    rest.calc_exp_needed(self, game_self.party.member[self.menu])

                    change = [0,0,0,0,0,0,0,0]
                    #level up if next is negative or 0
                    if game_self.party.member[self.menu].next <= 0:
                        if game_self.game_state == INN:
                            rest.level_up(self, game_self.party.member[self.menu], game_self.inn.inn_window.menu, change)
                        elif game_self.game_state == HOUSE:
                            rest.level_up(self, game_self.party.member[self.menu], game_self.party.house, change)

                        self.resting_window = Rest_window(Rect(100, 160 ,400, 50), Rest_window.REST)
                            
                        self.resting_window.get_change_status_values(change)
                        #show message of sleeping...
                        self.resting_window.lv_up_window = level_up_window(Rect(80, 140, 440, 300), 0)

                        self.resting_window.is_visible = True
                        #show message for lv up                        
                    else:
                        self.resting_window = Rest_window(Rect(100, 160 ,400, 50), Rest_window.REST)

                        self.resting_window.get_change_status_values(change)
                        #window to show next
                        #show message of sleeping...

                        #change the lv up to not lv up
                        self.resting_window.lv_up_window = level_up_window(Rect(80, 140, 440, 300), 1)

                        self.resting_window.is_visible = True
                        pass
                    #print change

                elif self.instruction == self.SELL:
                    if game_self.party.member[self.menu].status != [0,0,0,0,0,0,0,0,0]:
                        self.shop_not_movable = Donate_finish_window(Rect(150,160,300,50), Donate_finish_window.TEMPLE_NOT_MOVABLE)
                        self.shop_not_movable.is_visible = True
                    else:
                        self.character_sell_window = shop_window.Sell_window(Rect(120, 50, 400, 360))
                        self.character_sell_window.is_visible = True
                elif self.instruction == self.ITEM_OUT:
                    self.item_hold_window = Item_select_window( Rect(120, 50, 400, 360), Item_select_window.ITEM_OUT)
                    self.item_hold_window.is_visible = True
                elif self.instruction == self.ITEM_IN:
                    self.item_receive_window = Item_select_window( Rect(120, 50, 400, 360), Item_select_window.ITEM_IN) 
                    self.item_receive_window.is_visible = True
                elif self.instruction == self.COLLECT:  
                    self.collect_message = Donate_finish_window(Rect(150, 160, 300, 50), Donate_finish_window.COLLECT)
                    self.collect_message.is_visible = True
                    total_money = 0
                    for character in game_self.party.member:
                        total_money += character.money
                        character.money = 0
                    game_self.party.member[self.menu].money = total_money
                elif self.instruction == self.USE_ITEM:
                    self.item_view = Item_view(Rect(70, 50, 450, 360))
                    self.item_view.is_visible = True
                elif self.instruction == self.USE_MAGIC:
                    if game_self.party.member[self.menu].status[3] != 1 and game_self.party.member[self.menu].status[4] != 1 and game_self.party.member[self.menu].status[5] != 1 and game_self.party.member[self.menu].status[6] != 1 and game_self.party.member[self.menu].status[7] != 1 and game_self.party.member[self.menu].status[8] != 1:
                        self.magic_all_view = Magic_all_view(Rect(80, 50, 280 ,120))
                        self.magic_all_view.is_visible = True
                elif self.instruction == self.VIEW_STATUS:
                    self.status_view = character_view.Status_view_window(Rect(20, 20, 600, 440))
                    self.status_view.menu = self.menu
                    self.status_view.is_visible = True          
                elif self.instruction == self.CHANGE_PARTY:
                    game_self.menu.temp_party2.append(game_self.menu.temp_party1[self.menu])
                    del game_self.menu.temp_party1[self.menu]
                    if self.menu+1 > len(game_self.menu.temp_party1):
                        self.menu -= 1
                    if self.menu < 0:
                        game_self.party.member = []
                        for character in game_self.menu.temp_party2:
                            game_self.party.member.append(character)
                        self.is_visible = False
                        self.menu = 0
                        game_self.menu.temp_party1 = []
                        game_self.menu.temp_party2 = []

                elif self.instruction == self.TEMPLE_PAY:
                    if game_self.party.member[self.menu].status == [0,0,0,0,0,0,0,0,0]:
                        temple_cure = game_self.temple.temple_cure_window
                        cure_character = temple_cure.to_cure[temple_cure.menu+temple_cure.page*10]
                        cost = 0
                        if cure_character.status[4] == 1:
                            cost = 100*cure_character.level
                        elif cure_character.status[5] == 1:
                            cost = 200*cure_character.level
                        elif cure_character.status[6] == 1:
                            cost = 250*cure_character.level
                        elif cure_character.status[7] == 1:
                            cost = 500*cure_character.level

                        
                        if game_self.party.member[self.menu].money > cost:
                            game_self.party.member[self.menu].money-=cost

                            self.cured = False
                            if cure_character.status[4] == 1 or cure_character.status[5] == 1:
                                self.cured = True
                            else:
                                probability = random.randint(1,100)
                                if probability <= 90:
                                    self.cured = True
                                else:
                                    self.cured = False

                            self.temple_curing = temple_window.Curing_window(Rect(60, 40, 520, 400))
                            self.temple_curing.is_visible = True
                        else:
                            self.temple_not_enough = Donate_finish_window(Rect(150,160,300,50), Donate_finish_window.TEMPLE_NOT_ENOUGH)
                            self.temple_not_enough.is_visible = True
                            pass
                    else:
                        self.temple_not_movable = Donate_finish_window(Rect(150,160,300,50), Donate_finish_window.TEMPLE_NOT_MOVABLE)
                        self.temple_not_movable.is_visible = True
                        pass
                    pass
       

            if event.type == KEYDOWN and event.key == K_x:
                self.menu = 0
                self.is_visible = False
                if game_self.menu != None:
                    game_self.menu.temp_party1 = []
                    game_self.menu.temp_party2 = []

            if event.type == KEYDOWN and event.key == K_UP:
                self.menu -= 1
                if self.menu < 0:
                    self.menu = len(character)-1

            if event.type == KEYDOWN and event.key == K_DOWN:
                self.menu += 1
                if len(character) < self.menu+1:
                    self.menu = 0

         
 
class Donate_window(window.Window):

        
    def __init__(self, rectangle):
        window.Window.__init__(self, rectangle)
        self.is_visible = False

        #menu is what place it want to change
        self.menu = 0

        self.hundred_million = 0
        self.ten_million = 0
        self.million = 0
        self.hun_thousand = 0
        self.ten_thousand = 0
        self.thousand = 0
        self.hundred = 0
        self.ten = 0
        self.one = 0
 

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        #extra finishing windows
        self.no_finish = Donate_finish_window(Rect( 180, 200, 220, 50), 0)
        self.donate_finish = Donate_finish_window(Rect( 200, 200, 200, 50), 1)


    #input character should be actual charcter
    def draw(self, screen, character):
            """draw the window on the screen"""
            window.Window.draw(self, screen)        
            if self.is_visible == False: return

            top_font = self.menu_font.render( u"いくら寄付しますか？", True, COLOR_WHITE)      
            screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+15))

            possible_font = self.menu_font.render( u"所持金：" + str(character.money), True, COLOR_WHITE)      
            screen.blit(possible_font, (self.centerx - possible_font.get_width()/2, self.top+45))            

            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.right - 80 - self.menu*20, self.top+75, 10 , 20), 0)

            donate_font = self.menu_font.render( str(self.hundred_million) + str(self.ten_million) +str(self.million) +str(self.hun_thousand) +str(self.ten_thousand) +str(self.thousand) +str(self.hundred) +str(self.ten) +str(self.one), True, COLOR_WHITE)
            screen.blit(donate_font, (self.centerx - donate_font.get_width()/2, self.top+75))

            #draw extra windows
            self.no_finish.draw(screen)
            self.donate_finish.draw(screen)

    def donate_window_handler(self, event, game_self, character):

        if self.no_finish.is_visible:
            self.no_finish.donate_finish_window_handler(event, game_self)
            return
        elif self.donate_finish.is_visible:
            self.donate_finish.donate_finish_window_handler(event, game_self)
            return
 

        if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
            donate_money = self.hundred_million*100000000 + self.ten_million*10000000 + self.million*1000000 + self.hun_thousand*100000+self.ten_thousand*10000+self.thousand*1000+self.hundred*100+self.ten*10+self.one

            self.menu = 0
            self.hundred_million = 0
            self.ten_million = 0
            self.million = 0
            self.hun_thousand = 0
            self.ten_thousand = 0
            self.thousand = 0
            self.hundred = 0
            self.ten = 0
            self.one = 0
       
            if character.money < donate_money:
                self.no_finish.is_visible = True                
            else:
                self.donate_finish.is_visible = True
                character.money -= donate_money
                if game_self.game_state == BAR:
                    game_self.party.bar_donate += donate_money
                elif game_self.game_state == SHOP:
                    game_self.party.shop_donate += donate_money
                elif game_self.game_state == CASTLE:
                    game_self.party.castle_donate += donate_money
                elif game_self.game_state == TEMPLE:
                    game_self.party.temple_donate += donate_money
                    

            
        if event.type == KEYDOWN and event.key == K_x:
            self.menu = 0

            self.hundred_million = 0
            self.ten_million = 0
            self.million = 0
            self.hun_thousand = 0
            self.ten_thousand = 0
            self.thousand = 0
            self.hundred = 0
            self.ten = 0
            self.one = 0

            self.is_visible = False

            
        elif event.type == KEYDOWN and event.key == K_LEFT:
            self.menu += 1
            if self.menu > 8:
                self.menu = 0
            
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            self.menu -= 1
            if self.menu < 0:
                self.menu = 8

        #maybe want to clean up this... 
        elif event.type == KEYDOWN and event.key == K_UP:
            if self.menu == 0:
                self.one += 1
                if self.one > 9:
                    self.one = 0
            if self.menu == 1:
                self.ten += 1
                if self.ten > 9:
                    self.ten = 0
            if self.menu == 2:
                self.hundred += 1
                if self.hundred > 9:
                    self.hundred = 0
            if self.menu == 3:
                self.thousand += 1
                if self.thousand > 9:
                    self.thousand = 0
            if self.menu == 4:
                self.ten_thousand += 1
                if self.ten_thousand > 9:
                    self.ten_thousand = 0
            if self.menu == 5:
                self.hun_thousand += 1
                if self.hun_thousand > 9:
                    self.hun_thousand = 0
            if self.menu == 6:
                self.million += 1
                if self.million > 9:
                    self.million = 0
            if self.menu == 7:
                self.ten_million += 1
                if self.ten_million > 9:
                    self.ten_million = 0
            if self.menu == 8:
                self.hundred_million += 1
                if self.hundred_million > 9:
                    self.hundred_million = 0

        elif event.type == KEYDOWN and event.key == K_DOWN:
            if self.menu == 0:
                self.one -= 1
                if self.one < 0:
                    self.one = 9
            if self.menu == 1:
                self.ten -= 1
                if self.ten < 0:
                    self.ten = 9
            if self.menu == 2:
                self.hundred -= 1
                if self.hundred < 0:
                    self.hundred = 9
            if self.menu == 3:
                self.thousand -= 1
                if self.thousand < 0:
                    self.thousand = 9
            if self.menu == 4:
                self.ten_thousand -= 1
                if self.ten_thousand < 0:
                    self.ten_thousand = 9
            if self.menu == 5:
                self.hun_thousand -= 1
                if self.hun_thousand < 0:
                    self.hun_thousand = 9
            if self.menu == 6:
                self.million -= 1
                if self.million < 0:
                    self.million = 9
            if self.menu == 7:
                self.ten_million -= 1
                if self.ten_million < 0:
                    self.ten_million = 9
            if self.menu == 8:
                self.hundred_million -= 1
                if self.hundred_million < 0:
                    self.hundred_million = 9




#use as finish window?
class Donate_finish_window(window.Window):

    NOT_ENOUGH, FINISH = 0, 1
    BUY_HOUSE, REFORM_HOUSE = 2, 3
    BUY_ITEM = 4
    TOO_MUCH_ITEM = 5
    SOLD_ITEM = 6
    COLLECT = 7
    TEMPLE_NOT_ENOUGH = 8
    TEMPLE_NOT_MOVABLE = 9
    DUNGEON_LOCKED = 10
    KEY_UNLOCK = 11
    NO_ONE = 12
    
    def __init__(self, rectangle, instruction):
        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.instruction = instruction

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

    #input character should be actual charcter
    def draw(self, screen):
            """draw the window on the screen"""
            window.Window.draw(self, screen)        
            if self.is_visible == False: return

            if self.instruction == self.NOT_ENOUGH:
                not_enough_font = self.menu_font.render( u"*お金が足りません*", True, COLOR_WHITE)      
                screen.blit(not_enough_font, (self.centerx - not_enough_font.get_width()/2, self.top+15))

            elif self.instruction == self.FINISH:
                enough_font = self.menu_font.render( u"*寄付しました*", True, COLOR_WHITE)      
                screen.blit(enough_font, (self.centerx - enough_font.get_width()/2, self.top+15))

            elif self.instruction == self.BUY_HOUSE:
                enough_font = self.menu_font.render( u"*家を購入しました*", True, COLOR_WHITE)      
                screen.blit(enough_font, (self.centerx - enough_font.get_width()/2, self.top+15))

            elif self.instruction == self.REFORM_HOUSE:
                enough_font = self.menu_font.render( u"*家を改装しました*", True, COLOR_WHITE)      
                screen.blit(enough_font, (self.centerx - enough_font.get_width()/2, self.top+15))
            elif self.instruction == self.BUY_ITEM:
                enough_font = self.menu_font.render( u"*きっとお気に召しますよ*", True, COLOR_WHITE)      
                screen.blit(enough_font, (self.centerx - enough_font.get_width()/2, self.top+15))
            elif self.instruction == self.TOO_MUCH_ITEM:
                enough_font = self.menu_font.render( u"*持ち物が一杯で持てません*", True, COLOR_WHITE)      
                screen.blit(enough_font, (self.centerx - enough_font.get_width()/2, self.top+15))
            elif self.instruction == self.SOLD_ITEM:
                enough_font = self.menu_font.render( u"*ありがとうよ*", True, COLOR_WHITE)      
                screen.blit(enough_font, (self.centerx - enough_font.get_width()/2, self.top+15))
            elif self.instruction == self.COLLECT:
                enough_font = self.menu_font.render( u"*お金を集めました*", True, COLOR_WHITE)      
                screen.blit(enough_font, (self.centerx - enough_font.get_width()/2, self.top+15))
            elif self.instruction == self.TEMPLE_NOT_ENOUGH:
                enough_font = self.menu_font.render( u"*けちな背教者め！*", True, COLOR_WHITE)      
                screen.blit(enough_font, (self.centerx - enough_font.get_width()/2, self.top+15))
            elif self.instruction == self.TEMPLE_NOT_MOVABLE:
                enough_font = self.menu_font.render( u"*行動不能です*", True, COLOR_WHITE)      
                screen.blit(enough_font, (self.centerx - enough_font.get_width()/2, self.top+15))
            elif self.instruction == self.DUNGEON_LOCKED:
                enough_font = self.menu_font.render( u"*鍵が掛かっている*", True, COLOR_WHITE)
                screen.blit(enough_font, (self.centerx - enough_font.get_width()/2, self.top+15))
            elif self.instruction == self.KEY_UNLOCK:
                enough_font = self.menu_font.render( u"鍵が開いた!", True, COLOR_WHITE)
                screen.blit(enough_font, (self.centerx - enough_font.get_width()/2, self.top+15))
            elif self.instruction == self.NO_ONE:
                enough_font = self.menu_font.render( u"誰も見つかりませんでした", True, COLOR_WHITE)
                screen.blit(enough_font, (self.centerx - enough_font.get_width()/2, self.top+15))
                       


    def donate_finish_window_handler(self, event, game_self):
        if self.instruction == self.NOT_ENOUGH:          
            if event.type == KEYDOWN and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False
                #it is only used when buying a house and not enough money
                #it doesn't matter if it is not since it is initialized and should be false
                if game_self.shop != None:
                    if game_self.shop.buy_house != None:
                        game_self.shop.buy_house.who_pay_window.is_visible = False
                        game_self.shop.buy_house.who_pay_window.menu = 0
                        game_self.shop.buy_house.is_visible = False

         
        elif self.instruction == self.FINISH:
            if event.type == KEYDOWN and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False

        elif self.instruction == self.BUY_HOUSE:
            if event.type == KEYDOWN and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False
                if game_self.shop != None:
                    if game_self.shop.buy_house != None:
                        game_self.shop.buy_house.who_pay_window.is_visible = False
                        game_self.shop.buy_house.is_visible = False
                    #move the cursor to correct spot
                    game_self.shop.menu += 1

        elif self.instruction == self.REFORM_HOUSE:
            if event.type == KEYDOWN and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False
                if game_self.house.house_change.who_pay_window != None:
                    game_self.house.house_change.who_pay_window.is_visible = False
                if game_self.house.house_change != None:
                    game_self.house.house_change.is_visible = False
                #move the cursor to correct spot
                if game_self.party.house == 5:
                    game_self.house.menu += 1
                    
        elif self.instruction == self.TOO_MUCH_ITEM or self.instruction == self.SOLD_ITEM or self.instruction == self.COLLECT:
            if event.type == KEYDOWN and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False

        elif self.instruction == self.BUY_ITEM:
            if event.type == KEYDOWN and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False
                if game_self.shop.shop_window.buy_window.character_select.no_more == 1:
                    game_self.shop.shop_window.buy_window.character_select.is_visible = False
        elif self.instruction == self.TEMPLE_NOT_ENOUGH or self.instruction == self.TEMPLE_NOT_MOVABLE or self.instruction == self.DUNGEON_LOCKED or self.instruction == self.KEY_UNLOCK :
            if event.type == KEYDOWN and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False
            
        elif self.instruction == self.NO_ONE :
            if event.type == KEYDOWN and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False
                game_self.dungeon.dungeon_search_window.search_window = None

 
class Rest_window(window.Window):

    REST = 0
    LV_UP,LV_STAY = 0, 1
    
    def __init__(self, rectangle, instruction):
        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.instruction = instruction

        self.change = []

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        #draw extra window for lv up
        self.lv_up_window = level_up_window(Rect(80, 140, 440, 300), 0)

    #input character should be actual charcter
    def draw(self, screen, character):
            """draw the window on the screen"""
            window.Window.draw(self, screen)        
            if self.is_visible == False: return

            if self.instruction == self.REST:
                enough_font = self.menu_font.render( u"*休んでいます*", True, COLOR_WHITE)      
                screen.blit(enough_font, (self.centerx - enough_font.get_width()/2, self.top+15))


            self.lv_up_window.draw(screen, character, self.change)


    def resting_window_handler(self, event, game_self):

        if self.lv_up_window.is_visible:
            self.lv_up_window.level_up_window_handler(event, game_self)

        if self.instruction == self.REST:
            if event.type == KEYDOWN and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.lv_up_window.is_visible = True


    def get_change_status_values(self, change):
        self.change = change



class Confirm_window(window.Window):

    HOUSE, PAY  = 0, 1
    HOUSE_CHANGE = 10
    SAVE, LOAD = 100, 101
    JOB_CHANGE = 20
    DOWNSTAIRS = 30
    UPSTAIRS= 31

    SEARCH = 32
    PRESS = 33

    BUY_ITEM = 35


    YES, NO = 0, 1
    MENU_MAX = 1

    
    def __init__(self, rectangle, instruction):
        window.Window.__init__(self, rectangle)
        self.is_visible = False
        self.menu = self.YES

        self.instruction = instruction

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.who_pay_window = System_notify_window(Rect(150, 120, 340, 240), self.PAY +2)

    def draw(self, screen, game_self, characters):
         """draw the window on the screen"""
         window.Window.draw(self, screen)        
         if self.is_visible == False: return

         if self.instruction == self.HOUSE:
             confirm_font = self.menu_font.render( u"家を買いますか？（１万TG）", True, COLOR_WHITE)
         elif self.instruction == self.HOUSE_CHANGE:
             if game_self.party.house == 1:
                 confirm_font = self.menu_font.render( u"家を改装しますか？（5万TG）", True, COLOR_WHITE)
             elif game_self.party.house == 2:
                 confirm_font = self.menu_font.render( u"家を改装しますか？（10万TG）", True, COLOR_WHITE)
             elif game_self.party.house == 3:
                 confirm_font = self.menu_font.render( u"家を改装しますか？（20万TG）", True, COLOR_WHITE)
             else:
                 confirm_font = self.menu_font.render( u"家を改装しますか？（50万TG）", True, COLOR_WHITE)

         elif self.instruction == self.SAVE:
             confirm_font = self.menu_font.render( u"セーブしますか？", True, COLOR_WHITE)            
         elif self.instruction == self.LOAD:
             confirm_font = self.menu_font.render( u"ロードしますか？", True, COLOR_WHITE)            
         elif self.instruction == self.JOB_CHANGE:
             character = game_self.castle.change_job_window.possible_characters[game_self.castle.change_job_window.menu]
             confirm_font = self.menu_font.render( character.name + u"は" + u"転職します", True, COLOR_WHITE)
         elif self.instruction == self.DOWNSTAIRS:
             confirm_font = self.menu_font.render( u"下りる階段があります　下りますか？", True, COLOR_WHITE)
         elif self.instruction == self.UPSTAIRS:
             confirm_font = self.menu_font.render( u"上る階段があります　上りますか？", True, COLOR_WHITE)
         elif self.instruction == self.SEARCH:
             confirm_font = self.menu_font.render( u"探しますか？", True, COLOR_WHITE)
         elif self.instruction == self.PRESS:
             confirm_font = self.menu_font.render( u"押しますか？", True, COLOR_WHITE)
         elif self.instruction == self.BUY_ITEM:
             confirm_font = self.menu_font.render( u"買いますか？", True, COLOR_WHITE)
               

         yes_font = self.menu_font.render( u"はい", True, COLOR_WHITE) 
         no_font = self.menu_font.render( u"いいえ", True, COLOR_WHITE) 

         if self.menu == self.YES:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+45,(self.right-self.left)-8,30), 0)
         elif self.menu == self.NO:
             pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+75,(self.right-self.left)-8,30), 0)


         screen.blit(confirm_font, ( self.centerx - confirm_font.get_width()/2 , self.top + 20))
         screen.blit(yes_font, ( self.centerx - yes_font.get_width()/2 , self.top + 50))
         screen.blit(no_font, ( self.centerx - no_font.get_width()/2 , self.top + 80))

         #draw extra window
         self.who_pay_window.draw(screen, characters)
         
    def confirm_window_handler(self, game_self, event, character):

        if self.who_pay_window.is_visible:
            self.who_pay_window.system_notify_window_handler(event, game_self, game_self.party.member)
            return
        
        if event.type == KEYDOWN and event.key == K_UP: #moves the cursor up
            self.menu -= 1
            if self.menu < 0:
                self.menu = self.MENU_MAX
        elif event.type == KEYDOWN and event.key == K_DOWN:
                self.menu += 1
                if self.menu > self.MENU_MAX:
                    self.menu = 0

        if event.type == KEYDOWN and event.key == K_x:
            if self.instruction == self.SEARCH:
                self.is_visible = False
                game_self.dungeon.dungeon_message_window.search_window = None
                game_self.dungeon.dungeon_message_window.is_visible = False
                return

            self.menu = 0
            self.is_visible = False


        elif  event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
            if self.instruction == self.HOUSE:
                if self.menu == self.YES:
                    if len(game_self.party.member) > 0:
                        self.who_pay_window.is_visible = True
                else:
                    game_self.shop.buy_house.is_visible = False

            elif self.instruction == self.HOUSE_CHANGE:
                if self.menu == self.YES:
                    if len(game_self.party.member) > 0:
                        self.who_pay_window.is_visible = True
                else:
                    game_self.house.house_change.is_visible = False
    
            elif self.instruction == self.SAVE:
                if self.menu == self.YES:
                    save.save( self, game_self)
                    if game_self.inn != None:
                        game_self.inn.save_confirm.is_visible = False
                    if game_self.house != None:
                        game_self.house.save_confirm.is_visible = False
                else:
                    if game_self.inn != None:
                        game_self.inn.save_confirm.is_visible = False
                    if game_self.house != None:
                        game_self.house.save_confirm.is_visible = False
    
            elif self.instruction == self.LOAD:
                if self.menu == self.YES:
                    save.load( self, game_self)
                    if game_self.inn != None:
                        game_self.inn.load_confirm.is_visible = False
                    if game_self.house != None:
                        game_self.house.load_confirm.is_visible = False
                else:
                    if game_self.inn != None:
                        game_self.inn.load_confirm.is_visible = False
                    if game_self.house != None:
                        game_self.house.load_confirm.is_visible = False

            elif self.instruction == self.JOB_CHANGE:
                if self.menu == self.YES:

                    if character.job == 0:
                        character.strength = 10
                        character.intelligence = 5
                        character.piety = 8
                        character.vitality = 12
                        character.agility = 8
                        character.luck = 8            
                    elif character.job == 1:
                        character.strength = 12
                        character.intelligence = 8
                        character.piety = 8
                        character.vitality = 10
                        character.agility = 8
                        character.luck = 5           
                    elif character.job == 2:
                        character.strength = 8
                        character.intelligence = 12
                        character.piety = 8
                        character.vitality = 5
                        character.agility = 10
                        character.luck = 8            
                    elif character.job == 3:  
                        character.strength = 8
                        character.intelligence = 8
                        character.piety = 12
                        character.vitality = 10
                        character.agility = 5
                        character.luck = 8            
                    elif character.job == 4:  
                        character.strength = 8
                        character.intelligence = 8
                        character.piety = 5
                        character.vitality = 8
                        character.agility = 12
                        character.luck = 10           
                    elif character.job == 5:
                        character.strength = 5
                        character.intelligence = 8
                        character.piety = 8
                        character.vitality = 8
                        character.agility = 10
                        character.luck = 12  

                    if character.alignment == 1:
                        character.job = 10+(character.job*3)
                    elif character.alignment == 0:
                        character.job = 10+(character.job*3)+1
                    elif character.alignment == -1:
                        character.job = 10+(character.job*3)+2
                        
                        
                    character.strength_max += 10
                    character.intelligence_max += 10
                    character.piety_max += 10
                    character.vitality_max += 10
                    character.agility_max += 10
                    character.luck_max += 10
                    character.exp = 0

                    character.level = 1

                    del game_self.castle.change_job_window.possible_characters[game_self.castle.change_job_window.menu]

                    if game_self.castle.change_job_window.menu > len(game_self.castle.change_job_window.possible_characters)-1:
                        game_self.castle.change_job_window.menu-=1

                    
                    game_self.castle.change_job_window.job_change_confirm.is_visible = False

                    
                    pass
                else:
                    game_self.castle.change_job_window.job_change_confirm.is_visible = False
            elif self.instruction == self.DOWNSTAIRS:
                if self.menu == self.YES:
                    for character in game_self.party.member:
                        character.coordinate[2] = character.coordinate[2]-1

                    #TO-DO load new floor
                    if character.coordinate[2] != 0:
                        game_self.dungeon = dungeon.Dungeon(character.coordinate[2])
                        
                    #return to tower   
                    if game_self.party.member[0].coordinate[2] == 0:
                        game_self.game_state = TOWER
                        i = 0
                        for charcter in game_self.party.member:
                            game_self.party.member[i].coordinate = [-1,-1,-1]
                            i += 1
                        game_self.dungeon.battle = None
                        game_self.dungeon.battle_flag = 0
                        game_self.dungeon.music = 0
                        game_self.party.direction = 0
                        game_self.tower = tower.Tower()
                        game_self.dungeon = None

                        for character in game_self.party.member:
                            character.face_shield = 0
                            character.battle_ac = 0
                            character.permanant_ac = 0

                        self.is_visible = False
                        self = None
                    
                else:
                    self.is_visible = False
                    self = None

            elif self.instruction == self.UPSTAIRS:
                if self.menu == self.YES:
                    for character in game_self.party.member:
                        character.coordinate[2] = character.coordinate[2]+1

                    game_self.dungeon = dungeon.Dungeon(character.coordinate[2])

                else:
                    self.is_visible = False
                    self = None

            elif self.instruction == self.SEARCH:

                if self.menu == self.YES:
                    if game_self.dungeon.dungeon_message_window.coordinate == [10, 3, 1]:
                        game_self.dungeon.dungeon_message_window.message.append( "" )
                        game_self.dungeon.dungeon_message_window.message.append( u"冒険者は銅の鍵を見つけた!" )


                        i = 0
                        for chara in game_self.party.member:
                            while (len(chara.items) < chara.item_max):
                                chara.items.append( item.Item( game_self.item_data[900]))
                                i+=1
                                break
                            if i == 1:
                                break

                    if game_self.dungeon.dungeon_message_window.coordinate == [5, 4, 2]:
                        game_self.dungeon.dungeon_message_window.message.append( "" )
                        game_self.dungeon.dungeon_message_window.message.append( u"冒険者は緑の鍵を見つけた!" )

                        i = 0
                        for chara in game_self.party.member:
                            while (len(chara.items) < chara.item_max):
                                chara.items.append( item.Item( game_self.item_data[901]))
                                i+=1
                                break
                            if i == 1:
                                break


                    
                    self.is_visible = False
                    game_self.dungeon.dungeon_message_window.search_window = None
                    #game_self.dungeon.dungeon_message_window.is_visible = False                  
                    game_self.dungeon.dungeon_message_window.key_press = False                    
     
                        
                else:
                    self.is_visible = False
                    game_self.dungeon.dungeon_message_window.press_window = None
                    game_self.dungeon.dungeon_message_window.search_window = None
                    game_self.dungeon.dungeon_message_window.is_visible = False
                    game_self.dungeon.dungeon_message_window.message = None
                    game_self.dungeon.dungeon_message_window.coordinate = None
                    game_self.dungeon.dungeon_message_window.key_press = False                    


                pass

            elif self.instruction == self.PRESS:
                if self.menu == self.YES:
                    if game_self.dungeon.dungeon_message_window.coordinate == [15,14,2]:

                        game_self.dungeon.dungeon_message_window.message.append( "" )
                        game_self.dungeon.dungeon_message_window.message.append( u"どこかで鍵が開く音がした" )

                        #open the door
                        #need to add one to position of game because it start with 0
                        print game_self.dungeon.vertical_wall[13][7] 
                        game_self.dungeon.vertical_wall[13][7] = 2
                    
                    self.is_visible = False
                    game_self.dungeon.dungeon_message_window.press_window = None
                    game_self.dungeon.dungeon_message_window.key_press = False                    


                    pass
                else:
                    self.is_visible = False
                    game_self.dungeon.dungeon_message_window.press_window = None
                    game_self.dungeon.dungeon_message_window.search_window = None
                    game_self.dungeon.dungeon_message_window.is_visible = False
                    game_self.dungeon.dungeon_message_window.message = None
                    game_self.dungeon.dungeon_message_window.coordinate = None
                    game_self.dungeon.dungeon_message_window.key_press = False

            elif self.instruction == self.BUY_ITEM:
                if self.menu == self.YES:

                    total_money = 0
                    for chara in game_self.party.member:
                        total_money += chara.money


                    #if not enough money
                    if total_money < game_self.dungeon.party_encounter_window.message_window.price:
                        game_self.dungeon.party_encounter_window.message_window.message.append( "")
                        game_self.dungeon.party_encounter_window.message_window.message.append( u"だがお金が足りない！")

                        self.is_visible = False
                    else:

                        
                        for chara in game_self.party.member:
                            if len(chara.items) < chara.item_max:
                                chara.items.append( game_self.dungeon.party_encounter_window.message_window.get_item)
                                break

                        price = game_self.dungeon.party_encounter_window.message_window.price

                        for chara in game_self.party.member:
                            if price > chara.money:
                                price -= chara.money
                                chara.money = 0
                            else:
                                chara.money -= price
                                price = 0
                                

                        self.is_visible = False
                        game_self.dungeon.party_encounter_window.message_window.message.append( u"冒険者達は"+ game_self.dungeon.party_encounter_window.message_window.get_item.name+ u"を買った！")

                    
                else:
                    self.is_visible = False
                    game_self.dungeon.party_encounter_window.message_window = None
                pass
            #need x key too
            


                pass

class level_up_window(window.Window):

    UP, NOT_UP = 0 ,1
    
    def __init__(self, rectangle, instruction):
        window.Window.__init__(self, rectangle)
        self.is_visible = False
        self.menu = self.UP

        self.instruction = instruction

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

    def draw(self, screen, character, change):
        """draw the window on the screen"""
        window.Window.draw(self, screen)        
        if self.is_visible == False: return

        #if level doesn't go up
        if self.instruction == self.NOT_UP:

            name_font = self.menu_font.render( character.name, True, COLOR_WHITE)
            lv_font = self.menu_font.render( u"は次のレベルまで", True, COLOR_WHITE) 
            exp_font = self.menu_font.render( u"あと " + str(character.next) + u"EXPが必要です", True, COLOR_WHITE) 

            screen.blit(name_font, ( self.left + 20 , self.top + 20))
            screen.blit(lv_font, ( self.left + 25 + name_font.get_width() , self.top + 20))
            screen.blit(exp_font, ( self.left + 20 , self.top + 50))
 
            return
        
        
        #if level up
        name_font = self.menu_font.render( character.name, True, COLOR_WHITE)
        lv_up_font = self.menu_font.render( u"のレベルが上がりました！", True, COLOR_WHITE) 
        screen.blit(name_font, ( self.left + 20 , self.top + 20))
        screen.blit(lv_up_font, ( self.left + 25 + name_font.get_width() , self.top + 20))
 
        connect_font =  self.menu_font.render( u"は", True, COLOR_WHITE)
        gain_font =  self.menu_font.render( u"を得た", True, COLOR_WHITE)
        lose_font =  self.menu_font.render( u"を失った", True, COLOR_WHITE)

        strength_font =  self.menu_font.render( u"力", True, COLOR_WHITE)
        intelligence_font =  self.menu_font.render( u"知恵", True, COLOR_WHITE)
        piety_font =  self.menu_font.render( u"信仰心", True, COLOR_WHITE)
        vitality_font =  self.menu_font.render( u"生命力", True, COLOR_WHITE)
        agility_font =  self.menu_font.render( u"素早さ", True, COLOR_WHITE)
        luck_font =  self.menu_font.render( u"運", True, COLOR_WHITE)

        hp_font = self.menu_font.render( "HP", True, COLOR_WHITE)
        connect2_font = self.menu_font.render( u"が", True, COLOR_WHITE)
        hp_gain_font = self.menu_font.render( str(change[6]), True, COLOR_WHITE)
        gain2_font = self.menu_font.render( u"上がった", True, COLOR_WHITE)
        
        mp_font = self.menu_font.render( u"は新しい呪文を覚えた！", True, COLOR_WHITE)

        number_changed = 0
        #strength
        if change[0] > 0:
            screen.blit(name_font, ( self.left + 20 , self.top + 50))
            screen.blit(connect_font, ( self.left + 20 + name_font.get_width() , self.top + 50))
            screen.blit(strength_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() , self.top + 50))
            screen.blit(gain_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() + strength_font.get_width() , self.top + 50))
            number_changed += 1
        elif change[0] < 0:
            screen.blit(name_font, ( self.left + 20 , self.top + 50))
            screen.blit(connect_font, ( self.left + 20 + name_font.get_width() , self.top + 50))
            screen.blit(strength_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() , self.top + 50))
            screen.blit(lose_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() + strength_font.get_width() , self.top + 50))
            number_changed += 1           
        #intelligence
        if change[1] > 0:
            screen.blit(name_font, ( self.left + 20 , self.top + 50 + number_changed*30))
            screen.blit(connect_font, ( self.left + 20 + name_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(intelligence_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(gain_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() + intelligence_font.get_width() , self.top + 50 + number_changed*30))
            number_changed += 1
        elif change[1] < 0:
            screen.blit(name_font, ( self.left + 20 , self.top + 50 + number_changed*30))
            screen.blit(connect_font, ( self.left + 20 + name_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(intelligence_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(lose_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() + intelligence_font.get_width() , self.top + 50 + number_changed*30))
            number_changed += 1           
        #piety
        if change[2] > 0:
            screen.blit(name_font, ( self.left + 20 , self.top + 50 + number_changed*30))
            screen.blit(connect_font, ( self.left + 20 + name_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(piety_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(gain_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() + piety_font.get_width() , self.top + 50 + number_changed*30))
            number_changed += 1
        elif change[2] < 0:
            screen.blit(name_font, ( self.left + 20 , self.top + 50 + number_changed*30))
            screen.blit(connect_font, ( self.left + 20 + name_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(piety_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(lose_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() + piety_font.get_width() , self.top + 50 + number_changed*30))
            number_changed += 1           
        #vitality
        if change[3] > 0:
            screen.blit(name_font, ( self.left + 20 , self.top + 50 + number_changed*30))
            screen.blit(connect_font, ( self.left + 20 + name_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(vitality_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(gain_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() + vitality_font.get_width() , self.top + 50 + number_changed*30))
            number_changed += 1
        elif change[3] < 0:
            screen.blit(name_font, ( self.left + 20 , self.top + 50 + number_changed*30))
            screen.blit(connect_font, ( self.left + 20 + name_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(vitality_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(lose_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() + vitality_font.get_width() , self.top + 50 + number_changed*30))
            number_changed += 1           
        #agility
        if change[4] > 0:
            screen.blit(name_font, ( self.left + 20 , self.top + 50 + number_changed*30))
            screen.blit(connect_font, ( self.left + 20 + name_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(agility_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(gain_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() + agility_font.get_width() , self.top + 50 + number_changed*30))
            number_changed += 1
        elif change[4] < 0:
            screen.blit(name_font, ( self.left + 20 , self.top + 50 + number_changed*30))
            screen.blit(connect_font, ( self.left + 20 + name_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(agility_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(lose_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() + agility_font.get_width() , self.top + 50 + number_changed*30))
            number_changed += 1           
        #luck
        if change[5] > 0:
            screen.blit(name_font, ( self.left + 20 , self.top + 50 + number_changed*30))
            screen.blit(connect_font, ( self.left + 20 + name_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(luck_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(gain_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() + luck_font.get_width() , self.top + 50 + number_changed*30))
            number_changed += 1
        elif change[5] < 0:
            screen.blit(name_font, ( self.left + 20 , self.top + 50 + number_changed*30))
            screen.blit(connect_font, ( self.left + 20 + name_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(luck_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() , self.top + 50 + number_changed*30))
            screen.blit(lose_font, ( self.left + 20 + name_font.get_width() + connect_font.get_width() + luck_font.get_width() , self.top + 50 + number_changed*30))
            number_changed += 1           


        #hp
        screen.blit(name_font, ( self.left + 20 , self.top + 50 + number_changed*30))
        screen.blit(connect_font, ( self.left + 20 + name_font.get_width() , self.top + 50 + number_changed*30))
        screen.blit(hp_font, ( self.left + 25 + name_font.get_width() + connect_font.get_width() , self.top + 50 + number_changed*30))
        screen.blit(connect2_font, ( self.left + 25 + name_font.get_width() + connect_font.get_width() + hp_font.get_width() , self.top + 50 + number_changed*30))
        screen.blit(hp_gain_font, ( self.left + 30 + name_font.get_width() + connect_font.get_width() + hp_font.get_width() + connect2_font.get_width(), self.top + 50 + number_changed*30))
        screen.blit(gain2_font, ( self.left + 30 + name_font.get_width() + connect_font.get_width() + hp_font.get_width() + connect2_font.get_width() + hp_gain_font.get_width(), self.top + 50 + number_changed*30))
        number_changed += 1

        #mp
        if change[7] > 0:
            screen.blit(name_font, ( self.left + 20 , self.top + 50 + number_changed*30))
            screen.blit(mp_font, ( self.left + 20 + name_font.get_width() , self.top + 50 + number_changed*30))

    def level_up_window_handler(self, event , game_self):

        if event.type == KEYDOWN and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):

            if game_self.game_state == INN:
                game_self.inn.inn_window.who_rest.resting_window = Rest_window(Rect(100, 160 ,400, 50), Rest_window.REST)
                self.is_visible = False
       
            if game_self.game_state == HOUSE:
                game_self.house.who_rest.resting_window = Rest_window(Rect(100, 160 ,400, 50), Rest_window.REST)
                self.is_visible = False
       


class Item_select_window(window.Window):

    ITEM_OUT, ITEM_IN = 0,1

    MENU_MAX = 9

    def __init__(self, rectangle, instruction ):

        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.menu = 0
        self.page = 0

        self.instruction = instruction

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.top_font = self.menu_font.render( u"の持ち物:", True, COLOR_WHITE) 

        self.hold_item_window = Donate_finish_window( Rect(150, 160 ,300, 50), 6)
        self.receive_item_window = Donate_finish_window( Rect(150, 160 ,300, 50), 6)



    def draw( self, screen, game_self):
        """draw the shop window on screen"""

        if self.is_visible == False: return
        
        window.Window.draw(self, screen)

        if self.instruction == 0:
            if game_self.game_state == INN:            
                character = game_self.party.member[game_self.inn.item_out_window.menu]
                name_font = self.menu_font.render( character.name, True, COLOR_WHITE)
            if game_self.game_state == HOUSE:
                character = game_self.party.member[game_self.house.item_out_window.menu]
                name_font = self.menu_font.render( character.name, True, COLOR_WHITE)
        else:
            if game_self.game_state == INN:
                character = game_self.party.member[game_self.inn.item_in_window.menu]            
                name_font = self.menu_font.render( u"宿屋", True, COLOR_WHITE)
            if game_self.game_state == HOUSE:
                character = game_self.party.member[game_self.house.item_in_window.menu]            
                name_font = self.menu_font.render( u"自宅", True, COLOR_WHITE)                


        screen.blit( name_font, (self.left+20, self.top+20))
        screen.blit( self.top_font, (self.left+20+name_font.get_width(), self.top+20))

        if self.instruction == self.ITEM_OUT:
            #draw the box on item selected
            if character.items != []:
                #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
                #the height depends on the size of font
                pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+55 + 30*self.menu,(self.right-self.left)-8,30), 0)


            i = 0
            for item in character.items:
                item_font = self.menu_font.render( item.name, True, COLOR_WHITE)
                screen.blit ( item_font, (self.centerx - item_font.get_width()/2, self.top+60+i*30))
                i += 1

        if self.instruction == self.ITEM_IN:

            if game_self.game_state == INN:
                item_list = game_self.party.inn_item
            elif game_self.game_state == HOUSE:
                item_list = game_self.party.house_item

            if item_list != []:
                pygame.draw.rect(screen, COLOR_GLAY,  Rect( self.left+4, self.top+55 + 30*self.menu,(self.right-self.left)-8,30), 0)

            i = 0
            for item_id in item_list[self.page*10:(self.page+1)*10]:
                item_font = game_self.item_data[item_id][0].strip("\"")
                item_font = unicode(item_font, encoding="sjis")
                item_font = self.menu_font.render( item_font, True, COLOR_WHITE)
                screen.blit( item_font, (self.centerx - item_font.get_width()/2, self.top+60+i*30))
                i+=1
        
                


        self.hold_item_window.draw(screen)
        self.receive_item_window.draw(screen)

    def item_select_window_handler( self, event, game_self):

        if self.hold_item_window.is_visible == True:
            self.hold_item_window.donate_finish_window_handler( event, game_self)
            return
        if self.receive_item_window.is_visible == True:
            self.receive_item_window.donate_finish_window_handler( event, game_self)
            return

        if self.instruction == self.ITEM_OUT:
            if game_self.game_state == INN:
                character = game_self.party.member[game_self.inn.item_out_window.menu]
            elif game_self.game_state == HOUSE:
                character = game_self.party.member[game_self.house.item_out_window.menu]                
        elif self.instruction == self.ITEM_IN:
            if game_self.game_state == INN:
                character = game_self.party.member[game_self.inn.item_in_window.menu]
            elif game_self.game_state == HOUSE:
                character = game_self.party.member[game_self.house.item_in_window.menu]
        #moves back to shop
        if event.type == KEYDOWN and event.key == K_x:
            game_self.cancel_se.play()
            self.menu = 0
            self.page = 0
            self.is_visible =False

        #moves the cursor up
        elif event.type == KEYDOWN and event.key == K_UP:
            game_self.cursor_se.play()
            self.menu -= 1
            if self.menu < 0:
                self.menu = 0 
                
        #moves the cursor down
        elif event.type == KEYDOWN and event.key == K_DOWN:
            game_self.cursor_se.play()
            if self.instruction == self.ITEM_OUT:
                if len(character.items) > self.menu+1:
                    self.menu += 1
                    if self.menu > self.MENU_MAX:
                        self.menu = self.MENU_MAX
                        

            if self.instruction == self.ITEM_IN:
                if game_self.game_state == INN:
                    if len(game_self.party.inn_item) > self.menu+self.page*10+1:
                        self.menu+=1
                        if self.menu > self.MENU_MAX:
                            self.menu = self.MENU_MAX
                if game_self.game_state == HOUSE:
                    if len(game_self.party.house_item) > self.menu+self.page*10+1:
                        self.menu+=1
                        if self.menu > self.MENU_MAX:
                            self.menu = self.MENU_MAX


        elif event.type == KEYDOWN and event.key == K_RIGHT:
            if self.instruction == self.ITEM_IN:
                if game_self.game_state == INN:
                    if len(game_self.party.inn_item) > (self.page+1)*10:
                        game_self.cursor_se.play()
                        self.page += 1
                        self.menu = 0
                if game_self.game_state == HOUSE:
                    if len(game_self.party.house_item) > (self.page+1)*10:
                        game_self.cursor_se.play()
                        self.page += 1
                        self.menu = 0
                
        elif event.type == KEYDOWN and event.key == K_LEFT:
            if self.instruction == self.ITEM_IN:
                if self.page > 0:
                    game_self.cursor_se.play()
                    self.page -= 1
                    self.menu = 0


        elif event.type == KEYDOWN and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
            if self.instruction == self.ITEM_OUT:
                #max item to store for inn is 20
                if game_self.game_state == INN:
                    if len(game_self.party.inn_item) == 20:
                        return
                if game_self.game_state == HOUSE:
                    if len(game_self.party.house_item) == 10*game_self.party.house:
                        return
                    
                if len(character.items) > 0:

                    self.hold_item_window.is_visible = True
                    if game_self.game_state == INN:
                        game_self.party.inn_item.append( character.items[self.menu].id )
                    elif game_self.game_state == HOUSE:
                        game_self.party.house_item.append( character.items[self.menu].id )
                    del character.items[self.menu]
                    if self.menu+1 > len(character.items):
                        self.menu -=1

            if self.instruction == self.ITEM_IN:

                if len(character.items) == 10:
                    return
                if game_self.game_state == INN:
                    if len(game_self.party.inn_item) > 0:
                        character.items.append( item.Item( game_self.item_data[game_self.party.inn_item[self.menu+self.page*10]]))
                        del game_self.party.inn_item[self.menu+self.page*10]
                        self.receive_item_window.is_visible = True
                        if self.menu+self.page*10+1 > len(game_self.party.inn_item):
                            self.menu-=1
                elif game_self.game_state == HOUSE:
                    if len(game_self.party.house_item) > 0:
                        character.items.append( item.Item( game_self.item_data[game_self.party.house_item[self.menu+self.page*10]]))
                        del game_self.party.house_item[self.menu+self.page*10]
                        self.receive_item_window.is_visible = True
                        if self.menu+self.page*10+1 > len(game_self.party.house_item):
                            self.menu-=1

class Item_view(window.Window):


    def __init__(self, rectangle):

        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.menu = 0
        self.equip = 0
        self.select = 0


        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.top_font = self.menu_font.render( u"の持ち物:", True, COLOR_WHITE)

        self.item_todo_window = Item_menu_select(Rect(170, 80, 300, 180))


    def update(self):
        pass
    def draw(self, screen, game_self):

        if self.is_visible == False: return


        window.Window.draw(self, screen)

        if game_self.game_state == MENU:
            character = game_self.party.member[game_self.menu.item_window.menu]
        elif game_self.game_state == DUNGEON:
            character = game_self.party.member[game_self.dungeon.battle.selected]

        if character.items == []:
            self.select = 1

        name_font = self.menu_font.render( character.name, True, COLOR_WHITE)

        screen.blit( name_font, (self.left+20, self.top+20))
        screen.blit( self.top_font, (self.left+20+name_font.get_width(), self.top+20))

        #draw the box on item selected
        if character.items != []:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            #pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+55 + 30*self.menu,(self.right-self.left)-8,30), 0)
            if self.select == 0:
                pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+55 + 30*self.menu,self.right-320,30), 0)
        if self.select == 1:
            pygame.draw.rect(screen, COLOR_GLAY, Rect( self.right-250, self.top+55 + 30*self.equip, 246, 30), 0)



        i = 0
        for item_c in character.items:
            item_font = self.menu_font.render( item_c.name, True, COLOR_WHITE)
            #screen.blit ( item_font, (self.centerx - item_font.get_width()/2, self.top+60+i*30))
            screen.blit ( item_font, (self.left+20, self.top+60+i*30))

            i += 1

        i = 0
        for equip in character.equip:
            if isinstance( equip, item.Item):
                equip_font = self.menu_font.render( "E:" + equip.name, True, COLOR_WHITE)
                screen.blit( equip_font, (self.right-220, self.top+60+i*30))
            else:
                equip_font = self.menu_font.render( "----------", True, COLOR_WHITE)
                screen.blit( equip_font, (self.right-220, self.top+60+i*30))
                
            i+= 1

        self.item_todo_window.draw(screen, game_self)

      
    def item_view_handler(self, event, game_self):

        if game_self.game_state == MENU:
            character = game_self.party.member[game_self.menu.item_window.menu]
        if game_self.game_state == DUNGEON:
            character = game_self.party.member[game_self.dungeon.battle.selected]

        if self.item_todo_window.is_visible == True:
            self.item_todo_window.item_menu_select_handler(event, game_self)
            return


        #moves back to shop
        if event.type == KEYDOWN and event.key == K_x:
            game_self.cancel_se.play()
            self.menu = 0
            self.is_visible =False

        #moves the cursor up
        elif event.type == KEYDOWN and event.key == K_UP:
            game_self.cursor_se.play()
            if self.select == 0:
                self.menu -= 1
                if self.menu < 0:
                    self.menu = 0
            else:
                self.equip -= 1
                if self.equip < 0:
                    self.equip = 0
                
        #moves the cursor down
        elif event.type == KEYDOWN and event.key == K_DOWN:
            game_self.cursor_se.play()
            if self.select == 0 and len(character.items) > self.menu+1:
                self.menu += 1
            if self.select == 1 and self.equip < 5:
                self.equip += 1
                
        elif event.type == KEYDOWN and event.key == K_LEFT:
            game_self.cursor_se.play()
            if self.select == 1:
                self.select = 0
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            game_self.cursor_se.play()
            if self.select == 0:
                self.select = 1
                
        elif event.type == KEYDOWN and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):

            if game_self.game_state == MENU:
                if self.select == 0 and len(character.items) > 0:
                    self.item_todo_window.is_visible = True
                if self.select == 1:
                    if isinstance( character.equip[self.equip], item.Item) and len(character.items) < character.item_max:
                        character.items.append( character.equip[self.equip] )
                        character.equip[self.equip] = 0
                        
            elif game_self.game_state == DUNGEON:
                pass




class Magic_all_view(window.Window):
    
    def __init__(self, rectangle):

        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.menu = 0

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.top_font = self.menu_font.render( u"の呪文", True, COLOR_WHITE)

        self.magic_level_view = Magic_level(Rect(180, 50, 280, 250)) 
        #self.target_window = Target_select(Rect(120, 50, 400, 240)) 

    def update(self):
        pass
    def draw(self, screen, game_self):

        if self.is_visible == False: return
        
        window.Window.draw(self, screen)

        if game_self.game_state == MENU:
            character = game_self.party.member[game_self.menu.magic_window.menu]
        elif game_self.game_state == DUNGEON:
            character = game_self.party.member[game_self.dungeon.battle.selected]

            
        name_font = self.menu_font.render( character.name, True, COLOR_WHITE)

        screen.blit( name_font, (self.left+20, self.top+20))
        screen.blit( self.top_font, (self.left+20+name_font.get_width(), self.top+20))


        #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
        #the height depends on the size of font
        pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+20 + (self.menu%7)*30, self.top+55 + int(self.menu/7)*30, 15,25), 0)


        i = 0
        for magic in character.magician_mp:
            magic_font = self.menu_font.render( str(magic), True, COLOR_WHITE)
            screen.blit ( magic_font, ( self.left+20+30*i, self.top+60))
            if i < 7:
                slash_font = self.menu_font.render( "/" , True, COLOR_WHITE)
                screen.blit( slash_font, (self.left+20+30*i+15, self.top+60))
            i += 1
        i = 0
        for magic in character.priest_mp:
            magic_font = self.menu_font.render( str(magic), True, COLOR_WHITE)
            screen.blit ( magic_font, ( self.left+20+30*i, self.top+90))
            if i < 7:
                slash_font = self.menu_font.render( "/" , True, COLOR_WHITE)
                screen.blit( slash_font, (self.left+20+30*i+15, self.top+90))
            i += 1

        self.magic_level_view.draw(screen, game_self)
        
    def magic_all_view_handler( self, event, game_self):

        if self.magic_level_view.is_visible == True:
            self.magic_level_view.magic_level_view_handler(event, game_self)
            return

        #moves back to shop
        if event.type == KEYDOWN and event.key == K_x:
            game_self.cancel_se.play()
            self.menu = 0
            self.is_visible =False

        #moves the cursor up
        elif event.type == KEYDOWN and event.key == K_UP:
            game_self.cursor_se.play()
            self.menu -= 7
            if self.menu < 0:
                self.menu += 14
                
        #moves the cursor down
        elif event.type == KEYDOWN and event.key == K_DOWN:
            game_self.cursor_se.play()
            self.menu += 7
            if self.menu > 13:
                self.menu -= 14

                
        #moves the cursor left
        elif event.type == KEYDOWN and event.key == K_LEFT:
            game_self.cursor_se.play()
            self.menu -= 1
            if self.menu == 6:
                self.menu = 13
            if self.menu < 0:
                self.menu = 6
            
        #moves the cursor right
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            game_self.cursor_se.play()
            self.menu += 1
            if self.menu == 7:
                self.menu = 0
            if self.menu > 13:
                self.menu = 7

        elif event.type == KEYDOWN and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
            game_self.select_se.play()
            self.magic_level_view.is_visible = True


class Magic_level(window.Window):

    def __init__(self, rectangle):

        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.menu = 0

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.top_font = self.menu_font.render( u"呪文LV", True, COLOR_WHITE)

        #if this is true, draw selection window and have selection
        self.target_select = None

        self.draw_map = False
        self.created_dungeon = False


    def update(self):
        pass
    def draw(self, screen, game_self):

        if self.is_visible == False: return
        
        window.Window.draw(self, screen)

        if game_self.game_state == MENU:
            level = game_self.menu.magic_window.magic_all_view.menu
            character = game_self.party.member[game_self.menu.magic_window.menu]
        elif game_self.game_state == DUNGEON:
            level = game_self.dungeon.battle.magic_window.menu
            character = game_self.party.member[game_self.dungeon.battle.selected]
            

        if level < 7:
            top_font = self.menu_font.render( u"呪文LV" + str(level+1), True, COLOR_WHITE)
        else:
            top_font = self.menu_font.render( u"呪文LV" + str(level-6), True, COLOR_WHITE)
            
        screen.blit( top_font, (self.left+20, self.top+20))


        #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
        #the height depends on the size of font
        pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4,  self.top+55 + self.menu*30, self.right-self.left-8, 30), 0)

        if level < 7:
            i = 0
            for magic in character.magic[level]:
                if magic == 1:
                    magic_font = game_self.magic_data[level*6+1+i][0].strip("\"")
                    magic_font = unicode( magic_font, encoding="sjis")
                    #the magic is only used in battle
                    if game_self.game_state == MENU:
                        if game_self.magic_data[level*6+1+i][4] == "\"BATTLE\"":
                            magic_font = self.menu_font.render( magic_font, True, COLOR_GLAY)    
                        else:
                            magic_font = self.menu_font.render( magic_font, True, COLOR_WHITE)
                    elif game_self.game_state == DUNGEON:
                        magic_font = self.menu_font.render( magic_font, True, COLOR_WHITE)

                    screen.blit( magic_font, (self.centerx - magic_font.get_width()/2, self.top+60+i*30))
                else:
                    magic_font = self.menu_font.render( "????????", True, COLOR_GLAY)
                    screen.blit( magic_font, (self.centerx - magic_font.get_width()/2, self.top+60+i*30))
                    
                i+=1

        else:
            i = 0
            for magic in character.priest_magic[level-7]:
                if magic == 1:
                    magic_font = game_self.magic_data[(level-7)*6+50+i][0].strip("\"")
                    magic_font = unicode( magic_font, encoding="sjis")

                    if game_self.game_state == MENU:
                        #the magic is only used in battle
                        if game_self.magic_data[(level-7)*6+50+i][4] == "\"BATTLE\"":
                            magic_font = self.menu_font.render( magic_font, True, COLOR_GLAY)    
                        else:
                            magic_font = self.menu_font.render( magic_font, True, COLOR_WHITE)
                    elif game_self.game_state == DUNGEON:
                        magic_font = self.menu_font.render( magic_font, True, COLOR_WHITE)

                    screen.blit( magic_font, (self.centerx - magic_font.get_width()/2, self.top+60+i*30))
                else:
                    magic_font = self.menu_font.render( "????????", True, COLOR_GLAY)
                    screen.blit( magic_font, (self.centerx - magic_font.get_width()/2, self.top+60+i*30))
                i+=1

        if self.target_select != None:
            if self.target_select.remove == True:
                self.target_select = None
                return
            #draw enemy window or party window
            self.target_select.draw(screen, game_self)

        if self.draw_map == True:
            if self.created_dungeon == False:
                if game_self.party.member[0].coordinate[2] == -1:
                    game_self.dungeon = dungeon.Dungeon(1)
                else:
                    game_self.dungeon = dungeon.Dungeon(game_self.party.member[0].coordinate[2])
                self.created_dungeon = True
            screen.fill((0,0,0))
            game_self.dungeon.draw_dungeon_map(game_self, screen)

            #additionaly draw current coordinate and place

            #calculate point of triangle
            x = int(68+game_self.party.member[0].coordinate[0]*17)
            y = int(97+game_self.party.member[0].coordinate[1]*17)

            if game_self.party.direction == 0:
                pygame.draw.polygon(screen, (255,0,0), [(x+7,y+3), (x+11, y+11), (x+3, y+11)], 0)
            elif game_self.party.direction == 1:
                pygame.draw.polygon(screen, (255,0,0), [(x+13,y+7), (x+5, y+11), (x+5, y+3)], 0)
            elif game_self.party.direction == 2:
                pygame.draw.polygon(screen, (255,0,0), [(x+7,y+11), (x+11, y+3), (x+3, y+3)], 0)
            elif game_self.party.direction == 3:
                pygame.draw.polygon(screen, (255,0,0), [(x+3,y+7), (x+11, y+11), (x+11, y+3)], 0)

            coordinate_window = window.Window(Rect(415,270,210,60))
            coordinate_window.draw(screen)

            if len(str(game_self.party.member[0].coordinate[0])) == 1:
                x_font = "X:0" + str( game_self.party.member[0].coordinate[0])
            else:
                x_font = "X:" + str( game_self.party.member[0].coordinate[0])
                
            if len(str(game_self.party.member[0].coordinate[1])) == 1:
                y_font = " Y:0" + str( game_self.party.member[0].coordinate[1])
                self.menu_font.render( "Y: 0" + str( game_self.party.member[0].coordinate[1]), True, COLOR_WHITE)
            else:
                y_font = " Y:" + str( game_self.party.member[0].coordinate[1])
                self.menu_font.render( "Y: " + str( game_self.party.member[0].coordinate[1]), True, COLOR_WHITE)

            coordinate_font = x_font+ y_font
            coordinate_font = self.menu_font.render( coordinate_font, True, COLOR_WHITE)
            
            screen.blit( coordinate_font, (520-coordinate_font.get_width()/2, 290))

    def magic_level_view_handler( self, event, game_self):

        if self.target_select != None:
            self.target_select.magic_use_target_select_handler(event, game_self)
            return

        if self.draw_map == True:
            if event.type == KEYDOWN and ( event.key == K_x or event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
                game_self.dungeon = None
                self.draw_map = False
                self.created_dungeon = False
            
            return
                                                               

        #moves back to shop
        if event.type == KEYDOWN and event.key == K_x:
            game_self.cancel_se.play()
            self.menu = 0
            self.is_visible =False

        #moves the cursor up
        elif event.type == KEYDOWN and event.key == K_UP:
            game_self.cursor_se.play()
            self.menu -= 1
            if self.menu < 0:
                self.menu = 0
                
        #moves the cursor down
        elif event.type == KEYDOWN and event.key == K_DOWN:
            game_self.cursor_se.play()
            self.menu += 1
            if self.menu > 5:
                self.menu = 5

                
        #moves the cursor left
        elif event.type == KEYDOWN and event.key == K_LEFT:
            game_self.cursor_se.play()
            if game_self.game_state == MENU:
                game_self.menu.magic_window.magic_all_view.menu -= 1
                if game_self.menu.magic_window.magic_all_view.menu == 6:
                    game_self.menu.magic_window.magic_all_view.menu = 13
                if game_self.menu.magic_window.magic_all_view.menu < 0:
                    game_self.menu.magic_window.magic_all_view.menu = 6
            elif game_self.game_state == DUNGEON:
                game_self.dungeon.battle.magic_window.menu -= 1
                if game_self.dungeon.battle.magic_window.menu == 6:
                    game_self.dungeon.battle.magic_window.menu = 13
                if game_self.dungeon.battle.magic_window.menu < 0:
                    game_self.dungeon.battle.magic_window.menu = 6                
        #moves the cursor right
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            game_self.cursor_se.play()
            if game_self.game_state == MENU:
                game_self.menu.magic_window.magic_all_view.menu += 1
                if game_self.menu.magic_window.magic_all_view.menu == 7:
                    game_self.menu.magic_window.magic_all_view.menu = 0
                if game_self.menu.magic_window.magic_all_view.menu > 13:
                    game_self.menu.magic_window.magic_all_view.menu = 7
            elif game_self.game_state == DUNGEON:
                game_self.dungeon.battle.magic_window.menu += 1
                if game_self.dungeon.battle.magic_window.menu == 7:
                    game_self.dungeon.battle.magic_window.menu = 0
                if game_self.dungeon.battle.magic_window.menu > 13:
                    game_self.dungeon.battle.magic_window.menu = 7                

        elif event.type == KEYDOWN and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):

            if game_self.game_state == MENU:
                level = game_self.menu.magic_window.magic_all_view.menu
                character = game_self.party.member[game_self.menu.magic_window.menu]

                #TO-DO need to set magic function

                #is usable in camp and character is usable
                if level < 7 and game_self.magic_data[level*6+1+self.menu][4] == "\"CAMP\"" and character.magic[level][self.menu] == 1:

                    #if use is DUNGEON, it doesn't need target selection
                    if string.count(game_self.magic_data[level*6+1+self.menu][3], "DUNGEON") and ((level < 7 and character.magician_mp[level] > 0) or (level >= 7 and character.priest_mp[level-7] > 0)):

                        if level == 0 and self.menu == 3:
                            #draw map
                            self.draw_map = True
                            character.magician_mp[level] -= 1

                        if level == 1 and self.menu == 1:
                            #unseal the door
                            pass



                    elif ((level < 7 and character.magician_mp[level] > 0) or (level >= 7 and character.priest_mp[level-7] > 0)):
                        self.target_select = Magic_use_target_select(character, level, self.menu, "MAGICIAN", game_self.magic_data[level*6+1+self.menu][3].strip("\""))

                elif level >= 7 and game_self.magic_data[(level-7)*6+50+self.menu][4] == "\"CAMP\"" and character.priest_magic[level-7][self.menu] == 1:

                    if string.count(game_self.magic_data[(level-7)*6+50+self.menu][3], "DUNGEON") and (level < 7 and character.magician_mp[level] > 0 or (level >=7 and character.priest_mp[level-7] > 0)):

                        #priest
                        level +=1
                        
                        if level == 9 and self.menu == 2:
                            #light the dungeon
                            game_self.party.torch += 30
                            character.priest_mp[level-8] -= 1
                            
                        level -= 1
                        
                    elif ((level < 7 and character.magician_mp[level] > 0 ) or (level >= 7 and character.priest_mp[level-7] > 0)):
                        self.target_select = Magic_use_target_select(character, level, self.menu, "PRIEST", game_self.magic_data[(level-7)*6+50+self.menu][3].strip("\""))
                    

            elif game_self.game_state == DUNGEON:
                level = game_self.dungeon.battle.magic_window.menu
                character = game_self.party.member[game_self.dungeon.battle.selected]

                #TO-DO need to set command for these magic selection

                #is usable in camp and dungeon and character is usable
                if level < 7 and character.magic[level][self.menu] == 1:
                    self.target_select = Magic_use_target_select(character, level, self.menu, "MAGICIAN", game_self.magic_data[level*6+1+self.menu][3].strip("\""))

                elif level >= 7 and character.priest_magic[level-7][self.menu] == 1:
                    self.target_select = Magic_use_target_select(character, level, self.menu, "PRIEST", game_self.magic_data[(level-7)*6+50+self.menu][3].strip("\""))




class Magic_use_target_select:

    def __init__(self, character, level, magic_number, magic_type, target):

        #party window rect
        #Rect(10, 300, 620, 170)

        #enemy window rect
        #Rect(10, 10, 620, 100)

        self.menu = 0

        #character who is using magic
        self.character = character
        #level and number of the magic
        self.level = level
        self.magic_number = magic_number

        #magician or priest
        self.magic_type = magic_type
        #target group or person
        self.target = target

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.remove = False

        self.enemy_select = string.count(self.target, "ENEMY")
        self.party_select = string.count(self.target, "PARTY")
        self.dungeon_select = string.count(self.target, "DUNGEON")
        self.random_select = string.count(self.target, "RANDOM")



    def update(self):
        pass
    def draw(self, screen, game_self):

        #if target is enemy
        if self.enemy_select > 0:
            #occurs only on battle so it is safe
            game_self.dungeon.battle.enemy_window.draw(screen)

            #add box to show selected enemy
            if self.target == "ENEMY_ONE" or self.target == "ENEMY_GROUP":

                if self.menu < 4:
                    pygame.draw.rect(screen, COLOR_GLAY, Rect(15, 18+self.menu*20, 320, 20), 0)
                else:
                    pygame.draw.rect(screen, COLOR_GLAY, Rect(335, 18+(self.menu-4)*20, 290, 20), 0)

            elif self.target == "ENEMY_ROW":
                pygame.draw.rect(screen, COLOR_GLAY, Rect(15, 18+self.menu*20, 610, 20), 0)

            elif self.target == "ENEMY_LINE":

                if self.menu == 0:
                    pygame.draw.rect(screen, COLOR_GLAY, Rect(15, 18, 320, len(game_self.dungeon.battle.enemyList)*20), 0)
                elif self.menu == 1:
                    pygame.draw.rect(screen, COLOR_GLAY, Rect(335, 18, 290, len(game_self.dungeon.battle.enemyListBack)*20), 0)
                
            elif self.target == "ENEMY_BOX":

                if self.menu == 0:
                    pygame.draw.rect(screen, COLOR_GLAY, Rect(15, 18, 600, 40), 0)
                elif self.menu == 1:
                    pygame.draw.rect(screen, COLOR_GLAY, Rect(15, 38, 600, 40), 0)
                elif self.menu == 2:
                    pygame.draw.rect(screen, COLOR_GLAY, Rect(15, 58, 600, 40), 0)
  
            elif self.target == "ENEMY_ALL":
                length = 0

                if len(game_self.dungeon.battle.enemyList) > len(game_self.dungeon.battle.enemyListBack):
                    length = len(game_self.dungeon.battle.enemyList)
                else:
                    length = len(game_self.dungeon.battle.enemyListBack)
                pygame.draw.rect(screen, COLOR_GLAY, Rect(15, 18, 600, length*20), 0)
            
            game_self.dungeon.battle.draw_enemy_names(game_self, screen)
        elif self.party_select > 0:
            game_self.party.draw(screen, game_self)

        elif self.dungeon_select > 0:
            game_self.party.draw(screen, game_self)




    def magic_use_target_select_handler( self, event, game_self):

        enemyList = None
        enemyListBack = None
        front_length = 0
        back_length = 0

        if game_self.dungeon != None:
            enemyList = game_self.dungeon.battle.enemyList
            enemyListBack = game_self.dungeon.battle.enemyListBack

            front_length = len(enemyList)
            back_length = len(enemyListBack)

        #moves back
        if event.type == KEYDOWN and event.key == K_x:
            self.remove = True
            return
            pass

        #moves the cursor up
        elif event.type == KEYDOWN and event.key == K_UP:
            if self.enemy_select:
                if self.target == "ENEMY_ONE" or self.target == "ENEMY_GROUP":
                    self.menu-=1
                    if self.menu == 3:
                        self.menu = 4+back_length-1
                    if self.menu < 0:
                        self.menu = front_length-1
                    pass
                elif self.target == "ENEMY_ROW":
                    max_length = 0
                    if front_length > back_length:
                        max_length = front_length
                    else:
                        max_length = back_length

                    self.menu -= 1

                    if self.menu < 0:
                        self.menu = max_length-1
                    
                    pass
                elif self.target == "ENEMY_LINE":
                    #not necessary
                    pass
                elif self.target == "ENEMY_BOX":

                    self.menu -= 1

                    if self.menu < 0:
                        if front_length > 3:
                            self.menu = 2
                        elif front_length == 2:
                            self.menu = 1
                        elif front_length == 1:
                            self.menu = 0
                    pass
                elif self.target == "ENEMY_ALL":
                    #not necessary
                    pass
            elif self.party_select:
                if self.target == "PARTY_ONE":
                    self.menu-=1
                    if self.menu < 0:
                        self.menu = len(game_self.party.member)-1
        
        #moves the cursor down
        elif event.type == KEYDOWN and event.key == K_DOWN:
            if self.enemy_select:
                if self.target == "ENEMY_ONE" or self.target == "ENEMY_GROUP":
                    self.menu+=1
                    if self.menu == 4 or self.menu == front_length:
                        self.menu = 0
                    if self.menu == 8 or self.menu == 4+back_length:
                        self.menu = 4
                        
                elif self.target == "ENEMY_ROW":
                    max_length = 0
                    if front_length > back_length:
                        max_length = front_length
                    else:
                        max_length = back_length

                    self.menu += 1

                    if self.menu > max_length-1:
                        self.menu = 0
                    
                    pass
                elif self.target == "ENEMY_LINE":
                    #not necessary
                    pass
                elif self.target == "ENEMY_BOX":

                    self.menu += 1

                    if self.menu > front_length-2:
                        self.menu = 0
                        
                elif self.target == "ENEMY_ALL":
                    #not necessary
                    pass
            elif self.party_select:
                if self.target == "PARTY_ONE":
                    self.menu+=1
                    if self.menu > len(game_self.party.member)-1:
                        self.menu = 0
                #party self and all cannot move so do nothing


                
        #moves the cursor left
        elif event.type == KEYDOWN and event.key == K_LEFT:
            if self.enemy_select:
                if self.target == "ENEMY_ONE" or self.target == "ENEMY_GROUP":

                    if self.menu > 3:
                        self.menu-=4

                        if self.menu > front_length-1:
                            self.menu = front_length-1
                    else:
                        self.menu+=4
                        if back_length == 0:
                            self.menu -=4

                        if self.menu > back_length+4:
                            self.menu = back_length+4
                    pass
                elif self.target == "ENEMY_ROW":
                    #not necessary
                    pass
                elif self.target == "ENEMY_LINE":
                    self.menu -= 1

                    if self.menu < 0:
                        self.menu = 1
                    pass
                elif self.target == "ENEMY_BOX":
                    #not necessary
                    pass
                elif self.target == "ENEMY_ALL":
                    #not necessary
                    pass 
            elif self.party_select:
                #not necessary
                pass

        
        #moves the cursor right
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            if self.enemy_select:
                if self.target == "ENEMY_ONE" or self.target == "ENEMY_GROUP":

                    if self.menu > 3:
                        self.menu -= 4

                        if self.menu > front_length-1:
                            self.menu = front_length-1

                    else:
                        self.menu += 4

                        if back_length == 0:
                            self.menu -=4
                            
                        
                        if self.menu > back_length+4:
                            self.menu = back_length+4

                elif self.target == "ENEMY_ROW":
                    #not necessary
                    pass
                elif self.target == "ENEMY_LINE":

                    self.menu += 1
                    if self.menu > 1:
                        self.menu = 0
                    pass
                elif self.target == "ENEMY_BOX":
                    #not necessary
                    pass
                elif self.target == "ENEMY_ALL":
                    #not necessary
                    pass
            elif self.party_select:
                #not necessary
                pass

        elif event.type == KEYDOWN and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
            #need to determine menu or battle and if battle, add it to command
            if self.enemy_select:
                if game_self.dungeon != None and ((self.level < 7 and self.character.magician_mp[self.level] > 0) or (self.level >= 7 and self.character.priest_mp[self.level-7] > 0)):
                    if self.level >=7:
                        self.level+=1
                    game_self.dungeon.battle.party_movement.append( battle_command.Battle_command( self.character, game_self.dungeon.battle.MAGIC, self.menu, self.target, self.level, self.magic_number, None))
                    game_self.dungeon.battle.selected += 1

                    #need to close magic window
                    game_self.dungeon.battle.magic_window = None

                #menu won't have any enemy
                if game_self.menu != None:
                    pass
                
            elif self.party_select:
                
                if game_self.dungeon != None and ((self.level < 7 and self.character.magician_mp[self.level] > 0) or (self.level >= 7 and self.character.priest_mp[self.level-7] > 0)):
                    if self.level >= 7:
                        self.level+=1
                    game_self.dungeon.battle.party_movement.append( battle_command.Battle_command( self.character, game_self.dungeon.battle.MAGIC, self.menu, self.target, self.level, self.magic_number, None))
                    game_self.dungeon.battle.selected += 1

                    #need to close magic window
                    game_self.dungeon.battle.magic_window = None

                if game_self.menu != None and ((self.level < 7 and self.character.magician_mp[self.level] > 0) or (self.level >= 7 and self.character.priest_mp[self.level-7] > 0)):

                    if self.level >= 7:
                        self.level += 1

                    if self.level == 8 and self.magic_number == 0:
                        heal = random.randint(1,8)
                        game_self.party.member[self.menu].hp += heal
                        if game_self.party.member[self.menu].hp > game_self.party.member[self.menu].max_hp:
                            game_self.party.member[self.menu].hp = game_self.party.member[self.menu].max_hp
                        self.character.priest_mp[self.level-8] -= 1
                        pass
                    elif self.level == 8 and self.magic_number == 1:

                        for chara in game_self.party.member:
                            if chara.status[3] == 1:
                                chara.status[3] = 0

                        self.character.priest_mp[self.level-8] -= 1

                    elif self.level == 9 and self.magic_number == 1:

                        for chara in game_self.party.member:
                            if chara.face_shield == 0:
                                chara.permanant_ac -= 2
                                chara.face_shield = 1

                        self.character.priest_mp[1] -= 1

                    elif self.level == 9 and self.magic_number == 3:
                        
                        if game_self.party.member[self.menu].status[0] == 1:
                            game_self.party.member[self.menu].status[0] = 0

                        self.character.priest_mp[1] -= 1
                        

                    elif self.level == 10 and self.magic_number == 0:
                        
                        if game_self.party.member[self.menu].status[4] == 1:
                            game_self.party.member[self.menu].status[4] = 0

                        self.character.priest_mp[2] -= 1

                    elif self.level == 10 and self.magic_number == 2:

                        for chara in game_self.party.member:
                            heal = random.randint(2,16)
                            chara.hp += heal
                            if chara.hp > chara.max_hp:
                                chara.hp = chara.max_hp

                        self.character.priest_mp[2] -= 1
                        
                    elif self.level == 10 and self.magic_number == 3:

                        heal = random.randint(8,32)
                        game_self.party.member[self.menu].hp += heal
                        if game_self.party.member[self.menu].hp > game_self.party.member[self.menu].max_hp:
                            game_self.party.member[self.menu].hp = game_self.party.member[self.menu].max_hp
                        self.character.priest_mp[2] -= 1
                        
                        pass

                    if self.level >= 7:
                        self.level -=1
                    pass

            #not needed anymore?
            elif self.dungeon_select:
                if game_self.dungeon != None and ((self.level < 8 and self.character.magician_mp[self.level] > 0) or (self.level >= 8 and self.character.priest_mp[self.level-7] > 0)):
                    if self.level >= 7:
                        self.level += 1
                    game_self.dungeon.battle.party_movement.append( battle_command.Battle_command( self.character, game_self.dungeon.battle.MAGIC, self.menu, self.target, self.level, self.magic_number, None))
                    game_self.dungeon.battle.selected += 1

                    #need to close magic window
                    game_self.dungeon.battle.magic_window = None

                if game_self.menu != None and (self.level < 8 and self.character.magician_mp[self.level] > 0): #and game_self.magic_data[self.level*6+1+self.magic_number][4] == "\"CAMP\"":
                    #magician magic functionality here
                    pass
                elif game_self.menu != None and (self.level >= 8 and self.character.priest_mp[self.level-7] > 0): #and game_self.magic_data[(self.level-7)*6+50+self.magic_number][4] == "\"CAMP\"":
                    #priest magic functionality here
                    pass

            if game_self.dungeon != None:
                #set next character's initial command
                next_character = None
                if game_self.dungeon.battle.selected >= len(game_self.party.member):
                    next_character = game_self.party.member[0]
                else:
                    next_character = game_self.party.member[ game_self.dungeon.battle.selected ]

                #if next character can attack the enemy set command to FIGHT, otherwise set it to DEFEND
                check = battle.character_attackable ( game_self, next_character )

                if check == True:
                    game_self.dungeon.battle.menu = game_self.dungeon.battle.FIGHT
                else:
                    game_self.dungeon.battle.menu = game_self.dungeon.battle.DEFEND
               
      



            #if all command is set for party move to battle 
            if game_self.dungeon != None and game_self.dungeon.battle.selected == battle.player_count_movable(game_self.party.member):
                game_self.dungeon.battle.state = battle.Battle.BATTLE

                game_self.dungeon.battle.enemy_movement = battle.enemy_movement( game_self.dungeon.battle.enemyList, game_self.dungeon.battle.enemyListBack, game_self)

                for element in game_self.dungeon.battle.party_movement:
                    game_self.dungeon.battle.total_movement.append(element)
                for element in game_self.dungeon.battle.enemy_movement:
                    game_self.dungeon.battle.total_movement.append(element)

                #sort the elements by speed, highest first
                game_self.dungeon.battle.total_movement.sort(cmp=lambda x, y: cmp(x.speed,y.speed), reverse=True)                




      
class Target_select(window.Window):

    USE_ITEM = 0
    PASS_ITEM = 1

    def __init__(self, rectangle, instruction):

        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.menu = 0

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.instruction = instruction

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.top_font = self.menu_font.render( u"誰に使いますか？", True, COLOR_WHITE) 

    def update(self):
        pass
    def draw(self, screen, game_self):

        if self.is_visible == False: return
        
        window.Window.draw(self, screen)

        screen.blit( self.top_font, (self.centerx - self.top_font.get_width()/2, self.top+20))

        #draw the box on item selected
        if game_self.party.member != []:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+55 + 30*self.menu,(self.right-self.left)-8,30), 0)


        i = 0
        for character in game_self.party.member:            
            name_font = self.menu_font.render( character.name, True, COLOR_WHITE)
            screen.blit ( name_font, (self.centerx - name_font.get_width()/2, self.top+60+i*30))
            i += 1

    def target_select_handler(self, event, game_self):

        #moves back to shop
        if event.type == KEYDOWN and event.key == K_x:
            game_self.cancel_se.play()
            self.menu = 0
            self.is_visible =False

        #moves the cursor up
        elif event.type == KEYDOWN and event.key == K_UP:
            game_self.cursor_se.play()
            self.menu -= 1
            if self.menu < 0:
                self.menu = 0
                
        #moves the cursor down
        elif event.type == KEYDOWN and event.key == K_DOWN:
            game_self.cursor_se.play()
            self.menu += 1
            if self.menu+1 > len(game_self.party.member):
                self.menu = len(game_self.party.member)-1


        elif event.type == KEYDOWN and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):

            if self.instruction == self.USE_ITEM:
                user = game_self.party.member[game_self.menu.item_window.menu]
                use_item = user.items[game_self.menu.item_window.item_view.menu]
                target = game_self.party.member[self.menu]

                #use_item.mp_cure

                if use_item.hp_cure > 0:
                    hp_cure = random.randint(1, use_item.hp_cure)
                    target.hp += hp_cure
                    if target.hp > target.max_hp:
                        target.hp = target.max_hp

                if use_item.status_cure > 0:
                    if use_item.status_cure == 1:
                        if target.status[0] == 1:
                            target.status[0] = 0
                    if use_item.status_cure == 2:
                        if target.status[4] == 1:
                            target.status[4] = 0

                del user.items[game_self.menu.item_window.item_view.menu]

                if game_self.menu.item_window.item_view.menu > len(user.items)-1:
                    game_self.menu.item_window.item_view.menu -= 1

                self.menu = 0
                self.is_visible = False
                game_self.menu.item_window.item_view.item_todo_window.is_visible = False

            if self.instruction == self.PASS_ITEM:
                user = game_self.party.member[game_self.menu.item_window.menu]
                use_item = user.items[game_self.menu.item_window.item_view.menu]
                target = game_self.party.member[self.menu]

                #if length is less than max, it is able to pass
                if len(target.items) < 10:
                    target.items.append(use_item)
                    del user.items[game_self.menu.item_window.item_view.menu]
                    game_self.menu.item_window.item_view.item_todo_window.is_visible = False
                    self.menu = 0
                    self.is_visible = False
                else:
                    #item is full, do nothing
                    #need to show window that item is full
                    self.menu = 0
                    self.is_visible = False

                if game_self.menu.item_window.item_view.menu > len(user.items)-1:
                    game_self.menu.item_window.item_view.menu -= 1

                game_self.menu.item_window.item_view.item_todo_window.menu = 0


                    
               
                pass
            

class Item_menu_select(window.Window):

    MENU_MAX = 4
    USE_ITEM, EQUIP_ITEM, LOOK_ITEM, PASS_ITEM, TRASH_ITEM = 0, 1, 2, 3, 4

    def __init__(self, rectangle):

        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.menu = 0

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.use_font = self.menu_font.render( u"アイテムを使う", True, COLOR_WHITE) 
        self.equip_font = self.menu_font.render( u"アイテムを装備する", True, COLOR_WHITE) 
        self.look_font = self.menu_font.render( u"アイテムを見る", True, COLOR_WHITE) 
        self.pass_font = self.menu_font.render( u"アイテムを渡す", True, COLOR_WHITE) 
        self.trash_font = self.menu_font.render( u"アイテムを捨てる", True, COLOR_WHITE) 

        self.use_target_window = Target_select(Rect(170, 50, 400, 240), 0)
        self.pass_target_window = Target_select(Rect(170, 50, 400, 240), 1)

        self.key_unlocked_window = None

        self.item_description_window = None
        
    def update(self):
        pass
    def draw(self, screen, game_self):

        if self.is_visible == False: return
        
        window.Window.draw(self, screen)

        
        pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+15 + 30*self.menu,(self.right-self.left)-8,30), 0)



        screen.blit( self.use_font, (self.centerx - self.use_font.get_width()/2, self.top+20))
        screen.blit( self.equip_font, (self.centerx - self.equip_font.get_width()/2, self.top+50))
        screen.blit( self.look_font, (self.centerx - self.look_font.get_width()/2, self.top+80))
        screen.blit( self.pass_font, (self.centerx - self.pass_font.get_width()/2, self.top+110))
        screen.blit( self.trash_font, (self.centerx - self.trash_font.get_width()/2, self.top+140))


        self.use_target_window.draw( screen, game_self)
        self.pass_target_window.draw(screen,game_self)

        if self.key_unlocked_window != None:
            self.key_unlocked_window.draw(screen)

        if self.item_description_window != None:
            character = game_self.party.member[game_self.menu.item_window.menu]
            self.item_description_window.draw(screen, game_self, character)
         

    def item_menu_select_handler(self, event, game_self):

        character = game_self.party.member[game_self.menu.item_window.menu]


        if self.use_target_window.is_visible == True:
            self.use_target_window.target_select_handler( event, game_self)
            return
        elif self.pass_target_window.is_visible == True:
            self.pass_target_window.target_select_handler( event, game_self)
            return
        elif self.key_unlocked_window != None and self.key_unlocked_window.is_visible == True:
            self.key_unlocked_window.donate_finish_window_handler(event, game_self)
            return
        elif self.item_description_window != None and self.item_description_window.is_visible == True:
            self.item_description_window.item_view_window_handler(game_self,event, character)
            return
    
        
        if event.type == KEYDOWN and event.key == K_x:
            game_self.cancel_se.play()
            self.menu = 0
            self.is_visible =False

        #moves the cursor up
        elif event.type == KEYDOWN and event.key == K_UP:
            game_self.cursor_se.play()
            self.menu -= 1
            if self.menu < 0:
                self.menu = 0
                
        #moves the cursor down
        elif event.type == KEYDOWN and event.key == K_DOWN:
            game_self.cursor_se.play()
            self.menu += 1
            if self.menu > self.MENU_MAX:
                self.menu = self.MENU_MAX


        elif event.type == KEYDOWN and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):

            character = game_self.party.member[game_self.menu.item_window.menu]
            use_item = character.items[game_self.menu.item_window.item_view.menu]


            if self.menu == self.USE_ITEM:
                #if category is 100, it means it needs to select target (for party member)
                if use_item.category == 100:
                    self.use_target_window.is_visible = True
                #if category is 101, no target selection is needed
                #item like torches
                elif use_item.category == 101:
                    game_self.party.torch += 30
                    if game_self.party.torch > 128:
                        game_self.party.torch = 128
                    del character.items[game_self.menu.item_window.item_view.menu]
                    pass

                #keys
                elif use_item.category == 250:
                    if game_self.party.member[0].coordinate == [ 9, 10 ,1] or game_self.party.member[0].coordinate == [ 9, 9, 1]:
                        #dungeon is None in menu so change in temp of game_Self
                        game_self.horizontal_wall_temp[10][9] = 2
                        #need to show that key matched
                        self.key_unlocked_window = Donate_finish_window(Rect(150,160,300,50), Donate_finish_window.KEY_UNLOCK)
                        self.key_unlocked_window.is_visible = True
                    if game_self.party.member[0].coordinate == [ 7, 1 ,2] or game_self.party.member[0].coordinate == [ 7, 0, 2]:
                        #dungeon is None in menu so change in temp of game_Self
                        game_self.horizontal_wall_temp[1][7] = 2
                        #need to show that key matched
                        self.key_unlocked_window = Donate_finish_window(Rect(150,160,300,50), Donate_finish_window.KEY_UNLOCK)
                        self.key_unlocked_window.is_visible = True
                         
                else:
                    #not able to use in menu
                    pass
                self.menu = 0

                if game_self.menu.item_window.item_view.menu > len(character.items)-1:
                    game_self.menu.item_window.item_view.menu -= 1


            if self.menu == self.EQUIP_ITEM:

                
                #weapon
                if use_item.category == 1:
                    if character.job == 0:
                        if isinstance(character.equip[0], item.Item):
                            character.items.append(character.equip[0])
                            character.equip[0] = use_item
                        else:
                            character.equip[0] = use_item
                        del character.items[game_self.menu.item_window.item_view.menu]

                if use_item.category == 2:
                    if character.job == 1:
                        if isinstance(character.equip[0], item.Item):
                            character.items.append(character.equip[0])
                            character.equip[0] = use_item
                        else:
                            character.equip[0] = use_item
                        del character.items[game_self.menu.item_window.item_view.menu]

                if use_item.category == 3:
                    if character.job == 2 or character.job == 3:
                        if isinstance(character.equip[0], item.Item):
                            character.items.append(character.equip[0])
                            character.equip[0] = use_item
                        else:
                            character.equip[0] = use_item
                        del character.items[game_self.menu.item_window.item_view.menu]

                if use_item.category == 4:
                    if character.job == 5:
                        if isinstance(character.equip[0], item.Item):
                            character.items.append(character.equip[0])
                            character.equip[0] = use_item
                        else:
                            character.equip[0] = use_item
                        del character.items[game_self.menu.item_window.item_view.menu]

                if use_item.category == 5:
                    if character.job == 4:
                        if isinstance(character.equip[0], item.Item):
                            character.items.append(character.equip[0])
                            character.equip[0] = use_item
                        else:
                            character.equip[0] = use_item
                        del character.items[game_self.menu.item_window.item_view.menu]


                #shield
                if use_item.category == 30:
                    if isinstance(character.equip[1], item.Item):
                        character.items.append(character.equip[1])
                        character.equip[1] = use_item
                    else:
                        character.equip[1] = use_item
                    del character.items[game_self.menu.item_window.item_view.menu]

                #armor
                if use_item.category == 60:
                    if isinstance(character.equip[2], item.Item):
                        character.items.append(character.equip[2])
                        character.equip[2] = use_item
                    else:
                        character.equip[2] = use_item
                    del character.items[game_self.menu.item_window.item_view.menu]
                        
                #helmet
                if use_item.category == 90:
                    if isinstance(character.equip[3], item.Item):
                        character.items.append(character.equip[3])
                        character.equip[3] = use_item
                    else:
                        character.equip[3] = use_item
                    del character.items[game_self.menu.item_window.item_view.menu]

                #gauntlet
                if use_item.category == 120:
                    if isinstance(character.equip[4], item.Item):
                        character.items.append(character.equip[4])
                        character.equip[4] = use_item
                    else:
                        character.equip[4] = use_item
                    del character.items[game_self.menu.item_window.item_view.menu]

                #accessory
                if use_item.category == 150:
                    if isinstance(character.equip[5], item.Item):
                        character.items.append(character.equip[5])
                        character.equip[5] = use_item
                    else:
                        character.equip[5] = use_item
                    del character.items[game_self.menu.item_window.item_view.menu]

                if game_self.menu.item_window.item_view.menu >= len(character.items):
                    game_self.menu.item_window.item_view.menu -= 1
                    if game_self.menu.item_window.item_view.menu < 0:
                        game_self.menu.item_window.item_view.menu = 0

                self.is_visible = False
                self.menu = 0
                
            if self.menu == self.LOOK_ITEM:
                self.item_description_window = item_view.Item_view(Rect(Rect(20, 20, 600, 440)))
                self.item_description_window.is_visible = True
                pass
            if self.menu == self.PASS_ITEM:
                self.pass_target_window.is_visible = True
            if self.menu == self.TRASH_ITEM:
                del character.items[game_self.menu.item_window.item_view.menu]
                self.menu = 0
                self.is_visible = False
                
                if game_self.menu.item_window.item_view.menu > len(character.items)-1:
                    game_self.menu.item_window.item_view.menu -= 1

                
