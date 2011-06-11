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
import system_notify
import party
import string

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
    ENEMY_EXTRA = 6

    def __init__(self, enemy_data, floor):
        #initialize font
        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.battle_start_font = self.menu_font.render(u"何者かが現れた！", True, COLOR_WHITE)
        self.enemy_start_font = self.menu_font.render(u"いきなり襲い掛かってきた！", True, COLOR_WHITE)
        self.party_start_font = self.menu_font.render(u"まだこちらに気付いていない！", True, COLOR_WHITE)

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
        self.special_battle_window = window.Window(Rect(170, 120, 310, 60))
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

        #store enemy for drop items
        self.enemy_drop_items = []

        #if this is changed, event battle also needs change
        #take probability (drop% * number of enemy)
        #and if random value is less than that, add it to drop item
        for enemy_group in self.enemyList:
            i = 0
            probability = 0
            for item in enemy_group[0].drop_item:
                if i%2==0:
                    probability = item*len(enemy_group)
                    i+= 1
                    continue

                random_value = random.randint(1,100)
                if random_value < probability:
                    self.enemy_drop_items.append(item)
                i += 1

        for enemy_group in self.enemyListBack:
            i = 0
            probability = 0
            for item in enemy_group[0].drop_item:
                if i%2==0:
                    probability = item*len(enemy_group)
                    i+=1
                    continue

                random_value = random.randint(1,100)
                if random_value < probability:
                    self.enemy_drop_items.append(item)
                i += 1

        self.enemy_font = pygame.font.Font("ipag.ttf", 15)

        self.selected = 0

        self.party_movement = []
        self.enemy_movement = []
        self.total_movement = []

        #decides if damage is set or not
        self.damage_set = 0
        #actual damage
        self.damage = 0
        #number to need keyboard access until next command comes up
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

        #number of times player need to press key to get away from battle
        #shows drop item gained from battle
        self.drop_item_key = int(math.ceil(len(self.enemy_drop_items)/4.0))

        #extra window to show magic and items
        self.magic_window = None
        self.item_view = None

        #group selection of many groups
        self.group_selection = 0

        #if event battle, party cannot escape
        self.event_battle = 0

        self.first_attack = 0
        self.extra_key = 0

        probability = random.randint(1,100)
        if probability <= 10:
            #party attack first
            self.first_attack = 1
            self.extra_key = 2
        elif probability > 90:
            #enemy attack first
            self.first_attack = -1
            self.extra_key = 2
     
    def update(self):
        if self.state == self.COMMAND:
            if self.music == 0:
                pygame.mixer.music.load("BGM/hisyou.mp3")
                pygame.mixer.music.play(-1)
                self.music = 1

    def draw(self, game_self, screen):

        if self.state == self.INIT:

            self.battle_initiation(game_self, screen)

        if self.state == self.COMMAND:

            self.draw_command_windows(game_self, screen)

            self.draw_command_selection(game_self, screen)

            self.draw_battle_command(game_self, screen)

            self.draw_enemy_names(game_self, screen)

            if self.magic_window != None:
                self.magic_window.draw(screen, game_self)

            if self.item_view != None:
                self.item_view.draw(screen, game_self)
        

        if self.state == self.BATTLE:

            battle_window = window.Window(Rect(10, 10, 620, 150))
            battle_window.draw(screen)

            battle_command = self.total_movement[0]
    

            battle_font1 = None
            battle_font2 = None
            battle_font3 = None
            battle_font4 = None

            target = battle_command.target

            if self.target_font_set == 0:

                print battle_command.character.name
                if isinstance( battle_command.character, character.Character) and battle_command.magic_target == None:

                    if target < 4:
                        self.target_font = self.enemyList[target][0].name
                        self.target_group = self.enemyList[target]
                    else:
                        self.target_font = self.enemyListBack[target-4][0].name
                        self.target_group = self.enemyListBack[target-4]

                elif isinstance(battle_command.character, character.Character) and battle_command.magic_target != None and string.count(battle_command.magic_target, "ENEMY"):

                    if target < 4:
                        self.target_font = self.enemyList[target][0].name
                        self.target_group = self.enemyList[target]
                    else:
                        self.target_font = self.enemyListBack[target-4][0].name
                        self.target_group = self.enemyListBack[target-4]
  
                elif isinstance( battle_command.character, character.Character) and (battle_command.magic_target != None and string.count(battle_command.magic_target, "PARTY")):
                    self.target_font = game_self.party.member[target].name
                    self.target_group = game_self.party.member
                #still need to find out what to do for enemy's extra attack   
                else:
                    if isinstance( battle_command.character, enemy.Enemy) and (battle_command.magic_target != None and string.count(battle_command.magic_target, "ENEMY")):
                        print "ENEMY SPECIAL TO ENEMY"
                        print battle_command.target
                        if battle_command.target < len(self.enemyList):
                            self.target_font = self.enemyList[target][0].name
                            self.target_group = self.enemyList[target]
                        else:
                            self.target_font = self.enemyListBack[target-len(self.enemyList)][0].name
                            self.target_group = self.enemyListBack[target-len(self.enemyList)]
                    else:
                        self.target_font = game_self.party.member[target].name
                        self.target_group = game_self.party.member

                #if target need to be self party, it needs its own group
                
                self.target_font_set = 1

            #0 is normal attack
            if battle_command.movement == self.FIGHT:
                
                battle_font1 = battle_command.character.name + u"は" + self.target_font + u"を" + u"突き刺した"

                if self.hit_set == 0:
                    self.hit = 0
                    if isinstance( battle_command.character, character.Character):
                        #calculate hit or miss
                        str_bonus = calculate_str_bonus( battle_command.character )
                        level_bonus = calculate_level_bonus( battle_command.character )
                        equip_bonus = calculate_equip_str( battle_command.character )

                        accuracy = str_bonus + level_bonus + equip_bonus
                        
                        #offset is enemy group's attacking enemy
                        self.offset = 0 #random.randint(0, len(self.target_group)-1)
                    

                        accuracy_decision = 19 + battle_command.target - self.target_group[self.offset].ac - accuracy

                        if accuracy_decision < 0:
                            accuracy_decision = 0

                        accuracy_total = int( (19- accuracy_decision)*5)
                        
                        hit_times = calculate_hit_time(battle_command.character)

                        for attack in range(hit_times):
                            accuracy_probability = random.randint(1,100)
                            if accuracy_probability < accuracy_total:
                                self.hit += 1
                                
                    else:

                        accuracy1 = 19 - party.calculate_ac(self.target_group[target]) - battle_command.character.level
                        accuracy2 = accuracy1 - battle_command.character.ac

                        if accuracy1 < 0:
                            accuracy1 = 0

                        accuracy_total = int( (19-accuracy1)*5)

                        for attack in range(battle_command.character.attack_times):
                            accuracy_probability = random.randint(1,100)
                            if accuracy_probability < accuracy_total:
                                self.hit += 1

                    self.hit_set = 1


                if self.hit >= 1:    

                    battle_font2 = str(self.hit) + u"回当たり "

                    #calculate damage
                    if (self.damage_set == 0):
                        self.damage = calculate_damage(battle_command.character, self.hit)
                        self.damage_set = 1

                        if self.target_group[0].status[3] == 1 or self.target_group[0].status[4] == 1 or self.target_group[0].status[5] == 1:
                            self.damage*=2

                        #subtract damage and if hp < 0, remove that character
                        if isinstance( self.target_group[0], character.Character):
                            self.target_group[target].hp -= self.damage

                            self.character_dead()
                                
                        else:
                            self.target_group[self.offset].hp -= self.damage

                            self.enemy_dead(self.offset)
                        
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
                        self.probability = 100


                    #subtract damage and if hp < 0, remove that character
                    if self.probability < 50 and isinstance( self.target_group[0], character.Character):
                        self.character_dead()
                            
                    elif self.probability < 50 and isinstance( self.target_group[0], enemy.Enemy):

                        offset = len(self.target_group)-self.group_access
                        target = battle_command.target
                        self.gold += self.target_group[offset].drop_gold
                        battle_command.character.marks += 1
                        
                        #delete command of the dead enemy
                        i=0
                        for command in self.total_movement:
                            if isinstance(command.character, enemy.Enemy):
                                if self.target_group[offset] == command.character:
                                    del self.total_movement[i]
                            i+=1

                        del self.target_group[offset]

                        #delete command of party targeted at those enemy
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
                            
                            #del self.enemyList[target]

                        self.dead_set = 1
                        self.dead_font = self.target_font

                #only set the font
                if self.dead_set != 1:
                    #nothing happens
                    battle_font2 = self.target_font + u"は影響が無い"
                else:
                    battle_font2 = self.target_font + u"は成仏した"
                    #enemy dissapears
                    
            if battle_command.movement == self.MAGIC:

                #magician magic
                if battle_command.magic_level == 0:
                    if battle_command.magic_number == 0:
                        battle_font1 = battle_command.character.name + u"はエナジーアローを唱えた"

                        if self.damage_set == 0:
                            
                            self.damage = random.randint(1, 8)
                            self.damage = int(self.damage*math.floor(self.target_group[0].none_resistance/100.0))

                            probability = random.randint(1,100)
                            if probability < self.target_group[0].magic_resistance:
                                self.damage = -1

                            self.damage_set = 1

                            battle_command.character.magician_mp[0] -= 1


                            #subtract damage and if hp < 0, remove that character
                            if isinstance( self.target_group[0], character.Character):
                                self.target_group[target].hp -= self.damage

                                self.character_dead()
                                    
                            else:
                                self.target_group[self.offset].hp -= self.damage

                                self.enemy_dead(self.offset)


                        if self.damage != -1:
                            battle_font2 = self.target_font + u"に" + str(self.damage) + u"のダメージ"
                        else:
                            battle_font2 = self.target_font + u"は呪文を妨害した！"

                        if self.dead_set == 1:                    
                            battle_font3 = self.dead_font + u"は死んだ！"

                    elif battle_command.magic_number == 1:
                        battle_font1 = battle_command.character.name + u"はスリープを唱えた"

                        if self.check == 0:
                            self.group_access = len(self.target_group)
                            battle_command.character.magician_mp[0] -= 1
                            self.check= 1

                        if self.damage_set == 0:

                            self.damage_set = 1

                            self.damage = 1
                            
                            probability = random.randint(1,100)
                            if probability < self.target_group[len(self.target_group)-self.group_access].magic_resistance:
                                self.damage = 0

                            probability = random.randint(1,100)
                            if probability < self.target_group[len(self.target_group)-self.group_access].sleep_resistance:
                                self.damage = -1

                            if self.damage == 1:
                                self.target_group[len(self.target_group)-self.group_access].status[3] = 1

                                #delete command of the slept enemy
                                i=0
                                for command in self.total_movement:
                                    #needed?
                                    #if isinstance(command.character, enemy.Enemy):
                                    if self.target_group[len(self.target_group)-self.group_access] == command.character:
                                        del self.total_movement[i]
                                    i+=1


                        if self.damage == 1:
                            battle_font2 = self.target_font + u"は眠ってしまった！"
                        elif self.damage == 0:
                            battle_font2 = self.target_font + u"は呪文を妨害した！"
                        else:
                            battle_font2 = self.target_font + u"は眠らなかった。"
                            


                        pass
                    elif battle_command.magic_number == 2:
                        battle_font1 = battle_command.character.name + u"はシールドを唱えた"
                        battle_font2 = battle_command.character.name + u"の前に盾が現れた"
                        

                        if self.damage_set == 0:

                            battle_command.character.battle_ac -= 2
                            self.damage_set = 1
                            battle_command.character.magician_mp[0] -= 1   

                        pass
                    elif battle_command.magic_number == 3:
                        battle_font1 = battle_command.character.name + u"はポジションを唱えた"

                        battle_font2 = u"天龍の塔 " + str(battle_command.character.coordinate[2]) + u"階"
                        battle_font3 = "X:" + str(battle_command.character.coordinate[0]) + " Y:" + str(battle_command.character.coordinate[1])


                        if self.damage_set == 0:

                            self.damage_set = 1
                            battle_command.character.magician_mp[0] -= 1                        


                    pass
                elif battle_command.magic_level == 1:
                    if battle_command.magic_number == 0:
                        battle_font1 = battle_command.character.name + u"はミストを唱えた"
                        battle_font2 = u"辺りに深い霧が現れた"

                        if self.damage_set == 0:

                            self.damage_set = 1

                            for enemy_group in self.enemyList:
                                for enemies in enemy_group:
                                    enemies.ac += 2
                            for enemy_group in self.enemyListBack:
                                for enemies in enemy_group:
                                    enemies.ac += 2

                            battle_command.character.magician_mp[1] -= 1

                            

                                    
                        
                    elif battle_command.magic_number == 1:
                        battle_font1 = battle_command.character.name + u"はアンシールを唱えた"
                        battle_font2 = u"なにも起こらなかった"

                        battle_command.character.magician_mp[1] -= 1

                        
                    elif battle_command.magic_number == 2:
                        battle_font1 = battle_command.character.name + u"はエネルギーボルトを唱えた"
                        
                        if self.damage_set == 0:
                            
                            self.damage = random.randint(3, 18)
                            self.damage = int(self.damage*math.floor(self.target_group[0].none_resistance/100.0))

                            probability = random.randint(1,100)
                            if probability < self.target_group[0].magic_resistance:
                                self.damage = -1

                            self.damage_set = 1

                            battle_command.character.magician_mp[1] -= 1


                            #subtract damage and if hp < 0, remove that character
                            if isinstance( self.target_group[0], character.Character):
                                self.target_group[target].hp -= self.damage

                                self.character_dead()
                                    
                            else:
                                self.target_group[self.offset].hp -= self.damage

                                self.enemy_dead(self.offset)


                        if self.damage != -1:
                            battle_font2 = self.target_font + u"に" + str(self.damage) + u"のダメージ"
                        else:
                            battle_font2 = self.target_font + u"は呪文を妨害した！"

                        if self.dead_set == 1:                    
                            battle_font3 = self.dead_font + u"は死んだ！"

                        
                    elif battle_command.magic_number == 3:
                        battle_font1 = battle_command.character.name + u"はウォータースフィアを唱えた"


                        if self.check == 0:
                            self.group_access = len(self.target_group)
                            battle_command.character.magician_mp[1] -= 1
                            self.check= 1

                        if self.damage_set == 0:

                            self.damage_set = 1

                            self.damage = random.randint(2, 32)
                            self.damage = int(self.damage*math.floor(self.target_group[0].water_resistance/100.0))

                            probability = random.randint(1,100)
                            if probability < self.target_group[len(self.target_group)-self.group_access].magic_resistance:
                                self.damage = -1


                            #subtract damage and if hp < 0, remove that character
                            if self.damage > 0 and isinstance( self.target_group[0], character.Character):
                                self.target_group[len(self.target_group)-self.group_access].hp -= self.damage

                                self.character_dead()
                                    
                            elif self.damage > 0 and isinstance( self.target_group[0], enemy.Enemy):
                                self.target_group[len(self.target_group)-self.group_access].hp -= self.damage

                                self.enemy_dead(len(self.target_group)-self.group_access)

                        if self.damage != -1:
                            battle_font2 = self.target_font + u"に" + str(self.damage) + u"のダメージ"
                        else:
                            battle_font2 = self.target_font + u"は呪文を妨害した！"

                        if self.dead_set == 1:                    
                            battle_font3 = self.dead_font + u"は死んだ！"
                            

                    pass
                elif battle_command.magic_level == 2:

                    if battle_command.magic_number == 0:
                        battle_font1 = battle_command.character.name + u"はポイズンガスを唱えた"


                        if self.check == 0:
                            self.group_access = len(self.target_group)
                            battle_command.character.magician_mp[2] -= 1
                            self.check= 1

                        if self.damage_set == 0:

                            self.damage_set = 1

                            self.damage = 1

                            probability = random.randint(1,100)
                            if probability < self.target_group[len(self.target_group)-self.group_access].magic_resistance:
                                self.damage = 0


                            probability = random.randint(1,100)
                            if probability < self.target_group[len(self.target_group)-self.group_access].poison_resistance:
                                self.damage = -1
                                
                            if self.damage == 1:
                                self.target_group[len(self.target_group)-self.group_access].status[0] = 1



                        if self.damage == 1:
                            battle_font2 = self.target_font + u"は毒に侵された！"
                        elif self.damage == 0:
                            battle_font2 = self.target_font + u"は呪文を妨害した！"
                        else:
                            battle_font2 = self.target_font + u"は影響ない！"
                            
                    elif battle_command.magic_number == 1:
                        battle_font1 = battle_command.character.name + u"はダークフォースを唱えた"
                        
                        if self.damage_set == 0:
                            
                            self.damage = random.randint(8, 52)
                            self.damage = int(self.damage*math.floor(self.target_group[0].dark_resistance/100.0))

                            probability = random.randint(1,100)
                            if probability < self.target_group[0].magic_resistance:
                                self.damage = -1

                            self.damage_set = 1

                            battle_command.character.magician_mp[2] -= 1


                            #subtract damage and if hp < 0, remove that character
                            if isinstance( self.target_group[0], character.Character):
                                self.target_group[target].hp -= self.damage

                                self.character_dead()
                                    
                            else:
                                self.target_group[self.offset].hp -= self.damage

                                self.enemy_dead(self.offset)


                        if self.damage != -1:
                            battle_font2 = self.target_font + u"に" + str(self.damage) + u"のダメージ"
                        else:
                            battle_font2 = self.target_font + u"は呪文を妨害した！"

                        if self.dead_set == 1:                    
                            battle_font3 = self.dead_font + u"は死んだ！"
                            

                    elif battle_command.magic_number == 2:
                        battle_font1 = battle_command.character.name + u"はエクスプロージョンを唱えた"


                        if self.check == 0:
                            self.group_access = len(self.target_group)
                            battle_command.character.magician_mp[2] -= 1
                            self.check= 1

                        if self.damage_set == 0:

                            self.damage_set = 1

                            self.damage = random.randint(16, 64)
                            self.damage = int(self.damage*math.floor(self.target_group[0].fire_resistance/100.0))

                            probability = random.randint(1,100)
                            if probability < self.target_group[len(self.target_group)-self.group_access].magic_resistance:
                                self.damage = -1


                            #subtract damage and if hp < 0, remove that character
                            if self.damage > 0 and isinstance( self.target_group[0], character.Character):
                                self.target_group[len(self.target_group)-self.group_access].hp -= self.damage

                                self.character_dead()
                                    
                            elif self.damage > 0 and isinstance( self.target_group[0], enemy.Enemy):
                                self.target_group[len(self.target_group)-self.group_access].hp -= self.damage

                                self.enemy_dead(len(self.target_group)-self.group_access)

                        if self.damage != -1:
                            battle_font2 = self.target_font + u"に" + str(self.damage) + u"のダメージ"
                        else:
                            battle_font2 = self.target_font + u"は呪文を妨害した！"

                        if self.dead_set == 1:                    
                            battle_font3 = self.dead_font + u"は死んだ！"


                    elif battle_command.magic_number == 3:
                        battle_font1 = battle_command.character.name + u"はマジックフィールドを唱えた"
                        battle_font2 = u"冒険者たちは魔法の壁に包まれた！"

                        if self.damage_set == 0:
                            for chara in game_self.party.member:
                                chara.breath_resist += 1

                            battle_command.character.magician_mp[2] -= 1
                            self.damage_set = 1
                
                elif battle_command.magic_level == 3:
                    pass
                elif battle_command.magic_level == 4:
                    pass
                elif battle_command.magic_level == 5:
                    pass
                elif battle_command.magic_level == 6:
                    pass
                elif battle_command.magic_level == 7:
                    pass
                #priest magic
                elif battle_command.magic_level == 8:
                    if battle_command.magic_number == 0:

                        battle_font1 = battle_command.character.name + u"はヒールを唱えた"

                        if self.damage_set == 0:
                            
                            self.damage = random.randint(1, 8)

                            self.damage_set = 1

                            battle_command.character.priest_mp[0] -= 1

                            #add damage and if hp > 0, make hp = max_hp
                            if isinstance( self.target_group[0], character.Character):
                                self.target_group[target].hp += self.damage

                                if self.target_group[target].hp > self.target_group[target].max_hp:
                                    self.target_group[target].hp = self.target_group[target].max_hp
                                    self.damage = -1
                                    
                            else:
                                self.target_group[self.offset].hp += self.damage

                                if self.target_group[self.offset].hp > self.target_group[self.offset].max_hp:
                                    self.target_group[target].hp = self.target_group[target].max_hp
                                    self.damage = -1

                            

                        if self.damage != -1:
                            battle_font2 = self.target_font + u"は" + str(self.damage) + u"回復した"
                        else:
                            battle_font2 = self.target_font + u"は完治した！"



                        pass
                    elif battle_command.magic_number == 1:
                        battle_font1 = battle_command.character.name + u"はアウェイクを唱えた"
                        battle_font2 = battle_command.character.name + u"冒険者たちは目を覚ました！"

                        if self.damage_set == 0:

                            for chara in game_self.party.member:
                                if chara.status[3] == 1:
                                    chara.status[3] = 0

                            self.damage_set = 1
                            battle_command.character.priest_mp[0] -= 1

                        pass
                    elif battle_command.magic_number == 2:

                        battle_font1 = battle_command.character.name + u"はライトアローを唱えた"

                        if self.damage_set == 0:
                            
                            self.damage = random.randint(1, 6)
                            self.damage = int(self.damage*math.floor(self.target_group[0].light_resistance/100.0))

                            probability = random.randint(1,100)
                            if probability < self.target_group[0].magic_resistance:
                                self.damage = -1

                            self.damage_set = 1

                            battle_command.character.priest_mp[0] -= 1


                            #subtract damage and if hp < 0, remove that character
                            if isinstance( self.target_group[0], character.Character):
                                self.target_group[target].hp -= self.damage

                                self.character_dead()
                                    
                            else:
                                self.target_group[self.offset].hp -= self.damage

                                self.enemy_dead(self.offset)


                        if self.damage != -1:
                            battle_font2 = self.target_font + u"に" + str(self.damage) + u"のダメージ"
                        else:
                            battle_font2 = self.target_font + u"は呪文を妨害した！"

                        if self.dead_set == 1:                    
                            battle_font3 = self.dead_font + u"は死んだ！"

                        pass
                    elif battle_command.magic_number == 3:
                        battle_font1 = battle_command.character.name + u"はウォールを唱えた"
                        battle_font2 = battle_command.character.name + u"の前に壁が現れた"
                        

                        if self.damage_set == 0:

                            battle_command.character.battle_ac -= 3
                            self.damage_set = 1
                            battle_command.character.priest_mp[0] -= 1   



                elif battle_command.magic_level == 9:
                    if battle_command.magic_number == 0:
                        battle_font1 = battle_command.character.name + u"はサイレントを唱えた"


                        if self.check == 0:
                            self.group_access = len(self.target_group)
                            battle_command.character.priest_mp[1] -= 1
                            self.check = 1


                        
                        if self.probability_set == 0:
                            self.probability = random.randint(1,100)
                            self.probability_set = 1

                        if self.probability < self.target_group[0].silent_resistance:
                            battle_font2 = self.target_font + u"の魔法は封じられた"                            
                        else:
                            battle_font2 = self.target_font+ u"は影響無い"                            
                     
      
                        pass
                    
                    elif battle_command.magic_number == 1:
                        battle_font1 = battle_command.character.name + u"はフェイスシールドを唱えた"
                        battle_font2 = u"冒険者たちの前に壁が現れた"

                        if self.damage_set == 0:
                            for chara in game_self.party.member:
                                if chara.face_shield == 0:
                                    chara.permanant_ac -= 2
                                    chara.face_shield = 1

                            battle_command.character.priest_mp[1] -= 1
                            self.damage_set = 1
                                
                    elif battle_command.magic_number == 2:
                        battle_font1 = battle_command.character.name + u"はライトを唱えた"
                        battle_font2 = u"冒険者たちは光で照らされた"

                        if self.damage_set == 0:
                            game_self.party.torch += 30
                            battle_command.character.priest_mp[1] -= 1
                            self.damage_set = 1

                            
                        pass
                    elif battle_command.magic_number == 3:
                        battle_font1 = battle_command.character.name + u"はキュアポイズンを唱えた"

                        if self.damage_set == 0:

                            self.damage_set = 1

                            battle_command.character.priest_mp[1] -= 1

                            #add damage and if hp > 0, make hp = max_hp
                            if isinstance( self.target_group[0], character.Character):

                                if self.target_group[target].status[0] == 1:
                                    self.target_group[target].status[0] = 0
                                    self.check = 1
                                    
                            else:
                                if self.target_group[self.offset].status[0] == 1:
                                    self.target_group[target].status[0] = 0
                                    self.check = 1


                        if self.check == 1:
                            battle_font2 = self.target_font + u"の毒が消えた"
                        else:
                            battle_font2 = self.target_font + u"は影響無い"
                            


                elif battle_command.magic_level == 10:
                    if battle_command.magic_number == 0:
                        battle_font1 = battle_command.character.name + u"はキュアパラライズを唱えた"

                        if self.damage_set == 0:

                            self.damage_set = 1

                            battle_command.character.priest_mp[2] -= 1

                            #add damage and if hp > 0, make hp = max_hp
                            if isinstance( self.target_group[0], character.Character):

                                if self.target_group[target].status[4] == 1:
                                    self.target_group[target].status[4] = 0
                                    self.check = 1
                                    
                            else:
                                if self.target_group[self.offset].status[4] == 1:
                                    self.target_group[target].status[4] = 0
                                    self.check = 1


                        if self.check == 1:
                            battle_font2 = self.target_font + u"の麻痺が消えた"
                        else:
                            battle_font2 = self.target_font + u"は影響無い"

                    elif battle_command.magic_number == 1:
                        battle_font1 = battle_command.character.name + u"はベネディクトを唱えた"
                        battle_font2 = u"冒険者たちは精霊の加護を得た！"

                        if self.damage_set == 0:
                            for chara in game_self.party.member:
                                    chara.battle_ac -= 3

                            battle_command.character.priest_mp[2] -= 1
                            self.damage_set = 1                            

                    elif battle_command.magic_number == 2:
                        battle_font1 = battle_command.character.name + u"はヒールウィンドを唱えた"

                        if self.check == 0:
                            self.group_access = len(self.target_group)
                            battle_command.character.priest_mp[2] -= 1
                            self.check= 1

                        if self.damage_set == 0:

                            self.damage_set = 1

                            self.damage = random.randint(2, 16)


                            #subtract damage and if hp < 0, remove that character
                            if self.damage > 0 and isinstance( self.target_group[0], character.Character):
                                self.target_group[len(self.target_group)-self.group_access].hp += self.damage

                                if self.target_group[len(self.target_group)-self.group_access].hp > self.target_group[len(self.target_group)-self.group_access].max_hp:
                                    self.target_group[len(self.target_group)-self.group_access].hp = self.target_group[len(self.target_group)-self.group_access].max_hp
                                    self.damage = -1
                                    
                            elif self.damage > 0 and isinstance( self.target_group[0], enemy.Enemy):
                                self.target_group[len(self.target_group)-self.group_access].hp -= self.damage

                                if self.target_group[len(self.target_group)-self.group_access].hp > self.target_group[len(self.target_group)-self.group_access].max_hp:
                                    self.target_group[len(self.target_group)-self.group_access].hp = self.target_group[len(self.target_group)-self.group_access].max_hp
                                    self.damage = -1

                        self.target_font = game_self.party.member[len(self.target_group)-self.group_access].name

                        if self.damage == -1:
                            battle_font2 = self.target_font + u"は完治した！"
                        else:
                            battle_font2 = self.target_font + u"は" + str(self.damage) + u"回復した！"


                    if battle_command.magic_number == 3:

                        battle_font1 = battle_command.character.name + u"はサルヴを唱えた"

                        if self.damage_set == 0:
                            
                            self.damage = random.randint(8, 32)

                            self.damage_set = 1

                            battle_command.character.priest_mp[2] -= 1

                            #add damage and if hp > 0, make hp = max_hp
                            if isinstance( self.target_group[0], character.Character):
                                self.target_group[target].hp += self.damage

                                if self.target_group[target].hp > self.target_group[target].max_hp:
                                    self.target_group[target].hp = self.target_group[target].max_hp
                                    self.damage = -1
                                    
                            else:
                                self.target_group[self.offset].hp += self.damage

                                if self.target_group[self.offset].hp > self.target_group[self.offset].max_hp:
                                    self.target_group[target].hp = self.target_group[target].max_hp
                                    self.damage = -1

                            

                        if self.damage != -1:
                            battle_font2 = self.target_font + u"は" + str(self.damage) + u"回復した"
                        else:
                            battle_font2 = self.target_font + u"は完治した！"
                    pass
                elif battle_command.magic_level == 11:
                    pass
                elif battle_command.magic_level == 12:
                    pass
                elif battle_command.magic_level == 13:
                    pass
                elif battle_command.magic_level == 14:
                    pass
                elif battle_command.magic_level == 15:
                    pass

            if battle_command.movement == self.ESCAPE:
                battle_font1 = battle_command.character.name + u"は" + u"逃げ出した"
                if self.probability_set == 0:
                    self.probability = random.randint(1, 100)
                    self.probability_set = 1
                #TO-DO calculate escape probability
                if self.probability < 10 and event_battle == 0:
                    self.escape_flag = 1
                else:            
                    battle_font3 = u"しかし逃げられなかった"

            if battle_command.movement == self.ENEMY_EXTRA:

                if battle_command.magic_level == "麻痺攻撃":
                    battle_font1 = battle_command.character.name + u"は引っ掻いた！"


                    if self.hit_set == 0:
                        self.hit = 0
                        
                        accuracy1 = 19 - party.calculate_ac(self.target_group[target]) - battle_command.character.level
                        accuracy2 = accuracy1 - battle_command.character.ac

                        if accuracy1 < 0:
                            accuracy1 = 0

                        accuracy_total = int( (19-accuracy1)*5)

                        for attack in range(battle_command.character.attack_times):
                            accuracy_probability = random.randint(1,100)
                            if accuracy_probability < accuracy_total:
                                self.hit += 1

                        self.hit_set = 1


                    if self.hit >= 1:    

                        battle_font2 = str(self.hit) + u"回当たり "

                        #calculate damage
                        if (self.damage_set == 0):
                            self.damage = calculate_damage(battle_command.character, self.hit)
                            self.damage_set = 1

                            if self.target_group[0].status[3] == 1 or self.target_group[0].status[4] == 1 or self.target_group[0].status[5] == 1:
                                self.damage*=2

                            self.target_group[target].hp -= self.damage

                            self.character_dead()

                            probability = random.randint(1,100)
                            if probability > (100-(self.target_group[target].luck*3)):
                                self.check = 1

                            if self.check == 1:
                                self.target_group[target].status[4] = 1

                                #delete command of the paralized enemy
                                i=0
                                for command in self.total_movement:
                                    if self.target_group[target] == command.character:
                                        del self.total_movement[i]
                                    i+=1

                                #move the person to end of party
                                temp = self.target_group[target]  
                                del self.target_group[target]
                                self.target_group.append(temp)

                        battle_font2 += str(self.damage) + u"のダメージ"

                        if self.check == 1:
                            battle_font3 = self.target_font + u"は麻痺した！"
                            

                        if self.dead_set == 1:                    
                            battle_font3 = self.dead_font + u"は死んだ！"
                    else:
                        battle_font2 = u"だが外れた！"

                   
                elif battle_command.magic_level == "毒攻撃":
                    battle_font1 = battle_command.character.name + u"は噛み付いた！"

                    if self.hit_set == 0:
                        self.hit = 0
                        
                        accuracy1 = 19 - party.calculate_ac(self.target_group[target]) - battle_command.character.level
                        accuracy2 = accuracy1 - battle_command.character.ac

                        if accuracy1 < 0:
                            accuracy1 = 0

                        accuracy_total = int( (19-accuracy1)*5)

                        for attack in range(battle_command.character.attack_times):
                            accuracy_probability = random.randint(1,100)
                            if accuracy_probability < accuracy_total:
                                self.hit += 1

                        self.hit_set = 1


                    if self.hit >= 1:    

                        battle_font2 = str(self.hit) + u"回当たり "

                        #calculate damage
                        if (self.damage_set == 0):
                            self.damage = calculate_damage(battle_command.character, self.hit)
                            self.damage_set = 1

                            if self.target_group[0].status[3] == 1 or self.target_group[0].status[4] == 1 or self.target_group[0].status[5] == 1:
                                self.damage*=2

                            self.target_group[target].hp -= self.damage

                            self.character_dead()

                            probability = random.randint(1,100)
                            if probability > (100-(self.target_group[target].luck*3)):
                                self.check = 1

                            if self.check == 1:
                                self.target_group[target].status[0] = 1
                                    
                            
                        battle_font2 += str(self.damage) + u"のダメージ"

                        if self.check == 1:
                            battle_font3 = self.target_font + u"は毒に侵された！"
                            

                        if self.dead_set == 1:                    
                            battle_font3 = self.dead_font + u"は死んだ！"
                    else:
                        battle_font2 = u"だが外れた！"

                        

                elif battle_command.magic_level == "ヒール":


                    battle_font1 = battle_command.character.name + u"はヒールを唱えた"

                    if self.damage_set == 0:
                        
                        self.damage = random.randint(1, 8)

                        self.damage_set = 1


                        self.target_group[self.offset].hp += self.damage

                        if self.target_group[self.offset].hp > self.target_group[self.offset].max_hp:
                            self.target_group[target].hp = self.target_group[target].max_hp
                            self.damage = -1


                    if self.damage != -1:
                        battle_font2 = self.target_font + u"は" + str(self.damage) + u"回復した"
                    else:
                        battle_font2 = self.target_font + u"は完治した！"

                elif battle_command.magic_level == "エナジーアロー":

                    battle_font1 = battle_command.character.name + u"はエナジーアローを唱えた"

                    if self.damage_set == 0:
                        
                        self.damage = random.randint(1, 8+battle_command.character.intelligence)

                        self.damage_set = 1

                        self.target_group[target].hp -= self.damage

                        self.character_dead()
                                

                    if self.damage != -1:
                        battle_font2 = self.target_font + u"に" + str(self.damage) + u"のダメージ"
                    else:
                        battle_font2 = self.target_font + u"は呪文を妨害した！"

                    if self.dead_set == 1:                    
                        battle_font3 = self.dead_font + u"は死んだ！"

                    


                elif battle_command.magic_level == "ブレス" or battle_command.magic_level == "0ブレス" or battle_command.magic_level == "MAXブレス":

                    if battle_command.magic_level == "ブレス":
                        battle_font1 = battle_command.character.name + u"はブレスを吐いた"
                    elif battle_command.magic_level == "0ブレス":
                        battle_font1 = battle_command.character.name + u"は生暖かい吐息を吐いた"
                    elif battle_command.magic_level == "MAXブレス":
                        battle_font1 = battle_command.character.name + u"は燃え盛る吐息を吐いた"

                    

                    if self.check == 0:
                        self.group_access = player_count_alive(self.target_group)
                        self.check= 1

                    if self.damage_set == 0:

                        self.damage_set = 1

                        if battle_command.magic_level == "ブレス":
                            self.damage = battle_command.character.hp/2
                        elif battle_command.magic_level == "0ブレス":
                            self.damage = 0
                        elif battle_command.magic_level == "MAXブレス":
                            self.damage = battle_command.character.max_hp

                        if self.target_group[player_count_alive(self.target_group)-self.group_access].breath_resist > 0:
                            self.damage = self.damage - int(self.damage * (self.target_group[player_count_alive(self.target_group)-self.group_access].breath_resist*.20))

                                        
                        self.target_group[player_count_alive(self.target_group)-self.group_access].hp -= self.damage

                        self.character_dead_group(player_count_alive(self.target_group)-self.group_access)


                    if self.dead_set == 1:                    
                        battle_font2 = game_self.party.member[len(self.target_group)-1].name + u"に" + str(self.damage) + u"のダメージ"

                        battle_font3 = self.dead_font + u"は死んだ！"
                    else:
                        battle_font2 = game_self.party.member[player_count_alive(self.target_group)-self.group_access].name + u"に" + str(self.damage) + u"のダメージ"


                    

            
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

                if self.drop_item_key == int(math.ceil(len(self.enemy_drop_items)/4.0)):
                    count = 0
                    for member in game_self.party.member:
                        if member.status == [0,0,0,0,0,0,0,0,0] or (member.status[4] != 1 and member.status[5] != 1 and member.status[6] != 1 and member.status[7] != 1 and member.status[8] != 1):
                            count+= 1


                    exp_font = u"生き残ったメンバーは " + str(int(math.ceil(self.exp/count))) + "EXPを得た"
                    gold_font = u"生き残ったメンバーは " + str(int(math.ceil(self.gold/count))) + "TPを手に入れた"

                    exp_font = self.menu_font.render( exp_font, True, COLOR_WHITE)
                    gold_font = self.menu_font.render( gold_font, True, COLOR_WHITE)
                
                    screen.blit(exp_font, ( 320 - exp_font.get_width()/2, 50))
                    screen.blit(gold_font, ( 320 - gold_font.get_width()/2, 90))

                else:

                    #drop item
                    if len(self.enemy_drop_items) > 4 and self.drop_item_key == 1:
                        for items in range(0,4):
                                                       
                            item_font = game_self.item_data[self.enemy_drop_items[items]][0]
                            item_font = item_font.strip("\"")
                            item_font = unicode(item_font, encoding="sjis")
                            
                            item_font = self.menu_font.render( item_font + u"を拾った", True, COLOR_WHITE)
                            screen.blit(item_font, (320 - item_font.get_width()/2, 20+items*30))

                    else:

                        if len(self.enemy_drop_items) > 4:
                            for items in range(4, len(self.enemy_drop_items)):                
                                item_font = game_self.item_data[self.enemy_drop_items[items]][0]
                                item_font = item_font.strip("\"")
                                item_font = unicode(item_font, encoding="sjis")
                                
                                item_font = self.menu_font.render( item_font + u"を拾った", True, COLOR_WHITE)
                                screen.blit(item_font, (320 - item_font.get_width()/2, 20+(items-4)*30))
                            

                        else:
                            for items in range(0, len(self.enemy_drop_items)):                
                                item_font = game_self.item_data[self.enemy_drop_items[items]][0]
                                item_font = item_font.strip("\"")
                                item_font = unicode(item_font, encoding="sjis")
                                
                                item_font = self.menu_font.render( item_font + u"を拾った", True, COLOR_WHITE)
                                screen.blit(item_font, (320 - item_font.get_width()/2, 20+items*30))

                  
    def battle_handler(self, game_self, event):
        
        if self.enemy_select_window.is_visible == True:
            self.enemy_select_window.enemy_select_window_handler( game_self, event)
            if self.selected == player_count_movable(game_self.party.member):
                self.state = self.BATTLE

                if self.first_attack == 1:
                    self.enemy_movement = []
                    self.first_attack = 0
                else:
                    self.enemy_movement = enemy_movement( self.enemyList, self.enemyListBack, game_self)

                for element in self.party_movement:
                    self.total_movement.append(element)
                for element in self.enemy_movement:
                    self.total_movement.append(element)

                #sort the elements by speed, highest first
                self.total_movement.sort(cmp=lambda x, y: cmp(x.speed,y.speed), reverse=True)                

            return
        

        if self.state == self.INIT:
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN or event.key == K_x):
                if self.extra_key == 2:
                    self.extra_key -= 1
                    return

                if self.extra_key == 1 and self.first_attack == -1:
                    self.state = self.BATTLE
                    self.selected = player_count_movable(game_self.party.member)
                    self.total_movement = enemy_movement( self.enemyList, self.enemyListBack, game_self)
                    self.total_movement.sort(cmp=lambda x, y: cmp(x.speed, y.speed), reverse=True)
                    return

                self.state = self.COMMAND

            return



        elif self.state == self.COMMAND:

            if self.item_view != None and self.item_view.is_visible:
                self.item_view.item_view_handler(event, game_self)
                return
            elif self.magic_window != None and self.magic_window.is_visible == True:
                self.magic_window.magic_all_view_handler(event, game_self)
                return
            
            if event.type == KEYDOWN and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):

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
                    self.party_movement.append( battle_command.Battle_command( character, self.DEFEND, 0, None, None, None, None))
                    character.defend_ac -= 2
                    self.selected += 1
                if self.menu == self.ITEM:
                    self.item_view = system_notify.Item_view(Rect(70, 50, 450, 360))
                    self.item_view.is_visible = True
                    return
                if self.menu == self.CURSE:
                    #only priests could select
                    if character.job == 3 or character.job == 19 or character.job == 20 or character.job ==21:
                        self.enemy_select_window.is_visible = True

                    return
                if self.menu == self.MAGIC:
                    if self.first_attack == 1:
                        pass
                    else:
                        self.magic_window = system_notify.Magic_all_view(Rect(80, 50, 280 ,120))
                        self.magic_window.is_visible = True

                    return
                if self.menu == self.ESCAPE:
                    self.party_movement.append( battle_command.Battle_command( character, self.ESCAPE, 0, None, None, None, None))
                    self.selected+=1               

                #need to do something for sleep
                if self.selected == player_count_movable(game_self.party.member):
                    self.state = self.BATTLE

                    if self.first_attack == 1:
                        self.enemy_movement = []
                        self.first_attack = 0
                    else:
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
            
            if event.type == KEYDOWN and event.key == K_UP: #moves the cursor up
                game_self.cursor_se.play()
                self.menu -= 1
                if self.menu == self.ITEM:
                    self.menu = MENU_MAX
                if self.menu < 0:
                    self.menu = self.ITEM

            elif event.type == KEYDOWN and event.key == K_DOWN:
                game_self.cursor_se.play()
                self.menu += 1
                if self.menu % 3 == 0:
                    self.menu -= 3

            elif event.type == KEYDOWN and event.key == K_LEFT:
                game_self.cursor_se.play()
                self.menu -= 3
                if self.menu < 0:
                    self.menu += MENU_MAX+1

            elif event.type == KEYDOWN and event.key == K_RIGHT:
                game_self.cursor_se.play()
                self.menu += 3
                if self.menu > MENU_MAX:
                    self.menu = self.menu % (MENU_MAX+1)


            if event.type == KEYDOWN and event.key == K_x:
                if self.selected > 0:
                    self.selected -= 1
                    count = len(self.party_movement)
                    del (self.party_movement[count-1])
                    game_self.party.member[ self.selected ].defend_ac = 0

                else:
                    #to end battle
                    game_self.dungeon.battle_flag = 0
                    game_self.dungeon.battle = None
                    game_self.dungeon.music = 0


        elif self.state == self.BATTLE:

            if event.type == KEYDOWN and (event.key == K_x or event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
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

                    #need to move back one space

                    #not sure it is working correctly
                    if game_self.party.direction == 0:
                        for chara in game_self.party.member:
                            if game_self.dungeon.horizontal_wall[chara.coordinate[1]+1][chara.coordinate[0]] == 0 or game_self.dungeon.horizontal_wall[chara.coordinate[1]+1][chara.coordinate[0]] == 2 or game_self.dungeon.horizontal_wall[chara.coordinate[1]+1][chara.coordinate[0]] == 4 or game_self.dungeon.horizontal_wall[chara.coordinate[1]+1][chara.coordinate[0]] == 7 or game_self.dungeon.horizontal_wall[chara.coordinate[1]+1][chara.coordinate[0]] == 9:
                                chara.coordinate[1] += 1
                    elif game_self.party.direction == 1:
                        for chara in game_self.party.member:
                            if game_self.dungeon.vertical_wall[chara.coordinate[1]][chara.coordinate[0]-1] == 0 or game_self.dungeon.vertical_wall[chara.coordinate[1]][chara.coordinate[0]-1] == 2 or game_self.dungeon.vertical_wall[chara.coordinate[1]][chara.coordinate[0]-1] == 4 or game_self.dungeon.vertical_wall[chara.coordinate[1]][chara.coordinate[0]-1] == 6 or game_self.dungeon.vertical_wall[chara.coordinate[1]][chara.coordinate[0]-1] == 8:
                                chara.coordinate[0] -= 1
                    elif game_self.party.direction == 2:
                        for chara in game_self.party.member:
                            if game_self.dungeon.horizontal_wall[chara.coordinate[1]-1][chara.coordinate[0]] == 0 or game_self.dungeon.horizontal_wall[chara.coordinate[1]-1][chara.coordinate[0]] == 2 or game_self.dungeon.horizontal_wall[chara.coordinate[1]-1][chara.coordinate[0]] == 4 or game_self.dungeon.horizontal_wall[chara.coordinate[1]-1][chara.coordinate[0]] == 6 or game_self.dungeon.horizontal_wall[chara.coordinate[1]-1][chara.coordinate[0]] == 8:                        
                                chara.coordinate[1] -= 1
                    elif game_self.party.direction == 3:
                        for chara in game_self.party.member:
                            if game_self.dungeon.vertical_wall[chara.coordinate[1]][chara.coordinate[0]+1] == 0 or game_self.dungeon.vertical_wall[chara.coordinate[1]][chara.coordinate[0]+1] == 2 or game_self.dungeon.vertical_wall[chara.coordinate[1]][chara.coordinate[0]+1] == 4 or game_self.dungeon.vertical_wall[chara.coordinate[1]][chara.coordinate[0]+1] == 7 or game_self.dungeon.vertical_wall[chara.coordinate[1]][chara.coordinate[0]+1] == 9:
                                chara.coordinate[0] += 1
                        
                    return

                if self.group_access > 0:
                    self.group_access -= 1
                    self.probability_set = 0
                    self.dead_set = 0
                    self.hit_set = 0
                    self.damage_set = 0
                    self.probability_set = 0



                if self.group_access == 0:
                    del self.total_movement[0]
                    self.damage_set = 0
                    self.probability_set = 0
                    self.check = 0
                    self.target_font_set = 0
                    self.dead_set = 0
                    self.hit_set = 0

                    #turn ended
                    if self.total_movement == []:
                        self.party_movement = []
                        self.enemy_movement = []
                        self.menu = self.FIGHT
                        self.selected = 0
                        self.state = self.COMMAND

                        for chara in game_self.party.member:
                            chara.defend_ac = 0


                        #deduct damage from poison
                        for chara in game_self.party.member:
                            if chara.status[0] == 1:
                                chara.hp -= int(math.ceil(chara.max_hp/10.0))

                        party_dead_poison(game_self.party.member)

                        for enemy_group in self.enemyList:
                            for enemy in enemy_group:
                                if enemy.status[0] == 1:
                                    enemy.hp -= int(math.ceil(enemy.max_hp/10.0))
                        self.enemy_dead_poison(self.enemyList)
                        for enemy_group in self.enemyListBack:
                            for enemy in enemy_group:
                                if enemy.status[0] == 1:
                                    enemy.hp -= int(math.ceil(enemy.max_hp/10.0))
                        self.enemy_dead_poison(self.enemyListBack)

                        #remove empty lists
                        #all of the command for empty lists are removed
                        #so it could wait for end of turn to remove empty lists?
                        i = 0
                        to_delete = []
                        for group in self.enemyList:
                            if group == []:
                                to_delete.insert(0,i)
                            i+=1
                        for i in to_delete:
                            del self.enemyList[i]

                        i = 0
                        to_delete = []
                        for group in self.enemyListBack:
                            if group == []:
                                to_delete.insert(0,i)
                            i+=1
                        for i in to_delete:
                            del self.enemyListBack[i]

                        #if party member is in sleep, wake up with 50%
                        for chara in game_self.party.member:
                            if chara.status[3] == 1:
                                probability = random.randint(1,100)
                                if probability < 50:
                                    chara.status[3] = 0

                        #if enemy is in sleep, wake up with sleep resistance
                        for enemy_group in self.enemyList:
                            for enemy in enemy_group:
                                if enemy.status[3] == 1:
                                    probability = random.randint(1,100)
                                    if probability < enemy.sleep_resistance:
                                        enemy.status[3] = 0


                        if self.enemyList == [] and self.enemyListBack != []:
                            self.enemyList = self.enemyListBack
                            self.enemyListBack = []

                        if self.enemyList == [] and self.enemyListBack == []:
                            self.state = self.END
                            return
                            #this is for battle end

                        if player_count_movable( game_self.party.member)== 0:
                            self.state = self.END
                            return
                            #game_over

        elif self.state == self.END:
            
            if event.type == KEYDOWN and (event.key == K_x or event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):

                if player_count_movable( game_self.party.member ) == 0:
                    #game_over
                
                    game_self.dungeon.battle_flag = 0
                    game_self.dungeon.battle = None
                    game_self.dungeon.music = 0

                    for character in game_self.party.member:
                        game_self.dungeon_characters.append( character)

                    game_self.party.member = []
                    game_self.party.alignment = 0

                    game_self.game_state = CITY
                    game_self.dungeon = None
                    game_self.city = city.City()
                else:
                    #win


                    if self.drop_item_key == 0:                    
                        game_self.dungeon.battle_flag = 0
                        game_self.dungeon.battle = None
                        game_self.dungeon.music = 0

                        count = 0
                        for character in game_self.party.member:
                            if character.status == [0,0,0,0,0,0,0,0,0] or (character.status[4] != 1 and character.status[5] != 1 and character.status[6] != 1 and character.status[7] != 1 and character.status[8] != 1):
                                count+= 1


                        for character in game_self.party.member:
                            if character.status == [0,0,0,0,0,0,0,0,0] or (character.status[4] != 1 and character.status[5] != 1 and character.status[6] != 1 and character.status[7] != 1 and character.status[8] != 1):
                                character.exp += int(math.ceil(self.exp/count))
                                character.money += int(math.ceil(self.gold/count))
                        pass

                        i = 0
                        for chara in game_self.party.member:
                            while (len(chara.items) < chara.item_max and i < len(self.enemy_drop_items)):
                                chara.items.append( item.Item( game_self.item_data[self.enemy_drop_items[i]]))
                                i += 1

                        for chara in game_self.party.member:
                            chara.battle_ac = 0

                    else:
                        #there are drop items
                        self.drop_item_key -= 1
                        

    #used in battle INIT
    def battle_initiation(self, game_self, screen):
        if self.first == 0:
            encount_se = pygame.mixer.Sound("SE/thunder.wav")
            encount_se.play()
            self.first = 1
            pygame.mixer.music.stop()
            
        #if there is dead character, move them to end
        temp = []
        temp_num = []
        i = 0
        for chara in game_self.party.member:
            if chara.status[4] == 1 or chara.status[5] == 1 or chara.status[6] == 1 or chara.status[7] == 1 or chara.status[8] == 1:
                temp.append(chara)
                temp_num.insert(0,i)              
            i += 1

        for i in temp_num:
            del game_self.party.member[i]

        for chara in temp:
            game_self.party.member.append(chara)
                

        if self.extra_key == 2 or self.extra_key == 0:
            self.encount_window.draw(screen)
            screen.blit(self.battle_start_font, (230, 140))

        if self.extra_key == 1 and self.first_attack == 1:
            #player first
            self.special_battle_window.draw(screen)
            screen.blit(self.party_start_font, (190, 140))
        elif self.extra_key == 1 and self.first_attack == -1:
            #enemy first
            self.special_battle_window.draw(screen)
            screen.blit(self.enemy_start_font, (190, 140)) 


    #Used in battle COMMAND
    def draw_command_windows(self, game_self, screen):

        #draw default battle window

        #draw party information
        game_self.party.draw(screen, game_self)
        #draw command window
        self.command_window.draw(screen)
        #draw enemy information window
        self.enemy_window.draw(screen)

        #show rectangle around selected enemy when selecting target
        self.enemy_select_window.draw(screen)

    def draw_command_selection(self, game_self, screen):
        #draw rectangle around selected command
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

    def draw_battle_command(self, game_self, screen):
        #character for setting a command
        this_character = game_self.party.member[ self.selected ]

        #font "行動:"
        screen.blit(self.select_font, (380, 140))

        #draw character's name
        if self.selected < len(game_self.party.member):
            character_font = self.menu_font.render( this_character.name, True, COLOR_WHITE)     
            screen.blit(character_font, ( 440, 140))

        #check if character is attackable with distance
        if character_attackable ( game_self, this_character):
            screen.blit(self.battle_font, (380, 190))
        else:
            screen.blit(self.not_battle_font, (380,190))

        screen.blit(self.defend_font, (380, 220))
        screen.blit(self.item_font, (380, 250))
       
        #only priests could select curse
        if this_character.job == 3 or this_character.job == 19 or this_character.job == 20 or this_character.job == 21:
            screen.blit(self.curse_font, (500, 190))
        else:
            screen.blit(self.not_curse_font, (500,190))

        screen.blit(self.magic_font, (500, 220))
        screen.blit(self.escape_font, (500, 250))
        
    def draw_enemy_names(self, game_self, screen):
        #display the enemies names
                

        count = 0
        for group in self.enemyList:
            if group != []:
                movable_count = count_movable( group)
                group_font = self.enemy_font.render( str(len(group))+group[0].name + " ("+str(movable_count)+")", True, COLOR_WHITE)
                screen.blit(group_font, (20, 20+count*20))
                count+=1
            
        count = 0
        for group in self.enemyListBack:
            if group != []:
                movable_count = count_movable( group)
                group_font = self.enemy_font.render( str(len(group))+group[0].name + " ("+str(movable_count)+")", True, COLOR_WHITE)
                screen.blit(group_font, (340, 20+count*20))
                count+=1
    def character_dead(self):
        target = self.total_movement[0].target
        if self.target_group[target].hp <= 0:
            self.target_group[target].hp = 0
            self.target_group[target].status[6] = 1
            self.target_group[target].rip += 1
            temp = self.target_group[target]
            self.dead_set = 1
            self.dead_font = self.target_group[target].name
            #delete command of dead person
            i = 0
            for command in self.total_movement:
                if isinstance(command.character, character.Character):
                    if self.target_group[target] == command.character:
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
            
                    
            #move the person to end of party
            del self.target_group[target]
            self.target_group.append(temp)


            

    def character_dead_group(self, offset):
        if self.target_group[offset].hp <= 0:
            self.target_group[offset].hp = 0
            self.target_group[offset].status[6] = 1
            self.target_group[offset].rip += 1
            temp = self.target_group[offset]
            self.dead_set = 1
            self.dead_font = self.target_group[offset].name
            #delete command of dead person
            i = 0
            for command in self.total_movement:
                if isinstance(command.character, character.Character):
                    if self.target_group[offset] == command.character:
                        del self.total_movement[i]
                i+=1


            i = 0
            to_delete = []
            for command in self.total_movement:
                if isinstance(command.character, enemy.Enemy):
                    if offset == command.target:
                        if i!= 0:
                            to_delete.insert(0,i)                                        
                    i+=1
                
            for i in to_delete:
                del self.total_movement[i]
            
                    
            #move the person to end of party
            del self.target_group[offset]
            self.target_group.append(temp)
            
    def enemy_dead(self, offset):
        battle_command = self.total_movement[0]
        target = battle_command.target
        if self.target_group[offset].hp <= 0:
            self.exp += self.target_group[offset].exp
            self.gold += self.target_group[offset].drop_gold
            battle_command.character.marks += 1
            
            #delete command of the dead enemy
            i=0
            for command in self.total_movement:
                if isinstance(command.character, enemy.Enemy):
                    if self.target_group[offset] == command.character:
                        del self.total_movement[i]
                i+=1

            del self.target_group[offset]

            #delete command of party targeted at those enemy
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
                
                #del self.enemyList[target]

            self.dead_set = 1
            self.dead_font = self.target_font


    def enemy_dead_poison(self, enemyList):


        for enemy_group in enemyList:
            to_delete = []
            i = 0
            for enemy in enemy_group:
                if enemy.hp <= 0:
                    self.exp += enemy.exp
                    self.gold += enemy.drop_gold
                    to_delete.insert(0,i)

            for i in to_delete:
                del enemy_group[i]

        
def party_dead_poison(party):
    
    i = 0
    for chara in party:
        if chara.hp <= 0:
            chara.hp = 0
            chara.status[6] = 1
            chara.rip+=1
        i+= 1

    #if there is dead character, move them to end
    temp = []
    temp_num = []
    i = 0
    for chara in party:
        if chara.status[4] == 1 or chara.status[5] == 1 or chara.status[6] == 1 or chara.status[7] == 1 or chara.status[8] == 1:
            temp.append(chara)
            temp_num.insert(0,i)              
        i += 1

    for i in temp_num:
        del party[i]

    for chara in temp:
        party.append(chara)
        


def count_movable( enemy_group ):

    movable_count = 0
    for enemy_status in enemy_group:
        if enemy_status.status == [0,0,0,0,0,0,0,0,0] or (enemy_status.status[3] != 1 and enemy_status.status[4] != 1 and enemy_status.status[5] != 1 and enemy_status.status[6] != 1 and enemy_status.status[7] != 1 and enemy_status.status[8] != 1):
            movable_count += 1
    return movable_count

#used by monster selecting target
def player_count_movable ( player_group):
    movable_count = 0
    for player in player_group:
        if player.status == [0,0,0,0,0,0,0,0,0] or (player.status[4] != 1 and player.status[5] != 1 and player.status[6] != 1 and player.status[7] != 1 and player.status[8] != 1):
            movable_count += 1
    return movable_count

def player_count_alive ( player_group):
    alive_count = 0
    for player in player_group:
        if player.status[6] != 1 and player.status[7] != 1 and player.status[8] != 1:
            alive_count+=1
    return alive_count

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

    if floor == 2:

        group_number = random.randint( 2, 3)

        for group in range(1, group_number):
            enemy_id = random.randint(6,10)

            enemy_count = random.randint(1,4)

            enemy_group = []

            for i in range(enemy_count):
                enemy_group.append( enemy.Enemy(enemy_data[ enemy_id ]))

            enemy_front.append(enemy_group)

        enemy_total.append(enemy_front)
        enemy_total.append(enemy_back)

    if floor == 3:

        group_number = random.randint(2,3)
    
        for group in range(1,group_number):

            enemy_id = random.randint(12,14)

            enemy_count = random.randint(1,6)

            enemy_group = []

            for i in range(enemy_count):
                enemy_group.append( enemy.Enemy(enemy_data[ enemy_id ]))

            enemy_front.append( enemy_group)

        group_number = random.randint(2,2)
        for group in range(1, group_number):
            enemy_id = random.randint(12,14)

            enemy_count = random.randint(1,4)

            enemy_group = []

            for i in range(enemy_count):
                enemy_group.append( enemy.Enemy(enemy_data[ enemy_id ]))

            enemy_back.append( enemy_group)

        enemy_total.append(enemy_front)
        enemy_total.append(enemy_back)

    if floor == 4:
        group_number = random.randint(2,4) 
    
        for group in range(1,group_number):

            enemy_id = random.randint(16,18)

            enemy_count = random.randint(1,4)

            enemy_group = []

            for i in range(enemy_count):
                enemy_group.append( enemy.Enemy(enemy_data[ enemy_id ]))

            enemy_front.append( enemy_group)

        group_number = random.randint(2,3)
        for group in range(1, group_number):
            enemy_id = random.randint(16,18)

            enemy_count = random.randint(1,3)

            enemy_group = []

            for i in range(enemy_count):
                enemy_group.append( enemy.Enemy(enemy_data[ enemy_id ]))

            enemy_back.append( enemy_group)

        enemy_total.append(enemy_front)
        enemy_total.append(enemy_back)

    if floor == 5:
        #no encount

        enemy_total.append(enemy_front)
        enemy_total.append(enemy_back)

        pass
        
        

    return enemy_total
            

def calculate_hit_time( character ):
    
    if character.job == 0 or character.job == 3:
        return int(character.level/3) + 1

    elif character.job == 1:
        return int(character.level/3) + 1

    elif character.job == 2 or character.job == 4 or character.job == 5:
        return int(character.level/5) + 1

    elif character.job == 10 or character.job == 11 or character.job == 12:
        return int(character.level/3) + 2
        
    elif character.job == 13 or character.job == 14 or character.job == 15:
        return int(character.level/2) + 1
    
    elif character.job == 17 or character.job == 18:
        return int(character.level/5) + 1
        
    elif character.job == 16 or character.job == 19 or character.job == 20 or character.job == 21:
        return int(character.level/3) + 1
    
    elif character.job == 22 or character.job == 23 or character.job == 24:
        return int(character.level/3) + 2
    
    elif character.job == 25 or character.job == 26 or character.job == 27:
        return int(character.level/3) + 1

    
def calculate_damage( chara, hit_times):

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

    max_damage = damage

    total_damage = 0
    for i in range(hit_times):
        damage = random.randint(1, max_damage)
        total_damage += damage

    
    return total_damage


def enemy_movement( enemyList, enemyListBack, game_self):

    enemy_command = []

    for group in enemyList:
        for enemy in group:
            if enemy.status == [0,0,0,0,0,0,0,0,0] or (enemy.status[3] != 1 and enemy.status[4] != 1 and enemy.status[5] != 1 and enemy.status[6] != 1 and enemy.status[7] != 1 and enemy.status[8] != 1):
                movement = random.randint(1,100)
                player_movable = player_count_movable(game_self.party.member)


                if len(enemy.extra_attack) > 0 and movement < enemy.extra_attack[0]:
                    if enemy.extra_attack[2] == "PARTY_ONE":

                        if enemy.extra_attack[1] == 1:
                            if player_movable > 3:
                                target = random.randint(0, 2)
                            else:
                                target = random.randint(0, player_movable-1)
                        elif enemy.extra_attack[1] == 2:
                            target = random.randint(0, player_movable-1)
                    elif enemy.extra_attack[2] == "PARTY_LINE":
                        pass
                    elif enemy.extra_attack[2] == "PARTY_BOX":
                        pass
                    elif enemy.extra_attack[2] == "PARTY_ALL":
                        target = 0               
                    elif enemy.extra_attack[2] == "ENEMY_ONE":
                        length = len(enemyList)+len(enemyListBack)
                        target = random.randint(0,length-1)
                        pass
                        #target = random.randint(0, player_movable-1)
                    elif enemy.extra_attack[2] == "ENEMY_ALL":
                        pass
                    elif enemy.extra_attack[2] == "CALL":
                        pass
                    
                    enemy_command.append( battle_command.Battle_command( enemy, 6, target, enemy.extra_attack[2], enemy.extra_attack[3], None, None))
                    continue

                movement = random.randint(1,100)              
                if len(enemy.extra_attack) > 4 and movement < enemy.extra_attack[4]:

                    if enemy.extra_attack[6] == "PARTY_ONE":

                        if enemy.extra_attack[5] == 1:
                            if player_movable > 3:
                                target = random.randint(0, 2)
                            else:
                                target = random.randint(0, player_movable-1)
                        elif enemy.extra_attack[5] == 2:
                            target = random.randint(0, player_movable-1)
                    elif enemy.extra_attack[6] == "PARTY_LINE":
                        pass
                    elif enemy.extra_attack[6] == "PARTY_BOX":
                        pass
                    elif enemy.extra_attack[6] == "PARTY_ALL":
                        target = 0               
                    elif enemy.extra_attack[6] == "ENEMY_ONE":
                        length = len(enemyList)+len(enemyListBack)
                        target = random.randint(0,length-1)
                        pass
                        #target = random.randint(0, player_movable-1)
                    elif enemy.extra_attack[6] == "ENEMY_ALL":
                        pass
                    elif enemy.extra_attack[6] == "CALL":
                        pass

                    enemy_command.append( battle_command.Battle_command( enemy, 6, target, enemy.extra_attack[6], enemy.extra_attack[7], None, None))
                    continue

                movement = random.randint(1,100)                              
                if len(enemy.extra_attack) > 8 and movement < enemy.extra_attack[8]:

                    if enemy.extra_attack[10] == "PARTY_ONE":

                        if enemy.extra_attack[9] == 1:
                            if player_movable > 3:
                                target = random.randint(0, 2)
                            else:
                                target = random.randint(0, player_movable-1)
                        elif enemy.extra_attack[9] == 2:
                            target = random.randint(0, player_movable-1)
                    elif enemy.extra_attack[10] == "PARTY_LINE":
                        pass
                    elif enemy.extra_attack[10] == "PARTY_BOX":
                        pass
                    elif enemy.extra_attack[10] == "PARTY_ALL":
                        target = 0               
                    elif enemy.extra_attack[10] == "ENEMY_ONE":
                        length = len(enemyList)+len(enemyListBack)
                        target = random.randint(0,length-1)
                        pass
                        #target = random.randint(0, player_movable-1)
                    elif enemy.extra_attack[10] == "ENEMY_ALL":
                        pass
                    elif enemy.extra_attack[10] == "CALL":
                        pass

                    enemy_command.append( battle_command.Battle_command( enemy, 6, target, enemy.extra_attack[10], enemy.extra_attack[11], None, None))
                    continue

                movement = random.randint(1,100)                              
                if len(enemy.extra_attack) > 12 and movement < enemy.extra_attack[12]:

                    if enemy.extra_attack[14] == "PARTY_ONE":

                        if enemy.extra_attack[13] == 1:
                            if player_movable > 3:
                                target = random.randint(0, 2)
                            else:
                                target = random.randint(0, player_movable-1)
                        elif enemy.extra_attack[13] == 2:
                            target = random.randint(0, player_movable-1)
                    elif enemy.extra_attack[14] == "PARTY_LINE":
                        pass
                    elif enemy.extra_attack[14] == "PARTY_BOX":
                        pass
                    elif enemy.extra_attack[14] == "PARTY_ALL":
                        target = 0               
                    elif enemy.extra_attack[14] == "ENEMY_ONE":
                        length = len(enemyList)+len(enemyListBack)
                        target = random.randint(0,length-1)
                        pass
                        #target = random.randint(0, player_movable-1)
                    elif enemy.extra_attack[14] == "ENEMY_ALL":
                        pass
                    elif enemy.extra_attack[14] == "CALL":
                        pass

                    enemy_command.append( battle_command.Battle_command( enemy, 6, target, enemy.extra_attack[14], enemy.extra_attack[15], None, None))
                    continue

                if enemy.attack_range == 0:
                    if player_movable > 3:
                        target = random.randint(0,2)
                    else:
                        target = random.randint(0, player_movable-1)
                enemy_command.append( battle_command.Battle_command( enemy, 0, target, None, None, None, None))

    for group in enemyListBack:
        for enemy in group:
            if enemy.status == [0,0,0,0,0,0,0,0,0] or (enemy.status[3] != 1 and enemy.status[4] != 1 and enemy.status[5] != 1 and enemy.status[6] != 1 and enemy.status[7] != 1 and enemy.status[8] != 1):
                movement = random.randint(1,100)
                player_movable = player_count_movable(game_self.party.member)

                if len(enemy.extra_attack) > 0 and movement < enemy.extra_attack[0]:
                    if enemy.extra_attack[2] == "PARTY_ONE":

                        if enemy.extra_attack[1] == 1:
                            #not reachable
                            continue
                        elif enemy.extra_attack[1] == 2:
                            target = random.randint(0, player_movable-1)
                    elif enemy.extra_attack[2] == "PARTY_LINE":
                        pass
                    elif enemy.extra_attack[2] == "PARTY_BOX":
                        pass
                    elif enemy.extra_attack[2] == "PARTY_ALL":
                        target = 0               
                    elif enemy.extra_attack[2] == "ENEMY_ONE":
                        length = len(enemyList)+len(enemyListBack)
                        target = random.randint(0,length-1)
                        pass
                        #target = random.randint(0, player_movable-1)
                    elif enemy.extra_attack[2] == "ENEMY_ALL":
                        pass
                    elif enemy.extra_attack[2] == "CALL":
                        pass
                    
                    enemy_command.append( battle_command.Battle_command( enemy, 6, target, enemy.extra_attack[2], enemy.extra_attack[3], None, None))
                    continue

                movement = random.randint(1,100)              
                if len(enemy.extra_attack) > 4 and movement < enemy.extra_attack[4]:

                    if enemy.extra_attack[6] == "PARTY_ONE":

                        if enemy.extra_attack[5] == 1:
                            continue
                        elif enemy.extra_attack[5] == 2:
                            target = random.randint(0, player_movable-1)
                    elif enemy.extra_attack[6] == "PARTY_LINE":
                        pass
                    elif enemy.extra_attack[6] == "PARTY_BOX":
                        pass
                    elif enemy.extra_attack[6] == "PARTY_ALL":
                        target = 0               
                    elif enemy.extra_attack[6] == "ENEMY_ONE":
                        length = len(enemyList)+len(enemyListBack)
                        target = random.randint(0,length-1)
                        pass
                        #target = random.randint(0, player_movable-1)
                    elif enemy.extra_attack[6] == "ENEMY_ALL":
                        pass
                    elif enemy.extra_attack[6] == "CALL":
                        pass

                    enemy_command.append( battle_command.Battle_command( enemy, 6, target, enemy.extra_attack[6], enemy.extra_attack[7], None, None))
                    continue

                movement = random.randint(1,100)                              
                if len(enemy.extra_attack) > 8 and movement < enemy.extra_attack[8]:

                    if enemy.extra_attack[10] == "PARTY_ONE":

                        if enemy.extra_attack[9] == 1:
                            continue
                        elif enemy.extra_attack[9] == 2:
                            target = random.randint(0, player_movable-1)
                    elif enemy.extra_attack[10] == "PARTY_LINE":
                        pass
                    elif enemy.extra_attack[10] == "PARTY_BOX":
                        pass
                    elif enemy.extra_attack[10] == "PARTY_ALL":
                        target = 0               
                    elif enemy.extra_attack[10] == "ENEMY_ONE":
                        length = len(enemyList)+len(enemyListBack)
                        target = random.randint(0,length-1)
                        pass
                        #target = random.randint(0, player_movable-1)
                    elif enemy.extra_attack[10] == "ENEMY_ALL":
                        pass
                    elif enemy.extra_attack[10] == "CALL":
                        pass

                    enemy_command.append( battle_command.Battle_command( enemy, 6, target, enemy.extra_attack[10], enemy.extra_attack[11], None, None))
                    continue

                movement = random.randint(1,100)                              
                if len(enemy.extra_attack) > 12 and movement < enemy.extra_attack[12]:

                    if enemy.extra_attack[14] == "PARTY_ONE":

                        if enemy.extra_attack[13] == 1:
                            continue
                        elif enemy.extra_attack[13] == 2:
                            target = random.randint(0, player_movable-1)
                    elif enemy.extra_attack[14] == "PARTY_LINE":
                        pass
                    elif enemy.extra_attack[14] == "PARTY_BOX":
                        pass
                    elif enemy.extra_attack[14] == "PARTY_ALL":
                        target = 0               
                    elif enemy.extra_attack[14] == "ENEMY_ONE":
                        length = len(enemyList)+len(enemyListBack)
                        target = random.randint(0,length-1)
                        pass
                        #target = random.randint(0, player_movable-1)
                    elif enemy.extra_attack[14] == "ENEMY_ALL":
                        pass
                    elif enemy.extra_attack[14] == "CALL":
                        pass

                    enemy_command.append( battle_command.Battle_command( enemy, 6, target, enemy.extra_attack[14], enemy.extra_attack[15], None, None))
                    continue

                #if range is 0, it cannot reach character so do not yet.
                if enemy.attack_range > 0:
                    #if len(game_self.party.member) > 3:
                    #    target = random.randint(0,2)
                    #else:
                    target = random.randint(0, len(game_self.party.member)-1)
                    
                    enemy_command.append( battle_command.Battle_command( enemy, 0, target, None, None, None, None))

    if game_self.dungeon.battle.first_attack == -1:

        to_delete = []

        i = 0
        for command in enemy_command:
            if command.magic_level == "ヒール" or command.magic_level == "エナジーアロー":
                to_delete.insert(0,i)
            i+=1    

        for i in to_delete:
            del enemy_command[i]
        
        game_self.dungeon.battle.first_attack = 0 
                
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
            total += equip.bonus

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

def event_battle( game_self, enemyList, enemyListBack):
    game_self.dungeon.battle.enemyList = enemyList
    game_self.dungeon.battle.enemyListBack = enemyListBack

    game_self.dungeon.battle.enemy_drop_items = []

    #take probability (drop% * number of enemy)
    #and if random value is less than that, add it to drop item
    for enemy_group in enemyList:
        i = 0
        probability = 0
        for item in enemy_group[0].drop_item:
            if i%2==0:
                probability = item*len(enemy_group)
                i+= 1
                continue

            random_value = random.randint(1,100)
            if random_value < probability:
                game_self.dungeon.battle.enemy_drop_items.append(item)
            i += 1

    for enemy_group in enemyListBack:
        i = 0
        probability = 0
        for item in enemy_group[0].drop_item:
            if i%2==0:
                probability = item*len(enemy_group)
                i+=1
                continue

            random_value = random.randint(1,100)
            if random_value < probability:
                game_self.dungeon.battle.enemy_drop_items.append(item)
            i += 1

    game_self.dungeon.battle.event_battle = 1
