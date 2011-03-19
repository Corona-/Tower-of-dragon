#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sitecustomize
import sys
import save

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
NO_EXTRA, CHARACTER_VIEW, PARTY_REMOVE, CHARACTER_CHECK = 100, 101, 102, 103


SCREEN_RECTANGLE = Rect(0,0,640,480)

TEXT_SIZE_LARGE = 60
TEXT_SIZE_SMALL = 20
TEXT_SIZE_VERY_SMALL = 10

COLOR_BLACK = (0,0,0)
COLOR_WHITE = (255,255,255)


class Title:
    """creates title menu"""

    #used on menu, each selects item on menu
    START, CONTINUE, END = 0, 1, 2

    def __init__(self):
        self.menu = self.START

        #create fonts for displaying on screen
        self.title_font = pygame.font.Font("ipag.ttf", TEXT_SIZE_LARGE) # create the font
        self.menu_font = pygame.font.Font("ipag.ttf", TEXT_SIZE_SMALL) 
        self.copyright_font = pygame.font.Font("ipag.ttf", TEXT_SIZE_VERY_SMALL) 

        self.title = self.title_font.render("WIZARDPY", True, COLOR_BLACK)      
        self.subtitle = self.menu_font.render("TOWER OF ELDER DRAGON", True, COLOR_BLACK)      
        self.game_start = self.menu_font.render("NEW GAME", True, COLOR_BLACK)
        self.game_continue = self.menu_font.render("CONTINUE", True, COLOR_BLACK)
        self.game_end = self.menu_font.render("END GAME", True, COLOR_BLACK)
        self.credit_1 = self.copyright_font.render(u"Copyright: 2011 By MUSYOKU DOUTEI ◆HyQRiOn/vs", True, COLOR_BLACK)
        self.credit_2 = self.copyright_font.render("Created By ...?", True, COLOR_BLACK)
        self.cursor = self.menu_font.render(u"⇒", True, COLOR_BLACK)

        self.music = 0

    def update(self):

        if( self.music == 0):
            pygame.mixer.music.load("BGM/sennen_no_tuioku.mp3")
            pygame.mixer.music.play(-1)
            self.music = 1
        pass

    def draw(self, screen):
        #fill background with white
        screen.fill(COLOR_WHITE)

        #draw title 
        screen.blit(self.title,((SCREEN_RECTANGLE.width-self.title.get_width())/2,(SCREEN_RECTANGLE.height/6)))
        screen.blit(self.subtitle,((SCREEN_RECTANGLE.width-self.subtitle.get_width())/2,(SCREEN_RECTANGLE.height/6)+60))

        #draw menu item
        screen.blit(self.game_start, ((SCREEN_RECTANGLE.width-self.game_start.get_width())/2,SCREEN_RECTANGLE.height/2))
        screen.blit(self.game_continue, ((SCREEN_RECTANGLE.width-self.game_continue.get_width())/2,SCREEN_RECTANGLE.height/2 + SCREEN_RECTANGLE.height/12))
        screen.blit(self.game_end, ((SCREEN_RECTANGLE.width-self.game_end.get_width())/2,SCREEN_RECTANGLE.height/2 + SCREEN_RECTANGLE.height/6))

        #draw credits
        screen.blit(self.credit_1, ((SCREEN_RECTANGLE.width-self.credit_1.get_width())/2,SCREEN_RECTANGLE.height - (SCREEN_RECTANGLE.height/6)))
        screen.blit(self.credit_2, ((SCREEN_RECTANGLE.width-self.credit_2.get_width())/2,SCREEN_RECTANGLE.height - (SCREEN_RECTANGLE.height/6) + 20))


        #draw cursors depending on value of menu
        if self.menu == self.START:
            screen.blit(self.cursor, (((SCREEN_RECTANGLE.width-self.game_start.get_width()))/2-20,SCREEN_RECTANGLE.height/2))
        elif self.menu == self.CONTINUE:
            screen.blit(self.cursor, (((SCREEN_RECTANGLE.width-self.game_continue.get_width())/2)-20,SCREEN_RECTANGLE.height/2 + SCREEN_RECTANGLE.height/12))
        elif self.menu == self.END:
            screen.blit(self.cursor, (((SCREEN_RECTANGLE.width-self.game_end.get_width())/2)-20,SCREEN_RECTANGLE.height/2 + SCREEN_RECTANGLE.height/6))




def title_handler(self, event):
    """event handler of title"""

    #moves cursor up
    if event.type == KEYUP and event.key == K_UP:
        self.title.menu -= 1
        if self.title.menu < 0:
            self.title.menu = 0
    #moves cursor down
    elif event.type == KEYUP and event.key == K_DOWN:
        self.title.menu += 1
        if self.title.menu > 2:
            self.title.menu = 2
    #select menu item
    if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
        if self.title.menu == Title.START:
            self.game_state = CITY
        elif self.title.menu == Title.CONTINUE:
            save.load( self, self)
            self.game_state = CITY
        elif self.title.menu == Title.END:
            pygame.quit()
            sys.exit()

        self.title.music = 0
