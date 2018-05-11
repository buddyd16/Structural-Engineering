# -*- coding: utf-8 -*-
"""
Created on Thu May 10 16:08:02 2018

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
import math
import numpy as np
import matplotlib.pyplot as plt

class Line:
    def __init__(self, start=[0,0], end=[1,1], hc_ft = 1.0):
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
            
            self.length_calc()
            self.angle_degrees_calc()
            self.hc_ft = hc_ft
            
            self.drift_line_x = []
            self.drift_line_y = []
            self.drift_lu = []
            self.drift_hd = []
            self.drift_pd = []
            self.drift_plot_labels = []
            
            
    def reset_drift_lines(self):
        self.drift_line_x = []
        self.drift_line_y = []
        self.drift_lu = []
        self.drift_hd = []
        self.drift_pd = []
        self.drift_plot_labels = []
                  
    def length_calc(self):
        dx = abs(self.endx - self.startx)
        dy = abs(self.endy - self.starty)
        
        self.length = (dx**2 + dy**2)**0.5
        
        return self.length
        
    def angle_degrees_calc(self):
        dx = self.endx - self.startx
        dy = self.endy - self.starty
        
        if dx == 0 and dy > 0:
            angle = 90
            
        elif dx == 0  and dy <0:
            angle = 270
        
        else:
            angle = math.atan2(dy, dx)
            angle = angle * (180/math.pi)
            
            if angle < 0:
                angle = angle + 360
                
        self.perp_angle = angle + 90
                
        self.angle = angle
        
        
        return angle
        
    def interior_points_calc(self,num_points):
        l = self.length
        step = l/(num_points+1)
        
        points = []
        
        for i in range(1,num_points+1):
            t = (i*step)/self.length
            
            x = ((1-t)*self.startx) + (t*self.endx)
            y = ((1-t)*self.starty) + (t*self.endy)
            
            point = [x,y]
            
            points.append(point)
        
        self.internal_points = points
        self.internal_points_x = [coordx[0] for coordx in points]
        self.internal_points_y = [coordy[1] for coordy in points]
        
        return points

def point_at_angle_distance(a=[0,0],angle_degrees=0,distance=1):
    #determine point at distance and angle from point 0

    dx = math.cos(math.radians(angle_degrees))*distance
    dy = math.sin(math.radians(angle_degrees))*distance
    
    point = [a[0] + dx, a[1] + dy]
    
    return point

def line_line_intersection_points(a0x,a0y,a1x,a1y,b0x,b0y,b1x,b1y):
          
    try:
        A = np.array([[a0x, a0y], [a1x, a1y]])
        B = np.array([[b0x, b0y], [b1x, b1y]])
        t, s = np.linalg.solve(np.array([A[1]-A[0], B[0]-B[1]]).T, B[0]-A[0])
        res = []
        res.append(((1-t)*A[0] + t*A[1]))
        res.append(((1-s)*B[0] + s*B[1]))
    except:
        res = 'no int'
    
    return res

         
##testing area
pg_psf = 25
snow_density_pcf = min((0.13*pg_psf) + 14, 30)
Ce = 1.0
Ct = 1.0
Cs = 1.0
I = 1.0
pf_psf = 0.7*Ce*Ct*I*pg_psf
ps_psf = Cs*pf_psf
hb_ft = ps_psf/snow_density_pcf
hc_ft = [3.0,1.0,5.0,0.5,1.0]

x = [1,30,30,200,200,188,188,5,5,1]
y = [1,-30,-30,-1,-1,90,90,20,20,1]

lines = []

hc=0
for i in range(0, int(len(x)/2)):
    if i == 0:
        i = i
    else:
        i *=2
        
    xs = x[i]
    ys = y[i]
    start = [xs,ys]
    xe = x[i+1]
    ye = y[i+1]
    end = [xe,ye]
    lines.append(Line(start,end, hc_ft[hc]))
    hc+=1

perp_lines = []

intersect_points = []
points_x = []
points_y = []

dist = 40
check_string = '--Test Point--'
for line in lines:
    line.interior_points_calc(20)
    line.reset_drift_lines()
    
    for interior_point in line.internal_points:
        perp_line_start = interior_point
        angle = line.perp_angle
        perp_line_end = point_at_angle_distance(perp_line_start, angle, dist)
        
        perp_lines.append([perp_line_start, perp_line_end])
        
        b0x = perp_line_start[0]
        b0y = perp_line_start[1]
        b1x = perp_line_end[0]
        b1y = perp_line_end[1]
        
        for check_line in lines:
            if check_line == line:
                pass
            else:           
                a0x = check_line.startx
                a0y = check_line.starty
                a1x = check_line.endx
                a1y = check_line.endy
                
                intersect_point = line_line_intersection_points(a0x,a0y,a1x,a1y,b0x,b0y,b1x,b1y)
                
                if intersect_point == 'no int':
                    pass
                else:
                    point_x = intersect_point[0][0]
                    point_y = intersect_point[0][1] 
                    check_string = check_string + '\nx = {0}\n'.format(point_x)
                    check_string = check_string + 'range: {0} - {1}\n'.format(a0x,a1x)
                    x_ok = min(a0x,a1x) <= point_x <= max(a0x,a1x)
                    check_string = check_string + 'check: {0}\n'.format(x_ok)
                    check_string = check_string + 'y = {0}\n'.format(point_y)
                    check_string = check_string + 'range: {0} - {1}\n'.format(a0y,a1y)
                    y_ok = min(a0y,a1y) <= point_y <= max(a0y,a1y)
                    check_string = check_string + 'check: {0}\n'.format(y_ok)
                    if x_ok == True and y_ok == True:
                        intersect_points.append(intersect_point)
                        points_x.append(point_x)
                        points_y.append(point_y)
                        
                        dx = abs(point_x - b0x)
                        dy = abs(point_y - b0y)
            
                        lu = (dx**2 + dy**2)**0.5
                        
                        lu = max(lu,25)
                        
                        hd_ft = (0.43 * (lu**(1.0/3.0))*((pg_psf+10)**(1.0/4.0))) - 1.5
                        hd_ft = 0.75 * hd_ft 
                        
                        if hd_ft <= line.hc_ft:
                            w_ft = 4*hd_ft
                            hd_ft = hd_ft
                        else:
                            w_ft = min((4*hd_ft**2)/line.hc_ft, 8*line.hc_ft)
                            hd_ft = line.hc_ft
                        
                        drift_point = point_at_angle_distance(perp_line_start, angle,w_ft)
                        
                        pd_psf = snow_density_pcf*hd_ft
                        
                        line.drift_line_x.append(drift_point[0])
                        line.drift_line_y.append(drift_point[1])
                        line.drift_lu.append(lu)
                        line.drift_hd.append(hd_ft)
                        line.drift_pd.append(pd_psf)
                        drift_string = 'lu = {0:.2f} ft\nhd = {1:.2f} ft\nw = {2:.2f} ft\npd = {3:.2f} psf'.format(lu,hd_ft,w_ft,pd_psf)
                        line.drift_plot_labels.append(drift_string)
                        
                    else:
                        pass
colors = ['r','b','g','c','m','y','k']
i=0                 
for line in lines:
    plt.plot([line.startx,line.endx], [line.starty,line.endy], color=colors[i])
    plt.plot(line.drift_line_x, line.drift_line_y, color=colors[i], marker = 'o')
    plt.plot(line.internal_points_x, line.internal_points_y, color=colors[i], marker = 'x')
    i+=1
    '''
    for label, x, y in zip(line.drift_plot_labels, line.drift_line_x, line.drift_line_y):
        plt.annotate(
            label,
            xy=(x, y), xytext=(-5, 5),
            fontsize = 6,
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3))
    '''
plt.show()
    

    
    




         
            
        
