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
import math
import numpy as np
import matplotlib.pyplot as plt

def length_by_two_points(ax,ay,bx,by):
    dx = abs(bx - ax)
    dy = abs(by - ay)

    length = (dx*dx + dy*dy)**0.5

    return length

def angle_by_two_points(ax,ay,bx,by):
        dx = bx-ax
        dy = by-ay

        if dx == 0 and dy > 0:
            angle = 90

        elif dx == 0  and dy <0:
            angle = 270

        else:
            angle = math.atan2(dy, dx)
            angle = angle * (180/math.pi)

            if angle < 0:
                angle = angle + 360

        return angle

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

def vector_direction(x1,y1,x2,y2):
    dx = x2-x1
    dy = y2-y1
    angle = math.atan2(dy,dx) % (2*math.pi)
    
    return angle
    
class Line:
    def __init__(self, start=[0,0], end=[1,1], hc_ft = 1.0, label='1', location='e'):
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

            self.location = location
            self.length_calc()
            self.angle_degrees_calc()
            self.hc_ft = hc_ft
            self.label = label

            self.drift_line_x = []
            self.drift_line_y = []
            self.drift_lu = []
            self.drift_hd = []
            self.drift_pd = []
            self.drift_w = []
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

        if self.location == 'i':
            self.perp_angle = self.perp_angle + 180
        else:
            pass

        self.angle = angle

        return angle

    def interior_points_calc(self,num_points):
        l = self.length
        step = l/(num_points+1)
        
        start = point_at_angle_distance(self.start,self.angle,0.125)
        end = point_at_angle_distance(self.end,self.angle,-0.125)
        points = [start]

        for i in range(1,num_points+1):
            t = (i*step)/self.length

            x = ((1-t)*self.startx) + (t*self.endx)
            y = ((1-t)*self.starty) + (t*self.endy)

            point = [x,y]

            points.append(point)
        
        points.append(end)
        self.internal_points = points
        self.internal_points_x = [coordx[0] for coordx in points]
        self.internal_points_y = [coordy[1] for coordy in points]

        return points
    
    def drift_at_point(self, point_on_self, lines, snow_density_pcf, pg_psf, logging=1):
        dist=10
        perp_line_start = point_on_self
        angle = self.perp_angle
        
        calc_log = ''
        
        perp_lines = []
        intersect_points = []
        points_x = []
        points_y = []
        
        if logging == 1:
            calc_log = calc_log + indent + 'Internal Point ({0:.3f},{1:.3f}):\n'.format(point_on_self[0],point_on_self[1])
            calc_log = calc_log + 2*indent + 'Perpendicular Angle:{0:.4f} degrees\n'.format(angle)
        else:
            pass

        perp_line_end = point_at_angle_distance(perp_line_start, angle, dist)

        b0x = perp_line_start[0]
        b0y = perp_line_start[1]
        b1x = perp_line_end[0]
        b1y = perp_line_end[1]
        
        perp_line_vector = vector_direction(b0x,b0y,b1x,b1y)
        
        if logging == 1:
            calc_log = calc_log + 2*indent + 'Perpendicular Line:\n'+ 2*indent +'start:({0:.4f},{1:.4f})\n{4}end:({2:.4f},{3:.4f})\n'.format(b0x,b0y,b1x,b1y,2*indent)
        else:
            pass

        valid_point = 0
        lu_valid = []
        for check_line in lines:
            if check_line == self:
                pass
            else:
                if logging == 1:
                    calc_log = calc_log + '\n' + 3*indent + 'Intersection with {0}:\n'.format(check_line.label)
                else:
                    pass
                a0x = check_line.startx
                a0y = check_line.starty
                a1x = check_line.endx
                a1y = check_line.endy

                intersect_point = line_line_intersection_points(a0x,a0y,a1x,a1y,b0x,b0y,b1x,b1y)

                if intersect_point == 'no int':
                    if logging == 1:
                        calc_log = calc_log + 3*indent + 'No Intersection\n'
                    else:
                        pass
                else:
                    point_x = intersect_point[0][0]
                    point_y = intersect_point[0][1]

                    #check point within start, end vertices of line being checked against
                    x_ok = min(a0x,a1x)-tolerance <= point_x <= max(a0x,a1x)+tolerance
                    y_ok = min(a0y,a1y)-tolerance <= point_y <= max(a0y,a1y)+tolerance

                    #check point vector same as perp line
                    point_vector = vector_direction(b0x,b0y,point_x,point_y)

                    if logging == 1:
                        calc_log = calc_log + 3*indent + 'x = {0}\n'.format(point_x)
                        calc_log = calc_log + 3*indent + 'range: {0} - {1}\n'.format(a0x,a1x)
                        calc_log = calc_log + 3*indent + 'check: {0}\n'.format(x_ok)
                        calc_log = calc_log + 3*indent + 'y = {0}\n'.format(point_y)
                        calc_log = calc_log + 3*indent + 'range: {0} - {1}\n'.format(a0y,a1y)
                        calc_log = calc_log + 3*indent + 'check: {0}\n'.format(y_ok)
                        calc_log = calc_log + 3*indent + 'Vector: {0} = Perp-Vector: {1}\n'.format(point_vector,perp_line_vector)
                    else:
                        pass

                    if x_ok == True and y_ok == True and (perp_line_vector-tolerance) <= point_vector <= (perp_line_vector+tolerance):
                        valid_point +=1

                        intersect_points.append(intersect_point)
                        points_x.append(point_x)
                        points_y.append(point_y)

                        dx = abs(point_x - b0x)
                        dy = abs(point_y - b0y)

                        lu = (dx**2 + dy**2)**0.5
                        lu_calc = lu
                        lu = max(lu,25)

                        lu_valid.append(lu)

                        if logging == 1:
                            calc_log = calc_log + 3*indent + 'Valid Intersection\n'
                            calc_log = calc_log + 4*indent + 'Lu = {0:.3f}\n'.format(lu_calc)
                            calc_log = calc_log + 4*indent + 'Lu = {0:.3f} - min lu of 25\n'.format(lu)
                        else:
                            pass

                    else:
                        pass
        try:
            lu = min(lu_valid)
        except:
            lu = 0
            
        hd_ft = (0.43 * (lu**(1.0/3.0))*((pg_psf+10)**(1.0/4.0))) - 1.5
        hd_calc = hd_ft
        hd_ft = 0.75 * hd_ft

        if logging == 1:
            calc_log = calc_log + '\n' + 2*indent + 'Valid Intersections:{0}\n\n'.format(valid_point)
            calc_log = calc_log + 2*indent + '**Drift Calculation**\n'.format(lu)
            calc_log = calc_log + 2*indent + 'Lu = {0:.3f}\n'.format(lu)
            calc_log = calc_log + 2*indent + 'Lu = {0:.3f} - min lu of 25\n'.format(lu)
            calc_log = calc_log + 2*indent + 'hd = {0:.3f}\n'.format(hd_calc)
            calc_log = calc_log + 2*indent + '0.75*hd = {0:.3f}\n'.format(hd_ft)
            calc_log = calc_log + 2*indent + 'Edge Height = {0:.3f}\n'.format(self.hc_ft)
        else:
            pass

        if hd_ft <= self.hc_ft:
            w_ft = 4*hd_ft
            hd_ft = hd_ft
            if logging == 1:
                calc_log = calc_log + 2*indent + 'w = 4*hd = {0:.3f}\n'.format(w_ft)
                calc_log = calc_log + 2*indent + 'hd = hd = {0:.3f}\n'.format(hd_ft)
            else:
                pass
        else:
            w_ft = min((4*hd_ft**2)/self.hc_ft, 8*self.hc_ft)
            hd_ft = self.hc_ft
            if logging == 1:
                calc_log = calc_log + 2*indent + 'w = min of 4*hd^2 / hc and 8*hc  = {0:.3f}\n'.format(w_ft)
                calc_log = calc_log + 2*indent + 'hd = hc = {0:.3f}\n'.format(self.hc_ft)
            else:
                pass

        drift_point = point_at_angle_distance(perp_line_start, angle, w_ft)

        pd_psf = snow_density_pcf*hd_ft

        if logging == 1:
            calc_log = calc_log + 2*indent + 'Angle to Intersection: {0:.3f}\n'.format(angle)
            calc_log = calc_log + 2*indent + 'pd = {0:.3f}\n'.format(pd_psf)
            calc_log = calc_log + 2*indent + 'Interior Drift Coord = ({0:.3f},{1:.3f})\n\n'.format(drift_point[0],drift_point[1])
        else:
            pass

        drift_string = 'lu = {0:.2f} ft\nhd = {1:.2f} ft\nw = {2:.2f} ft\npd = {3:.2f} psf'.format(lu,hd_ft,w_ft,pd_psf)
        
        return calc_log, perp_lines, intersect_points, points_x, points_y, drift_string

def drift_all(lines, snow_density_pcf, pg_psf,number_of_points=10, logging=1, tolerance=0.0001):
    
    calc_log = ''
    
    perp_lines = []
    intersect_points = []
    points_x = []
    points_y = []
    
    dist = 3000
    
    for line in lines:
        if logging == 1:
            int_points = number_of_points
            calc_log = calc_log + 'Number of Interior Points: {0}:\n'.format(int_points)
        else:
            int_points = number_of_points
            
        line.interior_points_calc(int_points)
        line.reset_drift_lines()
    
        if logging == 1:
            calc_log = calc_log + '\n--Intersection points for {0}--:\n'.format(line.label)
        else:
            pass
    
        count = 0
        for interior_point in line.internal_points:
            perp_line_start = interior_point
            angle = line.perp_angle
    
            if logging == 1:
                calc_log = calc_log + indent + 'Internal Point {0}:\n'.format(count+1)
                calc_log = calc_log + 2*indent + 'Perpendicular Angle:{0:.4f} degrees\n'.format(angle)
            else:
                pass
    
            perp_line_end = point_at_angle_distance(perp_line_start, angle, dist)
    
            perp_lines.append([perp_line_start, perp_line_end])
    
            b0x = perp_line_start[0]
            b0y = perp_line_start[1]
            b1x = perp_line_end[0]
            b1y = perp_line_end[1]
            
            perp_line_vector = vector_direction(b0x,b0y,b1x,b1y)
    
            if logging == 1:
                calc_log = calc_log + 2*indent + 'Perpendicular Line:\n'+ 2*indent +'start:({0:.4f},{1:.4f})\n{4}end:({2:.4f},{3:.4f})\n'.format(b0x,b0y,b1x,b1y,2*indent)
            else:
                pass
    
            valid_point = 0
            lu_valid = []
            for check_line in lines:
                if check_line == line:
                    pass
                else:
                    if logging == 1:
                        calc_log = calc_log + '\n' + 3*indent + 'Intersection with {0}:\n'.format(check_line.label)
                    else:
                        pass
                    a0x = check_line.startx
                    a0y = check_line.starty
                    a1x = check_line.endx
                    a1y = check_line.endy
    
                    intersect_point = line_line_intersection_points(a0x,a0y,a1x,a1y,b0x,b0y,b1x,b1y)
    
                    if intersect_point == 'no int':
                        if logging == 1:
                            calc_log = calc_log + 3*indent + 'No Intersection\n'
                        else:
                            pass
                    else:
                        point_x = intersect_point[0][0]
                        point_y = intersect_point[0][1]
    
                        #check point within start, end vertices of line being checked against
                        x_ok = min(a0x,a1x)-tolerance <= point_x <= max(a0x,a1x)+tolerance
                        y_ok = min(a0y,a1y)-tolerance <= point_y <= max(a0y,a1y)+tolerance
    
                        #check point vector same as perp line
                        #point_vector = vector_direction(b0x,b0y,point_x,point_y)
                        
                        #check point within perp line start, end vertices
                        x_perp_ok = min(b0x,b1x)-tolerance <= point_x <= max(b0x,b1x)+tolerance
                        y_perp_ok = min(b0y,b1y)-tolerance <= point_y <= max(b0y,b1y)+tolerance
    
                        if logging == 1:
                            calc_log = calc_log + 3*indent + 'x = {0}\n'.format(point_x)
                            calc_log = calc_log + 3*indent + 'range: {0} - {1}\n'.format(a0x,a1x)
                            calc_log = calc_log + 3*indent + 'check: {0}\n'.format(x_ok)
                            calc_log = calc_log + 3*indent + 'y = {0}\n'.format(point_y)
                            calc_log = calc_log + 3*indent + 'range: {0} - {1}\n'.format(a0y,a1y)
                            calc_log = calc_log + 3*indent + 'check: {0}\n'.format(y_ok)
                            calc_log = calc_log + 3*indent + 'Vector: {0} = Perp-Vector: {1}\n'.format(point_vector,perp_line_vector)
                        else:
                            pass
    
                        if x_ok == True and y_ok == True and x_perp_ok == True and y_perp_ok == True:
                            valid_point +=1
    
                            intersect_points.append(intersect_point)
                            points_x.append(point_x)
                            points_y.append(point_y)
    
                            dx = abs(point_x - b0x)
                            dy = abs(point_y - b0y)
    
                            lu = (dx**2 + dy**2)**0.5
                            lu_calc = lu
                            lu = max(lu,25)
    
                            lu_valid.append(lu)
    
                            if logging == 1:
                                calc_log = calc_log + 3*indent + 'Valid Intersection\n'
                                calc_log = calc_log + 4*indent + 'Lu = {0:.3f}\n'.format(lu_calc)
                                calc_log = calc_log + 4*indent + 'Lu = {0:.3f} - min lu of 25\n'.format(lu)
                            else:
                                pass
    
                        else:
                            pass
            try:
                lu = min(lu_valid)
            except:
                lu = 0
                
            hd_ft = (0.43 * (lu**(1.0/3.0))*((pg_psf+10)**(1.0/4.0))) - 1.5
            hd_calc = hd_ft
            hd_ft = 0.75 * hd_ft
    
            if logging == 1:
                calc_log = calc_log + '\n' + 2*indent + 'Valid Intersections:{0}\n\n'.format(valid_point)
                calc_log = calc_log + 2*indent + '**Drift Calculation**\n'.format(lu)
                calc_log = calc_log + 2*indent + 'Lu = {0:.3f}\n'.format(lu)
                calc_log = calc_log + 2*indent + 'Lu = {0:.3f} - min lu of 25\n'.format(lu)
                calc_log = calc_log + 2*indent + 'hd = {0:.3f}\n'.format(hd_calc)
                calc_log = calc_log + 2*indent + '0.75*hd = {0:.3f}\n'.format(hd_ft)
                calc_log = calc_log + 2*indent + 'Edge Height = {0:.3f}\n'.format(line.hc_ft)
            else:
                pass
    
            if hd_ft <= line.hc_ft:
                w_ft = 4*hd_ft
                hd_ft = hd_ft
                if logging == 1:
                    calc_log = calc_log + 2*indent + 'w = 4*hd = {0:.3f}\n'.format(w_ft)
                    calc_log = calc_log + 2*indent + 'hd = hd = {0:.3f}\n'.format(hd_ft)
                else:
                    pass
            else:
                w_ft = min((4*hd_ft**2)/line.hc_ft, 8*line.hc_ft)
                hd_ft = line.hc_ft
                if logging == 1:
                    calc_log = calc_log + 2*indent + 'w = min of 4*hd^2 / hc and 8*hc  = {0:.3f}\n'.format(w_ft)
                    calc_log = calc_log + 2*indent + 'hd = hc = {0:.3f}\n'.format(line.hc_ft)
                else:
                    pass
    
            drift_point = point_at_angle_distance(perp_line_start, angle, w_ft)
    
            pd_psf = snow_density_pcf*hd_ft
    
            if logging == 1:
                calc_log = calc_log + 2*indent + 'Angle to Intersection: {0:.3f}\n'.format(angle)
                calc_log = calc_log + 2*indent + 'pd = {0:.3f}\n'.format(pd_psf)
                calc_log = calc_log + 2*indent + 'Interior Drift Coord = ({0:.3f},{1:.3f})\n\n'.format(drift_point[0],drift_point[1])
            else:
                pass
    
            line.drift_line_x.append(drift_point[0])
            line.drift_line_y.append(drift_point[1])
            line.drift_lu.append(lu)
            line.drift_hd.append(hd_ft)
            line.drift_pd.append(pd_psf)
            line.drift_w.append(w_ft)
            drift_string = 'lu = {0:.2f} ft, hd = {1:.2f} ft, w = {2:.2f} ft\npd = {3:.2f} psf'.format(lu,hd_ft,w_ft,pd_psf)
            line.drift_plot_labels.append(drift_string)
    
            count+=1
        
    return calc_log, perp_lines, intersect_points, points_x, points_y

def lines_transformation_to_origin(lines):
    x = []
    y = []

    for line in lines:
        x.append(line.startx)
        y.append(line.starty)
        x.append(line.endx)
        y.append(line.endy)

    shift_x = min(x)
    shift_y = min(y)

    max_x = max(x) - shift_x
    max_y = max(y) - shift_y

    return shift_x, shift_y, max_x, max_y

def line_closest_to_point_and_point_on_line(point, lines):
    point_x = point[0]
    point_y = point[1]

    distance_to_each_line = []
    point_on_each_line = []

    tolerance = 0.000001 

    for line in lines:
        a0x = line.startx
        a0y = line.starty
        a1x = line.endx
        a1y = line.endy
        #check point within start, end vertices of line being checked against
        x_ok = min(a0x,a1x)-tolerance <= point_x <= max(a0x,a1x)+tolerance
        y_ok = min(a0y,a1y)-tolerance <= point_y <= max(a0y,a1y)+tolerance

        #secondary point at unit distance at 180+line perp angle
        point_2 = point_at_angle_distance(point,line.perp_angle+180,1)
        int_point = line_line_intersection_points(a0x,a0y,a1x,a1y,point[0],point[1],point_2[0],point_2[1])
        
        if int_point == 'no int':
            distance_to_each_line.append(1000000)
            point_on_each_line.append([line.startx,line.starty])
        else:
            #check point within start, end vertices of line being checked against
            x1_ok = min(a0x,a1x)-tolerance <= int_point[0][0] <= max(a0x,a1x)+tolerance
            y1_ok = min(a0y,a1y)-tolerance <= int_point[0][1] <= max(a0y,a1y)+tolerance

            if x1_ok==False or y1_ok==False:
                distance_to_each_line.append(1000000)
                point_on_each_line.append([line.startx,line.starty])
            else:
                distance = length_by_two_points(point[0],point[1],int_point[0][0],int_point[0][1])
                distance_to_each_line.append(distance)
                point_on_each_line.append([int_point[0][0],int_point[0][1]])
    
    segment = distance_to_each_line.index(min(distance_to_each_line))
    segment_point = point_on_each_line[segment]
    segment += 1 
    
    return distance_to_each_line, point_on_each_line, segment, segment_point

def export_dxf(path, lines):
    file = open(path,'w')
    file.write('  0\nSECTION\n  2\nENTITIES\n')

    for line in lines:
        x0 = line.startx
        y0 = line.starty
        x1 = line.endx
        y1 = line.endy
        if line.location == 'e':
            layer = 'Exterior'
        else:
            layer = 'Interior'

        file.write('  0\nPOLYLINE\n  8\n{0}\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n'.format(layer))
        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer,x0,y0))
        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer,x1,y1))
        file.write('  0\nSEQEND\n')

        file.write('  0\nPOLYLINE\n 62\n4\n  8\nDrift\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')

        for i in range(0, len(line.drift_line_x)):
            x_drift = line.drift_line_x[i]
            y_drift = line.drift_line_y[i]
            file.write('  0\nVERTEX\n  8\nDrift\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format(x_drift,y_drift))
        file.write('  0\nSEQEND\n')

        k=0
        prev_label = ''
        for point in line.internal_points_x:
            label = '{0:.2f} psf - w = {1:.2f} ft'.format(line.drift_pd[k], line.drift_w[k])
            if k+1 > len(line.drift_w)-1 or k+1 > len(line.drift_pd)-1:
                next_label = ''
            else:
                next_label = '{0:.2f} psf - w = {1:.2f} ft'.format(line.drift_pd[k+1], line.drift_w[k+1])
            if label != prev_label or label != next_label:
                file.write('  0\nPOLYLINE\n  8\nDrift-Label\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
                x2 = line.internal_points_x[k]
                y2 = line.internal_points_y[k]
                x3 = line.drift_line_x[k]
                y3 = line.drift_line_y[k]
                file.write('  0\nVERTEX\n  8\nDrift-Label\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format(x2,y2))
                file.write('  0\nVERTEX\n  8\nDrift-Label\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format(x3,y3))
                file.write('  0\nSEQEND\n')

                real_label = 'pd = {0:.2f} psf, w = {1:.2f} ft'.format(line.drift_pd[k], line.drift_w[k])

                angle = angle_by_two_points(x2,y2,x3,y3)
                length = length_by_two_points(x2,y2,x3,y3)
                anno_pt = point_at_angle_distance([x2,y2],angle,0)

                if 90.99 < angle < 269.99:
                    angle = angle + 180
                else:
                    pass

                file.write('  0\nTEXT\n 62\n3\n  8\nDrift-Label\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n0.5\n  1\n{2}\n 72\n0\n 50\n{3:.4f}\n 11\n{0:.3f}\n 21\n{1:.3f}\n 31\n0.0\n 73\n1\n'.format(anno_pt[0],anno_pt[1],real_label,angle))
            else:
                pass
            k+=1
            prev_label = label

    file.write('  0\nENDSEC\n  0\nEOF')
    file.close()

'''       
##testing area
logging = 0
write_dxf = 0
create_plot = 0

tolerance = 0.000001

pg_psf = 25
snow_density_pcf = min((0.13*pg_psf) + 14, 30)
Ce = 1.0
Ct = 1.0
Cs = 1.0
I = 1.0
pf_psf = 0.7*Ce*Ct*I*pg_psf
ps_psf = Cs*pf_psf
hb_ft = ps_psf/snow_density_pcf

hc_ft = [3,3,3,3,3,3,3,3]

x = [1,51,51,51,51,26,26,26,26,11,11,11,11,1,1,1]
y = [1,1,1,51,51,51,51,26,26,26,26,61,61,61,61,1]

loc = ['e','e','e','e','e','e','e','e']

if logging == 1:
    calc_log = '---Calculation Log---\n\n--Create Lines--\n'
else:
    pass

indent = '    '
lines = []

hc=0
for i in range(0, int(len(x)/2)):
    if logging == 1:
        calc_log = calc_log + 'Line {0}:\n'.format(i+1)
    label = 'Line {0}'.format(i+1)
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
    lines.append(Line(start,end, hc_ft[hc],label,loc[hc]))
    if logging == 1:
        calc_log = calc_log + 'start:({0:.4f},{1:.4f})\nend:({2:.4f},{3:.4f})\n\n'.format(xs,ys,xe,ye)
    else:
        pass
    hc+=1

aab = ((1-0.5)*lines[0].startx) + (0.5*lines[0].endx)
baa = ((1-0.5)*lines[0].starty) + (0.5*lines[0].endy)

point_on_self = [aab,baa]
a_calc_log_line, a_perp_lines_line, a_intersect_points_line, a_points_x_line, a_points_y_line, a_drift_string_line = lines[0].drift_at_point(point_on_self, lines, snow_density_pcf, pg_psf, 1)

calc_log, perp_lines, intersect_points, points_x, points_y = drift_all(lines,snow_density_pcf,pg_psf,25,1)

s_x, s_y, mx, my = lines_transformation_to_origin(lines)
print s_x
print s_y
print mx
print my

test1, test2, segment, segment_point = line_closest_to_point_and_point_on_line([35.5,9.4],lines)
print test1
print test2
print segment
print segment_point

colors = ['r','b','g','c','m','y','k','r','b','g','c','m','y','k','r','b','g','c','m','y','k','r','b','g','c','m','y','k','r','b','g','c','m','y','k','r','b','g','c','m','y','k','r','b','g','c','m','y','k']
i=0

if create_plot == 1:
    for line in lines:
        plt.plot([line.startx,line.endx], [line.starty,line.endy], color=colors[i])
        plt.plot(line.drift_line_x, line.drift_line_y, color=colors[i], marker = '+')
        plt.plot(line.internal_points_x, line.internal_points_y, color=colors[i], marker = '+')
        #plt.plot(line.drift_line_x, line.drift_line_y, color=colors[i])
        #plt.plot(line.internal_points_x, line.internal_points_y, color=colors[i])
        k=0
        prev_label = ''
        for point in line.internal_points_x:
            label = '{0:.2f} psf\nw = {1:.2f} ft'.format(line.drift_pd[k], line.drift_w[k])
            if k+1 > len(line.drift_w)-1:
                next_label = ''
            else:
                next_label = '{0:.2f} psf\nw = {1:.2f} ft'.format(line.drift_pd[k+1], line.drift_w[k+1])
            if label != prev_label or label != next_label:
                angle = 45
                plt.annotate(label,xy=(line.internal_points_x[k], line.internal_points_y[k]), xycoords='data', rotation=angle, horizontalalignment='left', verticalalignment='bottom' )
                plt.plot([line.internal_points_x[k],line.drift_line_x[k]], [line.internal_points_y[k],line.drift_line_y[k]], color='k')
            else:
                pass
            k+=1
            prev_label = label
        i+=1

    plt.ylim(ymax=max(y)+5, ymin=min(y)-5)
    plt.xlim(xmax=max(x)+5, xmin=min(x)-5)

    plt.show()
else:
    pass

if logging == 1:
    file = open('Drift_by_lines_log.txt','w')
    file.write(calc_log)
    file.close()
else:
    pass

#DXF file
if write_dxf == 1:
    export_dxf('Drift_by_lines.dxf',lines)
else:
    pass
'''
