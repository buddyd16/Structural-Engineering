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


import pin_pin_beam_equations_classes as ppbeam
import matplotlib.pyplot as plt


l = 5.0 #ft

E = 29000.00 * 144    #144 is conversion from ksi to ksf - 12^2
I = 30.8 / 12.0**4    #covert from in^4 to ft^4

#Loads
#loads = [ppbeam.cant_left_point(1,0,l,0),
#            ppbeam.cant_left_point_moment(1,(l*0.5),l,0),
#            ppbeam.cant_left_udl(1,0,l,l,0),
#            ppbeam.cant_left_trap(0,1,0,l,l,0)]
            
loads = [ppbeam.cant_right_trap(1,0,0,l,l,0)]

stations = 50

analysis = ppbeam.fixed_free_right_by_stations(loads, stations)


x = l/5.0
analysisx = ppbeam.fixed_free_at_x(loads,x)

plt.plot(analysis[0],analysis[4])
plt.plot([x,x], [0,analysisx[1]], 'r+-')
plt.show()