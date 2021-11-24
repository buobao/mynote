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
# colorbar()
# =============================================================================

# chapter3
t = linspace(0, 2*pi, 50)
x = sin(t)
y = cos(t)

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




