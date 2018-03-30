# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 17:35:53 2018

@author: DonB
"""
from numpy import zeros
import pin_pin_beam_equations_classes as ppbeam
import matplotlib.pyplot as plt

#soil
w1 = 0.215
w2 = 0
a = 0
b = 5.383

l = 8.125

soil = ppbeam.trap(w1,w2,a,b,l)
surcharge = ppbeam.udl(.02,0,5.383,l)
wind = ppbeam.udl(.02,5.383,8.125,l)
ftg = ppbeam.point_moment(-1.02,0,l)


step = l/500.0
xs = zeros(501)

xs[0]=0

for i in range(1,501):
    xs[i] = xs[i-1] + step

v_soil = soil.v(xs)
v_surcharge = surcharge.v(xs)
v_wind = wind.v(xs)
v_ftg = ftg.v(xs)

shear = v_soil + v_surcharge + v_wind + v_ftg

m_soil = soil.m(xs)
m_surcharge = surcharge.m(xs)
m_wind = wind.m(xs)
m_ftg = ftg.mo(xs)

moment = m_soil + m_surcharge + m_wind + m_ftg

s_soil = soil.eis(xs)
s_surcharge = surcharge.eis(xs)
s_wind = wind.eis(xs)
s_ftg = ftg.eis(xs)

slope = s_soil + s_surcharge + s_wind + s_ftg

d_soil = soil.eid(xs)
d_surcharge = surcharge.eid(xs)
d_wind = wind.eid(xs)
d_ftg = ftg.eid(xs)

delta = d_soil + d_surcharge + d_wind + d_ftg

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)

ax1.plot(xs,shear)
ax1.plot(xs,[0]*len(xs))
ax1.fill_between(xs,shear,[0]*len(xs), facecolor='blue', alpha=0.2)
ax1.minorticks_on()
ax1.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
ax1.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)

ax2.plot(xs,moment)
ax2.plot(xs,[0]*len(xs))
ax2.fill_between(xs,moment,[0]*len(xs), facecolor='red', alpha=0.2)
ax2.minorticks_on()
ax2.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
ax2.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)

ax3.plot(xs,slope)
ax3.plot(xs,[0]*len(xs))
ax3.fill_between(xs,slope,[0]*len(xs), facecolor='green', alpha=0.2)
ax3.minorticks_on()
ax3.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
ax3.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)

ax4.plot(xs,delta)
ax4.plot(xs,[0]*len(xs))
ax4.fill_between(xs,delta,[0]*len(xs), facecolor='yellow', alpha=0.2)
ax4.minorticks_on()
ax4.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
ax4.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)

plt.show()