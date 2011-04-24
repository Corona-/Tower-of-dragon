#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window
import random

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
        self.inn_not_enough.is_visible = True
    else:
        if inn:
            game_self.party.member[self.menu].money -= payment        
        game_self.party.member[self.menu].magician_mp = game_self.party.member[self.menu].max_magician_mp
        game_self.party.member[self.menu].priest_mp = game_self.party.member[self.menu].max_priest_mp

        if rest_level > 0 and cure == 0:
            cure = 1
        game_self.party.member[self.menu].hp += cure
        if game_self.party.member[self.menu].hp > game_self.party.member[self.menu].max_hp:
            game_self.party.member[self.menu].hp = game_self.party.member[self.menu].max_hp


#calculate the exp needed
#need to find better way to calculate exp
def calc_exp_needed(self, character):
    necessary_exp = int(100*1.75*character.level)  
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
        hp_changed = random.randint(1, (character.level*10+character.vitality/2))
    elif character.job == 1 or character.job == 3:
        hp_changed = random.randint(1, (character.level*8+character.vitality/2))
    elif character.job == 4 or character.job == 5:
        hp_changed = random.randint(1, (character.level*6+character.vitality/2))
    elif character.job == 2:
        hp_changed = random.randint(1, (character.level*4+character.vitality/2))

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

            for mp in character.magician_mp:
                #if that level magic is learned add mp
                if mp > 0:
                    magic_change = random.randint(0, 2)
                    character.magician_mp[i] += magic_change
                    if character.magician_mp[i] > 9:
                        character.magician_mp[i] = 9
                else:
                    #learn new magic lv
                    if magic_lv_up == 0:
                        if character.job == 2:
                            learn = random.randint(0,1)
                            character.magician_mp[i] += learn
                            magic_lv_up = 1
                i += 1

            character.max_magician_mp = character.magician_mp

            #learn new magic
            i = 0
            j = 0
            learn = 0
            for a in character.magic:
                for b in character.magic[i]:
                    if b == 0 and character.magician_mp[i] > 0:
                        learn = random.randint(1, 3)
                        if learn == 3:
                            character.magic[i][j] = 1
                    j += 1
                i += 1
                j = 0

            if learn == 3:
                lv_change[7] = 1
            

        #PRIEST
        if character.job == 3:
            magic_lv_up = 0
            i = 0
            for mp in character.priest_mp:
                if mp > 0:
                    priest_change = random.randint(0, 2)
                    character.priest_mp[i] += priest_change
                    if character.priest_mp[i] > 9:
                        character.priest_mp[i] = 9
                else:
                    #learn new magic lv
                    if magic_lv_up == 0:
                        if character.job == 3:
                            learn = random.randint(0,1)
                            character.priest_mp[i] += learn
                            magic_lv_up = 1
                i += 1

            character.max_priest_mp = character.priest_mp

            #learn new magic

            i = 0
            j = 0
            learn = 0
            for a in character.priest_magic:
                for b in character.priest_magic[i]:
                    if b == 0 and character.priest_mp[i] > 0:
                        learn = random.randint(1, 3)
                        if learn == 3:
                            character.priest_magic[i][j] = 1
                    j += 1
                i += 1
                j = 0

            
            if learn == 3:
                lv_change[7] = 1

#strength,intelligence,piety,vitality,agility,luck = 0,1,2,3,4,5
#change stores which status changed,
#0=str,1=int,2=pie,3=vit,4=agi,5=luc,6=hp,7=magic
def status_change( self, change, down, stay, character, instruction, lv_change):

    if instruction == 0:
        if change < down:
            character.strength -= 1
            if character.strength < 1:
                charcter.strength = 1
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

    
