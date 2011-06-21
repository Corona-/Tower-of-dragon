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
import dungeon_search
import math
import encount_party
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

        self.switch1 = pygame.image.load("Images/switch_1.png").convert()
        self.switch2 = pygame.image.load("Images/switch_2.png").convert()
        self.switch3 = pygame.image.load("Images/switch_3.png").convert()
        self.switch4 = pygame.image.load("Images/switch_4.png").convert()


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

        self.switchedgeList1 = load_side_images("Images/switchedge_1.png", 256, 1024, 1, 0, 1, 0)
        self.switchedgeList2 = load_side_images("Images/switchedge_2.png", 128, 512, 1, 0, 1, 0)
        self.switchedgeList3 = load_side_images("Images/switchedge_3.png", 64, 256, 1, 0, 1, 0)        
        self.switchedgeList4 = load_side_images("Images/switchedge_4.png", 32, 128, 1, 0, 1, 0)

        self.switchedgeList3_2 = load_side_images("Images/switchedge_3-2.png", 192, 256, 5,0, 5, 0)
        self.switchedgeList4_2 = load_side_images("Images/switchedge_4-2.png", 96, 128, 5,0, 5, 0)

        self.switchedgeList3_3 = load_side_images("Images/switchedge_3-3.png", 320, 256, 5,0, 5, 0)
        self.switchedgeList4_3 = load_side_images("Images/switchedge_4-3.png", 160, 128, 5,0, 5, 0)
        
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


        self.dungeon_visited = pygame.image.load("Images/dungeon_map.png").convert()

        
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

        self.show_map = False

        #reads as left top is 0,0 and right down is 19,19
        for i in range(0, 20):
            for j in range(0, 21):
                self.temp.append(int(map_data[35+i+self.floor*20][j*2:j*2+2], 16))
            self.vertical_wall.append(self.temp)
            self.temp = []

        for i in range(0, 21):
            for j in range(0,20):
                self.temp.append(int(map_data[635+i+self.floor*21][j*2:j*2+2], 16))
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


        #add other parties in self.object
        if floor != 5:
            count = 0
            row_num = 0
            for row in self.object:
                column_num = 0
                for column in row:
                    if column == 0:
                        probability = random.randint(1,1000)
                        if probability <= 10:
                            self.object[row_num][column_num] = 99
                            count+=1
                    column_num += 1
                row_num+=1     
    

        #draw extra window
        self.downstairs_window = None #system_notify.Confirm_window( Rect(160, 150, 380, 110) , system_notify.Confirm_window.DOWNSTAIRS)
        self.upstairs_window = None

        self.dungeon_locked_window = None

        self.dungeon_message_window = dungeon_message.Dungeon_message( Rect(10, 10, 620, 200))

        self.dungeon_search_window = None
        #menu_window = window.Window(Rect(160,80,320,200))

        self.party_encounter_window = None
       # menu_window.draw(screen)

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

        if self.show_map == True:
            self.draw_dungeon_map(game_self, screen)
            return

        coordinate = game_self.party.member[0].coordinate
        x = coordinate[0]
        y = coordinate[1]

        if self.space[y][x] != 1:
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

        self.dungeon_message_window.draw( game_self, screen)

        if self.dungeon_locked_window != None:
            self.dungeon_locked_window.draw(screen)

        if self.dungeon_search_window != None:
            self.dungeon_search_window.draw(screen, game_self)
        #menu_window = window.Window(Rect(160,80,320,200))
       # menu_window.draw(screen)

        if self.party_encounter_window != None:
            self.party_encounter_window.draw(screen, game_self)
           

    def dungeon_handler(self, game_self, event):
        """event handler for dungeon"""

        if self.downstairs_window != None and self.downstairs_window.is_visible == True:
            self.downstairs_window.confirm_window_handler( game_self, event, None)
            return
        elif self.upstairs_window != None and self.upstairs_window.is_visible == True:
            self.upstairs_window.confirm_window_handler( game_self, event, None)
            return
        elif self.dungeon_message_window.is_visible == True:
            self.dungeon_message_window.dungeon_message_handler( game_self, event)
            return
        elif self.dungeon_locked_window != None and self.dungeon_locked_window.is_visible == True:
            self.dungeon_locked_window.donate_finish_window_handler(event, game_self)
            return
        elif self.dungeon_search_window != None and self.dungeon_search_window.is_visible == True:
            self.dungeon_search_window.dungeon_search_window_handler(event, game_self)
            return
        elif self.party_encounter_window != None and self.party_encounter_window.is_visible == True:
            self.party_encounter_window.encount_party_handler( event, game_self)
            return

        
        if self.battle_flag == 1:
            self.battle.battle_handler(game_self, event)
            return

        if event.type == KEYDOWN and event.key == K_s:
            self.dungeon_search_window = dungeon_search.Dungeon_search_window(Rect(160,80,320, 120))
            self.dungeon_search_window.is_visible = True



        if event.type == KEYDOWN and (event.key ==K_m):
            self.show_map = not self.show_map
            return

        if self.show_map and event.type == KEYDOWN and (event.key == K_x or event.key == K_z or event.key ==K_m or event.key == K_SPACE or event.key == K_RETURN):
            self.show_map = not self.show_map
            return

        if self.show_map == True:
            return

        #party member all has same coordinate so take one of it
        coordinate = game_self.party.member[0].coordinate
        x = coordinate[0]
        y = coordinate[1]

        #need to calculate theif level
        #theif_level = 2
        theif_level = calculate_thief_level(game_self)
        
        #add this coordinate to visited coordinate
        game_self.party.dungeon_visited[coordinate[2]][x][y] = theif_level


        encount = random.randint(1, 100)

        if event.type == KEYDOWN and (event.key ==K_UP):
            
            if game_self.party.torch > 0:
                game_self.party.torch -= 1

            walked = 0   
            for character in game_self.party.member:
                if (game_self.party.direction == 0):
                    #if there is a wall in front, can't move up
                    if( self.horizontal_wall[y][x] == 0):
                        character.coordinate[1] = decrement(character.coordinate[1],1)
                        walked = 1
                elif (game_self.party.direction == 1):
                    if( self.vertical_wall[y][increment(x,1)] == 0):
                        character.coordinate[0] = increment(character.coordinate[0],1)
                        walked = 1
                elif (game_self.party.direction == 2):
                    if( self.horizontal_wall[increment(y,1)][x] == 0):
                        character.coordinate[1] = increment(character.coordinate[1],1)
                        walked = 1
                elif (game_self.party.direction == 3):
                    if( self.vertical_wall[y][x] == 0):
                        character.coordinate[0] = decrement(character.coordinate[0],1)
                        walked = 1

            if walked == 1:
                self.footstep_se.play()
                #change direction randomly by turn table
                if self.ground[character.coordinate[1]][character.coordinate[0]] == 4:
                    random_direction = random.randint(0, 3)
                    game_self.party.direction = random_direction

                for chara in game_self.party.member:
                    if chara.status[0] == 1:
                        chara.hp -= int(math.ceil(chara.max_hp/20.0))

                coordinate = game_self.party.member[0].coordinate
                x = coordinate[0]
                y = coordinate[1]

                if self.object[y][x] == 99:
                    self.party_encounter_window = encount_party.Encount_party( Rect(130,80,380, 240), coordinate[2], game_self)
                    self.party_encounter_window.is_visible = True

                battle.party_dead_poison(game_self.party.member)
                    
                
            self.battle_encount( 5, game_self.party.member[0] )

            self.dungeon_message_window.set_coordinate( game_self, game_self.party.member[0].coordinate)

            
            
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


        if event.type == KEYDOWN and (event.key ==K_x):
            game_self.game_state = MENU
            game_self.menu = menu.Menu()
                
            game_self.vertical_wall_temp = self.vertical_wall
            game_self.horizontal_wall_temp =  self.horizontal_wall
            game_self.ground_temp = self.ground
            game_self.space_temp = self.space
            game_self.object_temp = self.object


            game_self.dungeon = None
            #for character in game_self.party.member:
            #    character.coordinate = [-1,-1,-1]
            #self.music = 0

        if event.type == KEYDOWN and (event.key ==K_z or event.key == K_SPACE or event.key == K_RETURN):

            walked = 0
            
            if game_self.party.direction == 0:
                #normal door or hidden door or one way door up
                if (self.horizontal_wall[y][x] == 2) or self.horizontal_wall[y][x] == 4 or  self.horizontal_wall[y][x] == 6:
                    self.door_se.play()
                    for character in game_self.party.member:
                        character.coordinate[1] = decrement(character.coordinate[1],1)
                    walked = 1
                #locked door
                elif (self.horizontal_wall[y][x] == 3):
                    self.dungeon_locked_window = system_notify.Donate_finish_window(Rect(150,160,300,50), system_notify.Donate_finish_window.DUNGEON_LOCKED)
                    self.dungeon_locked_window.is_visible = True
                    pass
                    

            if game_self.party.direction == 1:
                if self.vertical_wall[y][increment(x,1)] == 2 or self.vertical_wall[y][increment(x,1)] == 4 or self.vertical_wall[y][increment(x,1)] == 7:
                    self.door_se.play()
                    for character in game_self.party.member:
                        character.coordinate[0] = increment(character.coordinate[0],1)
                    walked = 1
                elif self.vertical_wall[y][increment(x,1)] == 3:
                    self.dungeon_locked_window = system_notify.Donate_finish_window(Rect(150,160,300,50), system_notify.Donate_finish_window.DUNGEON_LOCKED)
                    self.dungeon_locked_window.is_visible = True
                    pass


            if game_self.party.direction == 2:
                if self.horizontal_wall[increment(y,1)][x] == 2 or self.horizontal_wall[increment(y,1)][x] == 4 or self.horizontal_wall[increment(y,1)][x] == 7:
                    self.door_se.play()
                    for character in game_self.party.member:
                        character.coordinate[1] = increment(character.coordinate[1],1)
                    walked = 1
                elif self.horizontal_wall[increment(y,1)][x] == 3:
                    self.dungeon_locked_window = system_notify.Donate_finish_window(Rect(150,160,300,50), system_notify.Donate_finish_window.DUNGEON_LOCKED)
                    self.dungeon_locked_window.is_visible = True
                    pass
                
            if game_self.party.direction == 3:
                if self.vertical_wall[y][x] == 2 or self.vertical_wall[y][x] == 4 or self.vertical_wall[y][x] == 6:
                    self.door_se.play()
                    for character in game_self.party.member:
                        character.coordinate[0] = decrement(character.coordinate[0],1)
                    walked = 1
                elif self.vertical_wall[y][x] == 3:
                    self.dungeon_locked_window = system_notify.Donate_finish_window(Rect(150,160,300,50), system_notify.Donate_finish_window.DUNGEON_LOCKED)
                    self.dungeon_locked_window.is_visible = True
                    pass

            self.dungeon_message_window.set_coordinate( game_self, game_self.party.member[0].coordinate)

            if walked == 1 and self.dungeon_message_window.message == None:
                #change direction randomly by turn table
                if self.ground[character.coordinate[1]][character.coordinate[0]] == 4:
                    random_direction = random.randint(0, 3)
                    game_self.party.direction = random_direction

                self.battle_encount( 10, game_self.party.member[0] )

                for chara in game_self.party.member:
                    if chara.status[0] == 1:
                        chara.hp -= int(math.ceil(chara.max_hp/10.0))

                battle.party_dead_poison(game_self.party.member)



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


            #show switch message when key is pressed
            if self.horizontal_wall[y][x] == 12 and game_self.party.direction == 0:
                #show switch message
                self.dungeon_message_window.key_press = True
                self.dungeon_message_window.set_coordinate( game_self, game_self.party.member[0].coordinate)
            if self.horizontal_wall[increment(y,1)][x] == 13 and game_self.party.direction == 2:
                self.dungeon_message_window.key_press = True
                self.dungeon_message_window.set_coordinate( game_self, game_self.party.member[0].coordinate)
            if self.vertical_wall[y][x] == 12 and game_self.party.direction == 3:
                self.dungeon_message_window.key_press = True
                self.dungeon_message_window.set_coordinate( game_self, game_self.party.member[0].coordinate)
            if self.vertical_wall[y][increment(x,1)] == 13 and game_self.party.direction == 1:
                self.dungeon_message_window.key_press = True
                self.dungeon_message_window.set_coordinate( game_self, game_self.party.member[0].coordinate)



 
            #battle with room guard
            if self.object[y][x] == 15:
                self.battle_encount( 80, game_self.party.member[0] )
                self.object[y][x] = 0
                self.add_item_to_battle( game_self.party.member)

        #warp on fourth floor
        if self.object[y][x] == 17 and game_self.party.member[0].coordinate == [8, 19, 4]:
            for chara in game_self.party.member:
                chara.coordinate = [ 15, 15 , 4]

        #move back to entrance
        if self.ground[y][x] == 11:
            game_self.game_state = TOWER
            i = 0
            for charcter in game_self.party.member:
                game_self.party.member[i].coordinate = [-1,-1,-1]
                i += 1
            game_self.dungeon.battle = None
            game_self.dungeon.battle_flag = 0
            game_self.dungeon.music = 0
            game_self.party.direction = 0
            game_self.tower = tower.Tower()
            game_self.dungeon = None

            for character in game_self.party.member:
                character.face_shield = 0
                character.battle_ac = 0
                character.permanant_ac = 0







        #probability is out of 1 - 100
    def battle_encount( self, probability, character ):

        encount = random.randint(1, 100)

        if character.coordinate[2] != 5 and encount < probability:
            self.battle = battle.Battle(self.enemy_data, character.coordinate[2])
            self.battle_flag = 1

        

    def add_item_to_battle( self, members):

        floor = members[0].coordinate[2]

        if self.battle == None:
            return

        if floor == 1:
            items = [1, 6, 100, 150, 200, 215, 250, 300, 350, 351, 400, 426, 500, 550]
            rare_items = [101, 151, 201, 251, 301, 401, 427, 501, 551, 600]

            max_percent = 20
            rare_percent = 5

            percent = random.randint(1,100)
            if percent <= max_percent:
                item_number = random.randint( 0, len(items)-1)
                self.battle.enemy_drop_items.append( items[item_number])

            percent = random.randint(1,100)
            if percent <= rare_percent:
                item_number = random.randint( 0, len(rare_items)-1)
                self.battle.enemy_drop_items.append( rare_items[item_number])

        elif floor == 2:

            items = [1, 6, 100, 150, 200, 215, 250, 300, 350, 351, 400, 426, 500, 550, 101, 151, 201, 251, 301, 401, 427, 501, 551, 600]
            rare_items = [102, 152, 202, 216, 252, 302, 352, 402, 502, 552]

            max_percent = 25
            rare_percent = 5
            
            percent = random.randint(1,100)
            if percent <= max_percent:
                item_number = random.randint( 0, len(items)-1)
                self.battle.enemy_drop_items.append( items[item_number])

            percent = random.randint(1,100)
            if percent <= rare_percent:
                item_number = random.randint( 0, len(rare_items)-1)
                self.battle.enemy_drop_items.append( rare_items[item_number])

        elif floor == 3:
            items = [1,4,5,6,600,601,602,603,604,605,606]

            max_percent = 8
            
            percent = random.randint(1,100)
            if percent <= max_percent:
                item_number = random.randint( 0, len(items)-1)
                self.battle.enemy_drop_items.append( items[item_number])

        elif floor == 4:
            items = [1,2,4,5,6, 102, 152,202,216,252,302,352,402,502,552]
            rare_items = [103, 153, 203, 253, 303, 353, 403, 503, 553]

            max_percent = 20
            rare_percent = 5

            percent = random.randint(1,100)
            if percent <= max_percent:
                item_number = random.randint( 0, len(items)-1)
                self.battle.enemy_drop_items.append( items[item_number])

            percent = random.randint(1,100)
            if percent <= rare_percent:
                item_number = random.randint( 0, len(rare_items)-1)
                self.battle.enemy_drop_items.append( rare_items[item_number])
            
        elif floor == 5:
            items = [600,601,602,603,604,605,606,504,428,404,355,304,254,219,204,154,104]

            max_percent = 30

            percent = random.randint(1,100)
            if percent <= max_percent:
                item_number = random.randint( 0, len(items)-1)
                self.battle.enemy_drop_items.append( items[item_number])

        
        pass

    def draw_dungeon_map(self, game_self, screen):

        #party member all has same coordinate so take one of it
        coordinate = game_self.party.member[0].coordinate
        x = coordinate[0]
        y = coordinate[1]

        screen.blit(self.dungeon_visited, (50,75))

        floor_window = window.Window(Rect(415,80,210,60))
        floor_window.draw(screen)

        menu_font = pygame.font.Font("ipag.ttf", 20)

        floor_font = menu_font.render(u"天龍の塔 " + str(coordinate[2]) + u"階", True, COLOR_WHITE)
        screen.blit(floor_font, (520-floor_font.get_width()/2, 100))

        theif_font = menu_font.render( u"盗賊LV" + str(calculate_thief_level(game_self)), True, COLOR_WHITE)
        merchant_font = menu_font.render( u"商人LV" + str(calculate_merchant_level(game_self)), True, COLOR_WHITE)

        level_window = window.Window(Rect(415,160,210,90))
        level_window.draw(screen)

        screen.blit(theif_font, (520 - theif_font.get_width()/2, 180))
        screen.blit(merchant_font, (520 - merchant_font.get_width()/2, 210))
        


        floor_data = game_self.party.dungeon_visited[coordinate[2]]

        #screen coordinate of (0,0)
        #Rect(68,97,16,16)

        x = 0
        for i in floor_data:
            y = 0
            for j in i:

                #calculate where to place rectangle
                rect_x = 68 + x*16+x
                rect_y = 97 + y*16+y
                
                if j > 0 and j >= 1:
                    #only show floor and stairs
                    pygame.draw.rect(screen, Color(126,197,119), Rect(rect_x,rect_y,16,16), 0)

                    #downstairs
                    if self.ground[y][x] == 2:
                        pygame.draw.polygon(screen, (0,0,0), [(rect_x+3,rect_y+3), (rect_x+11, rect_y+3), (rect_x+7, rect_y+11)], 0)
                    #upstairs
                    if self.ground[y][x] == 1:
                        pygame.draw.polygon(screen, (0,0,0), [(rect_x+3,rect_y+11), (rect_x+11, rect_y+11), (rect_x+7, rect_y+3)], 0)

                #need to be before wall to be accurate
                if j > 0 and j >= 2:
                    #additionaly show dark zone
                    if self.space[y][x] == 1:
                        pygame.draw.rect(screen, Color(255,0,255), Rect(rect_x,rect_y,16,16), 0)
          

                if j > 0 and j >= 1:
                    #additionaly show wall and door

                    #show wall
                    if self.horizontal_wall[y][x] == 1 or self.horizontal_wall[y][x] == 2 or self.horizontal_wall[y][x] == 3 or self.horizontal_wall[y][x] == 4 or self.horizontal_wall[y][x] == 13:
                        pygame.draw.rect(screen, Color(0,0,0), Rect(rect_x,rect_y,16,2), 0)
                    if self.horizontal_wall[increment(y,1)][x] == 1 or self.horizontal_wall[increment(y,1)][x] == 2 or self.horizontal_wall[increment(y,1)][x] == 3 or self.horizontal_wall[increment(y,1)][x] == 4 or self.horizontal_wall[increment(y,1)][x] == 12:
                        pygame.draw.rect(screen, Color(0,0,0), Rect(rect_x,rect_y+14,16,2), 0)
                    if self.vertical_wall[y][x] == 1 or self.vertical_wall[y][x] == 2 or self.vertical_wall[y][x] == 3 or self.vertical_wall[y][x] == 4 or self.vertical_wall[y][x] == 13:
                        pygame.draw.rect(screen, Color(0,0,0), Rect(rect_x,rect_y,2,16), 0)
                    if self.vertical_wall[y][increment(x,1)] == 1 or self.vertical_wall[y][increment(x,1)] == 2 or self.vertical_wall[y][increment(x,1)] == 3 or self.vertical_wall[y][increment(x,1)] == 4 or  self.vertical_wall[y][increment(x,1)] == 12:
                        pygame.draw.rect(screen, Color(0,0,0), Rect(rect_x+14,rect_y,2,16), 0)

                    #show door                                 
                    if self.horizontal_wall[y][x] == 2 or self.horizontal_wall[y][x] == 3:
                        pygame.draw.rect(screen, Color(190,128,14), Rect(rect_x+4,rect_y,8,2), 0)
                    if self.horizontal_wall[increment(y,1)][x] == 2 or self.horizontal_wall[increment(y,1)][x] == 3:
                        pygame.draw.rect(screen, Color(190,128,14), Rect(rect_x+4,rect_y+14,8,2), 0)
                    if self.vertical_wall[y][x] == 2 or self.vertical_wall[y][x] == 3:
                        pygame.draw.rect(screen, Color(190,128,14), Rect(rect_x,rect_y+4,2,8), 0)
                    if self.vertical_wall[y][increment(x,1)] == 2 or self.vertical_wall[y][increment(x,1)] == 3:
                        pygame.draw.rect(screen, Color(190,128,14), Rect(rect_x+14,rect_y+4,2,8), 0)
                                               
                    pass
          
                    pass
                if j > 0 and j >= 3:
                    #additionaly show locked door
                    if self.horizontal_wall[y][x] == 3:
                        pygame.draw.rect(screen, Color(255,0,0), Rect(rect_x+4,rect_y,8,2), 0)
                    if self.horizontal_wall[increment(y,1)][x] == 3:
                        pygame.draw.rect(screen, Color(255,0,0), Rect(rect_x+4,rect_y+14,8,2), 0)
                    if self.vertical_wall[y][x] == 3:
                        pygame.draw.rect(screen, Color(255,0,0), Rect(rect_x,rect_y+4,2,8), 0)
                    if self.vertical_wall[y][increment(x,1)] == 3:
                        pygame.draw.rect(screen, Color(255,0,0), Rect(rect_x+14,rect_y+4,2,8), 0)

                    #additionaly show switch

##                    if self.horizontal_wall[y][x] == 12:
##                        pygame.draw.arc( screen, Color(0,0,255), Rect(rect_x+6, rect_y, 8, 4), 0, 3.14, 1)
##                    if self.horizontal_wall[increment(y,1)][x] == 13:
##                        pygame.draw.arc( screen, Color(0,0,255), Rect(rect_x+6, rect_y+16, 8, 4), 0, 3.14, 1)
##                    if self.vertical_wall[y][x] == 12:
##                        pygame.draw.arc( screen, Color(0,0,255), Rect(rect_x, rect_y+6, 4, 8), 0, 3.14, 1)
##                    if self.vertical_wall[y][increment(x,1)] == 13:
##                        pygame.draw.arc( screen, Color(0,0,255), Rect(rect_x+16, rect_y+6, 4, 8), 0, 3.14, 1)
##                        

                    if self.horizontal_wall[y][x] == 12:
                        pygame.draw.rect(screen, Color(0,0,255), Rect(rect_x,rect_y,16,2), 0)
                    if self.horizontal_wall[increment(y,1)][x] == 13:
                        pygame.draw.rect(screen, Color(0,0,255), Rect(rect_x,rect_y+14,16,2), 0)
                    if self.vertical_wall[y][x] == 12:
                        pygame.draw.rect(screen, Color(0,0,255), Rect(rect_x,rect_y,2,16), 0)
                    if self.vertical_wall[y][increment(x,1)] == 13:
                        pygame.draw.rect(screen, Color(0,0,255), Rect(rect_x+14,rect_y,2,16), 0)

                                      
                if j > 0 and j >= 4:
                    #additionaly show hidden door
                    if self.horizontal_wall[y][x] == 4:
                        pygame.draw.rect(screen, Color(255,255,0), Rect(rect_x+4,rect_y,8,2), 0)
                    if self.horizontal_wall[increment(y,1)][x] == 4:
                        pygame.draw.rect(screen, Color(255,255,0), Rect(rect_x+4,rect_y+14,8,2), 0)
                    if self.vertical_wall[y][x] == 4:
                        pygame.draw.rect(screen, Color(255,255,0), Rect(rect_x,rect_y+4,2,8), 0)
                    if self.vertical_wall[y][increment(x,1)] == 4:
                        pygame.draw.rect(screen, Color(255,255,0), Rect(rect_x+14,rect_y+4,2,8), 0)


                    #additionaly show trap
                    pass
                if j > 0 and j >= 5:
                    #additionaly show each trap
                    pass
                    
                y+=1
            x+=1
                

        pass
        

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
            draw_dungeon_ground( screen, self.ground[y][x], self.ground_center1, (32, 448))
            #draw ground left
            draw_dungeon_ground( screen, self.ground[y][decrement(x,1)], self.ground_sideList1[0], (0, 448))
            #draw ground right
            draw_dungeon_ground( screen, self.ground[y][increment(x,1)], self.ground_sideList1[1], (576, 448))
            #draw ground up left
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][decrement(x,1)], self.ground_sideList2[0], (0,320))
            #draw ground up right
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][increment(x,1)], self.ground_sideList2[1], (448,320))
            #draw ground up two left
            draw_dungeon_ground( screen, self.ground[decrement(y,2)][decrement(x,1)], self.ground_sideList3[0], (-128,256))
            #draw ground up two right
            draw_dungeon_ground( screen, self.ground[decrement(y,2)][increment(x,1)], self.ground_sideList3[1], (384,256))
            #draw ground up two left two
            draw_dungeon_ground( screen, self.ground[decrement(y,2)][decrement(x,2)], self.ground_sideList3_2[0], (0,256))
            #draw ground up two right two
            draw_dungeon_ground( screen, self.ground[decrement(y,2)][increment(x,2)], self.ground_sideList3_2[1], (576,256))
            #draw ground up three left
            draw_dungeon_ground( screen, self.ground[decrement(y,3)][decrement(x,1)], self.ground_sideList4[0], (128,224))
            #draw ground up three right
            draw_dungeon_ground( screen, self.ground[decrement(y,3)][increment(x,1)], self.ground_sideList4[1], (352,224))
            #draw ground up three left two
            draw_dungeon_ground( screen, self.ground[decrement(y,3)][decrement(x,2)], self.ground_sideList4_2[0], (0,224))
            #draw ground up three right two
            draw_dungeon_ground( screen, self.ground[decrement(y,3)][increment(x,2)], self.ground_sideList4_2[1], (416,224))                
            #draw ground up one
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][x], self.ground_center2, (64,320))
            #draw ground up two
            draw_dungeon_ground( screen, self.ground[decrement(y,2)][x], self.ground_center3, (192,256))                
            #draw ground up three
            draw_dungeon_ground( screen, self.ground[decrement(y,3)][x], self.ground_center4, (256,224))

            #draw straight three block wall left two
            #wall
            if (self.horizontal_wall[decrement(y,3)][decrement(x,2)] == 1):
                screen.blit(self.center4, (160, 160))
            #door
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,2)] == 2):
                screen.blit(self.door4, (160,160))
            #locked door
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,2)] == 3):
                screen.blit(self.door4, (160,160))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,2)] == 4):
                screen.blit(self.door4, (160,160))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,2)] == 6):
                screen.blit(self.door4, (160,160))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,2)] == 7):
                screen.blit(self.center4, (160,160))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,2)] == 8):
                screen.blit(self.door4, (160,160))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,2)] == 9):
                screen.blit(self.center4, (160,160))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,2)] == 12):
                screen.blit(self.switch4, (160,160))                                                               
            #switch on left side
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,2)] == 13):
                screen.blit(self.center4, (160,160))                                               

            #draw straight three block wall left one
            if (self.horizontal_wall[decrement(y,3)][decrement(x,1)] == 1):
                screen.blit(self.center4, (224, 160))
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,1)] == 2):
                screen.blit(self.door4, (224,160))                                               
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,1)] == 3):
                screen.blit(self.door4, (224,160))                                               
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,1)] == 4):
                screen.blit(self.door4, (224,160))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,1)] == 6):
                screen.blit(self.door4, (224,160))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,1)] == 7):
                screen.blit(self.center4, (224,160))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,1)] == 8):
                screen.blit(self.door4, (224,160))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,1)] == 9):
                screen.blit(self.center4, (224,160))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,1)] == 12):
                screen.blit(self.switch4, (224,160))  
            #switch on left side
            elif (self.horizontal_wall[decrement(y,3)][decrement(x,1)] == 13):
                screen.blit(self.center4, (224,160))  

            #draw straight three block wall
            if (self.horizontal_wall[decrement(y,3)][x] == 1):
                screen.blit(self.center4, (288, 160))
            elif (self.horizontal_wall[decrement(y,3)][x] == 2):
                screen.blit(self.door4, (288,160))
            elif (self.horizontal_wall[decrement(y,3)][x] == 3):
                screen.blit(self.door4, (288,160))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,3)][x] == 4):
                screen.blit(self.door4, (288,160))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,3)][x] == 6):
                screen.blit(self.door4, (288,160))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,3)][x] == 7):
                screen.blit(self.center4, (288,160))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,3)][x] == 8):
                screen.blit(self.door4, (288,160))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,3)][x] == 9):
                screen.blit(self.center4, (288,160))
            #switch on left side
            elif (self.horizontal_wall[decrement(y,3)][x] == 12):
                screen.blit(self.switch4, (288,160))  
            #switch on left side
            elif (self.horizontal_wall[decrement(y,3)][x] == 13):
                screen.blit(self.center4, (288,160))  

            #draw straight three block wall right one
            if (self.horizontal_wall[decrement(y,3)][increment(x,1)] == 1):
                screen.blit(self.center4, (352, 160))
            elif (self.horizontal_wall[decrement(y,3)][increment(x,1)] == 2):
                screen.blit(self.door4, (352,160))                                               
            elif (self.horizontal_wall[decrement(y,3)][increment(x,1)] == 3):
                screen.blit(self.door4, (352,160))                                               
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,3)][increment(x,1)] == 4):
                screen.blit(self.door4, (352,160))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,3)][increment(x,1)] == 6):
                screen.blit(self.door4, (352,160))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,3)][increment(x,1)] == 7):
                screen.blit(self.center4, (352,160))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,3)][increment(x,1)] == 8):
                screen.blit(self.door4, (352,160))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,3)][increment(x,1)] == 9):
                screen.blit(self.center4, (352,160))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,3)][increment(x,1)] == 12):
                screen.blit(self.switch4, (352,160))  
            #switch on left side
            elif (self.horizontal_wall[decrement(y,3)][increment(x,1)] == 13):
                screen.blit(self.center4, (352,160))  

            #draw straight three block wall right two
            if (self.horizontal_wall[decrement(y,3)][increment(x,2)] == 1):
                screen.blit(self.center4, (416, 160))
            elif (self.horizontal_wall[decrement(y,3)][increment(x,2)] == 2):
                screen.blit(self.door4, (416,160))
            elif (self.horizontal_wall[decrement(y,3)][increment(x,2)] == 3):
                screen.blit(self.door4, (416,160))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,3)][increment(x,2)] == 4):
                screen.blit(self.door4, (416,160))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,3)][increment(x,2)] == 6):
                screen.blit(self.door4, (416,160))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,3)][increment(x,2)] == 7):
                screen.blit(self.center4, (416,160))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,3)][increment(x,2)] == 8):
                screen.blit(self.door4, (416,160))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,3)][increment(x,2)] == 9):
                screen.blit(self.center4, (416,160))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,3)][increment(x,2)] == 12):
                screen.blit(self.switch4, (416,160))  
            #switch on left side
            elif (self.horizontal_wall[decrement(y,3)][increment(x,2)] == 13):
                screen.blit(self.center4, (416,160))  
                
            #draw up three wall on left three
            if (self.vertical_wall[decrement(y,3)][decrement(x,2)] == 1):
                screen.blit(self.edgeList4_3[0], (0, 128))
            elif (self.vertical_wall[decrement(y,3)][decrement(x,2)] == 2):
                screen.blit(self.doorList4_3[0], (0, 128))
            elif (self.vertical_wall[decrement(y,3)][decrement(x,2)] == 3):
                screen.blit(self.doorList4_3[0], (0, 128))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,3)][decrement(x,2)] == 4):
                screen.blit(self.doorList4_3[0], (0, 128))
            #one way door from right
            elif (self.vertical_wall[decrement(y,3)][decrement(x,2)] == 6):
                screen.blit(self.doorList4_3[0], (0, 128))
            #one way door from left
            elif (self.vertical_wall[decrement(y,3)][decrement(x,2)] == 7):
                screen.blit(self.edgeList4_3[0], (0, 128))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,3)][decrement(x,2)] == 8):
                screen.blit(self.doorList4_3[0], (0, 128))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,3)][decrement(x,2)] == 9):
                screen.blit(self.edgeList4_3[0], (0, 128))
            #switch on right side
            elif (self.vertical_wall[decrement(y,3)][decrement(x,2)] == 12):
                screen.blit(self.switchedgeList4_3[0], (0, 128)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,3)][decrement(x,2)] == 13):
                screen.blit(self.edgeList4_3[0], (0, 128)) 

            #draw up three wall on left two
            if (self.vertical_wall[decrement(y,3)][decrement(x,1)] == 1):
                screen.blit(self.edgeList4_2[0], (128, 128))
            elif (self.vertical_wall[decrement(y,3)][decrement(x,1)] == 2):
                screen.blit(self.doorList4_2[0], (128, 128))
            elif (self.vertical_wall[decrement(y,3)][decrement(x,1)] == 3):
                screen.blit(self.doorList4_2[0], (128, 128))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,3)][decrement(x,1)] == 4):
                screen.blit(self.doorList4_2[0], (128, 128))
            #one way door from right
            elif (self.vertical_wall[decrement(y,3)][decrement(x,1)] == 6):
                screen.blit(self.doorList4_2[0], (128, 128))
            #one way door from left
            elif (self.vertical_wall[decrement(y,3)][decrement(x,1)] == 7):
                screen.blit(self.edgeList4_2[0], (128, 128))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,3)][decrement(x,1)] == 8):
                screen.blit(self.doorList4_2[0], (128, 128))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,3)][decrement(x,1)] == 9):
                screen.blit(self.edgeList4_2[0], (128, 128))
            #switch on right side
            elif (self.vertical_wall[decrement(y,3)][decrement(x,1)] == 12):
                screen.blit(self.switchedgeList4_2[0], (128, 128)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,3)][decrement(x,1)] == 13):
                screen.blit(self.edgeList4_2[0], (128, 128)) 

            #draw up three wall on left
            if (self.vertical_wall[decrement(y,3)][x] == 1):
                screen.blit(self.edgeList4[0], (256, 128))
            elif (self.vertical_wall[decrement(y,3)][x] == 2):
                screen.blit(self.doorList4[0], (256, 128))
            elif (self.vertical_wall[decrement(y,3)][x] == 3):
                screen.blit(self.doorList4[0], (256, 128))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,3)][x] == 4):
                screen.blit(self.doorList4[0], (256, 128))
            #one way door from right
            elif (self.vertical_wall[decrement(y,3)][x] == 6):
                screen.blit(self.doorList4[0], (256, 128))
            #one way door from left
            elif (self.vertical_wall[decrement(y,3)][x] == 7):
                screen.blit(self.edgeList4[0], (256, 128))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,3)][x] == 8):
                screen.blit(self.doorList4[0], (256, 128))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,3)][x] == 9):
                screen.blit(self.edgeList4[0], (256, 128))
            #switch on right side
            elif (self.vertical_wall[decrement(y,3)][x] == 12):
                screen.blit(self.switchedgeList4[0], (256, 128)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,3)][x] == 13):
                screen.blit(self.edgeList4[0], (256, 128)) 


            #draw up three wall on right three
            if (self.vertical_wall[decrement(y,3)][increment(x,3)] == 1):
                screen.blit(self.edgeList4_3[1], (480, 128))                
            elif (self.vertical_wall[decrement(y,3)][increment(x,3)] == 2):
                screen.blit(self.doorList4_3[1], (480, 128))  
            elif (self.vertical_wall[decrement(y,3)][increment(x,3)] == 3):
                screen.blit(self.doorList4_3[1], (480, 128))  
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,3)][increment(x,3)] == 4):
                screen.blit(self.doorList4_3[1], (480, 128))
            #one way door from right
            elif (self.vertical_wall[decrement(y,3)][increment(x,3)] == 6):
                screen.blit(self.edgeList4_3[1], (480, 128))
            #one way door from left
            elif (self.vertical_wall[decrement(y,3)][increment(x,3)] == 7):
                screen.blit(self.doorList4_3[1], (480, 128))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,3)][increment(x,3)] == 8):
                screen.blit(self.edgeList4_3[1], (480, 128))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,3)][increment(x,3)] == 9):
                screen.blit(self.doorList4_3[1], (480, 128))
            #switch on right side
            elif (self.vertical_wall[decrement(y,3)][increment(x,3)] == 12):
                screen.blit(self.edgeList4_3[1], (480, 128)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,3)][increment(x,3)] == 13):
                screen.blit(self.switchedgeList4_3[1], (480, 128)) 


            #draw up three wall on right two
            if (self.vertical_wall[decrement(y,3)][increment(x,2)] == 1):
                screen.blit(self.edgeList4_2[1], (416, 128))                
            elif (self.vertical_wall[decrement(y,3)][increment(x,2)] == 2):
                screen.blit(self.doorList4_2[1], (416, 128))                               
            elif (self.vertical_wall[decrement(y,3)][increment(x,2)] == 3):
                screen.blit(self.doorList4_2[1], (416, 128))                               
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,3)][increment(x,2)] == 4):
                screen.blit(self.doorList4_2[1], (416, 128))
            #one way door from right
            elif (self.vertical_wall[decrement(y,3)][increment(x,2)] == 6):
                screen.blit(self.edgeList4_2[1], (416, 128))
            #one way door from left
            elif (self.vertical_wall[decrement(y,3)][increment(x,2)] == 7):
                screen.blit(self.doorList4_2[1], (416, 128))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,3)][increment(x,2)] == 8):
                screen.blit(self.edgeList4_2[1], (416, 128))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,3)][increment(x,2)] == 9):
                screen.blit(self.doorList4_2[1], (416, 128))
            #switch on right side
            elif (self.vertical_wall[decrement(y,3)][increment(x,2)] == 12):
                screen.blit(self.edgeList4_2[1], (416, 128)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,3)][increment(x,2)] == 13):
                screen.blit(self.switchedgeList4_2[1], (416, 128)) 

            #draw up three wall on right
            if (self.vertical_wall[decrement(y,3)][increment(x,1)] == 1):
                screen.blit(self.edgeList4[1], (352, 128))                
            elif (self.vertical_wall[decrement(y,3)][increment(x,1)] == 2):
                screen.blit(self.doorList4[1], (352, 128))                
            elif (self.vertical_wall[decrement(y,3)][increment(x,1)] == 3):
                screen.blit(self.doorList4[1], (352, 128))                
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,3)][increment(x,1)] == 4):
                screen.blit(self.doorList4[1], (352, 128))
            #one way door from right
            elif (self.vertical_wall[decrement(y,3)][increment(x,1)] == 6):
                screen.blit(self.edgeList4[1], (352, 128))
            #one way door from left
            elif (self.vertical_wall[decrement(y,3)][increment(x,1)] == 7):
                screen.blit(self.doorList4[1], (352, 128))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,3)][increment(x,1)] == 8):
                screen.blit(self.edgeList4[1], (352, 128))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,3)][increment(x,1)] == 9):
                screen.blit(self.doorList4[1], (352, 128))
            #switch on right side
            elif (self.vertical_wall[decrement(y,3)][increment(x,1)] == 12):
                screen.blit(self.edgeList4[1], (352, 128)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,3)][increment(x,1)] == 13):
                screen.blit(self.switchedgeList4[1], (352, 128)) 


            #draw straight two block wall left one
            if (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 1):
                screen.blit(self.center3, (0, 128))
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 2):
                screen.blit(self.door3, (0,128))
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 3):
                screen.blit(self.door3, (0,128))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 4):
                screen.blit(self.door3, (0,128))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 6):
                screen.blit(self.door3, (0,128))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 7):
                screen.blit(self.center3, (0,128))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 8):
                screen.blit(self.door3, (0,128))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 9):
                screen.blit(self.center3, (0,128))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 12):
                screen.blit(self.switch3, (0,128))  
            #switch on left side
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 13):
                screen.blit(self.center3, (0,128))  

            #draw straight two block wall left one
            if (self.horizontal_wall[decrement(y,2)][decrement(x,1)] == 1):
                screen.blit(self.center3, (128, 128))
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,1)] == 2):
                screen.blit(self.door3, (128,128))
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,1)] == 3):
                screen.blit(self.door3, (128,128))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,1)] == 4):
                screen.blit(self.door3, (128,128))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,1)] == 6):
                screen.blit(self.door3, (128,128))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,1)] == 7):
                screen.blit(self.center3, (128,128))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,1)] == 8):
                screen.blit(self.door3, (128,128))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,1)] == 9):
                screen.blit(self.center3, (128,128))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,1)] == 12):
                screen.blit(self.switch3, (128,128))  
            #switch on left side
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,1)] == 13):
                screen.blit(self.center3, (128,128))  

            #draw straight two block wall
            if (self.horizontal_wall[decrement(y,2)][x] == 1):
                screen.blit(self.center3, (256, 128))
            elif (self.horizontal_wall[decrement(y,2)][x] == 2):
                screen.blit(self.door3, (256,128))
            elif (self.horizontal_wall[decrement(y,2)][x] == 3):
                screen.blit(self.door3, (256,128))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,2)][x] == 4):
                screen.blit(self.door3, (256,128))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,2)][x] == 6):
                screen.blit(self.door3, (256,128))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,2)][x] == 7):
                screen.blit(self.center3, (256,128))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,2)][x] == 8):
                screen.blit(self.door3, (256,128))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,2)][x] == 9):
                screen.blit(self.center3, (256,128))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,2)][x] == 12):
                screen.blit(self.switch3, (256,128))  
            #switch on left side
            elif (self.horizontal_wall[decrement(y,2)][x] == 13):
                screen.blit(self.center3, (256,128))
                
            #draw straight two block wall right one
            if (self.horizontal_wall[decrement(y,2)][increment(x,1)] == 1):
                screen.blit(self.center3, (384, 128))
            elif (self.horizontal_wall[decrement(y,2)][increment(x,1)] == 2):
                screen.blit(self.door3, (384,128))
            elif (self.horizontal_wall[decrement(y,2)][increment(x,1)] == 3):
                screen.blit(self.door3, (384,128))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,2)][increment(x,1)] == 4):
                screen.blit(self.door3, (384,128))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,2)][increment(x,1)] == 6):
                screen.blit(self.door3, (384,128))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,2)][increment(x,1)] == 7):
                screen.blit(self.center3, (384,128))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,2)][increment(x,1)] == 8):
                screen.blit(self.door3, (384,128))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,2)][increment(x,1)] == 9):
                screen.blit(self.center3, (384,128))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,2)][increment(x,1)] == 12):
                screen.blit(self.switch3, (384,128))  
            #switch on left side
            elif (self.horizontal_wall[decrement(y,2)][increment(x,1)] == 13):
                screen.blit(self.center3, (384,128))
                
            #draw straight two block wall right two
            if (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 1):
                screen.blit(self.center3, (512, 128))
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 2):
                screen.blit(self.door3, (512,128))
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 3):
                screen.blit(self.door3, (512,128))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 4):
                screen.blit(self.door3, (512,128))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 6):
                screen.blit(self.door3, (512,128))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 7):
                screen.blit(self.center3, (512,128))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 8):
                screen.blit(self.door3, (512,128))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 9):
                screen.blit(self.center3, (512,128))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 12):
                screen.blit(self.switch3, (512,128))  
            #switch on left side
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 13):
                screen.blit(self.center3, (512,128))

            #draw up two wall on left three
            if (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 1):
                screen.blit(self.edgeList3_3[0], (-320, 64))
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 2):
                screen.blit(self.doorList3_3[0], (-320, 64))
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 3):
                screen.blit(self.doorList3_3[0], (-320, 64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 4):
                screen.blit(self.doorList3_3[0], (-320, 64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 6):
                screen.blit(self.doorList3_3[0], (-320, 64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 7):
                screen.blit(self.edgeList3_3[0], (-320, 64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 8):
                screen.blit(self.doorList3_3[0], (-320, 64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 9):
                screen.blit(self.edgeList3_3[0], (-320, 64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 12):
                screen.blit(self.switchedgeList3_3[0], (-320, 64)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 13):
                screen.blit(self.edgeList3_3[0], (-320, 64)) 


            #draw up two wall on left two
            if (self.vertical_wall[decrement(y,2)][decrement(x,1)] == 1):
                screen.blit(self.edgeList3_2[0], (-64, 64))
            elif (self.vertical_wall[decrement(y,2)][decrement(x,1)] == 2):
                screen.blit(self.doorList3_2[0], (-64, 64))
            elif (self.vertical_wall[decrement(y,2)][decrement(x,1)] == 3):
                screen.blit(self.doorList3_2[0], (-64, 64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,2)][decrement(x,1)] == 4):
                screen.blit(self.doorList3_2[0], (-64, 64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,2)][decrement(x,1)] == 6):
                screen.blit(self.doorList3_2[0], (-64, 64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,2)][decrement(x,1)] == 7):
                screen.blit(self.edgeList3_2[0], (-64, 64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,2)][decrement(x,1)] == 8):
                screen.blit(self.doorList3_2[0], (-64, 64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,2)][decrement(x,1)] == 9):
                screen.blit(self.edgeList3_2[0], (-64, 64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,2)][decrement(x,1)] == 12):
                screen.blit(self.switchedgeList3_2[0], (-64, 64)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,2)][decrement(x,1)] == 13):
                screen.blit(self.edgeList3_2[0], (-64, 64)) 

            #draw up two wall on left
            if (self.vertical_wall[decrement(y,2)][x] == 1):
                screen.blit(self.edgeList3[0], (192, 64))
            elif (self.vertical_wall[decrement(y,2)][x] == 2):
                screen.blit(self.doorList3[0], (192, 64))
            elif (self.vertical_wall[decrement(y,2)][x] == 3):
                screen.blit(self.doorList3[0], (192, 64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,2)][x] == 4):
                screen.blit(self.doorList3[0], (-64, 64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,2)][x] == 6):
                screen.blit(self.doorList3[0], (-64, 64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,2)][x] == 7):
                screen.blit(self.edgeList3[0], (-64, 64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,2)][x] == 8):
                screen.blit(self.doorList3[0], (-64, 64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,2)][x] == 9):
                screen.blit(self.edgeList3[0], (-64, 64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,2)][x] == 12):
                screen.blit(self.switchedgeList3[0], (-64, 64)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,2)][x] == 13):
                screen.blit(self.edgeList3[0], (-64, 64)) 
                
            #draw up two wall on right three
            if (self.vertical_wall[decrement(y,2)][increment(x,3)] == 1):
                screen.blit(self.edgeList3_3[1], (640, 64))                
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 2):
                screen.blit(self.doorList3_3[1], (640, 64))    
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 3):
                screen.blit(self.doorList3_3[1], (640, 64))    
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 4):
                screen.blit(self.doorList3_3[1], (640, 64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 6):
                screen.blit(self.edgeList3_3[1], (640, 64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 7):
                screen.blit(self.doorList3_3[1], (640, 64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 8):
                screen.blit(self.edgeList3_3[1], (640, 64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 9):
                screen.blit(self.doorList3_3[1], (640, 64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 12):
                screen.blit(self.edgeList3_3[1], (640, 64)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 13):
                screen.blit(self.switchedgeList3_3[1], (640, 64)) 



            #draw up two wall on right two
            if (self.vertical_wall[decrement(y,2)][increment(x,2)] == 1):
                screen.blit(self.edgeList3_2[1], (512, 64))                
            elif (self.vertical_wall[decrement(y,2)][increment(x,2)] == 2):
                screen.blit(self.doorList3_2[1], (512, 64))    
            elif (self.vertical_wall[decrement(y,2)][increment(x,2)] == 3):
                screen.blit(self.doorList3_2[1], (512, 64))    
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,2)][increment(x,2)] == 4):
                screen.blit(self.doorList3_2[1], (512, 64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,2)][increment(x,2)] == 6):
                screen.blit(self.edgeList3_2[1], (512, 64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,2)][increment(x,2)] == 7):
                screen.blit(self.doorList3_2[1], (512, 64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,2)][increment(x,2)] == 8):
                screen.blit(self.edgeList3_2[1], (512, 64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,2)][increment(x,2)] == 9):
                screen.blit(self.doorList3_2[1], (512, 64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,2)][increment(x,2)] == 12):
                screen.blit(self.edgeList3_2[1], (512, 64)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,2)][increment(x,2)] == 13):
                screen.blit(self.switchedgeList3_2[1], (512, 64)) 


            #draw up two wall on right
            if (self.vertical_wall[decrement(y,2)][increment(x,1)] == 1):
                screen.blit(self.edgeList3[1], (384, 64))                
            elif (self.vertical_wall[decrement(y,2)][increment(x,1)] == 2):
                screen.blit(self.doorList3[1], (384, 64))                
            elif (self.vertical_wall[decrement(y,2)][increment(x,1)] == 3):
                screen.blit(self.doorList3[1], (384, 64))                
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,2)][increment(x,1)] == 4):
                screen.blit(self.doorList3[1], (384, 64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,2)][increment(x,1)] == 6):
                screen.blit(self.edgeList3[1], (384, 64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,2)][increment(x,1)] == 7):
                screen.blit(self.doorList3[1], (384, 64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,2)][increment(x,1)] == 8):
                screen.blit(self.edgeList3[1], (384, 64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,2)][increment(x,1)] == 9):
                screen.blit(self.doorList3[1], (384, 64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,2)][increment(x,1)] == 12):
                screen.blit(self.edgeList3[1], (384, 64)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,2)][increment(x,1)] == 13):
                screen.blit(self.switchedgeList3[1], (384, 64)) 

            #draw straight one block wall left one
            if (self.horizontal_wall[decrement(y,1)][decrement(x,1)] == 1):
                screen.blit(self.center2, (-64, 64))
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,1)] == 2):
                screen.blit(self.door2, (-64,64))
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,1)] == 3):
                screen.blit(self.door2, (-64,64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,1)] == 4):
                screen.blit(self.door2, (-64,64))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,1)] == 6):
                screen.blit(self.door2, (-64,64))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,1)] == 7):
                screen.blit(self.center2, (-64,64))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,1)] == 8):
                screen.blit(self.door2, (-64,64))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,1)] == 9):
                screen.blit(self.center2, (-64,64))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,1)] == 12):
                screen.blit(self.switch2, (-64,64))  
            #switch on left side
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,1)] == 13):
                screen.blit(self.center2, (-64,64))
        
            #draw straight one block wall
            if (self.horizontal_wall[decrement(y,1)][x] == 1):
                screen.blit(self.center2, (192, 64))
            elif (self.horizontal_wall[decrement(y,1)][x] == 2):
                screen.blit(self.door2, (192,64))
            elif (self.horizontal_wall[decrement(y,1)][x] == 3):
                screen.blit(self.door2, (192,64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,1)][x] == 4):
                screen.blit(self.door2, (192,64))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,1)][x] == 6):
                screen.blit(self.door2, (192,64))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,1)][x] == 7):
                screen.blit(self.center2, (192,64))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,1)][x] == 8):
                screen.blit(self.door2, (192,64))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,1)][x] == 9):
                screen.blit(self.center2, (192,64))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,1)][x] == 12):
                screen.blit(self.switch2, (192,64))  
            #switch on left side
            elif (self.horizontal_wall[decrement(y,1)][x] == 13):
                screen.blit(self.center2, (192,64))

            #draw straight one block wall right one
            if (self.horizontal_wall[decrement(y,1)][increment(x,1)] == 1):
                screen.blit(self.center2, (448, 64))
            elif (self.horizontal_wall[decrement(y,1)][increment(x,1)] == 2):
                screen.blit(self.door2, (448,64))
            elif (self.horizontal_wall[decrement(y,1)][increment(x,1)] == 3):
                screen.blit(self.door2, (448,64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,1)][increment(x,1)] == 4):
                screen.blit(self.door2, (448,64))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,1)][increment(x,1)] == 6):
                screen.blit(self.door2, (448,64))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,1)][increment(x,1)] == 7):
                screen.blit(self.center2, (448,64))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,1)][increment(x,1)] == 8):
                screen.blit(self.door2, (448,64))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,1)][increment(x,1)] == 9):
                screen.blit(self.center2, (448,64))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,1)][increment(x,1)] == 12):
                screen.blit(self.switch2, (448,64))  
            #switch on left side
            elif (self.horizontal_wall[decrement(y,1)][increment(x,1)] == 13):
                screen.blit(self.center2, (448,64))

            #draw up two wall on left
            if (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 1):
                screen.blit(self.edgeList2[0], (-192, -64))
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 2):
                screen.blit(self.doorList2[0], (-192, -64))
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 3):
                screen.blit(self.doorList2[0], (-192, -64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 4):
                screen.blit(self.doorList2[0], (-192, -64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 6):
                screen.blit(self.doorList2[0], (-192, -64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 7):
                screen.blit(self.edgeList2[0], (-192, -64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 8):
                screen.blit(self.doorList2[0], (-192, -64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 9):
                screen.blit(self.edgeList2[0], (-192, -64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 12):
                screen.blit(self.switchedgeList2[0], (-192, -64)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 13):
                screen.blit(self.edgeList2[0], (-192, -64)) 
                                  

            #draw up one wall on left
            if (self.vertical_wall[decrement(y,1)][x] == 1):
                screen.blit(self.edgeList2[0], (64, -64))
            elif (self.vertical_wall[decrement(y,1)][x] == 2):
                screen.blit(self.doorList2[0], (64, -64))
            elif (self.vertical_wall[decrement(y,1)][x] == 3):
                screen.blit(self.doorList2[0], (64, -64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,1)][x] == 4):
                screen.blit(self.doorList2[0], (64, -64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,1)][x] == 6):
                screen.blit(self.doorList2[0], (64, -64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,1)][x] == 7):
                screen.blit(self.edgeList2[0], (64, -64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,1)][x] == 8):
                screen.blit(self.doorList2[0], (64, -64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,1)][x] == 9):
                screen.blit(self.edgeList2[0], (64, -64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,1)][x] == 12):
                screen.blit(self.switchedgeList2[0], (64, -64)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,1)][x] == 13):
                screen.blit(self.edgeList2[0], (64, -64)) 
                                   
            #draw up one wall on right
            if (self.vertical_wall[decrement(y,1)][increment(x,1)] == 1):
                screen.blit(self.edgeList2[1], (448, -64))                
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 2):
                screen.blit(self.doorList2[1], (448, -64))                
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 3):
                screen.blit(self.doorList2[1], (448, -64))                
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 4):
                screen.blit(self.doorList2[1], (448, -64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 6):
                screen.blit(self.edgeList2[1], (448, -64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 7):
                screen.blit(self.doorList2[1], (448, -64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 8):
                screen.blit(self.edgeList2[1], (448, -64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 9):
                screen.blit(self.doorList2[1], (448, -64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 12):
                screen.blit(self.edgeList2[1], (448, -64)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 13):
                screen.blit(self.switchedgeList2[1], (448, -64)) 

            #draw left one up wall
            if (self.horizontal_wall[y][decrement(x,1)] == 1):
                screen.blit(self.center1, (-448,-64))
            elif (self.horizontal_wall[y][decrement(x,1)] == 2):
                screen.blit(self.door1, (-448,-64))
            elif (self.horizontal_wall[y][decrement(x,1)] == 3):
                screen.blit(self.door1, (-448,-64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][decrement(x,1)] == 4):
                screen.blit(self.door1, (-448,-64))
            #one way door from right
            elif (self.horizontal_wall[y][decrement(x,1)] == 6):
                screen.blit(self.door1, (-448,-64))
            #one way door from left
            elif (self.horizontal_wall[y][decrement(x,1)] == 7):
                screen.blit(self.center1, (-448,-64))
            #hidden one way door from right
            elif (self.horizontal_wall[y][decrement(x,1)] == 8):
                screen.blit(self.door1, (-448,-64))
            #hidden one way door from left
            elif (self.horizontal_wall[y][decrement(x,1)] == 9):
                screen.blit(self.center1, (-448,-64))
            #switch on right side
            elif (self.horizontal_wall[y][decrement(x,1)] == 12):
                screen.blit(self.switch1, (-448,-64))  
            #switch on left side
            elif (self.horizontal_wall[y][decrement(x,1)] == 13):
                screen.blit(self.center1, (-448,-64))


            #draw right one up wall
            if (self.horizontal_wall[y][increment(x,1)] == 1):
                screen.blit(self.center1, (576,-64))
            elif (self.horizontal_wall[y][increment(x,1)] == 2):
                screen.blit(self.door1, (576,-64))
            elif (self.horizontal_wall[y][increment(x,1)] == 3):
                screen.blit(self.door1, (576,-64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][increment(x,1)] == 4):
                screen.blit(self.door1, (576,-64))
            #one way door from right
            elif (self.horizontal_wall[y][increment(x,1)] == 6):
                screen.blit(self.door1, (576,-64))
            #one way door from left
            elif (self.horizontal_wall[y][increment(x,1)] == 7):
                screen.blit(self.center1, (576,-64))
            #hidden one way door from right
            elif (self.horizontal_wall[y][increment(x,1)] == 8):
                screen.blit(self.door1, (576,-64))
            #hidden one way door from left
            elif (self.horizontal_wall[y][increment(x,1)] == 9):
                screen.blit(self.center1, (576,-64))
            #switch on right side
            elif (self.horizontal_wall[y][increment(x,1)] == 12):
                screen.blit(self.switch1,(576,-64))  
            #switch on left side
            elif (self.horizontal_wall[y][increment(x,1)] == 13):
                screen.blit(self.center1, (576,-64))


            #draw just up wall
            if (self.horizontal_wall[y][x] == 1):
                screen.blit(self.center1, (64,-64))
            elif (self.horizontal_wall[y][x] == 2):
                screen.blit(self.door1, (64,-64))
            elif (self.horizontal_wall[y][x] == 3):
                screen.blit(self.door1, (64,-64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][x] == 4):
                screen.blit(self.door1, (64,-64))
            #one way door from right
            elif (self.horizontal_wall[y][x] == 6):
                screen.blit(self.door1, (64,-64))
            #one way door from left
            elif (self.horizontal_wall[y][x] == 7):
                screen.blit(self.center1, (64,-64))
            #hidden one way door from right
            elif (self.horizontal_wall[y][x] == 8):
                screen.blit(self.door1, (64,-64))
            #hidden one way door from left
            elif (self.horizontal_wall[y][x] == 9):
                screen.blit(self.center1, (64,-64))
            #switch on right side
            elif (self.horizontal_wall[y][x] == 12):
                screen.blit(self.switch1,(64,-64))  
            #switch on left side
            elif (self.horizontal_wall[y][x] == 13):
                screen.blit(self.center1, (64,-64))


            #draw wall on left
            if (self.vertical_wall[y][x] == 1):
                screen.blit(self.edgeList1[0], (-192, -320))
            elif (self.vertical_wall[y][x] == 2):
                screen.blit(self.doorList1[0], (-192, -320))
            elif (self.vertical_wall[y][x] == 3):
                screen.blit(self.doorList1[0], (-192, -320))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][x] == 4):
                screen.blit(self.doorList1[0], (-192, -320))
            #one way door from right
            elif (self.vertical_wall[y][x] == 6):
                screen.blit(self.doorList1[0], (-192, -320))
            #one way door from left
            elif (self.vertical_wall[y][x] == 7):
                screen.blit(self.edgeList1[0], (-192, -320))
            #hidden one way door from right
            elif (self.vertical_wall[y][x] == 8):
                screen.blit(self.doorList1[0], (-192, -320))
            #hidden one way door from left
            elif (self.vertical_wall[y][x] == 9):
                screen.blit(self.edgeList1[0], (-192, -320))
            #switch on right side
            elif (self.vertical_wall[y][x] == 12):
                screen.blit(self.switchedgeList1[0], (-192, -320)) 
            #switch on left side
            elif (self.vertical_wall[y][x] == 13):
                screen.blit(self.edgeList1[0], (-192, -320)) 

            #draw wall on right
            if (self.vertical_wall[y][increment(x,1)] == 1):
                screen.blit(self.edgeList1[1], (576, -320))
            elif (self.vertical_wall[y][increment(x,1)] == 2):
                screen.blit(self.doorList1[1], (576, -320))
            elif (self.vertical_wall[y][increment(x,1)] == 3):
                screen.blit(self.doorList1[1], (576, -320))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][increment(x,1)] == 4):
                screen.blit(self.doorList1[1], (576, -320))
            #one way door from right
            elif (self.vertical_wall[y][increment(x,1)] == 6):
                screen.blit(self.edgeList1[1], (576, -320))
            #one way door from left
            elif (self.vertical_wall[y][increment(x,1)] == 7):
                screen.blit(self.doorList1[1], (576, -320))
            #hidden one way door from right
            elif (self.vertical_wall[y][increment(x,1)] == 8):
                screen.blit(self.edgeList1[1], (576, -320))
            #hidden one way door from left
            elif (self.vertical_wall[y][increment(x,1)] == 9):
                screen.blit(self.doorList1[1], (576, -320))
            #switch on right side
            elif (self.vertical_wall[y][increment(x,1)] == 12):
                screen.blit(self.edgeList1[1], (576, -320)) 
            #switch on left side
            elif (self.vertical_wall[y][increment(x,1)] == 13):
                screen.blit(self.switchedgeList1[1], (576, -320)) 

        #if player is looking right
        elif (game_self.party.direction == 1):

            #draw ground below
            draw_dungeon_ground( screen, self.ground[y][x], self.ground_center1, (32, 448))
            #draw ground left
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][x], self.ground_sideList1[0], (0, 448))
            #draw ground right
            draw_dungeon_ground( screen, self.ground[increment(y,1)][x], self.ground_sideList1[1], (576, 448))
            #draw ground up left
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][increment(x,1)], self.ground_sideList2[0], (0,320))
            #draw ground up right
            draw_dungeon_ground( screen, self.ground[increment(y,1)][increment(x,1)], self.ground_sideList2[1], (448,320))
            #draw ground up two left
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][increment(x,2)], self.ground_sideList3[0], (-128,256))
            #draw ground up two right
            draw_dungeon_ground( screen, self.ground[increment(y,1)][increment(x,2)], self.ground_sideList3[1], (384,256))
            #draw ground up two left two
            draw_dungeon_ground( screen, self.ground[decrement(y,2)][increment(x,2)], self.ground_sideList3_2[0], (0,256))
            #draw ground up two right two
            draw_dungeon_ground( screen, self.ground[increment(y,2)][increment(x,2)], self.ground_sideList3_2[1], (576,256))
            #draw ground up three left
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][increment(x,3)], self.ground_sideList4[0], (128,224))
            #draw ground up three right
            draw_dungeon_ground( screen, self.ground[increment(y,1)][increment(x,3)], self.ground_sideList4[1], (352,224))
            #draw ground up three left two
            draw_dungeon_ground( screen, self.ground[decrement(y,2)][increment(x,3)], self.ground_sideList4_2[0], (0,224))
            #draw ground up three right two
            draw_dungeon_ground( screen, self.ground[increment(y,2)][increment(x,3)], self.ground_sideList4_2[1], (416,224))                
            #draw ground up one
            draw_dungeon_ground( screen, self.ground[y][increment(x,1)], self.ground_center2, (64,320))
            #draw ground up two
            draw_dungeon_ground( screen, self.ground[y][increment(x,2)], self.ground_center3, (192,256))                
            #draw ground up three
            draw_dungeon_ground( screen, self.ground[y][increment(x,3)], self.ground_center4, (256,224))



            #draw straight three block wall left two
            if (self.vertical_wall[decrement(y,2)][increment(x,4)] == 1):
                screen.blit(self.center4, (160, 160))
            elif (self.vertical_wall[decrement(y,2)][increment(x,4)] == 2):
                screen.blit(self.door4, (160,160))                                               
            elif (self.vertical_wall[decrement(y,2)][increment(x,4)] == 3):
                screen.blit(self.door4, (160,160))                                               
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,2)][increment(x,4)] == 4):
                screen.blit(self.door4, (160,160))
            #one way door from right
            elif (self.vertical_wall[decrement(y,2)][increment(x,4)] == 6):
                screen.blit(self.center4, (160,160))
            #one way door from left
            elif (self.vertical_wall[decrement(y,2)][increment(x,4)] == 7):
                screen.blit(self.door4, (160,160))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,2)][increment(x,4)] == 8):
                screen.blit(self.center4, (160,160))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,2)][increment(x,4)] == 9):
                screen.blit(self.door4, (160,160))
            #switch on right side
            elif (self.vertical_wall[decrement(y,2)][increment(x,4)] == 12):
                screen.blit(self.center4, (160,160))                                                               
            #switch on left side
            elif (self.vertical_wall[decrement(y,2)][increment(x,4)] == 13):
                screen.blit(self.switch4, (160,160))   


            #draw straight three block wall left one
            if (self.vertical_wall[decrement(y,1)][increment(x,4)] == 1):
                screen.blit(self.center4, (224, 160))
            elif (self.vertical_wall[decrement(y,1)][increment(x,4)] == 2):
                screen.blit(self.door4, (224,160))                                               
            elif (self.vertical_wall[decrement(y,1)][increment(x,4)] == 3):
                screen.blit(self.door4, (224,160))                                               
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,1)][increment(x,4)] == 4):
                screen.blit(self.door4, (224,160))
            #one way door from right
            elif (self.vertical_wall[decrement(y,1)][increment(x,4)] == 6):
                screen.blit(self.center4, (224,160))
            #one way door from left
            elif (self.vertical_wall[decrement(y,1)][increment(x,4)] == 7):
                screen.blit(self.door4, (224,160))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,1)][increment(x,4)] == 8):
                screen.blit(self.center4, (224,160))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,1)][increment(x,4)] == 9):
                screen.blit(self.door4, (224,160))
            #switch on right side
            elif (self.vertical_wall[decrement(y,1)][increment(x,4)] == 12):
                screen.blit(self.center4, (224,160))                                                               
            #switch on left side
            elif (self.vertical_wall[decrement(y,1)][increment(x,4)] == 13):
                screen.blit(self.switch4, (224,160))   


            #draw straight three block wall
            if (self.vertical_wall[y][increment(x,4)] == 1):
                screen.blit(self.center4, (288, 160))
            elif (self.vertical_wall[y][increment(x,4)] == 2):
                screen.blit(self.door4, (288,160))
            elif (self.vertical_wall[y][increment(x,4)] == 3):
                screen.blit(self.door4, (288,160))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][increment(x,4)] == 4):
                screen.blit(self.door4, (288,160))
            #one way door from right
            elif (self.vertical_wall[y][increment(x,4)] == 6):
                screen.blit(self.center4, (288,160))
            #one way door from left
            elif (self.vertical_wall[y][increment(x,4)] == 7):
                screen.blit(self.door4, (288,160))
            #hidden one way door from right
            elif (self.vertical_wall[y][increment(x,4)] == 8):
                screen.blit(self.center4, (288,160))
            #hidden one way door from left
            elif (self.vertical_wall[y][increment(x,4)] == 9):
                screen.blit(self.door4, (288,160))
            #switch on right side
            elif (self.vertical_wall[y][increment(x,4)] == 12):
                screen.blit(self.center4, (288,160))                                                               
            #switch on left side
            elif (self.vertical_wall[y][increment(x,4)] == 13):
                screen.blit(self.switch4, (288,160))   


            #draw straight three block wall right one
            if (self.vertical_wall[increment(y,1)][increment(x,4)] == 1):
                screen.blit(self.center4, (352, 160))
            elif (self.vertical_wall[increment(y,1)][increment(x,4)] == 2):
                screen.blit(self.door4, (352,160))                                               
            elif (self.vertical_wall[increment(y,1)][increment(x,4)] == 3):
                screen.blit(self.door4, (352,160))                                               
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,1)][increment(x,4)] == 4):
                screen.blit(self.door4, (352,160))
            #one way door from right
            elif (self.vertical_wall[increment(y,1)][increment(x,4)] == 6):
                screen.blit(self.center4, (352,160))
            #one way door from left
            elif (self.vertical_wall[increment(y,1)][increment(x,4)] == 7):
                screen.blit(self.door4, (352,160))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,1)][increment(x,4)] == 8):
                screen.blit(self.center4, (352,160))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,1)][increment(x,4)] == 9):
                screen.blit(self.door4, (352,160))
            #switch on right side
            elif (self.vertical_wall[increment(y,1)][increment(x,4)] == 12):
                screen.blit(self.center4, (352,160))                                                               
            #switch on left side
            elif (self.vertical_wall[increment(y,1)][increment(x,4)] == 13):
                screen.blit(self.switch4, (352,160)) 

            #draw straight three block wall right two
            if (self.vertical_wall[increment(y,2)][increment(x,4)] == 1):
                screen.blit(self.center4, (416, 160))
            elif (self.vertical_wall[increment(y,2)][increment(x,4)] == 2):
                screen.blit(self.door4, (416,160))
            elif (self.vertical_wall[increment(y,2)][increment(x,4)] == 3):
                screen.blit(self.door4, (416,160))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,2)][increment(x,4)] == 4):
                screen.blit(self.door4, (416,160))
            #one way door from right
            elif (self.vertical_wall[increment(y,2)][increment(x,4)] == 6):
                screen.blit(self.center4, (416,160))
            #one way door from left
            elif (self.vertical_wall[increment(y,2)][increment(x,4)] == 7):
                screen.blit(self.door4, (416,160))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,2)][increment(x,4)] == 8):
                screen.blit(self.center4, (416,160))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,2)][increment(x,4)] == 9):
                screen.blit(self.door4, (416,160))
            #switch on right side
            elif (self.vertical_wall[increment(y,2)][increment(x,4)] == 12):
                screen.blit(self.center4, (416,160))                                                               
            #switch on left side
            elif (self.vertical_wall[increment(y,2)][increment(x,4)] == 13):
                screen.blit(self.switch4, (416,160)) 



            #draw up three wall on left three
            if (self.horizontal_wall[decrement(y,2)][increment(x,3)] == 1):
                screen.blit(self.edgeList4_3[0], (0, 128))
            elif (self.horizontal_wall[decrement(y,2)][increment(x,3)] == 2):
                screen.blit(self.doorList4_3[0], (0, 128))
            elif (self.horizontal_wall[decrement(y,2)][increment(x,3)] == 3):
                screen.blit(self.doorList4_3[0], (0, 128))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,2)][increment(x,3)] == 4):
                screen.blit(self.doorList4_3[0], (0, 128))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,2)][increment(x,3)] == 6):
                screen.blit(self.doorList4_3[0], (0, 128))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,2)][increment(x,3)] == 7):
                screen.blit(self.edgeList4_3[0], (0, 128))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,2)][increment(x,3)] == 8):
                screen.blit(self.doorList4_3[0], (0, 128))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,2)][increment(x,3)] == 9):
                screen.blit(self.edgeList4_3[0], (0, 128))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,2)][increment(x,3)] == 12):
                screen.blit(self.switchedgeList4_3[0], (0, 128)) 
            #switch on left side
            elif (self.horizontal_wall[decrement(y,2)][increment(x,3)] == 13):
                screen.blit(self.edgeList4_3[0], (0, 128)) 



            #draw up three wall on left two
            if (self.horizontal_wall[decrement(y,1)][increment(x,3)] == 1):
                screen.blit(self.edgeList4_2[0], (128, 128))
            elif (self.horizontal_wall[decrement(y,1)][increment(x,3)] == 2):
                screen.blit(self.doorList4_2[0], (128, 128))
            elif (self.horizontal_wall[decrement(y,1)][increment(x,3)] == 3):
                screen.blit(self.doorList4_2[0], (128, 128))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,1)][increment(x,3)] == 4):
                screen.blit(self.doorList4_2[0], (128, 128))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,1)][increment(x,3)] == 6):
                screen.blit(self.doorList4_2[0], (128, 128))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,1)][increment(x,3)] == 7):
                screen.blit(self.edgeList4_2[0], (128, 128))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,1)][increment(x,3)] == 8):
                screen.blit(self.doorList4_2[0], (128, 128))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,1)][increment(x,3)] == 9):
                screen.blit(self.edgeList4_2[0], (128, 128))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,1)][increment(x,3)] == 12):
                screen.blit(self.switchedgeList4_2[0], (128, 128)) 
            #switch on left side
            elif (self.horizontal_wall[decrement(y,1)][increment(x,3)] == 13):
                screen.blit(self.edgeList4_2[0], (128, 128)) 



            #draw up three wall on left
            if (self.horizontal_wall[y][increment(x,3)] == 1):
                screen.blit(self.edgeList4[0], (256, 128))
            elif (self.horizontal_wall[y][increment(x,3)] == 2):
                screen.blit(self.doorList4[0], (256, 128))
            elif (self.horizontal_wall[y][increment(x,3)] == 3):
                screen.blit(self.doorList4[0], (256, 128))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][increment(x,3)] == 4):
                screen.blit(self.doorList4[0], (256, 128))
            #one way door from right
            elif (self.horizontal_wall[y][increment(x,3)] == 6):
                screen.blit(self.doorList4[0], (256, 128))
            #one way door from left
            elif (self.horizontal_wall[y][increment(x,3)] == 7):
                screen.blit(self.edgeList4[0], (256, 128))
            #hidden one way door from right
            elif (self.horizontal_wall[y][increment(x,3)] == 8):
                screen.blit(self.doorList4[0], (256, 128))
            #hidden one way door from left
            elif (self.horizontal_wall[y][increment(x,3)] == 9):
                screen.blit(self.edgeList4[0], (256, 128))
            #switch on right side
            elif (self.horizontal_wall[y][increment(x,3)] == 12):
                screen.blit(self.switchedgeList4[0], (256, 128)) 
            #switch on left side
            elif (self.horizontal_wall[y][increment(x,3)] == 13):
                screen.blit(self.edgeList4[0], (256, 128)) 


            #draw up three wall on right three
            if (self.horizontal_wall[increment(y,3)][increment(x,3)] == 1):
                screen.blit(self.edgeList4_3[1], (480, 128))                
            elif (self.horizontal_wall[increment(y,3)][increment(x,3)] == 2):
                screen.blit(self.doorList4_3[1], (480, 128))  
            elif (self.horizontal_wall[increment(y,3)][increment(x,3)] == 3):
                screen.blit(self.doorList4_3[1], (480, 128))  
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,3)][increment(x,3)] == 4):
                screen.blit(self.doorList4_3[1], (480, 128))
            #one way door from right
            elif (self.horizontal_wall[increment(y,3)][increment(x,3)] == 6):
                screen.blit(self.edgeList4_3[1], (480, 128))
            #one way door from left
            elif (self.horizontal_wall[increment(y,3)][increment(x,3)] == 7):
                screen.blit(self.doorList4_3[1], (480, 128))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,3)][increment(x,3)] == 8):
                screen.blit(self.edgeList4_3[1], (480, 128))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,3)][increment(x,3)] == 9):
                screen.blit(self.doorList4_3[1], (480, 128))
            #switch on right side
            elif (self.horizontal_wall[increment(y,3)][increment(x,3)] == 12):
                screen.blit(self.edgeList4_3[1], (480, 128)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,3)][increment(x,3)] == 13):
                screen.blit(self.switchedgeList4_3[1], (480, 128)) 

            #draw up three wall on right two
            if (self.horizontal_wall[increment(y,2)][increment(x,3)] == 1):
                screen.blit(self.edgeList4_2[1], (416, 128))                
            elif (self.horizontal_wall[increment(y,2)][increment(x,3)] == 2):
                screen.blit(self.doorList4_2[1], (416, 128))                               
            elif (self.horizontal_wall[increment(y,2)][increment(x,3)] == 3):
                screen.blit(self.doorList4_2[1], (416, 128))                               
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,2)][increment(x,3)] == 4):
                screen.blit(self.doorList4_2[1], (416, 128))
            #one way door from right
            elif (self.horizontal_wall[increment(y,2)][increment(x,3)] == 6):
                screen.blit(self.edgeList4_2[1], (416, 128))
            #one way door from left
            elif (self.horizontal_wall[increment(y,2)][increment(x,3)] == 7):
                screen.blit(self.doorList4_2[1], (416, 128))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,2)][increment(x,3)] == 8):
                screen.blit(self.edgeList4_2[1], (416, 128))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,2)][increment(x,3)] == 9):
                screen.blit(self.doorList4_2[1], (416, 128))
            #switch on right side
            elif (self.horizontal_wall[increment(y,2)][increment(x,3)] == 12):
                screen.blit(self.edgeList4_2[1], (416, 128)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,2)][increment(x,3)] == 13):
                screen.blit(self.switchedgeList4_2[1], (416, 128)) 

            #draw up three wall on right
            if (self.horizontal_wall[increment(y,1)][increment(x,3)] == 1):
                screen.blit(self.edgeList4[1], (352, 128))                
            elif (self.horizontal_wall[increment(y,1)][increment(x,3)] == 2):
                screen.blit(self.doorList4[1], (352, 128))                
            elif (self.horizontal_wall[increment(y,1)][increment(x,3)] == 3):
                screen.blit(self.doorList4[1], (352, 128))                
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,1)][increment(x,3)] == 4):
                screen.blit(self.doorList4[1], (352, 128))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][increment(x,3)] == 6):
                screen.blit(self.edgeList4[1], (352, 128))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][increment(x,3)] == 7):
                screen.blit(self.doorList4[1], (352, 128))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][increment(x,3)] == 8):
                screen.blit(self.edgeList4[1], (352, 128))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][increment(x,3)] == 9):
                screen.blit(self.doorList4[1], (352, 128))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][increment(x,3)] == 12):
                screen.blit(self.edgeList4[1], (352, 128)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][increment(x,3)] == 13):
                screen.blit(self.switchedgeList4[1], (352, 128)) 

            #draw straight two block wall left two
            if (self.vertical_wall[decrement(y,2)][increment(x,3)] == 1):
                screen.blit(self.center3, (0, 128))
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 2):
                screen.blit(self.door3, (0,128))
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 3):
                screen.blit(self.door3, (0,128))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 4):
                screen.blit(self.door3, (0,128))
            #one way door from right
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 6):
                screen.blit(self.center3, (0,128))
            #one way door from left
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 7):
                screen.blit(self.door3, (0,128))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 8):
                screen.blit(self.center3, (0,128))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 9):
                screen.blit(self.door3, (0,128))
            #switch on right side
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 12):
                screen.blit(self.center3, (0,128))                                                               
            #switch on left side
            elif (self.vertical_wall[decrement(y,2)][increment(x,3)] == 13):
                screen.blit(self.switch3, (0,128)) 

            #draw straight two block wall left one
            if (self.vertical_wall[decrement(y,1)][increment(x,3)] == 1):
                screen.blit(self.center3, (128, 128))
            elif (self.vertical_wall[decrement(y,1)][increment(x,3)] == 2):
                screen.blit(self.door3, (128,128))
            elif (self.vertical_wall[decrement(y,1)][increment(x,3)] == 3):
                screen.blit(self.door3, (128,128))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,1)][increment(x,3)] == 4):
                screen.blit(self.door3, (128,128))
            #one way door from right
            elif (self.vertical_wall[decrement(y,1)][increment(x,3)] == 6):
                screen.blit(self.center3, (128,128))
            #one way door from left
            elif (self.vertical_wall[decrement(y,1)][increment(x,3)] == 7):
                screen.blit(self.door3, (128,128))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,1)][increment(x,3)] == 8):
                screen.blit(self.center3, (128,128))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,1)][increment(x,3)] == 9):
                screen.blit(self.door3, (128,128))
            #switch on right side
            elif (self.vertical_wall[decrement(y,1)][increment(x,3)] == 12):
                screen.blit(self.center3, (128,128))                                                               
            #switch on left side
            elif (self.vertical_wall[decrement(y,1)][increment(x,3)] == 13):
                screen.blit(self.switch3, (128,128)) 


            #draw straight two block wall
            if (self.vertical_wall[y][increment(x,3)] == 1):
                screen.blit(self.center3, (256, 128))
            elif (self.vertical_wall[y][increment(x,3)] == 2):
                screen.blit(self.door3, (256,128))
            elif (self.vertical_wall[y][increment(x,3)] == 3):
                screen.blit(self.door3, (256,128))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][increment(x,3)] == 4):
                screen.blit(self.door3, (256,128))
            #one way door from right
            elif (self.vertical_wall[y][increment(x,3)] == 6):
                screen.blit(self.center3, (256,128))
            #one way door from left
            elif (self.vertical_wall[y][increment(x,3)] == 7):
                screen.blit(self.door3, (256,128))
            #hidden one way door from right
            elif (self.vertical_wall[y][increment(x,3)] == 8):
                screen.blit(self.center3, (256,128))
            #hidden one way door from left
            elif (self.vertical_wall[y][increment(x,3)] == 9):
                screen.blit(self.door3, (256,128))
            #switch on right side
            elif (self.vertical_wall[y][increment(x,3)] == 12):
                screen.blit(self.center3, (256,128))                                                               
            #switch on left side
            elif (self.vertical_wall[y][increment(x,3)] == 13):
                screen.blit(self.switch3, (256,128)) 

            #draw straight two block wall right one
            if (self.vertical_wall[increment(y,1)][increment(x,3)] == 1):
                screen.blit(self.center3, (384, 128))
            elif (self.vertical_wall[increment(y,1)][increment(x,3)] == 2):
                screen.blit(self.door3, (384,128))
            elif (self.vertical_wall[increment(y,1)][increment(x,3)] == 3):
                screen.blit(self.door3, (384,128))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,1)][increment(x,3)] == 4):
                screen.blit(self.door3, (384,128))
            #one way door from right
            elif (self.vertical_wall[increment(y,1)][increment(x,3)] == 6):
                screen.blit(self.center3, (384,128))
            #one way door from left
            elif (self.vertical_wall[increment(y,1)][increment(x,3)] == 7):
                screen.blit(self.door3, (384,128))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,1)][increment(x,3)] == 8):
                screen.blit(self.center3, (384,128))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,1)][increment(x,3)] == 9):
                screen.blit(self.door3, (384,128))
            #switch on right side
            elif (self.vertical_wall[increment(y,1)][increment(x,3)] == 12):
                screen.blit(self.center3, (384,128))                                                               
            #switch on left side
            elif (self.vertical_wall[increment(y,1)][increment(x,3)] == 13):
                screen.blit(self.switch3, (384,128)) 

            #draw straight two block wall right two
            if (self.vertical_wall[increment(y,2)][increment(x,3)] == 1):
                screen.blit(self.center3, (512, 128))
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 2):
                screen.blit(self.door3, (512,128))
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 3):
                screen.blit(self.door3, (512,128))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 4):
                screen.blit(self.door3, (512,128))
            #one way door from right
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 6):
                screen.blit(self.center3, (512,128))
            #one way door from left
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 7):
                screen.blit(self.door3, (512,128))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 8):
                screen.blit(self.center3, (512,128))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 9):
                screen.blit(self.door3, (512,128))
            #switch on right side
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 12):
                screen.blit(self.center3, (512,128))                                                               
            #switch on left side
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 13):
                screen.blit(self.switch3, (512,128)) 


            #draw up two wall on left three
            if (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 1):
                screen.blit(self.edgeList3_3[0], (-320, 64))
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 2):
                screen.blit(self.doorList3_3[0], (-320, 64))
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 3):
                screen.blit(self.doorList3_3[0], (-320, 64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 4):
                screen.blit(self.doorList3_3[0], (-320, 64))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 6):
                screen.blit(self.doorList3_3[0], (-320, 64))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 7):
                screen.blit(self.edgeList3_3[0], (-320, 64))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 8):
                screen.blit(self.doorList3_3[0], (-320, 64))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 9):
                screen.blit(self.edgeList3_3[0], (-320, 64))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 12):
                screen.blit(self.switchedgeList3_3[0], (-320, 64)) 
            #switch on left side
            elif (self.horizontal_wall[decrement(y,2)][increment(x,2)] == 13):
                screen.blit(self.edgeList3_3[0], (-320, 64)) 


            #draw up two wall on left two
            if (self.horizontal_wall[decrement(y,1)][increment(x,2)] == 1):
                screen.blit(self.edgeList3_2[0], (-64, 64))
            elif (self.horizontal_wall[decrement(y,1)][increment(x,2)] == 2):
                screen.blit(self.doorList3_2[0], (-64, 64))
            elif (self.horizontal_wall[decrement(y,1)][increment(x,2)] == 3):
                screen.blit(self.doorList3_2[0], (-64, 64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,1)][increment(x,2)] == 4):
                screen.blit(self.doorList3_2[0], (-64, 64))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,1)][increment(x,2)] == 6):
                screen.blit(self.doorList3_2[0], (-64, 64))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,1)][increment(x,2)] == 7):
                screen.blit(self.edgeList3_2[0], (-64, 64))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,1)][increment(x,2)] == 8):
                screen.blit(self.doorList3_2[0], (-64, 64))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,1)][increment(x,2)] == 9):
                screen.blit(self.edgeList3_2[0], (-64, 64))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,1)][increment(x,2)] == 12):
                screen.blit(self.switchedgeList3_2[0], (-64, 64)) 
            #switch on left side
            elif (self.horizontal_wall[decrement(y,1)][increment(x,2)] == 13):
                screen.blit(self.edgeList3_2[0], (-64, 64)) 

            #draw up two wall on left
            if (self.horizontal_wall[y][increment(x,2)] == 1):
                screen.blit(self.edgeList3[0], (192, 64))
            elif (self.horizontal_wall[y][increment(x,2)] == 2):
                screen.blit(self.doorList3[0], (192, 64))
            elif (self.horizontal_wall[y][increment(x,2)] == 3):
                screen.blit(self.doorList3[0], (192, 64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][increment(x,2)] == 4):
                screen.blit(self.doorList3[0], (192, 64))
            #one way door from right
            elif (self.horizontal_wall[y][increment(x,2)] == 6):
                screen.blit(self.doorList3[0], (192, 64))
            #one way door from left
            elif (self.horizontal_wall[y][increment(x,2)] == 7):
                screen.blit(self.edgeList3[0], (192, 64))
            #hidden one way door from right
            elif (self.horizontal_wall[y][increment(x,2)] == 8):
                screen.blit(self.doorList3[0], (192, 64))
            #hidden one way door from left
            elif (self.horizontal_wall[y][increment(x,2)] == 9):
                screen.blit(self.edgeList3[0], (192, 64))
            #switch on right side
            elif (self.horizontal_wall[y][increment(x,2)] == 12):
                screen.blit(self.switchedgeList3[0], (192, 64)) 
            #switch on left side
            elif (self.horizontal_wall[y][increment(x,2)] == 13):
                screen.blit(self.edgeList3[0], (192, 64)) 
                
            #draw up two wall on right three
            if (self.horizontal_wall[increment(y,3)][increment(x,2)] == 1):
                screen.blit(self.edgeList3_3[1], (640, 64))                
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 2):
                screen.blit(self.doorList3_3[1], (640, 64))    
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 3):
                screen.blit(self.doorList3_3[1], (640, 64))    
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 4):
                screen.blit(self.doorList3_3[1],  (640, 64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 6):
                screen.blit(self.edgeList3_3[1],  (640, 64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 7):
                screen.blit(self.doorList3_3[1],  (640, 64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 8):
                screen.blit(self.edgeList3_3[1],  (640, 64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 9):
                screen.blit(self.doorList3_3[1],  (640, 64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 12):
                screen.blit(self.edgeList3_3[1],  (640, 64)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 13):
                screen.blit(self.switchedgeList3_3[1],  (640, 64)) 


            #draw up two wall on right two
            if (self.horizontal_wall[increment(y,2)][increment(x,2)] == 1):
                screen.blit(self.edgeList3_2[1], (512, 64))                
            elif (self.horizontal_wall[increment(y,2)][increment(x,2)] == 2):
                screen.blit(self.doorList3_2[1], (512, 64))    
            elif (self.horizontal_wall[increment(y,2)][increment(x,2)] == 3):
                screen.blit(self.doorList3_2[1], (512, 64))    
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,2)][increment(x,2)] == 4):
                screen.blit(self.doorList3_2[1],  (512, 64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,2)][increment(x,2)] == 6):
                screen.blit(self.edgeList3_2[1],  (512, 64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,2)][increment(x,2)] == 7):
                screen.blit(self.doorList3_2[1],  (512, 64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,2)][increment(x,2)] == 8):
                screen.blit(self.edgeList3_2[1],  (512, 64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,2)][increment(x,2)] == 9):
                screen.blit(self.doorList3_2[1],  (512, 64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,2)][increment(x,2)] == 12):
                screen.blit(self.edgeList3_2[1],  (512, 64)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,2)][increment(x,2)] == 13):
                screen.blit(self.switchedgeList3_2[1],  (512, 64)) 

            #draw up two wall on right
            if (self.horizontal_wall[increment(y,1)][increment(x,2)] == 1):
                screen.blit(self.edgeList3[1], (384, 64))                
            elif (self.horizontal_wall[increment(y,1)][increment(x,2)] == 2):
                screen.blit(self.doorList3[1], (384, 64))  
            elif (self.horizontal_wall[increment(y,1)][increment(x,2)] == 3):
                screen.blit(self.doorList3[1], (384, 64))  
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,1)][increment(x,2)] == 4):
                screen.blit(self.doorList3[1],  (384, 64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][increment(x,2)] == 6):
                screen.blit(self.edgeList3[1],  (384, 64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][increment(x,2)] == 7):
                screen.blit(self.doorList3[1],  (384, 64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][increment(x,2)] == 8):
                screen.blit(self.edgeList3[1],  (384, 64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][increment(x,2)] == 9):
                screen.blit(self.doorList3[1],  (384, 64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][increment(x,2)] == 12):
                screen.blit(self.edgeList3[1],  (384, 64)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][increment(x,2)] == 13):
                screen.blit(self.switchedgeList3[1],  (384, 64)) 


            #draw straight one block wall left one
            if (self.vertical_wall[decrement(y,1)][increment(x,2)] == 1):
                screen.blit(self.center2, (-64, 64))
            elif (self.vertical_wall[decrement(y,1)][increment(x,2)] == 2):
                screen.blit(self.door2, (-64,64))
            elif (self.vertical_wall[decrement(y,1)][increment(x,2)] == 3):
                screen.blit(self.door2, (-64,64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,1)][increment(x,2)] == 4):
                screen.blit(self.door2, (-64,64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,1)][increment(x,2)] == 6):
                screen.blit(self.center2, (-64,64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,1)][increment(x,2)] == 7):
                screen.blit(self.door2, (-64,64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,1)][increment(x,2)] == 8):
                screen.blit(self.center2, (-64,64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,1)][increment(x,2)] == 9):
                screen.blit(self.door2, (-64,64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,1)][increment(x,2)] == 12):
                screen.blit(self.center2, (-64,64))                                                               
            #switch on left side
            elif (self.vertical_wall[decrement(y,1)][increment(x,2)] == 13):
                screen.blit(self.switch2, (-64,64)) 
        
            #draw straight one block wall
            if (self.vertical_wall[y][increment(x,2)] == 1):
                screen.blit(self.center2, (192, 64))
            elif (self.vertical_wall[y][increment(x,2)] == 2):
                screen.blit(self.door2, (192, 64))
            elif (self.vertical_wall[y][increment(x,2)] == 3):
                screen.blit(self.door2, (192, 64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][increment(x,2)] == 4):
                screen.blit(self.door2, (192,64))
            #one way door from right
            elif (self.vertical_wall[y][increment(x,2)] == 6):
                screen.blit(self.center2, (192,64))
            #one way door from left
            elif (self.vertical_wall[y][increment(x,2)] == 7):
                screen.blit(self.door2, (192,64))
            #hidden one way door from right
            elif (self.vertical_wall[y][increment(x,2)] == 8):
                screen.blit(self.center2, (192,64))
            #hidden one way door from left
            elif (self.vertical_wall[y][increment(x,2)] == 9):
                screen.blit(self.door2, (192,64))
            #switch on right side
            elif (self.vertical_wall[y][increment(x,2)] == 12):
                screen.blit(self.center2, (192,64))                                                               
            #switch on left side
            elif (self.vertical_wall[y][increment(x,2)] == 13):
                screen.blit(self.switch2, (192,64)) 

            #draw straight one block wall right one
            if (self.vertical_wall[increment(y,1)][increment(x,2)] == 1):
                screen.blit(self.center2, (448, 64))
            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 2):
                screen.blit(self.door2, (448,64))
            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 3):
                screen.blit(self.door2, (448,64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 4):
                screen.blit(self.door2, (448,64))
            #one way door from right
            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 6):
                screen.blit(self.center2, (448,64))
            #one way door from left
            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 7):
                screen.blit(self.door2, (448,64))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 8):
                screen.blit(self.center2, (448,64))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 9):
                screen.blit(self.door2, (448,64))
            #switch on right side
            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 12):
                screen.blit(self.center2, (448,64))                                                               
            #switch on left side
            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 13):
                screen.blit(self.switch2, (448,64)) 


            #draw up one wall on left
            if (self.horizontal_wall[y][increment(x,1)] == 1):
                screen.blit(self.edgeList2[0], (64, -64))
            elif (self.horizontal_wall[y][increment(x,1)] == 2):
                screen.blit(self.doorList2[0], (64, -64))
            elif (self.horizontal_wall[y][increment(x,1)] == 3):
                screen.blit(self.doorList2[0], (64, -64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][increment(x,1)] == 4):
                screen.blit(self.doorList2[0], (64, -64))
            #one way door from right
            elif (self.horizontal_wall[y][increment(x,1)] == 6):
                screen.blit(self.doorList2[0], (64, -64))
            #one way door from left
            elif (self.horizontal_wall[y][increment(x,1)] == 7):
                screen.blit(self.edgeList2[0], (64, -64))
            #hidden one way door from right
            elif (self.horizontal_wall[y][increment(x,1)] == 8):
                screen.blit(self.doorList2[0], (64, -64))
            #hidden one way door from left
            elif (self.horizontal_wall[y][increment(x,1)] == 9):
                screen.blit(self.edgeList2[0], (64, -64))
            #switch on right side
            elif (self.horizontal_wall[y][increment(x,1)] == 12):
                screen.blit(self.switchedgeList2[0], (64, -64)) 
            #switch on left side
            elif (self.horizontal_wall[y][increment(x,1)] == 13):
                screen.blit(self.edgeList2[0], (64, -64)) 
                
            #draw up one wall on right
            if (self.horizontal_wall[increment(y,1)][increment(x,1)] == 1):
                screen.blit(self.edgeList2[1], (448, -64))                
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 2):
                screen.blit(self.doorList2[1], (448, -64))                
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 3):
                screen.blit(self.doorList2[1], (448, -64))                
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 4):
                screen.blit(self.doorList2[1],  (448, -64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 6):
                screen.blit(self.edgeList2[1],  (448, -64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 7):
                screen.blit(self.doorList2[1],  (448, -64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 8):
                screen.blit(self.edgeList2[1],  (448, -64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 9):
                screen.blit(self.doorList2[1],  (448, -64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 12):
                screen.blit(self.edgeList2[1],  (448, -64)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 13):
                screen.blit(self.switchedgeList2[1],  (448, -64)) 


            #draw left one up wall
            if (self.vertical_wall[decrement(y,1)][increment(x,1)] == 1):
                screen.blit(self.center1, (-448,-64))
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 2):
                screen.blit(self.door1, (-448,-64))
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 3):
                screen.blit(self.door1, (-448,-64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 4):
                screen.blit(self.door1, (-448,-64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 6):
                screen.blit(self.center1, (-448,-64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 7):
                screen.blit(self.door1, (-448,-64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 8):
                screen.blit(self.center1, (-448,-64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 9):
                screen.blit(self.door1, (-448,-64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 12):
                screen.blit(self.center1, (-448,-64))                                                               
            #switch on left side
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 13):
                screen.blit(self.switch1, (-448,-64)) 

            #draw right one up wall
            if (self.vertical_wall[increment(y,1)][increment(x,1)] == 1):
                screen.blit(self.center1, (576,-64))
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 2):
                screen.blit(self.door1, (576,-64))
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 3):
                screen.blit(self.door1, (576,-64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 4):
                screen.blit(self.door1, (576,-64))
            #one way door from right
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 6):
                screen.blit(self.center1, (576,-64))
            #one way door from left
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 7):
                screen.blit(self.door1, (576,-64))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 8):
                screen.blit(self.center1, (576,-64))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 9):
                screen.blit(self.door1, (576,-64))
            #switch on right side
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 12):
                screen.blit(self.center1, (576,-64))                                                               
            #switch on left side
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 13):
                screen.blit(self.switch1, (576,-64)) 


            #draw just up wall
            if (self.vertical_wall[y][increment(x,1)] == 1):
                screen.blit(self.center1, (64,-64))
            elif (self.vertical_wall[y][increment(x,1)] == 2):
                screen.blit(self.door1, (64,-64))
            elif (self.vertical_wall[y][increment(x,1)] == 3):
                screen.blit(self.door1, (64,-64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][increment(x,1)] == 4):
                screen.blit(self.door1, (64,-64))
            #one way door from right
            elif (self.vertical_wall[y][increment(x,1)] == 6):
                screen.blit(self.center1, (64,-64))
            #one way door from left
            elif (self.vertical_wall[y][increment(x,1)] == 7):
                screen.blit(self.door1, (64,-64))
            #hidden one way door from right
            elif (self.vertical_wall[y][increment(x,1)] == 8):
                screen.blit(self.center1, (64,-64))
            #hidden one way door from left
            elif (self.vertical_wall[y][increment(x,1)] == 9):
                screen.blit(self.door1, (64,-64))
            #switch on right side
            elif (self.vertical_wall[y][increment(x,1)] == 12):
                screen.blit(self.center1, (64,-64))                                                               
            #switch on left side
            elif (self.vertical_wall[y][increment(x,1)] == 13):
                screen.blit(self.switch1, (64,-64)) 

            #draw wall on left
            if (self.horizontal_wall[y][x] == 1):
                screen.blit(self.edgeList1[0], (-192, -320))
            elif (self.horizontal_wall[y][x] == 2):
                screen.blit(self.doorList1[0], (-192, -320))
            elif (self.horizontal_wall[y][x] == 3):
                screen.blit(self.doorList1[0], (-192, -320))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][x] == 4):
                screen.blit(self.doorList1[0], (-192, -320))
            #one way door from right
            elif (self.horizontal_wall[y][x] == 6):
                screen.blit(self.doorList1[0], (-192, -320))
            #one way door from left
            elif (self.horizontal_wall[y][x] == 7):
                screen.blit(self.edgeList1[0], (-192, -320))
            #hidden one way door from right
            elif (self.horizontal_wall[y][x] == 8):
                screen.blit(self.doorList1[0], (-192, -320))
            #hidden one way door from left
            elif (self.horizontal_wall[y][x] == 9):
                screen.blit(self.edgeList1[0], (-192, -320))
            #switch on right side
            elif (self.horizontal_wall[y][x] == 12):
                screen.blit(self.switchedgeList1[0], (-192, -320)) 
            #switch on left side
            elif (self.horizontal_wall[y][x] == 13):
                screen.blit(self.edgeList1[0], (-192, -320)) 

            #draw wall on right
            if (self.horizontal_wall[increment(y,1)][x] == 1):
                screen.blit(self.edgeList1[1], (576, -320))
            elif (self.horizontal_wall[increment(y,1)][x] == 2):
                screen.blit(self.doorList1[1], (576, -320))
            elif (self.horizontal_wall[increment(y,1)][x] == 3):
                screen.blit(self.doorList1[1], (576, -320))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,1)][x] == 4):
                screen.blit(self.doorList1[1],  (576, -320))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][x] == 6):
                screen.blit(self.edgeList1[1],  (576, -320))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][x] == 7):
                screen.blit(self.doorList1[1],  (576, -320))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][x] == 8):
                screen.blit(self.edgeList1[1],  (576, -320))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][x] == 9):
                screen.blit(self.doorList1[1],  (576, -320))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][x] == 12):
                screen.blit(self.edgeList1[1],  (576, -320)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][x] == 13):
                screen.blit(self.switchedgeList1[1],  (576, -320)) 


        #if party is looking down
        elif (game_self.party.direction == 2):

            #draw ground below
            draw_dungeon_ground( screen, self.ground[y][x], self.ground_center1, (32, 448))
            #draw ground left
            draw_dungeon_ground( screen, self.ground[y][increment(x,1)], self.ground_sideList1[0], (0, 448))
            #draw ground right
            draw_dungeon_ground( screen, self.ground[y][decrement(x,1)], self.ground_sideList1[1], (576, 448))
            #draw ground up left
            draw_dungeon_ground( screen, self.ground[increment(y,1)][increment(x,1)], self.ground_sideList2[0], (0,320))
            #draw ground up right
            draw_dungeon_ground( screen, self.ground[increment(y,1)][decrement(x,1)], self.ground_sideList2[1], (448,320))
            #draw ground up two left
            draw_dungeon_ground( screen, self.ground[increment(y,2)][increment(x,1)], self.ground_sideList3[0], (-128,256))
            #draw ground up two right
            draw_dungeon_ground( screen, self.ground[increment(y,2)][decrement(x,1)], self.ground_sideList3[1], (384,256))
            #draw ground up two left two
            draw_dungeon_ground( screen, self.ground[increment(y,2)][increment(x,2)], self.ground_sideList3_2[0], (0,256))
            #draw ground up two right two
            draw_dungeon_ground( screen, self.ground[increment(y,2)][decrement(x,2)], self.ground_sideList3_2[1], (576,256))
            #draw ground up three left
            draw_dungeon_ground( screen, self.ground[increment(y,3)][increment(x,1)], self.ground_sideList4[0], (128,224))
            #draw ground up three right
            draw_dungeon_ground( screen, self.ground[increment(y,3)][decrement(x,1)], self.ground_sideList4[1], (352,224))
            #draw ground up three left two
            draw_dungeon_ground( screen, self.ground[increment(y,3)][increment(x,2)], self.ground_sideList4_2[0], (0,224))
            #draw ground up three right two
            draw_dungeon_ground( screen, self.ground[increment(y,3)][decrement(x,2)], self.ground_sideList4_2[1], (416,224))                
            #draw ground up one
            draw_dungeon_ground( screen, self.ground[increment(y,1)][x], self.ground_center2, (64,320))
            #draw ground up two
            draw_dungeon_ground( screen, self.ground[increment(y,2)][x], self.ground_center3, (192,256))                
            #draw ground up three
            draw_dungeon_ground( screen, self.ground[increment(y,3)][x], self.ground_center4, (256,224))


            #draw straight three block wall left two
            if (self.horizontal_wall[increment(y,4)][increment(x,2)] == 1):
                screen.blit(self.center4, (160, 160))
            elif (self.horizontal_wall[increment(y,4)][increment(x,2)] == 2):
                screen.blit(self.door4, (160,160))                                               
            elif (self.horizontal_wall[increment(y,4)][increment(x,2)] == 3):
                screen.blit(self.door4, (160,160))
            #hidden door
            elif (self.horizontal_wall[increment(y,4)][increment(x,2)] == 4):
                screen.blit(self.door4, (160,160))
            #one way door from right
            elif (self.horizontal_wall[increment(y,4)][increment(x,2)] == 6):
                screen.blit(self.center4, (160,160))
            #one way door from left
            elif (self.horizontal_wall[increment(y,4)][increment(x,2)] == 7):
                screen.blit(self.door4, (160,160))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,4)][increment(x,2)] == 8):
                screen.blit(self.center4, (160,160))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,4)][increment(x,2)] == 9):
                screen.blit(self.door4, (160,160))
            #switch on right side
            elif (self.horizontal_wall[increment(y,4)][increment(x,2)] == 12):
                screen.blit(self.center4, (160,160))                                                               
            #switch on left side
            elif (self.horizontal_wall[increment(y,4)][increment(x,2)] == 13):
                screen.blit(self.switch4, (160,160))    

            #draw straight three block wall left one
            if (self.horizontal_wall[increment(y,4)][increment(x,1)] == 1):
                screen.blit(self.center4, (224, 160))
            elif (self.horizontal_wall[increment(y,4)][increment(x,1)] == 2):
                screen.blit(self.door4, (224,160))                                               
            elif (self.horizontal_wall[increment(y,4)][increment(x,1)] == 3):
                screen.blit(self.door4, (224,160))                                               
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,4)][increment(x,1)] == 4):
                screen.blit(self.door4, (224,160))
            #one way door from right
            elif (self.horizontal_wall[increment(y,4)][increment(x,1)] == 6):
                screen.blit(self.center4, (224,160))
            #one way door from left
            elif (self.horizontal_wall[increment(y,4)][increment(x,1)] == 7):
                screen.blit(self.door4, (224,160))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,4)][increment(x,1)] == 8):
                screen.blit(self.center4, (224,160))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,4)][increment(x,1)] == 9):
                screen.blit(self.door4, (224,160))
            #switch on right side
            elif (self.horizontal_wall[increment(y,4)][increment(x,1)] == 12):
                screen.blit(self.center4, (224,160))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,4)][increment(x,1)] == 13):
                screen.blit(self.switch4, (224,160)) 

            #draw straight three block wall
            if (self.horizontal_wall[increment(y,4)][x] == 1):
                screen.blit(self.center4, (288, 160))
            elif (self.horizontal_wall[increment(y,4)][x] == 2):
                screen.blit(self.door4, (288,160))
            elif (self.horizontal_wall[increment(y,4)][x] == 3):
                screen.blit(self.door4, (288,160))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,4)][x] == 4):
                screen.blit(self.door4, (288,160))
            #one way door from right
            elif (self.horizontal_wall[increment(y,4)][x] == 6):
                screen.blit(self.center4, (288,160))
            #one way door from left
            elif (self.horizontal_wall[increment(y,4)][x] == 7):
                screen.blit(self.door4, (288,160))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,4)][x] == 8):
                screen.blit(self.center4, (288,160))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,4)][x] == 9):
                screen.blit(self.door4, (288,160))
            #switch on right side
            elif (self.horizontal_wall[increment(y,4)][x] == 12):
                screen.blit(self.center4, (288,160))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,4)][x] == 13):
                screen.blit(self.switch4, (288,160)) 


            #draw straight three block wall right one
            if (self.horizontal_wall[increment(y,4)][decrement(x,1)] == 1):
                screen.blit(self.center4, (352, 160))
            elif (self.horizontal_wall[increment(y,4)][decrement(x,1)] == 2):
                screen.blit(self.door4, (352,160))                                               
            elif (self.horizontal_wall[increment(y,4)][decrement(x,1)] == 3):
                screen.blit(self.door4, (352,160))                                               
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,4)][decrement(x,1)] == 4):
                screen.blit(self.door4, (352,160))
            #one way door from right
            elif (self.horizontal_wall[increment(y,4)][decrement(x,1)] == 6):
                screen.blit(self.center4, (352,160))
            #one way door from left
            elif (self.horizontal_wall[increment(y,4)][decrement(x,1)] == 7):
                screen.blit(self.door4, (352,160))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,4)][decrement(x,1)] == 8):
                screen.blit(self.center4, (352,160))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,4)][decrement(x,1)] == 9):
                screen.blit(self.door4, (352,160))
            #switch on right side
            elif (self.horizontal_wall[increment(y,4)][decrement(x,1)] == 12):
                screen.blit(self.center4, (352,160))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,4)][decrement(x,1)] == 13):
                screen.blit(self.switch4, (352,160)) 

            #draw straight three block wall right two
            if (self.horizontal_wall[increment(y,4)][decrement(x,2)] == 1):
                screen.blit(self.center4, (416, 160))
            elif (self.horizontal_wall[increment(y,4)][decrement(x,2)] == 2):
                screen.blit(self.door4, (416,160))
            elif (self.horizontal_wall[increment(y,4)][decrement(x,2)] == 3):
                screen.blit(self.door4, (416,160))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,4)][decrement(x,2)] == 4):
                screen.blit(self.door4, (416,160))
            #one way door from right
            elif (self.horizontal_wall[increment(y,4)][decrement(x,2)] == 6):
                screen.blit(self.center4, (416,160))
            #one way door from left
            elif (self.horizontal_wall[increment(y,4)][decrement(x,2)] == 7):
                screen.blit(self.door4, (416,160))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,4)][decrement(x,2)] == 8):
                screen.blit(self.center4, (416,160))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,4)][decrement(x,2)] == 9):
                screen.blit(self.door4, (416,160))
            #switch on right side
            elif (self.horizontal_wall[increment(y,4)][decrement(x,2)] == 12):
                screen.blit(self.center4, (416,160))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,4)][decrement(x,2)] == 13):
                screen.blit(self.switch4, (416,160)) 

            #draw up three wall on left three
            if (self.vertical_wall[increment(y,3)][increment(x,3)] == 1):
                screen.blit(self.edgeList4_3[0], (0, 128))
            elif (self.vertical_wall[increment(y,3)][increment(x,3)] == 2):
                screen.blit(self.doorList4_3[0], (0, 128))
            elif (self.vertical_wall[increment(y,3)][increment(x,3)] == 3):
                screen.blit(self.doorList4_3[0], (0, 128))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,3)][increment(x,3)] == 4):
                screen.blit(self.doorList4_3[0], (0, 128))
            #one way door from right
            elif (self.vertical_wall[increment(y,3)][increment(x,3)] == 6):
                screen.blit(self.edgeList4_3[0], (0, 128))
            #one way door from left
            elif (self.vertical_wall[increment(y,3)][increment(x,3)] == 7):
                screen.blit(self.doorList4_3[0], (0, 128))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,3)][increment(x,3)] == 8):
                screen.blit(self.edgeList4_3[0], (0, 128))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,3)][increment(x,3)] == 9):
                screen.blit(self.doorList4_3[0], (0, 128))
            #switch on right side
            elif (self.vertical_wall[increment(y,3)][increment(x,3)] == 12):
                screen.blit(self.edgeList4_3[0], (0, 128)) 
            #switch on left side
            elif (self.vertical_wall[increment(y,3)][increment(x,3)] == 13):
                screen.blit(self.switchedgeList4_3[0], (0, 128)) 


            #draw up three wall on left two
            if (self.vertical_wall[increment(y,3)][increment(x,2)] == 1):
                screen.blit(self.edgeList4_2[0], (128, 128))
            elif (self.vertical_wall[increment(y,3)][increment(x,2)] == 2):
                screen.blit(self.doorList4_2[0], (128, 128))
            elif (self.vertical_wall[increment(y,3)][increment(x,2)] == 3):
                screen.blit(self.doorList4_2[0], (128, 128))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,3)][increment(x,2)] == 4):
                screen.blit(self.doorList4_2[0], (128, 128))
            #one way door from right
            elif (self.vertical_wall[increment(y,3)][increment(x,2)] == 6):
                screen.blit(self.edgeList4_2[0], (128, 128))
            #one way door from left
            elif (self.vertical_wall[increment(y,3)][increment(x,2)] == 7):
                screen.blit(self.doorList4_2[0], (128, 128))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,3)][increment(x,2)] == 8):
                screen.blit(self.edgeList4_2[0], (128, 128))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,3)][increment(x,2)] == 9):
                screen.blit(self.doorList4_2[0], (128, 128))
            #switch on right side
            elif (self.vertical_wall[increment(y,3)][increment(x,2)] == 12):
                screen.blit(self.edgeList4_2[0], (128, 128)) 
            #switch on left side
            elif (self.vertical_wall[increment(y,3)][increment(x,2)] == 13):
                screen.blit(self.switchedgeList4_2[0], (128, 128)) 

            #draw up three wall on left
            if (self.vertical_wall[increment(y,3)][increment(x,1)] == 1):
                screen.blit(self.edgeList4[0], (256, 128))
            elif (self.vertical_wall[increment(y,3)][increment(x,1)] == 2):
                screen.blit(self.doorList4[0], (256, 128))
            elif (self.vertical_wall[increment(y,3)][increment(x,1)] == 3):
                screen.blit(self.doorList4[0], (256, 128))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,3)][increment(x,1)] == 4):
                screen.blit(self.doorList4[0], (256, 128))
            #one way door from right
            elif (self.vertical_wall[increment(y,3)][increment(x,1)] == 6):
                screen.blit(self.edgeList4[0], (256, 128))
            #one way door from left
            elif (self.vertical_wall[increment(y,3)][increment(x,1)] == 7):
                screen.blit(self.doorList4[0], (256, 128))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,3)][increment(x,1)] == 8):
                screen.blit(self.edgeList4[0], (256, 128))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,3)][increment(x,1)] == 9):
                screen.blit(self.doorList4[0], (256, 128))
            #switch on right side
            elif (self.vertical_wall[increment(y,3)][increment(x,1)] == 12):
                screen.blit(self.edgeList4[0], (256, 128)) 
            #switch on left side
            elif (self.vertical_wall[increment(y,3)][increment(x,1)] == 13):
                screen.blit(self.switchedgeList4[0], (256, 128)) 


            #draw up three wall on right three
            if (self.vertical_wall[increment(y,3)][decrement(x,2)] == 1):
                screen.blit(self.edgeList4_3[1], (480, 128))                
            elif (self.vertical_wall[increment(y,3)][decrement(x,2)] == 2):
                screen.blit(self.doorList4_3[1], (480, 128))  
            elif (self.vertical_wall[increment(y,3)][decrement(x,2)] == 3):
                screen.blit(self.doorList4_3[1], (480, 128))  
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,3)][decrement(x,2)] == 4):
                screen.blit(self.doorList4_3[1], (480, 128))
            #one way door from right
            elif (self.vertical_wall[increment(y,3)][decrement(x,2)] == 6):
                screen.blit(self.doorList4_3[1], (480, 128))
            #one way door from left
            elif (self.vertical_wall[increment(y,3)][decrement(x,2)] == 7):
                screen.blit(self.edgeList4_3[1], (480, 128))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,3)][decrement(x,2)] == 8):
                screen.blit(self.doorList4_3[1], (480, 128))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,3)][decrement(x,2)] == 9):
                screen.blit(self.edgeList4_3[1], (480, 128))
            #switch on right side
            elif (self.vertical_wall[increment(y,3)][decrement(x,2)] == 12):
                screen.blit(self.switchedgeList4_3[1], (480, 128)) 
            #switch on left side
            elif (self.vertical_wall[increment(y,3)][decrement(x,2)] == 13):
                screen.blit(self.edgeList4_3[1], (480, 128)) 

            #draw up three wall on right two
            if (self.vertical_wall[increment(y,3)][decrement(x,1)] == 1):
                screen.blit(self.edgeList4_2[1], (416, 128))                
            elif (self.vertical_wall[increment(y,3)][decrement(x,1)] == 2):
                screen.blit(self.doorList4_2[1], (416, 128))                               
            elif (self.vertical_wall[increment(y,3)][decrement(x,1)] == 3):
                screen.blit(self.doorList4_2[1], (416, 128))                               
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,3)][decrement(x,1)] == 4):
                screen.blit(self.doorList4_2[1], (416, 128))
            #one way door from right
            elif (self.vertical_wall[increment(y,3)][decrement(x,1)] == 6):
                screen.blit(self.doorList4_2[1], (416, 128))
            #one way door from left
            elif (self.vertical_wall[increment(y,3)][decrement(x,1)] == 7):
                screen.blit(self.edgeList4_2[1], (416, 128))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,3)][decrement(x,1)] == 8):
                screen.blit(self.doorList4_2[1], (416, 128))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,3)][decrement(x,1)] == 9):
                screen.blit(self.edgeList4_2[1], (416, 128))
            #switch on right side
            elif (self.vertical_wall[increment(y,3)][decrement(x,1)] == 12):
                screen.blit(self.switchedgeList4_2[1], (416, 128)) 
            #switch on left side
            elif (self.vertical_wall[increment(y,3)][decrement(x,1)] == 13):
                screen.blit(self.edgeList4_2[1], (416, 128)) 

            #draw up three wall on right
            if (self.vertical_wall[increment(y,3)][x] == 1):
                screen.blit(self.edgeList4[1], (352, 128))                
            elif (self.vertical_wall[increment(y,3)][x] == 2):
                screen.blit(self.doorList4[1], (352, 128))                
            elif (self.vertical_wall[increment(y,3)][x] == 3):
                screen.blit(self.doorList4[1], (352, 128))                
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,3)][x] == 4):
                screen.blit(self.doorList4[1], (352, 128))
            #one way door from right
            elif (self.vertical_wall[increment(y,3)][x] == 6):
                screen.blit(self.doorList4[1], (352, 128))
            #one way door from left
            elif (self.vertical_wall[increment(y,3)][x] == 7):
                screen.blit(self.edgeList4[1], (352, 128))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,3)][x] == 8):
                screen.blit(self.doorList4[1], (352, 128))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,3)][x] == 9):
                screen.blit(self.edgeList4[1], (352, 128))
            #switch on right side
            elif (self.vertical_wall[increment(y,3)][x] == 12):
                screen.blit(self.switchedgeList4[1], (352, 128)) 
            #switch on left side
            elif (self.vertical_wall[increment(y,3)][x] == 13):
                screen.blit(self.edgeList4[1], (352, 128)) 


            #draw straight two block wall left one
            if (self.horizontal_wall[increment(y,3)][increment(x,2)] == 1):
                screen.blit(self.center3, (0, 128))
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 2):
                screen.blit(self.door3, (0,128))
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 3):
                screen.blit(self.door3, (0,128))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 4):
                screen.blit(self.door3, (0,128))
            #one way door from right
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 6):
                screen.blit(self.center3, (0,128))
            #one way door from left
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 7):
                screen.blit(self.door3, (0,128))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 8):
                screen.blit(self.center3, (0,128))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 9):
                screen.blit(self.door3, (0,128))
            #switch on right side
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 12):
                screen.blit(self.center3, (0,128))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,3)][increment(x,2)] == 13):
                screen.blit(self.switch3, (0,128))  

            #draw straight two block wall left one
            if (self.horizontal_wall[increment(y,3)][increment(x,1)] == 1):
                screen.blit(self.center3, (128, 128))
            elif (self.horizontal_wall[increment(y,3)][increment(x,1)] == 2):
                screen.blit(self.door3, (128,128))
            elif (self.horizontal_wall[increment(y,3)][increment(x,1)] == 3):
                screen.blit(self.door3, (128,128))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,3)][increment(x,1)] == 4):
                screen.blit(self.door3, (128,128))
            #one way door from right
            elif (self.horizontal_wall[increment(y,3)][increment(x,1)] == 6):
                screen.blit(self.center3, (128,128))
            #one way door from left
            elif (self.horizontal_wall[increment(y,3)][increment(x,1)] == 7):
                screen.blit(self.door3, (128,128))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,3)][increment(x,1)] == 8):
                screen.blit(self.center3, (128,128))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,3)][increment(x,1)] == 9):
                screen.blit(self.door3, (128,128))
            #switch on right side
            elif (self.horizontal_wall[increment(y,3)][increment(x,1)] == 12):
                screen.blit(self.center3, (128,128))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,3)][increment(x,1)] == 13):
                screen.blit(self.switch3, (128,128))  

            #draw straight two block wall
            if (self.horizontal_wall[increment(y,3)][x] == 1):
                screen.blit(self.center3, (256, 128))
            elif (self.horizontal_wall[increment(y,3)][x] == 2):
                screen.blit(self.door3, (256,128))
            elif (self.horizontal_wall[increment(y,3)][x] == 3):
                screen.blit(self.door3, (256,128))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,3)][x] == 4):
                screen.blit(self.door3, (256,128))
            #one way door from right
            elif (self.horizontal_wall[increment(y,3)][x] == 6):
                screen.blit(self.center3, (256,128))
            #one way door from left
            elif (self.horizontal_wall[increment(y,3)][x] == 7):
                screen.blit(self.door3, (256,128))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,3)][x] == 8):
                screen.blit(self.center3, (256,128))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,3)][x] == 9):
                screen.blit(self.door3, (256,128))
            #switch on right side
            elif (self.horizontal_wall[increment(y,3)][x] == 12):
                screen.blit(self.center3, (256,128))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,3)][x] == 13):
                screen.blit(self.switch3, (256,128))
                

            #draw straight two block wall right one
            if (self.horizontal_wall[increment(y,3)][decrement(x,1)] == 1):
                screen.blit(self.center3, (384, 128))
            elif (self.horizontal_wall[increment(y,3)][decrement(x,1)] == 2):
                screen.blit(self.door3, (384,128))
            elif (self.horizontal_wall[increment(y,3)][decrement(x,1)] == 3):
                screen.blit(self.door3, (384,128))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,3)][decrement(x,1)] == 4):
                screen.blit(self.door3, (384,128))
            #one way door from right
            elif (self.horizontal_wall[increment(y,3)][decrement(x,1)] == 6):
                screen.blit(self.center3, (384,128))
            #one way door from left
            elif (self.horizontal_wall[increment(y,3)][decrement(x,1)] == 7):
                screen.blit(self.door3, (384,128))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,3)][decrement(x,1)] == 8):
                screen.blit(self.center3, (384,128))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,3)][decrement(x,1)] == 9):
                screen.blit(self.door3, (384,128))
            #switch on right side
            elif (self.horizontal_wall[increment(y,3)][decrement(x,1)] == 12):
                screen.blit(self.center3, (384,128))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,3)][decrement(x,1)] == 13):
                screen.blit(self.switch3, (384,128))

            #draw straight two block wall right two
            if (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 1):
                screen.blit(self.center3, (512, 128))
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 2):
                screen.blit(self.door3, (512,128))
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 3):
                screen.blit(self.door3, (512,128))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 4):
                screen.blit(self.door3, (512,128))
            #one way door from right
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 6):
                screen.blit(self.center3, (512,128))
            #one way door from left
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 7):
                screen.blit(self.door3, (512,128))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 8):
                screen.blit(self.center3, (512,128))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 9):
                screen.blit(self.door3, (512,128))
            #switch on right side
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 12):
                screen.blit(self.center3, (512,128))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 13):
                screen.blit(self.switch3, (512,128))

            #draw up two wall on left three
            if (self.vertical_wall[increment(y,2)][increment(x,3)] == 1):
                screen.blit(self.edgeList3_3[0], (-320, 64))
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 2):
                screen.blit(self.doorList3_3[0], (-320, 64))
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 3):
                screen.blit(self.doorList3_3[0], (-320, 64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 4):
                screen.blit(self.doorList3_3[0], (-320, 64))
            #one way door from right
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 6):
                screen.blit(self.edgeList3_3[0], (-320, 64))
            #one way door from left
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 7):
                screen.blit(self.doorList3_3[0], (-320, 64))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 8):
                screen.blit(self.edgeList3_3[0], (-320, 64))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 9):
                screen.blit(self.doorList3_3[0], (-320, 64))
            #switch on right side
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 12):
                screen.blit(self.edgeList3_3[0], (-320, 64)) 
            #switch on left side
            elif (self.vertical_wall[increment(y,2)][increment(x,3)] == 13):
                screen.blit(self.switchedgeList3_3[0], (-320, 64)) 


            #draw up two wall on left two
            if (self.vertical_wall[increment(y,2)][increment(x,2)] == 1):
                screen.blit(self.edgeList3_2[0], (-64, 64))
            elif (self.vertical_wall[increment(y,2)][increment(x,2)] == 2):
                screen.blit(self.doorList3_2[0], (-64, 64))
            elif (self.vertical_wall[increment(y,2)][increment(x,2)] == 3):
                screen.blit(self.doorList3_2[0], (-64, 64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,2)][increment(x,2)] == 4):
                screen.blit(self.doorList3_2[0], (-64, 64))
            #one way door from right
            elif (self.vertical_wall[increment(y,2)][increment(x,2)] == 6):
                screen.blit(self.edgeList3_2[0], (-64, 64))
            #one way door from left
            elif (self.vertical_wall[increment(y,2)][increment(x,2)] == 7):
                screen.blit(self.doorList3_2[0], (-64, 64))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,2)][increment(x,2)] == 8):
                screen.blit(self.edgeList3_2[0], (-64, 64))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,2)][increment(x,2)] == 9):
                screen.blit(self.doorList3_2[0], (-64, 64))
            #switch on right side
            elif (self.vertical_wall[increment(y,2)][increment(x,2)] == 12):
                screen.blit(self.edgeList3_2[0], (-64, 64)) 
            #switch on left side
            elif (self.vertical_wall[increment(y,2)][increment(x,2)] == 13):
                screen.blit(self.switchedgeList3_2[0], (-64, 64)) 

            #draw up two wall on left
            if (self.vertical_wall[increment(y,2)][increment(x,1)] == 1):
                screen.blit(self.edgeList3[0], (192, 64))
            elif (self.vertical_wall[increment(y,2)][increment(x,1)] == 2):
                screen.blit(self.doorList3[0], (192, 64))
            elif (self.vertical_wall[increment(y,2)][increment(x,1)] == 3):
                screen.blit(self.doorList3[0], (192, 64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,2)][increment(x,1)] == 4):
                screen.blit(self.doorList3[0], (-64, 64))
            #one way door from right
            elif (self.vertical_wall[increment(y,2)][increment(x,1)] == 6):
                screen.blit(self.edgeList3[0], (-64, 64))
            #one way door from left
            elif (self.vertical_wall[increment(y,2)][increment(x,1)] == 7):
                screen.blit(self.doorList3[0], (-64, 64))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,2)][increment(x,1)] == 8):
                screen.blit(self.edgeList3[0], (-64, 64))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,2)][increment(x,1)] == 9):
                screen.blit(self.doorList3[0], (-64, 64))
            #switch on right side
            elif (self.vertical_wall[increment(y,2)][increment(x,1)] == 12):
                screen.blit(self.edgeList3[0], (-64, 64)) 
            #switch on left side
            elif (self.vertical_wall[increment(y,2)][increment(x,1)] == 13):
                screen.blit(self.switchedgeList3[0], (-64, 64)) 
                
            #draw up two wall on right three
            if (self.vertical_wall[increment(y,2)][decrement(x,2)] == 1):
                screen.blit(self.edgeList3_3[1], (640, 64))                
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 2):
                screen.blit(self.doorList3_3[1], (640, 64))    
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 3):
                screen.blit(self.doorList3_3[1], (640, 64))    
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 4):
                screen.blit(self.doorList3_3[1], (640, 64))
            #one way door from right
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 6):
                screen.blit(self.doorList3_3[1], (640, 64))
            #one way door from left
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 7):
                screen.blit(self.edgeList3_3[1], (640, 64))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 8):
                screen.blit(self.doorList3_3[1], (640, 64))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 9):
                screen.blit(self.edgeList3_3[1], (640, 64))
            #switch on right side
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 12):
                screen.blit(self.switchedgeList3_3[1], (640, 64)) 
            #switch on left side
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 13):
                screen.blit(self.edgeList3_3[1], (640, 64)) 


            #draw up two wall on right two
            if (self.vertical_wall[increment(y,2)][decrement(x,1)] == 1):
                screen.blit(self.edgeList3_2[1], (512, 64))                
            elif (self.vertical_wall[increment(y,2)][decrement(x,1)] == 2):
                screen.blit(self.doorList3_2[1], (512, 64))    
            elif (self.vertical_wall[increment(y,2)][decrement(x,1)] == 3):
                screen.blit(self.doorList3_2[1], (512, 64))    
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,2)][decrement(x,1)] == 4):
                screen.blit(self.doorList3_2[1], (512, 64))
            #one way door from right
            elif (self.vertical_wall[increment(y,2)][decrement(x,1)] == 6):
                screen.blit(self.doorList3_2[1], (512, 64))
            #one way door from left
            elif (self.vertical_wall[increment(y,2)][decrement(x,1)] == 7):
                screen.blit(self.edgeList3_2[1], (512, 64))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,2)][decrement(x,1)] == 8):
                screen.blit(self.doorList3_2[1], (512, 64))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,2)][decrement(x,1)] == 9):
                screen.blit(self.edgeList3_2[1], (512, 64))
            #switch on right side
            elif (self.vertical_wall[increment(y,2)][decrement(x,1)] == 12):
                screen.blit(self.switchedgeList3_2[1], (512, 64)) 
            #switch on left side
            elif (self.vertical_wall[increment(y,2)][decrement(x,1)] == 13):
                screen.blit(self.edgeList3_2[1], (512, 64)) 

            #draw up two wall on right
            if (self.vertical_wall[increment(y,2)][x] == 1):
                screen.blit(self.edgeList3[1], (384, 64))                
            elif (self.vertical_wall[increment(y,2)][x] == 2):
                screen.blit(self.doorList3[1], (384, 64))  
            elif (self.vertical_wall[increment(y,2)][x] == 3):
                screen.blit(self.doorList3[1], (384, 64))  
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,2)][x] == 4):
                screen.blit(self.doorList3[1], (384, 64))
            #one way door from right
            elif (self.vertical_wall[increment(y,2)][x] == 6):
                screen.blit(self.doorList3[1], (384, 64))
            #one way door from left
            elif (self.vertical_wall[increment(y,2)][x] == 7):
                screen.blit(self.edgeList3[1], (384, 64))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,2)][x] == 8):
                screen.blit(self.doorList3[1], (384, 64))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,2)][x] == 9):
                screen.blit(self.edgeList3[1], (384, 64))
            #switch on right side
            elif (self.vertical_wall[increment(y,2)][x] == 12):
                screen.blit(self.switchedgeList3[1], (384, 64)) 
            #switch on left side
            elif (self.vertical_wall[increment(y,2)][x] == 13):
                screen.blit(self.edgeList3[1], (384, 64)) 

            #draw straight one block wall left one
            if (self.horizontal_wall[increment(y,2)][increment(x,1)] == 1):
                screen.blit(self.center2, (-64, 64))
            elif (self.horizontal_wall[increment(y,2)][increment(x,1)] == 2):
                screen.blit(self.door2, (-64,64))
            elif (self.horizontal_wall[increment(y,2)][increment(x,1)] == 3):
                screen.blit(self.door2, (-64,64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,2)][increment(x,1)] == 4):
                screen.blit(self.door2, (-64,64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,2)][increment(x,1)] == 6):
                screen.blit(self.center2, (-64,64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,2)][increment(x,1)] == 7):
                screen.blit(self.door2, (-64,64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,2)][increment(x,1)] == 8):
                screen.blit(self.center2, (-64,64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,2)][increment(x,1)] == 9):
                screen.blit(self.door2, (-64,64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,2)][increment(x,1)] == 12):
                screen.blit(self.center2, (-64,64))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,2)][increment(x,1)] == 13):
                screen.blit(self.switch2, (-64,64))
        
            #draw straight one block wall
            if (self.horizontal_wall[increment(y,2)][x] == 1):
                screen.blit(self.center2, (192, 64))
            elif (self.horizontal_wall[increment(y,2)][x] == 2):
                screen.blit(self.door2, (192, 64))
            elif (self.horizontal_wall[increment(y,2)][x] == 3):
                screen.blit(self.door2, (192, 64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,2)][x] == 4):
                screen.blit(self.door2, (192,64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,2)][x] == 6):
                screen.blit(self.center2, (192,64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,2)][x] == 7):
                screen.blit(self.door2, (192,64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,2)][x] == 8):
                screen.blit(self.center2, (192,64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,2)][x] == 9):
                screen.blit(self.door2, (192,64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,2)][x] == 12):
                screen.blit(self.center2, (192,64))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,2)][x] == 13):
                screen.blit(self.switch2, (192,64))

            #draw straight one block wall right one
            if (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 1):
                screen.blit(self.center2, (448, 64))
            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 2):
                screen.blit(self.door2, (448,64))
            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 3):
                screen.blit(self.door2, (448,64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 4):
                screen.blit(self.door2, (448,64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 6):
                screen.blit(self.center2, (448,64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 7):
                screen.blit(self.door2, (448,64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 8):
                screen.blit(self.center2, (448,64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 9):
                screen.blit(self.door2, (448,64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 12):
                screen.blit(self.center2, (448,64))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 13):
                screen.blit(self.switch2, (448,64))

            #draw up one wall on left
            if (self.vertical_wall[increment(y,1)][increment(x,1)] == 1):
                screen.blit(self.edgeList2[0], (64, -64))
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 2):
                screen.blit(self.doorList2[0], (64, -64))
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 3):
                screen.blit(self.doorList2[0], (64, -64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 4):
                screen.blit(self.doorList2[0], (64, -64))
            #one way door from right
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 6):
                screen.blit(self.edgeList2[0], (64, -64))
            #one way door from left
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 7):
                screen.blit(self.doorList2[0], (64, -64))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 8):
                screen.blit(self.edgeList2[0], (64, -64))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 9):
                screen.blit(self.doorList2[0], (64, -64))
            #switch on right side
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 12):
                screen.blit(self.edgeList2[0], (64, -64)) 
            #switch on left side
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 13):
                screen.blit(self.switchedgeList2[0], (64, -64)) 
                
            #draw up one wall on right
            if (self.vertical_wall[increment(y,1)][x] == 1):
                screen.blit(self.edgeList2[1], (448, -64))                
            elif (self.vertical_wall[increment(y,1)][x] == 2):
                screen.blit(self.doorList2[1], (448, -64))                
            elif (self.vertical_wall[increment(y,1)][x] == 3):
                screen.blit(self.doorList2[1], (448, -64))                
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,1)][x] == 4):
                screen.blit(self.doorList2[1], (448, -64))
            #one way door from right
            elif (self.vertical_wall[increment(y,1)][x] == 6):
                screen.blit(self.doorList2[1], (448, -64))
            #one way door from left
            elif (self.vertical_wall[increment(y,1)][x] == 7):
                screen.blit(self.edgeList2[1], (448, -64))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,1)][x] == 8):
                screen.blit(self.doorList2[1], (448, -64))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,1)][x] == 9):
                screen.blit(self.edgeList2[1], (448, -64))
            #switch on right side
            elif (self.vertical_wall[increment(y,1)][x] == 12):
                screen.blit(self.switchedgeList2[1], (448, -64)) 
            #switch on left side
            elif (self.vertical_wall[increment(y,1)][x] == 13):
                screen.blit(self.edgeList2[1], (448, -64)) 

            #draw left one up wall
            if (self.horizontal_wall[increment(y,1)][increment(x,1)] == 1):
                screen.blit(self.center1, (-448,-64))
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 2):
                screen.blit(self.door1, (-448,-64))
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 3):
                screen.blit(self.door1, (-448,-64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 4):
                screen.blit(self.door1, (-448,-64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 6):
                screen.blit(self.center1, (-448,-64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 7):
                screen.blit(self.door1, (-448,-64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 8):
                screen.blit(self.center1, (-448,-64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 9):
                screen.blit(self.door1, (-448,-64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 12):
                screen.blit(self.center1, (-448,-64))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 13):
                screen.blit(self.switch1, (-448,-64))


            #draw right one up wall
            if (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 1):
                screen.blit(self.center1, (576,-64))
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 2):
                screen.blit(self.door1, (576,-64))
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 3):
                screen.blit(self.door1, (576,-64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 4):
                screen.blit(self.door1, (576,-64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 6):
                screen.blit(self.center1, (576,-64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 7):
                screen.blit(self.door1, (576,-64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 8):
                screen.blit(self.center1, (576,-64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 9):
                screen.blit(self.door1, (576,-64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 12):
                screen.blit(self.center,(576,-64))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 13):
                screen.blit(self.switch1, (576,-64))

            #draw just up wall
            if (self.horizontal_wall[increment(y,1)][x] == 1):
                screen.blit(self.center1, (64,-64))
            elif (self.horizontal_wall[increment(y,1)][x] == 2):
                screen.blit(self.door1, (64,-64))
            elif (self.horizontal_wall[increment(y,1)][x] == 3):
                screen.blit(self.door1, (64,-64))
            elif (self.horizontal_wall[increment(y,1)][x] == 4):
                screen.blit(self.door1, (64,-64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][x] == 6):
                screen.blit(self.center1, (64,-64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][x] == 7):
                screen.blit(self.door1, (64,-64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][x] == 8):
                screen.blit(self.center1, (64,-64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][x] == 9):
                screen.blit(self.door1, (64,-64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][x] == 12):
                screen.blit(self.center1,(64,-64))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][x] == 13):
                screen.blit(self.switch1, (64,-64))
                
            #draw wall on left
            if (self.vertical_wall[y][increment(x,1)] == 1):
                screen.blit(self.edgeList1[0], (-192, -320))
            elif (self.vertical_wall[y][increment(x,1)] == 2):
                screen.blit(self.doorList1[0], (-192, -320))
            elif (self.vertical_wall[y][increment(x,1)] == 3):
                screen.blit(self.doorList1[0], (-192, -320))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][increment(x,1)] == 4):
                screen.blit(self.doorList1[0], (-192, -320))
            #one way door from right
            elif (self.vertical_wall[y][increment(x,1)] == 6):
                screen.blit(self.edgeList1[0], (-192, -320))
            #one way door from left
            elif (self.vertical_wall[y][increment(x,1)] == 7):
                screen.blit(self.doorList1[0], (-192, -320))
            #hidden one way door from right
            elif (self.vertical_wall[y][increment(x,1)] == 8):
                screen.blit(self.edgeList1[0], (-192, -320))
            #hidden one way door from left
            elif (self.vertical_wall[y][increment(x,1)] == 9):
                screen.blit(self.doorList1[0], (-192, -320))
            #switch on right side
            elif (self.vertical_wall[y][increment(x,1)] == 12):
                screen.blit(self.edgeList1[0], (-192, -320)) 
            #switch on left side
            elif (self.vertical_wall[y][increment(x,1)] == 13):
                screen.blit(self.switchedgeList1[0], (-192, -320))
                
            #draw wall on right
            if (self.vertical_wall[y][x] == 1):
                screen.blit(self.edgeList1[1], (576, -320))
            elif (self.vertical_wall[y][x] == 2):
                screen.blit(self.doorList1[1], (576, -320))
            elif (self.vertical_wall[y][x] == 3):
                screen.blit(self.doorList1[1], (576, -320))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][x] == 4):
                screen.blit(self.doorList1[1], (576, -320))
            #one way door from right
            elif (self.vertical_wall[y][x] == 6):
                screen.blit(self.doorList1[1], (576, -320))
            #one way door from left
            elif (self.vertical_wall[y][x] == 7):
                screen.blit(self.edgeList1[1], (576, -320))
            #hidden one way door from right
            elif (self.vertical_wall[y][x] == 8):
                screen.blit(self.doorList1[1], (576, -320))
            #hidden one way door from left
            elif (self.vertical_wall[y][x] == 9):
                screen.blit(self.edgeList1[1], (576, -320))
            #switch on right side
            elif (self.vertical_wall[y][x] == 12):
                screen.blit(self.switchedgeList1[1], (576, -320)) 
            #switch on left side
            elif (self.vertical_wall[y][x] == 13):
                screen.blit(self.edgeList1[1], (576, -320)) 


        #if the player is looking left
        elif (game_self.party.direction == 3):

            #draw ground below
            draw_dungeon_ground( screen, self.ground[y][x], self.ground_center1, (32, 448))
            #draw ground left
            draw_dungeon_ground( screen, self.ground[increment(y,1)][x], self.ground_sideList1[0], (0, 448))
            #draw ground right
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][x], self.ground_sideList1[1], (576, 448))
            #draw ground up left
            draw_dungeon_ground( screen, self.ground[increment(y,1)][decrement(x,1)], self.ground_sideList2[0], (0,320))
            #draw ground up right
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][decrement(x,1)], self.ground_sideList2[1], (448,320))
            #draw ground up two left
            draw_dungeon_ground( screen, self.ground[increment(y,1)][decrement(x,2)], self.ground_sideList3[0], (-128,256))
            #draw ground up two right
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][decrement(x,2)], self.ground_sideList3[1], (384,256))
            #draw ground up two left two
            draw_dungeon_ground( screen, self.ground[increment(y,2)][decrement(x,2)], self.ground_sideList3_2[0], (0,256))
            #draw ground up two right two
            draw_dungeon_ground( screen, self.ground[decrement(y,2)][decrement(x,2)], self.ground_sideList3_2[1], (576,256))
            #draw ground up three left
            draw_dungeon_ground( screen, self.ground[increment(y,1)][decrement(x,3)], self.ground_sideList4[0], (128,224))
            #draw ground up three right
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][decrement(x,3)], self.ground_sideList4[1], (352,224))
            #draw ground up three left two
            draw_dungeon_ground( screen, self.ground[increment(y,2)][decrement(x,3)], self.ground_sideList4_2[0], (0,224))
            #draw ground up three right two
            draw_dungeon_ground( screen, self.ground[decrement(y,2)][decrement(x,3)], self.ground_sideList4_2[1], (416,224))                
            #draw ground up one
            draw_dungeon_ground( screen, self.ground[y][decrement(x,1)], self.ground_center2, (64,320))
            #draw ground up two
            draw_dungeon_ground( screen, self.ground[y][decrement(x,2)], self.ground_center3, (192,256))                
            #draw ground up three
            draw_dungeon_ground( screen, self.ground[y][decrement(x,3)], self.ground_center4, (256,224))
                                            
                                
            #draw straight three block wall left two
            if (self.vertical_wall[increment(y,2)][decrement(x,3)] == 1):
                screen.blit(self.center4, (160, 160))
            elif (self.vertical_wall[increment(y,2)][decrement(x,3)] == 2):
                screen.blit(self.door4, (160,160))                                               
            elif (self.vertical_wall[increment(y,2)][decrement(x,3)] == 3):
                screen.blit(self.door4, (160,160))                                               
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,2)][decrement(x,3)] == 4):
                screen.blit(self.door4, (160,160))
            #one way door from right
            elif (self.vertical_wall[increment(y,2)][decrement(x,3)] == 6):
                screen.blit(self.door4, (160,160))
            #one way door from left
            elif (self.vertical_wall[increment(y,2)][decrement(x,3)] == 7):
                screen.blit(self.center4, (160,160))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,2)][decrement(x,3)] == 8):
                screen.blit(self.door4, (160,160))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,2)][decrement(x,3)] == 9):
                screen.blit(self.center4, (160,160))
            #switch on right side
            elif (self.vertical_wall[increment(y,2)][decrement(x,3)] == 12):
                screen.blit(self.switch4, (160,160))                                                               
            #switch on left side
            elif (self.vertical_wall[increment(y,2)][decrement(x,3)] == 13):
                screen.blit(self.center4, (160,160))   

            #draw straight three block wall left one
            if (self.vertical_wall[increment(y,1)][decrement(x,3)] == 1):
                screen.blit(self.center4, (224, 160))
            elif (self.vertical_wall[increment(y,1)][decrement(x,3)] == 2):
                screen.blit(self.door4, (224,160))                                               
            elif (self.vertical_wall[increment(y,1)][decrement(x,3)] == 3):
                screen.blit(self.door4, (224,160))                                               
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,1)][decrement(x,3)] == 4):
                screen.blit(self.door4, (224,160))
            #one way door from right
            elif (self.vertical_wall[increment(y,1)][decrement(x,3)] == 6):
                screen.blit(self.door4, (224,160))
            #one way door from left
            elif (self.vertical_wall[increment(y,1)][decrement(x,3)] == 7):
                screen.blit(self.center4, (224,160))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,1)][decrement(x,3)] == 8):
                screen.blit(self.door4, (224,160))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,1)][decrement(x,3)] == 9):
                screen.blit(self.center4, (224,160))
            #switch on right side
            elif (self.vertical_wall[increment(y,1)][decrement(x,3)] == 12):
                screen.blit(self.switch4, (224,160))                                                               
            #switch on left side
            elif (self.vertical_wall[increment(y,1)][decrement(x,3)] == 13):
                screen.blit(self.center4, (224,160))  

            #draw straight three block wall
            if (self.vertical_wall[y][decrement(x,3)] == 1):
                screen.blit(self.center4, (288, 160))
            elif (self.vertical_wall[y][decrement(x,3)] == 2):
                screen.blit(self.door4, (288,160))
            elif (self.vertical_wall[y][decrement(x,3)] == 3):
                screen.blit(self.door4, (288,160))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][decrement(x,3)] == 4):
                screen.blit(self.door4, (288,160))
            #one way door from right
            elif (self.vertical_wall[y][decrement(x,3)] == 6):
                screen.blit(self.door4, (288,160))
            #one way door from left
            elif (self.vertical_wall[y][decrement(x,3)] == 7):
                screen.blit(self.center4, (288,160))
            #hidden one way door from right
            elif (self.vertical_wall[y][decrement(x,3)] == 8):
                screen.blit(self.door4, (288,160))
            #hidden one way door from left
            elif (self.vertical_wall[y][decrement(x,3)] == 9):
                screen.blit(self.center4, (288,160))
            #switch on right side
            elif (self.vertical_wall[y][decrement(x,3)] == 12):
                screen.blit(self.switch4, (288,160))                                                               
            #switch on left side
            elif (self.vertical_wall[y][decrement(x,3)] == 13):
                screen.blit(self.center4, (288,160))   

            #draw straight three block wall right one
            if (self.vertical_wall[decrement(y,1)][decrement(x,3)] == 1):
                screen.blit(self.center4, (352, 160))
            elif (self.vertical_wall[decrement(y,1)][decrement(x,3)] == 2):
                screen.blit(self.door4, (352,160))                                               
            elif (self.vertical_wall[decrement(y,1)][decrement(x,3)] == 3):
                screen.blit(self.door4, (352,160))                                               
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,1)][decrement(x,3)] == 4):
                screen.blit(self.door4, (352,160))
            #one way door from right
            elif (self.vertical_wall[decrement(y,1)][decrement(x,3)] == 6):
                screen.blit(self.door4, (352,160))
            #one way door from left
            elif (self.vertical_wall[decrement(y,1)][decrement(x,3)] == 7):
                screen.blit(self.center4, (352,160))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,1)][decrement(x,3)] == 8):
                screen.blit(self.door4, (352,160))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,1)][decrement(x,3)] == 9):
                screen.blit(self.center4, (352,160))
            #switch on right side
            elif (self.vertical_wall[decrement(y,1)][decrement(x,3)] == 12):
                screen.blit(self.switch4, (352,160))                                                               
            #switch on left side
            elif (self.vertical_wall[decrement(y,1)][decrement(x,3)] == 13):
                screen.blit(self.center4, (352,160)) 

            #draw straight three block wall right two
            if (self.vertical_wall[decrement(y,2)][decrement(x,3)] == 1):
                screen.blit(self.center4, (416, 160))
            elif (self.vertical_wall[decrement(y,2)][decrement(x,3)] == 2):
                screen.blit(self.door4, (416,160))
            elif (self.vertical_wall[decrement(y,2)][decrement(x,3)] == 3):
                screen.blit(self.door4, (416,160))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,2)][decrement(x,3)] == 4):
                screen.blit(self.door4, (416,160))
            #one way door from right
            elif (self.vertical_wall[decrement(y,2)][decrement(x,3)] == 6):
                screen.blit(self.door4, (416,160))
            #one way door from left
            elif (self.vertical_wall[decrement(y,2)][decrement(x,3)] == 7):
                screen.blit(self.center4, (416,160))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,2)][decrement(x,3)] == 8):
                screen.blit(self.door4, (416,160))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,2)][decrement(x,3)] == 9):
                screen.blit(self.center4, (416,160))
            #switch on right side
            elif (self.vertical_wall[decrement(y,2)][decrement(x,3)] == 12):
                screen.blit(self.switch4, (416,160))                                                               
            #switch on left side
            elif (self.vertical_wall[decrement(y,2)][decrement(x,3)] == 13):
                screen.blit(self.center4, (416,160)) 

            #draw up three wall on left three
            if (self.horizontal_wall[increment(y,3)][decrement(x,3)] == 1):
                screen.blit(self.edgeList4_3[0], (0, 128))
            elif (self.horizontal_wall[increment(y,3)][decrement(x,3)] == 2):
                screen.blit(self.doorList4_3[0], (0, 128))
            elif (self.horizontal_wall[increment(y,3)][decrement(x,3)] == 3):
                screen.blit(self.doorList4_3[0], (0, 128))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,3)][decrement(x,3)] == 4):
                screen.blit(self.doorList4_3[0], (0, 128))
            #one way door from right
            elif (self.horizontal_wall[increment(y,3)][decrement(x,3)] == 6):
                screen.blit(self.edgeList4_3[0], (0, 128))
            #one way door from left
            elif (self.horizontal_wall[increment(y,3)][decrement(x,3)] == 7):
                screen.blit(self.doorList4_3[0], (0, 128))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,3)][decrement(x,3)] == 8):
                screen.blit(self.edgeList4_3[0], (0, 128))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,3)][decrement(x,3)] == 9):
                screen.blit(self.doorList4_3[0], (0, 128))
            #switch on right side
            elif (self.horizontal_wall[increment(y,3)][decrement(x,3)] == 12):
                screen.blit(self.edgeList4_3[0], (0, 128)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,3)][decrement(x,3)] == 13):
                screen.blit(self.switchedgeList4_3[0], (0, 128)) 

            #draw up three wall on left two
            if (self.horizontal_wall[increment(y,2)][decrement(x,3)] == 1):
                screen.blit(self.edgeList4_2[0], (128, 128))
            elif (self.horizontal_wall[increment(y,2)][decrement(x,3)] == 2):
                screen.blit(self.doorList4_2[0], (128, 128))
            elif (self.horizontal_wall[increment(y,2)][decrement(x,3)] == 3):
                screen.blit(self.doorList4_2[0], (128, 128))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,2)][decrement(x,3)] == 4):
                screen.blit(self.doorList4_2[0], (128, 128))
            #one way door from right
            elif (self.horizontal_wall[increment(y,2)][decrement(x,3)] == 6):
                screen.blit(self.edgeList4_2[0], (128, 128))
            #one way door from left
            elif (self.horizontal_wall[increment(y,2)][decrement(x,3)] == 7):
                screen.blit(self.doorList4_2[0], (128, 128))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,2)][decrement(x,3)] == 8):
                screen.blit(self.edgeList4_2[0], (128, 128))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,2)][decrement(x,3)] == 9):
                screen.blit(self.doorList4_2[0], (128, 128))
            #switch on right side
            elif (self.horizontal_wall[increment(y,2)][decrement(x,3)] == 12):
                screen.blit(self.edgeList4_2[0], (128, 128)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,2)][decrement(x,3)] == 13):
                screen.blit(self.switchedgeList4_2[0], (128, 128)) 

            #draw up three wall on left
            if (self.horizontal_wall[increment(y,1)][decrement(x,3)] == 1):
                screen.blit(self.edgeList4[0], (256, 128))
            elif (self.horizontal_wall[increment(y,1)][decrement(x,3)] == 2):
                screen.blit(self.doorList4[0], (256, 128))
            elif (self.horizontal_wall[increment(y,1)][decrement(x,3)] == 3):
                screen.blit(self.doorList4[0], (256, 128))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,1)][decrement(x,3)] == 4):
                screen.blit(self.doorList4[0], (256, 128))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][decrement(x,3)] == 6):
                screen.blit(self.edgeList4[0], (256, 128))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][decrement(x,3)] == 7):
                screen.blit(self.doorList4[0], (256, 128))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][decrement(x,3)] == 8):
                screen.blit(self.edgeList4[0], (256, 128))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][decrement(x,3)] == 9):
                screen.blit(self.doorList4[0], (256, 128))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][decrement(x,3)] == 12):
                screen.blit(self.edgeList4[0], (256, 128)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][decrement(x,3)] == 13):
                screen.blit(self.switchedgeList4[0], (256, 128)) 

            #draw up three wall on right three
            if (self.horizontal_wall[decrement(y,2)][decrement(x,3)] == 1):
                screen.blit(self.edgeList4_3[1], (480, 128))                
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,3)] == 2):
                screen.blit(self.doorList4_3[1], (480, 128))  
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,3)] == 3):
                screen.blit(self.doorList4_3[1], (480, 128))  
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,3)] == 4):
                screen.blit(self.doorList4_3[1], (480, 128))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,3)] == 6):
                screen.blit(self.doorList4_3[1], (480, 128))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,3)] == 7):
                screen.blit(self.edgeList4_3[1], (480, 128))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,3)] == 8):
                screen.blit(self.doorList4_3[1], (480, 128))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,3)] == 9):
                screen.blit(self.edgeList4_3[1], (480, 128))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,3)] == 12):
                screen.blit(self.switchedgeList4_3[1], (480, 128)) 
            #switch on left side
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,3)] == 13):
                screen.blit(self.edgeList4_3[1], (480, 128)) 


            #draw up three wall on right two
            if (self.horizontal_wall[decrement(y,1)][decrement(x,3)] == 1):
                screen.blit(self.edgeList4_2[1], (416, 128))                
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,3)] == 2):
                screen.blit(self.doorList4_2[1], (416, 128))                               
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,3)] == 3):
                screen.blit(self.doorList4_2[1], (416, 128))                               
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,3)] == 4):
                screen.blit(self.doorList4_2[1], (416, 128))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,3)] == 6):
                screen.blit(self.doorList4_2[1], (416, 128))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,3)] == 7):
                screen.blit(self.edgeList4_2[1], (416, 128))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,3)] == 8):
                screen.blit(self.doorList4_2[1], (416, 128))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,3)] == 9):
                screen.blit(self.edgeList4_2[1], (416, 128))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,3)] == 12):
                screen.blit(self.switchedgeList4_2[1], (416, 128)) 
            #switch on left side
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,3)] == 13):
                screen.blit(self.edgeList4_2[1], (416, 128)) 

            #draw up three wall on right
            if (self.horizontal_wall[y][decrement(x,3)] == 1):
                screen.blit(self.edgeList4[1], (352, 128))                
            elif (self.horizontal_wall[y][decrement(x,3)] == 2):
                screen.blit(self.doorList4[1], (352, 128))  
            elif (self.horizontal_wall[y][decrement(x,3)] == 3):
                screen.blit(self.doorList4[1], (352, 128))  
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][decrement(x,3)] == 4):
                screen.blit(self.doorList4[1], (352, 128))
            #one way door from right
            elif (self.horizontal_wall[y][decrement(x,3)] == 6):
                screen.blit(self.doorList4[1], (352, 128))
            #one way door from left
            elif (self.horizontal_wall[y][decrement(x,3)] == 7):
                screen.blit(self.edgeList4[1], (352, 128))
            #hidden one way door from right
            elif (self.horizontal_wall[y][decrement(x,3)] == 8):
                screen.blit(self.doorList4[1], (352, 128))
            #hidden one way door from left
            elif (self.horizontal_wall[y][decrement(x,3)] == 9):
                screen.blit(self.edgeList4[1], (352, 128))
            #switch on right side
            elif (self.horizontal_wall[y][decrement(x,3)] == 12):
                screen.blit(self.switchedgeList4[1], (352, 128)) 
            #switch on left side
            elif (self.horizontal_wall[y][decrement(x,3)] == 13):
                screen.blit(self.edgeList4[1], (352, 128)) 

            #draw straight two block wall left two
            if (self.vertical_wall[increment(y,2)][decrement(x,2)] == 1):
                screen.blit(self.center3, (0, 128))
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 2):
                screen.blit(self.door3, (0,128))
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 3):
                screen.blit(self.door3, (0,128))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 4):
                screen.blit(self.door3, (0,128))
            #one way door from right
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 6):
                screen.blit(self.door3, (0,128))
            #one way door from left
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 7):
                screen.blit(self.center3, (0,128))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 8):
                screen.blit(self.door3, (0,128))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 9):
                screen.blit(self.center3, (0,128))
            #switch on right side
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 12):
                screen.blit(self.switch3, (0,128))                                                               
            #switch on left side
            elif (self.vertical_wall[increment(y,2)][decrement(x,2)] == 13):
                screen.blit(self.center3, (0,128)) 


            #draw straight two block wall left one
            if (self.vertical_wall[increment(y,1)][decrement(x,2)] == 1):
                screen.blit(self.center3, (128, 128))
            elif (self.vertical_wall[increment(y,1)][decrement(x,2)] == 2):
                screen.blit(self.door3, (128,128))
            elif (self.vertical_wall[increment(y,1)][decrement(x,2)] == 3):
                screen.blit(self.door3, (128,128))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,1)][decrement(x,2)] == 4):
                screen.blit(self.door3, (128,128))
            #one way door from right
            elif (self.vertical_wall[increment(y,1)][decrement(x,2)] == 6):
                screen.blit(self.door3, (128,128))
            #one way door from left
            elif (self.vertical_wall[increment(y,1)][decrement(x,2)] == 7):
                screen.blit(self.center3, (128,128))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,1)][decrement(x,2)] == 8):
                screen.blit(self.door3, (128,128))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,1)][decrement(x,2)] == 9):
                screen.blit(self.center3, (128,128))
            #switch on right side
            elif (self.vertical_wall[increment(y,1)][decrement(x,2)] == 12):
                screen.blit(self.switch3, (128,128))                                                               
            #switch on left side
            elif (self.vertical_wall[increment(y,1)][decrement(x,2)] == 13):
                screen.blit(self.center3, (128,128)) 


            #draw straight two block wall
            if (self.vertical_wall[y][decrement(x,2)] == 1):
                screen.blit(self.center3, (256, 128))
            elif (self.vertical_wall[y][decrement(x,2)] == 2):
                screen.blit(self.door3, (256,128))
            elif (self.vertical_wall[y][decrement(x,2)] == 3):
                screen.blit(self.door3, (256,128))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][decrement(x,2)] == 4):
                screen.blit(self.door3, (256,128))
            #one way door from right
            elif (self.vertical_wall[y][decrement(x,2)] == 6):
                screen.blit(self.door3, (256,128))
            #one way door from left
            elif (self.vertical_wall[y][decrement(x,2)] == 7):
                screen.blit(self.center3, (256,128))
            #hidden one way door from right
            elif (self.vertical_wall[y][decrement(x,2)] == 8):
                screen.blit(self.door3, (256,128))
            #hidden one way door from left
            elif (self.vertical_wall[y][decrement(x,2)] == 9):
                screen.blit(self.center3, (256,128))
            #switch on right side
            elif (self.vertical_wall[y][decrement(x,2)] == 12):
                screen.blit(self.switch3, (256,128))                                                               
            #switch on left side
            elif (self.vertical_wall[y][decrement(x,2)] == 13):
                screen.blit(self.center3, (256,128)) 


            #draw straight two block wall right one
            if (self.vertical_wall[decrement(y,1)][decrement(x,2)] == 1):
                screen.blit(self.center3, (384, 128))
            elif (self.vertical_wall[decrement(y,1)][decrement(x,2)] == 2):
                screen.blit(self.door3, (384,128))
            elif (self.vertical_wall[decrement(y,1)][decrement(x,2)] == 3):
                screen.blit(self.door3, (384,128))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,1)][decrement(x,2)] == 4):
                screen.blit(self.door3, (384,128))
            #one way door from right
            elif (self.vertical_wall[decrement(y,1)][decrement(x,2)] == 6):
                screen.blit(self.door3, (384,128))
            #one way door from left
            elif (self.vertical_wall[decrement(y,1)][decrement(x,2)] == 7):
                screen.blit(self.center3, (384,128))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,1)][decrement(x,2)] == 8):
                screen.blit(self.door3, (384,128))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,1)][decrement(x,2)] == 9):
                screen.blit(self.center3, (384,128))
            #switch on right side
            elif (self.vertical_wall[decrement(y,1)][decrement(x,2)] == 12):
                screen.blit(self.switch3, (384,128))                                                               
            #switch on left side
            elif (self.vertical_wall[decrement(y,1)][decrement(x,2)] == 13):
                screen.blit(self.center3, (384,128)) 

            #draw straight two block wall right two
            if (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 1):
                screen.blit(self.center3, (512, 128))
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 2):
                screen.blit(self.door3, (512,128))
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 3):
                screen.blit(self.door3, (512,128))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 4):
                screen.blit(self.door3, (512,128))
            #one way door from right
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 6):
                screen.blit(self.door3, (512,128))
            #one way door from left
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 7):
                screen.blit(self.center3, (512,128))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 8):
                screen.blit(self.door3, (512,128))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 9):
                screen.blit(self.center3, (512,128))
            #switch on right side
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 12):
                screen.blit(self.switch3, (512,128))                                                               
            #switch on left side
            elif (self.vertical_wall[decrement(y,2)][decrement(x,2)] == 13):
                screen.blit(self.center3, (512,128)) 


            #draw up two wall on left three
            if (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 1):
                screen.blit(self.edgeList3_3[0], (-320, 64))
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 2):
                screen.blit(self.doorList3_3[0], (-320, 64))
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 3):
                screen.blit(self.doorList3_3[0], (-320, 64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 4):
                screen.blit(self.doorList3_3[0], (-320, 64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 6):
                screen.blit(self.edgeList3_3[0], (-320, 64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 7):
                screen.blit(self.doorList3_3[0], (-320, 64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 8):
                screen.blit(self.edgeList3_3[0], (-320, 64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 9):
                screen.blit(self.doorList3_3[0], (-320, 64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 12):
                screen.blit(self.edgeList3_3[0], (-320, 64)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,3)][decrement(x,2)] == 13):
                screen.blit(self.switchedgeList3_3[0], (-320, 64)) 


            #draw up two wall on left two
            if (self.horizontal_wall[increment(y,2)][decrement(x,2)] == 1):
                screen.blit(self.edgeList3_2[0], (-64, 64))
            elif (self.horizontal_wall[increment(y,2)][decrement(x,2)] == 2):
                screen.blit(self.doorList3_2[0], (-64, 64))
            elif (self.horizontal_wall[increment(y,2)][decrement(x,2)] == 3):
                screen.blit(self.doorList3_2[0], (-64, 64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,2)][decrement(x,2)] == 4):
                screen.blit(self.doorList3_2[0], (-64, 64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,2)][decrement(x,2)] == 6):
                screen.blit(self.edgeList3_2[0], (-64, 64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,2)][decrement(x,2)] == 7):
                screen.blit(self.doorList3_2[0], (-64, 64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,2)][decrement(x,2)] == 8):
                screen.blit(self.edgeList3_2[0], (-64, 64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,2)][decrement(x,2)] == 9):
                screen.blit(self.doorList3_2[0], (-64, 64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,2)][decrement(x,2)] == 12):
                screen.blit(self.edgeList3_2[0], (-64, 64)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,2)][decrement(x,2)] == 13):
                screen.blit(self.switchedgeList3_2[0], (-64, 64)) 


            #draw up two wall on left
            if (self.horizontal_wall[increment(y,1)][decrement(x,2)] == 1):
                screen.blit(self.edgeList3[0], (192, 64))
            elif (self.horizontal_wall[increment(y,1)][decrement(x,2)] == 2):
                screen.blit(self.doorList3[0], (192, 64))
            elif (self.horizontal_wall[increment(y,1)][decrement(x,2)] == 3):
                screen.blit(self.doorList3[0], (192, 64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,1)][decrement(x,2)] == 4):
                screen.blit(self.doorList3[0], (192, 64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][decrement(x,2)] == 6):
                screen.blit(self.edgeList3[0], (192, 64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][decrement(x,2)] == 7):
                screen.blit(self.doorList3[0], (192, 64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][decrement(x,2)] == 8):
                screen.blit(self.edgeList3[0], (192, 64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][decrement(x,2)] == 9):
                screen.blit(self.doorList3[0], (192, 64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][decrement(x,2)] == 12):
                screen.blit(self.edgeList3[0], (192, 64)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][decrement(x,2)] == 13):
                screen.blit(self.switchedgeList3[0], (192, 64)) 
                
                
            #draw up two wall on right three
            if (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 1):
                screen.blit(self.edgeList3_3[1], (640, 64))                
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 2):
                screen.blit(self.doorList3_3[1], (640, 64))    
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 3):
                screen.blit(self.doorList3_3[1], (640, 64))    
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 4):
                screen.blit(self.doorList3_3[1],  (640, 64))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 6):
                screen.blit(self.doorList3_3[1],  (640, 64))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 7):
                screen.blit(self.edgeList3_3[1],  (640, 64))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 8):
                screen.blit(self.doorList3_3[1],  (640, 64))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 9):
                screen.blit(self.edgeList3_3[1],  (640, 64))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 12):
                screen.blit(self.switchedgeList3_3[1],  (640, 64)) 
            #switch on left side
            elif (self.horizontal_wall[decrement(y,2)][decrement(x,2)] == 13):
                screen.blit(self.edgeList3_3[1],  (640, 64))

            #draw up two wall on right two
            if (self.horizontal_wall[decrement(y,1)][decrement(x,2)] == 1):
                screen.blit(self.edgeList3_2[1], (512, 64))                
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,2)] == 2):
                screen.blit(self.doorList3_2[1], (512, 64))    
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,2)] == 3):
                screen.blit(self.doorList3_2[1], (512, 64))    
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,2)] == 4):
                screen.blit(self.doorList3_2[1],  (512, 64))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,2)] == 6):
                screen.blit(self.doorList3_2[1],  (512, 64))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,2)] == 7):
                screen.blit(self.edgeList3_2[1],  (512, 64))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,2)] == 8):
                screen.blit(self.doorList3_2[1],  (512, 64))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,2)] == 9):
                screen.blit(self.edgeList3_2[1],  (512, 64))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,2)] == 12):
                screen.blit(self.switchedgeList3_2[1],  (512, 64)) 
            #switch on left side
            elif (self.horizontal_wall[decrement(y,1)][decrement(x,2)] == 13):
                screen.blit(self.edgeList3_2[1],  (512, 64)) 

            #draw up two wall on right
            if (self.horizontal_wall[y][decrement(x,2)] == 1):
                screen.blit(self.edgeList3[1], (384, 64))                
            elif (self.horizontal_wall[y][decrement(x,2)] == 2):
                screen.blit(self.doorList3[1], (384, 64))  
            elif (self.horizontal_wall[y][decrement(x,2)] == 3):
                screen.blit(self.doorList3[1], (384, 64))  
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][decrement(x,2)] == 4):
                screen.blit(self.doorList3[1],  (384, 64))
            #one way door from right
            elif (self.horizontal_wall[y][decrement(x,2)] == 6):
                screen.blit(self.doorList3[1],  (384, 64))
            #one way door from left
            elif (self.horizontal_wall[y][decrement(x,2)] == 7):
                screen.blit(self.edgeList3[1],  (384, 64))
            #hidden one way door from right
            elif (self.horizontal_wall[y][decrement(x,2)] == 8):
                screen.blit(self.doorList3[1],  (384, 64))
            #hidden one way door from left
            elif (self.horizontal_wall[y][decrement(x,2)] == 9):
                screen.blit(self.edgeList3[1],  (384, 64))
            #switch on right side
            elif (self.horizontal_wall[y][decrement(x,2)] == 12):
                screen.blit(self.switchedgeList3[1],  (384, 64)) 
            #switch on left side
            elif (self.horizontal_wall[y][decrement(x,2)] == 13):
                screen.blit(self.edgeList3[1],  (384, 64)) 
                
            #draw straight one block wall left one
            if (self.vertical_wall[increment(y,1)][decrement(x,1)] == 1):
                screen.blit(self.center2, (-64, 64))
            elif (self.vertical_wall[increment(y,1)][decrement(x,1)] == 2):
                screen.blit(self.door2, (-64,64))
            elif (self.vertical_wall[increment(y,1)][decrement(x,1)] == 3):
                screen.blit(self.door2, (-64,64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,1)][decrement(x,1)] == 4):
                screen.blit(self.door2, (-64,64))
            #one way door from right
            elif (self.vertical_wall[increment(y,1)][decrement(x,1)] == 6):
                screen.blit(self.door2, (-64,64))
            #one way door from left
            elif (self.vertical_wall[increment(y,1)][decrement(x,1)] == 7):
                screen.blit(self.center2, (-64,64))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,1)][decrement(x,1)] == 8):
                screen.blit(self.door2, (-64,64))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,1)][decrement(x,1)] == 9):
                screen.blit(self.center2, (-64,64))
            #switch on right side
            elif (self.vertical_wall[increment(y,1)][decrement(x,1)] == 12):
                screen.blit(self.switch2, (-64,64))                                                               
            #switch on left side
            elif (self.vertical_wall[increment(y,1)][decrement(x,1)] == 13):
                screen.blit(self.center2, (-64,64)) 
        
            #draw straight one block wall
            if (self.vertical_wall[y][decrement(x,1)] == 1):
                screen.blit(self.center2, (192, 64))
            elif (self.vertical_wall[y][decrement(x,1)] == 2):
                screen.blit(self.door2, (192, 64))
            elif (self.vertical_wall[y][decrement(x,1)] == 3):
                screen.blit(self.door2, (192, 64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][decrement(x,1)] == 4):
                screen.blit(self.door2, (192,64))
            #one way door from right
            elif (self.vertical_wall[y][decrement(x,1)] == 6):
                screen.blit(self.door2, (192,64))
            #one way door from left
            elif (self.vertical_wall[y][decrement(x,1)] == 7):
                screen.blit(self.center2, (192,64))
            #hidden one way door from right
            elif (self.vertical_wall[y][decrement(x,1)] == 8):
                screen.blit(self.door2, (192,64))
            #hidden one way door from left
            elif (self.vertical_wall[y][decrement(x,1)] == 9):
                screen.blit(self.center2, (192,64))
            #switch on right side
            elif (self.vertical_wall[y][decrement(x,1)] == 12):
                screen.blit(self.switch2, (192,64))                                                               
            #switch on left side
            elif (self.vertical_wall[y][decrement(x,1)] == 13):
                screen.blit(self.center2, (192,64)) 

            #draw straight one block wall right one
            if (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 1):
                screen.blit(self.center2, (448, 64))
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 2):
                screen.blit(self.door2, (448,64))
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 3):
                screen.blit(self.door2, (448,64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 4):
                screen.blit(self.door2, (448,64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 6):
                screen.blit(self.door2, (448,64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 7):
                screen.blit(self.center2, (448,64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 8):
                screen.blit(self.door2, (448,64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 9):
                screen.blit(self.center2, (448,64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 12):
                screen.blit(self.switch2, (448,64))                                                               
            #switch on left side
            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 13):
                screen.blit(self.center2, (448,64)) 

            #draw up one wall on left
            if (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 1):
                screen.blit(self.edgeList2[0], (64, -64))
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 2):
                screen.blit(self.doorList2[0], (64, -64))
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 3):
                screen.blit(self.doorList2[0], (64, -64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 4):
                screen.blit(self.doorList2[0], (64, -64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 6):
                screen.blit(self.edgeList2[0], (64, -64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 7):
                screen.blit(self.doorList2[0], (64, -64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 8):
                screen.blit(self.edgeList2[0], (64, -64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 9):
                screen.blit(self.doorList2[0], (64, -64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 12):
                screen.blit(self.edgeList2[0], (64, -64)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 13):
                screen.blit(self.switchedgeList2[0], (64, -64)) 
                
            #draw up one wall on right
            if (self.horizontal_wall[y][decrement(x,1)] == 1):
                screen.blit(self.edgeList2[1], (448, -64))                
            elif (self.horizontal_wall[y][decrement(x,1)] == 2):
                screen.blit(self.doorList2[1], (448, -64))                
            elif (self.horizontal_wall[y][decrement(x,1)] == 3):
                screen.blit(self.doorList2[1], (448, -64))                
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][decrement(x,1)] == 4):
                screen.blit(self.doorList2[1],  (448, -64))
            #one way door from right
            elif (self.horizontal_wall[y][decrement(x,1)] == 6):
                screen.blit(self.doorList2[1],  (448, -64))
            #one way door from left
            elif (self.horizontal_wall[y][decrement(x,1)] == 7):
                screen.blit(self.edgeList2[1],  (448, -64))
            #hidden one way door from right
            elif (self.horizontal_wall[y][decrement(x,1)] == 8):
                screen.blit(self.doorList2[1],  (448, -64))
            #hidden one way door from left
            elif (self.horizontal_wall[y][decrement(x,1)] == 9):
                screen.blit(self.edgeList2[1],  (448, -64))
            #switch on right side
            elif (self.horizontal_wall[y][decrement(x,1)] == 12):
                screen.blit(self.switchedgeList2[1],  (448, -64)) 
            #switch on left side
            elif (self.horizontal_wall[y][decrement(x,1)] == 13):
                screen.blit(self.edgeList2[1],  (448, -64)) 



            #draw left one up wall
            if (self.vertical_wall[increment(y,1)][x] == 1):
                screen.blit(self.center1, (-448,-64))
            elif (self.vertical_wall[increment(y,1)][x] == 2):
                screen.blit(self.door1, (-448,-64))
            elif (self.vertical_wall[increment(y,1)][x] == 3):
                screen.blit(self.door1, (-448,-64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,1)][x] == 4):
                screen.blit(self.door1, (-448,-64))
            #one way door from right
            elif (self.vertical_wall[increment(y,1)][x] == 6):
                screen.blit(self.door1, (-448,-64))
            #one way door from left
            elif (self.vertical_wall[increment(y,1)][x] == 7):
                screen.blit(self.center1, (-448,-64))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,1)][x] == 8):
                screen.blit(self.door1, (-448,-64))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,1)][x] == 9):
                screen.blit(self.center1, (-448,-64))
            #switch on right side
            elif (self.vertical_wall[increment(y,1)][x] == 12):
                screen.blit(self.switch1, (-448,-64))                                                               
            #switch on left side
            elif (self.vertical_wall[increment(y,1)][x] == 13):
                screen.blit(self.center1, (-448,-64)) 

            #draw right one up wall
            if (self.vertical_wall[decrement(y,1)][x] == 1):
                screen.blit(self.center1, (576,-64))
            if (self.vertical_wall[decrement(y,1)][x] == 2):
                screen.blit(self.door1, (576,-64))
            if (self.vertical_wall[decrement(y,1)][x] == 3):
                screen.blit(self.door1, (576,-64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,1)][x] == 4):
                screen.blit(self.door1, (576,-64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,1)][x] == 6):
                screen.blit(self.door1, (576,-64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,1)][x] == 7):
                screen.blit(self.center1, (576,-64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,1)][x] == 8):
                screen.blit(self.door1, (576,-64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,1)][x] == 9):
                screen.blit(self.center1, (576,-64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,1)][x] == 12):
                screen.blit(self.switch1, (576,-64))                                                               
            #switch on left side
            elif (self.vertical_wall[decrement(y,1)][x] == 13):
                screen.blit(self.center1, (576,-64)) 

            #draw just up wall
            if (self.vertical_wall[y][x] == 1):
                screen.blit(self.center1, (64,-64))
            elif (self.vertical_wall[y][x] == 2):
                screen.blit(self.door1, (64,-64))
            elif (self.vertical_wall[y][x] == 3):
                screen.blit(self.door1, (64,-64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][x] == 4):
                screen.blit(self.door1, (64,-64))
            #one way door from right
            elif (self.vertical_wall[y][x] == 6):
                screen.blit(self.door1, (64,-64))
            #one way door from left
            elif (self.vertical_wall[y][x] == 7):
                screen.blit(self.center1, (64,-64))
            #hidden one way door from right
            elif (self.vertical_wall[y][x] == 8):
                screen.blit(self.door1, (64,-64))
            #hidden one way door from left
            elif (self.vertical_wall[y][x] == 9):
                screen.blit(self.center1, (64,-64))
            #switch on right side
            elif (self.vertical_wall[y][x] == 12):
                screen.blit(self.switch1, (64,-64))                                                               
            #switch on left side
            elif (self.vertical_wall[y][x] == 13):
                screen.blit(self.center1, (64,-64)) 

            #draw wall on left
            if (self.horizontal_wall[increment(y,1)][x] == 1):
                screen.blit(self.edgeList1[0], (-192, -320))
            elif (self.horizontal_wall[increment(y,1)][x] == 2):
                screen.blit(self.doorList1[0], (-192, -320))
            elif (self.horizontal_wall[increment(y,1)][x] == 3):
                screen.blit(self.doorList1[0], (-192, -320))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,1)][x] == 4):
                screen.blit(self.doorList1[0], (-192, -320))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][x] == 6):
                screen.blit(self.edgeList1[0], (-192, -320))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][x] == 7):
                screen.blit(self.doorList1[0], (-192, -320))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][x] == 8):
                screen.blit(self.edgeList1[0], (-192, -320))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][x] == 9):
                screen.blit(self.doorList1[0], (-192, -320))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][x] == 12):
                screen.blit(self.edgeList1[0], (-192, -320)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][x] == 13):
                screen.blit(self.switchedgeList1[0], (-192, -320)) 

            #draw wall on right
            if (self.horizontal_wall[y][x] == 1):
                screen.blit(self.edgeList1[1], (576, -320))
            elif (self.horizontal_wall[y][x] == 2):
                screen.blit(self.doorList1[1], (576, -320))
            elif (self.horizontal_wall[y][x] == 3):
                screen.blit(self.doorList1[1], (576, -320))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][x] == 4):
                screen.blit(self.doorList1[1],  (576, -320))
            #one way door from right
            elif (self.horizontal_wall[y][x] == 6):
                screen.blit(self.doorList1[1],  (576, -320))
            #one way door from left
            elif (self.horizontal_wall[y][x] == 7):
                screen.blit(self.edgeList1[1],  (576, -320))
            #hidden one way door from right
            elif (self.horizontal_wall[y][x] == 8):
                screen.blit(self.doorList1[1],  (576, -320))
            #hidden one way door from left
            elif (self.horizontal_wall[y][x] == 9):
                screen.blit(self.edgeList1[1],  (576, -320))
            #switch on right side
            elif (self.horizontal_wall[y][x] == 12):
                screen.blit(self.switchedgeList1[1],  (576, -320)) 
            #switch on left side
            elif (self.horizontal_wall[y][x] == 13):
                screen.blit(self.edgeList1[1],  (576, -320)) 


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
            draw_dungeon_ground( screen, self.ground[y][x], self.ground_center1, (32, 448))
            #draw ground left
            draw_dungeon_ground( screen, self.ground[y][decrement(x,1)], self.ground_sideList1[0], (0, 448))
            #draw ground right
            draw_dungeon_ground( screen, self.ground[y][increment(x,1)], self.ground_sideList1[1], (576, 448))
            #draw ground up left
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][decrement(x,1)], self.ground_sideList2[0], (0,320))
            #draw ground up right
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][increment(x,1)], self.ground_sideList2[1], (448,320))
            #draw ground up one
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][x], self.ground_center2, (64,320))



           #draw straight one block wall
            if (self.horizontal_wall[decrement(y,1)][x] == 1):
                screen.blit(self.center2, (192, 64))
            elif (self.horizontal_wall[decrement(y,1)][x] == 2):
                screen.blit(self.door2, (192,64))
            elif (self.horizontal_wall[decrement(y,1)][x] == 3):
                screen.blit(self.door2, (192,64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[decrement(y,1)][x] == 4):
                screen.blit(self.center2, (192,64))
            #one way door from right
            elif (self.horizontal_wall[decrement(y,1)][x] == 6):
                screen.blit(self.door2, (192,64))
            #one way door from left
            elif (self.horizontal_wall[decrement(y,1)][x] == 7):
                screen.blit(self.center2, (192,64))
            #hidden one way door from right
            elif (self.horizontal_wall[decrement(y,1)][x] == 8):
                screen.blit(self.door2, (192,64))
            #hidden one way door from left
            elif (self.horizontal_wall[decrement(y,1)][x] == 9):
                screen.blit(self.center2, (192,64))
            #switch on right side
            elif (self.horizontal_wall[decrement(y,1)][x] == 12):
                screen.blit(self.switch2, (192,64))  
            #switch on left side
            elif (self.horizontal_wall[decrement(y,1)][x] == 13):
                screen.blit(self.center2, (192,64))


            #draw up one wall on left
            if (self.vertical_wall[decrement(y,1)][x] == 1):
                screen.blit(self.edgeList2[0], (64, -64))
            elif (self.vertical_wall[decrement(y,1)][x] == 2):
                screen.blit(self.doorList2[0], (64, -64))
            elif (self.vertical_wall[decrement(y,1)][x] == 3):
                screen.blit(self.doorList2[0], (64, -64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,1)][x] == 4):
                screen.blit(self.edgeList2[0], (64, -64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,1)][x] == 6):
                screen.blit(self.doorList2[0], (64, -64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,1)][x] == 7):
                screen.blit(self.edgeList2[0], (64, -64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,1)][x] == 8):
                screen.blit(self.doorList2[0], (64, -64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,1)][x] == 9):
                screen.blit(self.edgeList2[0], (64, -64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,1)][x] == 12):
                screen.blit(self.switchedgeList2[0], (64, -64)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,1)][x] == 13):
                screen.blit(self.edgeList2[0], (64, -64)) 
                                   
            #draw up one wall on right
            if (self.vertical_wall[decrement(y,1)][increment(x,1)] == 1):
                screen.blit(self.edgeList2[1], (448, -64))                
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 2):
                screen.blit(self.doorList2[1], (448, -64))                
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 3):
                screen.blit(self.doorList2[1], (448, -64))                
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 4):
                screen.blit(self.edgeList2[1], (448, -64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 6):
                screen.blit(self.edgeList2[1], (448, -64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 7):
                screen.blit(self.doorList2[1], (448, -64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 8):
                screen.blit(self.edgeList2[1], (448, -64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 9):
                screen.blit(self.doorList2[1], (448, -64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 12):
                screen.blit(self.edgeList2[1], (448, -64)) 
            #switch on left side
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 13):
                screen.blit(self.switchedgeList2[1], (448, -64)) 

            #draw left one up wall
            if (self.horizontal_wall[y][decrement(x,1)] == 1):
                screen.blit(self.center1, (-448,-64))
            elif (self.horizontal_wall[y][decrement(x,1)] == 2):
                screen.blit(self.door1, (-448,-64))
            elif (self.horizontal_wall[y][decrement(x,1)] == 3):
                screen.blit(self.door1, (-448,-64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][decrement(x,1)] == 4):
                screen.blit(self.center1, (-448,-64))
            #one way door from right
            elif (self.horizontal_wall[y][decrement(x,1)] == 6):
                screen.blit(self.door1, (-448,-64))
            #one way door from left
            elif (self.horizontal_wall[y][decrement(x,1)] == 7):
                screen.blit(self.center1, (-448,-64))
            #hidden one way door from right
            elif (self.horizontal_wall[y][decrement(x,1)] == 8):
                screen.blit(self.door1, (-448,-64))
            #hidden one way door from left
            elif (self.horizontal_wall[y][decrement(x,1)] == 9):
                screen.blit(self.center1, (-448,-64))
            #switch on right side
            elif (self.horizontal_wall[y][decrement(x,1)] == 12):
                screen.blit(self.switch1, (-448,-64))  
            #switch on left side
            elif (self.horizontal_wall[y][decrement(x,1)] == 13):
                screen.blit(self.center1, (-448,-64))


            #draw right one up wall
            if (self.horizontal_wall[y][increment(x,1)] == 1):
                screen.blit(self.center1, (576,-64))
            elif (self.horizontal_wall[y][increment(x,1)] == 2):
                screen.blit(self.door1, (576,-64))
            elif (self.horizontal_wall[y][increment(x,1)] == 3):
                screen.blit(self.door1, (576,-64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][increment(x,1)] == 4):
                screen.blit(self.center1, (576,-64))
            #one way door from right
            elif (self.horizontal_wall[y][increment(x,1)] == 6):
                screen.blit(self.door1, (576,-64))
            #one way door from left
            elif (self.horizontal_wall[y][increment(x,1)] == 7):
                screen.blit(self.center1, (576,-64))
            #hidden one way door from right
            elif (self.horizontal_wall[y][increment(x,1)] == 8):
                screen.blit(self.door1, (576,-64))
            #hidden one way door from left
            elif (self.horizontal_wall[y][increment(x,1)] == 9):
                screen.blit(self.center1, (576,-64))
            #switch on right side
            elif (self.horizontal_wall[y][increment(x,1)] == 12):
                screen.blit(self.switch1,(576,-64))  
            #switch on left side
            elif (self.horizontal_wall[y][increment(x,1)] == 13):
                screen.blit(self.center1, (576,-64))


            #draw just up wall
            if (self.horizontal_wall[y][x] == 1):
                screen.blit(self.center1, (64,-64))
            elif (self.horizontal_wall[y][x] == 2):
                screen.blit(self.door1, (64,-64))
            elif (self.horizontal_wall[y][x] == 3):
                screen.blit(self.door1, (64,-64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][x] == 4):
                screen.blit(self.center1, (64,-64))
            #one way door from right
            elif (self.horizontal_wall[y][x] == 6):
                screen.blit(self.door1, (64,-64))
            #one way door from left
            elif (self.horizontal_wall[y][x] == 7):
                screen.blit(self.center1, (64,-64))
            #hidden one way door from right
            elif (self.horizontal_wall[y][x] == 8):
                screen.blit(self.door1, (64,-64))
            #hidden one way door from left
            elif (self.horizontal_wall[y][x] == 9):
                screen.blit(self.center1, (64,-64))
            #switch on right side
            elif (self.horizontal_wall[y][x] == 12):
                screen.blit(self.switch1,(64,-64))  
            #switch on left side
            elif (self.horizontal_wall[y][x] == 13):
                screen.blit(self.center1, (64,-64))


            #draw wall on left
            if (self.vertical_wall[y][x] == 1):
                screen.blit(self.edgeList1[0], (-192, -320))
            elif (self.vertical_wall[y][x] == 2):
                screen.blit(self.doorList1[0], (-192, -320))
            elif (self.vertical_wall[y][x] == 3):
                screen.blit(self.doorList1[0], (-192, -320))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][x] == 4):
                screen.blit(self.edgeList1[0], (-192, -320))
            #one way door from right
            elif (self.vertical_wall[y][x] == 6):
                screen.blit(self.doorList1[0], (-192, -320))
            #one way door from left
            elif (self.vertical_wall[y][x] == 7):
                screen.blit(self.edgeList1[0], (-192, -320))
            #hidden one way door from right
            elif (self.vertical_wall[y][x] == 8):
                screen.blit(self.doorList1[0], (-192, -320))
            #hidden one way door from left
            elif (self.vertical_wall[y][x] == 9):
                screen.blit(self.edgeList1[0], (-192, -320))
            #switch on right side
            elif (self.vertical_wall[y][x] == 12):
                screen.blit(self.switchedgeList1[0], (-192, -320)) 
            #switch on left side
            elif (self.vertical_wall[y][x] == 13):
                screen.blit(self.edgeList1[0], (-192, -320)) 

            #draw wall on right
            if (self.vertical_wall[y][increment(x,1)] == 1):
                screen.blit(self.edgeList1[1], (576, -320))
            elif (self.vertical_wall[y][increment(x,1)] == 2):
                screen.blit(self.doorList1[1], (576, -320))
            elif (self.vertical_wall[y][increment(x,1)] == 3):
                screen.blit(self.doorList1[1], (576, -320))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][increment(x,1)] == 4):
                screen.blit(self.edgeList1[1], (576, -320))
            #one way door from right
            elif (self.vertical_wall[y][increment(x,1)] == 6):
                screen.blit(self.edgeList1[1], (576, -320))
            #one way door from left
            elif (self.vertical_wall[y][increment(x,1)] == 7):
                screen.blit(self.doorList1[1], (576, -320))
            #hidden one way door from right
            elif (self.vertical_wall[y][increment(x,1)] == 8):
                screen.blit(self.edgeList1[1], (576, -320))
            #hidden one way door from left
            elif (self.vertical_wall[y][increment(x,1)] == 9):
                screen.blit(self.doorList1[1], (576, -320))
            #switch on right side
            elif (self.vertical_wall[y][increment(x,1)] == 12):
                screen.blit(self.edgeList1[1], (576, -320)) 
            #switch on left side
            elif (self.vertical_wall[y][increment(x,1)] == 13):
                screen.blit(self.switchedgeList1[1], (576, -320)) 

        #if player is looking right
        elif (game_self.party.direction == 1):

            #draw ground below
            draw_dungeon_ground( screen, self.ground[y][x], self.ground_center1, (32, 448))
            #draw ground left
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][x], self.ground_sideList1[0], (0, 448))
            #draw ground right
            draw_dungeon_ground( screen, self.ground[increment(y,1)][x], self.ground_sideList1[1], (576, 448))
            #draw ground up left
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][increment(x,1)], self.ground_sideList2[0], (0,320))
            #draw ground up right
            draw_dungeon_ground( screen, self.ground[increment(y,1)][increment(x,1)], self.ground_sideList2[1], (448,320))             
            #draw ground up one
            draw_dungeon_ground( screen, self.ground[y][increment(x,1)], self.ground_center2, (64,320))

        
            #draw straight one block wall
            if (self.vertical_wall[y][increment(x,2)] == 1):
                screen.blit(self.center2, (192, 64))
            elif (self.vertical_wall[y][increment(x,2)] == 2):
                screen.blit(self.door2, (192, 64))
            elif (self.vertical_wall[y][increment(x,2)] == 3):
                screen.blit(self.door2, (192, 64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][increment(x,2)] == 4):
                screen.blit(self.center2, (192,64))
            #one way door from right
            elif (self.vertical_wall[y][increment(x,2)] == 6):
                screen.blit(self.center2, (192,64))
            #one way door from left
            elif (self.vertical_wall[y][increment(x,2)] == 7):
                screen.blit(self.door2, (192,64))
            #hidden one way door from right
            elif (self.vertical_wall[y][increment(x,2)] == 8):
                screen.blit(self.center2, (192,64))
            #hidden one way door from left
            elif (self.vertical_wall[y][increment(x,2)] == 9):
                screen.blit(self.door2, (192,64))
            #switch on right side
            elif (self.vertical_wall[y][increment(x,2)] == 12):
                screen.blit(self.center2, (192,64))                                                               
            #switch on left side
            elif (self.vertical_wall[y][increment(x,2)] == 13):
                screen.blit(self.switch2, (192,64)) 

##            #draw straight one block wall right one
##            if (self.vertical_wall[increment(y,1)][increment(x,2)] == 1):
##                screen.blit(self.center2, (448, 64))
##            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 2):
##                screen.blit(self.door2, (448,64))
##            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 3):
##                screen.blit(self.door2, (448,64))
##            #hidden door, with light it can see door
##            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 4):
##                screen.blit(self.center2, (448,64))
##            #one way door from right
##            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 6):
##                screen.blit(self.center2, (448,64))
##            #one way door from left
##            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 7):
##                screen.blit(self.door2, (448,64))
##            #hidden one way door from right
##            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 8):
##                screen.blit(self.center2, (448,64))
##            #hidden one way door from left
##            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 9):
##                screen.blit(self.door2, (448,64))
##            #switch on right side
##            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 12):
##                screen.blit(self.center2, (448,64))                                                               
##            #switch on left side
##            elif (self.vertical_wall[increment(y,1)][increment(x,2)] == 13):
##                screen.blit(self.switch2, (448,64)) 
##

            #draw up one wall on left
            if (self.horizontal_wall[y][increment(x,1)] == 1):
                screen.blit(self.edgeList2[0], (64, -64))
            elif (self.horizontal_wall[y][increment(x,1)] == 2):
                screen.blit(self.doorList2[0], (64, -64))
            elif (self.horizontal_wall[y][increment(x,1)] == 3):
                screen.blit(self.doorList2[0], (64, -64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][increment(x,1)] == 4):
                screen.blit(self.edgeList2[0], (64, -64))
            #one way door from right
            elif (self.horizontal_wall[y][increment(x,1)] == 6):
                screen.blit(self.doorList2[0], (64, -64))
            #one way door from left
            elif (self.horizontal_wall[y][increment(x,1)] == 7):
                screen.blit(self.edgeList2[0], (64, -64))
            #hidden one way door from right
            elif (self.horizontal_wall[y][increment(x,1)] == 8):
                screen.blit(self.doorList2[0], (64, -64))
            #hidden one way door from left
            elif (self.horizontal_wall[y][increment(x,1)] == 9):
                screen.blit(self.edgeList2[0], (64, -64))
            #switch on right side
            elif (self.horizontal_wall[y][increment(x,1)] == 12):
                screen.blit(self.switchedgeList2[0], (64, -64)) 
            #switch on left side
            elif (self.horizontal_wall[y][increment(x,1)] == 13):
                screen.blit(self.edgeList2[0], (64, -64)) 
                
            #draw up one wall on right
            if (self.horizontal_wall[increment(y,1)][increment(x,1)] == 1):
                screen.blit(self.edgeList2[1], (448, -64))                
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 2):
                screen.blit(self.doorList2[1], (448, -64))                
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 3):
                screen.blit(self.doorList2[1], (448, -64))                
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 4):
                screen.blit(self.edgeList2[1],  (448, -64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 6):
                screen.blit(self.edgeList2[1],  (448, -64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 7):
                screen.blit(self.doorList2[1],  (448, -64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 8):
                screen.blit(self.edgeList2[1],  (448, -64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 9):
                screen.blit(self.doorList2[1],  (448, -64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 12):
                screen.blit(self.edgeList2[1],  (448, -64)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 13):
                screen.blit(self.switchedgeList2[1],  (448, -64)) 


            #draw left one up wall
            if (self.vertical_wall[decrement(y,1)][increment(x,1)] == 1):
                screen.blit(self.center1, (-448,-64))
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 2):
                screen.blit(self.door1, (-448,-64))
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 3):
                screen.blit(self.door1, (-448,-64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 4):
                screen.blit(self.center1, (-448,-64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 6):
                screen.blit(self.center1, (-448,-64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 7):
                screen.blit(self.door1, (-448,-64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 8):
                screen.blit(self.center1, (-448,-64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 9):
                screen.blit(self.door1, (-448,-64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 12):
                screen.blit(self.center1, (-448,-64))                                                               
            #switch on left side
            elif (self.vertical_wall[decrement(y,1)][increment(x,1)] == 13):
                screen.blit(self.switch1, (-448,-64)) 

            #draw right one up wall
            if (self.vertical_wall[increment(y,1)][increment(x,1)] == 1):
                screen.blit(self.center1, (576,-64))
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 2):
                screen.blit(self.door1, (576,-64))
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 3):
                screen.blit(self.door1, (576,-64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 4):
                screen.blit(self.center1, (576,-64))
            #one way door from right
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 6):
                screen.blit(self.center1, (576,-64))
            #one way door from left
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 7):
                screen.blit(self.door1, (576,-64))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 8):
                screen.blit(self.center1, (576,-64))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 9):
                screen.blit(self.door1, (576,-64))
            #switch on right side
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 12):
                screen.blit(self.center1, (576,-64))                                                               
            #switch on left side
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 13):
                screen.blit(self.switch1, (576,-64)) 


            #draw just up wall
            if (self.vertical_wall[y][increment(x,1)] == 1):
                screen.blit(self.center1, (64,-64))
            elif (self.vertical_wall[y][increment(x,1)] == 2):
                screen.blit(self.door1, (64,-64))
            elif (self.vertical_wall[y][increment(x,1)] == 3):
                screen.blit(self.door1, (64,-64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][increment(x,1)] == 4):
                screen.blit(self.center1, (64,-64))
            #one way door from right
            elif (self.vertical_wall[y][increment(x,1)] == 6):
                screen.blit(self.center1, (64,-64))
            #one way door from left
            elif (self.vertical_wall[y][increment(x,1)] == 7):
                screen.blit(self.door1, (64,-64))
            #hidden one way door from right
            elif (self.vertical_wall[y][increment(x,1)] == 8):
                screen.blit(self.center1, (64,-64))
            #hidden one way door from left
            elif (self.vertical_wall[y][increment(x,1)] == 9):
                screen.blit(self.door1, (64,-64))
            #switch on right side
            elif (self.vertical_wall[y][increment(x,1)] == 12):
                screen.blit(self.center1, (64,-64))                                                               
            #switch on left side
            elif (self.vertical_wall[y][increment(x,1)] == 13):
                screen.blit(self.switch1, (64,-64)) 

            #draw wall on left
            if (self.horizontal_wall[y][x] == 1):
                screen.blit(self.edgeList1[0], (-192, -320))
            elif (self.horizontal_wall[y][x] == 2):
                screen.blit(self.doorList1[0], (-192, -320))
            elif (self.horizontal_wall[y][x] == 3):
                screen.blit(self.doorList1[0], (-192, -320))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][x] == 4):
                screen.blit(self.edgeList1[0], (-192, -320))
            #one way door from right
            elif (self.horizontal_wall[y][x] == 6):
                screen.blit(self.doorList1[0], (-192, -320))
            #one way door from left
            elif (self.horizontal_wall[y][x] == 7):
                screen.blit(self.edgeList1[0], (-192, -320))
            #hidden one way door from right
            elif (self.horizontal_wall[y][x] == 8):
                screen.blit(self.doorList1[0], (-192, -320))
            #hidden one way door from left
            elif (self.horizontal_wall[y][x] == 9):
                screen.blit(self.edgeList1[0], (-192, -320))
            #switch on right side
            elif (self.horizontal_wall[y][x] == 12):
                screen.blit(self.switchedgeList1[0], (-192, -320)) 
            #switch on left side
            elif (self.horizontal_wall[y][x] == 13):
                screen.blit(self.edgeList1[0], (-192, -320)) 

            #draw wall on right
            if (self.horizontal_wall[increment(y,1)][x] == 1):
                screen.blit(self.edgeList1[1], (576, -320))
            elif (self.horizontal_wall[increment(y,1)][x] == 2):
                screen.blit(self.doorList1[1], (576, -320))
            elif (self.horizontal_wall[increment(y,1)][x] == 3):
                screen.blit(self.doorList1[1], (576, -320))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,1)][x] == 4):
                screen.blit(self.edgeList1[1],  (576, -320))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][x] == 6):
                screen.blit(self.edgeList1[1],  (576, -320))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][x] == 7):
                screen.blit(self.doorList1[1],  (576, -320))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][x] == 8):
                screen.blit(self.edgeList1[1],  (576, -320))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][x] == 9):
                screen.blit(self.doorList1[1],  (576, -320))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][x] == 12):
                screen.blit(self.edgeList1[1],  (576, -320)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][x] == 13):
                screen.blit(self.switchedgeList1[1],  (576, -320)) 


        #if party is looking down
        elif (game_self.party.direction == 2):

            #draw ground below
            draw_dungeon_ground( screen, self.ground[y][x], self.ground_center1, (32, 448))
            #draw ground left
            draw_dungeon_ground( screen, self.ground[y][increment(x,1)], self.ground_sideList1[0], (0, 448))
            #draw ground right
            draw_dungeon_ground( screen, self.ground[y][decrement(x,1)], self.ground_sideList1[1], (576, 448))
            #draw ground up left
            draw_dungeon_ground( screen, self.ground[increment(y,1)][increment(x,1)], self.ground_sideList2[0], (0,320))
            #draw ground up right
            draw_dungeon_ground( screen, self.ground[increment(y,1)][decrement(x,1)], self.ground_sideList2[1], (448,320))             
            #draw ground up one
            draw_dungeon_ground( screen, self.ground[increment(y,1)][x], self.ground_center2, (64,320))

        
            #draw straight one block wall
            if (self.horizontal_wall[increment(y,2)][x] == 1):
                screen.blit(self.center2, (192, 64))
            elif (self.horizontal_wall[increment(y,2)][x] == 2):
                screen.blit(self.door2, (192, 64))
            elif (self.horizontal_wall[increment(y,2)][x] == 3):
                screen.blit(self.door2, (192, 64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,2)][x] == 4):
                screen.blit(self.center2, (192,64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,2)][x] == 6):
                screen.blit(self.center2, (192,64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,2)][x] == 7):
                screen.blit(self.door2, (192,64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,2)][x] == 8):
                screen.blit(self.center2, (192,64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,2)][x] == 9):
                screen.blit(self.door2, (192,64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,2)][x] == 12):
                screen.blit(self.center2, (192,64))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,2)][x] == 13):
                screen.blit(self.switch2, (192,64))

##            #draw straight one block wall right one
##            if (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 1):
##                screen.blit(self.center2, (448, 64))
##            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 2):
##                screen.blit(self.door2, (448,64))
##            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 3):
##                screen.blit(self.door2, (448,64))
##            #hidden door, with light it can see door
##            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 4):
##                screen.blit(self.center2, (448,64))
##            #one way door from right
##            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 6):
##                screen.blit(self.center2, (448,64))
##            #one way door from left
##            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 7):
##                screen.blit(self.door2, (448,64))
##            #hidden one way door from right
##            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 8):
##                screen.blit(self.center2, (448,64))
##            #hidden one way door from left
##            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 9):
##                screen.blit(self.door2, (448,64))
##            #switch on right side
##            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 12):
##                screen.blit(self.center2, (448,64))  
##            #switch on left side
##            elif (self.horizontal_wall[increment(y,2)][decrement(x,1)] == 13):
##                screen.blit(self.switch2, (448,64))
##
            #draw up one wall on left
            if (self.vertical_wall[increment(y,1)][increment(x,1)] == 1):
                screen.blit(self.edgeList2[0], (64, -64))
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 2):
                screen.blit(self.doorList2[0], (64, -64))
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 3):
                screen.blit(self.doorList2[0], (64, -64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 4):
                screen.blit(self.edgeList2[0], (64, -64))
            #one way door from right
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 6):
                screen.blit(self.edgeList2[0], (64, -64))
            #one way door from left
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 7):
                screen.blit(self.doorList2[0], (64, -64))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 8):
                screen.blit(self.edgeList2[0], (64, -64))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 9):
                screen.blit(self.doorList2[0], (64, -64))
            #switch on right side
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 12):
                screen.blit(self.edgeList2[0], (64, -64)) 
            #switch on left side
            elif (self.vertical_wall[increment(y,1)][increment(x,1)] == 13):
                screen.blit(self.switchedgeList2[0], (64, -64)) 
                
            #draw up one wall on right
            if (self.vertical_wall[increment(y,1)][x] == 1):
                screen.blit(self.edgeList2[1], (448, -64))                
            elif (self.vertical_wall[increment(y,1)][x] == 2):
                screen.blit(self.doorList2[1], (448, -64))                
            elif (self.vertical_wall[increment(y,1)][x] == 3):
                screen.blit(self.doorList2[1], (448, -64))                
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,1)][x] == 4):
                screen.blit(self.edgeList2[1], (448, -64))
            #one way door from right
            elif (self.vertical_wall[increment(y,1)][x] == 6):
                screen.blit(self.doorList2[1], (448, -64))
            #one way door from left
            elif (self.vertical_wall[increment(y,1)][x] == 7):
                screen.blit(self.edgeList2[1], (448, -64))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,1)][x] == 8):
                screen.blit(self.doorList2[1], (448, -64))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,1)][x] == 9):
                screen.blit(self.edgeList2[1], (448, -64))
            #switch on right side
            elif (self.vertical_wall[increment(y,1)][x] == 12):
                screen.blit(self.switchedgeList2[1], (448, -64)) 
            #switch on left side
            elif (self.vertical_wall[increment(y,1)][x] == 13):
                screen.blit(self.edgeList2[1], (448, -64)) 

            #draw left one up wall
            if (self.horizontal_wall[increment(y,1)][increment(x,1)] == 1):
                screen.blit(self.center1, (-448,-64))
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 2):
                screen.blit(self.door1, (-448,-64))
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 3):
                screen.blit(self.door1, (-448,-64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 4):
                screen.blit(self.center1, (-448,-64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 6):
                screen.blit(self.center1, (-448,-64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 7):
                screen.blit(self.door1, (-448,-64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 8):
                screen.blit(self.center1, (-448,-64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 9):
                screen.blit(self.door1, (-448,-64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 12):
                screen.blit(self.center1, (-448,-64))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][increment(x,1)] == 13):
                screen.blit(self.switch1, (-448,-64))


            #draw right one up wall
            if (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 1):
                screen.blit(self.center1, (576,-64))
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 2):
                screen.blit(self.door1, (576,-64))
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 3):
                screen.blit(self.door1, (576,-64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 4):
                screen.blit(self.center1, (576,-64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 6):
                screen.blit(self.center1, (576,-64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 7):
                screen.blit(self.door1, (576,-64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 8):
                screen.blit(self.center1, (576,-64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 9):
                screen.blit(self.door1, (576,-64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 12):
                screen.blit(self.center,(576,-64))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 13):
                screen.blit(self.switch1, (576,-64))

            #draw just up wall
            if (self.horizontal_wall[increment(y,1)][x] == 1):
                screen.blit(self.center1, (64,-64))
            elif (self.horizontal_wall[increment(y,1)][x] == 2):
                screen.blit(self.door1, (64,-64))
            elif (self.horizontal_wall[increment(y,1)][x] == 3):
                screen.blit(self.door1, (64,-64))
            elif (self.horizontal_wall[increment(y,1)][x] == 4):
                screen.blit(self.center1, (64,-64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][x] == 6):
                screen.blit(self.center1, (64,-64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][x] == 7):
                screen.blit(self.door1, (64,-64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][x] == 8):
                screen.blit(self.center1, (64,-64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][x] == 9):
                screen.blit(self.door1, (64,-64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][x] == 12):
                screen.blit(self.center1,(64,-64))  
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][x] == 13):
                screen.blit(self.switch1, (64,-64))
                
            #draw wall on left
            if (self.vertical_wall[y][increment(x,1)] == 1):
                screen.blit(self.edgeList1[0], (-192, -320))
            elif (self.vertical_wall[y][increment(x,1)] == 2):
                screen.blit(self.doorList1[0], (-192, -320))
            elif (self.vertical_wall[y][increment(x,1)] == 3):
                screen.blit(self.doorList1[0], (-192, -320))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][increment(x,1)] == 4):
                screen.blit(self.edgeList1[0], (-192, -320))
            #one way door from right
            elif (self.vertical_wall[y][increment(x,1)] == 6):
                screen.blit(self.edgeList1[0], (-192, -320))
            #one way door from left
            elif (self.vertical_wall[y][increment(x,1)] == 7):
                screen.blit(self.doorList1[0], (-192, -320))
            #hidden one way door from right
            elif (self.vertical_wall[y][increment(x,1)] == 8):
                screen.blit(self.edgeList1[0], (-192, -320))
            #hidden one way door from left
            elif (self.vertical_wall[y][increment(x,1)] == 9):
                screen.blit(self.doorList1[0], (-192, -320))
            #switch on right side
            elif (self.vertical_wall[y][increment(x,1)] == 12):
                screen.blit(self.edgeList1[0], (-192, -320)) 
            #switch on left side
            elif (self.vertical_wall[y][increment(x,1)] == 13):
                screen.blit(self.switchedgeList1[0], (-192, -320))
                
            #draw wall on right
            if (self.vertical_wall[y][x] == 1):
                screen.blit(self.edgeList1[1], (576, -320))
            elif (self.vertical_wall[y][x] == 2):
                screen.blit(self.doorList1[1], (576, -320))
            elif (self.vertical_wall[y][x] == 3):
                screen.blit(self.doorList1[1], (576, -320))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][x] == 4):
                screen.blit(self.edgeList1[1], (576, -320))
            #one way door from right
            elif (self.vertical_wall[y][x] == 6):
                screen.blit(self.doorList1[1], (576, -320))
            #one way door from left
            elif (self.vertical_wall[y][x] == 7):
                screen.blit(self.edgeList1[1], (576, -320))
            #hidden one way door from right
            elif (self.vertical_wall[y][x] == 8):
                screen.blit(self.doorList1[1], (576, -320))
            #hidden one way door from left
            elif (self.vertical_wall[y][x] == 9):
                screen.blit(self.edgeList1[1], (576, -320))
            #switch on right side
            elif (self.vertical_wall[y][x] == 12):
                screen.blit(self.switchedgeList1[1], (576, -320)) 
            #switch on left side
            elif (self.vertical_wall[y][x] == 13):
                screen.blit(self.edgeList1[1], (576, -320)) 


 

        #if the player is looking left
        elif (game_self.party.direction == 3):

            #draw ground below
            draw_dungeon_ground( screen, self.ground[y][x], self.ground_center1, (32, 448))
            #draw ground left
            draw_dungeon_ground( screen, self.ground[increment(y,1)][x], self.ground_sideList1[0], (0, 448))
            #draw ground right
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][x], self.ground_sideList1[1], (576, 448))
            #draw ground up left
            draw_dungeon_ground( screen, self.ground[increment(y,1)][decrement(x,1)], self.ground_sideList2[0], (0,320))
            #draw ground up right
            draw_dungeon_ground( screen, self.ground[decrement(y,1)][decrement(x,1)], self.ground_sideList2[1], (448,320))             
            #draw ground up one
            draw_dungeon_ground( screen, self.ground[y][decrement(x,1)], self.ground_center2, (64,320))

            #draw straight one block wall
            if (self.vertical_wall[y][decrement(x,1)] == 1):
                screen.blit(self.center2, (192, 64))
            elif (self.vertical_wall[y][decrement(x,1)] == 2):
                screen.blit(self.door2, (192, 64))
            elif (self.vertical_wall[y][decrement(x,1)] == 3):
                screen.blit(self.door2, (192, 64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][decrement(x,1)] == 4):
                screen.blit(self.center2, (192,64))
            #one way door from right
            elif (self.vertical_wall[y][decrement(x,1)] == 6):
                screen.blit(self.door2, (192,64))
            #one way door from left
            elif (self.vertical_wall[y][decrement(x,1)] == 7):
                screen.blit(self.center2, (192,64))
            #hidden one way door from right
            elif (self.vertical_wall[y][decrement(x,1)] == 8):
                screen.blit(self.door2, (192,64))
            #hidden one way door from left
            elif (self.vertical_wall[y][decrement(x,1)] == 9):
                screen.blit(self.center2, (192,64))
            #switch on right side
            elif (self.vertical_wall[y][decrement(x,1)] == 12):
                screen.blit(self.switch2, (192,64))                                                               
            #switch on left side
            elif (self.vertical_wall[y][decrement(x,1)] == 13):
                screen.blit(self.center2, (192,64)) 

##            #draw straight one block wall right one
##            if (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 1):
##                screen.blit(self.center2, (448, 64))
##            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 2):
##                screen.blit(self.door2, (448,64))
##            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 3):
##                screen.blit(self.door2, (448,64))
##            #hidden door, with light it can see door
##            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 4):
##                screen.blit(self.center2, (448,64))
##            #one way door from right
##            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 6):
##                screen.blit(self.door2, (448,64))
##            #one way door from left
##            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 7):
##                screen.blit(self.center2, (448,64))
##            #hidden one way door from right
##            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 8):
##                screen.blit(self.door2, (448,64))
##            #hidden one way door from left
##            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 9):
##                screen.blit(self.center2, (448,64))
##            #switch on right side
##            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 12):
##                screen.blit(self.switch2, (448,64))                                                               
##            #switch on left side
##            elif (self.vertical_wall[decrement(y,1)][decrement(x,1)] == 13):
##                screen.blit(self.center2, (448,64)) 

            #draw up one wall on left
            if (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 1):
                screen.blit(self.edgeList2[0], (64, -64))
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 2):
                screen.blit(self.doorList2[0], (64, -64))
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 3):
                screen.blit(self.doorList2[0], (64, -64))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 4):
                screen.blit(self.edgeList2[0], (64, -64))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 6):
                screen.blit(self.edgeList2[0], (64, -64))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 7):
                screen.blit(self.doorList2[0], (64, -64))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 8):
                screen.blit(self.edgeList2[0], (64, -64))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 9):
                screen.blit(self.doorList2[0], (64, -64))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 12):
                screen.blit(self.edgeList2[0], (64, -64)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][decrement(x,1)] == 13):
                screen.blit(self.switchedgeList2[0], (64, -64)) 
                
            #draw up one wall on right
            if (self.horizontal_wall[y][decrement(x,1)] == 1):
                screen.blit(self.edgeList2[1], (448, -64))                
            elif (self.horizontal_wall[y][decrement(x,1)] == 2):
                screen.blit(self.doorList2[1], (448, -64))                
            elif (self.horizontal_wall[y][decrement(x,1)] == 3):
                screen.blit(self.doorList2[1], (448, -64))                
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][decrement(x,1)] == 4):
                screen.blit(self.edgeList2[1],  (448, -64))
            #one way door from right
            elif (self.horizontal_wall[y][decrement(x,1)] == 6):
                screen.blit(self.doorList2[1],  (448, -64))
            #one way door from left
            elif (self.horizontal_wall[y][decrement(x,1)] == 7):
                screen.blit(self.edgeList2[1],  (448, -64))
            #hidden one way door from right
            elif (self.horizontal_wall[y][decrement(x,1)] == 8):
                screen.blit(self.doorList2[1],  (448, -64))
            #hidden one way door from left
            elif (self.horizontal_wall[y][decrement(x,1)] == 9):
                screen.blit(self.edgeList2[1],  (448, -64))
            #switch on right side
            elif (self.horizontal_wall[y][decrement(x,1)] == 12):
                screen.blit(self.switchedgeList2[1],  (448, -64)) 
            #switch on left side
            elif (self.horizontal_wall[y][decrement(x,1)] == 13):
                screen.blit(self.edgeList2[1],  (448, -64)) 



            #draw left one up wall
            if (self.vertical_wall[increment(y,1)][x] == 1):
                screen.blit(self.center1, (-448,-64))
            elif (self.vertical_wall[increment(y,1)][x] == 2):
                screen.blit(self.door1, (-448,-64))
            elif (self.vertical_wall[increment(y,1)][x] == 3):
                screen.blit(self.door1, (-448,-64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[increment(y,1)][x] == 4):
                screen.blit(self.center1, (-448,-64))
            #one way door from right
            elif (self.vertical_wall[increment(y,1)][x] == 6):
                screen.blit(self.door1, (-448,-64))
            #one way door from left
            elif (self.vertical_wall[increment(y,1)][x] == 7):
                screen.blit(self.center1, (-448,-64))
            #hidden one way door from right
            elif (self.vertical_wall[increment(y,1)][x] == 8):
                screen.blit(self.door1, (-448,-64))
            #hidden one way door from left
            elif (self.vertical_wall[increment(y,1)][x] == 9):
                screen.blit(self.center1, (-448,-64))
            #switch on right side
            elif (self.vertical_wall[increment(y,1)][x] == 12):
                screen.blit(self.switch1, (-448,-64))                                                               
            #switch on left side
            elif (self.vertical_wall[increment(y,1)][x] == 13):
                screen.blit(self.center1, (-448,-64)) 

            #draw right one up wall
            if (self.vertical_wall[decrement(y,1)][x] == 1):
                screen.blit(self.center1, (576,-64))
            if (self.vertical_wall[decrement(y,1)][x] == 2):
                screen.blit(self.door1, (576,-64))
            if (self.vertical_wall[decrement(y,1)][x] == 3):
                screen.blit(self.door1, (576,-64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[decrement(y,1)][x] == 4):
                screen.blit(self.center1, (576,-64))
            #one way door from right
            elif (self.vertical_wall[decrement(y,1)][x] == 6):
                screen.blit(self.door1, (576,-64))
            #one way door from left
            elif (self.vertical_wall[decrement(y,1)][x] == 7):
                screen.blit(self.center1, (576,-64))
            #hidden one way door from right
            elif (self.vertical_wall[decrement(y,1)][x] == 8):
                screen.blit(self.door1, (576,-64))
            #hidden one way door from left
            elif (self.vertical_wall[decrement(y,1)][x] == 9):
                screen.blit(self.center1, (576,-64))
            #switch on right side
            elif (self.vertical_wall[decrement(y,1)][x] == 12):
                screen.blit(self.switch1, (576,-64))                                                               
            #switch on left side
            elif (self.vertical_wall[decrement(y,1)][x] == 13):
                screen.blit(self.center1, (576,-64)) 

            #draw just up wall
            if (self.vertical_wall[y][x] == 1):
                screen.blit(self.center1, (64,-64))
            elif (self.vertical_wall[y][x] == 2):
                screen.blit(self.door1, (64,-64))
            elif (self.vertical_wall[y][x] == 3):
                screen.blit(self.door1, (64,-64))
            #hidden door, with light it can see door
            elif (self.vertical_wall[y][x] == 4):
                screen.blit(self.center1, (64,-64))
            #one way door from right
            elif (self.vertical_wall[y][x] == 6):
                screen.blit(self.door1, (64,-64))
            #one way door from left
            elif (self.vertical_wall[y][x] == 7):
                screen.blit(self.center1, (64,-64))
            #hidden one way door from right
            elif (self.vertical_wall[y][x] == 8):
                screen.blit(self.door1, (64,-64))
            #hidden one way door from left
            elif (self.vertical_wall[y][x] == 9):
                screen.blit(self.center1, (64,-64))
            #switch on right side
            elif (self.vertical_wall[y][x] == 12):
                screen.blit(self.switch1, (64,-64))                                                               
            #switch on left side
            elif (self.vertical_wall[y][x] == 13):
                screen.blit(self.center1, (64,-64)) 

            #draw wall on left
            if (self.horizontal_wall[increment(y,1)][x] == 1):
                screen.blit(self.edgeList1[0], (-192, -320))
            elif (self.horizontal_wall[increment(y,1)][x] == 2):
                screen.blit(self.doorList1[0], (-192, -320))
            elif (self.horizontal_wall[increment(y,1)][x] == 3):
                screen.blit(self.doorList1[0], (-192, -320))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[increment(y,1)][x] == 4):
                screen.blit(self.edgeList1[0], (-192, -320))
            #one way door from right
            elif (self.horizontal_wall[increment(y,1)][x] == 6):
                screen.blit(self.edgeList1[0], (-192, -320))
            #one way door from left
            elif (self.horizontal_wall[increment(y,1)][x] == 7):
                screen.blit(self.doorList1[0], (-192, -320))
            #hidden one way door from right
            elif (self.horizontal_wall[increment(y,1)][x] == 8):
                screen.blit(self.edgeList1[0], (-192, -320))
            #hidden one way door from left
            elif (self.horizontal_wall[increment(y,1)][x] == 9):
                screen.blit(self.doorList1[0], (-192, -320))
            #switch on right side
            elif (self.horizontal_wall[increment(y,1)][x] == 12):
                screen.blit(self.edgeList1[0], (-192, -320)) 
            #switch on left side
            elif (self.horizontal_wall[increment(y,1)][x] == 13):
                screen.blit(self.switchedgeList1[0], (-192, -320)) 

            #draw wall on right
            if (self.horizontal_wall[y][x] == 1):
                screen.blit(self.edgeList1[1], (576, -320))
            elif (self.horizontal_wall[y][x] == 2):
                screen.blit(self.doorList1[1], (576, -320))
            elif (self.horizontal_wall[y][x] == 3):
                screen.blit(self.doorList1[1], (576, -320))
            #hidden door, with light it can see door
            elif (self.horizontal_wall[y][x] == 4):
                screen.blit(self.edgeList1[1],  (576, -320))
            #one way door from right
            elif (self.horizontal_wall[y][x] == 6):
                screen.blit(self.doorList1[1],  (576, -320))
            #one way door from left
            elif (self.horizontal_wall[y][x] == 7):
                screen.blit(self.edgeList1[1],  (576, -320))
            #hidden one way door from right
            elif (self.horizontal_wall[y][x] == 8):
                screen.blit(self.doorList1[1],  (576, -320))
            #hidden one way door from left
            elif (self.horizontal_wall[y][x] == 9):
                screen.blit(self.edgeList1[1],  (576, -320))
            #switch on right side
            elif (self.horizontal_wall[y][x] == 12):
                screen.blit(self.switchedgeList1[1],  (576, -320)) 
            #switch on left side
            elif (self.horizontal_wall[y][x] == 13):
                screen.blit(self.edgeList1[1],  (576, -320))

                
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


def calculate_thief_level(game_self):

    max_theif_level = 0

    for character in game_self.party.member:
        theif_level = 0

        if character.status[3] == 1 or character.status[4] == 1 or character.status[5] == 1 or character.status[6] == 1 or character.status[7] == 1 or character.status[8] == 1:
            continue
        
        #thiefs
        if character.job == 4 or character.job == 22 or character.job == 23 or character.job == 24:
            theif_level = int(character.level/3)+1
        #merchants
        elif character.job == 5 or character.job == 25 or character.job == 26 or character.job == 27:
            theif_level = int(character.level/4)
        else:
            theif_level = int(character.level/15)

        if theif_level > max_theif_level:
            max_theif_level = theif_level

    return max_theif_level

def calculate_merchant_level(game_self):

    max_merchant_level = 0

    for character in game_self.party.member:
        merchant_level = 0

        if character.status[3] == 1 or character.status[4] == 1 or character.status[5] == 1 or character.status[6] == 1 or character.status[7] == 1 or character.status[8] == 1:
            continue

        #merchants
        if character.job == 5 or character.job == 25 or character.job == 26 or character.job == 27:
            merchant_level = int(character.level/3)+1
        elif character.job == 4 or character.job == 22 or character.job == 23 or character.job == 24:
            merchant_level = int(character.level/4)
        else:
            merchant_level = int(character.level/15)

        if merchant_level > max_merchant_level:
            max_merchant_level = merchant_level
    return max_merchant_level

def draw_dungeon_ground( screen, picture_number , picture, draw_coordinate):
    #0=normal ground, 4 = turn table, 16,17,18,19 = moving ground to up, down, left, right
    if picture_number == 0 or picture_number == 4 or picture_number ==16 or picture_number ==17 or picture_number == 18 or picture_number == 19:
        screen.blit( picture, draw_coordinate)

#return item and price at end
def party_encount_item( give, floor ):

    to_do_item = []
    price = 0

    if give == True:

        if floor == 1:
            items = [1, 6, 100, 150, 200, 215, 250, 300, 350, 351, 400, 426, 500, 550]

            item_number = random.randint( 0, len(items)-1)
            to_do_item.append( items[item_number])

        elif floor == 2:

            items = [1, 6, 100, 150, 200, 215, 250, 300, 350, 351, 400, 426, 500, 550, 101, 151, 201, 251, 301, 401, 427, 501, 551, 600]

            item_number = random.randint( 0, len(items)-1)
            to_do_item.append( items[item_number])
            
        elif floor == 3:
            items = [1,4,5,6,600,601,602,603,604,605,606]

            item_number = random.randint( 0, len(items)-1)
            to_do_item.append( items[item_number])

        elif floor == 4:
            items = [1,2,4,5,6, 102, 152,202,216,252,302,352,402,502,552]

            item_number = random.randint( 0, len(items)-1)
            to_do_item.append( items[item_number])

        elif floor == 5:
            pass

    else:

        if floor == 1:
            items = [1, 6, 100, 150, 200, 215, 250, 300, 350, 351, 400, 426, 500, 550, 101, 151, 201, 251, 301, 401, 427, 501, 551, 600]

            item_number = random.randint( 0, len(items)-1)
            to_do_item.append( items[item_number])
            price = 1500

        elif floor == 2:

            items = [1, 6, 100, 150, 200, 215, 250, 300, 350, 351, 400, 426, 500, 550, 101, 151, 201, 251, 301, 401, 427, 501, 551, 600, 102, 152, 202, 216, 252, 302, 352, 402, 502, 552]

            item_number = random.randint( 0, len(items)-1)
            to_do_item.append( items[item_number])

            price = 2000

        elif floor == 3:
            items = [1, 4,5,6,600,601,602,603,604,605,606]

            item_number = random.randint( 0, len(items)-1)
            to_do_item.append( items[item_number])

            price = 4000

        elif floor == 4:
            items = [1,2, 4,5,6, 102, 152,202,216,252,302,352,402,502,552, 103, 153, 203, 253, 303, 353, 403, 503, 553]

            price = 2500

            item_number = random.randint( 0, len(items)-1)
            to_do_item.append( items[item_number])

        elif floor == 5:
            pass

    to_do_item.append(price)

    return to_do_item

    
