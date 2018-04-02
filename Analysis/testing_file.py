# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 17:35:53 2018

@author: DonB
"""
from numpy import zeros
import pin_pin_beam_equations_classes as ppbeam
import matplotlib.pyplot as plt
import math

def reaction_graph(r,x):
    r = -1.0 * r
    arrow_height = r/6.0
    #30 degree arrow
    arrow_plus= x+(arrow_height*math.tan(math.radians(30)))
    arrow_minus= x-(arrow_height*math.tan(math.radians(30)))
    
    x_graph=[arrow_minus,x,arrow_plus,x,x]
    y_graph=[arrow_height,0,arrow_height,0,r]
    
    return x_graph, y_graph
    
ll = 5
lc = 10
lr =  5


E = 29000 * 144  #144 is conversion from ksi to ksf - 12^2
I = 30.8 / 12.0**4 #covert from in^4 to ft^4

step_left = ll/500.0
step_backspan = lc/500.0
step_right = lr/500.0

xsl = zeros(501)
xsc = zeros(501)
xsr = zeros(501)

xsl[0]=0
xsc[0]=0
xsr[0]=0

for i in range(1,501):
    xsl[i] = xsl[i-1] + step_left
    xsc[i] = xsc[i-1] + step_backspan
    xsr[i] = xsr[i-1] + step_right

load_left = ppbeam.cant_left_trap(1,0.5,1,4,ll,lc)
load_center = ppbeam.pl(0,0,lc)
load_right = ppbeam.cant_right_trap(-0.5,-1,1,4,lr,lc)

reaction_left = load_center.rl + load_right.backspan.rl + load_left.rr + load_left.backspan.rl
reaction_right = load_center.rr + load_right.backspan.rr + load_right.rl + load_left.backspan.rr

rlx, rly = reaction_graph(reaction_left,ll)
rrx, rry = reaction_graph(reaction_right,ll+lc)

shearl = load_left.v(xsl)
shearc = load_left.backspan.v(xsc) + load_center.v(xsc) + load_right.backspan.v(xsc)
shearr = load_right.v(xsr)

momentl = load_left.m(xsl)
momentc = load_left.backspan.m(xsc) + load_center.m(xsc) + load_right.backspan.m(xsc)
momentr = load_right.m(xsr)

slopel = (load_left.eis(xsl)+ ppbeam.cant_left_nl(load_center.eisx(0)+load_right.backspan.eisx(0),ll).eis(xsl))/ (E*I)
slopec = (load_left.backspan.eis(xsc) + load_center.eis(xsc) + load_right.backspan.eis(xsc)) / (E*I)
sloper = (load_right.eis(xsr) + ppbeam.cant_right_nl(load_center.eisx(lc)+load_left.backspan.eisx(lc)).eis(xsr))/ (E*I)

deltal = ((load_left.eid(xsl) + ppbeam.cant_left_nl(load_center.eisx(0)+load_right.backspan.eisx(0),ll).eid(xsl))/(E*I))*12.0
deltac = ((load_left.backspan.eid(xsc)+load_center.eid(xsc)+load_right.backspan.eid(xsc))/(E*I))*12.0
deltar = ((load_right.eid(xsr) + ppbeam.cant_right_nl(load_center.eisx(lc)+load_left.backspan.eisx(lc)).eid(xsr))/(E*I))*12.0

#convert x coordinates to global
xsl = xsl
xsc = xsc + xsl[-1]
xsr = xsr + xsc[-1]

fig=plt.figure

axb = plt.subplot2grid((4, 2), (0, 0), colspan=2)
axr = plt.subplot2grid((4, 2), (1, 0), colspan=2)
axv = plt.subplot2grid((4, 2), (2, 0))
axm = plt.subplot2grid((4, 2), (2, 1))
axs = plt.subplot2grid((4, 2), (3, 0))
axd = plt.subplot2grid((4, 2), (3, 1))

axb.plot(load_left.x_graph,load_left.y_graph)
axb.plot(load_center.x_graph+xsl[-1],load_center.y_graph)
axb.plot(load_right.x_graph+xsc[-1],load_right.y_graph)
axb.plot([0,0,0],[0.5,0,-0.5], alpha=0)
axb.plot(xsl,[0]*len(xsl))
axb.plot(xsc,[0]*len(xsc))
axb.plot(xsr,[0]*len(xsr))
axb.minorticks_on()
axb.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
axb.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
axb.set_ylabel('Load\n(kips, ft-kips, or klf)')
axb.set_xlabel('L (ft)')

axr.plot(rlx,rly)
axr.annotate('RL = {0:.3f} kips'.format(reaction_left), xy=(ll,min(rly)))
axr.plot(rrx,rry)
axr.annotate('RR = {0:.3f} kips'.format(reaction_right), xy=(ll+lc,min(rry)), ha="right")
axr.plot([0,0,0],[0.5,0,-0.5], alpha=0)
axr.plot(xsl,[0]*len(xsl))
axr.plot(xsc,[0]*len(xsc))
axr.plot(xsr,[0]*len(xsr))
axr.minorticks_on()
axr.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
axr.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
axr.set_ylabel('Reaction (kips)')
axr.set_xlabel('L (ft)')

axv.plot(xsl,shearl)
axv.plot(xsc,shearc)
axv.plot(xsr,shearr)
axv.plot(xsl,[0]*len(xsl))
axv.plot(xsc,[0]*len(xsc))
axv.plot(xsr,[0]*len(xsr))
axv.fill_between(xsl,shearl,[0]*len(xsl), facecolor='blue', alpha=0.2)
axv.fill_between(xsc,shearc,[0]*len(xsc), facecolor='blue', alpha=0.2)
axv.fill_between(xsr,shearr,[0]*len(xsr), facecolor='blue', alpha=0.2)
axv.minorticks_on()
axv.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
axv.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
axv.set_ylabel('V (kips)')
axv.set_xlabel('L (ft)')

axm.plot(xsl,momentl)
axm.plot(xsc,momentc)
axm.plot(xsr,momentr)
axm.plot(xsl,[0]*len(xsl))
axm.plot(xsc,[0]*len(xsc))
axm.plot(xsr,[0]*len(xsr))
axm.fill_between(xsl,momentl,[0]*len(xsl), facecolor='red', alpha=0.2)
axm.fill_between(xsc,momentc,[0]*len(xsc), facecolor='red', alpha=0.2)
axm.fill_between(xsr,momentr,[0]*len(xsr), facecolor='red', alpha=0.2)
axm.minorticks_on()
axm.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
axm.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
axm.set_ylabel('M (ft-kips)')
axm.set_xlabel('L (ft)')

axs.plot(xsl,slopel)
axs.plot(xsc,slopec)
axs.plot(xsr,sloper)
axs.plot(xsl,[0]*len(xsl))
axs.plot(xsc,[0]*len(xsc))
axs.plot(xsr,[0]*len(xsr))
axs.fill_between(xsl,slopel,[0]*len(xsl), facecolor='green', alpha=0.2)
axs.fill_between(xsc,slopec,[0]*len(xsc), facecolor='green', alpha=0.2)
axs.fill_between(xsr,sloper,[0]*len(xsr), facecolor='green', alpha=0.2)
axs.minorticks_on()
axs.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
axs.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
axs.set_ylabel('S (rad)')
axs.set_xlabel('L (ft)')

axd.plot(xsl,deltal)
axd.plot(xsc,deltac)
axd.plot(xsr,deltar)
axd.plot(xsl,[0]*len(xsl))
axd.plot(xsc,[0]*len(xsc))
axd.plot(xsr,[0]*len(xsr))
axd.fill_between(xsl,deltal,[0]*len(xsl), facecolor='yellow', alpha=0.2)
axd.fill_between(xsc,deltac,[0]*len(xsc), facecolor='yellow', alpha=0.2)
axd.fill_between(xsr,deltar,[0]*len(xsr), facecolor='yellow', alpha=0.2)
axd.minorticks_on()
axd.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
axd.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
axd.set_ylabel('D (in)')
axd.set_xlabel('L (ft)')

#plt.tight_layout()
plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.4)

plt.show()