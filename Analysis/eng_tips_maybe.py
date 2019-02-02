#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 15:08:30 2019

@author: donaldbockoven
"""

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import division
import math
import matplotlib.pyplot as plt
import section_props as secprop

def coord_trans(x,y, xo, yo, angle):
    '''
    given an angle in degrees
    and coordinate to translate about
    return the transformed values of
    the x and y lists
    '''
    theta = math.radians(angle)
    
    x_t = [(i-xo)*math.cos(theta)+(j-yo)*math.sin(theta) for i,j in zip(x, y)]
    y_t = [-1.0*(i-xo)*math.sin(theta)+(j-yo)*math.cos(theta) for i,j in zip(x, y)]
    
    x_t = [i+xo for i in x_t]
    y_t = [j+yo for j in y_t]
    
    
    return [x_t, y_t]

# KootK
x1 = [0,60,60,120,120,60,60,0,0]
y1 = [0,0,60,60,120,120,180,180,0]

x2 = [8,52,52,112,112,52,52,8,8]
y2 = [8,8,68,68,112,112,172,172,8]

shape1 = secprop.Section(x1,y1)
shape2 = secprop.Section(x2,y2, False, 1)

# Bar coordinates and As's
xb = []
yb = []
ab = []

# Es and Ec -- consistent units -- 
Es = 29000000 #psi
Ec = math.pow(150,1.5)*33*math.sqrt(5000) #psi

n = Es/Ec

# Desired neutral axis rotation
# positive = clockwise
na_angle = -45

# tranform the sections and the bars so the NA
# lies on the horiztonal about the centroid of major
# solid shape

shape1.transformed_vertices(shape1.cx,shape1.cy,na_angle)
shape2.transformed_vertices(shape1.cx,shape1.cy,na_angle)

# plot the section
na_y = 10
plt.plot(shape1.x,shape1.y,'r-')
plt.plot(shape2.x,shape2.y,'b-')

plt.axhline(y=na_y, color='g', linestyle='--')

#for c1 in cut1:
    #plt.plot(c1.x,c1.y,'c+-')

#for c2 in cut2:
#    plt.plot(c2.x,c2.y,'k-')

plt.show()

