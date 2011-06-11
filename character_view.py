#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import easygui
import string
import window
import item
import dungeon

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
DUNGEON = 100


MENU = 12

SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)



class Character_view(window.Window):

    GOOD, NEUTRAL, EVIL = 1, 0, -1
    WARRIOR, FIGHTER, MAGICIAN,PRIEST, THIEF, MERCHANT = 0, 1, 2, 3, 4, 5
    LORD, SWORDMASTER, MADOVERLORD = 10,11,12
    MASTERSWORDSMAN, GENERAL, MURDERER = 13,14,15
    RUNESWORDSMAN, SAGE, SORCERER = 16,17,18
    POPE, BISHOP, FANATIC = 19,20,21
    CHIVALROUSTHIEF, PHANTOMTHIEF, NINJA = 22,23,24
    GUILDMASTER, ARMEDMERCHANT, MONEYLENDER = 25, 26,27


    #from castle
    DELETE, RENAME= 0, 1
    #from bar
    ADD, REMOVE, CHECK = 2, 3, 4
    #from shop
    CURSE = 5

    CONTINUE_DUNGEON = 6
    
    MENU_MAX = 9

    def __init__(self, rectangle, instruction):
        window.Window.__init__(self, rectangle)
        self.is_visible = False
        
        self.menu = 0
        self.page = 0

        #what to do
        self.instruction = instruction

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

    def draw(self, screen, character):
            """draw the window on the screen"""
            window.Window.draw(self, screen)        
            if self.is_visible == False: return

            top_font = self.menu_font.render( u"冒険者一覧", True, COLOR_WHITE)      
            screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+20))

            if self.instruction == self.DELETE:
                instruction_font = self.menu_font.render( u"誰を街から追放しますか？", True, COLOR_WHITE)      
                instruction_window = window.Window(Rect(20,20, 30+instruction_font.get_width(), 50))
                instruction_window.draw(screen)
                screen.blit(instruction_font, ( 35 , 35))
            elif self.instruction == self.RENAME:
                instruction_font = self.menu_font.render( u"誰の名前を変えますか？", True, COLOR_WHITE)      
                instruction_window = window.Window(Rect(20,20, 30+instruction_font.get_width(), 50))
                instruction_window.draw(screen)
                screen.blit(instruction_font, ( 35 , 35))
            elif self.instruction == self.ADD:
                instruction_font = self.menu_font.render( u"誰をパーティに誘いますか？", True, COLOR_WHITE)      
                instruction_window = window.Window(Rect(20,20, 30+instruction_font.get_width(), 50))
                instruction_window.draw(screen)
                screen.blit(instruction_font, ( 35 , 35))
            elif self.instruction == self.REMOVE:
                instruction_font = self.menu_font.render( u"誰をパーティから外しますか？", True, COLOR_WHITE)      
                instruction_window = window.Window(Rect(20,20, 30+instruction_font.get_width(), 50))
                instruction_window.draw(screen)
                screen.blit(instruction_font, ( 35 , 35))
            elif self.instruction == self.CONTINUE_DUNGEON:
                instruction_font = self.menu_font.render( u"調査を再開", True, COLOR_WHITE)      
                instruction_window = window.Window(Rect(20,20, 30+instruction_font.get_width(), 50))
                instruction_window.draw(screen)
                screen.blit(instruction_font, ( 35 , 35))
                
                

            if character != []:
                #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
                #the height depends on the size of font
                pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+47+30*self.menu,(self.right-self.left)-8,25), 0)

            i = 0
            for chara in character[self.page*10:(self.page+1)*10]:
                character_font = self.menu_font.render(chara.name, True, COLOR_WHITE)
                screen.blit(character_font, (self.left+20, self.top+50+(i%10)*30))                                         
                level_font = self.menu_font.render("LV" + str(chara.level), True, COLOR_WHITE)
                screen.blit(level_font, (self.right - 100, self.top+50+(i%10)*30))                                         

                align = None
                job = None
                if chara.alignment == self.GOOD:
                    align = "G"
                elif chara.alignment == self.NEUTRAL:
                    align = "N"
                elif chara.alignment == self.EVIL:
                    align = "E"

                if chara.job == self.WARRIOR:
                    job = "WAR"
                elif chara.job == self.FIGHTER:
                    job = "FIG"
                elif chara.job == self.MAGICIAN:
                    job = "MAG"
                elif chara.job == self.PRIEST:
                    job = "PRI"
                elif chara.job == self.THIEF:
                    job = "THI"
                elif chara.job == self.MERCHANT:
                    job = "MER"
                elif chara.job == self.LORD:
                    job = "LOR"
                elif chara.job == self.SWORDMASTER:
                    job = "SWO"
                elif chara.job == self.MADOVERLORD:
                    job = "MAD"
                elif chara.job == self.MASTERSWORDSMAN:
                    job = "MAS"
                elif chara.job == self.GENERAL:
                    job = "GEN"
                elif chara.job == self.MURDERER:
                    job = "MUR"
                elif chara.job == self.RUNESWORDSMAN:
                    job = "RUN"
                elif chara.job == self.SAGE:
                    job = "SAG"
                elif chara.job == self.SORCERER:
                    job = "SOR"
                elif chara.job == self.POPE:
                    job = "POP"
                elif chara.job == self.BISHOP:
                    job = "BIS"
                elif chara.job == self.FANATIC:
                    job = "FAN"
                elif chara.job == self.GUILDMASTER:
                    job = "GUI"
                elif chara.job == self.ARMEDMERCHANT:
                    job = "ARM"
                elif chara.job == self.MONEYLENDER:
                    job = "MON"
                elif chara.job == self.CHIVALROUSTHIEF:
                    job = "CHI"
                elif chara.job == self.PHANTOMTHIEF:
                    job = "PHA"
                elif chara.job == self.NINJA:
                    job = "NIN"

                total = align + "-" + job
                total_font = self.menu_font.render(total, True, COLOR_WHITE)
                screen.blit(total_font, (self.centerx, self.top+50+(i%10)*30))              
                i+=1
                



    def character_view_handler(self, game_self, event, character):
        if event.type == KEYDOWN and event.key == K_x:
            self.menu = 0
            self.page = 0
            self.is_visible = False

        if event.type == KEYDOWN and event.key == K_UP: #moves the cursor up
            self.menu -= 1
            if self.menu < 0:
                self.menu = 0
        elif event.type == KEYDOWN and event.key == K_DOWN:
            if len(character) > self.menu+self.page*10+1:
                self.menu += 1
                if self.menu > self.MENU_MAX:
                    self.menu = self.MENU_MAX
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            if len(character) > (self.page+1)*10:
                self.page += 1
                self.menu = 0
        elif event.type == KEYDOWN and event.key == K_LEFT:
            if self.page > 0:
                self.page -= 1
                self.menu = 0

        elif  event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
            if len(character) == 0: return
            if self.instruction == self.DELETE:
                game_self.castle.delete_confirm.is_visible = True
            elif self.instruction == self.RENAME:
                character_name_message = u"名前を入力してください（8文字制限）"
                message_title = u"名前入力"
                fieldnames = [u"名前"]
                fieldvalues = []
                
                fieldvalues = easygui.multenterbox(character_name_message, message_title, fieldnames)

                if (fieldvalues != None):
                    #if length is > 8 or empty string, then re-enter
                    if len(fieldvalues[0]) > 8 or len(fieldvalues[0]) == 0:
                        return
                    #if it includes spaces, then also re-enter
                    if fieldvalues[0][0] == " ":
                        return
                if fieldvalues == None: return

                character[game_self.castle.character_rename.menu + game_self.castle.character_rename.page*10].name = u"" + fieldvalues[0]                
         
            elif self.instruction == self.ADD:
                if len(game_self.party.member) < 6:
                    if (game_self.party.alignment >= 0 and game_self.characters[game_self.bar.party_add.menu+game_self.bar.party_add.page*10].alignment > 0) or (game_self.party.alignment <= 0 and game_self.characters[game_self.bar.party_add.menu+game_self.bar.party_add.page*10].alignment < 0) or game_self.characters[game_self.bar.party_add.menu+game_self.bar.party_add.page*10].alignment == 0 :
                        game_self.party.member.append(game_self.characters[game_self.bar.party_add.menu + game_self.bar.party_add.page*10])
                        game_self.party.alignment += game_self.characters[game_self.bar.party_add.menu + game_self.bar.party_add.page*10].alignment
                        print game_self.party.alignment
                        del game_self.characters[game_self.bar.party_add.menu + game_self.bar.party_add.page*10]
                        if (game_self.bar.party_add.menu + game_self.bar.party_add.page*10)+1 > len(character):
                            game_self.bar.party_add.menu -=1
                            #if that page has no more, go back to previous page and set cursor to bottom
                            if game_self.bar.party_add.menu < 0:
                                game_self.bar.party_add.menu = 9
                                game_self.bar.party_add.page -= 1
            elif self.instruction == self.REMOVE:
                if len(game_self.party.member) > 0:
                    game_self.characters.append(game_self.party.member[game_self.bar.party_remove.menu + game_self.bar.party_remove.page*10])
                    game_self.party.alignment -= game_self.party.member[game_self.bar.party_remove.menu + game_self.bar.party_remove.page*10].alignment
                    del game_self.party.member[game_self.bar.party_remove.menu + game_self.bar.party_remove.page*10]
                    if (game_self.bar.party_remove.menu + game_self.bar.party_remove.page*10)+1 > len(character):
                        game_self.bar.party_remove.menu -=1
            elif self.instruction == self.CHECK:
                game_self.bar.status_view.is_visible = True
                game_self.bar.status_view.menu = self.menu

            elif self.instruction == self.CONTINUE_DUNGEON:
                #store current party in bar
                for chara in game_self.party.member:
                    game_self.characters.append(chara)
    
                game_self.party.member = []
                game_self.party.alignment = 0

                game_self.party.member.append( game_self.tower.dungeon_alive_characters[self.menu + self.page*10])

                game_self.party.alignment += game_self.party.member[0].alignment

                i = 0
                for chara in game_self.dungeon_characters:
                    if chara == game_self.party.member[0]:
                        del game_self.dungeon_characters[i]
                    i+= 1

                #initialize dungeon                
                game_self.game_state = DUNGEON
                game_self.dungeon = dungeon.Dungeon(game_self.party.member[0].coordinate[2])
                game_self.tower = None

                


class Delete_confirm_window(window.Window):

    YES, NO = 0, 1
    MENU_MAX = 1

    
    def __init__(self, rectangle):
        window.Window.__init__(self, rectangle)
        self.is_visible = False
        self.menu = self.YES

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

    def draw(self, screen):
         """draw the window on the screen"""
         window.Window.draw(self, screen)        
         if self.is_visible == False: return

         confirm_font = self.menu_font.render( u"本当に追放しますか？", True, COLOR_WHITE) 
         yes_font = self.menu_font.render( u"はい", True, COLOR_WHITE) 
         no_font = self.menu_font.render( u"いいえ", True, COLOR_WHITE) 

         if self.menu == self.YES:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+45,(self.right-self.left)-8,30), 0)
         elif self.menu == self.NO:
             pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+75,(self.right-self.left)-8,30), 0)


         screen.blit(confirm_font, ( self.centerx - confirm_font.get_width()/2 , self.top + 20))
         screen.blit(yes_font, ( self.centerx - yes_font.get_width()/2 , self.top + 50))
         screen.blit(no_font, ( self.centerx - no_font.get_width()/2 , self.top + 80))


    def delete_confirm_window_handler(self, game_self, event, character):
        if event.type == KEYDOWN and event.key == K_UP: #moves the cursor up
            self.menu -= 1
            if self.menu < 0:
                self.menu = self.MENU_MAX
        elif event.type == KEYDOWN and event.key == K_DOWN:
                self.menu += 1
                if self.menu > self.MENU_MAX:
                    self.menu = 0

        if event.type == KEYDOWN and event.key == K_x:
            self.menu = 0
            self.is_visible = False


        elif  event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
            if len(character) == 0: return
            if self.menu == self.YES:
                del character[game_self.castle.character_delete.menu + game_self.castle.character_delete.page*10]
                if (game_self.castle.character_delete.menu + game_self.castle.character_delete.page*10)+1 > len(character):
                    game_self.castle.character_delete.menu -=1
            game_self.castle.delete_confirm.is_visible = False


class Status_view_window(window.Window):

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
    

    def draw(self, screen, character):
            """draw the window on the screen"""
            window.Window.draw(self, screen)        
            if self.is_visible == False: return

            #setup fonts
            character_name_font = self.menu_font.render( character[self.menu].name , True, COLOR_WHITE)
            character_level_font = self.menu_font.render( "LV" + str(character[self.menu].level) , True, COLOR_WHITE)

            if character[self.menu].alignment == self.GOOD:
                alignment_font = "G"
            elif character[self.menu].alignment == self.NEUTRAL:
                alignment_font = "N"
            elif character[self.menu].alignment == self.EVIL:
                alignment_font = "E"

            if character[self.menu].job == self.WARRIOR:  
                job_font = "WAR"
            elif character[self.menu].job == self.FIGHTER:
                job_font = "FIG"
            elif character[self.menu].job == self.MAGICIAN:
                job_font = "MAG"
            elif character[self.menu].job == self.PRIEST:
                job_font = "PRI"
            elif character[self.menu].job == self.THIEF:
                job_font = "THI"
            elif character[self.menu].job == self.MERCHANT:
                job_font = "MER"
            elif character[self.menu].job == self.LORD:  
                job_font = "LOR"
            elif character[self.menu].job == self.SWORDMASTER:  
                job_font = "SWO"
            elif character[self.menu].job == self.MADOVERLORD:  
                job_font = "MAD"
            elif character[self.menu].job == self.MASTERSWORDSMAN:  
                job_font = "MAS"
            elif character[self.menu].job == self.GENERAL:  
                job_font = "GEN"
            elif character[self.menu].job == self.MURDERER:  
                job_font = "MUR"
            elif character[self.menu].job == self.RUNESWORDSMAN:  
                job_font = "RUN"
            elif character[self.menu].job == self.SAGE:  
                job_font = "SAG"
            elif character[self.menu].job == self.SORCERER:  
                job_font = "SOR"
            elif character[self.menu].job == self.POPE:  
                job_font = "POP"
            elif character[self.menu].job == self.BISHOP:  
                job_font = "BIS"
            elif character[self.menu].job == self.FANATIC:  
                job_font = "FAN"
            elif character[self.menu].job == self.GUILDMASTER:  
                job_font = "GUI"
            elif character[self.menu].job == self.ARMEDMERCHANT:  
                job_font = "ARM"
            elif character[self.menu].job == self.MONEYLENDER:  
                job_font = "MON"
            elif character[self.menu].job == self.CHIVALROUSTHIEF:  
                job_font = "CHI"
            elif character[self.menu].job == self.PHANTOMTHIEF:  
                job_font = "PHA"
            elif character[self.menu].job == self.NINJA:  
                job_font = "NIN"


            exp_font = self.menu_font.render( u"経験値：", True, COLOR_WHITE)
            marks_font = self.menu_font.render( u"MARKS:", True, COLOR_WHITE)
            gold_font = self.menu_font.render( u"お金：", True, COLOR_WHITE)
            rip_font = self.menu_font.render( u"RIP：", True, COLOR_WHITE)
            ac_font = self.menu_font.render( u"AC：", True, COLOR_WHITE)
            age_font = self.menu_font.render( u"年齢：", True, COLOR_WHITE)

            character_alignment_font = self.menu_font.render( alignment_font + "-" + job_font , True, COLOR_WHITE)
            character_exp_font = self.menu_font.render( str(character[self.menu].exp) , True, COLOR_WHITE)
            character_gold_font = self.menu_font.render( str(character[self.menu].money) , True, COLOR_WHITE)
            character_marks_font = self.menu_font.render( str(character[self.menu].marks), True, COLOR_WHITE)
            character_rip_font = self.menu_font.render( str(character[self.menu].rip) , True, COLOR_WHITE)
            character_ac_font = self.menu_font.render( str(character[self.menu].ac), True, COLOR_WHITE)
            character_age_font = self.menu_font.render( str(character[self.menu].age) , True, COLOR_WHITE)


            hp_font = self.menu_font.render( u"HP：", True, COLOR_WHITE)
            status_font = self.menu_font.render( u"状態：", True, COLOR_WHITE)

            character_hp_font = self.menu_font.render( str(character[self.menu].hp) + "/" + str(character[self.menu].max_hp), True, COLOR_WHITE)

            if character[self.menu].status == [0,0,0,0,0,0,0,0,0]:
                character_status_font = self.menu_font.render( "OK" , True, COLOR_WHITE)
            i = 0
            for st in character[self.menu].status:
                if i == 0 and st > 0:
                    character_status_font = self.menu_font.render( "POISON", True, COLOR_WHITE)
                if i == 1 and st > 0:
                    character_status_font = self.menu_font.render( "MUTE", True, COLOR_WHITE)
                if i == 2 and st > 0:
                    character_status_font = self.menu_font.render( "AFRAID", True, COLOR_WHITE)
                if i == 3 and st > 0:
                    character_status_font = self.menu_font.render( "ASLEEP", True, COLOR_WHITE)
                if i == 4 and st > 0:
                    character_status_font = self.menu_font.render( "PALALY", True, COLOR_WHITE)
                if i == 5 and st > 0:
                    character_status_font = self.menu_font.render( "PETRIF", True, COLOR_WHITE)
                if i == 6 and st > 0:
                    character_status_font = self.menu_font.render( "DEAD", True, COLOR_WHITE)
                if i == 7 and st > 0:
                    character_status_font = self.menu_font.render( "ASHED", True, COLOR_WHITE)
                if i == 8 and st > 0:
                    character_status_font = self.menu_font.render( "LOST", True, COLOR_WHITE)
                i+= 1




            strength_font = self.menu_font.render( u"力：", True, COLOR_WHITE)
            intelligence_font = self.menu_font.render( u"知恵：", True, COLOR_WHITE)
            piety_font = self.menu_font.render( u"信仰：", True, COLOR_WHITE)
            vitality_font = self.menu_font.render( u"生命力：", True, COLOR_WHITE)
            agility_font = self.menu_font.render( u"素早さ：", True, COLOR_WHITE)
            luck_font = self.menu_font.render( u"運：", True, COLOR_WHITE)

            character_strength_font = self.menu_font.render( str(character[self.menu].strength), True, COLOR_WHITE)
            character_intelligence_font = self.menu_font.render( str(character[self.menu].intelligence) , True, COLOR_WHITE)
            character_piety_font = self.menu_font.render( str(character[self.menu].piety), True, COLOR_WHITE)
            character_vitality_font = self.menu_font.render( str(character[self.menu].vitality) , True, COLOR_WHITE)
            character_agility_font = self.menu_font.render( str(character[self.menu].agility), True, COLOR_WHITE)
            character_luck_font = self.menu_font.render( str(character[self.menu].luck) , True, COLOR_WHITE)

            magic_font = self.menu_font.render( u"魔術：", True, COLOR_WHITE)
            priest_magic_font = self.menu_font.render( u"僧侶：", True, COLOR_WHITE)

            character_magic_font = self.menu_font.render( str(character[self.menu].magician_mp[0]) + "/" + str(character[self.menu].magician_mp[1]) + "/" + str(character[self.menu].magician_mp[2]) + "/" +str(character[self.menu].magician_mp[3]) + "/" + str(character[self.menu].magician_mp[4]) + "/" +str(character[self.menu].magician_mp[5]) + "/" + str(character[self.menu].magician_mp[6]) , True, COLOR_WHITE)
            character_priest_magic_font = self.menu_font.render( str(character[self.menu].priest_mp[0]) + "/" + str(character[self.menu].priest_mp[1]) + "/" + str(character[self.menu].priest_mp[2]) + "/" +str(character[self.menu].priest_mp[3]) + "/" + str(character[self.menu].priest_mp[4]) + "/" +str(character[self.menu].priest_mp[5]) + "/" + str(character[self.menu].priest_mp[6]) , True, COLOR_WHITE)

            #draw the status fonts onto screen
            screen.blit(character_name_font, ( 50 , 50))
            screen.blit(character_level_font, (250, 50))                                         
            screen.blit(character_alignment_font, ( 390 , 50))

            screen.blit(strength_font, ( 50 , 110))
            screen.blit(intelligence_font, ( 50 , 140))
            screen.blit(piety_font, ( 50 , 170))
            screen.blit(vitality_font, ( 50 , 200))
            screen.blit(agility_font, ( 50 , 230))
            screen.blit(luck_font, ( 50 , 260))

            screen.blit(character_strength_font, ( 150 , 110))
            screen.blit(character_intelligence_font, (150, 140))                                         
            screen.blit(character_piety_font, ( 150 , 170))
            screen.blit(character_vitality_font, (150, 200))                                         
            screen.blit(character_agility_font, ( 150 , 230))
            screen.blit(character_luck_font, (150, 260))

            screen.blit(hp_font, (220, 110))                                         
            screen.blit(status_font, (220, 150))                                         

            screen.blit(character_hp_font, (300, 110))                                         
            screen.blit(character_status_font, (300, 150))                                         

            screen.blit(age_font, (220, 200))     
            screen.blit(marks_font, (220, 230))                                         
            screen.blit(rip_font, (220, 260))

            screen.blit(character_age_font, (340, 200))                                          
            screen.blit(character_marks_font, (340, 230))                                         
            screen.blit(character_rip_font, (340 , 260))

            screen.blit(exp_font, (50, 300))
            screen.blit(gold_font, (50, 330))
            
            screen.blit(character_exp_font, (150, 300))                                         
            screen.blit(character_gold_font, ( 150 , 330))

            screen.blit(magic_font, (50, 370))
            screen.blit(priest_magic_font, (50, 400))
                                                   
            screen.blit(character_magic_font, ( 150 , 370))
            screen.blit(character_priest_magic_font, (150, 400))

            i = 0
            for equip in character[self.menu].equip:
                if isinstance( equip , item.Item):
                    item_font = self.item_font.render( "E:" + equip.name, True, COLOR_WHITE)
                    screen.blit( item_font, (450, 100+ i*20))
                i+=1
                
            i = 0
            for char_item in character[self.menu].items:
                item_font = self.item_font.render( char_item.name, True, COLOR_WHITE)
                screen.blit( item_font, ( 450, 220 + i*20))
                i+=1


    def status_view_window_handler(self, game_self, event, character):

        if game_self.game_state == BAR:

            if event.type == KEYDOWN and event.key == K_RIGHT:
                self.menu += 1
                game_self.bar.character_check.menu+=1
                if self.menu >= len(character):
                    self.menu = 0
                    game_self.bar.character_check.menu = 0
                    
            elif event.type == KEYDOWN and event.key == K_LEFT:
                self.menu -= 1
                game_self.bar.character_check.menu -= 1
                if self.menu < 0:
                    self.menu = len(character)-1
                    game_self.bar.character_check.menu = len(character)-1

            elif event.type == KEYDOWN and event.key == K_x:
                self.is_visible = False


        if game_self.game_state == SHOP:

            if event.type == KEYDOWN and (event.key == K_LSHIFT or event.key == K_x):
                self.is_visible = False


        if game_self.game_state == MENU:


            if event.type == KEYDOWN and event.key == K_RIGHT:
                self.menu += 1
                game_self.menu.status_window.menu+=1
                if self.menu >= len(character):
                    self.menu = 0
                    game_self.menu.status_window.menu = 0
                    
            elif event.type == KEYDOWN and event.key == K_LEFT:
                self.menu -= 1
                game_self.menu.status_window.menu -= 1
                if self.menu < 0:
                    self.menu = len(character)-1
                    game_self.menu.status_window.menu = len(character)-1

            elif event.type == KEYDOWN and event.key == K_x:
                self.is_visible = False
            
