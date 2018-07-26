# -*- coding: utf-8 -*-

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

def center_of_two_points(p1=[0,0],p2=[1,1]):
    x_center = (p1[0]+p2[0])/2.0
    y_center = (p1[1]+p2[1])/2.0
    
    return [x_center, y_center]
    
def length_between_two_points(p1=[0,0],p2=[1,1]):
    dx = abs(p2[0] - p1[0])
    dy = abs(p2[1] - p1[1])

    length = (dx**2 + dy**2)**0.5

    return length

def parrallel_axis_theorem(momentofinertia=1, area=1, distancetoparallelaxis=1):
    '''
    Parralel axis theorem: I' = Ilocal + A*d^2
    '''
    return momentofinertia + (area*distancetoparallelaxis*distancetoparallelaxis)

def centroid_by_areas(areas=[0],areacenters=[[0,0]],referencepoint=[0,0]):
    '''
    computes the centroid x,y distances from a reference point
    and returns the global x,y coordinates relative to (0,0)
    
    length of areas and areacenters must be equal
    '''
    if len(areas) != len(areacenters):
        return 'Number of Areas needs to match the number of Area Centers'
    else:
        sumA = sum(areas)
        sumAx = 0
        sumAy = 0
        for area, areacenter in zip(areas, areacenters):
            cix = areacenter[0] - referencepoint[0]
            ciy = areacenter[1] - referencepoint[1]
            
            sumAx = sumAx + (area*cix)
            sumAy = sumAy + (area*ciy)
        
        Cx = sumAx/sumA
        Cy = sumAy/sumA
        
        global_center_x = Cx + referencepoint[0]
        global_center_y = Cy + referencepoint[1]
        
        return [global_center_x, global_center_y]
    
    
class weld_segment:
    def __init__(self, startcoordinates=[0,0], endcoordinates=[1,1]):
    
        self.start = startcoordinates
        
        self.end = endcoordinates
        
        self.m = self.end[0] - self.start[0]
        self.n = self.end[1] - self.start[1]
        
        self.center = center_of_two_points(self.start, self.end)
        
        self.length = length_between_two_points(self.start, self.end)
        self.area = self.length
        
        self.Ixo = (self.length*self.n*self.n)/12.0
        
        self.Iyo = (self.length*self.m*self.m)/12.0
    
    def global_moments_of_inertia(self, referencepoint=[0,0]):
        
        Cx = self.center[0] - referencepoint[0]
        Cy = self.center[1] - referencepoint[1]
        
        self.Ix = parrallel_axis_theorem(self.Ixo, self.area, Cy)
        self.Iy = parrallel_axis_theorem(self.Iyo, self.area, Cx)
        
        return [self.Ix, self.Iy]

class elastic_weld_group:
    def __init__(self, weld_segments=[weld_segment([0,0],[0,1])]):
        
        self.log = '--Elastic Weld Group Analysis--\nSegment Areas and Centroids:\n'
        
        # build lists of areas and center of areas for each weld segment to
        # pass into the centroid_by_areas function
        
        areas = [weld.area for weld in weld_segments]
        areacenters = [weld.center for weld in weld_segments]
        

        for area, areacenter in zip(areas,areacenters):
            self.log = self.log + 'Segment Area:{0:.3f} Segment Centroid: ({1:.3f},{2:.3f})\n'.format(area,areacenter[0],areacenter[1])
        
        # Determine the centroid coordinates for the weld group
        self.group_center = centroid_by_areas(areas, areacenters)
        
        self.log = self.log + '\nWeld Group Properties\nWeld Group Centroid: ({0:.3f},{1:.3f})\n'.format(self.group_center[0],self.group_center[1])
        
        # Determine Ix and Iy about the weld groupd centroidal axis
        self.Ix = 0
        self.Iy = 0
        
        self.log = self.log + '\nPer Segment Moment of Inertias:\n'
        for weld in weld_segments:
            
            Ixsegment = weld.global_moments_of_inertia(self.group_center)[0]
            Iysegment = weld.global_moments_of_inertia(self.group_center)[1]
            self.Ix = self.Ix + Ixsegment
            self.Iy = self.Iy + Iysegment
            
            self.log = self.log + 'Ix,segment = {0:.3f}\nIy,segment = {1:.3f}\n'.format(Ixsegment, Iysegment)
        
        self.log = self.log + '\nWeld Group Moment of Inertias:\nIx = sum of segment Ix = {0:.3f}\nIy = sum of segment Iy = {1:.3f}\n'.format(self.Ix, self.Iy)
            
        max_x = max(max([weld.start[0] for weld in weld_segments]), max([weld.end[0] for weld in weld_segments]))
        min_x = min(min([weld.start[0] for weld in weld_segments]), min([weld.end[0] for weld in weld_segments]))
        
        self.Cx_right = abs(max_x - self.group_center[0])
        self.Cx_left = abs(min_x - self.group_center[0])
        
        self.log = self.log + '\nLeft most Distance to Centroid, Cx,left = {0:.3f}\nRight most Distance to Centroid, Cx,right = {1:.3f}\n'.format(self.Cx_left, self.Cx_right)
        
        max_y = max(max([weld.start[1] for weld in weld_segments]), max([weld.end[1] for weld in weld_segments]))
        min_y = min(min([weld.start[1] for weld in weld_segments]), min([weld.end[1] for weld in weld_segments]))
        
        self.Cy_top = abs(max_y - self.group_center[1])
        self.Cy_bottom = abs(min_y - self.group_center[1])
        
        self.log = self.log + 'Top most Distance to Centroid, Cy,top = {0:.3f}\nBottom most Distance to Centroid, Cy,bottom = {1:.3f}\n'.format(self.Cy_top, self.Cy_bottom)        
        
        self.Area = sum(areas)
        self.log = self.log + '\nGroup Properties:\nArea = sum of lengths = {0:.3f}\n'.format(self.Area)
        self.Ip = self.Ix + self.Iy
        self.log = self.log + 'Polar Moment of Inertia, Ip = Ix + Iy = {0:.3f}\n'.format(self.Ip)
        self.Sx_top = self.Ix/self.Cy_top
        self.log = self.log + '\nElastic Section Moduli:\nSx,top = Ix/Cy,top = {0:.3f}\n'.format(self.Sx_top)
        self.Sx_bottom = self.Ix/self.Cy_bottom
        self.log = self.log + 'Sx,bottom = Ix/Cy,bottom = {0:.3f}\n'.format(self.Sx_bottom)
        self.Sy_left = self.Iy/self.Cx_left
        self.log = self.log + 'Sy,left = Iy/Cy,left = {0:.3f}\n'.format(self.Sy_left)
        self.Sy_right = self.Iy/self.Cx_right
        self.log = self.log + 'Sy,right = Iy/Cy,right = {0:.3f}\n'.format(self.Sy_right)
                  
    
    def force_analysis(self, Fz, Fx, Fy, Mx, My, Mz):
        self.log = self.log + '\n\n---Elastic Force Analysis of Weld Group---\n**All Loads Assumed to be applied at the weld group centroid.**\n'
        self.log = self.log + 'Fz,Axial = {0:.3f}\nFx,Shear X = {1:.3f}\nFy,Shear Y = {2:.3f}\nMx,Moment about x-axis = {3:.3f}\nMy,Moment about y-axis = {4:.3f}\nMz,Torsion aboiut the z-axis = {5:.3f}\n'.format(Fz, Fx, Fy, Mx, My, Mz)
        #Component Forces
        fz = Fz/self.Area
        self.log = self.log + '\n--Component Forces--\nfz = Fz/Area = {0:.3f}\n'.format(fz)
        fx = Fx/self.Area
        self.log = self.log + 'fx = Fx/Area = {0:.3f}\n'.format(fx)
        fy = Fy/self.Area
        self.log = self.log + 'fy = Fy/Area = {0:.3f}\n'.format(fy)
        mx = max(Mx/self.Sx_top, Mx/self.Sx_bottom)
        self.log = self.log + 'mx = max[Mx/Sx,top and Mx/Sx,bottom] = {0:.3f}\n'.format(mx)
        my = max(My/self.Sy_left, My/self.Sy_right)
        self.log = self.log + 'my = max[My/Sy,left and My/Sy,right] = {0:.3f}\n'.format(my)
        mzy = max((Mz*self.Cx_left)/self.Ip, (Mz*self.Cx_right)/self.Ip)
        self.log = self.log + 'mzy = max[Mz*Cx,left/Ip and Mz*Cx,right/Ip] = {0:.3f}\n'.format(mzy)
        mzx = max((Mz*self.Cy_bottom)/self.Ip,(Mz*self.Cy_top)/self.Ip)
        self.log = self.log + 'mzx = max[Mz*Cy,top/Ip and Mz*Cy,bottom/Ip] = {0:.3f}\n'.format(mzx)
        
        self.component_forces = [fz,fx,fy,mx,my,mzy,mzx]
        self.component_forces_key = 'fz, fx, fy, mx, my, mzy, mzx'         
        
        #Resultant Force
        self.resultant = math.sqrt(((fz+mx+my)*(fz+mx+my)) + ((fx+mzx)*(fx+mzx)) + ((fy+mzy)*(fy+mzy)))
        self.log = self.log + '\nResulatant force per unit length = [(fz+mx+my)^2 + (fx+mzx)^2 + (fy+mzy)^2]^(1/2) = {0:.3f}'.format(self.resultant)
        return self.resultant
    
    def aisc_weld_check(self, resultant, Fexx, Fy_base, Fu_base, base_thickness, asd=0):
        
        self.log = self.log + '\n\n---Weld Design---\n'
        if asd==0:        
            rn_weld = resultant/0.75
            rn_base_yield = resultant
            rn_base_rupture = resultant/0.75
            self.log = self.log + 'Ru,Ultimate Resultant Shear: {0:.3f}\n'.format(resultant)
            self.log = self.log + 'Fexx = {0:.3f}\nFy,base = {1:.3f}\nFu,base = {2:.3f}\nt,base material thickness = {3:.3f}\n\n'.format(Fexx, Fy_base, Fu_base, base_thickness)
            self.log = self.log + 'Rn,weld/phi = Ru/0.75 = {0:.3f}\nRn,base yield/phi = Ru/1.0 = {1:.3f}\nRn,base rupture/phi = Ru/0.75 = {2:.3f}\n\n'.format(rn_weld,rn_base_yield,rn_base_rupture)
        else:
            rn_weld = resultant*2.0
            rn_base_yield = resultant*1.5
            rn_base_rupture = resultant*2.0
            self.log = self.log + 'Rn,Nominal Resultant Shear: {0:.3f}\n'.format(resultant)
            self.log = self.log + 'Fexx = {0:.3f}\nFy,base = {1:.3f}\nFu,base = {2:.3f}\nt,base material thickness = {3:.3f}\n\n'.format(Fexx, Fy_base, Fu_base, base_thickness)
            self.log = self.log + 'Rn,weld*omega = Ru*2.0 = {0:.3f}\nRn,base yield*omega = Ru*1.5 = {1:.3f}\nRn,base rupture*omega = Ru*2.0 = {2:.3f}\n\n'.format(rn_weld,rn_base_yield,rn_base_rupture)
            
        Aweld = rn_weld/(0.6*Fexx)
        self.log = self.log + 'Required Effective Throat = Rn,weld / 0.6*Fexx [AISC Table J2.5] = {0:.3f}\n\n'.format(Aweld)
        
        fillet_weld_16th = math.ceil(rn_weld / ((math.sqrt(2)/2.0)*(1/16.0)*0.6*Fexx))
        fillet_weld = fillet_weld_16th/16.0
        self.log = self.log + 'As a Fillet Weld: {0:.1f} / 16" per loading\n\n'.format(fillet_weld_16th)
        
        # Minimum Fillet Weld - AISC Table J2.4
        if base_thickness > 0.75:          
            min_fillet_weld_16th = 5
            min_fillet_weld = 5/16.0
        elif 0.5 < base_thickness <= 0.75:
            min_fillet_weld_16th = 4
            min_fillet_weld = 1/4.0
        elif 0.25 < base_thickness <= 0.5:
            min_fillet_weld_16th = 3
            min_fillet_weld = 3/16.0
        else:
            min_fillet_weld_16th = 2
            min_fillet_weld = 2/16.0  
        self.log = self.log + 'Minimum Fillet Weld per AISC Table J2.4: {0:.1f}/16" or {1:.3f}"\n'.format(min_fillet_weld_16th,min_fillet_weld)
        
        # Max Fillet Weld - AISC J2b        
        if base_thickness < 0.25:
            max_fillet_weld_16th = 16.0*base_thickness
            max_fillet_weld = base_thickness
        else:           
            max_fillet_weld = base_thickness - (1/16.0)
            max_fillet_weld_16th = 16.0*max_fillet_weld
        self.log = self.log + 'Maximum Fillet Weld per AISC J2b: {0:.1f}/16" or {1:.3f}"\n\n'.format(max_fillet_weld_16th,max_fillet_weld)
        
        if fillet_weld < max_fillet_weld and fillet_weld < min_fillet_weld:
            self.log = self.log + 'Required Fillet < AISC Min - Use {0:.1f}/16" or {1:.3f}"\n\n'.format(min_fillet_weld_16th,min_fillet_weld)
        
        elif fillet_weld < max_fillet_weld and fillet_weld >= min_fillet_weld:
            self.log = self.log + 'Required Fillet > AISC Min - Use {0:.1f}/16" or {1:.3f}"\n\n'.format(fillet_weld_16th,fillet_weld)
        
        else:
            self.log = self.log + 'Required Fillet > AISC Maximum - **NG**\nIf Possible Increase Overall Weld Group Geometry\n\n'
            
        # Check if Base Material Ok
        Ag = base_thickness
        Anv = Ag
        self.log = self.log + '--Base Material Checks--\nAg = Anv = t,base*1.0 = {0:.3f}\n\n'.format(Ag)
        
        # AISC J4.2 - Shear Yielding and Shear Rupture
        shear_yield_base = 0.6*Fy_base*Ag # AISC eq J4-3
        self.log = self.log + 'AISC J4.2 - Shear Yielding of Base Material:\nRn = 0.60*Fy,base*Ag (J4-3) = {0:.3f}\n'.format(shear_yield_base)
        if shear_yield_base/rn_base_yield > 1.0:
            shear_yield_status = 'OK'
            self.log = self.log + 'Rn > Rn,base yield: OK\n\n'
        else:
            shear_yield_status = '**NG**'
            self.log = self.log + 'Rn < Rn,base yield: **NG**\n\n'
        
        shear_rupture_base = 0.6*Fu_base*Anv # AISC eq J4-4
        self.log = self.log + 'AISC J4.2 - Shear Rupture of Base Material:\nRn = 0.60*Fu,base*Anv (J4-4) = {0:.3f}\n'.format(shear_rupture_base)

        if shear_rupture_base/rn_base_rupture > 1.0:
            shear_rupture_status = 'OK'
            self.log = self.log + 'Rn > Rn,base rupture: OK\n'
        else:
            shear_rupture_status = '**NG**'
            self.log = self.log + 'Rn < Rn,base rupture: **NG**\n'
        
        
# Circle Helper
#segments = []
#r = 3
#for a in range(0,360):
#    x = r*math.sin(math.radians(a))
#    y = r*math.cos(math.radians(a))
#    x1 = r*math.sin(math.radians(a+1))
#    y1 = r*math.cos(math.radians(a+1))
#    
#    segments.append(weld_segment([x,y],[x1,y1]))

segments = [weld_segment([0,0],[0,6]),weld_segment([2,0],[2,6])]

weld_group = elastic_weld_group(segments)

#Loads:
Fz = 0
Fx = 5000
Fy = 5000
Mx = 50000
My = 0
Mz = 0

resultant = weld_group.force_analysis(Fz,Fx,Fy,Mx,My,Mz)

weld_group.aisc_weld_check(resultant,70000,36000,58000,0.5,1)

Ix = weld_group.Ix
Iy = weld_group.Iy
Ip = weld_group.Ip
center = weld_group.group_center

log = weld_group.log


    