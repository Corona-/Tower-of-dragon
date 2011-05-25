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
TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
MENU=12

CHARACTER_MAKE = 10

SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

MENU_MAX = 1

class Dungeon:

    def __init__(self, floor):

        self.enemy_data = []
        temp = []
        file = "Data/monster.csv"
        fp = open(file, "r")

        for line in fp:
            temp = line[:-1].split(',')
            self.enemy_data.append(temp)

        self.battle = None

        self.battle_flag = 0
        
        self.music = 0

        self.door_se = pygame.mixer.Sound("SE/door1.wav")
        self.footstep_se = pygame.mixer.Sound("SE/fstep2_short.wav")


        #load images and set invisible color
        self.center1 = pygame.image.load("Images/center_1.png").convert()
        self.center2 = pygame.image.load("Images/center_2.png").convert()
        self.center3 = pygame.image.load("Images/center_3.png").convert()
        self.center4 = pygame.image.load("Images/center_4.png").convert()

        self.door1 = pygame.image.load("Images/door_1.png").convert()
        self.door2 = pygame.image.load("Images/door_2.png").convert()
        self.door3 = pygame.image.load("Images/door_3.png").convert()
        self.door4 = pygame.image.load("Images/door_4.png").convert()

        self.ceiling = pygame.image.load("Images/ceiling.png").convert()


        self.ground_center1 = pygame.image.load("Images/ground_center1.png").convert()
        self.ground_center1.set_colorkey(self.ground_center1.get_at((0,0)), RLEACCEL)

        self.ground_center2 = pygame.image.load("Images/ground_center2.png").convert()
        self.ground_center2.set_colorkey(self.ground_center2.get_at((0,0)), RLEACCEL)

        self.ground_center3 = pygame.image.load("Images/ground_center3.png").convert()
        self.ground_center3.set_colorkey(self.ground_center3.get_at((0,0)), RLEACCEL)

        self.ground_center4 = pygame.image.load("Images/ground_center4.png").convert()
        self.ground_center4.set_colorkey(self.ground_center4.get_at((0,0)), RLEACCEL)


        #load image on sides, param = name of file, width of image, height of image, first image invisible x, y, second x, y
        self.ground_sideList1 = load_side_images("Images/ground_side1.png", 64, 32, 63, 16, 0, 16)
        self.ground_sideList2 = load_side_images("Images/ground_side2.png", 192, 128, 190, 120, 0, 120)
        self.ground_sideList3 = load_side_images("Images/ground_side3.png", 384, 64, 0, 0, 0, 20)
        self.ground_sideList3_2 = load_side_images("Images/ground_side3-2.png", 64, 22, 40, 20, 0, 10)
        self.ground_sideList4 = load_side_images("Images/ground_side4.png", 160, 32, 0, 0, 0, 10)
        self.ground_sideList4_2 = load_side_images("Images/ground_side4-2.png", 224, 32, 220, 30, 0, 10)


        self.edgeList1 = load_side_images("Images/edge_1.png", 256, 1024, 1, 0, 1, 0)
        self.edgeList2 = load_side_images("Images/edge_2.png", 128, 512, 1, 0, 1, 0)
        self.edgeList3 = load_side_images("Images/edge_3.png", 64, 256, 1, 0, 1, 0)        
        self.edgeList4 = load_side_images("Images/edge_4.png", 32, 128, 1, 0, 1, 0)

        self.edgeList3_2 = load_side_images("Images/edge_3-2.png", 192, 256, 5,0, 5, 0)
        self.edgeList4_2 = load_side_images("Images/edge_4-2.png", 96, 128, 5,0, 5, 0)

        self.edgeList3_3 = load_side_images("Images/edge_3-3.png", 320, 256, 5,0, 5, 0)
        self.edgeList4_3 = load_side_images("Images/edge_4-3.png", 160, 128, 5,0, 5, 0)
        
        self.doorList1 = load_side_images("Images/edgedoor_1.png", 256, 1024, 1, 0, 1, 0)
        self.doorList2 = load_side_images("Images/edgedoor_2.png", 128, 512, 1, 0, 1, 0)
        self.doorList3 = load_side_images("Images/edgedoor_3.png", 64, 256, 1, 0, 1, 0)        
        self.doorList4 = load_side_images("Images/edgedoor_4.png", 32, 128, 1, 0, 1, 0)

        self.doorList3_2 = load_side_images("Images/edgedoor_3-2.png", 192, 256, 5, 0, 5, 0)
        self.doorList4_2 = load_side_images("Images/edgedoor_4-2.png", 96, 128, 5, 0, 5, 0)

        self.doorList3_3 = load_side_images("Images/edgedoor_3-3.png", 320, 256, 5, 0, 5, 0)
        self.doorList4_3 = load_side_images("Images/edgedoor_4-3.png", 160, 128, 5, 0, 5, 0)


        #load ceiling images
        self.ceiling2 = pygame.image.load("Images/ceiling_2.png").convert()
        surface = pygame.Surface((512,128))
        surface.blit(self.ceiling2, (0,0), (0,0,512,128))
        surface.set_colorkey(surface.get_at((0,1)), RLEACCEL)
        surface.convert()
        self.ceiling2 = surface

        self.ceiling3 = pygame.image.load("Images/ceiling_3.png").convert()
        surface = pygame.Surface((256,64))
        surface.blit(self.ceiling3, (0,0), (0,0,256,64))
        surface.set_colorkey(surface.get_at((0,1)), RLEACCEL)
        surface.convert()
        self.ceiling3 = surface
        
        self.ceiling4 = pygame.image.load("Images/ceiling_4.png").convert()
        surface = pygame.Surface((128,32))
        surface.blit(self.ceiling4, (0,0), (0,0,128,32))
        surface.set_colorkey(surface.get_at((0,1)), RLEACCEL)
        surface.convert()
        self.ceiling4 = surface
        
        self.ceilingedgeList2 = load_side_images("Images/ceilingedge_2.png", 192, 128, 191, 0, 0, 0)
        self.ceilingedgeList3 = load_side_images("Images/ceilingedge_3.png", 384, 64, 0, 10, 0, 0)
        self.ceilingedgeList4 = load_side_images("Images/ceilingedge_4.png", 160, 32, 0, 10, 0, 0)
        self.ceilingedgeList3_2 = load_side_images("Images/ceilingedge_3-2.png", 192, 64, 20, 0, 0, 0)
        self.ceilingedgeList4_2 = load_side_images("Images/ceilingedge_4-2.png", 224, 32, 0, 10, 0, 0)

        
        #load the map of the dungeon
        file = "tower_of_dragon.txt"
        fp = open(file, "r")

        map_data = fp.readlines()

        #set up the arrays for the dungeon first floor
        self.vertical_wall = []
        self.horizontal_wall = []
        self.ground = []
        self.space = []
        self.object = []

        self.temp = []

        self.floor = floor-1

        #reads as left top is 0,0 and right down is 19,19
        for i in range(0, 20):
            for j in range(0, 21):
                self.temp.append(int(map_data[35+i+self.floor*20][j*2:j*2+2], 16))
            self.vertical_wall.append(self.temp)
            self.temp = []

        for i in range(0, 21):
            for j in range(0,20):
                self.temp.append(int(map_data[635+i+self.floor*20][j*2:j*2+2], 16))
            self.horizontal_wall.append(self.temp)
            self.temp = []

        for i in range(0, 20):
            for j in range(0,20):
                self.temp.append(int(map_data[1265+i+self.floor*20][j*2:j*2+2], 16))
            self.ground.append(self.temp)
            self.temp = []
        
        for i in range(0, 20):
            for j in range(0,20):
                self.temp.append(int(map_data[1865+i+self.floor*20][j*2:j*2+2], 16))
            self.space.append(self.temp)
            self.temp = []
            
        for i in range(0, 20):
           for j in range(0,20):
               self.temp.append(int(map_data[2465+i+self.floor*20][j*2:j*2+2], 16))
           self.object.append(self.temp)
           self.temp = []


        #draw extra window
        self.downstairs_window = None #system_notify.Confirm_window( Rect(160, 150, 380, 110) , system_notify.Confirm_window.DOWNSTAIRS)
        self.upstairs_window = None

    def update(self):

        if self.battle_flag == 1:
            self.battle.update()
            return
        
        if self.music == 0:
            pygame.mixer.music.load("BGM/yamikairou_no_hihou.mp3")
            pygame.mixer.music.play(-1)
            self.music = 1
            
        pass
    def draw(self, game_self, screen):

        game_self.party.torch = 1
        if ( game_self.party.torch >= 1 ):
            self.draw_dungeon_with_light(game_self, screen)
        else:
            self.draw_dungeon_no_light(game_self, screen)

        
        if self.battle_flag == 1:
            self.battle.draw(game_self, screen)

        if self.downstairs_window != None:
            self.downstairs_window.draw( screen, game_self, None)
        if self.upstairs_window != None:
            self.upstairs_window.draw( screen, game_self, None)

    def dungeon_handler(self, game_self, event):
        """event handler for dungeon"""

        if self.downstairs_window != None and self.downstairs_window.is_visible == True:
            self.downstairs_window.confirm_window_handler( game_self, event, None)
            return
        elif self.upstairs_window != None and self.upstairs_window.is_visible == True:
            self.upstairs_window.confirm_window_handler( game_self, event, None)
            return

        if self.battle_flag == 1:
            self.battle.battle_handler(game_self, event)
            return

        #party member all has same coordinate so take one of it
        coordinate = game_self.party.member[0].coordinate
        x = coordinate[0]
        y = coordinate[1]

        encount = random.randint(1, 100)

        if event.type == KEYDOWN and (event.key ==K_UP):
            self.footstep_se.play()
            for character in game_self.party.member:
                if (game_self.party.direction == 0):
                    #if there is a wall in front, can't move up
                    if( self.horizontal_wall[y][x] == 0):
                        character.coordinate[1] = decrement(character.coordinate[1],1)
                elif (game_self.party.direction == 1):
                    if( self.vertical_wall[y][increment(x,1)] == 0):
                        character.coordinate[0] = increment(character.coordinate[0],1)
                elif (game_self.party.direction == 2):
                    if( self.horizontal_wall[increment(y,1)][x] == 0):
                        character.coordinate[1] = increment(character.coordinate[1],1)
                elif (game_self.party.direction == 3):
                    if( self.vertical_wall[y][x] == 0):
                        character.coordinate[0] = decrement(character.coordinate[0],1)
            self.battle_encount( 10, game_self.party.member[0] )
            
        if event.type == KEYDOWN and (event.key ==K_DOWN):
            game_self.party.direction -= 2
            if game_self.party.direction < 0:
                game_self.party.direction += 4
            self.battle_encount( 5, game_self.party.member[0] )

        if event.type == KEYDOWN and (event.key ==K_LEFT):
            game_self.party.direction -= 1
            if game_self.party.direction < 0:
                game_self.party.direction = 3
            self.battle_encount( 5, game_self.party.member[0] )

        if event.type == KEYDOWN and (event.key ==K_RIGHT):
            game_self.party.direction += 1
            if game_self.party.direction > 3:
                game_self.party.direction = 0
            self.battle_encount( 5, game_self.party.member[0] )


      #print game_self.party.member[0].coordinate


        if event.type == KEYDOWN and (event.key ==K_x):
            game_self.game_state = MENU
            game_self.menu = menu.Menu()
            game_self.dungeon = None
            #for character in game_self.party.member:
            #    character.coordinate = [-1,-1,-1]
            #self.music = 0

        if event.type == KEYDOWN and (event.key ==K_z or event.key == K_SPACE or event.key == K_RETURN):
            if game_self.party.direction == 0:
                if (self.horizontal_wall[y][x] == 2):
                    self.door_se.play()
                    for character in game_self.party.member:
                        character.coordinate[1] = decrement(character.coordinate[1],1)
            if game_self.party.direction == 1:
                if self.vertical_wall[y][increment(x,1)] == 2:
                    self.door_se.play()
                    for character in game_self.party.member:
                        character.coordinate[0] = increment(character.coordinate[0],1)
            if game_self.party.direction == 2:
                if self.horizontal_wall[increment(y,1)][x] == 2:
                    self.door_se.play()
                    for character in game_self.party.member:
                        character.coordinate[1] = increment(character.coordinate[1],1)
            if game_self.party.direction == 3:
                if self.vertical_wall[y][x] == 2:
                    self.door_se.play()
                    for character in game_self.party.member:
                        character.coordinate[0] = decrement(character.coordinate[0],1)

            #find event on the new place?

            coordinate = game_self.party.member[0].coordinate
            x = coordinate[0]
            y = coordinate[1]

            #down stairs = 2, up stairs = 1, elevator = 3

            #下りる階段があります　下りますか　はい　いいえ
            if self.ground[y][x] == 2:
                self.downstairs_window = system_notify.Confirm_window( Rect(160, 150, 380, 110) , system_notify.Confirm_window.DOWNSTAIRS)
                self.downstairs_window.is_visible = True

            #上る階段があります　上りますか　はい　いいえ
            if self.ground[y][x] == 1:
                self.upstairs_window = system_notify.Confirm_window( Rect(160, 150, 380, 110) , system_notify.Confirm_window.UPSTAIRS)
                self.upstairs_window.is_visible = True
                
                    
                    
                pass

            

        #probability is out of 1 - 100
    def battle_encount( self, probability, character ):

        encount = random.randint(1, 100)

        if encount < probability:
            self.battle = battle.Battle(self.enemy_data, character.coordinate[2])
            self.battle_flag = 1

    def draw_dungeon_with_light(self, game_self, screen):
        
        #party member all has same coordinate so take one of it
        coordinate = game_self.party.member[0].coordinate
        x = coordinate[0]
        y = coordinate[1]        

        #with magic or torch, it could see up to four walls or 3 block
        #it is [y][x] since it is stored by rows

        #right now, ceiling would have nothing, so all of it needs it.
        screen.blit(self.ceiling2, (64,-64))
        screen.blit(self.ceilingedgeList2[0], (0,-64))
        screen.blit(self.ceilingedgeList2[1], (448,-64))
        screen.blit(self.ceiling3, (192,64))
        screen.blit(self.ceiling4, (256,128))
        screen.blit(self.ceilingedgeList3[0], (-64,64))
        screen.blit(self.ceilingedgeList3[1], (320,64))
        screen.blit(self.ceilingedgeList4[0], (128,128))
        screen.blit(self.ceilingedgeList4[1], (352,128))
        screen.blit(self.ceilingedgeList3_2[0], (0,64))
        screen.blit(self.ceilingedgeList3_2[1], (448,64))
        screen.blit(self.ceilingedgeList4_2[0], (0,128))
        screen.blit(self.ceilingedgeList4_2[1], (416,128))

        #if the player is looking up
        if ( game_self.party.direction == 0):
            #draw from back to front.
            #draw ground below
            if (self.ground[y][x] == 0 ):
                screen.blit(self.ground_center1, (32, 448))

            #draw ground left
            if (self.ground[y][decrement(x,1)] == 0 ):
                screen.blit(self.ground_sideList1[0], (0, 448))

            #draw ground right
            if (self.ground[y][increment(x,1)] == 0 ):
                screen.blit(self.ground_sideList1[1], (576, 448))

            #draw ground up left
            if (self.ground[decrement(y,1)][decrement(x,1)] == 0 ):
                screen.blit(self.ground_sideList2[0], (0, 320))             

            #draw ground up right
            if (self.ground[decrement(y,1)][increment(x,1)] == 0 ):
                screen.blit(self.ground_sideList2[1], (448, 320))

            #draw ground up left
            if (self.ground[decrement(y,2)][decrement(x,1)] == 0 ):
                screen.blit(self.ground_sideList3[0], (-128, 256))             

            #draw ground up right
            if (self.ground[decrement(y,2)][increment(x,1)] == 0 ):
                screen.blit(self.ground_sideList3[1], (384, 256))

            #draw ground up left
            if (self.ground[decrement(y,2)][decrement(x,2)] == 0 ):
                screen.blit(self.ground_sideList3_2[0], (0, 256))             

            #draw ground up right
            if (self.ground[decrement(y,2)][increment(x,2)] == 0 ):
                screen.blit(self.ground_sideList3_2[1], (576, 256))

            #draw ground up left
            if (self.ground[decrement(y,3)][decrement(x,1)] == 0 ):
                screen.blit(self.ground_sideList4[0], (128, 224))             

            #draw ground up right
            if (self.ground[decrement(y,3)][increment(x,1)] == 0 ):
                screen.blit(self.ground_sideList4[1], (352, 224))

            #draw ground up left
            if (self.ground[decrement(y,3)][decrement(x,2)] == 0 ):
                screen.blit(self.ground_sideList4_2[0], (0, 224))             

            #draw ground up right
            if (self.ground[decrement(y,3)][increment(x,2)] == 0 ):
                screen.blit(self.ground_sideList4_2[1], (416, 224))
                
            #draw ground up one
            if (self.ground[decrement(y,1)][x] == 0 ):
                screen.blit(self.ground_center2, (64, 320))

            #draw ground up two
            if (self.ground[decrement(y,2)][x] == 0 ):
                screen.blit(self.ground_center3, (192, 256))
                
            #draw ground up three
            if (self.ground[decrement(y,3)][x] == 0 ):
                screen.blit(self.ground_center4, (256, 224))

            #draw straight three block wall left two
            if (self.horizontal_wall[decrement(y,3)][decrement(x,2)] == 1):
                screen.blit(self.center4, (160, 160))
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,2)] == 2):
                screen.blit(self.door4, (160,160))                                               

            #draw straight three block wall left one
            if (self.horizontal_wall[decrement(y,3)][decrement(x,1)] == 1):
                screen.blit(self.center4, (224, 160))
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,1)] == 2):
                screen.blit(self.door4, (224,160))                                               

            #draw straight three block wall
            if (self.horizontal_wall[decrement(y,3)][x] == 1):
                screen.blit(self.center4, (288, 160))
            elif (self.horizontal_wall[decrement(y,3)][x] == 2):
                screen.blit(self.door4, (288,160))

            #draw straight three block wall right one
            if (self.horizontal_wall[decrement(y,3)][increment(x,1)] == 1):
                screen.blit(self.center4, (352, 160))
            elif (self.horizontal_wall[decrement(y,3)][increment(x,1)] == 2):
                screen.blit(self.door4, (352,160))                                               

            #draw straight three block wall right two
            if (self.horizontal_wall[decrement(y,3)][increment(x,2)] == 1):
                screen.blit(self.center4, (416, 160))
            elif (self.horizontal_wall[decrement(y,3)][increment(x,2)] == 2):
                screen.blit(self.door4, (416,160))
                
            #draw up three wall on left three
            if (self.vertical_wall[decrement(y,3)][decrement(x,2)] == 1):
                screen.blit(self.edgeList4_3[0], (0, 128))
            elif (self.vertical_wall[decrement(y,3)][decrement(x,2)] == 2):
                screen.blit(self.doorList4_3[0], (0, 128))

            #draw up three wall on left two
            if (self.vertical_wall[decrement(y,3)][decrement(x,1)] == 1):
                screen.blit(self.edgeList4_2[0], (128, 128))
            elif (self.vertical_wall[decrement(y,3)][decrement(x,1)] == 2):
                screen.blit(self.doorList4_2[0], (128, 128))


            #draw up three wall on left
            if (self.vertical_wall[decrement(y,3)][x] == 1):
                screen.blit(self.edgeList4[0], (256, 128))
            elif (self.vertical_wall[decrement(y,3)][x] == 2):
                screen.blit(self.doorList4[0], (256, 128))


            #draw up three wall on right three
            if (self.vertical_wall[decrement(y,3)][increment(x,3)] == 1):
                screen.blit(self.edgeList4_3[1], (480, 128))                
            elif (self.vertical_wall[decrement(y,3)][increment(x,3)] == 2):
                screen.blit(self.doorList4_3[1], (480, 128))  

            #draw up three wall on right two
            if (self.vertical_wall[decrement(y,3)][increment(x,2)] == 1):
                screen.blit(self.edgeList4_2[1], (416, 128))                
            elif (self.vertical_wall[decrement(y,3)][increment(x,2)] == 2):
                screen.blit(self.doorList4_2[1], (416, 128))                               

            #draw up three wall on right
            if (self.vertical_wall[decrement(y,3)][increment(x,1)] == 1):
                screen.blit(self.edgeList4[1], (352, 128))                
            elif (self.vertical_wall[decrement(y,3)][increment(x,1)] == 2):
                screen.blit(self.doorList4[1], (352, 128))                


            #draw straight two block wall left one
            if (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 1):
                screen.blit(self.center3, (0, 128))
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 2):
                screen.blit(self.door3, (0,128))


            #draw straight two block wall left one
            if (self.horizontal_wall[decrement(y,2)][decrement(x,1)] == 1):
                screen.blit(self.center3, (128, 128))
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,1)] == 2):
                screen.blit(self.door3, (128,128))

            #draw straight two block wall
            if (self.horizontal_wall[decrement(y,2)][x] == 1):
                screen.blit(self.center3, (256, 128))
            elif (self.horizontal_wall[decrement(y,2)][x] == 2):
                screen.blit(self.door3, (256,128))

            #draw straight two block wall right one
            if (self.horizontal_wall[decrement(y,2)][increment(x,1)] == 1):
                screen.blit(self.center3, (384, 128))
            elif (self.horizontal_wall[decrement(y,2)][increment(x,1)] == 2):
                screen.blit(self.door3, (384,128))

            #draw straight two block wall right two
            if (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 1):
                screen.blit(self.center3, (512, 128))
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 2):
                screen.blit(self.door3, (512,128))

            #draw up two wall on left three
            if (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 1):
                screen.blit(self.edgeList3_2[0], (-320, 64))
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 2):
                screen.blit(self.doorList3_2[0], (-320, 64))

            #draw up two wall on left two
            if (self.vertical_wall[decrement(y,2)][decrement(x,1)] == 1):
                screen.blit(self.edgeList3_2[0], (-64, 64))
            elif (self.vertical_wall[decrement(y,2)][decrement(x,1)] == 2):
                screen.blit(self.doorList3_2[0], (-64, 64))

            #draw up two wall on left
            if (self.vertical_wall[decrement(y,2)][x] == 1):
                screen.blit(self.edgeList3[0], (192, 64))
            elif (self.vertical_wall[decrement(y,2)][x] == 2):
                screen.blit(self.doorList3[0], (192, 64))
                
            #draw up two wall on right three
            if (self.vertical_wall[decrement(y,2)][increment(x,3)] == 1):
                screen.blit(self.edgeList3_3[1], (640, 64))                
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 2):
                screen.blit(self.doorList3_3[1], (640, 64))    


            #draw up two wall on right two
            if (self.vertical_wall[decrement(y,2)][increment(x,2)] == 1):
                screen.blit(self.edgeList3_2[1], (512, 64))                
            elif (self.vertical_wall[decrement(y,2)][increment(x,2)] == 2):
                screen.blit(self.doorList3_2[1], (512, 64))    

            #draw up two wall on right
            if (self.vertical_wall[decrement(y,2)][increment(x,1)] == 1):
                screen.blit(self.edgeList3[1], (384, 64))                
            elif (self.vertical_wall[decrement(y,2)][increment(x,1)] == 2):
                screen.blit(self.doorList3[1], (384, 64))                


            #draw straight one block wall left one
            if (self.horizontal_wall[decrement(y,1)][decrement(x,1)] == 1):
                screen.blit(self.center2, (-64, 64))
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,1)] == 2):
                screen.blit(self.door2, (-64,64))
        
            #draw straight one block wall
            if (self.horizontal_wall[decrement(y,1)][x] == 1):
                screen.blit(self.center2, (192, 64))
            elif (self.horizontal_wall[decrement(y,1)][x] == 2):
                screen.blit(self.door2, (192,64))

            #draw straight one block wall right one
            if (self.horizontal_wall[decrement(y,1)][increment(x,1)] == 1):
                screen.blit(self.center2, (448, 64))
            elif (self.horizontal_wall[decrement(y,1)][increment(x,1)] == 2):
                screen.blit(self.door2, (448,64))

            #draw up two wall on left
            if (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 1):
                screen.blit(self.edgeList2[0], (-192, -64))
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 2):
                screen.blit(self.doorList2[0], (-192, -64))
                                  

            #draw up one wall on left
            if (self.vertical_wall[decrement(y,1)][x] == 1):
                screen.blit(self.edgeList2[0], (64, -64))
            elif (self.vertical_wall[decrement(y,1)][x] == 2):
                screen.blit(self.doorList2[0], (64, -64))
                                   
            #draw up one wall on right
            if (self.vertical_wall[decrement(y,1)][increment(x,1)] == 1):
                screen.blit(self.edgeList2[1], (448, -64))                
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 2):
                screen.blit(self.doorList2[1], (448, -64))                

            #draw left one up wall
            if (self.horizontal_wall[y][decrement(x,1)] == 1):
                screen.blit(self.center1, (-448,-64))
            elif (self.horizontal_wall[y][decrement(x,1)] == 2):
                screen.blit(self.door1, (-448,-64))

            #draw right one up wall
            if (self.horizontal_wall[y][increment(x,1)] == 1):
                screen.blit(self.center1, (576,-64))
            elif (self.horizontal_wall[y][increment(x,1)] == 2):
                screen.blit(self.door1, (576,-64))

            #draw just up wall
            if (self.horizontal_wall[y][x] == 1):
                screen.blit(self.center1, (64,-64))
            elif (self.horizontal_wall[y][x] == 2):
                screen.blit(self.door1, (64,-64))

            #draw wall on left
            if (self.vertical_wall[y][x] == 1):
                screen.blit(self.edgeList1[0], (-192, -320))
            elif (self.vertical_wall[y][x] == 2):
                screen.blit(self.doorList1[0], (-192, -320))

            #draw wall on right
            if (self.vertical_wall[y][increment(x,1)] == 1):
                screen.blit(self.edgeList1[1], (576, -320))
            elif (self.vertical_wall[y][increment(x,1)] == 2):
                screen.blit(self.doorList1[1], (576, -320))



                             

##        #if player is looking right
##        elif (game_self.party.direction == 1):
##            
##            if (self.ground[y][x] == 0 ):
##                screen.blit(self.ground_center1, (32, 448))
##
##            #draw ground left
##            if (self.ground[decrement(y,1)][x] == 0 ):
##                screen.blit(self.ground_sideList1[0], (0, 448))
##
##            #draw ground right
##            if (self.ground[increment(y,1)][x] == 0 ):
##                screen.blit(self.ground_sideList1[1], (576, 448))
##
##            #draw ground up left
##            if (self.ground[decrement(y,1)][increment(x,1)] == 0 ):
##                screen.blit(self.ground_sideList2[0], (0, 320))             
##
##            #draw ground up right
##            if (self.ground[increment(y,1)][increment(x,1)] == 0 ):
##                screen.blit(self.ground_sideList2[1], (448, 320))             
##            
##            #draw ground up one
##            if (self.ground[y][increment(x,1)] == 0 ):
##                screen.blit(self.ground_center2, (64, 320))
##
##        
##            #draw straight one block wall
##            if (self.vertical_wall[y][increment(x,2)] == 1):
##                screen.blit(self.center2, (192, 64))
##            elif (self.vertical_wall[y][increment(x,2)] == 2):
##                screen.blit(self.door2, (192, 64))
##
##            #draw up one wall on left
##            if (self.horizontal_wall[y][increment(x,1)] == 1):
##                screen.blit(self.edgeList2[0], (64, -64))
##            elif (self.horizontal_wall[y][increment(x,1)] == 2):
##                screen.blit(self.doorList2[0], (64, -64))
##                
##            #draw up one wall on right
##            if (self.horizontal_wall[increment(y,1)][increment(x,1)] == 1):
##                screen.blit(self.edgeList2[1], (448, -64))                
##            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 2):
##                screen.blit(self.doorList2[1], (448, -64))                
##
##            #draw left one up wall
##            if (self.vertical_wall[decrement(y,1)][increment(x,1)] == 1):
##                screen.blit(self.center1, (-448,-64))
##            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 2):
##                screen.blit(self.door1, (-448,-64))
##
##            #draw right one up wall
##            if (self.vertical_wall[increment(y,1)][increment(x,1)] == 1):
##                screen.blit(self.center1, (576,-64))
##            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 2):
##                screen.blit(self.door1, (576,-64))
##
##            #draw just up wall
##            if (self.vertical_wall[y][increment(x,1)] == 1):
##                screen.blit(self.center1, (64,-64))
##            elif (self.vertical_wall[y][increment(x,1)] == 2):
##                screen.blit(self.door1, (64,-64))
##
##            #draw wall on left
##            if (self.horizontal_wall[y][x] == 1):
##                screen.blit(self.edgeList1[0], (-192, -320))
##            elif (self.horizontal_wall[y][x] == 2):
##                screen.blit(self.doorList1[0], (-192, -320))
##
##            #draw wall on right
##            if (self.horizontal_wall[increment(y,1)][x] == 1):
##                screen.blit(self.edgeList1[1], (576, -320))
##            elif (self.horizontal_wall[increment(y,1)][x] == 2):
##                screen.blit(self.doorList1[1], (576, -320))
##
##        #if party is looking down
##        elif (game_self.party.direction == 2):
##            
##            if (self.ground[y][x] == 0 ):
##                screen.blit(self.ground_center1, (32, 448))
##
##            #draw ground left
##            if (self.ground[y][increment(x,1)] == 0 ):
##                screen.blit(self.ground_sideList1[0], (0, 448))
##
##            #draw ground right
##            if (self.ground[y][decrement(x,1)] == 0 ):
##                screen.blit(self.ground_sideList1[1], (576, 448))
##
##            #draw ground up left
##            if (self.ground[increment(y,1)][increment(x,1)] == 0 ):
##                screen.blit(self.ground_sideList2[0], (0, 320))             
##
##            #draw ground up right
##            if (self.ground[increment(y,1)][decrement(x,1)] == 0 ):
##                screen.blit(self.ground_sideList2[1], (448, 320))             
##            
##            #draw ground up one
##            if (self.ground[increment(y,1)][x] == 0 ):
##                screen.blit(self.ground_center2, (64, 320))
##                
##        
##            #draw straight one block wall
##            if (self.horizontal_wall[increment(y,2)][x] == 1):
##                screen.blit(self.center2, (192, 64))
##            elif (self.horizontal_wall[increment(y,2)][x] == 2):
##                screen.blit(self.door2, (192, 64))
##
##            #draw up one wall on left
##            if (self.vertical_wall[increment(y,1)][increment(x,1)] == 1):
##                screen.blit(self.edgeList2[0], (64, -64))
##            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 2):
##                screen.blit(self.doorList2[0], (64, -64))
##                
##            #draw up one wall on right
##            if (self.vertical_wall[increment(y,1)][x] == 1):
##                screen.blit(self.edgeList2[1], (448, -64))                
##            elif (self.vertical_wall[increment(y,1)][x] == 2):
##                screen.blit(self.doorList2[1], (448, -64))                
##
##            #draw left one up wall
##            if (self.horizontal_wall[increment(y,1)][increment(x,1)] == 1):
##                screen.blit(self.center1, (-448,-64))
##            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 2):
##                screen.blit(self.door1, (-448,-64))
##
##            #draw right one up wall
##            if (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 1):
##                screen.blit(self.center1, (576,-64))
##            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 2):
##                screen.blit(self.door1, (576,-64))
##
##            #draw just up wall
##            if (self.horizontal_wall[increment(y,1)][x] == 1):
##                screen.blit(self.center1, (64,-64))
##            if (self.horizontal_wall[increment(y,1)][x] == 2):
##                screen.blit(self.door1, (64,-64))
##
##            #draw wall on left
##            if (self.vertical_wall[y][increment(x,1)] == 1):
##                screen.blit(self.edgeList1[0], (-192, -320))
##            elif (self.vertical_wall[y][increment(x,1)] == 2):
##                screen.blit(self.doorList1[0], (-192, -320))
##
##            #draw wall on right
##            if (self.vertical_wall[y][x] == 1):
##                screen.blit(self.edgeList1[1], (576, -320))
##            elif (self.vertical_wall[y][x] == 2):
##                screen.blit(self.doorList1[1], (576, -320))
##
##        #if the player is looking left
##        elif (game_self.party.direction == 3):
##
##            if (self.ground[y][x] == 0 ):
##                screen.blit(self.ground_center1, (32, 448))
##
##            #draw ground left
##            if (self.ground[increment(y,1)][x] == 0 ):
##                screen.blit(self.ground_sideList1[0], (0, 448))
##
##            #draw ground right
##            if (self.ground[decrement(y,1)][x] == 0 ):
##                screen.blit(self.ground_sideList1[1], (576, 448))
##
##            #draw ground up left
##            if (self.ground[increment(y,1)][decrement(x,1)] == 0 ):
##                screen.blit(self.ground_sideList2[0], (0, 320))             
##
##            #draw ground up right
##            if (self.ground[decrement(y,1)][decrement(x,1)] == 0 ):
##                screen.blit(self.ground_sideList2[1], (448, 320))             
##            
##            #draw ground up one
##            if (self.ground[y][decrement(x,1)] == 0 ):
##                screen.blit(self.ground_center2, (64, 320))
##
##        
##            #draw straight one block wall
##            if (self.vertical_wall[y][decrement(x,1)] == 1):
##                screen.blit(self.center2, (192, 64))
##            elif (self.vertical_wall[y][decrement(x,1)] == 2):
##                screen.blit(self.door2, (192, 64))
##
##            #draw up one wall on left
##            if (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 1):
##                screen.blit(self.edgeList2[0], (64, -64))
##            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 2):
##                screen.blit(self.doorList2[0], (64, -64))
##                
##            #draw up one wall on right
##            if (self.horizontal_wall[y][decrement(x,1)] == 1):
##                screen.blit(self.edgeList2[1], (448, -64))                
##            elif (self.horizontal_wall[y][decrement(x,1)] == 2):
##                screen.blit(self.doorList2[1], (448, -64))                
##
##            #draw left one up wall
##            if (self.vertical_wall[increment(y,1)][x] == 1):
##                screen.blit(self.center1, (-448,-64))
##            elif (self.vertical_wall[increment(y,1)][x] == 2):
##                screen.blit(self.door1, (-448,-64))
##
##            #draw right one up wall
##            if (self.vertical_wall[decrement(y,1)][x] == 1):
##                screen.blit(self.center1, (576,-64))
##            if (self.vertical_wall[decrement(y,1)][x] == 2):
##                screen.blit(self.door1, (576,-64))
##
##            #draw just up wall
##            if (self.vertical_wall[y][x] == 1):
##                screen.blit(self.center1, (64,-64))
##            elif (self.vertical_wall[y][x] == 2):
##                screen.blit(self.door1, (64,-64))
##
##            #draw wall on left
##            if (self.horizontal_wall[increment(y,1)][x] == 1):
##                screen.blit(self.edgeList1[0], (-192, -320))
##            elif (self.horizontal_wall[increment(y,1)][x] == 2):
##                screen.blit(self.doorList1[0], (-192, -320))
##
##            #draw wall on right
##            if (self.horizontal_wall[y][x] == 1):
##                screen.blit(self.edgeList1[1], (576, -320))
##            elif (self.horizontal_wall[y][x] == 2):
##                screen.blit(self.doorList1[1], (576, -320))


    def draw_dungeon_no_light(self, game_self, screen):

        #party member all has same coordinate so take one of it
        coordinate = game_self.party.member[0].coordinate
        x = coordinate[0]
        y = coordinate[1]
        
        #without magic or torch, it could see up to two walls or one block
        #it is [y][x] since it is stored by rows

        #right now, ceiling would have nothing, so all of it needs it.
        screen.blit(self.ceiling2, (64,-64))
        screen.blit(self.ceilingedgeList2[0], (0,-64))
        screen.blit(self.ceilingedgeList2[1], (448,-64))

        #if the player is looking up
        if ( game_self.party.direction == 0):
            #draw from back to front.
            #draw ground below
            if (self.ground[y][x] == 0 ):
                screen.blit(self.ground_center1, (32, 448))

            #draw ground left
            if (self.ground[y][decrement(x,1)] == 0 ):
                screen.blit(self.ground_sideList1[0], (0, 448))

            #draw ground right
            if (self.ground[y][increment(x,1)] == 0 ):
                screen.blit(self.ground_sideList1[1], (576, 448))

            #draw ground up left
            if (self.ground[decrement(y,1)][decrement(x,1)] == 0 ):
                screen.blit(self.ground_sideList2[0], (0, 320))             

            #draw ground up right
            if (self.ground[decrement(y,1)][increment(x,1)] == 0 ):
                screen.blit(self.ground_sideList2[1], (448, 320))             
            
            #draw ground up one
            if (self.ground[decrement(y,1)][x] == 0 ):
                screen.blit(self.ground_center2, (64, 320))
        
            #draw straight one block wall
            if (self.horizontal_wall[decrement(y,1)][x] == 1):
                screen.blit(self.center2, (192, 64))
            elif (self.horizontal_wall[decrement(y,1)][x] == 2):
                screen.blit(self.door2, (192,64))

            #draw up one wall on left
            if (self.vertical_wall[decrement(y,1)][x] == 1):
                screen.blit(self.edgeList2[0], (64, -64))
            elif (self.vertical_wall[decrement(y,1)][x] == 2):
                screen.blit(self.doorList2[0], (64, -64))
                                   
            #draw up one wall on right
            if (self.vertical_wall[decrement(y,1)][increment(x,1)] == 1):
                screen.blit(self.edgeList2[1], (448, -64))                
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 2):
                screen.blit(self.doorList2[1], (448, -64))                

            #draw left one up wall
            if (self.horizontal_wall[y][decrement(x,1)] == 1):
                screen.blit(self.center1, (-448,-64))
            elif (self.horizontal_wall[y][decrement(x,1)] == 2):
                screen.blit(self.door1, (-448,-64))

            #draw right one up wall
            if (self.horizontal_wall[y][increment(x,1)] == 1):
                screen.blit(self.center1, (576,-64))
            elif (self.horizontal_wall[y][increment(x,1)] == 2):
                screen.blit(self.door1, (576,-64))

            #draw just up wall
            if (self.horizontal_wall[y][x] == 1):
                screen.blit(self.center1, (64,-64))
            elif (self.horizontal_wall[y][x] == 2):
                screen.blit(self.door1, (64,-64))

            #draw wall on left
            if (self.vertical_wall[y][x] == 1):
                screen.blit(self.edgeList1[0], (-192, -320))
            elif (self.vertical_wall[y][x] == 2):
                screen.blit(self.doorList1[0], (-192, -320))

            #draw wall on right
            if (self.vertical_wall[y][increment(x,1)] == 1):
                screen.blit(self.edgeList1[1], (576, -320))
            elif (self.vertical_wall[y][increment(x,1)] == 2):
                screen.blit(self.doorList1[1], (576, -320))

        #if player is looking right
        elif (game_self.party.direction == 1):
            
            if (self.ground[y][x] == 0 ):
                screen.blit(self.ground_center1, (32, 448))

            #draw ground left
            if (self.ground[decrement(y,1)][x] == 0 ):
                screen.blit(self.ground_sideList1[0], (0, 448))

            #draw ground right
            if (self.ground[increment(y,1)][x] == 0 ):
                screen.blit(self.ground_sideList1[1], (576, 448))

            #draw ground up left
            if (self.ground[decrement(y,1)][increment(x,1)] == 0 ):
                screen.blit(self.ground_sideList2[0], (0, 320))             

            #draw ground up right
            if (self.ground[increment(y,1)][increment(x,1)] == 0 ):
                screen.blit(self.ground_sideList2[1], (448, 320))             
            
            #draw ground up one
            if (self.ground[y][increment(x,1)] == 0 ):
                screen.blit(self.ground_center2, (64, 320))

        
            #draw straight one block wall
            if (self.vertical_wall[y][increment(x,2)] == 1):
                screen.blit(self.center2, (192, 64))
            elif (self.vertical_wall[y][increment(x,2)] == 2):
                screen.blit(self.door2, (192, 64))

            #draw up one wall on left
            if (self.horizontal_wall[y][increment(x,1)] == 1):
                screen.blit(self.edgeList2[0], (64, -64))
            elif (self.horizontal_wall[y][increment(x,1)] == 2):
                screen.blit(self.doorList2[0], (64, -64))
                
            #draw up one wall on right
            if (self.horizontal_wall[increment(y,1)][increment(x,1)] == 1):
                screen.blit(self.edgeList2[1], (448, -64))                
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 2):
                screen.blit(self.doorList2[1], (448, -64))                

            #draw left one up wall
            if (self.vertical_wall[decrement(y,1)][increment(x,1)] == 1):
                screen.blit(self.center1, (-448,-64))
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 2):
                screen.blit(self.door1, (-448,-64))

            #draw right one up wall
            if (self.vertical_wall[increment(y,1)][increment(x,1)] == 1):
                screen.blit(self.center1, (576,-64))
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 2):
                screen.blit(self.door1, (576,-64))

            #draw just up wall
            if (self.vertical_wall[y][increment(x,1)] == 1):
                screen.blit(self.center1, (64,-64))
            elif (self.vertical_wall[y][increment(x,1)] == 2):
                screen.blit(self.door1, (64,-64))

            #draw wall on left
            if (self.horizontal_wall[y][x] == 1):
                screen.blit(self.edgeList1[0], (-192, -320))
            elif (self.horizontal_wall[y][x] == 2):
                screen.blit(self.doorList1[0], (-192, -320))

            #draw wall on right
            if (self.horizontal_wall[increment(y,1)][x] == 1):
                screen.blit(self.edgeList1[1], (576, -320))
            elif (self.horizontal_wall[increment(y,1)][x] == 2):
                screen.blit(self.doorList1[1], (576, -320))

        #if party is looking down
        elif (game_self.party.direction == 2):
            
            if (self.ground[y][x] == 0 ):
                screen.blit(self.ground_center1, (32, 448))

            #draw ground left
            if (self.ground[y][increment(x,1)] == 0 ):
                screen.blit(self.ground_sideList1[0], (0, 448))

            #draw ground right
            if (self.ground[y][decrement(x,1)] == 0 ):
                screen.blit(self.ground_sideList1[1], (576, 448))

            #draw ground up left
            if (self.ground[increment(y,1)][increment(x,1)] == 0 ):
                screen.blit(self.ground_sideList2[0], (0, 320))             

            #draw ground up right
            if (self.ground[increment(y,1)][decrement(x,1)] == 0 ):
                screen.blit(self.ground_sideList2[1], (448, 320))             
            
            #draw ground up one
            if (self.ground[increment(y,1)][x] == 0 ):
                screen.blit(self.ground_center2, (64, 320))
                
        
            #draw straight one block wall
            if (self.horizontal_wall[increment(y,2)][x] == 1):
                screen.blit(self.center2, (192, 64))
            elif (self.horizontal_wall[increment(y,2)][x] == 2):
                screen.blit(self.door2, (192, 64))

            #draw up one wall on left
            if (self.vertical_wall[increment(y,1)][increment(x,1)] == 1):
                screen.blit(self.edgeList2[0], (64, -64))
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 2):
                screen.blit(self.doorList2[0], (64, -64))
                
            #draw up one wall on right
            if (self.vertical_wall[increment(y,1)][x] == 1):
                screen.blit(self.edgeList2[1], (448, -64))                
            elif (self.vertical_wall[increment(y,1)][x] == 2):
                screen.blit(self.doorList2[1], (448, -64))                

            #draw left one up wall
            if (self.horizontal_wall[increment(y,1)][increment(x,1)] == 1):
                screen.blit(self.center1, (-448,-64))
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 2):
                screen.blit(self.door1, (-448,-64))

            #draw right one up wall
            if (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 1):
                screen.blit(self.center1, (576,-64))
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 2):
                screen.blit(self.door1, (576,-64))

            #draw just up wall
            if (self.horizontal_wall[increment(y,1)][x] == 1):
                screen.blit(self.center1, (64,-64))
            if (self.horizontal_wall[increment(y,1)][x] == 2):
                screen.blit(self.door1, (64,-64))

            #draw wall on left
            if (self.vertical_wall[y][increment(x,1)] == 1):
                screen.blit(self.edgeList1[0], (-192, -320))
            elif (self.vertical_wall[y][increment(x,1)] == 2):
                screen.blit(self.doorList1[0], (-192, -320))

            #draw wall on right
            if (self.vertical_wall[y][x] == 1):
                screen.blit(self.edgeList1[1], (576, -320))
            elif (self.vertical_wall[y][x] == 2):
                screen.blit(self.doorList1[1], (576, -320))

        #if the player is looking left
        elif (game_self.party.direction == 3):

            if (self.ground[y][x] == 0 ):
                screen.blit(self.ground_center1, (32, 448))

            #draw ground left
            if (self.ground[increment(y,1)][x] == 0 ):
                screen.blit(self.ground_sideList1[0], (0, 448))

            #draw ground right
            if (self.ground[decrement(y,1)][x] == 0 ):
                screen.blit(self.ground_sideList1[1], (576, 448))

            #draw ground up left
            if (self.ground[increment(y,1)][decrement(x,1)] == 0 ):
                screen.blit(self.ground_sideList2[0], (0, 320))             

            #draw ground up right
            if (self.ground[decrement(y,1)][decrement(x,1)] == 0 ):
                screen.blit(self.ground_sideList2[1], (448, 320))             
            
            #draw ground up one
            if (self.ground[y][decrement(x,1)] == 0 ):
                screen.blit(self.ground_center2, (64, 320))

        
            #draw straight one block wall
            if (self.vertical_wall[y][decrement(x,1)] == 1):
                screen.blit(self.center2, (192, 64))
            elif (self.vertical_wall[y][decrement(x,1)] == 2):
                screen.blit(self.door2, (192, 64))

            #draw up one wall on left
            if (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 1):
                screen.blit(self.edgeList2[0], (64, -64))
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 2):
                screen.blit(self.doorList2[0], (64, -64))
                
            #draw up one wall on right
            if (self.horizontal_wall[y][decrement(x,1)] == 1):
                screen.blit(self.edgeList2[1], (448, -64))                
            elif (self.horizontal_wall[y][decrement(x,1)] == 2):
                screen.blit(self.doorList2[1], (448, -64))                

            #draw left one up wall
            if (self.vertical_wall[increment(y,1)][x] == 1):
                screen.blit(self.center1, (-448,-64))
            elif (self.vertical_wall[increment(y,1)][x] == 2):
                screen.blit(self.door1, (-448,-64))

            #draw right one up wall
            if (self.vertical_wall[decrement(y,1)][x] == 1):
                screen.blit(self.center1, (576,-64))
            if (self.vertical_wall[decrement(y,1)][x] == 2):
                screen.blit(self.door1, (576,-64))

            #draw just up wall
            if (self.vertical_wall[y][x] == 1):
                screen.blit(self.center1, (64,-64))
            elif (self.vertical_wall[y][x] == 2):
                screen.blit(self.door1, (64,-64))

            #draw wall on left
            if (self.horizontal_wall[increment(y,1)][x] == 1):
                screen.blit(self.edgeList1[0], (-192, -320))
            elif (self.horizontal_wall[increment(y,1)][x] == 2):
                screen.blit(self.doorList1[0], (-192, -320))

            #draw wall on right
            if (self.horizontal_wall[y][x] == 1):
                screen.blit(self.edgeList1[1], (576, -320))
            elif (self.horizontal_wall[y][x] == 2):
                screen.blit(self.doorList1[1], (576, -320))



def decrement(variable, value):
    variable -= value
    if variable < 0:
        variable += 20
    return variable

def increment(variable, value):
    variable += value
    if variable > 19:
        variable -= 20
    return variable


def load_side_images( file_name , size_x, size_y, invisible1_x, invisible1_y, invisible2_x, invisible2_y):

    image = pygame.image.load(file_name).convert()


    image_list = []

    surface1 = pygame.Surface((size_x, size_y))
    surface2 = pygame.Surface((size_x, size_y))
    surface1.blit(image, (0,0), (0,0,size_x,size_y))
    surface2.blit(image, (0,0), (size_x,0,size_x,size_y))

    surface1.set_colorkey(surface1.get_at((invisible1_x,invisible1_y)), RLEACCEL)
    surface2.set_colorkey(surface2.get_at((invisible2_x,invisible2_y)), RLEACCEL)

    surface1.convert()
    surface2.convert()
    
    image_list.append(surface1)
    image_list.append(surface2)

    return image_list


