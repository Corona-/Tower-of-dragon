#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sitecustomize
import sys

import title
import city
import tower
import temple
import shop
import inn
import castle
import bar
import house
import dungeon

import party
import character
import character_make
import item

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
HOUSE = 11

CHARACTER_MAKE = 10

DUNGEON = 100


SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_BLACK = (0,0,0)

class tower_of_dragon:

    def __init__(self):
        pygame.init() # need to initialize pygame
        self.screen = pygame.display.set_mode(SCREEN_RECTANGLE.size) # creates screen of SCREEN_SIZE

        pygame.display.set_caption(u"天龍の塔") # set the words on title bar

        self.title = title.Title()
        self.city = city.City()
        self.tower = tower.Tower()
        self.temple = temple.Temple()
        self.shop = shop.Shop()
        self.inn = inn.Inn()
        self.castle = castle.Castle()
        self.bar = bar.Bar()
        self.house = house.House()
        self.dungeon = dungeon.Dungeon()

        self.party = party.Party()
        self.character_make = character_make.Character_make()

        self.game_state = TITLE

        self.characters = []

        self.cursor_se = pygame.mixer.Sound("SE/decide.wav")
        self.select_se = pygame.mixer.Sound("SE/decide.wav")
        self.cancel_se = pygame.mixer.Sound("SE/se_sab07.wav")

        self.item_data = []
        temp = []
        file = "Data/item_data.csv"
        fp = open(file, "r")

        for line in fp:
            temp = line[:-1].split(',')
            self.item_data.append(temp)

        self.magic_data = []
        temp = []
        file = "Data/magic_data.csv"
        fp = open(file, "r")

        for line in fp:
            temp = line[:-1].split(',')
            self.magic_data.append(temp)
            

        self.mainloop()

        



    def mainloop(self):
        """main loop"""
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            self.update()
            self.render()

            pygame.display.update()  # update the screen
        
            self.check_event()


     
    def update(self):
        """update game status"""
        if self.game_state == TITLE:
            self.title.update()
        elif self.game_state == CITY:
            self.city.update()
        elif self.game_state == BAR:
            self.bar.update()
        elif self.game_state == SHOP:
            self.shop.update()            
        elif self.game_state == INN:
            self.inn.update()
        elif self.game_state == HOUSE:
            self.house.update()
        elif self.game_state == TEMPLE:
            self.temple.update()            
        elif self.game_state == CASTLE:
            self.castle.update()            
        elif self.game_state == TOWER:
            self.tower.update()
        elif self.game_state == CHARACTER_MAKE:
            self.character_make.update()
        elif self.game_state == DUNGEON:
            self.dungeon.update()


    def render(self):
        """rendering of objects"""
        #fill background with black
        self.screen.fill(COLOR_BLACK)

        if self.game_state != TITLE and self.game_state != DUNGEON:
            self.party.draw(self.screen)

        if self.game_state == TITLE:
            self.title.draw(self.screen)
        elif self.game_state == CITY:
            self.city.draw(self.screen, self)
        elif self.game_state == BAR:
            self.bar.draw(self.screen, self)
        elif self.game_state == SHOP:
            self.shop.draw(self.screen, self)
        elif self.game_state == INN:
            self.inn.draw(self.screen, self)
        elif self.game_state == HOUSE:
            self.house.draw(self.screen, self)
        elif self.game_state == TEMPLE:
            self.temple.draw(self.screen, self)
        elif self.game_state == CASTLE:
            self.castle.draw(self.screen, self, self.characters)
        elif self.game_state == TOWER:
            self.tower.draw(self.screen)
        elif self.game_state == CHARACTER_MAKE:
            self.character_make.draw(self, self.screen)
        elif self.game_state == DUNGEON:
            self.dungeon.draw(self, self.screen)




      
    def check_event(self):
        """event handler"""

        for event in pygame.event.get():  # create function of events

            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):  # event to end program
                    pygame.quit()
                    sys.exit()

            if self.game_state == TITLE:
                title.title_handler(self, event)
            elif self.game_state == CITY:
                city.city_handler(self, event)
            elif self.game_state == BAR:
                bar.bar_handler(self, event)
            elif self.game_state == SHOP:
                shop.shop_handler(self, event)
            elif self.game_state == INN:
                inn.inn_handler(self, event)
            elif self.game_state == HOUSE:
                self.house.house_handler(self, event)
            elif self.game_state == TEMPLE:
                temple.temple_handler(self, event)
            elif self.game_state == CASTLE:
                castle.castle_handler(self, event)
            elif self.game_state == TOWER:
                tower.tower_handler(self, event)
            elif self.game_state == CHARACTER_MAKE:
                character_make.character_make_handler(self, event)
            elif self.game_state == DUNGEON:
                self.dungeon.dungeon_handler(self, event)




if __name__== "__main__":
    tower_of_dragon()
