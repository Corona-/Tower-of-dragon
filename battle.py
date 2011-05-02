#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

import window
import enemy
import random
import math
import battle_command
import character
import item
import city

import battle_window
TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10

SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

MENU_MAX = 5


class Battle:

    INIT, COMMAND, BATTLE, END = 0, 1, 2, 3

    FIGHT, DEFEND, ITEM, CURSE, MAGIC, ESCAPE = 0, 1, 2 ,3 ,4, 5

    def __init__(self, enemy_data, floor):
        #initialize font
        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.battle_start_font = self.menu_font.render(u"何者かが現れた！", True, COLOR_WHITE)

        self.select_font = self.menu_font.render(u"行動：", True, COLOR_WHITE)

        self.battle_font = self.menu_font.render(u"戦う", True, COLOR_WHITE)
        self.defend_font = self.menu_font.render(u"防御", True, COLOR_WHITE)
        self.magic_font = self.menu_font.render(u"呪文", True, COLOR_WHITE)
        self.curse_font = self.menu_font.render(u"呪いを解く", True, COLOR_WHITE)
        self.item_font = self.menu_font.render(u"アイテム", True, COLOR_WHITE)
        self.escape_font = self.menu_font.render(u"逃げる", True, COLOR_WHITE)

        self.not_battle_font = self.menu_font.render(u"戦う", True, COLOR_GLAY)
        self.not_defend_font = self.menu_font.render(u"防御", True, COLOR_GLAY)
        self.not_magic_font = self.menu_font.render(u"呪文", True, COLOR_GLAY)
        self.not_curse_font = self.menu_font.render(u"呪いを解く", True, COLOR_GLAY)
        self.not_item_font = self.menu_font.render(u"アイテム", True, COLOR_GLAY)
        self.not_escape_font = self.menu_font.render(u"逃げる", True, COLOR_GLAY)

        self.encount_window = window.Window(Rect(210, 120, 190, 60))
        self.command_window = window.Window(Rect(360, 120, 260, 170))
        self.enemy_window = window.Window(Rect(10, 10, 620, 100))
        self.message_window = window.Window(Rect(210, 120, 190, 60))

        self.enemy_select_window = battle_window.Enemy_select_window(Rect(10, 10, 620, 100))
        
        self.first = 0

        self.state = self.INIT

        self.music = 0

        self.menu = self.FIGHT

        self.enemy_data = enemy_data

        #has all enemies in a group
        #stores until four groups and Back stores enemy in back row
        self.enemy_encount = select_enemy( self.enemy_data, floor)
        self.enemyList = self.enemy_encount[0]
        self.enemyListBack = self.enemy_encount[1]


        self.enemy_font = pygame.font.Font("ipag.ttf", 15)

        self.selected = 0

        self.party_movement = []
        self.enemy_movement = []
        self.total_movement = []

        #decides if damage is set or not
        self.damage_set = 0
        #actual damage
        self.damage = 0
        #number to need keyboard until next command comes up
        self.group_access = 0

        #decides for some probability
        self.probability = 0
        #decides if probability is set or not
        self.probability_set = 0

        #only do this once in the instruction
        self.check = 0

        #exp and gold gained by this battle
        self.exp = 0 
        self.gold = 0

        #if escape successed it would be 1
        self.escape_flag = 0

        self.target_font = ""
        self.target_group = []
        self.target_font_set = 0

        #if monster died, it needs to store name
        self.dead_set = 0
        self.dead_font = ""

        #if hit or miss is set or not
        self.hit_set = 0
        #if hit, = 1
        self.hit = 0
        self.offset = -1

        #image of the tomb
        self.tomb = pygame.image.load("Images/tomb.png").convert()
        self.tomb.set_colorkey(self.tomb.get_at((0,0)), RLEACCEL)

     
    def update(self):
        if self.state == self.COMMAND:
            if self.music == 0:
                pygame.mixer.music.load("BGM/hisyou.mp3")
                pygame.mixer.music.play(-1)
                self.music = 1

    def draw(self, game_self, screen):

        if self.state == self.INIT:
            if self.first == 0:
                encount_se = pygame.mixer.Sound("SE/thunder.wav")
                encount_se.play()
                self.first = 1
                pygame.mixer.music.stop()
                


            self.encount_window.draw(screen)
            
            screen.blit(self.battle_start_font, (230, 140))

        if self.state == self.COMMAND:
            game_self.party.draw(screen)
            self.command_window.draw(screen)
            self.enemy_window.draw(screen)

            self.enemy_select_window.draw(screen)

            if self.menu == self.FIGHT:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(370,185,100,30), 0)
            elif self.menu == self.DEFEND:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(370,215,100,30), 0)
            elif self.menu == self.ITEM:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(370,245,100,30), 0)            
            elif self.menu == self.CURSE:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(490,185,120,30), 0)            
            elif self.menu == self.MAGIC:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(490,215,120,30), 0)            
            elif self.menu == self.ESCAPE:
                pygame.draw.rect(screen, COLOR_GLAY, Rect(490,245,120,30), 0)            

            if self.selected < len(game_self.party.member):
                character_font = self.menu_font.render( game_self.party.member[self.selected].name, True, COLOR_WHITE)     
                screen.blit(character_font, ( 440, 140))


            this_character = game_self.party.member[ self.selected ]
  

            screen.blit(self.select_font, (380, 140))
            if character_attackable ( game_self, this_character):
                screen.blit(self.battle_font, (380, 190))
            else:
                screen.blit(self.not_battle_font, (380,190))

            screen.blit(self.defend_font, (380, 220))
            screen.blit(self.item_font, (380, 250))
           
            if this_character.job == 3 or this_character.job == 19 or this_character.job == 20 or this_character.job == 21:
                screen.blit(self.curse_font, (500, 190))
            else:
                screen.blit(self.not_curse_font, (500,190))

            screen.blit(self.magic_font, (500, 220))
            screen.blit(self.escape_font, (500, 250))
    
            #display the enemies names
            count = 0
            for group in self.enemyList:
                movable_count = count_movable( group)
                group_font = self.enemy_font.render( str(len(group))+group[0].name + " ("+str(movable_count)+")", True, COLOR_WHITE)
                screen.blit(group_font, (20, 20+count*20))
                count+=1
                
            count = 0
            for group in self.enemyListBack:
                movable_count = count_movable( group)
                group_font = self.enemy_font.render( str(len(group))+group[0].name + " ("+str(movable_count)+")", True, COLOR_WHITE)
                screen.blit(group_font, (340, 20+count*20))
                count+=1

        if self.state == self.BATTLE:

            battle_window = window.Window(Rect(10, 10, 620, 150))
            battle_window.draw(screen)

            battle_command = self.total_movement[0]
    

            battle_font1 = None
            battle_font2 = None
            battle_font3 = None
            battle_font4 = None

            #print battle_command.character.name + "　" + str(battle_command.target) + " " + str(battle_command.movement) + " " + str(battle_command.speed)

            target = battle_command.target

            if self.target_font_set == 0:
                if isinstance( battle_command.character, character.Character):
                    if target < 4:
                        self.target_font = self.enemyList[target][0].name
                        self.target_group = self.enemyList[target]
                    else:
                        self.target_font = self.enemyListBack[target][0].name
                        self.target_group = self.enemyListBack[target]
                else:
                    self.target_font = game_self.party.member[target].name
                    self.target_group = game_self.party.member
                self.target_font_set = 1

            #0 is normal attack
            if battle_command.movement == self.FIGHT:
                
                battle_font1 = battle_command.character.name + u"は" + self.target_font + u"を" + u"突き刺した"

                if self.hit_set == 0:
                    if isinstance( battle_command.character, character.Character):
                        #calculate hit or miss
                        str_bonus = calculate_str_bonus( battle_command.character )
                        level_bonus = calculate_level_bonus( battle_command.character )
                        equip_bonus = calculate_equip_str( battle_command.character )

                        accuracy = str_bonus + level_bonus + equip_bonus
                        
                        #offset is enemy group's attacking enemy
                        self.offset = random.randint(0, len(self.target_group)-1)
                    

                        accuracy_decision = 19 + battle_command.target - self.target_group[self.offset].ac - accuracy

                        if accuracy_decision < 0:
                            accuracy_ecision = 0

                        accuracy_total = int( (19- accuracy_decision)*5)

                        accuracy_probability = random.randint(1, 100)

                        if accuracy_probability < accuracy_total:
                            self.hit = 1
                        else:
                            self.hit = 0
                    else:

                        accuracy1 = 19 - self.target_group[target].ac - battle_command.character.level
                        accuracy2 = accuracy1 - battle_command.character.ac

                        if accuracy1 < 0:
                            accuracy1 = 0

                        accuracy_total = int( (19-accuracy1)*5)

                        accuracy_probability = random.randint(1,100)

                        if accuracy_probability < accuracy_total:
                            self.hit = 1
                        else:
                            self.hit = 0
                    self.hit_set = 1


                if self.hit == 1:    
                
                    #print battle_font1
                    #calculate hit times
                    hit_times = calculate_hit_time(battle_command.character)

                    battle_font2 = str(hit_times) + u"回当たり "

                    #calculate damage
                    if (self.damage_set == 0):
                        self.damage = calculate_damage(battle_command.character)
                        self.damage_set = 1
                        #need to select target on enemy in random
                        if isinstance( self.target_group[0], character.Character):
                            self.target_group[target].hp -= self.damage
                            if self.target_group[target].hp <= 0:
                                self.target_group[target].hp = 0
                                self.target_group[target].status = "DEAD"
                                self.target_group[target].rip += 1
                                temp = self.target_group[target]
                                self.dead_set = 1
                                self.dead_font = self.target_group[target].name
                                #delete command of dead person
                                i = 0
                                for command in self.total_movement:
                                    if isinstance(command.character, character.Character):
                                        if self.target_group[target] == command.character:
                                            print command.character.name
                                            del self.total_movement[i]
                                    i+=1


                                i = 0
                                to_delete = []
                                for command in self.total_movement:
                                    if isinstance(command.character, enemy.Enemy):
                                        if target == command.target:
                                            if i!= 0:
                                                to_delete.insert(0,i)                                        
                                        i+=1
                                    
                                for i in to_delete:
                                    del self.total_movement[i]
                                for i in self.total_movement:
                                    print i.character.name
                                
                                        
                                #move the person to end of party
                                del self.target_group[target]
                                self.target_group.append(temp)


                                
                        else:
                            self.target_group[self.offset].hp -= self.damage
                            if self.target_group[self.offset].hp <= 0:
                                self.exp += self.target_group[self.offset].exp
                                self.gold += self.target_group[self.offset].drop_gold
                                battle_command.character.marks += 1

                                #delete command of the dead enemy
                                i=0
                                for command in self.total_movement:
                                    if isinstance(command.character, enemy.Enemy):
                                        if self.target_group[self.offset] == command.character:
                                            del self.total_movement[i]
                                    i+=1
     
                                del self.target_group[self.offset]

                                #delete command of party targeted at thoses enemy
                                if self.target_group == []:                                
                                    i = 0

                                    to_delete = []
                                    for command in self.total_movement:
                                        if isinstance(command.character, character.Character):
                                            if target == command.target:
                                                #first one would be deleted at end of command so ignore
                                                if i != 0:
                                                    to_delete.insert(0,i)                                            
                                        i+=1
                                    
                                    for i in to_delete:
                                        del self.total_movement[i]
                                    
                                    del self.enemyList[target]

                                self.dead_set = 1
                                self.dead_font = self.target_font

                        
                    battle_font2 += str(self.damage) + u"のダメージ"

                    if self.dead_set == 1:                    
                        battle_font3 = self.dead_font + u"は死んだ！"
                else:
                    battle_font2 = u"だが外れた！"

            if battle_command.movement == self.DEFEND:
                battle_font1 = battle_command.character.name + u"は" + u"身を守っている"
               
            if battle_command.movement == self.ITEM:
                pass
            if battle_command.movement == self.CURSE:
                battle_font1 = battle_command.character.name + u"は" + self.target_font + u"の呪いを解いた"

                if self.check == 0:
                    self.group_access = len(self.target_group)
                    self.check = 1


                if self.probability_set == 0:
                    self.probability = random.randint(1,100)
                    self.probability_set = 1
                    #category 1 is undead
                    if self.target_group[0].category != 1:
                        self.probability = 0

                    #TO-DO set the probability
                    if self.probability >= 50:
                        del self.target_group[ len(self.target_group)-self.group_access]

                #only set the font
                if self.probability < 50:
                    #nothing happens
                    battle_font2 = self.target_font + u"は影響が無い"
                else:
                    battle_font2 = self.target_font + u"は成仏した"
                    #enemy dissapears
                    
            if battle_command.movement == self.MAGIC:
                pass
            if battle_command.movement == self.ESCAPE:
                battle_font1 = battle_command.character.name + u"は" + u"逃げ出した"
                if self.probability_set == 0:
                    self.probability = random.randint(1, 100)
                    self.probability_set = 1
                #TO-DO calculate escape probability
                if self.probability < 10:
                    self.escape_flag = 1
                else:            
                    battle_font3 = u"しかし逃げられなかった"
            
            if battle_font1 != None:
                battle_font1 = self.menu_font.render( battle_font1, True, COLOR_WHITE)
                screen.blit(battle_font1, ( 320 - battle_font1.get_width()/2, 20))

            if battle_font2 != None:
                battle_font2 = self.menu_font.render( battle_font2, True, COLOR_WHITE)
                screen.blit(battle_font2, ( 320 - battle_font2.get_width()/2, 50))

            if battle_font3 != None:
                battle_font3 = self.menu_font.render( battle_font3, True, COLOR_WHITE)
                screen.blit(battle_font3, ( 320 - battle_font3.get_width()/2, 80))

            if battle_font4 != None:
                battle_font4 = self.menu_font.render( battle_font4, True, COLOR_WHITE)
                screen.blit(battle_font4, ( 320 - battle_font4.get_width()/2, 110))

        if self.state == self.END:

            if player_count_movable ( game_self.party.member ) == 0:
                #game over just show image of tomb

                screen.fill( COLOR_WHITE)

                if len(game_self.party.member) >=1:
                    screen.blit(self.tomb, (230, 40))
                    name_font = self.menu_font.render( game_self.party.member[0].name, True, COLOR_BLACK)
                    screen.blit( name_font, (294 - name_font.get_width()/2, 180))
                if len(game_self.party.member) >=2:
                    screen.blit(self.tomb, (50,300))
                    name_font = self.menu_font.render( game_self.party.member[1].name, True, COLOR_BLACK)
                    screen.blit( name_font, (114 - name_font.get_width()/2, 440))
                if len(game_self.party.member) >=3:
                    screen.blit(self.tomb, (410,310))
                    name_font = self.menu_font.render( game_self.party.member[2].name, True, COLOR_BLACK)
                    screen.blit( name_font, (474 - name_font.get_width()/2, 450))                
                if len(game_self.party.member) >=4:
                    screen.blit(self.tomb, (230,290))
                    name_font = self.menu_font.render( game_self.party.member[3].name, True, COLOR_BLACK)
                    screen.blit( name_font, (294 - name_font.get_width()/2, 430))
                if len(game_self.party.member) >=5:
                    screen.blit(self.tomb, (50,50))
                    name_font = self.menu_font.render( game_self.party.member[4].name, True, COLOR_BLACK)
                    screen.blit( name_font, (114 - name_font.get_width()/2, 190))
                if len(game_self.party.member) >=6:
                    screen.blit(self.tomb, (410, 60))
                    name_font = self.menu_font.render( game_self.party.member[5].name, True, COLOR_BLACK)
                    screen.blit( name_font, (474 - name_font.get_width()/2, 200))


            if self.enemyList == [] and self.enemyListBack == []:
                battle_window = window.Window(Rect(10, 10, 620, 150))
                battle_window.draw(screen)

                count = 0
                for member in game_self.party.member:
                    if member.status == "OK" or member.status == "POISON" or member.status == "PALSY":
                        count+= 1


                exp_font = u"生き残ったメンバーは " + str(int(math.ceil(self.exp/count))) + "EXPを得た"
                gold_font = u"生き残ったメンバーは " + str(int(math.ceil(self.gold/count))) + "TPを手に入れた"

                exp_font = self.menu_font.render( exp_font, True, COLOR_WHITE)
                gold_font = self.menu_font.render( gold_font, True, COLOR_WHITE)
            
                screen.blit(exp_font, ( 320 - exp_font.get_width()/2, 50))
                screen.blit(gold_font, ( 320 - gold_font.get_width()/2, 90))

                #drop item


                  
    def battle_handler(self, game_self, event):
        
        if self.enemy_select_window.is_visible == True:
            self.enemy_select_window.enemy_select_window_handler( game_self, event)
            if self.selected == player_count_movable(game_self.party.member):
                self.state = self.BATTLE

                self.enemy_movement = enemy_movement( self.enemyList, self.enemyListBack, game_self)

                for element in self.party_movement:
                    self.total_movement.append(element)
                for element in self.enemy_movement:
                    self.total_movement.append(element)

                #sort the elements by speed, highest first
                self.total_movement.sort(cmp=lambda x, y: cmp(x.speed,y.speed), reverse=True)                

            return
        

        if self.state == self.INIT:
            if event.type == KEYUP and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN or event.key == K_x):
                self.state = self.COMMAND

            return



        elif self.state == self.COMMAND:

            print self.selected

            if event.type == KEYUP and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):

                game_self.select_se.play()
                
                character = game_self.party.member[ self.selected ]
                
                if self.menu == self.FIGHT:


                    check = character_attackable ( game_self, character )

                    if check == True:
                        self.enemy_select_window.is_visible = True
                    else:
                        pass

                    return

                    
                if self.menu == self.DEFEND:
                    self.party_movement.append( battle_command.Battle_command( character, self.DEFEND, 0))
                    self.selected += 1
                if self.menu == self.ITEM:
                    return
                if self.menu == self.CURSE:
                    #only priests could select
                    if character.job == 3 or character.job == 19 or character.job == 20 or character.job ==21:
                        self.enemy_select_window.is_visible = True

                    return
                if self.menu == self.MAGIC:
                    return
                if self.menu == self.ESCAPE:
                    self.party_movement.append( battle_command.Battle_command( character, self.ESCAPE, 0))
                    self.selected+=1               

                #need to do something for sleep
                if self.selected == player_count_movable(game_self.party.member):
                    self.state = self.BATTLE

                    self.enemy_movement = enemy_movement( self.enemyList, self.enemyListBack, game_self)

                    for element in self.party_movement:
                        self.total_movement.append(element)
                    for element in self.enemy_movement:
                        self.total_movement.append(element)

                    #sort the elements by speed, highest first
                    self.total_movement.sort(cmp=lambda x, y: cmp(x.speed,y.speed), reverse=True)


                #check if next character is attackable and set the menu to its original position
                #if enemy_Select_window is open, this should not be called
                next_character = None
                if self.selected >= len(game_self.party.member):
                    next_character = game_self.party.member[0]
                else:
                    next_character = game_self.party.member[ self.selected ]

                check = character_attackable ( game_self, next_character )

                if check == True:
                    self.menu = self.FIGHT
                else:
                    self.menu = self.DEFEND
                

                return
            
            if event.type == KEYUP and event.key == K_UP: #moves the cursor up
                game_self.cursor_se.play()
                self.menu -= 1
                if self.menu == self.ITEM:
                    self.menu = MENU_MAX
                if self.menu < 0:
                    self.menu = self.ITEM

            elif event.type == KEYUP and event.key == K_DOWN:
                game_self.cursor_se.play()
                self.menu += 1
                if self.menu % 3 == 0:
                    self.menu -= 3

            elif event.type == KEYUP and event.key == K_LEFT:
                game_self.cursor_se.play()
                self.menu -= 3
                if self.menu < 0:
                    self.menu += MENU_MAX+1

            elif event.type == KEYUP and event.key == K_RIGHT:
                game_self.cursor_se.play()
                self.menu += 3
                if self.menu > MENU_MAX:
                    self.menu = self.menu % (MENU_MAX+1)


            if event.type == KEYUP and event.key == K_x:
                if self.selected > 0:
                    self.selected -= 1
                    count = len(self.party_movement)
                    print count
                    del (self.party_movement[count-1])
                else:
                    #to end battle
                    game_self.dungeon.battle_flag = 0
                    game_self.dungeon.battle = None
                    game_self.dungeon.music = 0


        elif self.state == self.BATTLE:

            if event.type == KEYUP and (event.key == K_x or event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
                #game_self.dungeon.battle_flag = 0
                #game_self.dungeon.battle = None
                #ugame_self.dungeon.music = 0

                if self.escape_flag == 1:
                    game_self.dungeon.battle_flag = 0
                    game_self.dungeon.battle = None
                    game_self.dungeon.music = 0
                    self.party_movement = []
                    self.enemy_movement = []
                    self.total_movement = []
                    self.menu = self.FIGHT
                    self.selected = 0
                    self.probability_set = 0
                    self.damage_set = 0
                    self.check = 0
                    self.escape_flag = 0
                    self.target_font_set = 0
                    self.dead_set = 0
                    self.hit_set = 0
                    return

                if self.group_access > 0:
                    self.group_access -= 1
                    self.probability_set = 0
                    self.dead_set = 0
                    self.hit_set = 0


                if self.enemyList == [] and self.enemyListBack == []:
                    self.state = self.END
                    return
                    #this is for battle end

                if player_count_movable( game_self.party.member)== 0:
                    self.state = self.END
                    return
                    #game_over
            



                if self.group_access == 0:
                    del self.total_movement[0]
                    self.damage_set = 0
                    self.probability_set = 0
                    self.check = 0
                    self.target_font_set = 0
                    self.dead_set = 0
                    self.hit_set = 0



                    if self.total_movement == []:
                        self.party_movement = []
                        self.enemy_movement = []
                        self.menu = self.FIGHT
                        self.selected = 0
                        self.state = self.COMMAND

        elif self.state == self.END:
            
            if event.type == KEYUP and (event.key == K_x or event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):

                if player_count_movable( game_self.party.member ) == 0:
                    #game_over
                
                    game_self.dungeon.battle_flag = 0
                    game_self.dungeon.battle = None
                    game_self.dungeon.music = 0

                    for character in game_self.party.member:
                        game_self.dungeon_characters.append( character)

                    game_self.party.member = []

                    game_self.game_state = CITY
                    game_self.dungeon = None
                    game_self.city = city.City()
                else:
                    #win
                                        
                    game_self.dungeon.battle_flag = 0
                    game_self.dungeon.battle = None
                    game_self.dungeon.music = 0

                    count = 0
                    for character in game_self.party.member:
                        if character.status == "OK" or character.status == "POISON" or character.status == "PALSY":
                            count+= 1


                    for character in game_self.party.member:
                        if character.status == "OK" or character.status == "POISON" or character.status == "PALSY":                    
                            character.exp += int(math.ceil(self.exp/count))
                            character.money += int(math.ceil(self.gold/count))
                    pass




def count_movable( enemy_group ):

    movable_count = 0
    for enemy_status in enemy_group:
        if enemy_status.status == "OK" or enemy_status.status == "POISON":
            movable_count += 1
    return movable_count

#used by monster selecting target
def player_count_movable ( player_group):
    movable_count = 0
    for player in player_group:
        if player.status == "OK" or player.status == "POISON" or player.status == "SLEEP":
            movable_count += 1
    return movable_count


def select_enemy( enemy_data, floor ):

    enemy_total = []
    enemy_front = []
    enemy_back = []
    
    if floor == 1:

        enemy_id = random.randint(1,3)

        enemy_count = random.randint(1,3)

        #has enemies of a group
        enemy_group = []

        for i in range(enemy_count):
            enemy_group.append( enemy.Enemy(enemy_data[ enemy_id ] ) )

        enemy_front.append(enemy_group)

        enemy_total.append(enemy_front)
        enemy_total.append(enemy_back)


    return enemy_total
            

def calculate_hit_time( chara ):

    hit_time = 1

    return hit_time

def calculate_damage( chara):

    damage = 0

    if isinstance( chara, character.Character):
        damage = 0
        if isinstance( chara.equip[0], item.Item):
            damage += chara.equip[0].power
        if isinstance( chara.equip[1], item.Item):
            damage += chara.equip[1].power

        if damage == 0:
            damage = 4

        if chara.strength >= 16:
            damage += chara.strength-15

    if isinstance( chara,enemy.Enemy):
        damage = chara.strength

    damage = random.randint(1, damage)

    return damage


def enemy_movement( enemyList, enemyListBack, game_self):

    enemy_command = []

    for group in enemyList:
        for enemy in group:
            if enemy.status == "OK" or enemy.status == "POISON":
                movement = random.randint(1,100)
                player_movable = player_count_movable(game_self.party.member)
                
                if enemy.extra_attack != []:
                    if movement < enemy.extra_attack[0]:
                        if enemy.extra_attack[2] == 1:
                            if player_movable > 3:
                                target = random.randint(0, 2)
                            else:
                                target = random.randint(0, player_movable-1)
                        if enemy.extra_attack[2] == 2:
                            target = random.randint(0, player_movable-1)                  
                        if enemy.extra_attack[2] == 3:
                            target = random.randint(0, player_movable-1)
                        
                        enemy_command.append( battle_command.Battle_command( enemy, 0, target))
                    elif movement < enemy.extra_attack[4]:
                        if enemy.extra_attack[6] == 1:
                            if player_movable > 3:
                                target = random.randint(0,2)
                            else:
                                target = random.randint(0, player_movable-1)
                        if enemy.extra_attack[6] == 2:
                            target = random.randint(0, player_movable-1)                  
                        if enemy.extra_attack[6] == 3:
                            target = random.randint(0, player_movable-1)
                        enemy_command.append( battle_command.Battle_command( enemy, 3, target))
                    elif movement < enemy.extra_attack[8]:
                        if enemy.extra_attack[10] == 1:
                            if player_movable > 3:
                                target = random.randint(0,2)
                            else:
                                target = random.randint(0, player_movable-1)
                        if enemy.extra_attack[10] == 2:
                            target = random.randint(0, player_movable-1)                  
                        if enemy.extra_attack[10] == 3:
                            target = random.randint(0, player_movable-1)
                        enemy_command.append( battle_command.Battle_command( enemy, 6, target))
                    elif movement < enemy.extra_attack[12]:
                        if enemy.extra_attack[14] == 1:
                            if player_movable > 3:
                                target = random.randint(0,2)
                            else:
                                target = random.randint(0, player_movable-1)
                        if enemy.extra_attack[14] == 2:
                            target = random.randint(0, player_movable-1)                  
                        if enemy.extra_attack[14] == 3:
                            target = random.randint(0, player_movable-1)
                        enemy_command.append( battle_command.Battle_command( enemy, 9, target))
                else:
                    if enemy.attack_range == 0:
                        if player_movable > 3:
                            target = random.randint(0,2)
                        else:
                            target = random.randint(0, player_movable-1)
                    enemy_command.append( battle_command.Battle_command( enemy, 0, target))

    for group in enemyListBack:
        for enemy in group:
            if enemy.status == "OK":
                movement = random.randint(1,100)
                player_movable = player_count_movable(game_self.party.member)

                if enemy.extra_attack != []:
                    if movement < enemy.extra_attack[0]:
                        if enemy.extra_attack[2] == 1:
                            if player_movable > 3:
                                target = random.randint(0, 2)
                            else:
                                target = random.randint(0, player_movable-1)
                        if enemy.extra_attack[2] == 2:
                            target = random.randint(0, player_movable-1)                  
                        if enemy.extra_attack[2] == 3:
                            target = random.randint(0, player_movable-1)
                        
                        enemy_command.append( battle_command.Battle_command( enemy, 0, target))
                    elif movement < enemy.extra_attack[4]:
                        if enemy.extra_attack[6] == 1:
                            if player_movable > 3:
                                target = random.randint(0,2)
                            else:
                                target = random.randint(0, player_movable-1)
                        if enemy.extra_attack[6] == 2:
                            target = random.randint(0, player_movable-1)                  
                        if enemy.extra_attack[6] == 3:
                            target = random.randint(0, player_movable-1)
                        enemy_command.append( battle_command.Battle_command( enemy, 3, target))
                    elif movement < enemy.extra_attack[8]:
                        if enemy.extra_attack[10] == 1:
                            if player_movable > 3:
                                target = random.randint(0,2)
                            else:
                                target = random.randint(0, player_movable-1)
                        if enemy.extra_attack[10] == 2:
                            target = random.randint(0, player_movable-1)                  
                        if enemy.extra_attack[10] == 3:
                            target = random.randint(0, player_movable-1)
                        enemy_command.append( battle_command.Battle_command( enemy, 6, target))
                    elif movement < enemy.extra_attack[12]:
                        if enemy.extra_attack[14] == 1:
                            if player_movable > 3:
                                target = random.randint(0,2)
                            else:
                                target = random.randint(0, player_movable-1)
                        if enemy.extra_attack[14] == 2:
                            target = random.randint(0, player_movable-1)                  
                        if enemy.extra_attack[14] == 3:
                            target = random.randint(0, player_movable-1)
                        enemy_command.append( battle_command.Battle_command( enemy, 9, target))
                else:
                    pass
                    #if range is 0, it cannot reach character so do not yet.
                    #if enemy.attack_range == 0:
                    #    if len(game_self.party.member) > 3:
                    #        target = random.randint(0,2)
                    #    else:
                    #        target = random.randint(0, len(game_self.party.member)-1)
                    #enemy_command.append( battle_command.Battle_command( enemy, 10, target))

                
    return enemy_command


def calculate_str_bonus(character):

    if character.strength > 15:
        return character.strength - 15
    elif character.strength > 5:
        return 0
    else:
        return character.strength-6


    WARRIOR, FIGHTER, MAGICIAN, PRIEST, THIEF, MERCHANT = 0, 1, 2, 3, 4, 5
    LORD, SWORDMASTER, MADOVERLORD = 10,11,12
    MASTERSWORDSMAN, GENERAL, MURDERER = 13,14,15
    RUNESWORDSMAN, SAGE, SORCERER = 16,17,18
    POPE, BISHOP, FANATIC = 19,20,21
    CHIVALROUSTHIEF, PHANTOMTHIEF, NINJA = 22,23,24
    GUILDMASTER, ARMEDMERCHANT, MONEYLENDER = 25, 26,27

def calculate_level_bonus(character):

    if character.job == 0 or character.job == 3:
        return int(character.level/3) + 1

    elif character.job == 1:
        return int(character.level/3) + 2

    elif character.job == 2 or character.job == 4 or character.job == 5:
        return int(character.level/5)

    elif character.job == 10 or character.job == 11 or character.job == 12:
        return int(character.level/3) + 2
        
    elif character.job == 13 or character.job == 14 or character.job == 15:
        return int(character.level/2)
    
    elif character.job == 17 or character.job == 18:
        return int(character.level/5)
        
    elif character.job == 16 or character.job == 19 or character.job == 20 or character.job == 21:
        return int(character.level/3) + 1
    
    elif character.job == 22 or character.job == 23 or character.job == 24:
        return int(character.level/3) + 2
    
    elif character.job == 25 or character.job == 26 or character.job == 27:
        return int(character.level/3) + 1

def calculate_equip_str(character):

    total = 0
    for equip in character.equip:
        if isinstance( equip, item.Item):
            total += equip.strength

    return total

def calculate_character_distance( game_self, character ):

    count = 0

    for chara in game_self.party.member:
        if character == chara:
            break
        count += 1

    if count < 3:
        return 0
    else:
        return 1
        
        
def character_attackable ( game_self, character ):

    distance = calculate_character_distance( game_self, character)

    if isinstance ( character.equip[0], item.Item):
        if distance == 1 and character.equip[0].range > 1:
            return True
        if distance == 0:
            return True
    else:
        if distance == 1:
            return False
        else:
            return True
