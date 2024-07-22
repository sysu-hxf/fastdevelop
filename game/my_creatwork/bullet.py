# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 17:52:02 2022

@author: DELL
"""

"""
-*- coding:uft-8 -*-
author: 小甜
date:2020/6/3
"""
import pygame
import random
from pygame.sprite import Sprite
class Bullet(Sprite):  # 继承pygame.sprite中的Sprite类
    """子弹的管理"""
    def __init__(self, setting, screen, plane):
        super().__init__()
        self.screen = screen
        # 在(0,0)处创建一个表示子弹的矩形
        # pygame.Rect
        # 用于存储直角坐标的pygame对象
        self.rect = pygame.Rect(0,0, setting.bullet_width, setting.bullet_height)
        # 设置显示的位置
        self.rect.centerx = plane.rect.centerx
        self.rect.top = plane.rect.top
        # 让子弹的位置跟小飞机重叠，当子弹飞出了以后，就显得跟从小飞机里面射出来一样

        # 将子弹的坐标转换为浮点数
        self.y = float(self.rect.y)

        # 子弹的颜色
        self.color = random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)
        # 子弹的速度
        self.speed = setting.bullet_speed

    def update(self):
        # 向上移动子弹
        self.y -= self.speed
        # 根据self.y的值更新self.rect.y
        self.rect.y = self.y

    def draw_bullet(self):
        """绘制子弹"""
        # pygame.draw.rect（）画一个矩形的形状
        pygame.draw.rect(self.screen, self.color, self.rect)

class Ebullet(Sprite):  # 继承pygame.sprite中的Sprite类
    """子弹的管理"""
    def __init__(self, setting, screen, enemy):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0,0, setting.ebullet_width, setting.ebullet_height)
        # 设置显示的位置
        self.rect.centerx = enemy.rect.centerx
        self.rect.top = enemy.rect.top
        self.y = float(self.rect.y)
        self.color = random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)
        self.speed = setting.ebullet_speed

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """绘制子弹"""
        # pygame.draw.rect（）画一个矩形的形状
        pygame.draw.rect(self.screen, self.color, self.rect)