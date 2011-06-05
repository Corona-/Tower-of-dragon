#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

import window
import random

import battle
import codecs
import system_notify
import city
import menu
import dungeon
import enemy
import item
TITLE, CITY, BAR, INN, SHOP, TEMPLE, CASTLE, TOWER, STATUS_CHECK, GAMEOVER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
MENU=12

CHARACTER_MAKE = 10

SCREEN_RECTANGLE = Rect(0,0,640,480)

COLOR_WHITE = (255,255,255)
COLOR_GLAY = (128,128,128)
COLOR_BLACK = (0,0,0)

MENU_MAX = 1



class Dungeon_message(window.Window):

    def __init__(self, rectangle):
        window.Window.__init__(self, rectangle)
        self.is_visible = False

        self.top = rectangle.top
        self.left = rectangle.left
        self.right = rectangle.right
        self.centerx = rectangle.centerx

        self.coordinate = None
        self.message = None

        self.menu_font = pygame.font.Font("ipag.ttf", 20)

        #needs "探しますか？" 
        self.search_window = None
        #"押しますか？"
        self.press_window = None

        self.key_press = False

        #need to press key once more to show more message
        self.message_number = 0
        self.more_message = False

    def update(self):
            
        pass
    def draw(self, game_self, screen):
        window.Window.draw(self, screen)        
        if self.is_visible == False: return

        if self.message != None:
            i = 0
            for message in self.message:
                if message == "change":
                    self.message_number = i+1
                    self.more_message = True
                    break
                message_font = self.menu_font.render( message, True, COLOR_WHITE)
                screen.blit( message_font, (self.centerx - message_font.get_width()/2, self.top+15+i*20))
                i += 1


        if self.search_window != None:
            self.search_window.draw(screen, game_self, None)
        if self.press_window != None:
            self.press_window.draw(screen, game_self, None)

    def dungeon_message_handler(self, game_self, event):
        """event handler for dungeon"""

        if self.search_window != None and self.search_window.is_visible:
            self.search_window.confirm_window_handler(game_self, event, None)
            return
        elif self.press_window != None and self.press_window.is_visible:
            self.press_window.confirm_window_handler(game_self, event, None)
            return

        if event.type == KEYDOWN and (event.key == K_x or event.key ==K_z or event.key == K_SPACE or event.key == K_RETURN):

            if self.more_message == True:
                del self.message[0:self.message_number]

                self.more_message = False
                return

            if self.coordinate == [13,14,4]:
                game_self.dungeon.battle_encount( 100, game_self.party.member[0] )
                enemyListBack = []
                enemyList = []
                enemy_group = []
                enemy_group.append( enemy.Enemy(game_self.dungeon.enemy_data[ 19 ] ))
                enemyList.append(  enemy_group )

                battle.event_battle( game_self, enemyList, enemyListBack)


            if self.coordinate == [ 6, 6, 5]:

                game_self.dungeon.battle = battle.Battle(game_self.dungeon.enemy_data, game_self.party.member[0].coordinate[2])
                game_self.dungeon.battle_flag = 1

                enemyListBack = []
                enemyList = []
                enemy_group = []
                enemy_group.append( enemy.Enemy(game_self.dungeon.enemy_data[ 21 ] ))
                enemyList.append(  enemy_group )

                battle.event_battle( game_self, enemyList, enemyListBack)

                game_self.dungeon.object[game_self.party.member[0].coordinate[1]][game_self.party.member[0].coordinate[0]] = 0

            if self.coordinate == [ 6,2,5]:
                i = 0
                for chara in game_self.party.member:
                    while (len(chara.items) < chara.item_max):
                        chara.items.append( item.Item( game_self.item_data[902]))
                        i+=1
                        break
                    if i == 1:
                        break
                    
                game_self.dungeon.object[game_self.party.member[0].coordinate[1]][game_self.party.member[0].coordinate[0]] = 0
        

            #need to close the message
            self.is_visible = False
            self.coordinate = None
            self.message = None
            self.search_window = None
            self.press_window = None
            self.key_press = False
                


    def set_coordinate(self, game_self, coordinate):

        self.coordinate = coordinate

        #set message
        if self.coordinate == [10,3,1]:
            self.message = [u"部屋の中には、龍の彫像がある。", u"彫像はブロンズで、台座はオニキスで出来ている。"]
            self.search_window = system_notify.Confirm_window(Rect(190, 200, 200, 110), system_notify.Confirm_window.SEARCH)
            self.search_window.is_visible = True
            self.key_press = True

        if self.coordinate == [5,4,2]:
            self.message = [u"部屋の中には、水溜りがある。", u"あまり綺麗とは言えないが不快ではない。"]
            self.search_window = system_notify.Confirm_window(Rect(190, 200, 200, 110), system_notify.Confirm_window.SEARCH)
            self.search_window.is_visible = True
            self.key_press = True


        if self.coordinate == [15,14,2]:
            self.message = [ u"目の前にスイッチがある"]
            if self.key_press == True:
                self.press_window = system_notify.Confirm_window(Rect(190,200,200,110), system_notify.Confirm_window.PRESS)
                self.press_window.is_visible = True

        if self.coordinate == [13, 14, 4]:
            self.message = [ u"フードを被った人間型の大きな彫像が見える。", u"フードの穴の中からはキン色の光が漏れていて、", u"彫像にはさまざまなかたちの宝石が散りばめられている。", u"彫像の前には祭壇があり、新しい香が焚かれている。"]
            self.key_press = True

        if self.coordinate == [5, 9, 5]:
            self.message = [ u"勇気無き者は南の扉を開け、逃げ戻るが良い。", u"勇気有る者は北の扉を開けるが良い。"]            
            self.key_press = True

        if self.coordinate == [ 6, 6, 5] and game_self.dungeon.object[6][6] == 16:
            self.message = [ u"冒険者達が扉を開けると荘厳な、",
                             u"まるで王宮の一室の如き部屋に出た。",
                             u"",
                             u"しかし、床も壁も全て酷く血に汚れ、",
                             u"先ほどまで生きていた冒険者の死体や、",
                             u"何ヶ月も放置された腐敗した死体等、",
                             u"無数の屍がむせ返る血の臭いがした。",
                             "change",
                             u"そしてその奥からのっそりと竜が這い出てきた。",
                             u"その体は無数の冒険者の血を浴び、",
                             u"赤黒く見るもおぞましい姿であった。",
                             u"",
                             u"竜は冒険者達を見つけると",
                             u"口から炎を混じらせた恐ろしい叫び声を上げつつ、",
                             u"冒険者達に襲い掛かった！"]
            self.key_press = True

        if self.coordinate == [ 6, 2, 5]  and game_self.dungeon.object[2][6] == 4:
            self.message = [ u"冒険者達は新たな部屋に入ると",
                             u"そこは大きな祭壇のある部屋であった。",
                             u"",
                             u"祭壇の上に立つと",
                             u"七色に輝く羅針盤が手の中に現れた。",
                             u"",
                             u"そして、冒険者達の心に直接呼びかける声が聞こえた。",
                             u"change",
                             u"ようこそ、我が塔へ。",
                             u"勇気と強さ、そして何よりも意思強き者達よ。",
                             u"",
                             u"我が名はエルダードラゴン、",
                             u"始まりの龍にしてこの塔の支配者なり。",
                             u"change",
                             u"諸君、私はこの塔を諸君等の為に作った。",
                             u"この大地に生きる生き物は欲深く、",
                             u"時に罪を重ねる。",
                             u"",
                             u"飽くなき戦いを繰り返し",
                             u"その欲望を成就させようとしている、",
                             u"それは良い。",
                             u"それが生きる者、生物の業であると私は思う。",
                             u"change",
                             u"しかし、それだけで良いはずが無い…",
                             u"私は過去の世界を見た、この世界で無い別の世界も見た。",
                             u"それにより、私は知ったのだ。",
                             u"",
                             u"世界を動かし、変革してゆくのは常に強く、",
                             u"そして確固たる己を持ち、",
                             u"そして勇気と知恵を持って進むものであると。",
                             u"change",
                             u"私は大いなる力を持つ、",
                             u"諸君らが神と呼ぶものに近い力を持つ。",
                             u"しかし私はこの世界を如何に変えるか、その目的を持たぬ。",
                             u"",
                             u"何故ならば、私が諸君らが、",
                             u"この大地の生命が如何様な運命を",
                             u"辿ろうとも私には何の支障も生まれぬからだ",
                             u"だから、私は一つの事を決めた。",
                             u"change",
                             u"それは生命に試練を与えその試練を乗り越えし者に",
                             u"世界を変えるチャンスを与えようと。",
                             u"",
                             u"諸君、私はこの塔の頂上にて諸君らを待つ。",
                             u"change",
                             u"試練を乗り越え、",
                             u"運命や世界を変えるに相応しい者であると証明すれば",
                             u"私は諸君等の如何なる願いでも叶えるであろう。",
                             u"change",
                             u"塔を進むも自由、戻るも自由、去るも自由。",
                             u"",
                             u"諸君等の道は諸君等が決めるが良い。",
                             u"私は何の手も貸さず、慈悲も与えぬ。",
                             u"",
                             u"己の運命を切り開く者のみに私はこの力を使おう…",
                             u"塔の最上階にて私は諸君等を待つ…",
                             u"change",
                             u"語りかける声が消えると同時に羅針盤は",
                             u"その輝きを弱め、小さく七色の光を湛えている…",
                             u"",
                             u"冒険者達は「天龍の羅針盤」を手に入れた！"
                             ]            
            self.key_press = True
            
            
        if self.message != None and self.key_press == True:
            self.is_visible = True

