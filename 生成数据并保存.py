# -*- coding: utf-8 -*-
"""
Created on Wed May 18 14:19:35 2022

@author: 01
"""

import xlwt
import random
import pandas as pd
book = xlwt.Workbook(encoding='utf-8',style_compression=0)

	
sheet = book.add_sheet('遗传算法实现数据',cell_overwrite_ok=True)

col = ('x1', 'x2', 'x3','x4','y')
for i in range(len(col)):
    sheet.write(0,i,col[i])
    
#sheet.write(i+1,j,moneys[i])
#print("添加成功%S",moneys[i],j,i)
ls=[[]for i in range(len(col))]


for i in range(200):
    x1=random.randint(1,30)
    x2=random.randint(1,30)
    x3=random.randint(1,30)
    x4=random.randint(1,30)
    ls[0].append(x1)
    ls[1].append(x2)
    ls[2].append(x3)
    ls[3].append(x4)
    y=10*x1*x1+20*x2*1-30*x3*x3/40*x4*1#
    ls[4].append(y)
for i in range(len(col)):
    for j in range(200):
        sheet.write(j+1,i,ls[i][j])
savepath = 'data.xls'
book.save(savepath)