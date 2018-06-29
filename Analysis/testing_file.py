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
import datetime


l = 100.0 #ft

E = 29000.00 * 144    #144 is conversion from ksi to ksf - 12^2
I = 30.8 / 12.0**4    #covert from in^4 to ft^4

#Left Cantilever Loads
#loads = [ppbeam.cant_left_point(1,0,l,0),
#            ppbeam.cant_left_point_moment(1,(l*0.5),l,0),
#            ppbeam.cant_left_udl(1,0,l,l,0),
#            ppbeam.cant_left_trap(0,1,0,l,l,0)]

#Right Cantilever Loads           
#loads = [ppbeam.cant_right_trap(1,0,0,l,l,0)]

#Single Span Loads
loads = [ppbeam.udl(1,0,10,l),ppbeam.udl(1,20,30,l),ppbeam.udl(1,40,50,l),ppbeam.udl(1,60,70,l),ppbeam.udl(1,80,90,l)]


stations = 100000

start_t = datetime.datetime.now()
#Cantilever Analysis
#analysis = ppbeam.fixed_free_right_by_stations(loads, stations)
analysis = ppbeam.pin_pin_single_span_by_stations(loads, stations)

interior = [10,20,30,40,50,60,70,80,90]

delta = [analysis[5][0],analysis[5][-1]]

for support in interior:
    
    delta.append(ppbeam.pin_pin_single_span_at_x(loads,support)[3])
    
R, reaction_loads = ppbeam.single_span_solve_fixed_ends_and_redundant_interiors(delta, interior, l, [0,0])

loads = loads + reaction_loads

analysis = ppbeam.pin_pin_single_span_by_stations(loads, stations)

end_t = datetime.datetime.now()

analysis_time = end_t - start_t

x = interior[0]
analysisx = ppbeam.pin_pin_single_span_at_x(loads,x)

start_plot_t = datetime.datetime.now()
plt.plot(analysis[0],analysis[6])
plt.plot([x,x], [0,analysisx[3]], 'r+-')
plt.plot([0,l],[0,0])
plt.show()
end_plot_t = datetime.datetime.now()
plotting_time = end_plot_t - start_plot_t

print 'Analysis: {0}'.format(analysis_time)
print 'Plot: {0}'.format(plotting_time)