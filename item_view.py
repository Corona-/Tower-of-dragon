#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import easygui
import string
import window
import item

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10

MENU = 12

SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

class Item_view(window.Window):
    
    GOOD, NEUTRAL, EVIL = 1, 0, -1
    WARRIOR, FIGHTER, MAGICIAN, PRIEST, THIEF, MERCHANT = 0, 1, 2, 3, 4, 5
    LORD, SWORDMASTER, MADOVERLORD = 10,11,12
    MASTERSWORDSMAN, GENERAL, MURDERER = 13,14,15
    RUNESWORDSMAN, SAGE, SORCERER = 16,17,18
    POPE, BISHOP, FANATIC = 19,20,21
    CHIVALROUSTHIEF, PHANTOMTHIEF, NINJA = 22,23,24
    GUILDMASTER, ARMEDMERCHANT, MONEYLENDER = 25, 26,27


    def __init__(self, rectangle):
        window.Window.__init__(self, rectangle)
        self.is_visible = False
        
        self.menu = 0

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)
        self.item_font = pygame.font.Font("ipag.ttf", 16)


    def draw(self, screen, game_self, character):
        """draw the item description on the screen"""

        window.Window.draw(self, screen)
        if self.is_visible == False: return

        items = character.items
        self.menu = game_self.menu.item_window.item_view.menu

        item_name_font = self.menu_font.render( u"アイテム名 " + items[self.menu].name , True, COLOR_WHITE)
     
        item_attack_font = self.menu_font.render( u"攻撃力 " + str(items[self.menu].power) , True, COLOR_WHITE)
        item_attack_time_font = self.menu_font.render( u"攻撃回数 " + str(items[self.menu].attack_times) , True, COLOR_WHITE)
        item_range_font = self.menu_font.render( u"攻撃距離 " + str(items[self.menu].range) , True, COLOR_WHITE)
        item_hit_prob_font = self.menu_font.render( u"命中率 " + str(items[self.menu].evade) , True, COLOR_WHITE)

        item_price_font = self.menu_font.render( u"価値 " + str(items[self.menu].price) , True, COLOR_WHITE)

        item_evade_font = self.menu_font.render( u"AC " + str(items[self.menu].evade) , True, COLOR_WHITE)

        item_job_font = self.menu_font.render( u"使用可能職業" , True, COLOR_WHITE)


        item_warrior_font = self.menu_font.render( u"戦士" , True, COLOR_GLAY)
        item_fighter_font = self.menu_font.render( u"武士" , True, COLOR_GLAY)
        item_magician_font = self.menu_font.render( u"魔術師" , True, COLOR_GLAY)
        item_priest_font = self.menu_font.render( u"僧侶" , True, COLOR_GLAY)
        item_thief_font = self.menu_font.render( u"盗賊" , True, COLOR_GLAY)
        item_merchant_font = self.menu_font.render( u"商人" , True, COLOR_GLAY)
        item_lord_font = self.menu_font.render( u"君主" , True, COLOR_GLAY)
        item_sword_font = self.menu_font.render( u"ソードマスター" , True, COLOR_GLAY)
        item_mad_font = self.menu_font.render( u"狂王" , True, COLOR_GLAY)
        item_master_font = self.menu_font.render( u"剣聖" , True, COLOR_GLAY)
        item_general_font = self.menu_font.render( u"大将" , True, COLOR_GLAY)
        item_murderer_font = self.menu_font.render( u"ヒトキリ" , True, COLOR_GLAY)
        item_rune_font = self.menu_font.render( u"魔法戦士" , True, COLOR_GLAY)
        item_sage_font = self.menu_font.render( u"大魔導" , True, COLOR_GLAY)
        item_sorcerer_font = self.menu_font.render( u"邪術師" , True, COLOR_GLAY)
        item_pope_font = self.menu_font.render( u"法王" , True, COLOR_GLAY)
        item_bishop_font = self.menu_font.render( u"司祭" , True, COLOR_GLAY)
        item_fanatic_font = self.menu_font.render( u"狂信者" , True, COLOR_GLAY)
        item_chivalrous_font = self.menu_font.render( u"義賊" , True, COLOR_GLAY)
        item_phantom_font = self.menu_font.render( u"怪盗" , True, COLOR_GLAY)
        item_ninja_font = self.menu_font.render( u"忍者" , True, COLOR_GLAY)
        item_guild_font = self.menu_font.render( u"ギルドマスター" , True, COLOR_GLAY)
        item_armed_font = self.menu_font.render( u"武装商人" , True, COLOR_GLAY)
        item_money_font = self.menu_font.render( u"高利貸し" , True, COLOR_GLAY)


        if items[self.menu].job == self.WARRIOR:
            item_warrior_font = self.menu_font.render( u"戦士" , True, COLOR_WHITE)
            item_lord_font = self.menu_font.render( u"君主" , True, COLOR_WHITE)
            item_sword_font = self.menu_font.render( u"ソードマスター" , True, COLOR_WHITE)
            item_mad_font = self.menu_font.render( u"狂王" , True, COLOR_WHITE)
        elif items[self.menu].job == self.FIGHTER:
            item_fighter_font = self.menu_font.render( u"武士" , True, COLOR_WHITE)
            item_master_font = self.menu_font.render( u"剣聖" , True, COLOR_WHITE)
            item_general_font = self.menu_font.render( u"大将" , True, COLOR_WHITE)
            item_murderer_font = self.menu_font.render( u"ヒトキリ" , True, COLOR_WHITE)
        elif items[self.menu].job == self.MAGICIAN:
            item_magician_font = self.menu_font.render( u"魔術師" , True, COLOR_WHITE)
            item_rune_font = self.menu_font.render( u"魔法戦士" , True, COLOR_WHITE)
            item_sage_font = self.menu_font.render( u"大魔導" , True, COLOR_WHITE)
            item_sorcerer_font = self.menu_font.render( u"邪術師" , True, COLOR_WHITE)
        elif items[self.menu].job == self.PRIEST:
            item_priest_font = self.menu_font.render( u"僧侶" , True, COLOR_WHITE)
            item_pope_font = self.menu_font.render( u"法王" , True, COLOR_WHITE)
            item_bishop_font = self.menu_font.render( u"司祭" , True, COLOR_WHITE)
            item_fanatic_font = self.menu_font.render( u"狂信者" , True, COLOR_WHITE)
        elif items[self.menu].job == self.THIEF:
            item_thief_font = self.menu_font.render( u"盗賊" , True, COLOR_WHITE)
            item_chivalrous_font = self.menu_font.render( u"義賊" , True, COLOR_WHITE)
            item_phantom_font = self.menu_font.render( u"怪盗" , True, COLOR_WHITE)
            item_ninja_font = self.menu_font.render( u"忍者" , True, COLOR_WHITE)
        elif items[self.menu].job == self.MERCHANT:
            item_merchant_font = self.menu_font.render( u"商人" , True, COLOR_WHITE)
            item_guild_font = self.menu_font.render( u"ギルドマスター" , True, COLOR_WHITE)
            item_armed_font = self.menu_font.render( u"武装商人" , True, COLOR_WHITE)
            item_money_font = self.menu_font.render( u"高利貸し" , True, COLOR_WHITE)
        elif items[self.menu].job == self.LORD:            
            item_lord_font = self.menu_font.render( u"君主" , True, COLOR_WHITE)
        elif items[self.menu].job == self.SWORDMASTER:
            item_sword_font = self.menu_font.render( u"ソードマスター" , True, COLOR_WHITE)
        elif items[self.menu].job == self.MADOVERLORD:
            item_mad_font = self.menu_font.render( u"狂王" , True, COLOR_WHITE)
        elif items[self.menu].job == self.MASTERSWORDSMAN:
            item_master_font = self.menu_font.render( u"剣聖" , True, COLOR_WHITE)
        elif items[self.menu].job == self.GENERAL:
            item_general_font = self.menu_font.render( u"大将" , True, COLOR_WHITE)
        elif items[self.menu].job == self.MURDERER:
            item_murderer_font = self.menu_font.render( u"ヒトキリ" , True, COLOR_WHITE)
        elif items[self.menu].job == self.RUNESWORDSMAN:
            item_rune_font = self.menu_font.render( u"魔法戦士" , True, COLOR_WHITE)
        elif items[self.menu].job == self.SAGE:
            item_sage_font = self.menu_font.render( u"大魔導" , True, COLOR_WHITE)
        elif items[self.menu].job == self.SORCERER:
            item_sorcerer_font = self.menu_font.render( u"邪術師" , True, COLOR_WHITE)
        elif items[self.menu].job == self.POPE:
            item_pope_font = self.menu_font.render( u"法王" , True, COLOR_WHITE)
        elif items[self.menu].job == self.BISHOP:
            item_bishop_font = self.menu_font.render( u"司祭" , True, COLOR_WHITE)
        elif items[self.menu].job == self.FANATIC:
            item_fanatic_font = self.menu_font.render( u"狂信者" , True, COLOR_WHITE)
        elif items[self.menu].job == self.CHIVALROUSTHIEF:
            item_chivalrous_font = self.menu_font.render( u"義賊" , True, COLOR_WHITE)
        elif items[self.menu].job == self.PHANTOMTHIEF:
            item_phantom_font = self.menu_font.render( u"怪盗" , True, COLOR_WHITE)
        elif items[self.menu].job == self.NINJA:
            item_ninja_font = self.menu_font.render( u"忍者" , True, COLOR_WHITE)
        elif items[self.menu].job == self.GUILDMASTER:
            item_guild_font = self.menu_font.render( u"ギルドマスター" , True, COLOR_WHITE)
        elif items[self.menu].job == self.ARMEDMERCHANT:
            item_armed_font = self.menu_font.render( u"武装商人" , True, COLOR_WHITE)
        elif items[self.menu].job == self.MONEYLENDER:
            item_money_font = self.menu_font.render( u"高利貸し" , True, COLOR_WHITE)
        elif items[self.menu].job == 100:
            item_warrior_font = self.menu_font.render( u"戦士" , True, COLOR_WHITE)
            item_fighter_font = self.menu_font.render( u"武士" , True, COLOR_WHITE)
            item_magician_font = self.menu_font.render( u"魔術師" , True, COLOR_WHITE)
            item_priest_font = self.menu_font.render( u"僧侶" , True, COLOR_WHITE)
            item_thief_font = self.menu_font.render( u"盗賊" , True, COLOR_WHITE)
            item_merchant_font = self.menu_font.render( u"商人" , True, COLOR_WHITE)
            item_lord_font = self.menu_font.render( u"君主" , True, COLOR_GLAY)
            item_sword_font = self.menu_font.render( u"ソードマスター" , True, COLOR_WHITE)
            item_mad_font = self.menu_font.render( u"狂王" , True, COLOR_WHITE)
            item_master_font = self.menu_font.render( u"剣聖" , True, COLOR_WHITE)
            item_general_font = self.menu_font.render( u"大将" , True, COLOR_WHITE)
            item_murderer_font = self.menu_font.render( u"ヒトキリ" , True, COLOR_WHITE)
            item_rune_font = self.menu_font.render( u"魔法戦士" , True, COLOR_WHITE)
            item_sage_font = self.menu_font.render( u"大魔導" , True, COLOR_WHITE)
            item_sorcerer_font = self.menu_font.render( u"邪術師" , True, COLOR_WHITE)
            item_pope_font = self.menu_font.render( u"法王" , True, COLOR_WHITE)
            item_bishop_font = self.menu_font.render( u"司祭" , True, COLOR_WHITE)
            item_fanatic_font = self.menu_font.render( u"狂信者" , True, COLOR_WHITE)
            item_chivalrous_font = self.menu_font.render( u"義賊" , True, COLOR_WHITE)
            item_phantom_font = self.menu_font.render( u"怪盗" , True, COLOR_WHITE)
            item_ninja_font = self.menu_font.render( u"忍者" , True, COLOR_WHITE)
            item_guild_font = self.menu_font.render( u"ギルドマスター" , True, COLOR_WHITE)
            item_armed_font = self.menu_font.render( u"武装商人" , True, COLOR_WHITE)
            item_money_font = self.menu_font.render( u"高利貸し" , True, COLOR_WHITE)

        item_good_font = self.menu_font.render( u"善" , True, COLOR_GLAY)
        item_neutral_font = self.menu_font.render( u"中立" , True, COLOR_GLAY)
        item_evil_font = self.menu_font.render( u"悪" , True, COLOR_GLAY)

        if items[self.menu].person == self.GOOD:
            item_good_font = self.menu_font.render( u"善" , True, COLOR_WHITE)
        elif items[self.menu].person == self.NEUTRAL:
            item_neutral_font = self.menu_font.render( u"中立" , True, COLOR_WHITE)
        elif items[self.menu].person == self.EVIL:
            item_evil_font = self.menu_font.render( u"悪" , True, COLOR_WHITE)
        #if there is more than one add here
##        elif items[self.menu].person == :
        

## may add different columns on item data
##        item_category_font = self.menu_font.render( str(items[self.menu].category) , True, COLOR_WHITE)

##        item_alignment_font = self.menu_font.render( str(items[self.menu].alignment) , True, COLOR_WHITE)
##        
##        #item.curse
##        #need to change to fit in, cut by some amount of words
##        item_description_font = self.menu_font.render( items[self.menu].description , True, COLOR_WHITE)


        screen.blit( item_name_font, (40,40))
        
        screen.blit( item_attack_font, (40,120))
        screen.blit( item_attack_time_font, (160,120))
        screen.blit( item_range_font, (280,120))
        screen.blit( item_hit_prob_font, (40,160))
        screen.blit( item_price_font, (160,160))
        screen.blit( item_evade_font, (40,200))



    def item_view_window_handler(self, game_self, event, character):

        if event.type == KEYDOWN and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
            self.is_visible = False
