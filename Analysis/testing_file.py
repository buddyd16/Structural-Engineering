# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 17:35:53 2018

@author: DonB
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
lr = 5


E = 29000 * 144  #144 is conversion from ksi to ksf - 12^2
I = 30.8 / 12.0**4 #covert from in^4 to ft^4

step_left = ll/500.0
step_backspan = lc/500.0
step_right = lr/500.0

xsl = zeros(501)
xsc = zeros(501)
xsr = zeros(501)

reaction_left = 0
reaction_right = 0

shearl = zeros(501)
shearc = zeros(501)
shearr = zeros(501)

momentl = zeros(501)
momentc = zeros(501)
momentr = zeros(501)

slopel = zeros(501)
slopec = zeros(501)
sloper = zeros(501)

deltal = zeros(501)
deltac = zeros(501)
deltar = zeros(501)

xsl[0]=0
xsc[0]=0
xsr[0]=0

for i in range(1,501):
    xsl[i] = xsl[i-1] + step_left
    xsc[i] = xsc[i-1] + step_backspan
    xsr[i] = xsr[i-1] + step_right

if ll == 0:
    load_left = [ppbeam.cant_left_point(0,0,ll,lc)]

else:
    load_left = [ppbeam.cant_left_point(0,0,ll,lc), ppbeam.cant_left_trap(1,0.5,1,4,ll,lc), ppbeam.cant_left_point_moment(1,2,ll,lc), ppbeam.cant_left_point(0.75,3,ll,lc)]

load_center = [ppbeam.pl(0,0,lc), ppbeam.trap(1,0.5,2,4,lc), ppbeam.trap(-0.5,-1,6,8,lc), ppbeam.point_moment(-1,5,lc), ppbeam.udl(0.375,0,lc,lc), ppbeam.pl(2,4.5,lc)]

if lr == 0:
    load_right = [ppbeam.cant_right_point(0,0,lr,lc)]
else:
    load_right = [ppbeam.cant_right_point(0,0,lr,lc), ppbeam.cant_right_trap(-0.5,-1,1,4,lr,lc), ppbeam.cant_right_point_moment(1,4,lr,lc), ppbeam.cant_right_udl(0.4,1,3.25,lr,lc)]    


for load in load_left:
    reaction_left = reaction_left + load.rr + load.backspan.rl
    reaction_right = reaction_right + load.backspan.rr
    
    shearl = shearl + load.v(xsl)
    shearc = shearc + load.backspan.v(xsc)
    
    momentl = momentl + load.m(xsl)
    momentc = momentc + load.backspan.m(xsc)
    
    slopel = slopel + load.eis(xsl)
    slopec = slopec + load.backspan.eis(xsc)
    sloper = sloper + ppbeam.cant_right_nl(load.backspan.eisx(lc)).eis(xsr)
    
    deltal = deltal + load.eid(xsl)
    deltac = deltac + load.backspan.eid(xsc)
    deltar = deltar + ppbeam.cant_right_nl(load.backspan.eisx(lc)).eid(xsr)

for load in load_center:
    reaction_left = reaction_left + load.rl
    reaction_right = reaction_right  + load.rr
    
    shearc = shearc + load.v(xsc)
    
    momentc = momentc + load.m(xsc)
   
    slopel = slopel + ppbeam.cant_left_nl(load.eisx(0),ll).eis(xsl)
    slopec = slopec + load.eis(xsc)
    sloper = sloper + ppbeam.cant_right_nl(load.eisx(lc)).eis(xsr)
    
    deltal = deltal + ppbeam.cant_left_nl(load.eisx(0),ll).eid(xsl)
    deltac = deltac + load.eid(xsc)
    deltar = deltar + ppbeam.cant_right_nl(load.eisx(lc)).eid(xsr)

for load in load_right:
    reaction_left = reaction_left + load.backspan.rl
    reaction_right = reaction_right + load.backspan.rr + load.rl
    
    shearc = shearc + load.backspan.v(xsc)
    shearr = shearr + load.v(xsr)
    
    momentc = momentc + load.backspan.m(xsc)
    momentr = momentr + load.m(xsr)
    
    slopel = slopel + ppbeam.cant_left_nl(load.backspan.eisx(0),ll).eis(xsl)
    slopec = slopec + load.backspan.eis(xsc)
    sloper = sloper + load.eis(xsr)
    
    deltal = deltal + ppbeam.cant_left_nl(load.backspan.eisx(0),ll).eid(xsl)
    deltac = deltac + load.backspan.eid(xsc)
    deltar = deltar + load.eid(xsr)

slopel = slopel / (E*I)
slopec = slopec / (E*I)
sloper = sloper / (E*I)

deltal = (deltal / (E*I))*12.0
deltac = (deltac / (E*I))*12.0
deltar = (deltar / (E*I))*12.0
  
rlx, rly = reaction_graph(reaction_left,ll)
rrx, rry = reaction_graph(reaction_right,ll+lc)

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

for load in load_left:
    axb.plot(load.x_graph,load.y_graph)
for load in load_center:
    axb.plot(load.x_graph+xsl[-1],load.y_graph)
for load in load_right:
    axb.plot(load.x_graph+xsc[-1],load.y_graph)
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