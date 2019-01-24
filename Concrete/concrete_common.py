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
import math
from scipy.integrate import simps
import matplotlib.pyplot as plt

def stress_strain_desayi_krishnan(fprimec, ultimate_strain, k, strain_report):
    '''
    method for a parabolic stress-strain relationship for concrete in compression
    Desayi, P. and Krishnan, S., Equation for the Stress-Strain Curve of Concrete, ACI
    Journal, Proceedings V. 61, No. 3, Mar. 1964, pp. 345-350
    
    fprimec = f'c = 28-day compressive strength of concrete -- type: float
    ultimate_strain = eu = strain at failure -- type: float  ACI: 0.003 (English Units)
    k = k*f'c = stress at ultimate strain -- type: float  ACI: 0.85 (English Units)
    strain_report = e = strain at location where stress is desired -- type: float
    '''
    
    fo = fprimec
    
    # solve for eo = strain at fo
    # E = 2*fo / eo
    # eo has two possible solutions
    # eo = eu - sqrt(-1*(k^2 - 1) * eu^2) / k or sqrt(-1*(k^2 - 1) * eu^2) + eu / k
    
    eo1 = (ultimate_strain - math.sqrt(-1*(math.pow(k,2) - 1)*math.pow(ultimate_strain,2))) / k
    eo2 = (math.sqrt(-1*(math.pow(k,2) - 1)*math.pow(ultimate_strain,2))+ultimate_strain) / k
    
    eo = min(eo1,eo2)
    
    E = 2*fo / eo
    
    f = (E*strain_report) / (1+math.pow(strain_report/eo,2))
    
    return f

def stress_strain_collins_et_all(fprimec, ultimate_strain, strain_report):
    '''
    method for a parabolic stress-strain relationship for concrete in compression
    Collins, M.P., Mitchell D. and MacGregor, J.G., Structural Consideration for High-Strength
    Concrete, Concrete International, V. 15, No. 5, May 1993, pp. 27-34. 
    '''
    k = 0.67 + (fprimec / 9000.0) # for PSI units
    n = 0.8 + (fprimec / 2500.0) # for PSI units
    Ec = (40000*math.sqrt(fprimec)) + 1000000 # for PSI units
    
    ecprime = (fprimec / Ec)*(n/(n-1))
    
    e = strain_report/ecprime
    if e <= 1:
        f = ((e) * (n / (n-1+math.pow(e,n)))) * fprimec
    else:
        f = ((e) * (n / (n-1+math.pow(e,n*k)))) * fprimec
    
    return f
    
def strain_at_depth_from_top(eu,na_depth,depth):
    
    return (eu/na_depth)*depth

def polygon_area(x,y):
    '''
    given a list of x and y coordinates
    return the signed area of the polygon
    polygon must be closed
    '''
    
    num_points = len(x)-1
    
    area = 0
    
    i=0
    for i in range(0,num_points):
        area = area + (x[i]*y[i+1]-x[i+1]*y[i])
    area = area/2
    
    return area

def polygon_center(x,y):
    '''
    given a list of x and y coordinates
    return the x,y coordinated of the polygon centroid
    polygon must be closed
    '''
    num_points = len(x)-1
    x_bar=0
    y_bar=0
    
    i=0
    for i in range(0,num_points):
        x_bar = x_bar + (x[i]+x[i+1])*(x[i]*y[i+1]-x[i+1]*y[i])
        y_bar = y_bar + (y[i]+y[i+1])*(x[i]*y[i+1]-x[i+1]*y[i])

    area = polygon_area(x,y)
    
    x_bar = x_bar / (6*area)
    y_bar = y_bar/(6*area)
    
    return (x_bar,y_bar)

def length_by_two_points(ax,ay,bx,by):
    dx = abs(bx - ax)
    dy = abs(by - ay)

    length = (dx*dx + dy*dy)**0.5

    return length

def x_point_on_line_by_two_points(ax,ay,bx,by,y):
    
    if ax == bx:
        return ax
    else:
        l = (y-ay)
        
        c = (by-ay) / (bx-ax)
    
        r = c*ax
        
        return (l + r) / c
    
class Line:
    def __init__(self, start=[0,0], end=[1,1]):
        self.error_string = ''
        
        if start == end:
            self.error_string = 'Not Valid - Start Point = End Point'
        
        else:
            self.start = start
            self.end = end
            self.startx = start[0]
            self.starty = start[1]
            self.endx = end[0]
            self.endy = end[1]
        
def compression_forces_locations_general_poly_collins(lines,fprimec,eu,na_depth):
    '''
    given an list of lines that form a closed polygon
    return a list of compression forces and (x,y) application points
    
    assumptions
    section is oriented such that the neutral axis is horizontal
        this may require the cross section to be transformed to the neutral axis angle
    
    Method:
    determine the peak coordinate - max y value NA depth is from this point down
    at each slice get the strain and parabolic stress distribution
    determine the edge intersection points at the slice elevation
    at each slice determine the width of the member - force @ slice = width*stress
    (x,y) application point is slice width/2 + slice left coord y is slice elevation
    '''
    
    # Loop thru the lines and find the max y coordinate
    y = []
    for line in lines:
        y.extend([line.start[1],line.end[1]])
    
    top = max(y)
    
    na_y = top - na_depth
    
    # create the slices and determine the strains and stresse at each slice
    slices = []
    
    num_slices = 100
    
    step = na_depth / num_slices

    for i in range(0,num_slices+1):
        slices.append(0+step*i)
        
    strains = []
    
    for s in slices:
        strains.append(strain_at_depth_from_top(eu,na_depth,s))
        
    stresses = []
    for strain in strains:
        stresses.append(stress_strain_collins_et_all(fc_psi,eu,strain))
        
    # correct slice elevations to be on the cross section and not start at 0
    
    slices_global = [x+na_y for x in slices]
    
    # at each slice determine what lines are intersected
    # for polygons with holes determine left and right pairs
    # a left intersection is where the line start point is above the slice
    # a right intersection is where the line end point is above the slice
    
    slice_forces = []
    
    s = 0
    
    for loc in slices_global:
        
        pts = []
        for line in lines:
            if line.start[1] < loc < line.end[1] or line.end[1] < loc < line.start[1]:
                int_point_x = x_point_on_line_by_two_points(line.start[0],line.start[1],line.end[0],line.end[1],loc)
                
                if line.start[1] > loc:
                    side = 'left'
                    
                else:
                    side = 'right'
                
                pts.append([int_point_x,side])
                    
            elif line.start[1] == loc and line.end[1] == loc:
                
                left = min(line.start[0],line.end[0])
                right = max(line.start[0],line.end[0])
                pts.extend([[left,'left'],[right,'right']])
            
            else:
                pass
                   
        # sort the list of pts by x coord
        # this should result in pairs of left and right pieces
        pts.sort(key=lambda x:x[0])
        
        i=0
        for point in pts:
            
            if point[1] == 'left':
                
                if pts[i+1][1] == 'right':
                    
                    width = length_by_two_points(point[0],loc,pts[i+1][0],loc)
                    
                    f = stresses[s]*width*step
                    
                    slice_forces.append([f,[(point[0]+width/2.0),loc]])
                else:
                    pass
            else:
                pass
            i+=1
        
        s+=1
    
    return [slices_global, strains, stresses, slice_forces]
                
                
        
    
eu = 0.003
fc_psi = 3000

na_depth_in = 2.03

num_pts = 100

x = []
step = na_depth_in / num_pts

for i in range(0,num_pts+1):
    x.append(0+step*i)
    
strains = []

for i in x:
    strains.append(strain_at_depth_from_top(eu,na_depth_in,i))
    
stresses = []

for strain in strains:
    stresses.append(stress_strain_desayi_krishnan(fc_psi,eu,0.85,strain))

stresses_collins = []
for strain in strains:
    stresses_collins.append(stress_strain_collins_et_all(fc_psi,eu,strain))
    

area_desayi = simps(stresses,x)
area_collins = simps(stresses_collins,x)

# add points to make a closed polygon

stresses.extend([0,0]) 
stresses_collins.extend([0,0])
x.extend([na_depth_in,0])

center_desayi = polygon_center(x,stresses)
center_collins = polygon_center(x,stresses_collins)

NA_moment_desayi = area_desayi * center_desayi[0]
NA_moment_collins = area_collins * center_collins[0]

print area_desayi, polygon_area(x,stresses)
print area_collins, polygon_area(x,stresses_collins)
print center_desayi[0]
print center_collins[0]


# concrete beam Mn test
# 12x24 f'c = 3000 fy=60 ksi w/ (2)#6 bottom

Ts = 2*60000*0.44
sect_b = 12

# find NA depth so Cc = Ts - desayi
a=0
b=21.75
c=0
pna = 0

loop_max = 10000
tol = 0.0000000000001
loop = 0

while loop<loop_max:
    c = (a+b)/2
    na_depth_in = c

    num_pts = 100

    x = []
    step = na_depth_in / num_pts

    for i in range(0,num_pts+1):
        x.append(0+step*i)
        
    strains = []

    for i in x:
        strains.append(strain_at_depth_from_top(eu,na_depth_in,i))
        
    stresses = []

    for strain in strains:
        stresses.append(stress_strain_desayi_krishnan(fc_psi,eu,0.85,strain))
    
    stresses.extend([0,0])
    x.extend([na_depth_in,0])
    
    comp_area = polygon_area(x,stresses)
    compression_c = comp_area*sect_b
    
    if abs(compression_c) == Ts or (b-a)/2 <= tol:
        pna = c
        loop = loop_max
    elif abs(compression_c) > Ts:
        b = c
    else:
        a = c
    loop+=1

na_desayi = na_depth_in
center_desayi = polygon_center(x,stresses)

while loop<loop_max:
    c = (a+b)/2
    na_depth_in = c

    num_pts = 100

    x = []
    step = na_depth_in / num_pts

    for i in range(0,num_pts+1):
        x.append(0+step*i)
        
    strains = []

    for i in x:
        strains.append(strain_at_depth_from_top(eu,na_depth_in,i))
        
    stresses = []

    for strain in strains:
        stresses.append(stress_strain_collins_et_all(fc_psi,eu,strain))
    
    stresses.extend([0,0])
    x.extend([na_depth_in,0])
    
    comp_area = polygon_area(x,stresses)
    compression_c = comp_area*sect_b
    
    if abs(compression_c) == Ts or (b-a)/2 <= tol:
        pna = c
        loop = loop_max
    elif abs(compression_c) > Ts:
        b = c
    else:
        a = c
    loop+=1
    
na_collins = na_depth_in
center_collins = polygon_center(x,stresses)

#plt.plot(x,stresses)
#plt.plot(center_desayi[0],center_desayi[1],'b+')
#plt.plot(center_collins[0],center_collins[1],'go')
#
#plt.show()

shape = [Line([0,0],[12,0]),Line([12,0],[12,24]),Line([12,24],[0,24]),Line([0,24],[0,0])]


res = compression_forces_locations_general_poly_collins(shape,fc_psi,eu,na_collins)

comp_c = sum(x[0] for x in res[3])

cs = [sc[0] for sc in res[3]]
xs = res[0][:]

plt.plot(xs, cs)
plt.show()