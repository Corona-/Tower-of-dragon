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
    DEVIL, DEMON = 10, 11

    NONE, LIGHT, DARK = 0, 1, 2
    WOOD, FIRE, EARTH, METAL, WATER = 3, 4, 5, 6, 7

    def __init__(self, enemy):
        self.name = enemy[0]

        self.name = self.name.strip("\"")
        self.name = unicode(self.name, encoding="sjis")

        self.category = int(enemy[1])    
        self.level = 0

        self.alignment = int(enemy[2])

        self.hp = int(enemy[3])
        self.max_hp = int(enemy[3])

        self.ac = int(enemy[4])

        self.status = "OK"

        self.strength = int(enemy[5])
        self.intelligence = int(enemy[6])
        self.piety = int(enemy[7])
        self.vitality = int(enemy[8])
        self.agility = int(enemy[9])
        self.luck = int(enemy[10])

        #it stores: probability of attack
        #           strength of the attack
        #           and the string of the attack
        self.extra_attack = []

        if int(enemy[11]) > 0:
            self.extra_attack.append(int(enemy[11]))
            self.extra_attack.append(int(enemy[12]))
            attack_name = enemy[13]
            attack_name = attack_name.strip("\"")
            attack_name = unicode(attack_name, encoding="sjis")
            self.extra_attack.append(attack_name)



        if int(enemy[14]) > 0:
            self.extra_attack.append(int(enemy[14]))
            self.extra_attack.append(int(enemy[15]))
            attack_name = enemy[16]
            attack_name = attack_name.strip("\"")
            attack_name = unicode(attack_name, encoding="sjis")
            self.extra_attack.append(attack_name)

        if int(enemy[17]) > 0:
            self.extra_attack.append(int(enemy[17]))
            self.extra_attack.append(int(enemy[18]))
            attack_name = enemy[19]
            attack_name = attack_name.strip("\"")
            attack_name = unicode(attack_name, encoding="sjis")
            self.extra_attack.append(attack_name)

        if int(enemy[20]) > 0:
            self.extra_attack.append(int(enemy[20]))
            self.extra_attack.append(int(enemy[21]))
            attack_name = enemy[22]
            attack_name = attack_name.strip("\"")
            attack_name = unicode(attack_name, encoding="sjis")
            self.extra_attack.append(attack_name)

        #it stores: probability of dropping the item
        #           and the name of the item
        self.drop_item = []

        if int(enemy[23]) > 0:
            self.extra_attack.append(int(enemy[23]))
            item_name = enemy[24]
            item_name = item_name.strip("\"")
            item_name = unicode(item_name, encoding="sjis")
            self.drop_item.append(item_name)
 
        if int(enemy[25]) > 0:
            self.extra_attack.append(int(enemy[25]))
            item_name = enemy[26]
            item_name = item_name.strip("\"")
            item_name = unicode(item_name, encoding="sjis")
            self.drop_item.append(item_name)

        if int(enemy[27]) > 0:
            self.extra_attack.append(int(enemy[27]))
            item_name = enemy[28]
            item_name = item_name.strip("\"")
            item_name = unicode(item_name, encoding="sjis")
            self.drop_item.append(item_name)
         
        self.drop_gold = int(enemy[29])
        self.exp = int(enemy[30])

        self.magic_resistance = int(enemy[31])

        self.wood_resistance = int(enemy[32])
        self.fire_resistance = int(enemy[33])
        self.earth_resistance = int(enemy[34])
        self.metal_resistance = int(enemy[35])
        self.water_resistance = int(enemy[36])
        self.light_resistance = int(enemy[37])
        self.dark_resistance = int(enemy[38])
        self.none_resistance = int(enemy[39])

        

        
   
