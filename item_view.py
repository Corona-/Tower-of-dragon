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

        self.menu_font = pygame.font.Font("ipag.ttf", 16)


    def draw(self, screen, game_self, character):
        """draw the item description on the screen"""

        window.Window.draw(self, screen)
        if self.is_visible == False: return

        items = character.items
        self.menu = game_self.menu.item_window.item_view.menu

        item_name_font = self.menu_font.render( u"アイテム名 " + items[self.menu].name , True, COLOR_WHITE)
     
        item_attack_font = self.menu_font.render( u"攻撃力 " + str(items[self.menu].min_damage) + u"-" + str(items[self.menu].power) , True, COLOR_WHITE)
        item_attack_time_font = self.menu_font.render( u"攻撃回数 " + str(items[self.menu].attack_times) , True, COLOR_WHITE)
        item_range_font = self.menu_font.render( u"攻撃距離 " + str(items[self.menu].range) , True, COLOR_WHITE)
        item_hit_prob_font = self.menu_font.render( u"命中率 " + str(items[self.menu].attack_probability) , True, COLOR_WHITE)

        item_price_font = self.menu_font.render( u"価値 " + str(items[self.menu].price) , True, COLOR_WHITE)

        item_evade_font = self.menu_font.render( u"AC " + str(items[self.menu].evade) , True, COLOR_WHITE)

        item_job_font = self.menu_font.render( u"装備条件" , True, COLOR_WHITE)


        item_warrior_font = self.menu_font.render( u"WAR" , True, COLOR_GLAY)
        item_fighter_font = self.menu_font.render( u"FIG" , True, COLOR_GLAY)
        item_magician_font = self.menu_font.render( u"MAG" , True, COLOR_GLAY)
        item_priest_font = self.menu_font.render( u"PRI" , True, COLOR_GLAY)
        item_thief_font = self.menu_font.render( u"THI" , True, COLOR_GLAY)
        item_merchant_font = self.menu_font.render( u"MER" , True, COLOR_GLAY)
        item_lord_font = self.menu_font.render( u"LOR" , True, COLOR_GLAY)
        item_sword_font = self.menu_font.render( u"SWO" , True, COLOR_GLAY)
        item_mad_font = self.menu_font.render( u"MAD" , True, COLOR_GLAY)
        item_master_font = self.menu_font.render( u"MAS" , True, COLOR_GLAY)
        item_general_font = self.menu_font.render( u"GEN" , True, COLOR_GLAY)
        item_murderer_font = self.menu_font.render( u"MUR" , True, COLOR_GLAY)
        item_rune_font = self.menu_font.render( u"RUN" , True, COLOR_GLAY)
        item_sage_font = self.menu_font.render( u"SAG" , True, COLOR_GLAY)
        item_sorcerer_font = self.menu_font.render( u"SOR" , True, COLOR_GLAY)
        item_pope_font = self.menu_font.render( u"POP" , True, COLOR_GLAY)
        item_bishop_font = self.menu_font.render( u"BIS" , True, COLOR_GLAY)
        item_fanatic_font = self.menu_font.render( u"FAN" , True, COLOR_GLAY)
        item_chivalrous_font = self.menu_font.render( u"CHI" , True, COLOR_GLAY)
        item_phantom_font = self.menu_font.render( u"PHA" , True, COLOR_GLAY)
        item_ninja_font = self.menu_font.render( u"NIN" , True, COLOR_GLAY)
        item_guild_font = self.menu_font.render( u"GUI" , True, COLOR_GLAY)
        item_armed_font = self.menu_font.render( u"ARM" , True, COLOR_GLAY)
        item_money_font = self.menu_font.render( u"MON" , True, COLOR_GLAY)


        if items[self.menu].job == self.WARRIOR:
            item_warrior_font = self.menu_font.render( u"WAR" , True, COLOR_WHITE)
            item_lord_font = self.menu_font.render( u"LOR" , True, COLOR_WHITE)
            item_sword_font = self.menu_font.render( u"SWO" , True, COLOR_WHITE)
            item_mad_font = self.menu_font.render( u"MAD" , True, COLOR_WHITE)
        elif items[self.menu].job == self.FIGHTER:
            item_fighter_font = self.menu_font.render( u"FIG" , True, COLOR_WHITE)
            item_master_font = self.menu_font.render( u"MAS" , True, COLOR_WHITE)
            item_general_font = self.menu_font.render( u"GEN" , True, COLOR_WHITE)
            item_murderer_font = self.menu_font.render( u"MUR" , True, COLOR_WHITE)
        elif items[self.menu].job == self.MAGICIAN:
            item_magician_font = self.menu_font.render( u"MAG" , True, COLOR_WHITE)
            item_rune_font = self.menu_font.render( u"RUN" , True, COLOR_WHITE)
            item_sage_font = self.menu_font.render( u"SAG" , True, COLOR_WHITE)
            item_sorcerer_font = self.menu_font.render( u"SOR" , True, COLOR_WHITE)
        elif items[self.menu].job == self.PRIEST:
            item_priest_font = self.menu_font.render( u"PRI" , True, COLOR_WHITE)
            item_pope_font = self.menu_font.render( u"POP" , True, COLOR_WHITE)
            item_bishop_font = self.menu_font.render( u"BIS" , True, COLOR_WHITE)
            item_fanatic_font = self.menu_font.render( u"FAN" , True, COLOR_WHITE)
        elif items[self.menu].job == self.THIEF:
            item_thief_font = self.menu_font.render( u"THI" , True, COLOR_WHITE)
            item_chivalrous_font = self.menu_font.render( u"CHI" , True, COLOR_WHITE)
            item_phantom_font = self.menu_font.render( u"PHA" , True, COLOR_WHITE)
            item_ninja_font = self.menu_font.render( u"NIN" , True, COLOR_WHITE)
        elif items[self.menu].job == self.MERCHANT:
            item_merchant_font = self.menu_font.render( u"MER" , True, COLOR_WHITE)
            item_guild_font = self.menu_font.render( u"GUI" , True, COLOR_WHITE)
            item_armed_font = self.menu_font.render( u"ARM" , True, COLOR_WHITE)
            item_money_font = self.menu_font.render( u"MON" , True, COLOR_WHITE)
        elif items[self.menu].job == self.LORD:            
            item_lord_font = self.menu_font.render( u"LOR" , True, COLOR_WHITE)
        elif items[self.menu].job == self.SWORDMASTER:
            item_sword_font = self.menu_font.render( u"SWO" , True, COLOR_WHITE)
        elif items[self.menu].job == self.MADOVERLORD:
            item_mad_font = self.menu_font.render( u"MAD" , True, COLOR_WHITE)
        elif items[self.menu].job == self.MASTERSWORDSMAN:
            item_master_font = self.menu_font.render( u"MAS" , True, COLOR_WHITE)
        elif items[self.menu].job == self.GENERAL:
            item_general_font = self.menu_font.render( u"GEN" , True, COLOR_WHITE)
        elif items[self.menu].job == self.MURDERER:
            item_murderer_font = self.menu_font.render( u"MUR" , True, COLOR_WHITE)
        elif items[self.menu].job == self.RUNESWORDSMAN:
            item_rune_font = self.menu_font.render( u"RUN" , True, COLOR_WHITE)
        elif items[self.menu].job == self.SAGE:
            item_sage_font = self.menu_font.render( u"SAG" , True, COLOR_WHITE)
        elif items[self.menu].job == self.SORCERER:
            item_sorcerer_font = self.menu_font.render( u"SOR" , True, COLOR_WHITE)
        elif items[self.menu].job == self.POPE:
            item_pope_font = self.menu_font.render( u"POP" , True, COLOR_WHITE)
        elif items[self.menu].job == self.BISHOP:
            item_bishop_font = self.menu_font.render( u"BIS" , True, COLOR_WHITE)
        elif items[self.menu].job == self.FANATIC:
            item_fanatic_font = self.menu_font.render( u"FAN" , True, COLOR_WHITE)
        elif items[self.menu].job == self.CHIVALROUSTHIEF:
            item_chivalrous_font = self.menu_font.render( u"CHI" , True, COLOR_WHITE)
        elif items[self.menu].job == self.PHANTOMTHIEF:
            item_phantom_font = self.menu_font.render( u"PHA" , True, COLOR_WHITE)
        elif items[self.menu].job == self.NINJA:
            item_ninja_font = self.menu_font.render( u"NIN" , True, COLOR_WHITE)
        elif items[self.menu].job == self.GUILDMASTER:
            item_guild_font = self.menu_font.render( u"GUI" , True, COLOR_WHITE)
        elif items[self.menu].job == self.ARMEDMERCHANT:
            item_armed_font = self.menu_font.render( u"ARM" , True, COLOR_WHITE)
        elif items[self.menu].job == self.MONEYLENDER:
            item_money_font = self.menu_font.render( u"MON" , True, COLOR_WHITE)
        elif items[self.menu].job == 100:
            item_warrior_font = self.menu_font.render( u"WAR" , True, COLOR_WHITE)
            item_fighter_font = self.menu_font.render( u"FIG" , True, COLOR_WHITE)
            item_magician_font = self.menu_font.render( u"MAG" , True, COLOR_WHITE)
            item_priest_font = self.menu_font.render( u"PRI" , True, COLOR_WHITE)
            item_thief_font = self.menu_font.render( u"THI" , True, COLOR_WHITE)
            item_merchant_font = self.menu_font.render( u"MER" , True, COLOR_WHITE)
            item_lord_font = self.menu_font.render( u"LOR" , True, COLOR_WHITE)
            item_sword_font = self.menu_font.render( u"SWO" , True, COLOR_WHITE)
            item_mad_font = self.menu_font.render( u"MAD" , True, COLOR_WHITE)
            item_master_font = self.menu_font.render( u"MAS" , True, COLOR_WHITE)
            item_general_font = self.menu_font.render( u"GEN" , True, COLOR_WHITE)
            item_murderer_font = self.menu_font.render( u"MUR" , True, COLOR_WHITE)
            item_rune_font = self.menu_font.render( u"RUN" , True, COLOR_WHITE)
            item_sage_font = self.menu_font.render( u"SAG" , True, COLOR_WHITE)
            item_sorcerer_font = self.menu_font.render( u"SOR" , True, COLOR_WHITE)
            item_pope_font = self.menu_font.render( u"POP" , True, COLOR_WHITE)
            item_bishop_font = self.menu_font.render( u"BIS" , True, COLOR_WHITE)
            item_fanatic_font = self.menu_font.render( u"FAN" , True, COLOR_WHITE)
            item_chivalrous_font = self.menu_font.render( u"CHI" , True, COLOR_WHITE)
            item_phantom_font = self.menu_font.render( u"PHA" , True, COLOR_WHITE)
            item_ninja_font = self.menu_font.render( u"NIN" , True, COLOR_WHITE)
            item_guild_font = self.menu_font.render( u"GUI" , True, COLOR_WHITE)
            item_armed_font = self.menu_font.render( u"ARM" , True, COLOR_WHITE)
            item_money_font = self.menu_font.render( u"MON" , True, COLOR_WHITE)

        item_good_font = self.menu_font.render( u"善" , True, COLOR_GLAY)
        item_neutral_font = self.menu_font.render( u"中立" , True, COLOR_GLAY)
        item_evil_font = self.menu_font.render( u"悪" , True, COLOR_GLAY)

        if items[self.menu].person == self.GOOD:
            item_good_font = self.menu_font.render( u"善" , True, COLOR_WHITE)
        elif items[self.menu].person == self.NEUTRAL:
            item_neutral_font = self.menu_font.render( u"中立" , True, COLOR_WHITE)
        elif items[self.menu].person == self.EVIL:
            item_evil_font = self.menu_font.render( u"悪" , True, COLOR_WHITE)

        else:
            item_good_font = self.menu_font.render( u"善" , True, COLOR_WHITE)
            item_neutral_font = self.menu_font.render( u"中立" , True, COLOR_WHITE)
            item_evil_font = self.menu_font.render( u"悪" , True, COLOR_WHITE)

##        #item.curse
##        #need to change to fit in, cut by some amount of words
##        item_description_font = self.menu_font.render( items[self.menu].description , True, COLOR_WHITE)

        item_state_font = self.menu_font.render( u"状態異常", True, COLOR_WHITE)

        if items[self.menu].poison > 0:
            item_poison_font = self.menu_font.render( u"猛毒", True, COLOR_WHITE)
        else:
            item_poison_font = self.menu_font.render( u"猛毒", True, COLOR_GLAY)
        if items[self.menu].mute > 0:
            item_mute_font = self.menu_font.render( u"沈黙", True, COLOR_WHITE)
        else:
            item_mute_font = self.menu_font.render( u"沈黙", True, COLOR_GLAY)
        if items[self.menu].sleep > 0:
            item_sleep_font = self.menu_font.render( u"睡眠", True, COLOR_WHITE)
        else:
            item_sleep_font = self.menu_font.render( u"睡眠", True, COLOR_GLAY)
        if items[self.menu].paralysis > 0:
            item_paraly_font = self.menu_font.render( u"麻痺", True, COLOR_WHITE)
        else:
            item_paraly_font = self.menu_font.render( u"麻痺", True, COLOR_GLAY)
        if items[self.menu].petrify > 0:
            item_petrif_font = self.menu_font.render( u"石化", True, COLOR_WHITE)
        else:
            item_petrif_font = self.menu_font.render( u"石化", True, COLOR_GLAY)
        if items[self.menu].death > 0:
            item_death_font = self.menu_font.render( u"即死", True, COLOR_WHITE)
        else:
            item_death_font = self.menu_font.render( u"即死", True, COLOR_GLAY)

        item_alignment_font = self.menu_font.render( u"属性", True, COLOR_WHITE)

        if items[self.menu].wood_alignment > 0:
            item_wood_font = self.menu_font.render( u"木", True, COLOR_WHITE)
        else:
            item_wood_font = self.menu_font.render( u"木", True, COLOR_GLAY)
        if items[self.menu].fire_alignment > 0:
            item_fire_font = self.menu_font.render( u"火", True, COLOR_WHITE)
        else:
            item_fire_font = self.menu_font.render( u"火", True, COLOR_GLAY)
        if items[self.menu].earth_alignment > 0:
            item_earth_font = self.menu_font.render( u"地", True, COLOR_WHITE)
        else:
            item_earth_font = self.menu_font.render( u"地", True, COLOR_GLAY)
        if items[self.menu].metal_alignment > 0:
            item_metal_font = self.menu_font.render( u"金", True, COLOR_WHITE)
        else:
            item_metal_font = self.menu_font.render( u"金", True, COLOR_GLAY)
        if items[self.menu].water_alignment > 0:
            item_water_font = self.menu_font.render( u"水", True, COLOR_WHITE)
        else:
            item_water_font = self.menu_font.render( u"水", True, COLOR_GLAY)
        if items[self.menu].light_alignment > 0:
            item_light_font = self.menu_font.render( u"光", True, COLOR_WHITE)
        else:
            item_light_font = self.menu_font.render( u"光", True, COLOR_GLAY)
        if items[self.menu].dark_alignment > 0:
            item_dark_font = self.menu_font.render( u"闇", True, COLOR_WHITE)
        else:
            item_dark_font = self.menu_font.render( u"闇", True, COLOR_GLAY)
        if items[self.menu].none_alignment > 0:
            item_none_font = self.menu_font.render( u"無", True, COLOR_WHITE)
        else:
            item_none_font = self.menu_font.render( u"無", True, COLOR_GLAY)

        item_change_status_font = self.menu_font.render( u"能力変化", True, COLOR_WHITE)
        item_str_font = self.menu_font.render( "STR+" + str(items[self.menu].extra_strength), True, COLOR_WHITE)
        item_int_font = self.menu_font.render( "INT+" + str(items[self.menu].extra_intelligence), True, COLOR_WHITE)
        item_pie_font = self.menu_font.render( "PIE+" + str(items[self.menu].extra_piety), True, COLOR_WHITE)
        item_vit_font = self.menu_font.render( "VIT+" + str(items[self.menu].extra_vitality), True, COLOR_WHITE)
        item_agi_font = self.menu_font.render( "AGI+" + str(items[self.menu].extra_agility), True, COLOR_WHITE)
        item_luc_font = self.menu_font.render( "LUC+" + str(items[self.menu].extra_luck), True, COLOR_WHITE)
         
        item_enemy_category_font = self.menu_font.render( u"対種族", True, COLOR_WHITE)

        if items[self.menu].to_human > 0:
            item_human_font = self.menu_font.render( u"人間", True, COLOR_WHITE)
        else:
            item_human_font = self.menu_font.render( u"人間", True, COLOR_GLAY)
        if items[self.menu].to_undead > 0:
            item_undead_font = self.menu_font.render( u"アンデッド", True, COLOR_WHITE)
        else:
            item_undead_font = self.menu_font.render( u"アンデッド", True, COLOR_GLAY)
        if items[self.menu].to_fairy > 0:
            item_fairy_font = self.menu_font.render( u"妖精", True, COLOR_WHITE)
        else:
            item_fairy_font = self.menu_font.render( u"妖精", True, COLOR_GLAY)
        if items[self.menu].to_animal > 0:
            item_animal_font = self.menu_font.render( u"動物", True, COLOR_WHITE)
        else:
            item_animal_font = self.menu_font.render( u"動物", True, COLOR_GLAY)
        if items[self.menu].to_therianthrope > 0:
            item_therian_font = self.menu_font.render( u"獣人", True, COLOR_WHITE)
        else:
            item_therian_font = self.menu_font.render( u"獣人", True, COLOR_GLAY)
        if items[self.menu].to_legendary > 0:
            item_legend_font = self.menu_font.render( u"神話獣", True, COLOR_WHITE)
        else:
            item_legend_font = self.menu_font.render( u"神話獣", True, COLOR_GLAY)
        if items[self.menu].to_dragon > 0:
            item_dragon_font = self.menu_font.render( u"ドラゴン", True, COLOR_WHITE)
        else:
            item_dragon_font = self.menu_font.render( u"ドラゴン", True, COLOR_GLAY)
        if items[self.menu].to_giant > 0:
            item_giant_font = self.menu_font.render( u"巨人", True, COLOR_WHITE)
        else:
            item_giant_font = self.menu_font.render( u"巨人", True, COLOR_GLAY)
        if items[self.menu].to_spirit > 0:
            item_spirit_font = self.menu_font.render( u"精霊", True, COLOR_WHITE)
        else:
            item_spirit_font = self.menu_font.render( u"精霊", True, COLOR_GLAY)
        if items[self.menu].to_magic > 0:
            item_magic_font = self.menu_font.render( u"魔法生物", True, COLOR_WHITE)
        else:
            item_magic_font = self.menu_font.render( u"魔法生物", True, COLOR_GLAY)
        if items[self.menu].to_devil > 0:
            item_devil_font = self.menu_font.render( u"悪魔", True, COLOR_WHITE)
        else:
            item_devil_font = self.menu_font.render( u"悪魔", True, COLOR_GLAY)
        if items[self.menu].to_demon > 0:
            item_demon_font = self.menu_font.render( u"鬼", True, COLOR_WHITE)
        else:
            item_demon_font = self.menu_font.render( u"鬼", True, COLOR_GLAY)
        if items[self.menu].to_insect > 0:
            item_insect_font = self.menu_font.render( u"昆虫", True, COLOR_WHITE)
        else:
            item_insect_font = self.menu_font.render( u"昆虫", True, COLOR_GLAY)
            


        screen.blit( item_name_font, (40,40))
        
        screen.blit( item_attack_font, (40,80))
        screen.blit( item_attack_time_font, (200,80))
        screen.blit( item_range_font, (330,80))
        screen.blit( item_hit_prob_font, (40,120))
        screen.blit( item_price_font, (200,120))
        screen.blit( item_evade_font, (40,160))


        screen.blit( item_job_font, (40,200))
        screen.blit( item_warrior_font, (40,270))
        screen.blit( item_lord_font, (80,270))
        screen.blit( item_sword_font, (120,270))
        screen.blit( item_mad_font, (160,270))

        screen.blit( item_fighter_font, (40,300))
        screen.blit( item_master_font, (80,300))
        screen.blit( item_general_font, (120,300))
        screen.blit( item_murderer_font, (160,300))

        screen.blit( item_magician_font, (40,330))
        screen.blit( item_rune_font, (80,330))
        screen.blit( item_sage_font, (120,330))
        screen.blit( item_sorcerer_font, (160,330))

        screen.blit( item_priest_font, (40,360))
        screen.blit( item_pope_font, (80,360))
        screen.blit( item_bishop_font, (120,360))
        screen.blit( item_fanatic_font, (160,360))

        screen.blit( item_thief_font, (40,390))
        screen.blit( item_chivalrous_font, (80,390))
        screen.blit( item_ninja_font, (120,390))
        screen.blit( item_phantom_font, (160,390))

        screen.blit( item_merchant_font, (40,420))
        screen.blit( item_guild_font, (80,420))
        screen.blit( item_armed_font, (120,420))
        screen.blit( item_money_font, (160,420))

        
        screen.blit( item_good_font, (40,230))
        screen.blit( item_neutral_font, (80,230))
        screen.blit( item_evil_font, (140,230))

        screen.blit( item_state_font, (440,160))
        screen.blit( item_poison_font, (400,200))
        screen.blit( item_mute_font, (460,200))
        screen.blit( item_sleep_font, (520,200))
        screen.blit( item_paraly_font, (400,230))
        screen.blit( item_petrif_font, (460,230))
        screen.blit( item_death_font, (520,230))

        screen.blit( item_alignment_font, (280,160))
        screen.blit( item_wood_font, (220,200))
        screen.blit( item_fire_font, (250,200))
        screen.blit( item_earth_font, (280,200))
        screen.blit( item_metal_font, (310,200))
        screen.blit( item_water_font, (340,200))
        screen.blit( item_light_font, (250,230))
        screen.blit( item_dark_font, (280,230))
        screen.blit( item_none_font, (310,230))


        screen.blit( item_change_status_font, (230,270))
        screen.blit( item_str_font, (240,300))
        screen.blit( item_int_font, (240,320))
        screen.blit( item_pie_font, (240,340))
        screen.blit( item_vit_font, (240,360))
        screen.blit( item_agi_font, (240,380))
        screen.blit( item_luc_font, (240,400))

        screen.blit( item_enemy_category_font, (470,270))
        screen.blit( item_human_font, (350,300))
        screen.blit( item_undead_font, (400,300))
        screen.blit( item_fairy_font, (500,300))
        screen.blit( item_animal_font, (570,300))
        screen.blit( item_therian_font, (350,330))
        screen.blit( item_legend_font, (400,330))
        screen.blit( item_dragon_font, (500,330))
        screen.blit( item_giant_font, (570,330))
        screen.blit( item_spirit_font, (350,360))
        screen.blit( item_magic_font, (400,360))
        screen.blit( item_devil_font, (500,360))
        screen.blit( item_demon_font, (570,360))
        screen.blit( item_insect_font, (350,390))
         
    def item_view_window_handler(self, game_self, event, character):

        if event.type == KEYDOWN and (event.key == K_z or event.key == K_x or event.key == K_SPACE or event.key == K_RETURN):
            self.is_visible = False
