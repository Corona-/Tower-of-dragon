#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window
import random
import system_notify

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

HORSE, EASY, ECONOMY, SUITE, ROYAL, MAX = 0, 1, 2, 3, 4, 5

#rest level is level of the place resting
#inn is resting in inn (1) or resting in house

def rest(self, game_self, rest_level, inn):

    payment = 0
    cure = 0
    if rest_level == HORSE:
        payment = 0      
    elif rest_level == EASY:
        payment = 10
        cure = (int)(game_self.party.member[self.menu].max_hp / 10)
    elif rest_level == ECONOMY:
        payment = 50
        cure = (int)(game_self.party.member[self.menu].max_hp / 5)
    elif rest_level == SUITE:
        payment = 200
        cure = (int)(game_self.party.member[self.menu].max_hp / 2)
    elif rest_level == ROYAL:
        payment = 500
        cure = (int)(game_self.party.member[self.menu].max_hp)
    elif rest_level == MAX:
        payment = 0
        cure = (int)(game_self.party.member[self.menu].max_hp)

    if game_self.party.member[self.menu].money < payment:
        self.inn_not_enough = system_notify.Donate_finish_window(Rect(150, 160 ,300, 50), system_notify.Donate_finish_window.NOT_ENOUGH)

        self.inn_not_enough.is_visible = True
    else:
        if inn:
            game_self.party.member[self.menu].money -= payment

        #i = 0
        #for magic_times in game_self.party.member[self.menu].max_magician_mp:
        #    game_self.party.member[self.menu].magician_mp[i] = magic_times
        #    i+= 1
        game_self.party.member[self.menu].magician_mp = game_self.party.member[self.menu].max_magician_mp[:]
        
            
        #i = 0
        #for magic_times in game_self.party.member[self.menu].max_priest_mp:
        #    game_self.party.member[self.menu].priest_mp[i] = magic_times
        #    i+= 1
        game_self.party.member[self.menu].priest_mp = game_self.party.member[self.menu].max_priest_mp[:]


##        print game_self.party.member[self.menu].max_magician_mp
##        print game_self.party.member[self.menu].magician_mp
##        print game_self.party.member[self.menu].max_priest_mp
##        print game_self.party.member[self.menu].priest_mp

        if rest_level > 0 and cure == 0:
            cure = 1
        game_self.party.member[self.menu].hp += cure
        if game_self.party.member[self.menu].hp > game_self.party.member[self.menu].max_hp:
            game_self.party.member[self.menu].hp = game_self.party.member[self.menu].max_hp


#calculate the exp needed
#need to find better way to calculate exp
def calc_exp_needed(self, character):
    necessary_exp = int(100*1.6 ** character.level)  
    character.next = necessary_exp - character.exp


def level_up(self, character, rest_level, lv_change):
    
    character.level += 1

    strength_change = random.randint(1, 10)
    intelligence_change = random.randint(1, 10)
    piety_change = random.randint(1, 10)
    vitality_change = random.randint(1, 10)
    agility_change = random.randint(1, 10)
    luck_change = random.randint(1, 10)


    if rest_level == 0:
        status_change(self, strength_change, 5, 7, character, 0, lv_change)
        status_change(self, intelligence_change, 5, 7, character, 1, lv_change)
        status_change(self, piety_change, 5, 7, character, 2, lv_change)
        status_change(self, vitality_change, 5, 7, character, 3, lv_change)
        status_change(self, agility_change, 5, 7, character, 4, lv_change)
        status_change(self, luck_change, 5, 7, character, 5, lv_change)        
    if rest_level == 1:
        status_change(self, strength_change, 4, 7, character, 0, lv_change)
        status_change(self, intelligence_change, 4, 7, character, 1, lv_change)
        status_change(self, piety_change, 4, 7, character, 2, lv_change)
        status_change(self, vitality_change, 4, 7, character, 3, lv_change)
        status_change(self, agility_change, 4, 7, character, 4, lv_change)
        status_change(self, luck_change, 4, 7, character, 5, lv_change)        
    if rest_level == 2:
        status_change(self, strength_change, 4, 6, character, 0, lv_change)
        status_change(self, intelligence_change,4, 6, character, 1, lv_change)
        status_change(self, piety_change, 4, 6, character, 2, lv_change)
        status_change(self, vitality_change, 4, 6, character, 3, lv_change)
        status_change(self, agility_change, 4, 6, character, 4, lv_change)
        status_change(self, luck_change, 4, 6, character, 5, lv_change)    
    if rest_level == 3:
        status_change(self, strength_change, 3, 6, character, 0, lv_change)
        status_change(self, intelligence_change, 3, 6, character, 1, lv_change)
        status_change(self, piety_change, 3, 6, character, 2, lv_change)
        status_change(self, vitality_change, 3, 6, character, 3, lv_change)
        status_change(self, agility_change, 3, 6, character, 4, lv_change)
        status_change(self, luck_change, 3, 6, character, 5, lv_change)        
    if rest_level == 4:
        status_change(self, strength_change, 2, 5, character, 0, lv_change)
        status_change(self, intelligence_change, 2, 5, character, 1, lv_change)
        status_change(self, piety_change, 2, 5, character, 2, lv_change)
        status_change(self, vitality_change, 2, 5, character, 3, lv_change)
        status_change(self, agility_change, 2, 5, character, 4, lv_change)
        status_change(self, luck_change, 2, 5, character, 5, lv_change)        
    if rest_level == 5:
        status_change(self, strength_change, 1, 4, character, 0, lv_change)
        status_change(self, intelligence_change, 1, 4, character, 1, lv_change)
        status_change(self, piety_change, 1, 4, character, 2, lv_change)
        status_change(self, vitality_change, 1, 4, character, 3, lv_change)
        status_change(self, agility_change, 1, 4, character, 4, lv_change)
        status_change(self, luck_change, 1, 4, character, 5, lv_change)        

    hp_changed = 0
    if character.job == 0:
        hp_changed = random.randint(1, (character.level*character.vitality/10)+character.level*10)
    elif character.job == 1 or character.job == 3:
        hp_changed = random.randint(1, (character.level*character.vitality/10)+character.level*8)
    elif character.job == 4 or character.job == 5:
        hp_changed = random.randint(1, (character.level*character.vitality/10)+character.level*6)
    elif character.job == 2:
        hp_changed = random.randint(1, (character.level*character.vitality/10)+character.level*4)

    if hp_changed <= character.max_hp:
        character.max_hp += 1
        character.hp += 1
        lv_change[6] = 1
    else:
        change = hp_changed - character.max_hp 
        character.max_hp = hp_changed
        character.hp += change
        lv_change[6] = change
        

    #TO-DO learn new magic

    #increase mp and learn new magic
    if character.job == 2 or character.job == 3:

        #MAGICIAN
        if character.job == 2:
            magic_lv_up = 0
            i = 0

            for mp in character.max_magician_mp:

                if character.job == 2 and i == 7:
                    break

                #if that level magic is learned add mp
                if mp > 0:
                    magic_change = random.randint(0, 1)

                    if character.magic[i][0] == 1 and character.magic[i][1] == 1 and character.magic[i][2] == 1 and character.magic[i][3] == 1:
                        magic_change = 1
                                    
                    character.max_magician_mp[i] += magic_change
                    if character.max_magician_mp[i] > 9:
                        character.max_magician_mp[i] = 9
                else:
                    #learn new magic lv
                    if magic_lv_up == 0:
                        if character.job == 2:
                            if character.intelligence >= 10:
                                learn = random.randint(1, character.intelligence_max+100)

                                if i > 0 and character.magic[i-1][0] == 1 and character.magic[i-1][1] == 1 and character.magic[i-1][2] == 1 and character.magic[i-1][3] == 1:
                                    learn = 0


                                    
                                if learn < character.intelligence:
                                    character.max_magician_mp[i] += 1
                                    magic_lv_up = 1
                            else:
                                learn = random.randint(1, 100)

                                if i > 0 and character.magic[i-1][0] == 1 and character.magic[i-1][1] == 1 and character.magic[i-1][2] == 1 and character.magic[i-1][3] == 1:
                                    learn = 0

                                if learn <= 7:
                                    character.max_magician_mp[i] += 1
                                    magic_lv_up = 1
                        magic_lv_up = 1


                i += 1

            character.magician_mp = character.max_magician_mp[:]

            #learn new magic
            i = 0
            j = 0
            learn = 0
            learned = False
            for a in character.magic:
                for b in character.magic[i]:
                    if character.job == 2 and j == 4:
                        break
                    
                    if b == 0 and character.max_magician_mp[i] > 0:
                        if character.intelligence >= 10:
                            learn = random.randint(1, character.intelligence_max+45)
                            if learn < character.intelligence:
                                character.magic[i][j] = 1
                                learned = True
                        else:
                            learn = random.randint(1, 100)
                            if learn <= 15:
                                character.magic[i][j] = 1
                                learned = True                            
                    j += 1

                    if learned == True:
                        break
                if learned == True:
                    break
                i += 1
                j = 0

            if learned == True:
                lv_change[7] = 1

            #if no magic in that level, make mp = 0
            i = 0
            for magic_level in character.magic:
                count = 0
                for each_magic in character.magic[i]:
                    if each_magic == 1:
                        count +=1

                if count == 0:
                    character.max_magician_mp[i] = 0

                i+=1

            character.magician_mp = character.max_magician_mp[:]
                    
            

        #PRIEST
        if character.job == 3:
            magic_lv_up = 0
            i = 0
            for mp in character.max_priest_mp:

                if character.job == 3 and i == 7:
                    break
                
                if mp > 0:
                    priest_change = random.randint(0, 1)

                    if character.priest_magic[i][0] == 1 and character.priest_magic[i][1] == 1 and character.priest_magic[i][2] == 1 and character.priest_magic[i][3] == 1:
                        priest_change = 1


                    character.max_priest_mp[i] += priest_change
                    if character.max_priest_mp[i] > 9:
                        character.max_priest_mp[i] = 9
                else:
                    #learn new magic lv
                    if magic_lv_up == 0:
                        if character.job == 3:
                            if character.piety >= 10:
                                learn = random.randint(1, character.intelligence_max+100)

                                if i > 0 and character.priest_magic[i-1][0] == 1 and character.priest_magic[i-1][1] == 1 and character.priest_magic[i-1][2] == 1 and character.priest_magic[i-1][3] == 1:
                                    learn = 0

                                if learn < character.piety:
                                    character.max_priest_mp[i] += 1
                                    magic_lv_up = 1
                            else:
                                learn = random.randint(1, 100)

                                if i > 0 and character.priest_magic[i-1][0] == 1 and character.priest_magic[i-1][1] == 1 and character.priest_magic[i-1][2] == 1 and character.priest_magic[i-1][3] == 1:
                                    learn = 0
                                
                                if learn <= 7:
                                    character.max_priest_mp[i] += 1
                                    magic_lv_up = 1
                        magic_lv_up = 1

                i += 1

            character.priest_mp = character.max_priest_mp[:]

            #learn new magic

            i = 0
            j = 0
            learn = 0
            learned = False
            for a in character.priest_magic:
                for b in character.priest_magic[i]:

                    if character.job == 3 and j == 4:
                        break
                    
                    
                    if b == 0 and character.max_priest_mp[i] > 0:

                        if character.piety >= 10:
                            learn = random.randint(1, character.piety_max+45)
                            if learn < character.piety:
                                character.priest_magic[i][j] = 1
                                learned = True
                        else:
                            learn = random.randint(1, 100)
                            if learn <= 15:
                                character.priest_magic[i][j] = 1
                                learned = True
                    if learned == True:
                        break
                    j += 1
                    
                if learned == True:
                    break
                i += 1
                j = 0

            
            if learned == True:
                lv_change[7] = 1

            #if no magic in that level, make mp = 0
            i = 0
            for magic_level in character.priest_magic:
                count = 0
                for each_magic in character.priest_magic[i]:
                    if each_magic == 1:
                        count +=1

                if count == 0:
                    character.max_priest_mp[i] = 0

                i+=1

            character.priest_mp = character.max_priest_mp[:]
                    



#strength,intelligence,piety,vitality,agility,luck = 0,1,2,3,4,5
#change stores which status changed,
#0=str,1=int,2=pie,3=vit,4=agi,5=luc,6=hp,7=magic
def status_change( self, change, down, stay, character, instruction, lv_change):

    if instruction == 0:
        if change < down:
            character.strength -= 1
            if character.strength < 1:
                character.strength = 1
            else:
                lv_change[0] = -1
        if change < stay:
            pass
        else:
            character.strength += 1
            if character.strength > character.strength_max:
                character.strength = character.strength_max
            else:
                lv_change[0] = 1
    elif instruction == 1:
        if change < down:
            character.intelligence -= 1
            if character.intelligence < 1:
                character.intelligence = 1
            else:
                lv_change[1] = -1
        if change < stay:
            pass
        else:
            character.intelligence += 1
            if character.intelligence > character.intelligence_max:
                character.intelligence = character.intelligence_max
            else:
                lv_change[1] = 1
    elif instruction == 2:
        if change < down:
            character.piety -= 1
            if character.piety < 1:
                character.piety = 1
            else:
                lv_change[2] = -1
        if change < stay:
            pass
        else:
            character.piety += 1
            if character.piety > character.piety_max:
                character.piety = character.piety_max
            else:
                lv_change[2] = 1
    elif instruction == 3:
        if change < down:
            character.vitality -= 1
            if character.vitality < 1:
                character.vitality = 1
            else:
                lv_change[3] = -1
        if change < stay:
            pass
        else:
            character.vitality += 1
            if character.vitality > character.vitality_max:
                character.vitality = character.vitality_max
            else:
                lv_change[3] = 1
    elif instruction == 4:
        if change < down:
            character.agility -= 1
            if character.agility < 1:
                character.agility = 1
            else:
                lv_change[4] = -1
        if change < stay:
            pass
        else:
            character.agility += 1
            if character.agility > character.agility_max:
                character.agility = character.agility_max
            else:
                lv_change[4] = 1
    elif instruction == 5:
        if change < down:
            character.luck -= 1
            if character.luck < 1:
                character.luck = 1
            else:
                lv_change[5] = -1
        if change < stay:
            pass
        else:
            character.luck += 1
            if character.luck > character.luck_max:
                character.luck = character.luck_max
            else:
                lv_change[5] = 1

    
#if magician == 1 , then check magician_magic else check priest

def check_magic_mastered( character, magic_level, magician):

    if magic_level < 0:
        return 1

    if magician == 1:

        count = 0

        for magic in character.magic[magic_level]:
            if magic == 1:
                count += 1

        if count == 6:
            return 1
        else:
            return 0

    else:


        count = 0

        for magic in character.priest_magic[magic_level]:
            if magic == 1:
                count += 1

        if count == 6:
            return 1
        else:
            return 0
    
