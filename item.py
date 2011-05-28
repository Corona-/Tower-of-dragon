#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

class Item:

    def __init__(self, item):

        self.name = item[0]

        self.name = self.name.strip("\"")
        self.name = unicode(self.name, encoding="sjis")
        
        self.category = int(item[1])

        self.price = int(item[2])
        #increase in damage
        self.power = int(item[3])

        #how much it decreases enemy attack
        self.defense = int(item[4])

        #how much it evades enemy attack
        #on weapon, how much it hits enemy
        self.evade = int(item[5])

        #where it use when equipped
        self.equip = int(item[6])

        #how long the attack would go
        self.range = int(item[7])

        #how many times it hits enemy
        self.attack_times = int(item[8])

        #how much hp cured if used
        self.hp_cure = int(item[9])
        
        #how much mp cured if used
        self.mp_cure = int(item[10])

        #what status cured if used
        self.status_cure = int(item[11])

        #possible jobs that can use this item
        self.job = int(item[12])

        #character's alignment that can use this item
        self.person = int(item[13])

        #attack alignment ex.fire, water , etc
        self.alignment = int(item[14])

        #strength and weaknesses
        self.weakness = int(item[15])
        self.strength = int(item[16])

        #if the item is cursed or not
        self.curse = int(item[17])
      

        #extra status or attack status it has
        self.extra1 = int(item[18])
        self.extra2 = int(item[19])
        self.extra3 = int(item[20])

        #bonus points on status?
        self.bonus = int(item[21])

        self.description = item[22]
        self.description = self.description.strip("\"")
        self.description = unicode(self.description, encoding="sjis")

        self.id = int(item[23])

        self.break_percent = int(item[24])

        self.attack_extra = int(item[25])
        self.attack_extra_percent = int(item[26])

        

