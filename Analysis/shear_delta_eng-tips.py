# -*- coding: utf-8 -*-
"""
Created on Mon May 13 16:43:13 2019

@author: DonB
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def point_shear_delta(P_kips,a_ft,L_ft,x_ft,G_ksi,kA_in2):
    
    #Reaction
    RL_kips = P_kips*(L_ft-a_ft)*(1/L_ft)
    RR_kips = P_kips - RL_kips
    #convert G to ksf
    G_ksf = G_ksi*144.0
    
    #convert kA to ft^2
    kA_ft2 = kA_in2 * (1/144.0)
    
    C4 = P_kips*a_ft / (kA_ft2*G_ksf)
    
    if x_ft <= a_ft:
        delta_ft = (RL_kips*x_ft) / (kA_ft2*G_ksf)
    
    else:
        delta_ft = ((-1.0*RR_kips*x_ft) / (kA_ft2*G_ksf)) + C4
    
    delta_in = 12.0*delta_ft
    
    return delta_in

def animation_step(frame,p,L,x,x_rev,g,ka, ret):

    a_front = x[frame]
    
    a_back = x_rev[frame]
    
    delta_front = [point_shear_delta(p,a_front,L,i,g,ka) for i in x]
    delta_back = [point_shear_delta(-p,a_back,L,i,g,ka) for i in x]
    
    delta = [i+y for i,y in zip(delta_front, delta_back)]
    
    l1.set_data(x, delta)
    l2.set_data([a_front,a_front],[0,-0.9])
    l3.set_data([a_back,a_back],[0,0.9])

def animation_step_amp(frame,p,L,x,x_rev,g,ka, ret):
    
    if  x_rev[frame] == x[frame]:
        multi=1
    else:
        L_prime = x_rev[frame] - x[frame]
        multi = L/L_prime
    
    a_front = x[frame]  
    a_back = x_rev[frame]
    
    delta_front = [point_shear_delta(p*multi,a_front,L,i,g,ka) for i in x]
    delta_back = [point_shear_delta(-p*multi,a_back,L,i,g,ka) for i in x]
    
    delta = [i+y for i,y in zip(delta_front, delta_back)]
    
    l1.set_data(x, delta)
    l2.set_data([a_front,a_front],[0,-0.9])
    l3.set_data([a_back,a_back],[0,0.9])          
        
G_ksi = 11200
kA_in2 = 21.36
L_ft = 5
a_ft = 2.5
P_kips = 1000.0
x_ft = 2.5

step = L_ft/100.0

x = [0+(i*step) for i in range(101)]
x_rev = x[::-1]

bm = [0]*len(x)

fig, ax = plt.subplots()

ax.set_xlim(-1,6)
ax.set_ylim(-0.12,0.12)
ax.plot(x,bm)

l1, = ax.plot([],[],'g')
l2, = ax.plot([],[],'r')
l3, = ax.plot([],[],'b')

ani = animation.FuncAnimation(fig, animation_step_amp, frames = np.arange(0,100), fargs=(P_kips,L_ft,x,x_rev,G_ksi,kA_in2,0), interval=100)

plt.rcParams["animation.convert_path"] = "C:\Program Files\ImageMagick-7.0.7-Q16\magick.exe"

ani.save("eng-tips_collapsing_point_loads_amped.gif",writer="imagemagick", extra_args="convert")

plt.show()



