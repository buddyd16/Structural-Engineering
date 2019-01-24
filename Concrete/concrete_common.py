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
    
eu = 0.003
fc_psi = 3000

na_depth_in = 1.43

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

plt.plot(x,stresses)
plt.plot(x,stresses_collins)
plt.plot(center_desayi[0],center_desayi[1],'b+')
plt.plot(center_collins[0],center_collins[1],'go')

plt.show()
