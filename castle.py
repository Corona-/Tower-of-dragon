#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import window
import character_view
import system_notify
import city

TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

CHARACTER_MAKE = 10
NO_EXTRA, CHARACTER_VIEW, PARTY_REMOVE, CHARACTER_CHECK = 100, 101, 102, 103

SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

MENU_MAX = 5

class Castle:

    NEW, DELETE, NAME_CHANGE, JOB_CHANGE, DONATE, BACK = 0, 1, 2, 3 ,4 ,5

    
    
    def __init__(self):
        self.menu = self.NEW

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.castle_font = self.menu_font.render(u"ジークフロント城", True, COLOR_WHITE)

        self.new_font = self.menu_font.render(u"冒険者を募集する", True, COLOR_WHITE)
        self.delete_font = self.menu_font.render(u"冒険者を追放する", True, COLOR_WHITE)
        self.name_change_font = self.menu_font.render(u"名前を変える", True, COLOR_WHITE)
        self.job_change_font = self.menu_font.render(u"転職する", True, COLOR_WHITE)
        self.donate_font = self.menu_font.render(u"寄付をする", True, COLOR_WHITE)
        self.back_font = self.menu_font.render(u"街に戻る", True, COLOR_WHITE)

        self.no_delete_font = self.menu_font.render(u"冒険者を追放する", True, COLOR_GLAY)
        self.no_name_change_font = self.menu_font.render(u"名前を変える", True, COLOR_GLAY)
        self.no_job_change_font = self.menu_font.render(u"転職する", True, COLOR_GLAY)
        self.no_donate_font = self.menu_font.render(u"寄付をする", True, COLOR_GLAY)

        self.music = 0


        #extra windows initialization
        #-1 to adjust with view.
        self.character_delete = None #character_view.Character_view(Rect(80, 60, 480, 360), character_view.Character_view.DELETE)
        self.delete_confirm = character_view.Delete_confirm_window(Rect(200, 160, 240, 120))
        self.character_rename = None #character_view.Character_view(Rect(80, 60, 480, 360), character_view.Character_view.NAME_CHANGE)
        self.donate_money = None #system_notify.System_notify_window(Rect(200,120,240,240), system_notify.System_notify.DONATE)
        self.change_job_window = None #Change_job_window(Rect(80,60,480,360))
        
    def update(self):
        if self.music == 0:
            pygame.mixer.music.load("BGM/sakusen_kaigi.mp3")
            pygame.mixer.music.play(-1)
            self.music = 1
        pass
    def draw(self, screen, game_self, characters):

        #draw window for title and menu
        title_window = window.Window(Rect(20,20, 190, 50))
        title_window.draw(screen)
        
        screen.blit(self.castle_font, (35, 35))

        menu_window = window.Window(Rect(320,20,300,210))
        menu_window.draw(screen)

        #set cursors for menu item
        if self.menu == self.NEW:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,35,292,30), 0)
        elif self.menu == self.DELETE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,65,292,30), 0)
        elif self.menu == self.NAME_CHANGE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,95,292,30), 0)
        elif self.menu == self.JOB_CHANGE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,125,292,30), 0)
        elif self.menu == self.DONATE:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,155,292,30), 0)
        elif self.menu == self.BACK:
            pygame.draw.rect(screen, COLOR_GLAY, Rect(324,185,292,30), 0)


        #draw the image fonts onto screen
        WINDOW_START_WIDTH = 300
        MENU_CENTER = SCREEN_RECTANGLE.width + WINDOW_START_WIDTH

        screen.blit(self.new_font, ((MENU_CENTER-self.new_font.get_width())/2, 40))

        if len(game_self.characters) == 0:
            screen.blit(self.no_delete_font, ((MENU_CENTER-self.no_delete_font.get_width())/2, 70))
        else:
            screen.blit(self.delete_font, ((MENU_CENTER-self.delete_font.get_width())/2, 70))

        if len(game_self.characters) == 0:
            screen.blit(self.no_name_change_font, ((MENU_CENTER-self.no_name_change_font.get_width())/2, 100))
        else:
            screen.blit(self.name_change_font, ((MENU_CENTER-self.name_change_font.get_width())/2, 100))

        if len(game_self.party.member) == 0:
            screen.blit(self.no_job_change_font, ((MENU_CENTER-self.no_job_change_font.get_width())/2, 130))
        else:
            screen.blit(self.job_change_font, ((MENU_CENTER-self.job_change_font.get_width())/2, 130))

        if len(game_self.party.member) == 0:
            screen.blit(self.no_donate_font, ((MENU_CENTER-self.no_donate_font.get_width())/2, 160))
        else:
            screen.blit(self.donate_font, ((MENU_CENTER-self.donate_font.get_width())/2, 160))

        screen.blit(self.back_font, ((MENU_CENTER-self.back_font.get_width())/2, 190))


        #draw the extra window
        if self.character_delete != None:
            self.character_delete.draw(screen, characters)
        if self.delete_confirm != None:
            self.delete_confirm.draw(screen)
        if self.character_rename != None:
            self.character_rename.draw(screen, characters)
        if self.donate_money != None:
            self.donate_money.draw(screen, game_self.party.member)
        if self.change_job_window != None:
            self.change_job_window.draw(screen,game_self)

def castle_handler(self, event):
    """event handler of castle"""

    if self.castle.delete_confirm != None and self.castle.delete_confirm.is_visible:
        self.castle.delete_confirm.delete_confirm_window_handler(self, event, self.characters)
        return
    elif self.castle.character_rename != None and self.castle.character_rename.is_visible:
        self.castle.character_rename.character_view_handler( self, event, self.characters)
        return
    elif self.castle.character_delete != None and self.castle.character_delete.is_visible:
        self.castle.character_delete.character_view_handler( self, event, self.characters)
        return
    elif self.castle.donate_money != None and self.castle.donate_money.is_visible:
        self.castle.donate_money.system_notify_window_handler( event, self, self.party.member)
        return
    elif self.castle.change_job_window != None and self.castle.change_job_window.is_visible:
        self.castle.change_job_window.change_job_window_handler( self, event)
        return
    
    
    if event.type == KEYDOWN and event.key == K_UP: #moves the cursor up
        self.cursor_se.play()
        self.castle.menu -= 1
        if self.castle.menu < 0:
            self.castle.menu = MENU_MAX
    elif event.type == KEYDOWN and event.key == K_DOWN:
        self.cursor_se.play()
        self.castle.menu += 1
        if self.castle.menu > MENU_MAX:
            self.castle.menu = 0

    if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_z or event.key == K_RETURN):
        if self.castle.menu == Castle.NEW:
            self.game_state = CHARACTER_MAKE
        elif self.castle.menu == Castle.DELETE:
            if len(self.characters) > 0:
                self.castle.character_delete = character_view.Character_view(Rect(80, 60, 480, 360), character_view.Character_view.DELETE)
                self.castle.character_delete.is_visible = True
        elif self.castle.menu == Castle.NAME_CHANGE:
            if len(self.characters) > 0:
                self.castle.character_rename = character_view.Character_view(Rect(80, 60, 480, 360), character_view.Character_view.RENAME)
                self.castle.character_rename.is_visible = True
        elif self.castle.menu == Castle.JOB_CHANGE:
            if len(self.party.member) > 0:
                self.castle.change_job_window = Change_job_window(Rect(80,60,480,360))
                self.castle.change_job_window.is_visible = True
        elif self.castle.menu == Castle.DONATE:
            if len(self.party.member) > 0:
                self.castle.donate_money = system_notify.System_notify_window(Rect(200,120,240,240), system_notify.System_notify_window.DONATE)
                self.castle.donate_money.is_visible = True
        elif self.castle.menu == Castle.BACK:
            self.game_state = CITY
            self.castle.menu = Castle.NEW
            self.castle.music = 0
            self.castle = None
            self.city = city.City()
        self.select_se.play()

    if event.type == KEYDOWN and (event.key ==K_x):
        self.game_state = CITY
        self.castle.menu = Castle.NEW
        self.castle.music = 0
        self.castle = None
        self.city = city.City()

        self.cancel_se.play()


class Change_job_window(window.Window):

    GOOD, NEUTRAL, EVIL = 1, 0, -1
    WARRIOR, FIGHTER, MAGICIAN,PRIEST, THIEF, MERCHANT = 0, 1, 2, 3, 4, 5


    def __init__(self, rectangle):
        window.Window.__init__(self,rectangle)
        self.is_visible = False

        self.menu = 0
        #if job change includes character in bar
        self.page = 0

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        self.job_change_confirm = system_notify.Confirm_window( Rect(180, 80, 360, 110), 20)

        #find all characters that could change job
        self.possible_characters = []

    def draw(self, screen, game_self):
        """draw the window on the screen"""
        window.Window.draw(self, screen)        
        if self.is_visible == False: return

        instruction_font = self.menu_font.render( u"誰が転職しますか？", True, COLOR_WHITE)      
        instruction_window = window.Window(Rect(20,20, 30+instruction_font.get_width(), 50))
        instruction_window.draw(screen)
        screen.blit(instruction_font, ( 35 , 35))

        top_font = self.menu_font.render( u"転職可能な冒険者", True, COLOR_WHITE)      
        screen.blit(top_font, (self.centerx - top_font.get_width()/2, self.top+20))

        self.possible_characters = []
        for character in game_self.party.member:
            if character.job == self.WARRIOR:
                if game_self.party.castle_donate > 100000 and charcter.level > 20:
                    self.possible_characters.append(character)
            elif character.job == self.FIGHTER:
                if character.marks > 2000 and charcter.level> 20:
                    self.possible_characters.append(character)
            elif character.job == self.MAGICIAN:
                if game_self.party.house > 3 and charcter.level > 20:
                    self.possible_characters.append(character)
            elif character.job == self.PRIEST:
                if game_self.party.temple_donate > 100000 and charcter.level > 20:
                    self.possible_characters.append(character)
            elif character.job == self.THIEF:
                if game_self.party.shop_donate > 100000 and charcter.level > 20:
                    self.possible_characters.append(character)
            elif character.job == self.MERCHANT:
                if game_self.party.bar_donate > 100000 and charcter.level > 20:
                    self.possible_characters.append(character)
            
            pass

        if self.possible_characters != []:
            #draws rectangle on the menu item size of rectangle has width of window rectangle - edge_length*2
            #the height depends on the size of font
            pygame.draw.rect(screen, COLOR_GLAY, Rect( self.left+4, self.top+47+30*self.menu,(self.right-self.left)-8,25), 0)

        i = 0
        for character in self.possible_characters:
            
            character_font = self.menu_font.render(character.name, True, COLOR_WHITE)
            screen.blit(character_font, (self.left+20, self.top+50+(i%10)*30))                                         

            job_font = None
            new_job_font = None
            if character.job == self.WARRIOR:
                job_font = u"戦士"
                if character.alignment == self.GOOD:
                    new_job_font = u"君主"
                elif character.alignment == self.NEUTRAL:
                    new_job_font = u"ソードマスター"
                elif character.alignment == self.EVIL:
                    new_job_font = u"狂王"

            elif character.job == self.FIGHTER:
                job_font = u"武士"
                if character.alignment == self.GOOD:
                    new_job_font = u"剣聖"
                elif character.alignment == self.NEUTRAL:
                    new_job_font = u"大将"
                elif character.alignment == self.EVIL:
                    new_job_font = u"ヒトキリ"
            elif character.job == self.MAGICIAN:
                job_font = u"魔術師"
                if character.alignment == self.GOOD:
                    new_job_font = u"魔法戦士"
                elif character.alignment == self.NEUTRAL:
                    new_job_font = u"大魔導"
                elif character.alignment == self.EVIL:
                    new_job_font = u"邪術師"
            elif character.job == self.PRIEST:
                job_font = u"僧侶"
                if character.alignment == self.GOOD:
                    new_job_font = u"法王"
                elif character.alignment == self.NEUTRAL:
                    new_job_font = u"司祭"
                elif character.alignment == self.EVIL:
                    new_job_font = u"狂信者"
            elif character.job == self.THIEF:
                job_font = u"盗賊"
                if character.alignment == self.GOOD:
                    new_job_font = u"義賊"
                elif character.alignment == self.NEUTRAL:
                    new_job_font = u"怪盗"
                elif character.alignment == self.EVIL:
                    new_job_font = u"忍者"
            elif character.job == self.MERCHANT:
                job_font = u"商人"
                if character.alignment == self.GOOD:
                    new_job_font = u"ギルドマスター"
                elif character.alignment == self.NEUTRAL:
                    new_job_font = u"武装商人"
                elif character.alignment == self.EVIL:
                    new_job_font = u"高利貸し"

            total_font = job_font + " -> "  + new_job_font
            total_font = self.menu_font.render(total_font, True, COLOR_WHITE)
            screen.blit(total_font, (self.centerx-40, self.top+50+(i%10)*30))              
            i+=1

        self.job_change_confirm.draw(screen, game_self, None)
 

    def change_job_window_handler(self, game_self, event):

        if self.job_change_confirm.is_visible == True:
            self.job_change_confirm.confirm_window_handler( game_self, event, self.possible_characters[self.menu])
            return

        if event.type == KEYDOWN and event.key == K_x:
            self.menu = 0
            self.page = 0
            self.is_visible = False

        if event.type == KEYDOWN and event.key == K_UP: #moves the cursor up
            self.menu -= 1
            if self.menu < 0:
                self.menu = 0
        elif event.type == KEYDOWN and event.key == K_DOWN:
            if len(self.possible_characters) > self.menu+self.page*10+1:
                self.menu += 1
                if self.menu > len(self.possible_characters)-1:
                    self.menu = len(self.possible_characters)-1
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            if len(game_self.party.member) > (self.page+1)*10:
                self.page += 1
                self.menu = 0
        elif event.type == KEYDOWN and event.key == K_LEFT:
            if self.page > 0:
                self.page -= 1
                self.menu = 0

        #TO-DO add enter and change job
        if event.type == KEYDOWN and (event.key ==K_z or event.key == K_SPACE or event.key == K_RETURN):
            if self.possible_characters != []:
                self.job_change_confirm.is_visible = True
            
            pass
        
