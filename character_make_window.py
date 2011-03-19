#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import random

import character
import character_make
import window

import string

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)


class Alignment_window(window.Window):

    GOOD, NEUTRAL, EVIL = 0, 1, 2
    MENU_MAX = 2


    def __init__(self, rectangle):
        window.Window.__init__(self, rectangle)
        self.menu = self.GOOD

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.is_visible = True

    def draw(self, screen):
        """draw the window on the screen"""
        window.Window.draw(self, screen)        
        if self.is_visible == False: return

        alignment_select_font = self.menu_font.render(u"アライメント選択", True, COLOR_WHITE)
        good_font = self.menu_font.render(u"善", True, COLOR_WHITE)
        neutral_font = self.menu_font.render(u"中立", True, COLOR_WHITE)
        evil_font = self.menu_font.render(u"悪", True, COLOR_WHITE)

        screen.blit(alignment_select_font, (self.centerx-(alignment_select_font.get_width())/2, self.top+20 ))

        #set cursors for menu item
        if self.menu == self.GOOD:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+45 , (self.right-self.left)-8,30), 0)
        elif self.menu == self.NEUTRAL:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+75 , (self.right-self.left)-8,30), 0)
        elif self.menu == self.EVIL:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+105 , (self.right-self.left)-8,30), 0)
  
        #draw each alignment        
        screen.blit(good_font, (self.centerx-good_font.get_width()/2, self.top+50))
        screen.blit(neutral_font, (self.centerx-neutral_font.get_width()/2, self.top+80))
        screen.blit(evil_font, (self.centerx-evil_font.get_width()/2, self.top+110))

        #draw the possible jobs by that alignment
        job_font = self.menu_font.render(u"選択可能職業", True, COLOR_WHITE)
        warrior_font = self.menu_font.render(u"戦士", True, COLOR_WHITE)
        fighter_font = self.menu_font.render(u"武士", True, COLOR_WHITE) 
        magician_font = self.menu_font.render(u"魔術師", True, COLOR_WHITE) 
        priest_font = self.menu_font.render(u"僧侶", True, COLOR_WHITE) 
        thief_font = self.menu_font.render(u"盗賊", True, COLOR_WHITE)
        merchant_font = self.menu_font.render(u"商人", True, COLOR_WHITE)

        centerx = Rect(self.right+10, self.top, 150, 200).centerx
        possible_job_window = window.Window(Rect(self.right+10, self.top, 150, 240))
        possible_job_window.draw(screen)

        screen.blit(job_font, (465 , self.top+20))

        screen.blit(warrior_font, (centerx - warrior_font.get_width()/2 , self.top+50))
        screen.blit(fighter_font, (centerx - fighter_font.get_width()/2 , self.top+80))
        screen.blit(magician_font, (centerx - magician_font.get_width()/2 , self.top+110))
        screen.blit(priest_font, (centerx - priest_font.get_width()/2 , self.top+140))
        screen.blit(thief_font, (centerx - thief_font.get_width()/2 , self.top+170))
        screen.blit(merchant_font, (centerx - merchant_font.get_width()/2, self.top+200))
        


    def alignment_window_handler(self, game_self, event):

        if event.type == KEYUP and event.key == K_x:
            game_self.character_make.fieldvalues = []

        if event.type == KEYUP and event.key == K_UP: #moves the cursor up
            self.menu -= 1
            if self.menu < 0:
                self.menu = self.MENU_MAX
        elif event.type == KEYUP and event.key == K_DOWN:
            self.menu += 1
            if self.menu > self.MENU_MAX:
                self.menu = 0

        if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
            if self.menu == self.GOOD:
                game_self.character_make.alignment = 1
            elif self.menu == self.NEUTRAL:
                game_self.character_make.alignment = 0
            elif self.menu == self.EVIL:
                game_self.character_make.alignment = -1
            self.is_visible = False
            game_self.character_make.job_window.is_visible = True


class Job_window(window.Window):

    WARRIOR, FIGHTER, MAGICIAN, PRIEST, THIEF, MERCHANT = 0, 1, 2, 3, 4, 5
    MENU_MAX = 5
    
    def __init__(self, rectangle):
        window.Window.__init__(self, rectangle)
        self.menu = self.WARRIOR

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.is_visible = False

    def draw(self, character_make, screen):
        """draw the window on the screen"""
        window.Window.draw(self, screen)        
        if self.is_visible == False: return


       #set cursors for menu item
        if self.menu == self.WARRIOR:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+45 , (self.right-self.left)-8,30), 0)
        elif self.menu == self.FIGHTER:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+75 , (self.right-self.left)-8,30), 0)
        elif self.menu == self.MAGICIAN:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+105 , (self.right-self.left)-8,30), 0)
        elif self.menu == self.PRIEST:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+135 , (self.right-self.left)-8,30), 0)
        elif self.menu == self.THIEF:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+165 , (self.right-self.left)-8,30), 0)
        elif self.menu == self.MERCHANT:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+195 , (self.right-self.left)-8,30), 0)

        #if job is pointed, it show its job's ability
        #if job is selected, it the ability is chosen
        if self.menu == self.WARRIOR:
            character_make.strength = 10
            character_make.intelligence = 5
            character_make.piety = 8
            character_make.vitality = 12
            character_make.agility = 8
            character_make.luck = 8            
        elif self.menu == self.FIGHTER:
            character_make.strength = 12
            character_make.intelligence = 8
            character_make.piety = 8
            character_make.vitality = 10
            character_make.agility = 8
            character_make.luck = 5           
        elif self.menu == self.MAGICIAN:
            character_make.strength = 8
            character_make.intelligence = 12
            character_make.piety = 8
            character_make.vitality = 5
            character_make.agility = 10
            character_make.luck = 8            
        elif self.menu == self.PRIEST:  
            character_make.strength = 8
            character_make.intelligence = 8
            character_make.piety = 12
            character_make.vitality = 10
            character_make.agility = 5
            character_make.luck = 8            
        elif self.menu == self.THIEF:  
            character_make.strength = 8
            character_make.intelligence = 8
            character_make.piety = 5
            character_make.vitality = 8
            character_make.agility = 12
            character_make.luck = 10           
        elif self.menu == self.MERCHANT:
            character_make.strength = 5
            character_make.intelligence = 8
            character_make.piety = 8
            character_make.vitality = 8
            character_make.agility = 10
            character_make.luck = 12          



        #draw the possible jobs
        job_select_font = self.menu_font.render(u"職業選択", True, COLOR_WHITE)
        warrior_font = self.menu_font.render(u"戦士", True, COLOR_WHITE)
        fighter_font = self.menu_font.render(u"武士", True, COLOR_WHITE) 
        magician_font = self.menu_font.render(u"魔術師", True, COLOR_WHITE) 
        priest_font = self.menu_font.render(u"僧侶", True, COLOR_WHITE) 
        thief_font = self.menu_font.render(u"盗賊", True, COLOR_WHITE)
        merchant_font = self.menu_font.render(u"商人", True, COLOR_WHITE)

        screen.blit(job_select_font, (self.centerx-(job_select_font.get_width())/2, self.top+20 ))
        screen.blit(warrior_font, (self.centerx-(warrior_font.get_width())/2, self.top+50 ))
        screen.blit(fighter_font, (self.centerx-(fighter_font.get_width())/2, self.top+80 ))
        screen.blit(magician_font, (self.centerx-(magician_font.get_width())/2, self.top+110 ))
        screen.blit(priest_font, (self.centerx-(priest_font.get_width())/2, self.top+140 ))
        screen.blit(thief_font, (self.centerx-(thief_font.get_width())/2, self.top+170 ))
        screen.blit(merchant_font, (self.centerx-(merchant_font.get_width())/2, self.top+200 ))


    def job_window_handler(self, game_self, event):

        if event.type == KEYUP and event.key == K_x:
            self.menu = self.WARRIOR
            self.is_visible = False

            #initilaize everything from job window
            game_self.character_make.alignment = None
            game_self.character_make.alignment_window.is_visible = True

            game_self.character_make.strength = 0
            game_self.character_make.intelligence = 0
            game_self.character_make.piety = 0
            game_self.character_make.vitality = 0
            game_self.character_make.agility = 0
            game_self.character_make.luck = 0

        if event.type == KEYUP and event.key == K_UP: #moves the cursor up
            self.menu -= 1
            if self.menu < 0:
                self.menu = self.MENU_MAX
        elif event.type == KEYUP and event.key == K_DOWN:
            self.menu += 1
            if self.menu > self.MENU_MAX:
                self.menu = 0

        if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
            if self.menu == self.WARRIOR:
                game_self.character_make.job = 0
            elif self.menu == self.FIGHTER:
                game_self.character_make.job = 1
            elif self.menu == self.MAGICIAN:
                game_self.character_make.job = 2
            elif self.menu == self.PRIEST:
                game_self.character_make.job = 3
            elif self.menu == self.THIEF:
                game_self.character_make.job = 4
            elif self.menu == self.MERCHANT:
                game_self.character_make.job = 5
            self.is_visible = False
            game_self.character_make.bonus_window.is_visible = True

class Bonus_window(window.Window):

    STRENGTH, INTELLIGENCE, PIETY, VITALITY, AGILITY, LUCK = 0, 1, 2, 3, 4, 5
    MENU_MAX = 5
    
    def __init__(self, rectangle):
        window.Window.__init__(self, rectangle)
        self.menu = self.STRENGTH

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.is_visible = False

    def draw(self, character_make, screen):
        """draw the window on the screen"""
        window.Window.draw(self, screen)        
        if self.is_visible == False: return

       #set cursors for menu item
        if self.menu == self.STRENGTH:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+45 , (self.right-self.left)-8,30), 0)
        elif self.menu == self.INTELLIGENCE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+75 , (self.right-self.left)-8,30), 0)
        elif self.menu == self.PIETY:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+105 , (self.right-self.left)-8,30), 0)
        elif self.menu == self.VITALITY:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+135 , (self.right-self.left)-8,30), 0)
        elif self.menu == self.AGILITY:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+165 , (self.right-self.left)-8,30), 0)
        elif self.menu == self.LUCK:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+195 , (self.right-self.left)-8,30), 0)

        #draw status items
        bonus_select_font = self.menu_font.render(u"ボーナス振り分け", True, COLOR_WHITE)
        strength_font = self.menu_font.render(u"力：", True, COLOR_WHITE)
        intelligence_font = self.menu_font.render(u"知恵:", True, COLOR_WHITE) 
        piety_font = self.menu_font.render(u"信仰:", True, COLOR_WHITE) 
        vitality_font = self.menu_font.render(u"生命力:", True, COLOR_WHITE) 
        agility_font = self.menu_font.render(u"素早さ:", True, COLOR_WHITE)
        luck_font = self.menu_font.render(u"運:", True, COLOR_WHITE)

        screen.blit(bonus_select_font, (self.centerx-(bonus_select_font.get_width())/2, self.top+20 ))
        
        screen.blit(strength_font, (self.left + 20, self.top+50 ))
        screen.blit(intelligence_font, (self.left + 20, self.top+80 ))
        screen.blit(piety_font, (self.left + 20, self.top+110 ))
        screen.blit(vitality_font, (self.left + 20, self.top+140 ))
        screen.blit(agility_font, (self.left + 20, self.top+170 ))
        screen.blit(luck_font, (self.left + 20, self.top+200 ))

        #draw bonus points on status
        strength_plus_font = self.menu_font.render("".join(str(character_make.strength_plus)), True, COLOR_WHITE)
        intelligence_plus_font = self.menu_font.render("".join(str(character_make.intelligence_plus)), True, COLOR_WHITE) 
        piety_plus_font = self.menu_font.render("".join(str(character_make.piety_plus)), True, COLOR_WHITE) 
        vitality_plus_font = self.menu_font.render("".join(str(character_make.vitality_plus)), True, COLOR_WHITE) 
        agility_plus_font = self.menu_font.render("".join(str(character_make.agility_plus)), True, COLOR_WHITE)
        luck_plus_font = self.menu_font.render("".join(str(character_make.luck_plus)), True, COLOR_WHITE)

        screen.blit(strength_plus_font, (self.right-60 , self.top+50 ))
        screen.blit(intelligence_plus_font, (self.right-60 , self.top+80 ))
        screen.blit(piety_plus_font, (self.right-60 , self.top+110 ))
        screen.blit(vitality_plus_font, (self.right-60 , self.top+140 ))
        screen.blit(agility_plus_font, (self.right-60 , self.top+170 ))
        screen.blit(luck_plus_font, (self.right-60 , self.top+200 ))


        #draw the remaining points
        bonus_remaining_window = window.Window(Rect(self.right+10, self.top, 160, 100))
        bonus_remaining_window.draw(screen)

        bonus_remaining_font = self.menu_font.render(u"ボーナス残り：", True, COLOR_WHITE)
        points_font = self.menu_font.render("".join(str(character_make.bonus_point)), True, COLOR_WHITE)

        screen.blit(bonus_remaining_font, (self.right+95-(bonus_remaining_font.get_width())/2, self.top+20 ))
        screen.blit(points_font, (self.right+95 -(points_font.get_width())/2, self.top+50 ))

        

    def bonus_window_handler(self, game_self, event):

        if event.type == KEYUP and event.key == K_x:
            self.menu = self.STRENGTH
            self.is_visible = False

            game_self.character_make.job = None

            #initilaize everything from bonus
            game_self.character_make.job_window.is_visible = True
            #initialize bonus points
            game_self.character_make.strength_plus = 0
            game_self.character_make.intelligence_plus = 0
            game_self.character_make.piety_plus = 0
            game_self.character_make.vitality_plus = 0
            game_self.character_make.agility_plus = 0
            game_self.character_make.luck_plus = 0
            game_self.character_make.bonus_point = game_self.character_make.max_bonus_point



        if event.type == KEYUP and event.key == K_UP: #moves the cursor up
            self.menu -= 1
            if self.menu < 0:
                self.menu = self.MENU_MAX
        elif event.type == KEYUP and event.key == K_DOWN:
            self.menu += 1
            if self.menu > self.MENU_MAX:
                self.menu = 0

        #adds bonus points if it is below max
        if event.type == KEYUP and event.key == K_RIGHT:
            if self.menu == self.STRENGTH:
                if game_self.character_make.strength_plus < 10 and game_self.character_make.bonus_point > 0:
                    game_self.character_make.strength_plus += 1
                    game_self.character_make.bonus_point -= 1
            if self.menu == self.INTELLIGENCE:
                if game_self.character_make.intelligence_plus < 10 and game_self.character_make.bonus_point > 0:
                    game_self.character_make.intelligence_plus += 1
                    game_self.character_make.bonus_point -= 1
            if self.menu == self.PIETY:
                if game_self.character_make.piety_plus < 10 and game_self.character_make.bonus_point > 0:
                    game_self.character_make.piety_plus += 1
                    game_self.character_make.bonus_point -= 1
            if self.menu == self.VITALITY:
                if game_self.character_make.vitality_plus < 10 and game_self.character_make.bonus_point > 0:
                    game_self.character_make.vitality_plus += 1
                    game_self.character_make.bonus_point -= 1
            if self.menu == self.AGILITY:
                if game_self.character_make.agility_plus < 10 and game_self.character_make.bonus_point > 0:
                    game_self.character_make.agility_plus += 1
                    game_self.character_make.bonus_point -= 1
            if self.menu == self.LUCK:
                if game_self.character_make.luck_plus < 10 and game_self.character_make.bonus_point > 0:
                    game_self.character_make.luck_plus += 1
                    game_self.character_make.bonus_point -= 1
                    
        #decreases the bonus if it is greater than 0    
        if event.type == KEYUP and event.key == K_LEFT: 
            if self.menu == self.STRENGTH:
                if game_self.character_make.strength_plus > 0:
                    game_self.character_make.strength_plus -= 1
                    game_self.character_make.bonus_point += 1
            if self.menu == self.INTELLIGENCE:
                if game_self.character_make.intelligence_plus > 0:
                    game_self.character_make.intelligence_plus -= 1
                    game_self.character_make.bonus_point += 1
            if self.menu == self.PIETY:
                if game_self.character_make.piety_plus > 0:
                    game_self.character_make.piety_plus -= 1
                    game_self.character_make.bonus_point += 1
            if self.menu == self.VITALITY:
                if game_self.character_make.vitality_plus > 0:
                    game_self.character_make.vitality_plus -= 1
                    game_self.character_make.bonus_point += 1
            if self.menu == self.AGILITY:
                if game_self.character_make.agility_plus > 0:
                    game_self.character_make.agility_plus -= 1
                    game_self.character_make.bonus_point += 1
            if self.menu == self.LUCK:
                if game_self.character_make.luck_plus > 0:
                    game_self.character_make.luck_plus -= 1
                    game_self.character_make.bonus_point += 1


        if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
            self.is_visible = False
            game_self.character_make.select_window.is_visible = True


            
class Select_window(window.Window):

    YES, NO = 0, 1
    MENU_MAX = 1
    
    def __init__(self, rectangle):
        window.Window.__init__(self, rectangle)
        self.menu = self.YES

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.is_visible = False


    def draw(self, screen):
        """draw the window on the screen"""
        window.Window.draw(self, screen)        
        if self.is_visible == False: return

       #set cursors for menu item
        if self.menu == self.YES:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+45 , (self.right-self.left)-8,30), 0)
        elif self.menu == self.NO:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(self.left+4 ,self.top+75 , (self.right-self.left)-8,30), 0)


        #draw select items
        select_font = self.menu_font.render(u"この冒険者の登録を許可しますか？", True, COLOR_WHITE)
        yes_font = self.menu_font.render(u"はい", True, COLOR_WHITE)
        no_font = self.menu_font.render(u"いいえ", True, COLOR_WHITE) 

        screen.blit(select_font, (self.centerx-(select_font.get_width())/2, self.top+20 ))
        
        screen.blit(yes_font, (self.centerx-(yes_font.get_width())/2, self.top+50 ))
        screen.blit(no_font, (self.centerx-(no_font.get_width())/2, self.top+80 ))

    def select_window_handler(self, game_self, event):

        if event.type == KEYUP and event.key == K_x:
            self.menu = self.YES
            self.is_visible = False

            game_self.character_make.bonus_window.is_visible = True

        if event.type == KEYUP and event.key == K_UP: #moves the cursor up
            self.menu -= 1
            if self.menu < 0:
                self.menu = self.MENU_MAX
        elif event.type == KEYUP and event.key == K_DOWN:
            self.menu += 1
            if self.menu > self.MENU_MAX:
                self.menu = 0

        if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
            if self.menu == self.YES:
                game_self.characters.append(character.Character(game_self.character_make.name, game_self.character_make.alignment, game_self.character_make.job,
                                game_self.character_make.strength + game_self.character_make.strength_plus, game_self.character_make.intelligence + game_self.character_make.intelligence_plus, game_self.character_make.piety + game_self.character_make.piety_plus, game_self.character_make.vitality + game_self.character_make.vitality_plus, game_self.character_make.agility + game_self.character_make.agility_plus, game_self.character_make.luck + game_self.character_make.luck_plus,
                                game_self.character_make.strength+10, game_self.character_make.intelligence+10,  game_self.character_make.piety+10, game_self.character_make.vitality+10, game_self.character_make.agility+10, game_self.character_make.luck+10,
                                ))
                game_self.character_make = character_make.Character_make()
                game_self.game_state = CASTLE
                self.is_visible = False

                
            if self.menu == self.NO:
                self.menu = self.YES
                self.is_visible = False

                game_self.character_make.bonus_window.is_visible = True
                



