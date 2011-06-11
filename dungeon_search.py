#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

import window
import random

import battle
import codecs
import system_notify
import city
import menu
import dungeon_message
import tower
TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
MENU=12

CHARACTER_MAKE = 10

SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

class Dungeon_search_window(window.Window):

    def __init__(self, rectangle):

        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.menu = 0

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.check_font = self.menu_font.render( u"調査", True, COLOR_WHITE) 
        self.search_font = self.menu_font.render( u"仲間を探す", True, COLOR_WHITE) 
        self.break_font = self.menu_font.render( u"冒険を中断する", True, COLOR_WHITE)


        self.search_window = None
        self.check_window = None


    def draw(self, screen, game_self):

        if self.is_visible == False: return        
        window.Window.draw(self, screen)

        pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+15 + 30*self.menu,(self.right-self.left)-8,30), 0)


        screen.blit( self.check_font, (self.centerx - self.check_font.get_width()/2, self.top+20))
        screen.blit( self.search_font, (self.centerx - self.search_font.get_width()/2, self.top+50))
        screen.blit( self.break_font, (self.centerx - self.break_font.get_width()/2, self.top+80))

        if self.search_window != None:
            self.search_window.draw(screen, game_self)
        if self.check_window != None:
            self.check_window.draw(screen, game_self)
                
        
    def dungeon_search_window_handler(self, event, game_self):

        if self.search_window != None and self.search_window.is_visible == True:
            self.search_window.search_window_handler(event, game_self)
            return
        elif self.check_window != None and self.check_window.is_visible == True:
            self.check_window.search_window_handler(event,game_self)
            return


        if event.type == KEYDOWN and event.key == K_x:
            self.menu = 0
            self.is_visible = False
            
        elif event.type == KEYDOWN and (event.key ==K_UP):
            self.menu -= 1
            if self.menu < 0:
                self.menu = 2
        elif event.type == KEYDOWN and (event.key ==K_DOWN):
            self.menu += 1
            if self.menu > 2:
                self.menu = 0
                
     
        elif event.type == KEYDOWN and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
            if self.menu == 0:
                pass
            elif self.menu == 1:
                self.search_window = Search_window(Rect(100,  140 ,440, 100), 1)
                self.search_window.is_visible = True
                pass
            elif self.menu == 2:
                for character in game_self.party.member:
                    game_self.dungeon_characters.append( character)

                game_self.party.member = []
                game_self.party.alignment = 0

                game_self.dungeon = None
                game_self.game_state = CITY
                game_self.city = city.City()
                

class Search_window(window.Window):

    GOOD, NEUTRAL, EVIL = 1, 0, -1
    WARRIOR, FIGHTER, MAGICIAN,PRIEST, THIEF, MERCHANT = 0, 1, 2, 3, 4, 5
    LORD, SWORDMASTER, MADOVERLORD = 10,11,12
    MASTERSWORDSMAN, GENERAL, MURDERER = 13,14,15
    RUNESWORDSMAN, SAGE, SORCERER = 16,17,18
    POPE, BISHOP, FANATIC = 19,20,21
    CHIVALROUSTHIEF, PHANTOMTHIEF, NINJA = 22,23,24
    GUILDMASTER, ARMEDMERCHANT, MONEYLENDER = 25, 26,27

    MENU_MAX = 9

    def __init__(self, rectangle, instruction):

        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.instruction = instruction

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.check_font = self.menu_font.render( u"調査中", True, COLOR_WHITE) 
        self.wait_font = u"・"

        self.join_font = self.menu_font.render(u"誰をパーティに加えますか？", True, COLOR_WHITE)
        self.not_found_font = self.menu_font.render(u"誰も見つかりませんでした", True, COLOR_WHITE)

        self.found_character = []
        self.find = False

        self.menu = 0
        self.page = 0

        self.count = 0

        self.no_one_found = None

    def draw(self, screen, game_self):

        if self.is_visible == False: return        
        window.Window.draw(self, screen)

        if self.count < 94:
            screen.blit( self.check_font, (self.centerx - self.check_font.get_width()/2, self.top+20))

            self.bullet_font = self.menu_font.render( self.wait_font, True, COLOR_WHITE) 
            screen.blit( self.bullet_font, (self.left+24, self.top+70))

            if self.count % 5 == 0:
                self.wait_font += u"・"

            self.count+=1

        else:

            if self.find == False:

                self.find = True

                for character in game_self.dungeon_characters:
                    if character.coordinate == game_self.party.member[0].coordinate:
                        self.found_character.append(character)
                if self.found_character == []:
                    self.no_one_found = system_notify.Donate_finish_window( Rect(150,160,300,50),system_notify.Donate_finish_window.NO_ONE)
                    self.no_one_found.is_visible = True
    


            if self.found_character != []:
                instruction_window = window.Window(Rect(20,20, 30+self.join_font.get_width(), 50))
                instruction_window.draw(screen)
                screen.blit(self.join_font, ( 35 , 35))           

                character = self.found_character

                self.top = 60
                self.left = 80
                self.right = 560
                self.centerx = 320


                character_window = window.Window(Rect(80, 60, 480, 360))
                character_window.draw(screen)

                top_font = self.menu_font.render( u"冒険者一覧", True, COLOR_WHITE)      
                screen.blit(top_font, (self.centerx - top_font.get_width()/2, 80))


                if character != []:
                    #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
                    #the height depends on the size of font
                    pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+47+30*self.menu,(self.right-self.left)-8,25), 0)

                i = 0
                for chara in character[self.page*10:(self.page+1)*10]:
                    character_font = self.menu_font.render(chara.name, True, COLOR_WHITE)
                    screen.blit(character_font, (self.left+20, self.top+50+(i%10)*30))                                         
                    level_font = self.menu_font.render("LV" + str(chara.level), True, COLOR_WHITE)
                    screen.blit(level_font, (self.right - 100, self.top+50+(i%10)*30))                                         

                    align = None
                    job = None
                    if chara.alignment == self.GOOD:
                        align = "G"
                    elif chara.alignment == self.NEUTRAL:
                        align = "N"
                    elif chara.alignment == self.EVIL:
                        align = "E"

                    if chara.job == self.WARRIOR:
                        job = "WAR"
                    elif chara.job == self.FIGHTER:
                        job = "FIG"
                    elif chara.job == self.MAGICIAN:
                        job = "MAG"
                    elif chara.job == self.PRIEST:
                        job = "PRI"
                    elif chara.job == self.THIEF:
                        job = "THI"
                    elif chara.job == self.MERCHANT:
                        job = "MER"
                    elif chara.job == self.LORD:
                        job = "LOR"
                    elif chara.job == self.SWORDMASTER:
                        job = "SWO"
                    elif chara.job == self.MADOVERLORD:
                        job = "MAD"
                    elif chara.job == self.MASTERSWORDSMAN:
                        job = "MAS"
                    elif chara.job == self.GENERAL:
                        job = "GEN"
                    elif chara.job == self.MURDERER:
                        job = "MUR"
                    elif chara.job == self.RUNESWORDSMAN:
                        job = "RUN"
                    elif chara.job == self.SAGE:
                        job = "SAG"
                    elif chara.job == self.SORCERER:
                        job = "SOR"
                    elif chara.job == self.POPE:
                        job = "POP"
                    elif chara.job == self.BISHOP:
                        job = "BIS"
                    elif chara.job == self.FANATIC:
                        job = "FAN"
                    elif chara.job == self.GUILDMASTER:
                        job = "GUI"
                    elif chara.job == self.ARMEDMERCHANT:
                        job = "ARM"
                    elif chara.job == self.MONEYLENDER:
                        job = "MON"
                    elif chara.job == self.CHIVALROUSTHIEF:
                        job = "CHI"
                    elif chara.job == self.PHANTOMTHIEF:
                        job = "PHA"
                    elif chara.job == self.NINJA:
                        job = "NIN"

                    total = align + "-" + job
                    total_font = self.menu_font.render(total, True, COLOR_WHITE)
                    screen.blit(total_font, (self.centerx, self.top+50+(i%10)*30))              
                    i+=1

            else:

                if self.no_one_found != None:
                    self.no_one_found.draw(screen)

    def search_window_handler(self, event, game_self):

        if self.no_one_found != None and self.no_one_found.is_visible == True:
            self.no_one_found.donate_finish_window_handler(event, game_self)
            return

        if self.count < 94:
            pass

        else:
            character = self.found_character
            
            if event.type == KEYDOWN and event.key == K_x:
                self.menu = 0
                self.page = 0
                self.is_visible = False

            if event.type == KEYDOWN and event.key == K_UP: #moves the cursor up
                self.menu -= 1
                if self.menu < 0:
                    self.menu = 0
            elif event.type == KEYDOWN and event.key == K_DOWN:
                if len(character) > self.menu+self.page*10+1:
                    self.menu += 1
                    if self.menu > self.MENU_MAX:
                        self.menu = self.MENU_MAX
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                if len(character) > (self.page+1)*10:
                    self.page += 1
                    self.menu = 0
            elif event.type == KEYDOWN and event.key == K_LEFT:
                if self.page > 0:
                    self.page -= 1
                    self.menu = 0
            elif  event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
                if len(character) == 0: return
                if len(game_self.party.member) < 6:
                    game_self.party.member.append(character[self.menu + self.page*10])
                    game_self.party.alignment += character[self.menu + self.page*10].alignment
                    print game_self.party.alignment

                    #found_characterで足す人を決めて
                    #足したら、dungeon_characterでその人を探して削除する
                    i = 0
                    for chara in game_self.dungeon_characters:
                        if chara == character[self.menu + self.page*10]:
                            del game_self.dungeon_characters[i]
                            break
                        i += 1
                    del character[self.menu + self.page*10]

                    if (self.menu + self.page*10)+1 > len(character):
                        self.menu -=1
                        #if that page has no more, go back to previous page and set cursor to bottom
                        if self.menu < 0:
                            self.menu = 9
                            self.page -= 1

                if self.found_character == []:
                    self.is_visible = False
