#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import easygui
import random

import character
import window

import character_make_window

import string

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
NO_EXTRA, CHARACTER_VIEW, PARTY_REMOVE, CHARACTER_CHECK = 100, 101, 102, 103


SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)


class Character_make:

    GOOD, NEUTRAL, EVIL = 1, 0, -1
    WARRIOR, FIGHTER, MAGICIAN, PRIEST,  THIEF, MERCHANT = 0, 1, 2, 3, 4, 5
    STRENGTH, INTELLIGENCE, PIETY, VITALITY, AGILITY, LUCK = 10, 11, 12, 13, 14, 15

    def __init__(self):

        self.menu = self.GOOD
        self.menu_font = pygame.font.Font("ipag.ttf", 20) 
        self.character_name_message = u"名前を入力してください（8文字制限）"
        self.message_title = u"名前入力"
        self.fieldnames = [u"名前"]
        self.fieldvalues = []
        self.name = []

        #good = 1, neutral = 0, evil = -1
        self.alignment = None
        #warrior = 0, fighter = 1, magician = 2, priest = 3, thief = 4, merchant = 5
        self.job = None
        self.bonus_point = -1
        self.max_bonus_point = -1

        self.strength = 0
        self.intelligence = 0
        self.piety = 0
        self.vitality = 0
        self.agility = 0
        self.luck = 0

        #stores bonus points
        self.strength_plus = 0
        self.intelligence_plus = 0
        self.piety_plus = 0
        self.vitality_plus = 0
        self.agility_plus = 0
        self.luck_plus = 0
        
        #creates bonus points randomly
        probability = random.randint(1, 100)
        if probability < 80:
            self.bonus_point = random.randint(5, 12)
        elif probability < 100:
            self.bonus_point = random.randint(13, 19)
        elif probability == 100:
            self.bonus_point = random.randint(20,27)
            
        self.max_bonus_point = self.bonus_point


        
        self.cursor = self.menu_font.render(u"⇒", True, COLOR_WHITE)
        #set up selecting window
        self.alignment_window = character_make_window.Alignment_window(Rect(250, 100, 190, 150))
        self.job_window = character_make_window.Job_window(Rect(250, 100, 190, 240))
        self.bonus_window = character_make_window.Bonus_window(Rect(250, 100, 190, 240))
        self.select_window = character_make_window.Select_window(Rect(250, 100, 340, 140))
          

    def update(self):
        pass
    def draw(self, game_self, screen):
        #set the background to black
        screen.fill(COLOR_BLACK)

        #show the messagebox while input is empty
        if( self.fieldvalues == []):
            self.fieldvalues = easygui.multenterbox(self.character_name_message, self.message_title, self.fieldnames)


        if (self.fieldvalues != None):
            #if length is > 8 or empty string, then re-enter
            if len(self.fieldvalues[0]) > 8 or len(self.fieldvalues[0]) == 0:
                game_self.character_make = Character_make()
                game_self.game_state = CASTLE
                return
            #if it includes spaces, then also re-enter
            #if string.count(self.fieldvalues[0], " "):
            #if there is space at the front, re-enter
            if self.fieldvalues[0][0] == " ":
                game_self.character_make = Character_make()
                game_self.game_state = CASTLE
                return
            
        #if cancel is pressed, go back to castle menu
        elif self.fieldvalues == None:
            game_self.character_make = Character_make()  
            game_self.game_state = CASTLE
            return 

        #set the name of the character
        self.name = u"".join(self.fieldvalues)

        #print the name on screen
        self.name_font = self.menu_font.render(u"".join(self.name), True, COLOR_WHITE)
        title_font = self.menu_font.render(u"名前：", True, COLOR_WHITE)

        name_window = window.Window(Rect(20,20, self.name_font.get_width() + title_font.get_width()+20, 50))
        name_window.draw(screen)

        screen.blit(title_font, ( 30 ,35))        
        screen.blit(self.name_font, ( 30 + title_font.get_width() , 35))

        #print the alignment on screen
        alignment_font = self.menu_font.render(u"性格：", True, COLOR_WHITE)
        not_selected_font = self.menu_font.render(u"？？？", True, COLOR_WHITE)
        good_font = self.menu_font.render(u"善", True, COLOR_WHITE)
        neutral_font = self.menu_font.render(u"中立", True, COLOR_WHITE)
        evil_font = self.menu_font.render(u"悪", True, COLOR_WHITE)
 

        alignment_window = window.Window(Rect(20, 90, 20 + alignment_font.get_width() + not_selected_font.get_width(), 50))
        alignment_window.draw(screen)

        screen.blit(alignment_font, ( 30 ,105))        

        if self.alignment == None:
            screen.blit(not_selected_font, ( 30 + alignment_font.get_width() , 105))
        elif self.alignment == self.GOOD:
            screen.blit(good_font, ( 30 + alignment_font.get_width() , 105))
        elif self.alignment == self.NEUTRAL:
            screen.blit(neutral_font, ( 30 + alignment_font.get_width() , 105))
        elif self.alignment == self.EVIL:
            screen.blit(evil_font, ( 30 + alignment_font.get_width() , 105))

        #print the job on screen
        job_font = self.menu_font.render(u"職業：", True, COLOR_WHITE)
        warrior_font = self.menu_font.render(u"戦士", True, COLOR_WHITE)
        fighter_font = self.menu_font.render(u"武士", True, COLOR_WHITE) 
        magician_font = self.menu_font.render(u"魔術師", True, COLOR_WHITE) 
        priest_font = self.menu_font.render(u"僧侶", True, COLOR_WHITE) 
        thief_font = self.menu_font.render(u"盗賊", True, COLOR_WHITE)
        merchant_font = self.menu_font.render(u"商人", True, COLOR_WHITE)
 
        job_window = window.Window(Rect(20, 160, 20 + job_font.get_width() + not_selected_font.get_width(), 50))
        job_window.draw(screen)

        screen.blit(job_font, ( 30 ,175))        

        if self.job == None:
            screen.blit(not_selected_font, ( 30 + job_font.get_width() , 175))
        if self.job == self.WARRIOR:
            screen.blit(warrior_font, ( 30 + job_font.get_width() , 175))            
        if self.job == self.FIGHTER:
            screen.blit(fighter_font, ( 30 + job_font.get_width() , 175))            
        if self.job == self.MAGICIAN:
            screen.blit(magician_font, ( 30 + job_font.get_width() , 175))            
        if self.job == self.PRIEST:
            screen.blit(priest_font, ( 30 + job_font.get_width() , 175))            
        if self.job == self.THIEF:
            screen.blit(thief_font, ( 30 + job_font.get_width() , 175))            
        if self.job == self.MERCHANT:
            screen.blit(merchant_font, ( 30 + job_font.get_width() , 175))            


        #print the status on screen
        status_font = self.menu_font.render(u"能力値", True, COLOR_WHITE)

        strength_font = self.menu_font.render(u"力：", True, COLOR_WHITE)
        intelligence_font = self.menu_font.render(u"知恵：", True, COLOR_WHITE)
        piety_font = self.menu_font.render(u"信仰：", True, COLOR_WHITE) 
        vitality_font = self.menu_font.render(u"生命力：", True, COLOR_WHITE)
        agility_font = self.menu_font.render(u"素早さ：", True, COLOR_WHITE) 
        luck_font = self.menu_font.render(u"運：", True, COLOR_WHITE) 

        #fonts for actual status (with bonus points)
        not_selected_font = self.menu_font.render(u"？？", True, COLOR_WHITE)
        ch_strength_font = self.menu_font.render("".join(str(self.strength+self.strength_plus)), True, COLOR_WHITE)
        ch_intelligence_font = self.menu_font.render("".join(str(self.intelligence+self.intelligence_plus)), True, COLOR_WHITE)
        ch_piety_font = self.menu_font.render("".join(str(self.piety+self.piety_plus)), True, COLOR_WHITE)
        ch_vitality_font = self.menu_font.render("".join(str(self.vitality+self.vitality_plus)), True, COLOR_WHITE)
        ch_agility_font = self.menu_font.render("".join(str(self.agility+self.agility_plus)), True, COLOR_WHITE)
        ch_luck_font = self.menu_font.render(str(self.luck+self.luck_plus), True, COLOR_WHITE)

        #print the status points on screen   
        status_window = window.Window(Rect(20, 230, 20 + vitality_font.get_width() + not_selected_font.get_width(), 230))
        status_window.draw(screen)

        screen.blit(status_font, ( 60 ,245))        
        screen.blit(strength_font, ( 30 , 275))
        screen.blit(intelligence_font, ( 30 , 305))
        screen.blit(piety_font, ( 30 , 335))
        screen.blit(vitality_font, ( 30 , 365))
        screen.blit(agility_font, ( 30 , 395))
        screen.blit(luck_font, ( 30 , 425))

        screen.blit(ch_strength_font, ( 115, 275))
        screen.blit(ch_intelligence_font, ( 115, 305))
        screen.blit(ch_piety_font, ( 115, 335))
        screen.blit(ch_vitality_font, ( 115, 365))
        screen.blit(ch_agility_font, ( 115, 395))
        screen.blit(ch_luck_font, ( 115, 425))

        #draw the appropriate selecting window
        self.alignment_window.draw(screen)
        self.job_window.draw( self, screen)
        self.bonus_window.draw( self, screen)
        self.select_window.draw(screen)



def character_make_handler(self, event):
    """event handler of character"""

    if self.character_make.alignment_window.is_visible:
        self.character_make.alignment_window.alignment_window_handler(self, event)
        return

    elif self.character_make.job_window.is_visible:
        self.character_make.job_window.job_window_handler(self, event)
        return

    elif self.character_make.bonus_window.is_visible:
        self.character_make.bonus_window.bonus_window_handler(self, event)
        return

    elif self.character_make.select_window.is_visible:
        self.character_make.select_window.select_window_handler(self, event)
        return

    if event.type == KEYUP and event.key == K_x:
        self.character_make = Character_make()
        self.game_state = CASTLE
