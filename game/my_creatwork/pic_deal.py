# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 20:45:11 2022

@author: DELL
"""
# 本模块的功能:<更改图片尺寸>
import os
import os.path
from PIL import Image
'''
filein: 输入图片
fileout: 输出图片
width: 输出图片宽度
height:输出图片高度
type:输出图片类型（png, gif, jpeg...）
'''
def ResizeImage(filein, fileout, width, height, type):
  img = Image.open(filein)
  out = img.resize((width, height),Image.ANTIALIAS)
  #resize image with high-quality
  out.save(fileout, type)
if __name__ == "__main__":
  filein = r'./background.jpg'
  fileout = r'./background.jpg'
  width = 1920#137飞机参数
  height = 1080#194飞机参数
  type = 'png'
  ResizeImage(filein, fileout, width, height, type)

