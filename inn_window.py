#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window
import system_notify

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)


class Inn_window(window.Window):

    HORSE, EASY, ECONOMY, SUITE, ROYAL = 0, 1, 2, 3, 4
    MENU_MAX = 4

    REST = 4
    def __init__(self, rectangle):
        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.menu = 0

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.title_font = self.menu_font.render(u"どこに泊まりますか？", True, COLOR_WHITE)

        self.horse_font = self.menu_font.render(u"馬小屋：", True, COLOR_WHITE)
        self.easy_font = self.menu_font.render(u"簡易寝台：", True, COLOR_WHITE)
        self.economy_font = self.menu_font.render(u"エコノミールーム：", True, COLOR_WHITE)
        self.suite_font = self.menu_font.render(u"スイートルーム：", True, COLOR_WHITE)
        self.royal_font = self.menu_font.render(u"ロイヤルスイート：", True, COLOR_WHITE)

        self.price1_font = self.menu_font.render(u"無料", True, COLOR_WHITE)
        self.price2_font = self.menu_font.render(u"10TG", True, COLOR_WHITE)
        self.price3_font = self.menu_font.render(u"50TG", True, COLOR_WHITE)
        self.price4_font = self.menu_font.render(u"200TG", True, COLOR_WHITE)
        self.price5_font = self.menu_font.render(u"500TG", True, COLOR_WHITE)

        self.who_rest = None #system_notify.System_notify_window(Rect(240, 80 ,240, 240), system_notify.System_notify_window.REST)
        
    def draw(self, screen, character):
        """draw the window on the screen"""
        
        window.Window.draw(self, screen)        
        if self.is_visible == False: return

        screen.blit(self.title_font, (self.centerx - self.title_font.get_width()/2 , self.top+15))


        #set cursor on menu items
        if self.menu == self.HORSE:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4,self.top+40,self.right-self.left-8,30), 0)
        if self.menu == self.EASY:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4,self.top+70,self.right-self.left-8,30), 0)
        if self.menu == self.ECONOMY:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4,self.top+100,self.right-self.left-8,30), 0)
        if self.menu == self.SUITE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4,self.top+130,self.right-self.left-8,30), 0)
        if self.menu == self.ROYAL:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4,self.top+160,self.right-self.left-8,30), 0)


        screen.blit(self.horse_font, (self.left + 20 , self.top+45))
        screen.blit(self.easy_font, (self.left + 20, self.top+75))
        screen.blit(self.economy_font, (self.left + 20 , self.top+105))
        screen.blit(self.suite_font, (self.left + 20 , self.top+135))
        screen.blit(self.royal_font, (self.left + 20 , self.top+165))
        
        screen.blit(self.price1_font, (self.right - 30 - self.price1_font.get_width() , self.top+45))
        screen.blit(self.price2_font, (self.right - 20 - self.price2_font.get_width() , self.top+75))
        screen.blit(self.price3_font, (self.right - 20 - self.price3_font.get_width() , self.top+105))
        screen.blit(self.price4_font, (self.right - 20 - self.price4_font.get_width() , self.top+135))
        screen.blit(self.price5_font, (self.right - 20 - self.price5_font.get_width() , self.top+165))

        #draws extra window
        if self.who_rest != None:
            self.who_rest.draw(screen, character)


    def inn_window_handler(self, event, game_self, character):

        if self.who_rest != None and self.who_rest.is_visible == True:
            self.who_rest.system_notify_window_handler( event, game_self, character)
            return

        if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
            self.who_rest = system_notify.System_notify_window(Rect(240, 80 ,240, 240), system_notify.System_notify_window.REST)
            self.who_rest.is_visible = True
                        
        if event.type == KEYUP and event.key == K_x:
            self.menu = 0
            self.is_visible = False

        if event.type == KEYUP and event.key == K_UP:
            self.menu -= 1
            if self.menu < 0:
                self.menu = self.MENU_MAX

        if event.type == KEYUP and event.key == K_DOWN:
            self.menu += 1
            if self.menu > self.MENU_MAX:
                self.menu = 0

#def rest_lv_up(self, rest_level):

    

