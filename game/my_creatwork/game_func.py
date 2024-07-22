# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 16:22:40 2022

@author: DELL
"""

import sys
import pygame
from bullet import Bullet,Ebullet
from missile import Missile

def check_keydown_events(event, plane,enemy,setting,screen,bullets,missiles,ebullets):
    # 捕捉用户按下
    if event.key == pygame.K_RIGHT:
        plane.mv_right = True
    elif event.key == pygame.K_LEFT:
        plane.mv_left = True
    elif event.key == pygame.K_UP:
        plane.mv_up = True
    elif event.key == pygame.K_DOWN:
        plane.mv_down = True
        
    elif event.key == pygame.K_d:
        enemy.mv_right = True
    elif event.key == pygame.K_a:
        enemy.mv_left = True
    elif event.key == pygame.K_s:
        enemy.mv_up = True
    elif event.key == pygame.K_w:
        enemy.mv_down = True    
    
    elif event.key == pygame.K_SPACE:
        # 创建一个子弹，并将其加入到编组bullets中
        new_bullet = Bullet(setting, screen, plane)
        bullets.add(new_bullet)
    elif event.key == pygame.K_RETURN:
        new_missile = Missile(screen, plane)
        missiles.add(new_missile)
        
    elif event.key == pygame.K_q:
        new_bullet = Ebullet(setting, screen, enemy)
        ebullets.add(new_bullet)
def check_keyup_events(event, plane,enemy):
    # 捕捉用户松开
    if event.key == pygame.K_RIGHT:
        plane.mv_right = False
    elif event.key == pygame.K_LEFT:
        plane.mv_left = False
    elif event.key == pygame.K_UP:
        plane.mv_up = False
    elif event.key == pygame.K_DOWN:
        plane.mv_down = False
        
    elif event.key == pygame.K_a:
        enemy.mv_left = False
    elif event.key == pygame.K_d:
        enemy.mv_right = False
    elif event.key == pygame.K_s:
        enemy.mv_up = False
    elif event.key == pygame.K_w:
        enemy.mv_down = False
        
def check_events(plane,enemy,setting,screen,bullets,missiles,ebullets):
    # 为了防止游戏窗口启动会立马关闭，在其中增加一个游戏循环(无限循环)，
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # QUIT用户请求程序关闭
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, plane,enemy,setting,screen,bullets,missiles,ebullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, plane,enemy)

def update_screen(screen, bg_img, plane,bullets,enemy,missiles,ebullets):
    # 更新屏幕的图像
    # 每次循环都会重新绘制屏幕
    screen.blit(bg_img, [0, 0])  # 绘制图像
    plane.blitme()  # 将飞船绘制到屏幕上
    enemy.blitme()
    # 绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()  # 绘制子弹
    for missile in missiles.sprites():
        missile.blitme()
    for ebullet in ebullets.sprites():
        ebullet.draw_bullet()
    # 将完整显示Surface更新到屏幕
    pygame.display.flip()
    
def update_bullets(bullets, enemy, setting, screen, plane):
    # 将编组中的每个子弹调用bullet.update()
    bullets.update()
    # 删除已经消失的子弹       
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

        collisions_1 = pygame.sprite.collide_rect(bullet,enemy)

        if collisions_1 ==True:
            bullets.remove(bullet)
            enemy.killed()
    collisions_2 = pygame.sprite.collide_rect(plane, enemy)   
    if collisions_2 == True:
        enemy.killed()
def update_missiles(missiles,enemy,setting,screen,plane):
    missiles.update()
    for missile in missiles.copy():
        if missile.rect.bottom <=0:
            missiles.remove(missile)
            
        collisions_1 = pygame.sprite.collide_rect(missile, enemy)
        if collisions_1 == True:
            missiles.remove(missile)
            enemy.mkilled()
            
def update_ebullets(ebullets, enemy, setting, screen, plane):
    ebullets.update()
    # 删除已经消失的子弹       
    for ebullet in ebullets.copy():
        if ebullet.rect.bottom >= 600:
            ebullets.remove(ebullet)

        collisions_1 = pygame.sprite.collide_rect(ebullet,plane)

        if collisions_1 ==True:
            ebullets.remove(ebullet)
            plane.killed()    
    collisions_2 = pygame.sprite.collide_rect(plane, enemy)   
    if collisions_2 == True:
        plane.killed()
        
        
def update_offset(bullets,ebullets,missiles):
    pygame.sprite.groupcollide(bullets, ebullets, True, True)

    pygame.sprite.groupcollide(missiles, ebullets, True, True)
