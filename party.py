#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
NO_EXTRA, CHARACTER_VIEW, PARTY_REMOVE, CHARACTER_CHECK = 100, 101, 102, 103


SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)



class Party:

    GOOD, NEUTRAL, EVIL = 1, 0, -1
    WARRIOR, FIGHTER, MAGICIAN, PRIEST, THIEF, MERCHANT = 0, 1, 2, 3, 4, 5
    
    def __init__(self):
        self.member = []

        self.days = 0

        #the direction of the party in the dungeon
        #0 is up, 1 is right, 2 is down, 3 is left
        self.direction = 0

        #if magic is used to view better, change it to 1
        self.torch = 0

        #if the party has house or not,
        #if > 0 it stores level of the house
        self.house = 0

        self.alignment = 0

        self.bar_donate = 0
        self.shop_donate = 0
        self.temple_donate = 0
        self.castle_donate = 0

        self.inn_item = []
        self.house_item = []

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.name_font = self.menu_font.render( "NAME", True, COLOR_WHITE)
        self.class_font = self.menu_font.render( "CLASS", True, COLOR_WHITE)
        self.ac_font = self.menu_font.render( "AC", True, COLOR_WHITE)
        self.hits_font = self.menu_font.render( "HITS", True, COLOR_WHITE)
        self.status_font = self.menu_font.render( "STATUS", True, COLOR_WHITE)

        self.bar_font = self.menu_font.render( "-", True, COLOR_WHITE)
        
    def update(self):
        pass
    def draw(self, screen):

        party_window = window.Window(Rect(10, 300, 620, 170))
        party_window.draw(screen)

        screen.blit(self.name_font, ((SCREEN_RECTANGLE.width-self.name_font.get_width())/4-100,SCREEN_RECTANGLE.height/2+80))   
        screen.blit(self.class_font, ((SCREEN_RECTANGLE.width-self.class_font.get_width())/2-80,SCREEN_RECTANGLE.height/2+80))   
        screen.blit(self.ac_font, ((SCREEN_RECTANGLE.width-self.ac_font.get_width())/2+20,SCREEN_RECTANGLE.height/2+80))   
        screen.blit(self.hits_font, ((SCREEN_RECTANGLE.width-self.hits_font.get_width())/2+110,SCREEN_RECTANGLE.height/2+80))   
        screen.blit(self.status_font, ((SCREEN_RECTANGLE.width-self.status_font.get_width())/2+240,SCREEN_RECTANGLE.height/2+80))   

        if self.member != []:
            i = 0
            for character in self.member:
                character_name_font = self.menu_font.render( character.name , True, COLOR_WHITE)
                screen.blit(character_name_font, (SCREEN_RECTANGLE.width/4-140,SCREEN_RECTANGLE.height/2+100+i*20))

                if character.alignment == self.GOOD:
                    alignment_font = self.menu_font.render( "G", True, COLOR_WHITE)
                elif character.alignment == self.NEUTRAL:
                    alignment_font = self.menu_font.render( "N", True, COLOR_WHITE)
                elif character.alignment == self.EVIL:
                    alignment_font = self.menu_font.render( "E", True, COLOR_WHITE)

                if character.job == self.WARRIOR:  
                    job_font = self.menu_font.render( "WAR", True, COLOR_WHITE)
                elif character.job == self.FIGHTER:
                    job_font = self.menu_font.render( "FIG", True, COLOR_WHITE)
                elif character.job == self.MAGICIAN:
                    job_font = self.menu_font.render( "MAG", True, COLOR_WHITE)
                elif character.job == self.PRIEST:
                    job_font = self.menu_font.render( "PRI", True, COLOR_WHITE)
                elif character.job == self.THIEF:
                    job_font = self.menu_font.render( "THI", True, COLOR_WHITE)
                elif character.job == self.MERCHANT:
                    job_font = self.menu_font.render( "MER", True, COLOR_WHITE)

                character_ac_font = self.menu_font.render( "".join(str(character.ac)), True, COLOR_WHITE)
                character_hits_font = self.menu_font.render( "".join(str(character.hp)), True, COLOR_WHITE)
                character_status_font = self.menu_font.render( "".join(str(character.max_hp)), True, COLOR_WHITE)
                 

                screen.blit(alignment_font, (SCREEN_RECTANGLE.width/2-130,SCREEN_RECTANGLE.height/2+100+i*20))
                screen.blit(self.bar_font, (SCREEN_RECTANGLE.width/2-130+alignment_font.get_width(),SCREEN_RECTANGLE.height/2+100+i*20))
                screen.blit(job_font, (SCREEN_RECTANGLE.width/2-130+alignment_font.get_width()+self.bar_font.get_width(),SCREEN_RECTANGLE.height/2+100+i*20))
                screen.blit(character_ac_font, (SCREEN_RECTANGLE.width/2,SCREEN_RECTANGLE.height/2+100+i*20))
                screen.blit(character_hits_font, (SCREEN_RECTANGLE.width/2+110 - character_hits_font.get_width()/2,SCREEN_RECTANGLE.height/2+100+i*20)) 
                screen.blit(character_status_font, (SCREEN_RECTANGLE.width/2+240 - character_status_font.get_width()/2,SCREEN_RECTANGLE.height/2+100+i*20))
    
                    
                i += 1
