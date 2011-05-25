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
            self.extra_attack.append(int(enemy[13]))
            attack_name = enemy[14]
            attack_name = attack_name.strip("\"")
            attack_name = unicode(attack_name, encoding="sjis")
            self.extra_attack.append(attack_name)



        if int(enemy[15]) > 0:
            self.extra_attack.append(int(enemy[15]))
            self.extra_attack.append(int(enemy[16]))
            self.extra_attack.append(int(enemy[17]))
            attack_name = enemy[18]
            attack_name = attack_name.strip("\"")
            attack_name = unicode(attack_name, encoding="sjis")
            self.extra_attack.append(attack_name)

        if int(enemy[19]) > 0:
            self.extra_attack.append(int(enemy[19]))
            self.extra_attack.append(int(enemy[20]))
            self.extra_attack.append(int(enemy[21]))
            attack_name = enemy[22]
            attack_name = attack_name.strip("\"")
            attack_name = unicode(attack_name, encoding="sjis")
            self.extra_attack.append(attack_name)

        if int(enemy[23]) > 0:
            self.extra_attack.append(int(enemy[23]))
            self.extra_attack.append(int(enemy[24]))
            self.extra_attack.append(int(enemy[25]))
            attack_name = enemy[26]
            attack_name = attack_name.strip("\"")
            attack_name = unicode(attack_name, encoding="sjis")
            self.extra_attack.append(attack_name)

        #it stores: probability of dropping the item
        #           and the name of the item
        self.drop_item = []

        if int(enemy[27]) > 0:
            self.drop_item.append(int(enemy[27]))
            self.drop_item.append(int(enemy[28]))
            #item_name = enemy[28]
            #item_name = item_name.strip("\"")
            #item_name = unicode(item_name, encoding="sjis")
            #self.drop_item.append(item_name)
 
        if int(enemy[29]) > 0:
            self.drop_item.append(int(enemy[29]))
            self.drop_item.append(int(enemy[30]))
            #item_name = enemy[30]
            #item_name = item_name.strip("\"")
            #item_name = unicode(item_name, encoding="sjis")
            #self.drop_item.append(item_name)

        if int(enemy[31]) > 0:
            self.drop_item.append(int(enemy[31]))
            self.drop_item.append(int(enemy[32]))
            #item_name = enemy[32]
            #item_name = item_name.strip("\"")
            #item_name = unicode(item_name, encoding="sjis")
            #self.drop_item.append(item_name)
         
        self.drop_gold = int(enemy[33])
        self.exp = int(enemy[34])

        self.magic_resistance = int(enemy[35])

        self.wood_resistance = int(enemy[36])
        self.fire_resistance = int(enemy[37])
        self.earth_resistance = int(enemy[38])
        self.metal_resistance = int(enemy[39])
        self.water_resistance = int(enemy[40])
        self.light_resistance = int(enemy[41])
        self.dark_resistance = int(enemy[42])
        self.none_resistance = int(enemy[43])

        self.attack_range = int(enemy[44])

        self.sleep_resistance = int(enemy[45])
        self.silent_resistance = int(enemy[46])
        self.poison_resistance = int(enemy[47])
        self.dead_resistance = int(enemy[48])
        self.paralysis_resistance = int(enemy[49])
        self.confuse_resistance = int(enemy[50])
        self.blind_resistance = int(enemy[51])
        
        self.level = int(enemy[52])

        self.attack_times = int(enemy[53])
        

        
   
