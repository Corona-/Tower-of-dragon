#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window
import item

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
NO_EXTRA, CHARACTER_VIEW, PARTY_REMOVE, CHARACTER_CHECK = 100, 101, 102, 103

MENU = 12

DUNGEON = 100

SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)


class Party:

    GOOD, NEUTRAL, EVIL = 1, 0, -1
    WARRIOR, FIGHTER, MAGICIAN, PRIEST, THIEF, MERCHANT = 0, 1, 2, 3, 4, 5
    LORD, SWORDMASTER, MADOVERLORD = 10,11,12
    MASTERSWORDSMAN, GENERAL, MURDERER = 13,14,15
    RUNESWORDSMAN, SAGE, SORCERER = 16,17,18
    POPE, BISHOP, FANATIC = 19,20,21
    CHIVALROUSTHIEF, PHANTOMTHIEF, NINJA = 22,23,24
    GUILDMASTER, ARMEDMERCHANT, MONEYLENDER = 25, 26,27
   
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

        #show what thief level when party moved to that coordinate
        self.dungeon_visited = []

        for floor in range(30):
            floor_visited = []
            for x in range(20):
                row_visited = []
                for y in range(20):
                    row_visited.append(0)
                floor_visited.append(row_visited)
            self.dungeon_visited.append(floor_visited)


        self.party_name = u"パーティ"

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.name_font = self.menu_font.render( "NAME", True, COLOR_WHITE)
        self.class_font = self.menu_font.render( "CLASS", True, COLOR_WHITE)
        self.ac_font = self.menu_font.render( "AC", True, COLOR_WHITE)
        self.hits_font = self.menu_font.render( "HITS", True, COLOR_WHITE)
        self.status_font = self.menu_font.render( "STATUS", True, COLOR_WHITE)

        self.bar_font = self.menu_font.render( "-", True, COLOR_WHITE)
        
    def update(self):
        pass
    def draw(self, screen, game_self):

        party_window = window.Window(Rect(10, 300, 620, 170))
        party_window.draw(screen)

        #draw selection for magic use for party members
        if game_self.game_state == MENU and game_self.menu.magic_window != None and game_self.menu.magic_window.magic_all_view != None and game_self.menu.magic_window.magic_all_view.magic_level_view != None and game_self.menu.magic_window.magic_all_view.magic_level_view.target_select != None:

            target_select = game_self.menu.magic_window.magic_all_view.magic_level_view.target_select

            if target_select.target == "PARTY_ONE":
                pygame.draw.rect(screen, COLOR_GLAY, Rect(14, 341+target_select.menu*20, 612, 20 ), 0)

            elif target_select.target == "PARTY_ALL":
                pygame.draw.rect(screen, COLOR_GLAY, Rect(14, 341, 612, len(game_self.party.member)*20 ), 0)

        elif game_self.game_state == DUNGEON and game_self.dungeon.battle != None and game_self.dungeon.battle.magic_window != None and game_self.dungeon.battle.magic_window.magic_level_view != None and game_self.dungeon.battle.magic_window.magic_level_view.target_select != None:

            target_select = game_self.dungeon.battle.magic_window.magic_level_view.target_select

            if target_select.target == "PARTY_ONE":
                pygame.draw.rect(screen, COLOR_GLAY, Rect(14, 341+target_select.menu*20, 612, 20 ), 0)
            elif target_select.target == "PARTY_ALL" or target_select.target == "DUNGEON":
                pygame.draw.rect(screen, COLOR_GLAY, Rect(14, 341, 612, len(game_self.party.member)*20 ), 0)
            elif target_select.target == "PARTY_SELF":
                #self only occur on battle
                pygame.draw.rect(screen, COLOR_GLAY, Rect(14, 341+game_self.dungeon.battle.selected*20, 612, 20 ), 0)

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
                elif character.job == self.LORD:  
                    job_font = self.menu_font.render( "LOR", True, COLOR_WHITE)
                elif character.job == self.SWORDMASTER:
                    job_font = self.menu_font.render( "SWO", True, COLOR_WHITE)
                elif character.job == self.MADOVERLORD:
                    job_font = self.menu_font.render( "MAD", True, COLOR_WHITE)
                elif character.job == self.MASTERSWORDSMAN:
                    job_font = self.menu_font.render( "MAS", True, COLOR_WHITE)
                elif character.job == self.GENERAL:
                    job_font = self.menu_font.render( "GEN", True, COLOR_WHITE)
                elif character.job == self.MURDERER:
                    job_font = self.menu_font.render( "MUR", True, COLOR_WHITE)
                elif character.job == self.RUNESWORDSMAN:  
                    job_font = self.menu_font.render( "RUN", True, COLOR_WHITE)
                elif character.job == self.SAGE:
                    job_font = self.menu_font.render( "SAG", True, COLOR_WHITE)
                elif character.job == self.SORCERER:
                    job_font = self.menu_font.render( "SOR", True, COLOR_WHITE)
                elif character.job == self.POPE:
                    job_font = self.menu_font.render( "POP", True, COLOR_WHITE)
                elif character.job == self.BISHOP:
                    job_font = self.menu_font.render( "BIS", True, COLOR_WHITE)
                elif character.job == self.FANATIC:
                    job_font = self.menu_font.render( "FAN", True, COLOR_WHITE)
                elif character.job == self.GUILDMASTER:  
                    job_font = self.menu_font.render( "GUI", True, COLOR_WHITE)
                elif character.job == self.ARMEDMERCHANT:
                    job_font = self.menu_font.render( "ARM", True, COLOR_WHITE)
                elif character.job == self.MONEYLENDER:
                    job_font = self.menu_font.render( "MON", True, COLOR_WHITE)
                elif character.job == self.CHIVALROUSTHIEF:
                    job_font = self.menu_font.render( "CHI", True, COLOR_WHITE)
                elif character.job == self.PHANTOMTHIEF:
                    job_font = self.menu_font.render( "PHA", True, COLOR_WHITE)
                elif character.job == self.NINJA:
                    job_font = self.menu_font.render( "NIN", True, COLOR_WHITE)

                character_ac = calculate_ac(character)

                character_ac_font = self.menu_font.render( "".join(str(character_ac)), True, COLOR_WHITE)
                character_hits_font = self.menu_font.render( "".join(str(character.hp)), True, COLOR_WHITE)

                if character.status == [0,0,0,0,0,0,0,0,0]:
                    character_status_font = self.menu_font.render( "".join(str(character.max_hp)), True, COLOR_WHITE)
                else:

                    j = 0
                    for st in character.status:
                        if j == 0 and st > 0:
                            character_status_font = self.menu_font.render( "POISON", True, COLOR_WHITE)
                        if j == 1 and st > 0:
                            character_status_font = self.menu_font.render( "MUTE", True, COLOR_WHITE)
                        if j == 2 and st > 0:
                            character_status_font = self.menu_font.render( "AFRAID", True, COLOR_WHITE)
                        if j == 3 and st > 0:
                            character_status_font = self.menu_font.render( "ASLEEP", True, COLOR_WHITE)
                        if j == 4 and st > 0:
                            character_status_font = self.menu_font.render( "PARALY", True, COLOR_WHITE)
                        if j == 5 and st > 0:
                            character_status_font = self.menu_font.render( "PETRIF", True, COLOR_WHITE)
                        if j == 6 and st > 0:
                            character_status_font = self.menu_font.render( "DEAD", True, COLOR_WHITE)
                        if j == 7 and st > 0:
                            character_status_font = self.menu_font.render( "ASHED", True, COLOR_WHITE)
                        if j == 8 and st > 0:
                            character_status_font = self.menu_font.render( "LOST", True, COLOR_WHITE)
                        j+= 1

                screen.blit(alignment_font, (SCREEN_RECTANGLE.width/2-130,SCREEN_RECTANGLE.height/2+100+i*20))
                screen.blit(self.bar_font, (SCREEN_RECTANGLE.width/2-130+alignment_font.get_width(),SCREEN_RECTANGLE.height/2+100+i*20))
                screen.blit(job_font, (SCREEN_RECTANGLE.width/2-130+alignment_font.get_width()+self.bar_font.get_width(),SCREEN_RECTANGLE.height/2+100+i*20))                
                screen.blit(character_ac_font, (SCREEN_RECTANGLE.width/2+20-character_ac_font.get_width()/2,SCREEN_RECTANGLE.height/2+100+i*20))
                screen.blit(character_hits_font, (SCREEN_RECTANGLE.width/2+110 - character_hits_font.get_width()/2,SCREEN_RECTANGLE.height/2+100+i*20)) 
                screen.blit(character_status_font, (SCREEN_RECTANGLE.width/2+240 - character_status_font.get_width()/2,SCREEN_RECTANGLE.height/2+100+i*20))
    
                    
                i += 1

def calculate_ac(character):

    ac = character.ac

    #calculate ac from equipment
    for equip in character.equip:
        if isinstance(equip, item.Item):
            ac += equip.evade


    #calculate ac from magic
    ac += character.permanant_ac
    ac += character.battle_ac
    ac += character.defend_ac

    return ac










    
