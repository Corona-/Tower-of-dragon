#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

class Item:

    def __init__(self, name, price, power, attack_times, length, evade, guard, alignment, equip, job, person, curse, extra, enemy, bonus):

        self.name = name

        self.price = price
        #increase in damage
        self.power = power
        #how many times it hits enemy
        self.attack_times = attack_times
        #how long the attack would go
        self.length = length
        #how much it evades enemy attack
        self.evade = evade
        #how much it decreases enemy attack
        self.guard = guard
        #attack alignment ex.fire, water , etc
        self.alignment = alignment

        #where it use when equipped
        self.equip = equip
        #possible jobs that can use this item
        self.job = job

        #character's alignment that can use this item
        self.person = person
        #if the item is cursed or not
        self.curse = curse

        #extra status or attack status it has
        self.extra = extra

        #it works better on some enemy?
        self.enemy = enemy

        #bonus points on status?
        self.bonus = bonus

        

