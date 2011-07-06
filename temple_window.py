#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window
import system_notify
import temple_window
import random

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
NO_EXTRA, CHARACTER_VIEW, PARTY_REMOVE, CHARACTER_CHECK = 100, 101, 102, 103


SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_BLACK = (0,0,0)
COLOR_GLAY = (128,128,128)
COLOR_WHITE = (255,255,255)

MENU_MAX = 2
class Temple_window(window.Window):

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

        self.top_font = self.menu_font.render( u"誰の治療をする？", True, COLOR_WHITE)

        #places character who needs a cure
        self.to_cure = []

        #extra window
        self.cure_pay_window = None #system_notify.System_notify_window(Rect(200,120,340, 240),system_notify.System_notify_window.TEMPLE_PAY) 

    def draw(self,screen, game_self):
        window.Window.draw(self, screen)        
        if self.is_visible == False: return
    
        screen.blit( self.top_font, (self.centerx - self.top_font.get_width()/2, self.top+20))

        if self.to_cure == []:
            for character in game_self.party.member:
                if character.status != [0,0,0,0,0,0,0,0,0]:
                    self.to_cure.append(character)
            for character in game_self.characters:
                if character.status != [0,0,0,0,0,0,0,0,0]:
                    self.to_cure.append(character)

        if self.to_cure != []:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+47+30*self.menu,(self.right-self.left)-8,25), 0)


        i = 0
        for chara in self.to_cure[self.page*10:(self.page+1)*10]:
            character_font = self.menu_font.render(chara.name, True, COLOR_WHITE)
            screen.blit(character_font, (self.left+20, self.top+50+(i%10)*30))

            if chara.status[4] == 1:
                cost_font = 25*chara.level
                status_font = self.menu_font.render( "PALSY", True, COLOR_WHITE)
            if chara.status[5] == 1:
                status_font = self.menu_font.render( "PETRIF", True, COLOR_WHITE)
                cost_font = 200*chara.level
            if chara.status[6] == 1:
                status_font = self.menu_font.render( "DEAD", True, COLOR_WHITE)
                cost_font = 250*chara.level
            if chara.status[7] == 1:
                status_font = self.menu_font.render( "ASHED", True, COLOR_WHITE)
                cost_font = 500*chara.level
            if chara.status == [0,0,0,0,0,0,0,0,0]:
                cost_font = 0

            screen.blit(status_font, (self.centerx-60, self.top+50+(i%10)*30))


            cost_font = self.menu_font.render( str(cost_font) + "TP", True, COLOR_WHITE)
            screen.blit(cost_font, (self.right-20-cost_font.get_width(), self.top+50+(i%10)*30))
            i = i + 1

        if self.cure_pay_window != None:
            self.cure_pay_window.draw(screen, game_self)
        

    def temple_window_handler(self, event, game_self):

        if self.cure_pay_window != None and self.cure_pay_window.is_visible == True:
            self.cure_pay_window.system_notify_window_handler( event, game_self, game_self.party.member)
            return
        
        if event.type == KEYDOWN and event.key == K_x:
            self.menu = 0
            self.page = 0
            self.is_visible = False
            self.to_cure = []

        if event.type == KEYDOWN and event.key == K_UP: #moves the cursor up
            self.menu -= 1
            if self.menu < 0:
                self.menu = 0
        elif event.type == KEYDOWN and event.key == K_DOWN:
            if len(self.to_cure) > self.menu+self.page*10+1:
                self.menu += 1
                if self.menu > self.MENU_MAX:
                    self.menu = self.MENU_MAX
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            if len(self.to_cure) > (self.page+1)*10:
                self.page += 1
                self.menu = 0
        elif event.type == KEYDOWN and event.key == K_LEFT:
            if self.page > 0:
                self.page -= 1
                self.menu = 0

        elif  event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
            if len(self.to_cure) == 0: return

            if self.to_cure[self.menu+self.page*10].status == [0,0,0,0,0,0,0,0,0]:
                bad_status = random.randint(1,100)
                if bad_status < 25:
                    self.to_cure[self.menu+self.page*10].status[4] = 1
                elif bad_status < 50:
                    self.to_cure[self.menu+self.page*10].status[5] = 1
                elif bad_status < 75:
                    self.to_cure[self.menu+self.page*10].status[6] = 1
                else:
                    self.to_cure[self.menu+self.page*10].status[7] = 1


            else:
                self.cure_pay_window = system_notify.System_notify_window(Rect(200,120,340, 240),system_notify.System_notify_window.TEMPLE_PAY) 
                self.cure_pay_window.is_visible = True


class Curing_window(window.Window):

    def __init__(self, rectangle):
        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.cure_font1 = self.menu_font.render( u"囁き", True, COLOR_WHITE)
        self.cure_font2 = self.menu_font.render( u"祈り", True, COLOR_WHITE)
        self.cure_font3 = self.menu_font.render( u"詠唱", True, COLOR_WHITE)
        self.cure_font4 = self.menu_font.render( u"念じろ！", True, COLOR_WHITE)

        self.success_font = self.menu_font.render( u"成功！", True, COLOR_WHITE)
        self.failed_font = self.menu_font.render( u"失敗！", True, COLOR_WHITE)

        self.alive_font = u"は生き返った！"
        self.good_font = u"は元気になった！"
        self.ashed_font = u"は灰になった！"
        self.lost_font = u"は埋葬されます"

        self.count = 0
        #0 to ok, 1 to ashed, 2 to lost
        self.status_change = -1

    def draw(self, screen, game_self):
        window.Window.draw(self, screen)        
        if self.is_visible == False: return

        screen.blit( self.cure_font1, (640/3 - self.cure_font1.get_width()/2, self.top+80))
        
        if self.count > 30:        
            screen.blit( self.cure_font2, (640*2/3 - self.cure_font2.get_width()/2, self.top+80))

        if self.count > 60:
            screen.blit( self.cure_font3, (640/3 - self.cure_font3.get_width()/2, self.top+160))

        if self.count > 90:
            screen.blit( self.cure_font4, (640*2/3 - self.cure_font4.get_width()/2, self.top+160))

        if self.count > 120:
            cure_window = game_self.temple.temple_cure_window
            character = cure_window.to_cure[cure_window.menu+cure_window.page*10]
            if game_self.temple.temple_cure_window.cure_pay_window.cured == True:
                screen.blit( self.success_font, (self.centerx - self.success_font.get_width()/2, self.top+240))
                self.status_change = 0
                #if character is dead
                if character.status[6] == 1:
                    character_font = character.name + self.alive_font
                    character_font = self.menu_font.render(character_font, True, COLOR_WHITE)
                    screen.blit( character_font, (self.centerx - character_font.get_width()/2, self.top+280))
                else:
                    character_font = character.name + self.good_font
                    character_font = self.menu_font.render(character_font, True, COLOR_WHITE)
                    screen.blit( character_font, (self.centerx - character_font.get_width()/2, self.top+280))
            else:
                screen.blit( self.failed_font, (self.centerx - self.failed_font.get_width()/2, self.top+240))
                #if character is dead
                if character.status[6] == 1:
                    self.status_change = 1
                    character_font = character.name + self.ashed_font
                    character_font = self.menu_font.render(character_font, True, COLOR_WHITE)
                    screen.blit( character_font, (self.centerx - character_font.get_width()/2, self.top+280))
                else:
                    #is ashed so...
                    self.status_change = 2
                    character_font = character.name + self.lost_font
                    character_font = self.menu_font.render(character_font, True, COLOR_WHITE)
                    screen.blit( character_font, (self.centerx - character_font.get_width()/2, self.top+280))

        self.count+=1

    def curing_window_handler(self, event, game_self):

        if self.count > 120:
            if event.type == KEYDOWN and (event.key ==K_x or event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
                self.is_visible = False
                game_self.temple.temple_cure_window.cure_pay_window.menu = 0
                game_self.temple.temple_cure_window.cure_pay_window.is_visible = False
                self.count = 0

                cure_window = game_self.temple.temple_cure_window
                character = cure_window.to_cure[cure_window.menu+cure_window.page*10]
                if self.status_change == 0:
                    character.status = [0,0,0,0,0,0,0,0,0]
                    #it is OK now so remove from to_cure window
                    character.hp = character.max_hp
                    del cure_window.to_cure[cure_window.menu+cure_window.page*10]

                if self.status_change == 1:
                    character.status[7] = 1
                if self.status_change == 2:
                    character.status[8] = 1
                    del game_self.temple.temple_cure_window.to_cure[cure_window.menu+cure_window.page*10]
                    #search for character and delete
                    i = 0
                    for chara in game_self.party.member:
                        if character == chara:
                            del game_self.party.member[i]
                        i += 1
                    i = 0
                    for chara in game_self.characters:
                        if character == chara:
                            del game_self.characters[i]
                        i += 1
                    #change the window to -1 to not go over range
                    if cure_window.menu+cure_window.page*10+1 > len(game_self.temple.temple_cure_window.to_cure):
                        if cure_window.menu == 0:
                            cure_window.page-=1
                        else:
                            cure_window.menu-=1
                        

