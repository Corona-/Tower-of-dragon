#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import random

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
NO_EXTRA, CHARACTER_VIEW, PARTY_REMOVE, CHARACTER_CHECK = 100, 101, 102, 103


SCREEN_RECTANGLE = Rect(0,0,640,480)

class Character:

    WARRIOR, FIGHTER, MAGICIAN, PRIEST,  THIEF, MERCHANT = 0, 1, 2, 3, 4, 5

    POISON, MUTE, AFRAID, ASLEEP, PALALYSIS, PETRIFIED, DEAD, ASHED, LOST = 0, 1, 2, 3, 4, 5, 6, 7, 8

    """stores information of characters"""
    def __init__(self, name, alignment, job,
                 strength, intelligence, piety, vitality, agility, luck,
                 strength_max, intelligence_max, piety_max, vitality_max, agility_max, luck_max,
                 ):
        self.name = name
        self.level = 1
        self.alignment = alignment
        self.job = job
        
        self.ac = 10
        
        self.strength = strength
        self.intelligence = intelligence
        self.piety = piety
        self.vitality = vitality
        self.agility = agility
        self.luck = luck

        self.strength_max = strength_max
        self.intelligence_max = intelligence_max
        self.piety_max = piety_max
        self.vitality_max = vitality_max
        self.agility_max = agility_max
        self.luck_max = luck_max
 
        

        self.exp = 0
        self.next = 0
        self.marks = 0
        self.rip = 0
        self.age = 18

        self.items = []
        self.item_max = 10

        #right, left, body, helmet, gauntlet and accessory
        self.equip = [ 0,0,0,0,0,0]

        #where the character is in the tower
        #-1,-1, -1 is in the bar
        self.coordinate = [-1,-1,-1]
        #stores the status of the character
        #status has POISON, PALALYSIS, ASLEEP, MUTE, PETRIFIED, DEAD, ASHED, LOST, maybe AFRAID
        self.status = [0,0,0,0,0,0,0,0,0]

        #create hp money, magics randomly
        probability = random.randint(1, 100)
        
        self.hp = 0
        self.money = 0
        self.priest_mp = [0,0,0,0,0,0,0]
        self.magician_mp = [0,0,0,0,0,0,0]
        self.magic = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.priest_magic = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        
        if self.job == self.WARRIOR:
            self.hp = random.randint(1, 10+self.vitality/2)
        elif self.job == self.FIGHTER:
            self.hp = random.randint(1, 8+self.vitality/2)
        elif self.job == self.MAGICIAN:
            self.hp = random.randint(1, 4+self.vitality/2)
            self.magician_mp = [random.randint(0, 4), 0,0,0,0,0,0]
            #each array is magic lv, if it is 1, it means character can use that magic
            self.magic = [[random.randint(0,1), random.randint(0,1), random.randint(0,1), random.randint(0,1), random.randint(0,1), random.randint(0,1)], [0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        elif self.job == self.PRIEST:
            self.hp = random.randint(1, 8+self.vitality/2)
            self.priest_mp = [random.randint(0, 4), 0,0,0,0,0,0]
            self.priest_magic = [[random.randint(0,1), random.randint(0,1), random.randint(0,1), random.randint(0,1), random.randint(0,1), random.randint(0,1)], [0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        elif self.job == self.THIEF:
            self.hp = random.randint(1, 6+self.vitality/2)
        elif self.job == self.MERCHANT:
            self.hp = random.randint(1, 6+self.vitality/2)

        self.max_hp = self.hp
        self.max_priest_mp = self.priest_mp
        self.max_magician_mp = self.magician_mp


        probability = random.randint(1, 200)
        if probability < 170:
            self.money = random.randint(1, 200)               
        elif probability < 190:
            self.money = random.randint(200, 380)                          
        elif probability <= 200:
            self.money = random.randint(380, 800)

        #ac change from permanant skill
        self.permanant_ac = 0
        #ac change from battle
        self.battle_ac = 0
        self.defend_ac = 0

        self.face_shield = 0

        self.breath_resist = 0

        self.critical_flag = 0
 
        
    def load(self, name, level, alignment, job, ac,
             strength, intelligence, piety, vitality, agility, luck,
             strength_max, intelligence_max, piety_max, vitality_max, agility_max, luck_max,
             exp, next_exp, marks, rip, age, money,
             coordinate, status, hp, max_hp,
             magician_mp, priest_mp, max_magician_mp, max_priest_mp, magic, priest_magic,
             item_list, equip_list):
        self.name = name
        self.level = level
        self.alignment = alignment
        self.job = job
        self.ac = ac

        self.strength = strength
        self.intelligence = intelligence
        self.piety = piety
        self.vitality = vitality
        self.agility = agility
        self.luck = luck
        
        self.strength_max = strength_max
        self.intelligence_max = intelligence_max
        self.piety_max = piety_max
        self.vitality_max = vitality_max
        self.agility_max = agility_max
        self.luck_max = luck_max

        self.exp = exp
        self.next_exp = next_exp
        self.marks = marks
        self.rip = rip
        self.age = 18
        self.money = money

        self.coordinate = coordinate
        self.status = status
        self.hp = hp
        self.max_hp = max_hp

        self.magician_mp = magician_mp
        self.priest_mp = priest_mp
        self.max_magician_mp = max_magician_mp
        self.max_priest_mp = max_priest_mp

        self.magic = magic
        self.priest_magic = priest_magic

        #stable
        self.item_max = 10

        self.items = item_list
        self.equip = equip_list


    
