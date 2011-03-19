#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sitecustomize
import sys
import struct

import character

def save( self, game_self ):

    #first save characters in bar.
    number_of_characters = len(game_self.characters)

    file = "save.dat"
    fp = open(file, "wb")
    fp.seek(0)

    #first store number of characters
    fp.write(struct.pack("i", number_of_characters))

    for chara in game_self.characters:

        
        
        uname = chara.name.encode('utf-8')
        #store length of the name
        fp.write(struct.pack( "i", len(uname)))
        #store actual name
        fp.write(struct.pack( str(len(uname)) + "s", uname))
        #store lv, align, job, and ac
        fp.write(struct.pack("4i", chara.level, chara.alignment, chara.job, chara.ac))
        #store status values
        fp.write(struct.pack("6i", chara.strength, chara.intelligence, chara.piety, chara.vitality, chara.agility, chara.luck))
        #store max status values
        fp.write(struct.pack("6i", chara.strength_max, chara.intelligence_max, chara.piety_max, chara.vitality_max, chara.agility_max, chara.luck_max))
        #store exp, next, marks, rip, age, money
        fp.write(struct.pack("6i", chara.exp, chara.next, chara.marks, chara.rip, chara.age, chara.money))

        #skip item for now...
        
        #store coordinates #length would be 3.
        for i in chara.coordinate:
            fp.write(struct.pack("i", i))        

        #store length of the status
        fp.write(struct.pack( "i", len(chara.status)))
        #store actual status
        fp.write(struct.pack( str(len(chara.status)) + "s", chara.status))

        #store hp and hp max
        fp.write(struct.pack( "2i", chara.hp, chara.max_hp))
                 
        #store mp #length would be 7
        for i in chara.magician_mp:
            fp.write(struct.pack("i", i))
        for i in chara.priest_mp:
            fp.write(struct.pack("i", i))
        for i in chara.max_magician_mp:
            fp.write(struct.pack("i", i))
        for i in chara.max_priest_mp:
            fp.write(struct.pack("i", i))

        #store learned magics
        a = 0
        for i in chara.magic:
            for j in chara.magic[a]:
                fp.write(struct.pack("i",j))
            a+=1

        a = 0
        for i in chara.priest_magic:
            for j in chara.priest_magic[a]:
                 fp.write(struct.pack("i",j))
            a+=1
        a = 0
 
    #store party members; same as characters
            
    #first store number of characters
    number_of_characters = len(game_self.party.member)
    fp.write(struct.pack("i", number_of_characters))

    for chara in game_self.party.member:
        uname = chara.name.encode('utf-8')
        #store length of the name
        fp.write(struct.pack( "i", len(uname)))
        #store actual name
        fp.write(struct.pack( str(len(uname)) + "s", uname))
        #store lv, align, job, and ac
        fp.write(struct.pack("4i", chara.level, chara.alignment, chara.job, chara.ac))
        #store status values
        fp.write(struct.pack("6i", chara.strength, chara.intelligence, chara.piety, chara.vitality, chara.agility, chara.luck))
        #store max status values
        fp.write(struct.pack("6i", chara.strength_max, chara.intelligence_max, chara.piety_max, chara.vitality_max, chara.agility_max, chara.luck_max))
        #store exp, next, marks, rip, age, money
        fp.write(struct.pack("6i", chara.exp, chara.next, chara.marks, chara.rip, chara.age, chara.money))

        #skip item for now...
        
        #store coordinates #length would be 3.
        for i in chara.coordinate:
            fp.write(struct.pack("i", i))        

        #store length of the status
        fp.write(struct.pack( "i", len(chara.status)))
        #store actual status
        fp.write(struct.pack( str(len(chara.status)) + "s", chara.status))

        #store hp and hp max
        fp.write(struct.pack( "2i", chara.hp, chara.max_hp))
                 
        #store mp #length would be 7
        for i in chara.magician_mp:
            fp.write(struct.pack("i", i))
        for i in chara.priest_mp:
            fp.write(struct.pack("i", i))
        for i in chara.max_magician_mp:
            fp.write(struct.pack("i", i))
        for i in chara.max_priest_mp:
            fp.write(struct.pack("i", i))

        #store learned magics
        a = 0
        for i in chara.magic:
            for j in chara.magic[a]:
                fp.write(struct.pack("i",j))
            a+=1

        a = 0
        for i in chara.priest_magic:
            for j in chara.priest_magic[a]:
                 fp.write(struct.pack("i",j))
            a+=1
        a = 0

    #store donated money
    fp.write(struct.pack("i", game_self.party.bar_donate))
    fp.write(struct.pack("i", game_self.party.shop_donate))
    fp.write(struct.pack("i", game_self.party.temple_donate))
    fp.write(struct.pack("i", game_self.party.castle_donate))

    #store elappsed days
    fp.write(struct.pack("i", game_self.party.days))

    #store the house level
    fp.write(struct.pack("i", game_self.party.house))

    #store the item of the banks... not yet.

    fp.truncate()


    fp.close()



def load(self, game_self):

    file = "save.dat"
    fp = open(file, "rb")
    fp.seek(0)

    game_self.characters = []

    #first load number of characters
    number_of_characters = struct.unpack("i", fp.read(struct.calcsize("i")))[0]

    for chara in range(number_of_characters):
        #load length of name
        name_length = struct.unpack("i", fp.read(struct.calcsize("i")))[0]
        name = u"" + struct.unpack( str(name_length) + "s", fp.read(struct.calcsize("s")*name_length))[0]
        
        level = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        alignment = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        job = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        ac = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]

        strength = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        intelligence = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        piety = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        vitality = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        agility = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        luck = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]

        strength_max = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        intelligence_max = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        piety_max = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        vitality_max = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        agility_max = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        luck_max = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]

        exp = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        next_exp = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        marks = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        rip = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        age = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        money = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
  
        #skip item for now...

        x = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        y = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        z = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        coordinate = [x,y,z]


        status_length = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        status = struct.unpack( str(status_length) + "s", fp.read(struct.calcsize("s")*status_length))[0]

        hp = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        max_hp = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        
        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        seven = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        magician_mp = [one,two,three,four,five,six,seven]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        seven = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        priest_mp = [one,two,three,four,five,six,seven]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        seven = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        max_magician_mp = [one,two,three,four,five,six,seven]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        seven = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        max_priest_mp = [one,two,three,four,five,six,seven]


        #load all magic
        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        magic = [[],[],[],[],[],[],[]]

        magic[0] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        magic[1] = [one,two,three,four,five,six]
        
        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        magic[2] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        magic[3] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        magic[4] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        magic[5] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        magic[6] = [one,two,three,four,five,six]

        #load all magic
        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        priest_magic = [[],[],[],[],[],[],[]]

        priest_magic[0] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        priest_magic[1] = [one,two,three,four,five,six]
        
        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        priest_magic[2] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        priest_magic[3] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        priest_magic[4] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        priest_magic[5] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        priest_magic[6] = [one,two,three,four,five,six]

        #adds each characters
        character_load = character.Character(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        character_load.load(name,level, alignment, job, ac,
                       strength,intelligence, piety, vitality, agility, luck,
                       strength_max, intelligence_max, piety_max, vitality_max, agility_max, luck_max,
                       exp, next_exp, marks, rip, age, money,
                       coordinate, status, hp, max_hp,
                       magician_mp, priest_mp, max_magician_mp, max_priest_mp, magic, priest_magic)
        game_self.characters.append(character_load)


    #do the same for party members

    #first load number of characters
    number_of_characters = struct.unpack("i", fp.read(struct.calcsize("i")))[0]

    game_self.party.member = []

    for chara in range(number_of_characters):
        #load length of name
        name_length = struct.unpack("i", fp.read(struct.calcsize("i")))[0]
        name = u"" + struct.unpack( str(name_length) + "s", fp.read(struct.calcsize("s")*name_length))[0]
        
        level = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        alignment = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        job = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        ac = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]

        strength = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        intelligence = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        piety = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        vitality = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        agility = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        luck = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]

        strength_max = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        intelligence_max = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        piety_max = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        vitality_max = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        agility_max = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        luck_max = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]

        exp = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        next_exp = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        marks = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        rip = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        age = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        money = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
  
        #skip item for now...

        x = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        y = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        z = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        coordinate = [x,y,z]

        

        status_length = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        status = struct.unpack( str(status_length) + "s", fp.read(struct.calcsize("s")*status_length))[0]

        hp = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        max_hp = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        
        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        seven = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        magician_mp = [one,two,three,four,five,six,seven]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        seven = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        priest_mp = [one,two,three,four,five,six,seven]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        seven = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        max_magician_mp = [one,two,three,four,five,six,seven]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        seven = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        max_priest_mp = [one,two,three,four,five,six,seven]


        #load all magic
        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        magic = [[],[],[],[],[],[],[]]

        magic[0] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        magic[1] = [one,two,three,four,five,six]
        
        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        magic[2] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        magic[3] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        magic[4] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        magic[5] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        magic[6] = [one,two,three,four,five,six]

        #load all magic
        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        priest_magic = [[],[],[],[],[],[],[]]

        priest_magic[0] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        priest_magic[1] = [one,two,three,four,five,six]
        
        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        priest_magic[2] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        priest_magic[3] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        priest_magic[4] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        priest_magic[5] = [one,two,three,four,five,six]

        one = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        two = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        three = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        four = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        five = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        
        six = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]        

        priest_magic[6] = [one,two,three,four,five,six]

        character_load = character.Character(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        character_load.load(name,level, alignment, job, ac,
                       strength,intelligence, piety, vitality, agility, luck,
                       strength_max, intelligence_max, piety_max, vitality_max, agility_max, luck_max,
                       exp, next_exp, marks, rip, age, money,
                       coordinate, status, hp, max_hp,
                       magician_mp, priest_mp, max_magician_mp, max_priest_mp, magic, priest_magic)
        game_self.party.member.append(character_load)


    #load donated money
    game_self.party.bar_donate = struct.unpack("i", fp.read(struct.calcsize("i")))[0]
    game_self.party.shop_donate = struct.unpack("i", fp.read(struct.calcsize("i")))[0]
    game_self.party.temple_donate = struct.unpack("i", fp.read(struct.calcsize("i")))[0]
    game_self.party.castle_donate = struct.unpack("i", fp.read(struct.calcsize("i")))[0]


    #load elappsed days
    game_self.party.days = struct.unpack("i", fp.read(struct.calcsize("i")))[0]

    #store the house level
    game_self.party.house = struct.unpack("i", fp.read(struct.calcsize("i")))[0]

    #store the item of the banks... not yet.

    
    fp.close()
    
