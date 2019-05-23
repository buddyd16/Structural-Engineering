from __future__ import division
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import TimoshenkoFormulas as timobm
import pin_pin_beam_equations_classes as ebbm

# Properties for a W36x135
E_ksi = 29000
G_ksi = 11200
kA_in2 = 21.36
I_in4 = 7800

# Span Info
L_ft = 25
a_ft = 12.5
M_ftkips = 1000.0

#convert G and E to ksf
G_ksf = G_ksi*144.0
E_ksf = E_ksi*144.0

#convert kA to ft^2
kA_ft2 = kA_in2 * (1/144.0)

#convert I to ft^4
I_ft4 = I_in4 / math.pow(12,4)

step = L_ft/20.0

x = [0+(i*step) for i in range(21)]
bm = [0 for i in x]

M_timo = timobm.PointLoad(M_ftkips,a_ft,L_ft,E_ksf,I_ft4,G_ksf,kA_ft2)

M_ebb = ebbm.pl(M_ftkips,a_ft,L_ft)

theta_timo = [-1.0*M_timo.thetax(i) for i in x]

theta_ebb = [M_ebb.eisx(i)/(E_ksf*I_ft4) for i in x]

tol = 1e-15

theta_dif = [i-y if abs(i-y) > abs(tol) else 0 for i,y in zip(theta_timo,theta_ebb)]

delta_timo = [-12.0*M_timo.deltax(i) for i in x]

delta_ebb = [12.0*M_ebb.eidx(i)/(E_ksf*I_ft4) for i in x]

delta_dif = [i-y if abs(i-y) > abs(tol) else 0 for i,y in zip(delta_timo,delta_ebb)]

c1 = M_timo.c1
c2 = M_timo.c2
c3 = M_timo.c3
c4 = M_timo.c4

ax1 = plt.subplot2grid((3,3),(1,0))
ax2 = plt.subplot2grid((3,3),(2,0))
ax3 = plt.subplot2grid((3,3),(1,1))
ax4 = plt.subplot2grid((3,3),(2,1))
ax5 = plt.subplot2grid((3,3),(1,2))
ax6 = plt.subplot2grid((3,3),(2,2))
ax7 = plt.subplot2grid((3,3),(0,0))
ax8 = plt.subplot2grid((3,3),(0,1))
ax9 = plt.subplot2grid((3,3),(0,2))

ax1.plot(x,theta_ebb)
ax2.plot(x,delta_ebb)
ax3.plot(x,theta_timo)
ax4.plot(x,delta_timo)
ax5.plot(x,theta_dif)
ax6.plot(x,delta_dif)
ax7.plot(x,bm)
ax8.plot(x,bm)
ax9.plot(x,bm)

theta_timo_norm = [(i)/max((max(theta_timo), abs(min(theta_timo))))*1.25 if max((max(theta_timo), abs(min(theta_timo)))) != 0 else 0 for i in theta_timo]
theta_ebb_norm = [(i)/max((max(theta_ebb), abs(min(theta_ebb))))*1.25 if max((max(theta_ebb), abs(min(theta_ebb)))) != 0 else 0 for i in theta_ebb]
theta_dif_norm = [(i)/max((max(theta_dif), abs(min(theta_dif))))*1.25 if max((max(theta_dif), abs(min(theta_dif)))) !=0 else 0 for i in theta_dif]

for i,y in enumerate(x):
    
    h = 0.5
    
    xs_timo = [y+(theta_timo_norm[i]*h), y-(theta_timo_norm[i]*h)]
    xs_ebb = [y+(theta_ebb_norm[i]*h), y-(theta_ebb_norm[i]*h)]
    xs_dif = [y+(theta_dif_norm[i]*h), y-(theta_dif_norm[i]*h)]
    
    ys = [-h,h]
    
    ax7.plot(xs_ebb,[-h,h],'r')
    ax8.plot(xs_timo,[-h,h],'r')
    ax9.plot(xs_dif,[-h,h],'r')
   
    
ax7.set_ylim([-1,1])
ax8.set_ylim([-1,1])
ax9.set_ylim([-1,1])

plt.tight_layout()

plt.show()