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

        #max hit probability
        self.attack_probability = int(item[3])
        
        #increase in damage
        self.min_damage = int(item[4])
        self.power = int(item[5])

        #how much it decreases enemy attack
        self.defense = int(item[6])

        #how much it evades enemy attack
        self.evade = int(item[7])

        #where it use when equipped
        self.equip = int(item[8])

        #how long the attack would go
        self.range = int(item[9])

        #how many times it hits enemy
        self.attack_times = int(item[10])

        #how much hp cured if used
        self.hp_cure = int(item[11])
        
        #how much mp cured if used
        self.mp_cure = int(item[12])

        #what status cured if used
        self.status_cure = int(item[13])

        #possible jobs that can use this item
        self.job = int(item[14])

        #character's alignment that can use this item
        self.person = int(item[15])

        #if the item is cursed or not
        self.curse = int(item[16])
      

        #extra status or attack status it has
        self.extra1 = int(item[17])
        self.extra2 = int(item[18])
        self.extra3 = int(item[19])

        self.description = item[20]
        self.description = self.description.strip("\"")
        self.description = unicode(self.description, encoding="sjis")

        self.id = int(item[21])

        self.break_percent = int(item[22])

        #on weapon, it adds extra status to enemy
        #on guards, it is resistance to those status
        #max 200 least 0 
        self.poison = int(item[23])
        self.mute = int(item[24])
        self.sleep = int(item[25])
        self.paralysis = int(item[26])
        self.petrify = int(item[27])
        self.death = int(item[28])
        
        self.wood_alignment = int(item[29])
        self.fire_alignment = int(item[30])
        self.earth_alignment = int(item[31])
        self.metal_alignment = int(item[32])
        self.water_alignment = int(item[33])
        self.light_alignment = int(item[34])
        self.dark_alignment = int(item[35])
        self.none_alignment = int(item[36])

        self.breath_resistance = int(item[37])

        self.extra_strength = int(item[38])
        self.extra_intelligence = int(item[39])
        self.extra_piety = int(item[40])
        self.extra_vitality = int(item[41])
        self.extra_agility = int(item[42])
        self.extra_luck = int(item[43])

        self.to_human = int(item[44])
        self.to_undead = int(item[45])
        self.to_fairy = int(item[46])
        self.to_animal = int(item[47])
        self.to_therianthrope = int(item[48])
        self.to_legendary = int(item[49])
        self.to_dragon = int(item[50])
        self.to_giant = int(item[51])
        self.to_spirit = int(item[52])
        self.to_magic = int(item[53])
        self.to_devil = int(item[54])
        self.to_demon = int(item[55])
        self.to_insect = int(item[56])
        
