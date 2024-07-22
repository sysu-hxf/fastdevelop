# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 20:39:07 2022

@author: DELL
"""

import pygame
from pygame.sprite import Sprite
import random
class Missile(Sprite): 
    """导弹的管理"""
    def __init__(self, screen, plane):
        super().__init__()
        self.screen = screen
        self.img_missile = pygame.image.load("./missile.png")
        self.rect = self.img_missile.get_rect() 
        self.rect.centerx = plane.rect.left
        self.rect.top = plane.rect.top
        self.y = float(self.rect.y)
        self.speed = random.uniform(0.05,0.9)

    def update(self):
        # 向上移动子弹
        self.y -= self.speed
        # 根据self.y的值更新self.rect.y
        self.rect.y = self.y

    def blitme(self):
        # 在指定位置绘制
        self.screen.blit(self.img_missile, self.rect)
