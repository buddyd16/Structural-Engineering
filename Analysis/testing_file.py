# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 17:35:53 2018

@author: DonB
"""
from numpy import zeros
import pin_pin_beam_equations_classes as ppbeam
import matplotlib.pyplot as plt

l =  5
lb = 10

E = 29000 * 144  #144 is conversion from ksi to ksf - 12^2
I = 30.8 / 12.0**4 #covert from in^4 to ft^4

step = l/500.0
step_backspan = lb/500.0
xs = zeros(501)
xsb = zeros(501)

xs[0]=0
xsb[0]=0

for i in range(1,501):
    xs[i] = xs[i-1] + step
    xsb[i] = xsb[i-1] + step_backspan

cant_right_test = ppbeam.cant_right_trap(-0.5,-0.25,1,3,l,lb)
test = ppbeam.trap(0.5,1,2,5,lb)

c1 = cant_right_test.rl
c3 = cant_right_test.ml

shear = cant_right_test.v(xs)
shearb =cant_right_test.backspan.v(xsb) + test.v(xsb)

moment = cant_right_test.m(xs)
momentb = cant_right_test.backspan.m(xsb) + test.m(xsb)

slope = (cant_right_test.eis(xs) + test.eisx(lb))/ (E*I)
slopeb = (cant_right_test.backspan.eis(xsb) + test.eis(xsb)) / (E*I)


delta = ((cant_right_test.eid(xs) + ppbeam.cant_right_nl(test.eisx(lb)).eid(xs))/(E*I))*12.0
deltab = ((cant_right_test.backspan.eid(xsb)+test.eid(xsb))/(E*I))*12.0

fig=plt.figure

ax = plt.subplot2grid((3, 2), (0, 0), colspan=2)
ax1 = plt.subplot2grid((3, 2), (1, 0))
ax2 = plt.subplot2grid((3, 2), (1, 1))
ax3 = plt.subplot2grid((3, 2), (2, 0))
ax4 = plt.subplot2grid((3, 2), (2, 1))


ax.plot(test.x_graph,test.y_graph)
ax.plot(cant_right_test.x_graph+xsb[-1],cant_right_test.y_graph)
ax.plot(xsb,[0]*len(xsb))
ax.plot(xs+xsb[-1],[0]*len(xs))
ax.minorticks_on()
ax.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
ax.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
ax.set_ylabel('Load (kips or klf)')
ax.set_xlabel('L (ft)')

ax1.plot(xsb,shearb)
ax1.plot(xs+xsb[-1],shear)
ax1.plot(xsb,[0]*len(xsb))
ax1.plot(xs+xsb[-1],[0]*len(xs))
ax1.fill_between(xsb,shearb,[0]*len(xsb), facecolor='blue', alpha=0.2)
ax1.fill_between(xs+xsb[-1],shear,[0]*len(xs), facecolor='blue', alpha=0.2)
ax1.minorticks_on()
ax1.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
ax1.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
ax1.set_ylabel('V (kips)')
ax1.set_xlabel('L (ft)')

ax2.plot(xsb,momentb)
ax2.plot(xs+xsb[-1],moment)
ax2.plot(xsb,[0]*len(xsb))
ax2.plot(xs+xsb[-1],[0]*len(xs))
ax2.fill_between(xsb,momentb,[0]*len(xsb), facecolor='red', alpha=0.2)
ax2.fill_between(xs+xsb[-1],moment,[0]*len(xs), facecolor='red', alpha=0.2)
ax2.minorticks_on()
ax2.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
ax2.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
ax2.set_ylabel('M (ft-kips)')
ax2.set_xlabel('L (ft)')

ax3.plot(xsb,slopeb)
ax3.plot(xs+xsb[-1],slope)
ax3.plot(xsb,[0]*len(xsb))
ax3.plot(xs+xsb[-1],[0]*len(xs))
ax3.fill_between(xsb,slopeb,[0]*len(xsb), facecolor='green', alpha=0.2)
ax3.fill_between(xs+xsb[-1],slope,[0]*len(xs), facecolor='green', alpha=0.2)
ax3.minorticks_on()
ax3.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
ax3.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
ax3.set_ylabel('S (rad)')
ax3.set_xlabel('L (ft)')

ax4.plot(xsb,deltab)
ax4.plot(xs+xsb[-1],delta)
ax4.plot(xsb,[0]*len(xsb))
ax4.plot(xs+xsb[-1],[0]*len(xs))
ax4.fill_between(xsb,deltab,[0]*len(xsb), facecolor='yellow', alpha=0.2)
ax4.fill_between(xs+xsb[-1],delta,[0]*len(xs), facecolor='yellow', alpha=0.2)
ax4.minorticks_on()
ax4.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
ax4.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
ax4.set_ylabel('D (in)')
ax4.set_xlabel('L (ft)')

plt.tight_layout()

plt.show()