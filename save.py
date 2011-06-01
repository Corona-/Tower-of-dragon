#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sitecustomize
import sys
import struct
import item
import shop
import character
import os

def save( self, game_self ):

    save_character(game_self)

    save_donation(game_self)

    save_game_data(game_self)

    save_stored_item(game_self)

    save_dungeon_data(game_self)

    try:
        file = "Save/shop_item_temp.dat"
        fp = open( file, "rb")
    except IOError, (errno, msg):
        pass

    else:
        fp.close()

        try:
            file = "Save/shop_item.dat"
            fp = open( file, "rb")
        except IOError, (errno, msg):
            pass
        else:
            fp.close()
            os.remove( "Save/shop_item.dat")                

        os.rename( "Save/shop_item_temp.dat", "Save/shop_item.dat")



def load(self, game_self):

    load_character(game_self)

    load_donation(game_self)

    load_game_data(game_self)

    load_stored_item(game_self)

    load_dungeon_data(game_self)


def save_character(game_self):

    file = "Save/character.dat"
    fp = open(file, "wb")
    fp.seek(0)

    #first save characters in bar.
    number_of_characters = len(game_self.characters)
    #first store number of characters
    fp.write(struct.pack("i", number_of_characters))

    for chara in game_self.characters:
        save_each_character( fp, chara)
 
    #store party members; same as characters
    #first store number of characters
    number_of_characters = len(game_self.party.member)
    fp.write(struct.pack("i", number_of_characters))

    for chara in game_self.party.member:
        save_each_character( fp, chara)

    #cut remaining space
    fp.truncate()
    fp.close()


    

def save_each_character( fp, character ):
    

    uname = character.name.encode('utf-8')
    #store length of the name
    fp.write(struct.pack( "i", len(uname)))
    #store actual name
    fp.write(struct.pack( str(len(uname)) + "s", uname))
    #store lv, align, job, and ac
    fp.write(struct.pack("4i", character.level, character.alignment, character.job, character.ac))
    #store status values
    fp.write(struct.pack("6i", character.strength, character.intelligence, character.piety, character.vitality, character.agility, character.luck))
    #store max status values
    fp.write(struct.pack("6i", character.strength_max, character.intelligence_max, character.piety_max, character.vitality_max, character.agility_max, character.luck_max))
    #store exp, next, marks, rip, age, money
    fp.write(struct.pack("6i", character.exp, character.next, character.marks, character.rip, character.age, character.money))

    #save length of item
    fp.write(struct.pack( "i", len(character.items)))

    #save id of the item
    for items in character.items:
        fp.write(struct.pack( "i", items.id))

    #save equipment, length should be 6
    for equip in character.equip:
        if isinstance( equip, item.Item):
            fp.write(struct.pack( "i", 1))
            fp.write(struct.pack( "i", equip.id))
        else:
            fp.write(struct.pack( "i", 0))
    
    #store coordinates #length would be 3.
    for i in character.coordinate:
        fp.write(struct.pack("i", i))  

    #store length of the status
    fp.write(struct.pack( "i", len(character.status)))
    #store actual status
    fp.write(struct.pack( str(len(character.status)) + "s", character.status))

    #store hp and hp max
    fp.write(struct.pack( "2i", character.hp, character.max_hp))
             
    #store mp #length would be 7
    for i in character.magician_mp:
        fp.write(struct.pack("i", i))
    for i in character.priest_mp:
        fp.write(struct.pack("i", i))
    for i in character.max_magician_mp:
        fp.write(struct.pack("i", i))
    for i in character.max_priest_mp:
        fp.write(struct.pack("i", i))

    #store learned magics
    a = 0
    for i in character.magic:
        for j in character.magic[a]:
            fp.write(struct.pack("i",j))
        a+=1

    a = 0
    for i in character.priest_magic:
        for j in character.priest_magic[a]:
             fp.write(struct.pack("i",j))
        a+=1
    a = 0

def load_character(game_self):

    file = "Save/character.dat"
    fp = open(file, "rb")
    fp.seek(0)

    game_self.characters = []

    #first load number of characters
    number_of_characters = struct.unpack("i", fp.read(struct.calcsize("i")))[0]

    for chara in range(number_of_characters):
        game_self.characters.append(load_each_character( fp, game_self))

    #do the same for party members

    #first load number of characters
    number_of_characters = struct.unpack("i", fp.read(struct.calcsize("i")))[0]

    game_self.party.member = []

    for chara in range(number_of_characters):
        game_self.party.member.append(load_each_character( fp, game_self))
    
    fp.close()

def load_each_character( fp, game_self):

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

    #load item and equip
    number_of_item = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
    item_list = []
    for items in range(number_of_item):
        itemID = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        item_list.append( item.Item( game_self.item_data[itemID] ))

    equip_list = []
    for equip in range(6):
        check = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
        if check == 1:
             equipID = struct.unpack( "i", fp.read(struct.calcsize("i")))[0]
             equip_list.append( item.Item( game_self.item_data[equipID]))
        if check == 0:
             equip_list.append(0)

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
                   magician_mp, priest_mp, max_magician_mp, max_priest_mp, magic, priest_magic,
                   item_list, equip_list)
    return character_load

def save_donation(game_self):
    
    file = "Save/donation.dat"
    fp = open(file, "wb")
    fp.seek(0)

    #store donated money
    fp.write(struct.pack("i", game_self.party.bar_donate))
    fp.write(struct.pack("i", game_self.party.shop_donate))
    fp.write(struct.pack("i", game_self.party.temple_donate))
    fp.write(struct.pack("i", game_self.party.castle_donate))

    #cut remaining space
    fp.truncate()
    fp.close()

def load_donation(game_self):

    file = "Save/donation.dat"
    fp = open(file, "rb")
    fp.seek(0)

    #load donated money
    game_self.party.bar_donate = struct.unpack("i", fp.read(struct.calcsize("i")))[0]
    game_self.party.shop_donate = struct.unpack("i", fp.read(struct.calcsize("i")))[0]
    game_self.party.temple_donate = struct.unpack("i", fp.read(struct.calcsize("i")))[0]
    game_self.party.castle_donate = struct.unpack("i", fp.read(struct.calcsize("i")))[0]

    fp.close()

def save_game_data(game_self):

    file = "Save/data.dat"
    fp = open(file, "wb")
    fp.seek(0)

    #store party alignment
    fp.write(struct.pack("i", game_self.party.alignment))
    
    #store elappsed days
    fp.write(struct.pack("i", game_self.party.days))

    #store the house level
    fp.write(struct.pack("i", game_self.party.house))

    #store party name
    uname = game_self.party.party_name.encode('utf-8')
    #store length of the name
    fp.write(struct.pack( "i", len(uname)))
    #store actual name
    fp.write(struct.pack( str(len(uname)) + "s", uname))
    

    #cut remaining space
    fp.truncate()
    fp.close()

def load_game_data(game_self):

    file = "Save/data.dat"
    fp = open(file, "rb")
    fp.seek(0)

    #load party alignment
    game_self.party.alignment = struct.unpack("i", fp.read(struct.calcsize("i")))[0]
    
    #load elappsed days
    game_self.party.days = struct.unpack("i", fp.read(struct.calcsize("i")))[0]

    #store the house level
    game_self.party.house = struct.unpack("i", fp.read(struct.calcsize("i")))[0]

    #load party name
    name_length = struct.unpack("i", fp.read(struct.calcsize("i")))[0]
    game_self.party.party_name = u"" + struct.unpack( str(name_length) + "s", fp.read(struct.calcsize("s")*name_length))[0]
  
    fp.close()

def save_stored_item(game_self):

    file = "Save/stored_item.dat"
    fp = open(file, "wb")
    fp.seek(0)

    #first save number of items
    number_of_item = len(game_self.party.inn_item)
    fp.write(struct.pack("i", number_of_item))

    for items in game_self.party.inn_item:
        #save id of the item
        fp.write(struct.pack("i", items))
        
    #first save number of items
    number_of_item = len(game_self.party.house_item)
    fp.write(struct.pack("i", number_of_item))

    for items in game_self.party.house_item:
        #save id of the item
        fp.write(struct.pack("i", items))

    #cut remaining space
    fp.truncate()
    fp.close()
    
def load_stored_item(game_self):

    file = "Save/stored_item.dat"
    fp = open(file, "rb")
    fp.seek(0)

    game_self.party.inn_item = []
    game_self.party.house_item = []

    #load number of items
    number_of_item = struct.unpack("i", fp.read(struct.calcsize("i")))[0]

    for items in range(number_of_item):
        game_self.party.inn_item.append( struct.unpack("i", fp.read(struct.calcsize("i")))[0])
        
    #load number of items
    number_of_item = struct.unpack("i", fp.read(struct.calcsize("i")))[0]

    for items in range(number_of_item):
        game_self.party.house_item.append( struct.unpack("i", fp.read(struct.calcsize("i")))[0])
      
    fp.close()


def save_shop_item(game_self, path):

    file = path
    fp = open(file, "wb")
    fp.seek(0)

    #there are 11 categories of items
    for item_list in game_self.shop.stock:
        number_of_item = len(item_list)
        fp.write(struct.pack("i", number_of_item))
        for items in item_list:
            fp.write(struct.pack("2i", items.id, items.stock))
            
    #cut remaining space
    fp.truncate()
    fp.close()

def load_shop_item(self, path):
    
    file = path
    fp = open(file, "rb")
    fp.seek(0)

    self.stock = []

    for category in range(11):
        number_of_item = struct.unpack("i", fp.read(struct.calcsize("i")))[0]
        item_list= []
        for items in range(number_of_item):
            item_id = struct.unpack("i", fp.read(struct.calcsize("i")))[0]
            stock = struct.unpack("i", fp.read(struct.calcsize("i")))[0]
            item_list.append( shop.Shop_item( item_id, stock))
        self.stock.append( item_list)

      
    fp.close()


def save_dungeon_data(game_self):
    
    file = "Save/dungeon_data.dat"
    fp = open(file, "wb")
    fp.seek(0)

    #number of item is 20x20x30

    for floor in game_self.party.dungeon_visited:
        for x in floor:
            for y in x:
                fp.write(struct.pack("i", y))




    #cut remaining space
    fp.truncate()
    fp.close()

def load_dungeon_data(game_self):

    try:
        file = "Save/dungeon_data.dat"
        fp = open(file, "rb")
    except IOError, (errno, msg):
        pass
    else:
        
        fp.seek(0)

        game_self.party.dungeon_visited = []

        for floor in range(30):
            floor_visited = []
            for x in range(20):
                row_visited = []
                for y in range(20):
                    row_visited.append( struct.unpack("i", fp.read(struct.calcsize("i")))[0])
                floor_visited.append(row_visited)
            game_self.party.dungeon_visited.append(floor_visited)

                                        
        fp.close()



