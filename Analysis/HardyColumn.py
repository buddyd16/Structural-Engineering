'''
BSD 3-Clause License
Copyright (c) 2019, Donald N. Bockoven III
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

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