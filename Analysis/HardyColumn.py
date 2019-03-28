# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 15:30:06 2019

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

from __future__ import division

'''
Example of the Hardy Cross Column Analogy to calculate non-prismatic
member end stiffnesses and carry over factors to be used in a moment
distribution analysis
'''

segmentLengths = [12,12] #ft
E = [288000]*len(segmentLengths) #k/ft^2
I = [0.667,5.333] #ft^4

L_tot = sum(segmentLengths)

hardy_segment_widths = [1.0/(e*i) for e,i in zip(E,I)]

hardy_segment_areas = [a*b for a,b in zip(segmentLengths,hardy_segment_widths)]

hardy_Area = sum(hardy_segment_areas)

hardy_segment_centers = []
for i,L in enumerate(segmentLengths):
    if i == 0:
        hardy_segment_centers.append(L/2.0)
    else:
        x = L/2.0 + sum(segmentLengths[0:i])
        hardy_segment_centers.append(x)
        
hardy_segment_Ax = [a*b for a,b in zip(hardy_segment_areas,hardy_segment_centers)]

hardy_centroid = sum(hardy_segment_Ax) / hardy_Area

hardy_segment_xbar = [a - hardy_centroid for a in hardy_segment_centers]

hardy_segment_Icg = [(a*b*b*b)/ 12.0 for a,b in zip(hardy_segment_widths,segmentLengths)]

hardy_segment_Ad2 = [a*b*b for a,b in zip(hardy_segment_areas,hardy_segment_xbar)]

hardy_I = sum(hardy_segment_Icg)+sum(hardy_segment_Ad2)

'''
ca = distance from left end to centroid
cb = distance from right end to centroid
'''
ca = -1.0*hardy_centroid
cb = L_tot - hardy_centroid

'''
e_a = distance from point load @ end A to centroid = ca
e_b = distance from point load @ end B to centroid = cb
'''
e_a = ca
e_b = cb

faa = (1.0/hardy_Area) + ((1.0*e_a*ca) / hardy_I)
fba = (1.0/hardy_Area) + ((1.0*e_a*cb) / hardy_I)

Ka = faa
Ca = fba/faa

fab = (1.0/hardy_Area) + ((1.0*e_b*cb) / hardy_I)
fbb = (1.0/hardy_Area) + ((1.0*e_b*ca) / hardy_I)

Kb = fab
Cb = fbb/fab

CaKa = Ca*Ka
CbKb = Cb*Kb

check = CaKa == CbKb