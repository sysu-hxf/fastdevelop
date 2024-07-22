# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 15:13:18 2022

@author: DELL
"""
import pygame
from setting import Settings  # 引入settings.py
from plane import Plane,Enemy_Plane
import game_func as fg
from pygame.sprite import Group

def run_game():
    # 初始化游戏
    pygame.init()
    # 设置屏幕的分辨率
    setting = Settings()
    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))  # 大小为1000px乘以600px
    pygame.display.set_caption("微光计划")  # 标题
    
    # 创建小飞机
    plane = Plane(screen,setting)
    # 创建一个存储子弹的编组
    bullets = Group()
    ebullets = Group()
    #创建导弹编组
    missiles = Group()
    #创建敌机
    enemy = Enemy_Plane(screen,setting)
    
      # 开始游戏的主循环
    while(True):
        # 不关闭窗口
        fg.check_events(plane,enemy,setting,screen,bullets,missiles,ebullets)
        # 调用飞机移动的方法
        plane.update()
        enemy.update()
        # 弹药画面设置
        bullets.update()
        ebullets.update()
        missiles.update()
        #弹药溢出设置；敌机炸毁设置
        fg.update_bullets(bullets, enemy, setting, screen, plane)
        fg.update_missiles(missiles, enemy, setting, screen, plane)
        fg.update_ebullets(ebullets, enemy, setting, screen, plane)
        fg.update_offset(bullets, ebullets,missiles)
        #显示
        fg.update_screen(screen, setting.bg_img, plane,bullets,enemy,missiles,ebullets)

run_game()
