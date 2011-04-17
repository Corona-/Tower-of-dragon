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

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
HOUSE = 11

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
        self.donate_window = Donate_window(Rect(150, 160 ,300, 150))
        self.inn_not_enough = Donate_finish_window(Rect(150, 160 ,300, 50), Donate_finish_window.NOT_ENOUGH)
        self.resting_window = Rest_window(Rect(100, 160 ,400, 50), Rest_window.REST)
        self.house_buy_message = Donate_finish_window(Rect(170, 160, 300, 50), Donate_finish_window.BUY_HOUSE)                
        self.house_reform_message = Donate_finish_window(Rect(170, 160, 300, 50), Donate_finish_window.REFORM_HOUSE)
        self.character_sell_window = shop_window.Sell_window(Rect(120, 50, 400, 360))
        self.collect_message = Donate_finish_window(Rect(150, 160, 300, 50), Donate_finish_window.COLLECT)


        self.item_hold_window = Item_select_window( Rect(120, 50, 400, 360), 0)
        self.item_receive_window = Item_select_window( Rect(120, 50, 400, 360), 1) 

        self.status_view = character_view.Status_view_window(Rect(20, 20, 600, 440))

        self.item_view = Item_view(Rect(120, 50, 400, 360))
        self.magic_all_view = Magic_all_view(Rect(80, 50, 280 ,120))

        self.temple_not_enough = Donate_finish_window(Rect(150,160,300,50), Donate_finish_window.TEMPLE_NOT_ENOUGH)
        self.temple_not_movable = Donate_finish_window(Rect(150,160,300,50), Donate_finish_window.TEMPLE_NOT_MOVABLE)
        self.temple_curing = temple_window.Curing_window(Rect(60, 40, 520, 400))
        self.cured = False

        
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
                    top_font = self.menu_font.render( u"誰のアイテムを使いますか？", True, COLOR_WHITE)      
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
                    self.donate_window.draw(screen, character[self.menu])
                    self.resting_window.draw(screen, character[self.menu])
                self.inn_not_enough.draw(screen)
                self.house_buy_message.draw(screen)
                self.house_reform_message.draw(screen)
                self.character_sell_window.draw(screen, character[self.menu]) 
                self.collect_message.draw(screen)
                self.temple_not_enough.draw(screen)
                self.temple_not_movable.draw(screen)

                self.status_view.draw(screen, character)

                if self.instruction == self.TEMPLE_PAY:
                    self.temple_curing.draw(screen, game_self)

                if self.instruction == self.USE_ITEM:
                    self.item_view.draw(screen, game_self)

                if self.instruction == self.USE_MAGIC:
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
                self.item_hold_window.draw(screen, game_self) 
                self.item_receive_window.draw(screen, game_self) 
                       



    def system_notify_window_handler(self, event, game_self, character):

        if self.donate_window.is_visible:
            self.donate_window.donate_window_handler(event, game_self, character[self.menu])
            return
        elif self.inn_not_enough.is_visible:
            self.inn_not_enough.donate_finish_window_handler(event, game_self)
            return
        elif self.resting_window.is_visible:
            self.resting_window.resting_window_handler(event, game_self)
            return
        elif self.house_buy_message.is_visible:
            self.house_buy_message.donate_finish_window_handler(event, game_self)
            return
        elif self.house_reform_message.is_visible:
            self.house_reform_message.donate_finish_window_handler(event, game_self)
            return
        elif self.character_sell_window.is_visible:
            self.character_sell_window.character_sell_window_handler( event, game_self)
            return
        elif self.item_hold_window.is_visible:
            self.item_hold_window.item_select_window_handler( event, game_self)
            return
        elif self.item_receive_window.is_visible:
            self.item_receive_window.item_select_window_handler( event, game_self)
            return
        elif self.collect_message.is_visible:
            self.collect_message.donate_finish_window_handler(event, game_self)
            return
        elif self.status_view.is_visible:
            self.status_view.status_view_window_handler(game_self, event, game_self.party.member)
            return
        elif self.item_view.is_visible:
            self.item_view.item_view_handler(event, game_self)
            return
        elif self.magic_all_view.is_visible:
            self.magic_all_view.magic_all_view_handler(event, game_self)
            return
        elif self.temple_not_enough.is_visible:
            self.temple_not_enough.donate_finish_window_handler(event, game_self)
            return
        elif self.temple_not_movable.is_visible:
            self.temple_not_movable.donate_finish_window_handler(event, game_self)
            return
        elif self.temple_curing.is_visible:
            self.temple_curing.curing_window_handler(event, game_self)
            return
        
        if self.instruction == self.SHARE:        
            if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
                self.is_visible = False

        elif self.instruction == self.DONATE or self.instruction == self.CURSE or self.instruction == self.PAY or self.instruction == self.REST or self.instruction == self.SELL or self.instruction == self.ITEM_OUT or self.instruction == self.ITEM_IN or self.instruction == self.COLLECT or self.instruction == self.USE_ITEM or self.instruction == self.USE_MAGIC or self.instruction == self.VIEW_STATUS or self.instruction == self.CHANGE_PARTY or self.instruction == self.TEMPLE_PAY:
            
            if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
                if self.instruction == self.DONATE:
                    if len(character) > 0:
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
                            game_self.house.house_change.who_pay_window.house_reform_message.is_visible = True
                        else:
                            self.inn_not_enough.is_visible = True
                        return
                    # buy a house with 10000                    
                    if game_self.party.member[self.menu].money > 10000:
                        game_self.party.house = 1
                        game_self.party.member[self.menu].money -= 10000
                        game_self.shop.buy_house.who_pay_window.house_buy_message.is_visible = True
                    else:
                        self.inn_not_enough.is_visible = True
                elif self.instruction == self.REST and len(game_self.party.member) > 0:
                    #get the item chosen to rest for and if money is not enough, open inn_not_enough window
                    #else check exp points and rests

                    if game_self.game_state == INN:
                        rest.rest(self, game_self, game_self.inn.inn_window.menu, 1)
                    elif game_self.game_state == HOUSE:
                        rest.rest(self, game_self, game_self.party.house, 0)                         
                        
                    if self.inn_not_enough.is_visible:
                        return

                    #check exp and lv up
                    rest.calc_exp_needed(self, game_self.party.member[self.menu])

                    change = [0,0,0,0,0,0,0,0]
                    #level up if next is negative
                    if game_self.party.member[self.menu].next > 0:
                        if game_self.game_state == INN:
                            rest.level_up(self, game_self.party.member[self.menu], game_self.inn.inn_window.menu, change)
                        elif game_self.game_state == HOUSE:
                            rest.level_up(self, game_self.party.member[self.menu], game_self.party.house, change)
                            

                        self.resting_window.get_change_status_values(change)
                        #show message of sleeping...
                        self.resting_window.is_visible = True
                        #show message for lv up                        
                    else:
                        self.resting_window.get_change_status_values(change)
                        #window to show next
                        #show message of sleeping...
                        self.resting_window.is_visible = True
                        pass
                    #print change

                elif self.instruction == self.SELL:
                    self.character_sell_window.is_visible = True
                elif self.instruction == self.ITEM_OUT:
                    self.item_hold_window.is_visible = True
                elif self.instruction == self.ITEM_IN:
                    self.item_receive_window.is_visible = True
                elif self.instruction == self.COLLECT:
                    self.collect_message.is_visible = True
                    total_money = 0
                    for character in game_self.party.member:
                        total_money += character.money
                        character.money = 0
                    game_self.party.member[self.menu].money = total_money
                elif self.instruction == self.USE_ITEM:
                    self.item_view.is_visible = True
                elif self.instruction == self.USE_MAGIC:
                    self.magic_all_view.is_visible = True
                elif self.instruction == self.VIEW_STATUS:
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
                    if game_self.party.member[self.menu].status == "OK":
                        temple_cure = game_self.temple.temple_cure_window
                        cure_character = temple_cure.to_cure[temple_cure.menu+temple_cure.page*10]
                        cost = 0
                        if cure_character.status == "PALSY":
                            cost = 100*cure_character.level
                        elif cure_character.status == "STONE":
                            cost = 200*cure_character.level
                        elif cure_character.status == "DEAD":
                            cost = 250*cure_character.level
                        elif cure_character.status == "ASHED":
                            cost = 500*cure_character.level

                        
                        if game_self.party.member[self.menu].money > cost:
                            game_self.party.member[self.menu].money-=cost

                            self.cured = False
                            if cure_character.status == "PALSY" or cure_character.status == "STONE":
                                self.cured = True
                            else:
                                probability = random.randint(1,100)
                                if probability <= 5:
                                    self.cured = True
                                else:
                                    self.cured = False

                            self.temple_curing.is_visible = True
                        else:
                            self.temple_not_enough.is_visible = True
                            pass
                    else:
                        self.temple_not_movable.is_visible = True
                        pass
                    pass
                        
                
                
            

            if event.type == KEYUP and event.key == K_x:
                self.menu = 0
                self.is_visible = False

            if event.type == KEYUP and event.key == K_UP:
                self.menu -= 1
                if self.menu < 0:
                    self.menu = len(character)-1

            if event.type == KEYUP and event.key == K_DOWN:
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
 

        if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
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
                    

            
        if event.type == KEYUP and event.key == K_x:
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

            
        elif event.type == KEYUP and event.key == K_LEFT:
            self.menu += 1
            if self.menu > 8:
                self.menu = 0
            
        elif event.type == KEYUP and event.key == K_RIGHT:
            self.menu -= 1
            if self.menu < 0:
                self.menu = 8

        #maybe want to clean up this... 
        elif event.type == KEYUP and event.key == K_UP:
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

        elif event.type == KEYUP and event.key == K_DOWN:
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
                


    def donate_finish_window_handler(self, event, game_self):
        if self.instruction == self.NOT_ENOUGH:          
            if event.type == KEYUP and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False
                #it is only used when buying a house and not enough money
                #it doesn't matter if it is not since it is initialized and should be false
                game_self.shop.buy_house.who_pay_window.is_visible = False
                game_self.shop.buy_house.who_pay_window.menu = 0
                game_self.shop.buy_house.is_visible = False

         
        elif self.instruction == self.FINISH:
            if event.type == KEYUP and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False

        elif self.instruction == self.BUY_HOUSE:
            if event.type == KEYUP and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False
                game_self.shop.buy_house.who_pay_window.is_visible = False
                game_self.shop.buy_house.is_visible = False
                #move the cursor to correct spot
                game_self.shop.menu += 1

        elif self.instruction == self.REFORM_HOUSE:
            if event.type == KEYUP and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False
                game_self.house.house_change.who_pay_window.is_visible = False
                game_self.house.house_change.is_visible = False
                #move the cursor to correct spot
                if game_self.party.house == 5:
                    game_self.house.menu += 1
                    
        elif self.instruction == self.TOO_MUCH_ITEM or self.instruction == self.SOLD_ITEM or self.instruction == self.COLLECT:
            if event.type == KEYUP and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False

        elif self.instruction == self.BUY_ITEM:
            if event.type == KEYUP and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False
                if game_self.shop.shop_window.buy_window.character_select.no_more == 1:
                    game_self.shop.shop_window.buy_window.character_select.is_visible = False
        elif self.instruction == self.TEMPLE_NOT_ENOUGH or self.instruction == self.TEMPLE_NOT_MOVABLE:
            if event.type == KEYUP and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False
            


class Rest_window(window.Window):

    REST = 0
    
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
            if event.type == KEYUP and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.lv_up_window.is_visible = True


    def get_change_status_values(self, change):
        self.change = change



class Confirm_window(window.Window):

    HOUSE, PAY  = 0, 1
    HOUSE_CHANGE = 10
    SAVE, LOAD = 100, 101
    JOB_CHANGE = 20


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
        
        if event.type == KEYUP and event.key == K_UP: #moves the cursor up
            self.menu -= 1
            if self.menu < 0:
                self.menu = self.MENU_MAX
        elif event.type == KEYUP and event.key == K_DOWN:
                self.menu += 1
                if self.menu > self.MENU_MAX:
                    self.menu = 0

        if event.type == KEYUP and event.key == K_x:
            self.menu = 0
            self.is_visible = False


        elif  event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
            if self.instruction == self.HOUSE:
                if self.menu == self.YES:
                    if len(game_self.party.member) > 0:
                        self.who_pay_window.is_visible = True
                else:
                    game_self.shop.buy_house.is_visible = False

            if self.instruction == self.HOUSE_CHANGE:
                if self.menu == self.YES:
                    if len(game_self.party.member) > 0:
                        self.who_pay_window.is_visible = True
                else:
                    game_self.house.house_change.is_visible = False
    
            if self.instruction == self.SAVE:
                if self.menu == self.YES:
                    save.save( self, game_self)
                    game_self.inn.save_confirm.is_visible = False
                    game_self.house.save_confirm.is_visible = False
                else:
                    game_self.inn.save_confirm.is_visible = False
                    game_self.house.save_confirm.is_visible = False
    
            if self.instruction == self.LOAD:
                if self.menu == self.YES:
                    save.load( self, game_self)
                    game_self.inn.load_confirm.is_visible = False
                    game_self.house.load_confirm.is_visible = False
                else:
                    game_self.inn.load_confirm.is_visible = False
                    game_self.house.load_confirm.is_visible = False

            if self.instruction == self.JOB_CHANGE:
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

        if event.type == KEYUP and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):

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
        if event.type == KEYUP and event.key == K_x:
            game_self.cancel_se.play()
            self.menu = 0
            self.page = 0
            self.is_visible =False

        #moves the cursor up
        elif event.type == KEYUP and event.key == K_UP:
            game_self.cursor_se.play()
            self.menu -= 1
            if self.menu < 0:
                self.menu = 0 
                
        #moves the cursor down
        elif event.type == KEYUP and event.key == K_DOWN:
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


        elif event.type == KEYUP and event.key == K_RIGHT:
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
                
        elif event.type == KEYUP and event.key == K_LEFT:
            if self.instruction == self.ITEM_IN:
                if self.page > 0:
                    game_self.cursor_se.play()
                    self.page -= 1
                    self.menu = 0


        elif event.type == KEYUP and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
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

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.top_font = self.menu_font.render( u"の持ち物:", True, COLOR_WHITE)

        self.target_window = Target_select(Rect(120, 50, 400, 240)) 

    def update(self):
        pass
    def draw(self, screen, game_self):

        if self.is_visible == False: return
        
        window.Window.draw(self, screen)

        character = game_self.party.member[game_self.menu.item_window.menu]

        name_font = self.menu_font.render( character.name, True, COLOR_WHITE)

        screen.blit( name_font, (self.left+20, self.top+20))
        screen.blit( self.top_font, (self.left+20+name_font.get_width(), self.top+20))

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

        self.target_window.draw( screen, game_self)
        
    def item_view_handler(self, event, game_self):

        if self.target_window.is_visible == True:
            self.target_window.target_select_handler( event, game_self)
            return

        character = game_self.party.member[game_self.menu.item_window.menu]

        #moves back to shop
        if event.type == KEYUP and event.key == K_x:
            game_self.cancel_se.play()
            self.menu = 0
            self.is_visible =False

        #moves the cursor up
        elif event.type == KEYUP and event.key == K_UP:
            game_self.cursor_se.play()
            self.menu -= 1
            if self.menu < 0:
                self.menu = 0
                
        #moves the cursor down
        elif event.type == KEYUP and event.key == K_DOWN:
            game_self.cursor_se.play()
            if len(character.items) > self.menu+1:
                self.menu += 1

        elif event.type == KEYUP and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
            if len(character.items) > 0:
                use_item = character.items[game_self.menu.item_window.item_view.menu]
                #if category is 100, it means it needs to select target
                if use_item.category == 100:
                    self.target_window.is_visible = True
                #if category is 101, no target selection is needed
                elif use_item.category == 101:
                    pass
                #else not able to use in menu
                else:
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

        character = game_self.party.member[game_self.menu.magic_window.menu]

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
        if event.type == KEYUP and event.key == K_x:
            game_self.cancel_se.play()
            self.menu = 0
            self.is_visible =False

        #moves the cursor up
        elif event.type == KEYUP and event.key == K_UP:
            game_self.cursor_se.play()
            self.menu -= 7
            if self.menu < 0:
                self.menu += 14
                
        #moves the cursor down
        elif event.type == KEYUP and event.key == K_DOWN:
            game_self.cursor_se.play()
            self.menu += 7
            if self.menu > 13:
                self.menu -= 14

                
        #moves the cursor left
        elif event.type == KEYUP and event.key == K_LEFT:
            game_self.cursor_se.play()
            self.menu -= 1
            if self.menu == 6:
                self.menu = 13
            if self.menu < 0:
                self.menu = 6
            
        #moves the cursor right
        elif event.type == KEYUP and event.key == K_RIGHT:
            game_self.cursor_se.play()
            self.menu += 1
            if self.menu == 7:
                self.menu = 0
            if self.menu > 13:
                self.menu = 7

        elif event.type == KEYUP and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
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

        #self.target_window = Target_select(Rect(120, 50, 400, 240)) 

    def update(self):
        pass
    def draw(self, screen, game_self):

        if self.is_visible == False: return
        
        window.Window.draw(self, screen)

        level = game_self.menu.magic_window.magic_all_view.menu
        character = game_self.party.member[game_self.menu.magic_window.menu]

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
                    if game_self.magic_data[level*6+1+i][4] == 1:
                        magic_font = self.menu_font.render( magic_font, True, COLOR_GLAY)    
                    else:
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
                    #the magic is only used in battle
                    if game_self.magic_data[(level-7)*6+50+i][4] == 1:
                        magic_font = self.menu_font.render( magic_font, True, COLOR_GLAY)    
                    else:
                        magic_font = self.menu_font.render( magic_font, True, COLOR_WHITE)
                    screen.blit( magic_font, (self.centerx - magic_font.get_width()/2, self.top+60+i*30))
                else:
                    magic_font = self.menu_font.render( "????????", True, COLOR_GLAY)
                    screen.blit( magic_font, (self.centerx - magic_font.get_width()/2, self.top+60+i*30))
                i+=1
                    
        
    def magic_level_view_handler( self, event, game_self):

        #moves back to shop
        if event.type == KEYUP and event.key == K_x:
            game_self.cancel_se.play()
            self.menu = 0
            self.is_visible =False

        #moves the cursor up
        elif event.type == KEYUP and event.key == K_UP:
            game_self.cursor_se.play()
            self.menu -= 1
            if self.menu < 0:
                self.menu = 0
                
        #moves the cursor down
        elif event.type == KEYUP and event.key == K_DOWN:
            game_self.cursor_se.play()
            self.menu += 1
            if self.menu > 5:
                self.menu = 5

                
        #moves the cursor left
        elif event.type == KEYUP and event.key == K_LEFT:
            game_self.cursor_se.play()
            game_self.menu.magic_window.magic_all_view.menu -= 1
            if game_self.menu.magic_window.magic_all_view.menu < 0:
                game_self.menu.magic_window.magic_all_view.menu = 6
            if game_self.menu.magic_window.magic_all_view.menu == 6:
                game_self.menu.magic_window.magic_all_view.menu = 13
            
        #moves the cursor right
        elif event.type == KEYUP and event.key == K_RIGHT:
            game_self.cursor_se.play()
            game_self.menu.magic_window.magic_all_view.menu += 1
            if game_self.menu.magic_window.magic_all_view.menu == 7:
                game_self.menu.magic_window.magic_all_view.menu = 0
            if game_self.menu.magic_window.magic_all_view.menu > 13:
                game_self.menu.magic_window.magic_all_view.menu = 7



      
class Target_select(window.Window):


    def __init__(self, rectangle):

        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.menu = 0

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

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
        if event.type == KEYUP and event.key == K_x:
            game_self.cancel_se.play()
            self.menu = 0
            self.is_visible =False

        #moves the cursor up
        elif event.type == KEYUP and event.key == K_UP:
            game_self.cursor_se.play()
            self.menu -= 1
            if self.menu < 0:
                self.menu = 0
                
        #moves the cursor down
        elif event.type == KEYUP and event.key == K_DOWN:
            game_self.cursor_se.play()
            self.menu += 1
            if self.menu+1 > len(game_self.party.member):
                self.menu = len(game_self.party.member)-1


        elif event.type == KEYUP and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):

            if game_self.menu.item_window.is_visible == True:
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
                        if target.status == "POISON":
                            target.status = "OK"
                    if use_item.status_cure == 2:
                        if target.status == "PALSY":
                            target.status = "OK"

                del user.items[game_self.menu.item_window.item_view.menu]

                if game_self.menu.item_window.item_view.menu > len(user.items)-1:
                    game_self.menu.item_window.item_view.menu -= 1

                self.menu = 0
                self.is_visible = False
