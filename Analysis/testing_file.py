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

import three_moment_method_e as tmm

L = 10.0 #ft

E = 1    #144 is conversion from ksi to ksf - 12^2
I = 1    #covert from in^4 to ft^4

udl = ppbeam.udl(1,2,5,L)

ff_udl = udl.fef()

trap = ppbeam.trap(0,1,2,5,L)

ff_trap = trap.fef()

point = ppbeam.pl(1,2,L)

ff_point = point.fef()

point_moment = ppbeam.point_moment(1,2,L)

ff_pm = point_moment.fef()

L1 = ppbeam.trap(1,0,0,10,10)
L2 = ppbeam.udl(1,1,8,10)
L3 = ppbeam.pl(1,3,10)
L4 = ppbeam.point_moment(1,5,10)

loads = [L1,L2,L3,L4]

eq, eqs = ppbeam.center_span_piecewise_function(loads)

res = ppbeam.eval_beam_piece_function(eq,9)

##Left Cantilever Loads
##loads = [ppbeam.cant_left_point(1,0,l,0),
##            ppbeam.cant_left_point_moment(1,(l*0.5),l,0),
##            ppbeam.cant_left_udl(1,0,l,l,0),
##            ppbeam.cant_left_trap(0,1,0,l,l,0)]
#
##Right Cantilever Loads           
##loads = [ppbeam.cant_right_trap(1,0,0,l,l,0)]
#
##Single Span Loads
#loads = [ppbeam.udl(1,0,30,L)]
#
#
#stations = 500
#
#start_t = datetime.datetime.now()
##Cantilever Analysis
##analysis = ppbeam.fixed_free_right_by_stations(loads, stations)
#analysis = ppbeam.pin_pin_single_span_by_stations(loads, stations)
#
#interior = [10,20]
#
#delta = [analysis[5][0],analysis[5][-1]]
#
#for support in interior:
#    
#    delta.append(ppbeam.pin_pin_single_span_at_x(loads,support)[3])
#  
#R, reaction_loads = ppbeam.single_span_solve_fixed_ends_and_redundant_interiors(delta, interior, L, [0,0])
#
#loads = loads + reaction_loads
#
#analysis = ppbeam.pin_pin_single_span_by_stations(loads, stations)
#
#end_t = datetime.datetime.now()
#
#analysis_time = end_t - start_t
#
#start_t = datetime.datetime.now()
#
#w = 1000/12.0
#test_3mm = tmm.three_moment_method([120.0,120.0,120.0],[30.8,30.8,30.8],'N',[[w,w,0,120,'UDL',0],[w,w,0,120,'UDL',1],[w,w,0,120,'UDL',2]], 29000000.00,167,[0,0,0,0])
#
#end_t = datetime.datetime.now()
#
#analysis_3mm_time = end_t - start_t
#
#results_3mm = test_3mm.res()
#
#
#print 'Analysis: {0}'.format(analysis_time)
#print 'Analysis - 3mm: {0}'.format(analysis_3mm_time)