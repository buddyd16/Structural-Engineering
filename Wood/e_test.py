# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 18:39:51 2019

@author: DonB
"""

from __future__ import division
import wood_classes as wood
import matplotlib.pyplot as plt

wall = wood.wood_stud_wall(1.5,5.5,10,12,"No. 2",875,150,1150,1400000,510000,565,19,90,0,0, [1,1,1,1,1,1], 0, 48, 0, 0)

max_e = (5.5/6.0)
step_e = max_e/10.0

ecc = [0+(i*step_e) for i in range(11)]

ecc.extend([1,1.5,2,2.5,3,3.5,4])



fig, ax1 = plt.subplots()
fig.set_size_inches(17, 11)
ax1.minorticks_on()
ax1.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
ax1.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
ax2 = ax1.twinx()
for x in ecc: 
    w,p,d = wall.wall_pm_diagram_cd_stud(1,x)
    if x == max_e:
        ax1.plot(w,p, color='r')
        ax2.plot(w,d, color='r')
    else:
        ax1.plot(w,p, color='k')
        ax2.plot(w,d, color='k', alpha=0.4)

ax1.set_ylabel('Axial (lbs)')
ax1.set_xlabel('Moment (in-lbs)')
ax2.set_ylabel('Mid Height Deflection (in)')

plt.title('2x6 SPF No.2 - 10 ft tall - 12" spacing - variable ecc')
fig.tight_layout()

plt.savefig('wall_e_test.jpg', dpi=100)

plt.show()

