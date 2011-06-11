#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import random

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
NO_EXTRA, CHARACTER_VIEW, PARTY_REMOVE, CHARACTER_CHECK = 100, 101, 102, 103


SCREEN_RECTANGLE = Rect(0,0,640,480)


class Enemy:

    HUMAN, UNDEAD, FAIRY, ANIMAL, THERIANTHROPE = 0, 1, 2, 3, 4
    LEGENDARY, DRAGON, GIANT, SPIRIT, MAGIC = 5, 6, 7, 8, 9
    DEVIL, DEMON, INSECT = 10, 11, 12

    NONE, LIGHT, DARK = 0, 1, 2
    WOOD, FIRE, EARTH, METAL, WATER = 3, 4, 5, 6, 7

    def __init__(self, enemy):
        self.name = enemy[0]

        self.name = self.name.strip("\"")
        self.name = unicode(self.name, encoding="sjis")

        self.category = int(enemy[1])    
        self.level = 0

        self.alignment = int(enemy[2])

        self.min_hp = int(enemy[3])
        self.hp = int(enemy[4])

        self.hp = random.randint(self.min_hp, self.hp)
        self.max_hp = int(enemy[4])

        self.ac = int(enemy[5])

        self.status = [0,0,0,0,0,0,0,0,0]

        self.strength = int(enemy[6])
        self.intelligence = int(enemy[7])
        self.piety = int(enemy[8])
        self.vitality = int(enemy[9])
        self.agility = int(enemy[10])
        self.luck = int(enemy[11])

        #it stores: probability of attack
        #           strength of the attack
        #           and the string of the attack
        self.extra_attack = []

        if int(enemy[12]) > 0:
            self.extra_attack.append(int(enemy[12]))
            self.extra_attack.append(int(enemy[13]))
            target_name = enemy[14]
            target_name = target_name.strip("\"")
            self.extra_attack.append(target_name)
            attack_name = enemy[15]
            attack_name = attack_name.strip("\"")
            attack_name = unicode(attack_name, encoding="sjis")
            self.extra_attack.append(attack_name)



        if int(enemy[16]) > 0:
            self.extra_attack.append(int(enemy[16]))
            self.extra_attack.append(int(enemy[17]))
            target_name = enemy[18]
            target_name = target_name.strip("\"")
            self.extra_attack.append(target_name)

            attack_name = enemy[19]
            attack_name = attack_name.strip("\"")
            attack_name = unicode(attack_name, encoding="sjis")
            self.extra_attack.append(attack_name)

        if int(enemy[20]) > 0:
            self.extra_attack.append(int(enemy[20]))
            self.extra_attack.append(int(enemy[21]))
            target_name = enemy[22]
            target_name = target_name.strip("\"")
            self.extra_attack.append(target_name)

            attack_name = enemy[23]
            attack_name = attack_name.strip("\"")
            attack_name = unicode(attack_name, encoding="sjis")
            self.extra_attack.append(attack_name)

        if int(enemy[24]) > 0:
            self.extra_attack.append(int(enemy[24]))
            self.extra_attack.append(int(enemy[25]))
            target_name = enemy[26]
            target_name = target_name.strip("\"")
            self.extra_attack.append(target_name)

            attack_name = enemy[27]
            attack_name = attack_name.strip("\"")
            attack_name = unicode(attack_name, encoding="sjis")
            self.extra_attack.append(attack_name)

        #it stores: probability of dropping the item
        #           and the name of the item
        self.drop_item = []

        if int(enemy[28]) > 0:
            self.drop_item.append(int(enemy[28]))
            self.drop_item.append(int(enemy[29]))
            #item_name = enemy[28]
            #item_name = item_name.strip("\"")
            #item_name = unicode(item_name, encoding="sjis")
            #self.drop_item.append(item_name)
 
        if int(enemy[30]) > 0:
            self.drop_item.append(int(enemy[30]))
            self.drop_item.append(int(enemy[31]))
            #item_name = enemy[30]
            #item_name = item_name.strip("\"")
            #item_name = unicode(item_name, encoding="sjis")
            #self.drop_item.append(item_name)

        if int(enemy[32]) > 0:
            self.drop_item.append(int(enemy[32]))
            self.drop_item.append(int(enemy[33]))
            #item_name = enemy[32]
            #item_name = item_name.strip("\"")
            #item_name = unicode(item_name, encoding="sjis")
            #self.drop_item.append(item_name)
         
        self.drop_gold = int(enemy[34])
        self.exp = int(enemy[35])

        self.magic_resistance = int(enemy[36])

        self.wood_resistance = int(enemy[37])
        self.fire_resistance = int(enemy[38])
        self.earth_resistance = int(enemy[39])
        self.metal_resistance = int(enemy[40])
        self.water_resistance = int(enemy[41])
        self.light_resistance = int(enemy[42])
        self.dark_resistance = int(enemy[43])
        self.none_resistance = int(enemy[44])

        self.attack_range = int(enemy[45])

        self.sleep_resistance = int(enemy[46])
        self.silent_resistance = int(enemy[47])
        self.poison_resistance = int(enemy[48])
        self.dead_resistance = int(enemy[49])
        self.paralysis_resistance = int(enemy[50])
        self.confuse_resistance = int(enemy[51])
        self.blind_resistance = int(enemy[52])
        
        self.level = int(enemy[53])

        self.attack_times = int(enemy[54])
        

        
   
