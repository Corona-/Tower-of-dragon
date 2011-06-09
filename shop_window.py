#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window
import system_notify

import character_view
import item
import shop

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
NO_EXTRA, CHARACTER_VIEW, PARTY_REMOVE, CHARACTER_CHECK = 100, 101, 102, 103


SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_BLACK = (0,0,0)
COLOR_GLAY = (128,128,128)
COLOR_WHITE = (255,255,255)


class Shop_window(window.Window):

    SWORD, KATANA, BLUNT, GUN, THROW = 0, 1, 2, 3, 4
    SHIELD, ARMOR, HELMET, GAUNTLET, ACCESSORY = 5, 6, 7, 8, 9
    ITEM = 10

    MENU_MAX = 10
    
    def __init__(self, rectangle):

        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.menu = 0

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)


        self.top_font = self.menu_font.render( u"何が欲しいんだい？", True, COLOR_WHITE)

        self.sword_font = self.menu_font.render( u"剣", True, COLOR_WHITE)
        self.katana_font = self.menu_font.render( u"刀", True, COLOR_WHITE)
        self.blunt_font = self.menu_font.render( u"鈍器", True, COLOR_WHITE)
        self.gun_font = self.menu_font.render( u"銃", True, COLOR_WHITE)
        self.throw_font = self.menu_font.render( u"投擲", True, COLOR_WHITE)       
        self.shield_font = self.menu_font.render( u"盾", True, COLOR_WHITE)       
        self.armor_font = self.menu_font.render( u"鎧", True, COLOR_WHITE)
        self.helmet_font = self.menu_font.render( u"兜", True, COLOR_WHITE)
        self.gauntlet_font = self.menu_font.render( u"篭手", True, COLOR_WHITE)
        self.accessory_font = self.menu_font.render( u"アクセサリー", True, COLOR_WHITE)
        self.item_font = self.menu_font.render( u"アイテム", True, COLOR_WHITE)

        self.buy_window = Buy_window(Rect(120, 50, 400, 360))
        

    def draw( self, screen, game_self):
        """draw the shop window on screen"""

        if self.is_visible == False: return
        
        window.Window.draw(self, screen)

        screen.blit( self.top_font, ((self.centerx-self.top_font.get_width()/2), 60))
        

        if self.menu == self.SWORD:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(204, 95, 232, 30), 0)
        if self.menu == self.KATANA:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(204, 125, 232, 30), 0)
        if self.menu == self.BLUNT:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(204, 155, 232, 30), 0)
        if self.menu == self.GUN:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(204, 185, 232, 30), 0)
        if self.menu == self.THROW:           
            pygame.draw.rect(screen, COLOR_GLAY, Rect(204, 215, 232, 30), 0)
        if self.menu == self.SHIELD:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(204, 245, 232, 30), 0)
        if self.menu == self.ARMOR:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(204, 275, 232, 30), 0)
        if self.menu == self.HELMET:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(204, 305, 232, 30), 0)
        if self.menu == self.GAUNTLET:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(204, 335, 232, 30), 0)
        if self.menu == self.ACCESSORY:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(204, 365, 232, 30), 0)
        if self.menu == self.ITEM:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(204, 395, 232, 30), 0)


        screen.blit(self.sword_font, ((self.centerx-self.sword_font.get_width()/2), 100))
        screen.blit(self.katana_font, ((self.centerx-self.katana_font.get_width()/2), 130))
        screen.blit(self.blunt_font, ((self.centerx-self.blunt_font.get_width()/2), 160))
        screen.blit(self.gun_font, ((self.centerx-self.gun_font.get_width()/2), 190))
        screen.blit(self.throw_font, ((self.centerx-self.throw_font.get_width()/2), 220))
        screen.blit(self.shield_font, ((self.centerx-self.shield_font.get_width()/2), 250))
        screen.blit(self.armor_font, ((self.centerx-self.armor_font.get_width()/2), 280))
        screen.blit(self.helmet_font, ((self.centerx-self.helmet_font.get_width()/2), 310))
        screen.blit(self.gauntlet_font, ((self.centerx-self.gauntlet_font.get_width()/2), 340))
        screen.blit(self.accessory_font, ((self.centerx-self.accessory_font.get_width()/2), 370))
        screen.blit(self.item_font, ((self.centerx-self.item_font.get_width()/2), 400))


        #draw extra window
        self.buy_window.draw(screen, game_self)

    def shop_window_handler( self, event, game_self):

        if self.buy_window.is_visible == True:
            self.buy_window.buy_window_handler( event, game_self)
            return


        #moves the cursor up
        if event.type == KEYDOWN and event.key == K_UP:
            game_self.cursor_se.play()
            self.menu -= 1
            if self.menu < 0:
                self.menu = self.MENU_MAX
        #moves the cursor down
        elif event.type == KEYDOWN and event.key == K_DOWN:
            game_self.cursor_se.play()
            self.menu += 1
            if self.menu > self.MENU_MAX:
                self.menu = 0

        #moves back to shop
        elif event.type == KEYDOWN and event.key == K_x:
            game_self.cancel_se.play()
            self.menu = 0
            self.is_visible =False

        #select category to buy
        elif event.type == KEYDOWN and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
            self.buy_window.is_visible = True
 



class Buy_window(window.Window):

    SWORD, KATANA, BLUNT, GUN, THROW = 0, 1, 2, 3, 4
    SHIELD, ARMOR, HELMET, GAUNTLET, ACCESSORY = 5, 6, 7, 8, 9
    ITEM = 10

    MENU_MAX = 9

    def __init__(self, rectangle):

        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.menu = 0
        self.page = 0

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.top_font = self.menu_font.render( u"商品一覧:", True, COLOR_WHITE)

        self.category_item = []

        self.character_select = Character_select_window( Rect(100, 50, 440, 230))

    def draw( self, screen, game_self):
        """draw the shop window on screen"""

        if self.is_visible == False: return
        
        window.Window.draw(self, screen)

        screen.blit( self.top_font, (self.left + 20, self.top+20))

        selected = game_self.shop.shop_window.menu

        #show what is the category
        if selected == self.SWORD:
            category_font = self.menu_font.render( u"剣", True, COLOR_WHITE)
        if selected == self.KATANA:
            category_font = self.menu_font.render( u"刀", True, COLOR_WHITE)
        if selected == self.BLUNT:
            category_font = self.menu_font.render( u"鈍器", True, COLOR_WHITE)
        if selected == self.GUN:
            category_font = self.menu_font.render( u"銃", True, COLOR_WHITE)            
        if selected == self.THROW:
            category_font = self.menu_font.render( u"投擲", True, COLOR_WHITE)            

        if selected == self.SHIELD:
            category_font = self.menu_font.render( u"盾", True, COLOR_WHITE)
        if selected == self.ARMOR:
            category_font = self.menu_font.render( u"鎧", True, COLOR_WHITE)
        if selected == self.HELMET:
            category_font = self.menu_font.render( u"兜", True, COLOR_WHITE)
        if selected == self.GAUNTLET:
            category_font = self.menu_font.render( u"篭手", True, COLOR_WHITE)
        if selected == self.ACCESSORY:
            category_font = self.menu_font.render( u"アクセサリー", True, COLOR_WHITE)

        if selected == self.ITEM:
            category_font = self.menu_font.render( u"アイテム", True, COLOR_WHITE)
        
        
        screen.blit( category_font, (self.left + 20 + self.top_font.get_width(), self.top+20))


        #store the item in the shop and quantity of it
        item_data = game_self.item_data
        
        #category item is the array of selected category items
        self.category_item = game_self.shop.stock[selected]

        #draw the box on item selected
        if self.category_item != []:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+55 + 30*self.menu,(self.right-self.left)-8,30), 0)

        #draws the item 10 at a time in the page
        i = 0
        for item in self.category_item[self.page*10:(self.page+1)*10]:
            item_font = item_data[item.id][0].strip("\"")
            item_font = unicode(item_font, encoding="sjis")
            item_font = self.menu_font.render( item_font, True, COLOR_WHITE)
            screen.blit( item_font, (self.left + 20, self.top+60+i*30))
            cost_font = self.menu_font.render( item_data[item.id][2] + "TG", True, COLOR_WHITE)
            screen.blit( cost_font, (self.right - 20 - cost_font.get_width(), self.top+60+i*30))
                        
            i+=1


        self.character_select.draw( screen, game_self)

        
    def buy_window_handler(self, event, game_self):

        if self.character_select.is_visible == True:
            self.character_select.character_select_handler( event, game_self)
            return


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
            if len(self.category_item) > self.menu+self.page*10+1:
                self.menu += 1
                if self.menu > self.MENU_MAX:
                    self.menu = self.MENU_MAX


        #moves the cursor down
        elif event.type == KEYDOWN and event.key == K_LEFT:
            game_self.cursor_se.play()
            if self.page > 0:
                self.page-= 1
                self.menu = 0

        #moves the cursor down
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            game_self.cursor_se.play()
            if len(self.category_item) > (self.page+1)*10:
                self.page += 1
                self.menu = 0


        #moves the cursor down
        elif event.type == KEYDOWN and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
            if len(self.category_item) > 0:
                game_self.select_se.play()
                self.character_select.is_visible = True


class Sell_window(window.Window):

    MENU_MAX = 9

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

        self.sold_item_window = system_notify.Donate_finish_window( Rect(150, 160 ,300, 50), 6)



    def draw( self, screen, character):
        """draw the shop window on screen"""

        if self.is_visible == False: return
        
        window.Window.draw(self, screen)

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
            screen.blit ( item_font, (self.left+20, self.top+60+i*30))
            cost_font = self.menu_font.render( str(item.price/2) + "TG", True, COLOR_WHITE)
            screen.blit( cost_font, (self.right-20 - cost_font.get_width(), self.top+60+i*30))

            i += 1


        self.sold_item_window.draw(screen)

    def character_sell_window_handler( self, event, game_self):

        if self.sold_item_window.is_visible == True:
            self.sold_item_window.donate_finish_window_handler( event, game_self)
            return

        character = game_self.party.member[game_self.shop.sell_window.menu]

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
            if len(character.items) > self.menu+1:
                self.menu += 1
                if self.menu > self.MENU_MAX:
                    self.menu = self.MENU_MAX

        elif event.type == KEYDOWN and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
            if len(character.items) > 0:
                self.sold_item_window.is_visible = True
                money = character.items[self.menu].price
                #if not_found is 100, it means that there was no item with that id so add new one
                not_found = shop_item_change( character.items[self.menu].id , game_self, 0)
                if not_found == 100:
                    add_new_shop_item( character.items[self.menu].id, game_self )
                #delete character's items and adjust money
                del character.items[self.menu]
                character.money += (money/2)
                if self.menu+1 > len(character.items):
                    self.menu -= 1



class Character_select_window(window.Window):

    def __init__(self, rectangle):

        window.Window.__init__(self, rectangle)
        self.is_visible = False
        
        self.menu = 0

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        #if there is no more item left in stock
        self.no_more = 0


        self.top_font = self.menu_font.render( u"誰が買いますか？", True, COLOR_WHITE)

        self.status = character_view.Status_view_window( Rect(20,20,600, 440))
        self.buy_window = system_notify.Donate_finish_window( Rect(150, 160 ,300, 50), 4)
        self.not_enough_window = system_notify.Donate_finish_window( Rect(150, 160 ,300, 50), 0)
        self.too_much_item_window = system_notify.Donate_finish_window( Rect(150, 160 ,300, 50), 5)
        self.not_movable = system_notify.Donate_finish_window( Rect(150,160,300,50), system_notify.Donate_finish_window.TEMPLE_NOT_MOVABLE)
        
                

    def draw(self, screen, game_self):

        if self.is_visible == False: return
        
        window.Window.draw(self, screen)
      

        screen.blit( self.top_font, ( self.centerx - self.top_font.get_width()/2 , self.top+20))

        
        #draw the box on item selected
        if game_self.party.member != []:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+45 + 30*self.menu,(self.right-self.left)-8,30), 0)



        i = 0
        for character in game_self.party.member:
            character_font = self.menu_font.render( character.name, True, COLOR_WHITE)
            screen.blit(character_font, (self.left+20, self.top+50 + 30*i))
            money_font = self.menu_font.render( u"所持金：" + str(character.money) + "TG", True, COLOR_WHITE) 
            screen.blit(money_font, (self.right - 20 - money_font.get_width(), self.top+50 + 30*i))
            i+=1

        self.status.draw( screen, game_self.party.member)

        self.buy_window.draw( screen)
        self.not_enough_window.draw(screen)
        self.too_much_item_window.draw(screen)
        self.not_movable.draw(screen)

        
    def character_select_handler(self, event, game_self):

        if self.buy_window.is_visible == True:
            self.buy_window.donate_finish_window_handler( event, game_self)
            return
        elif self.not_enough_window.is_visible == True:
            self.not_enough_window.donate_finish_window_handler( event, game_self)
            return
        elif self.status.is_visible == True:
            self.status.status_view_window_handler( game_self, event, None)
            return
        elif self.too_much_item_window.is_visible == True:
            self.too_much_item_window.donate_finish_window_handler( event, game_self)
            return
        elif self.not_movable.is_visible == True:
            self.not_movable.donate_finish_window_handler( event, game_self)
            return

        length = len(game_self.party.member)-1

        #moves back to item window
        if event.type == KEYDOWN and event.key == K_x:
            game_self.cancel_se.play()
            self.menu = 0
            self.is_visible =False



        #moves the cursor up
        elif event.type == KEYDOWN and event.key == K_UP:
            game_self.cursor_se.play()
            self.menu -= 1
            self.status.menu -= 1
            if self.menu < 0:
                self.menu = length
                self.status.menu = length
                
        #moves the cursor down
        elif event.type == KEYDOWN and event.key == K_DOWN:
            game_self.cursor_se.play()
            self.menu += 1
            self.status.menu += 1
            if self.menu > length:
                self.menu = 0
                self.status.menu = 0

        #status view
        elif event.type == KEYDOWN and event.key == K_LSHIFT:
            game_self.cursor_se.play()
            self.status.is_visible = True

        #buy
        elif event.type == KEYDOWN and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
            game_self.select_se.play()

            #get the cost of the item
            category_item = game_self.shop.shop_window.buy_window.category_item
            item_menu = game_self.shop.shop_window.buy_window.menu

            if game_self.party.member[self.menu].status != [0,0,0,0,0,0,0,0,0]:
                self.not_movable.is_visible = True
            
            elif game_self.party.member[self.menu].money > int(game_self.item_data[category_item[item_menu].id][2]) and len(game_self.party.member[self.menu].items) < 10:
                game_self.party.member[self.menu].money -= int(game_self.item_data[category_item[item_menu].id][2])
                game_self.party.member[self.menu].items.append( item.Item( game_self.item_data[category_item[item_menu].id] ))

                self.no_more = shop_item_change( category_item[item_menu].id, game_self, 1)


                self.buy_window.is_visible = True

            elif game_self.party.member[self.menu].money < int(game_self.item_data[category_item[item_menu].id][2]):
                self.not_enough_window.is_visible = True
            elif len(game_self.party.member[self.menu].items) == 10:
                self.too_much_item_window.is_visible = True
          
#increase(0) or decrease(1) item
#if no item was found, it returns 100, else it returns 101
def shop_item_change( item_id, game_self, i ):

    found = 100 

    j = 0
    k = 0
    for item_array in game_self.shop.stock:
        for item in item_array:

            if i == 1:
                if item.id == item_id:
                    found = 101
                    #if stock is negative it has infinity stock
                    if item.stock < 0:
                        return found
                    item.stock -= 1
                    if item.stock == 0:
                        del game_self.shop.stock[j][k]
                        game_self.shop.shop_window.buy_window.menu -= 1
                        if game_self.shop.shop_window.buy_window.menu < 0:
                            game_self.shop.shop_window.buy_window.menu = 0
                        return 1
            else:
                if item.id == item_id:
                    item.stock += 1
                    found = 101
                    if item.stock > 9:
                        item.stock = 9
            k += 1
        j += 1
        k = 0

    return found



def add_new_shop_item( item_id, game_self ):

    item_id = int(item_id)
    
    new_item = shop.Shop_item( item_id, 1)

    if item_id < 100:
        game_self.shop.stock[10].append(new_item)
    elif item_id < 150:
        game_self.shop.stock[0].append(new_item)
    elif item_id < 200:
        game_self.shop.stock[1].append(new_item)        
    elif item_id < 250:
        game_self.shop.stock[2].append(new_item)        
    elif item_id < 300:
        game_self.shop.stock[3].append(new_item)        
    elif item_id < 350:
        game_self.shop.stock[4].append(new_item)        
    elif item_id < 400:
        game_self.shop.stock[5].append(new_item)        
    elif item_id < 450:
        game_self.shop.stock[6].append(new_item)        
    elif item_id < 500:
        game_self.shop.stock[7].append(new_item)
    elif item_id < 550:
        game_self.shop.stock[8].append(new_item)
    elif item_id < 600:
        game_self.shop.stock[9].append(new_item)
