#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window
import rest

import save
import shop_window
import item


COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
HOUSE = 11

class System_notify_window(window.Window):

    SHARE, DONATE, CURSE, PAY, REST = 0, 1, 2, 3, 4
    SELL = 5
    ITEM_OUT, ITEM_IN = 6, 7
    
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

        self.item_hold_window = Item_select_window( Rect(120, 50, 400, 360), 0)
        self.item_receive_window = Item_select_window( Rect(120, 50, 400, 360), 1) 

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

            if self.instruction == self.DONATE or self.instruction == self.CURSE or self.instruction == self.PAY or self.instruction == self.REST or self.instruction == self.SELL:

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

        
        
        if self.instruction == self.SHARE:        
            if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
                self.is_visible = False

        elif self.instruction == self.DONATE or self.instruction == self.CURSE or self.instruction == self.PAY or self.instruction == self.REST or self.instruction == self.SELL or self.instruction == self.ITEM_OUT or self.instruction == self.ITEM_IN:
            
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
                    if game_self.party.member[self.menu].money > 0:#10000:
                        game_self.party.house = 1
                        game_self.party.member[self.menu].money -= 0#10000
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
                    
        elif self.instruction == self.TOO_MUCH_ITEM or self.instruction == self.SOLD_ITEM:
            if event.type == KEYUP and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False

        elif self.instruction == self.BUY_ITEM:
            if event.type == KEYUP and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False
                if game_self.shop.shop_window.buy_window.character_select.no_more == 1:
                    game_self.shop.shop_window.buy_window.character_select.is_visible = False


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

