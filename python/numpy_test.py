# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 22:08:30 2021

@author: lebro
"""

from numpy import *
from matplotlib.pyplot import *
from numpy.random import rand

# chapter1
# =============================================================================
# a = linspace(0,4*math.pi,201)
# b = sin(a)
# 
# plot(a,b)
# 
# mask = b>0
# plot(a[mask], b[mask], 'ro')
# =============================================================================

# chapter2
# a = linspace(0, 2*math.pi, 50)
# plot(sin(a))
# plot(a,sin(a),a,sin(3*a))
# plot(a,cos(a),a,sin(a))
# plot(a,sin(a),'r-^')
# x = linspace(0, 2*math.pi, 50)
# plot(x, sin(x), 'b-o', x, sin(2 * x), 'g-^')
#点图
# scatter(x,sin(x))

# =============================================================================
# x = rand(200)
# y = rand(200)
# size = rand(200) * 30
# color = rand(200)
# scatter(x, y, size, color)
# colorbar()    #显示颜色条
# =============================================================================

# chapter3
# t = linspace(0, 2*pi, 50)
# x = sin(t)
# y = cos(t)

#顺序展示两张图
# =============================================================================
# figure()
# plot(x)
# figure()
# plot(y)
# =============================================================================

# 同时展示两张图
# =============================================================================
# subplot(1, 2, 1)
# plot(x)
# subplot(1, 2, 2)
# plot(y)
# =============================================================================

# 标签展示
# subplot(1, 2, 1)
# plot(x,label="xline")
# legend()   #加这句话才能显示标签
# subplot(1, 2, 2)
# plot(y,label="yline")
# legend()

# plot(x, sin(x))
# xlabel('radians')
# # 可以设置字体大小
# ylabel('amplitude', fontsize='large')
# title('Sin(x)')

# clf()


# 显示图片
# from PIL import Image
# im = Image.open(r"C:\Users\lebro\Pictures\Default.jpg")
# im.show()

# 直方图表示的是给定数组中不同item出现的次数
#hist(rand(1000))
# hist([1,1,1,2,1,3,3,4,4,4,4,2,2,2,2,5,6,7,8,3,4,2,5,9,9,9,4])
# hist(["hello","jack","hello","lebron","tom","hello","mom","lebron"])


# 向量化
# def sinc(x):
#     if x==0.0:
#         return 1.0
#     else:
#         w = pi*x
#         return sin(w)/w

# print(sinc(1))

# x = array([1,2,3])
# vsinc = vectorize(sinc)
# print(vsinc(x))
# x = linspace(-5, 5,101)
# plot(x,vsinc(x))

import matplotlib.pyplot as plt
from functools import partial

fig = plt.figure()
# 画两个坐标轴
plt.axhline(y=0, c='black')
plt.axvline(x=0, c='black')

# 设置坐标轴的取值范围
ax = plt.gca()
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-3, 4)

arrow_vector = partial(plt.arrow, width=0.01, head_width=0.1, head_length=0.2, length_includes_head=True)

arrow_vector(0, 0, 2, -1, color='g')
arrow_vector(0, 0, -1, 2, color='c')
arrow_vector(2, -1, -2, 4, color='b')
arrow_vector(0, 0, 0, 3, width=0.05, color='r')

plt.draw()
















