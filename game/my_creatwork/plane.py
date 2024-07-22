# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 15:28:28 2022

@author: DELL
"""

import pygame
import sys
import time


class Plane:
    def __init__(self, screen, setting):
        # 初始化小飞机并设置其初始位置
        self.screen = screen
        self.setting = setting  # 实例化属性
        # 加载图像，并获得其矩形区域
        self.img_plane = pygame.image.load("./plane.png")
        self.rect = self.img_plane.get_rect()  # 得到小飞机的的矩形区域
        self.screen_rect = self.screen.get_rect()  # 得到screen的矩形区域
        # 将小飞机放到底部中央
        self.rect.centerx = self.screen_rect.centerx  # 水平居中
        self.rect.bottom = self.screen_rect.bottom  # 底部
        # 将其修改为浮点数
        self.center = float(self.rect.centerx)
        self.low    = float(self.rect.bottom)
        # 标志位
        self.mv_right = False
        self.mv_left = False
        self.mv_up = False
        self.mv_down = False
    # 定义一个调整小飞机位置的方法
    def update(self):
        # 根据标志位的调整小飞机的位置
        if self.mv_right:
            if self.center<self.setting.screen_width:
                self.center += self.setting.plane_speed  # settings中的属性
            else:
                self.center=self.center
        
        if self.mv_left:
            if self.center>0:
                self.center -= self.setting.plane_speed
            else:
                self.center=self.center
         
        if self.mv_up:
            if self.low>100:
                self.low-=self.setting.plane_speed
            else:
                self.low=self.low
        
        if self.mv_down:
            if self.low<self.setting.screen_height:
                self.low+=self.setting.plane_speed
            else:
                self.low=self.low       

        # 根据self.center的值来更新self.rect.centerx
        self.rect.centerx = self.center
        self.rect.bottom  = self.low
        
    def blitme(self):
        # 在指定位置绘制小飞机
        self.screen.blit(self.img_plane, self.rect)
        pygame.draw.rect(self.screen, (0, 128, 0),
                         (self.rect.centerx+80,self.rect.bottom-100,200,8))
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.rect.centerx +80,self.rect.bottom-100,
                          200 - self.setting.plane_life , 8))
    
    def killed(self):
        self.setting.plane_life = self.setting.plane_life - self.setting.damage
        if self.setting.plane_life <= 0:
            time.sleep(0.3)
            print("wsad胜利,得分："+str(self.setting.enemy_life))
            pygame.quit()
            sys.exit()
   
class Enemy_Plane:
    def __init__(self,screen,setting):
        self.screen=screen
        self.setting = setting
        self.img_plane = pygame.image.load("./enemy_plane.png")
        self.rect = self.img_plane.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = 200
        self.center = float(self.rect.centerx)
        self.low    = float(self.rect.bottom)
        # 标志位
        self.mv_right = False
        self.mv_left = False
        self.mv_up = False
        self.mv_down = False
        
    def update(self):
        # 根据标志位的调整小飞机的位置
        if self.mv_right:
            if self.center<self.setting.screen_width:
                self.center += self.setting.enemy_speed  # settings中的属性
            else:
                self.center=self.center
        
        if self.mv_left:
            if self.center>0:
                self.center -= self.setting.enemy_speed
            else:
                self.center=self.center
         
        if self.mv_up:
            if self.low>100:
                self.low-=self.setting.enemy_speed
            else:
                self.low=self.low
        
        if self.mv_down:
            if self.low<self.setting.screen_height:
                self.low+=self.setting.enemy_speed
            else:
                self.low=self.low       

        # 根据self.center的值来更新self.rect.centerx
        self.rect.centerx = self.center
        self.rect.bottom  = self.low
    
        
    def blitme(self):
        # 在指定位置绘制小飞机
        self.screen.blit(self.img_plane, self.rect)   
        #血条设置
        pygame.draw.rect(self.screen, (0, 128, 0),
                         (self.rect.centerx+80,self.rect.bottom-100,200,8))
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.rect.centerx +80,self.rect.bottom-100,
                          200 - self.setting.enemy_life , 8))
    
    def killed(self):
        self.setting.enemy_life = self.setting.enemy_life - self.setting.damage
        if self.setting.enemy_life <= 0:
            time.sleep(0.3)
            print("↑↓←→胜利,得分："+str(self.setting.plane_life))
            pygame.quit()
            sys.exit()
    
    def mkilled(self):
        a = self.setting.enemy_life
        b = self.setting.plane_life
        self.setting.enemy_life -= (a/b)*self.setting.damage
        if self.setting.enemy_life<=0:
            self.setting.enemy_life = 20
        else:
            None
