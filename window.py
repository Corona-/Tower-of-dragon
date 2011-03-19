#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)


class Window:
    """simple class for creating window for messages"""
    #the width of the outer edge
    EDGE_WIDTH = 4

    def __init__(self, rectangle):
        #outer white rectangle
        self.rectangle = rectangle
        #inner black rectange
        self.inner_rectangle = self.rectangle.inflate( -self.EDGE_WIDTH*2, -self.EDGE_WIDTH*2 ) 

        self.is_visible = True
        
    def draw(self, screen):
        """draw the window on the screen"""
        if self.is_visible == False: return
        pygame.draw.rect(screen, COLOR_WHITE, self.rectangle, 0)
        pygame.draw.rect(screen, COLOR_BLACK, self.inner_rectangle, 0)
    def show(self):
        """show the window"""
        self.is_visible = True
    def hide(self):
        """hide the window"""
        self.is_visible = False
        
