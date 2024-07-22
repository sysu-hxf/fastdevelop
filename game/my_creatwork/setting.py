# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 16:20:35 2022

@author: DELL
"""

import pygame

class Settings:
    """存储所有设置"""
    def __init__(self):
        # 屏幕设置
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_img = pygame.image.load("./background.jpg")
        #飞机设置
        self.plane_speed = 0.8
        self.enemy_speed = 0.8
        self.plane_life = 200.0
        self.enemy_life = 200.0
        # 子弹的设置
        self.bullet_speed = 2  # 速度
        self.bullet_width = 5  # 子弹的宽
        self.bullet_height = 25  # 子弹的高
        
        self.ebullet_speed = 2 # 速度
        self.ebullet_width = 5  # 子弹的宽
        self.ebullet_height = 25  # 子弹的高
        
        #
        self.damage = 20