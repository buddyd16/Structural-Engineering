# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 21:52:07 2021

@author: buddyd16
"""
import math
import matplotlib.pyplot as plt

def segments_from_xy(x,y):
    '''
    

    Parameters
    ----------
    x : list, float
        List of x-coordinates.
    y : list, float
        list of y-coordinates.

    Returns
    -------
    segements : list of list pairs.
    
    ordered coordinate pairs creating segments joined by the input coordinates

    '''
    
    # enumerate(x[1:]) produces an index result of 0...len(x)-1
    # this lets us do a +1 on the index for the last value to get the final
    # x or y coordinate.
    
    segments = [[[x[i[0]],y[j[0]]],[x[i[0]+1],y[j[0]+1]]] 
                 for i,j in zip(enumerate(x[1:]),enumerate(y[1:]))]
    
    return segments

def segment_length(segment):
    '''
    Parameters
    ----------
    segment : list of two tuples
        List of two tuples or list containing the start and end x,y
        coordinates of the line segment.
        [[x1,y1],[x2,y2]]

    Returns
    -------
    length = linear length of the line segment.
    
    assumptions
    -----------
    coordinates are entered in consistent units
    '''

    x1 = segment[0][0]
    y1 = segment[0][1]
    x2 = segment[1][0]
    y2 = segment[1][1]
    
    # standard linear distance between two point formula
    return math.sqrt(((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1)))

def segment_center(segment):
    
    x1 = segment[0][0]
    y1 = segment[0][1]
    x2 = segment[1][0]
    y2 = segment[1][1]
    
    x_center = (x1+x2)/2.0
    y_center = (y1+y2)/2.0
    
    return [x_center, y_center]

def rotate_segments(segments,alpha_radians,center_pt=[0,0]):
    
    rotated_segments = []
    
    xo = center_pt[0]
    yo = center_pt[1]
    
    for segment in segments:
        
        x1 = segment[0][0]
        y1 = segment[0][1]
        x2 = segment[1][0]
        y2 = segment[1][1]
        
        c = math.cos(alpha_radians)
        s = math.sin(alpha_radians)
        
        x1r = (((x1-xo)*c)
                +((y1-yo)*s))
        y1r = ((-1*(x1-xo)*s)
               +((y1-yo)*c))
        x2r = (((x2-xo)*c)
               +((y2-yo)*s))
        y2r = ((-1*(x2-xo)*s)
               +((y2-yo)*c))
        
        rotated_segments.append([[x1r,y1r],[x2r,y2r]])
    
    return rotated_segments

def Bo(segments):
    '''
    Parameters
    ----------
    segments : list of two tuples
        List of two tuples or list containing the start and end x,y
        coordinates of the line segment.
        [[x1,y1],[x2,y2]]

    Returns
    -------
    sum_L = total length of the segments = perimeter.

    '''
    sum_L = sum([segment_length(i) for i in segments])
    
    return sum_L
    
def A_c(segments,d):
    '''
    Parameters
    ----------
    segments : list of two tuples
        List of two tuples or list containing the start and end x,y
        coordinates of the line segment.
        [[x1,y1],[x2,y2]]
    d : list of floats
        Effective depth of each punch perimeter segment as defined by ACI 318.

    Returns
    -------
    Ac = total vertical surface area of the punch perimeter.

    '''
    
    # sum of the segment lengths
    Ac = 0
    
    for i,segment in enumerate(segments):
        Ac += d[i]*segment_length(segment)
        
    return Ac

def perimeter_centroid(segments,d):
    '''
    Parameters
    ----------
    segments : list of two tuples
        List of two tuples or list containing the start and end x,y
        coordinates of the line segment.
        [[x1,y1],[x2,y2]]
    d : list of floats
        Effective depth of each punch perimeter segment as defined by ACI 318.

    Returns
    -------
    [x,y] - x and y coordinate of the perimeter centroid

    '''
    
    Ac = A_c(segments,d)

    My = 0 
    Mx = 0 
    
    for i,segment in enumerate(segments):
        My += segment_length(segment)*d[i]*segment_center(segment)[0]
        Mx += segment_length(segment)*d[i]*segment_center(segment)[1]
    
    x = My/Ac
    y = Mx/Ac
    
    return [x,y]

def J_cx(segments,d):
    '''
    Parameters
    ----------
    segments : list of two tuples
        List of two tuples or list containing the start and end x,y
        coordinates of the line segment.
        [[x1,y1],[x2,y2]]
    d : list of floats
        Effective depth of each punch perimeter segment as defined by ACI 318.

    Returns
    -------
    Jcx = property of the assumed crticical section of any shape,
            equal to d multiplied by second moment of perimeter about the
            x-axis.

    '''
    # Jcx
    # ACI 421.1R-20 - Equation B.8
    jcx = 0
    
    for i,segment in enumerate(segments):
        jcx += ((segment_length(segment)/3.0)
                *((segment[0][1]*segment[0][1])     #yi^2
                  + (segment[0][1]*segment[1][1])   #yi*yj
                  + (segment[1][1]*segment[1][1])   #yj^2
                  ))*d[i]
    
    
    return jcx

def J_cy(segments,d):
    '''
    Parameters
    ----------
    segments : list of two tuples
        List of two tuples or list containing the start and end x,y
        coordinates of the line segment.
        [[x1,y1],[x2,y2]]
    d : list of floats
        Effective depth of each punch perimeter segment as defined by ACI 318.

    Returns
    -------
    Jcy = property of the assumed crticical section of any shape,
            equal to d multiplied by second moment of perimeter about the
            y-axis.

    '''
    # Jcy
    # ACI 421.1R-20 - Equation B.9
    jcy = 0
    
    for i,segment in enumerate(segments):
        jcy += ((segment_length(segment)/3.0)
                *((segment[0][0]*segment[0][0])     #xi^2
                  + (segment[0][0]*segment[1][0])   #xi*xj
                  + (segment[1][0]*segment[1][0])   #xj^2
                  ))*d[i]
    
    return jcy    

def J_cxy(segments,d):
    '''
    Parameters
    ----------
    segments : list of two tuples
        List of two tuples or list containing the start and end x,y
        coordinates of the line segment.
        [[x1,y1],[x2,y2]]
    d : list of floats
        Effective depth of each punch perimeter segment as defined by ACI 318.

    Returns
    -------
    Jcxy = property of the assumed crticical section of any shape,
            equal to d multiplied by second moment of perimeter about the
            y-axis.

    '''
    # Jcxy
    # ACI 421.1R-20 - Equation B.11
    jcxy = 0
    
    for i,segment in enumerate(segments):
        jcxy += ((segment_length(segment)/6.0)
                *((2*segment[0][0]*segment[0][1])       #2*xi*yi
                  + (segment[0][0]*segment[1][1])       #xi*yj
                  + (segment[1][0]*segment[0][1])       #xj*yi
                  + (2*segment[1][0]*segment[1][1])     #2*xj*yj
                  ))*d[i]
    
    return jcxy

def Theta(jcx,jcy,jcxy):
    
    y = -2.0*jcxy
    x = jcx-jcy
    
    if x==0 or y==0:
        two_theta = 0
    else:
        two_theta = math.atan2(y,x)
    
    theta = two_theta/2.0
    
    return theta

class Punch_Perimeter:
    def __init__(self,segments,d_in):
        '''
        Parameters
        ----------
        segments : list of two tuples
            List of two tuples or list containing the start and end x,y
            coordinates of the line segment.
            [[x1,y1],[x2,y2]]
        d : list of floats
            Effective depth of each punch perimeter segment as defined by ACI 318.

        Returns
        -------
        None.

        '''
        
        self.d_in = d_in
        
        self.segments = segments
        
        self.bo = Bo(segments)
        self.ac = A_c(segments,d_in)
        self.center = perimeter_centroid(segments,d_in)
        # Translate segments to align centroid with 0,0
        # Jcx,Jcy,Jcxy should be centroidal punch axis properties
        self.translate_segments = rotate_segments(segments,0,self.center)
        self.jcx = J_cx(self.translate_segments,d_in)
        self.jcy = J_cy(self.translate_segments,d_in)
        self.jcxy = J_cxy(self.translate_segments,d_in)
        
        # Principal Punch Axis
        self.alpha = Theta(self.jcx,self.jcy,self.jcxy)
        self.rotated_segments = rotate_segments(segments,self.alpha,self.center)
        self.jcxp = J_cx(self.rotated_segments,d_in)
        self.jcyp = J_cy(self.rotated_segments,d_in)
        self.jcxyp = J_cxy(self.rotated_segments,d_in)
        
        # ACI 318-14 -- EQ 8.4.2.3.2
        # b1 = dimension of the critical section bo measured in the 
        #       direction of the span for which moments are determined.
        # b2 = dimension of the critical section bo measured in the
        #       direction perpendicular to b1
        
        x = [i[0][0] for i in segments]
        x.append(segments[-1][1][0])
        y = [j[0][1] for j in segments]
        y.append(segments[-1][1][1])

        # x is for Mx so span is in the y
        self.b1x = max(y)-min(y)
        self.b2x = max(x)-min(x)
        # y is for My so span is in the x
        self.b1y = max(x)-min(x)
        self.b2y = max(y)-min(y)
        self.gamma_fx =  1.0 / (1+((2/3.0)*math.sqrt(self.b1x/self.b2x)))
        self.gamma_vx = 1-self.gamma_fx
        
        self.gamma_fy =  1.0 / (1+((2/3.0)*math.sqrt(self.b1y/self.b2y)))
        self.gamma_vy = 1-self.gamma_fy
        

class Interior_Rectangular_Column:
    
    def __init__(self,B_in,H_in,d_in,t_slab_in):
        '''
        Parameters
        ----------
        B_in : float
            X plan dimension of column.assumed to be plan left-right.
        H_in : float
            Y plan dimension of columns.assumed to be plan up-down.
        d_in : float
            depth from extreme compression fiber to centroid of tension steel.

        Returns
        -------
        None.

        '''
        
        self.B_in = B_in
        self.H_in = H_in
        self.d_in = d_in
        self.t_slab_in = t_slab_in
        self.Drop = False
        self.punch_perimeters_calculated = False
        self.punch_properties_calculated = False
        
        # Initialize Warning and Error Lists
        self.warnings = []
        self.errors = []
        
        # Coordinates of Column assuming center of column is (0,0)
        self.x = [-1*B_in/2.0,B_in/2.0,B_in/2.0,-1*B_in/2.0,-1*B_in/2.0]
        self.y = [-1*H_in/2.0,-1*H_in/2.0,H_in/2.0,H_in/2.0,-1*H_in/2.0]
        
    def add_drop_panel(self, Drop_B_left_in=0,Drop_B_right_in=0
                ,Drop_H_top_in=0,Drop_H_bottom_in=0,Drop_t_in=0):
        '''
        Parameters
        ----------
        Drop_B_left_in : float, optional
            Drop panel X plan dimension to the left of the column centerline. 
            The default is 0.
        Drop_B_right_in : float, optional
            Drop panel X plan dimension to the right of the column centerline. 
            The default is 0.
        Drop_H_top_in : float, optional
            Drop panel Y plan dimension above the column centerline. 
            The default is 0.
        Drop_H_bottom_in : float, optional
            Drop panel Y plan dimension below the column centerline. 
            The default is 0.
        Drop_t_in : float, optional
            Drop panel thickness from soffit of slab, d at the punch perimeter
            created at the drop will be assumed to be d_in - Drop_t_in. 
            The default is 0.
        
        Returns
        -------
        None.
        '''
        
        self.Drop = True
        self.Drop_B_left_in = Drop_B_left_in 
        self.Drop_B_right_in = Drop_B_right_in
        self.Drop_H_top_in = Drop_H_top_in
        self.Drop_H_bottom_in = Drop_H_bottom_in
        self.Drop_t_in = Drop_t_in
        
        # Determine d for the Drop panel
        self.d_drop_in = self.d_in - self.Drop_t_in
        
        # Coordinates of the Drop panel assuming center of the column is (0,0)
        self.drop_x = [-1*Drop_B_left_in,Drop_B_right_in
                       ,Drop_B_right_in,-1*Drop_B_left_in,-1*Drop_B_left_in]
        
        self.drop_y = [-1*Drop_H_bottom_in,-1*Drop_H_bottom_in
                       ,Drop_H_top_in,Drop_H_top_in,-1*Drop_H_bottom_in]
    
    def determine_punching_perimeters(self):
        
        offset_column = self.d_in/2.0
        self.punch_perimeters = []
        self.punch_col_x = []
        self.punch_col_y = []
        self.punch_segments = []
        self.d_segments = []
        
        if self.Drop:
            # self.drop is a boolean value 
            offset_drop = self.d_drop_in/2.0
            
            self.punch_drop_x = []
            self.punch_drop_y = []
            self.punch_drop_segments = []
            
            # Column Punch Perimeter
            for i,x in enumerate(self.x):
                if x<0:
                    self.punch_col_x.append(x-offset_column)
                else:
                    self.punch_col_x.append(x+offset_column)
            
            for j,y in enumerate(self.y):
                if y<0:
                    self.punch_col_y.append(y-offset_column)
                else:
                    self.punch_col_y.append(y+offset_column)
            
            punch_col_segments = segments_from_xy(self.punch_col_x, self.punch_col_y)
            
            self.punch_segments.append(punch_col_segments)
            
            self.d_segments.append([self.d_in]*(len(self.x)-1))
            
            # Drop panel punch perimeter
            for x in self.drop_x:
                if x<0:
                    self.punch_drop_x.append(x-offset_drop)
                else:
                    self.punch_drop_x.append(x+offset_drop)
            
            for y in self.drop_y:
                if y<0:
                    self.punch_drop_y.append(y-offset_drop)
                else:
                    self.punch_drop_y.append(y+offset_drop)
            
            punch_drop_segments = segments_from_xy(self.punch_drop_x, self.punch_drop_y)
            
            self.punch_segments.append(punch_drop_segments)
            
            self.d_segments.append([self.d_drop_in]*(len(self.drop_x)-1))
            
            self.punch_perimeters_calculated = True
            
        else:
            for x in self.x:
                if x<0:
                    self.punch_col_x.append(x-offset_column)
                else:
                    self.punch_col_x.append(x+offset_column)
            
            for y in self.y:
                if y<0:
                    self.punch_col_y.append(y-offset_column)
                else:
                    self.punch_col_y.append(y+offset_column)
            
            self.punch_segments.append(segments_from_xy(self.punch_col_x, self.punch_col_y))
            
            self.d_segments.append([self.d_in]*(len(self.x)-1))
            
            self.punch_perimeters_calculated = True

    def determine_punching_properties(self):
        
        self.punch_properties = []

        if self.Drop:
            
            d = self.d_segments
            
            for i,segments in enumerate(self.punch_segments):
                
                self.punch_properties.append(Punch_Perimeter(segments,d[i]))
                
                self.punch_properties_calculated = True
        else:
            d = self.d_segments[0]
            segments = self.punch_segments[0]
            
            self.punch_properties.append(Punch_Perimeter(segments,d))
            
            self.punch_properties_calculated = True
    
    def process_load(self,Vu_kips,Mscx_ftkips,Mscy_ftkips):
        '''
        Parameters
        ----------
        Vu_kips : float
            Factored Vertical shear, + = up.
        Mscx_ftkips : float
            Factored slab moment that is resisted by the column at a joint
            about the column centroid x-axis.
            + = right hand rule thumb pointing left
        Mscy_ftkips : float
            Factored slab moment that is resisted by the column at a joint
            about the column centroid y-axis.
            + = right hand rule thumb pointing down

        Returns
        -------
        vc_ksi = [[]].
            a list of lists of shear stress values at the vertices of
            each punch perimeter

        '''
        
        self.vc_ksi_out = []
        
        for perimeter in self.punch_properties:
            
            # Determine additional moment from shear 
            # eccentricity to punch centroid
            if perimeter.center == [0.0,0.0]:
                mxv_inkips = 0
                myv_inkips = 0
                
            else:
                # Vu up produces proper signed Mx moment at the signed distance
                # to the punch centroid
                mxv_inkips = Vu_kips*perimeter.center[1]
                
                # Vu up requires the opposite signed x distance 
                # to the punch centroid for My
                myv_inkips = Vu_kips*-1*perimeter.center[0]
            
            mx_inkips = (mxv_inkips + (12*Mscx_ftkips))*perimeter.gamma_vx
            my_inkips = (myv_inkips + (12*Mscy_ftkips))*perimeter.gamma_vy
            
            # Determine direct shear stress, vug
            # vug = Vu/Ac
            vug_ksi = Vu_kips/perimeter.ac
            
            # Align moments to punch principal axis
            alpha = perimeter.alpha
            s = math.sin(alpha)
            c = math.cos(alpha)
            mxp_inkips = mx_inkips*c+my_inkips*s
            myp_inkips = -1*mx_inkips*s+my_inkips*c
            
            jcxp = perimeter.jcxp
            jcyp = perimeter.jcyp
            
            # determine jcxp/y for each vertice, anlagous to s = I/y
            y = [j[0][1] for j in perimeter.segments]
            y.append(perimeter.segments[-1][1][1])
            
            jcxp_y = [jcxp/j for j in y]  
            
            # determine jcyp/x for each vertice, anlagous to s = I/x
            x = [j[0][0] for j in perimeter.segments]
            x.append(perimeter.segments[-1][1][0])
            jcyp_x = [jcyp/j for j in x]
            
            # determine vertice stresses
            vc_ksi = [vug_ksi-(mxp_inkips/i)+(myp_inkips/j) for i,j in zip(jcxp_y,jcyp_x)]
            
            self.vc_ksi_out.append(vc_ksi)
            
        return self.vc_ksi_out

class Edge_Rectangular_Column:
    
    def __init__(self,B_in,H_in,d_in,t_slab_in,edge_distance_in):
        '''
        Parameters
        ----------
        B_in : float
            X plan dimension of column.assumed to be plan left-right.
        H_in : float
            Y plan dimension of columns.assumed to be plan up-down.
        d_in : float
            depth from extreme compression fiber to centroid of tension steel.
        t_slab_in : float
            thickness of the slab.
        edge_distance_in: float
            distance from the column centerline to the free edge.

        Returns
        -------
        None.

        '''
        
        self.B_in = B_in
        self.H_in = H_in
        self.d_in = d_in
        self.t_slab_in = t_slab_in
        self.edge_distance_in = edge_distance_in
        self.Drop = False
        self.punch_perimeters_calculated = False
        self.punch_properties_calculated = False
        
        # Initialize Warning and Error Lists
        self.warnings = []
        self.errors = []
        
        # Coordinates of Column assuming center of column is (0,0)
        self.x = [-1*B_in/2.0,B_in/2.0,B_in/2.0,-1*B_in/2.0,-1*B_in/2.0]
        self.y = [-1*H_in/2.0,-1*H_in/2.0,H_in/2.0,H_in/2.0,-1*H_in/2.0]

class Corner_Rectangular_Column:
    
    def __init__(self,B_in,H_in,d_in,t_slab_in,edge_x_in,edge_y_in):
        
        self.B_in = B_in
        self.H_in = H_in
        self.d_in = d_in
        self.t_slab_in = t_slab_in
        self.edge_x_in = edge_x_in
        self.edge_y_in = edge_y_in
        self.Drop = False
        self.punch_perimeters_calculated = False
        self.punch_properties_calculated = False
        
        # Initialize Warning and Error Lists
        self.warnings = []
        self.errors = []
        
        # Coordinates of Column assuming center of column is (0,0)
        self.x = [-1*B_in/2.0,B_in/2.0,B_in/2.0,-1*B_in/2.0,-1*B_in/2.0]
        self.y = [-1*H_in/2.0,-1*H_in/2.0,H_in/2.0,H_in/2.0,-1*H_in/2.0]
        
    def determine_punching_perimeters(self):
        
        offset_column = self.d_in/2.0
        self.punch_perimeters = []
        self.punch_col_x = []
        self.punch_col_y = []
        self.punch_segments = []
        self.d_segments = []
    
        for x in self.x:
            if x<0:
                base_offset = x-offset_column
                if base_offset <= self.edge_x_in and self.edge_x_in < 0:
                    self.punch_col_x.append(self.edge_x_in)
                else:
                    self.punch_col_x.append(base_offset)
            else:
                base_offset = x+offset_column
                if base_offset >= self.edge_x_in and self.edge_x_in > 0:
                    self.punch_col_x.append(self.edge_x_in)
                else:
                    self.punch_col_x.append(base_offset)
        
        for y in self.y:
            if y<0:
                base_offset = y-offset_column
                if base_offset <= self.edge_y_in and self.edge_y_in < 0:
                    self.punch_col_y.append(self.edge_y_in)
                else:
                    self.punch_col_y.append(base_offset)
            else:
                base_offset = y+offset_column
                if base_offset >= self.edge_y_in and self.edge_y_in > 0:
                    self.punch_col_y.append(self.edge_y_in)
                else:
                    self.punch_col_y.append(base_offset)
        
        punch_segments_raw=segments_from_xy(self.punch_col_x, self.punch_col_y)
        for segment in punch_segments_raw:
            if segment[0][0] == self.edge_x_in and segment[1][0] == self.edge_x_in:
                pass
            elif segment[0][1] == self.edge_y_in and segment[1][1] == self.edge_y_in:
                pass
            else:
                self.punch_segments.append(segment)
        
        self.d_segments.append([self.d_in]*(len(self.punch_segments)))
        
        self.punch_perimeters_calculated = True

    def determine_punching_properties(self):
        
        self.punch_properties = []

        d = self.d_segments[0]
        segments = self.punch_segments
        
        self.punch_properties.append(Punch_Perimeter(segments,d))
        
        self.punch_properties_calculated = True
    
    def process_load(self,Vu_kips,Mscx_ftkips,Mscy_ftkips, area_load_in_perimeter=0):
        '''
        Parameters
        ----------
        Vu_kips : float
            Factored Vertical shear, + = up.
        Mscx_ftkips : float
            Factored slab moment that is resisted by the column at a joint
            about the column centroid x-axis.
            + = right hand rule thumb pointing left
        Mscy_ftkips : float
            Factored slab moment that is resisted by the column at a joint
            about the column centroid y-axis.
            + = right hand rule thumb pointing down

        Returns
        -------
        vc_ksi = [[]].
            a list of lists of shear stress values at the vertices of
            each punch perimeter

        '''
        
        self.vc_ksi_out = []
        
        for perimeter in self.punch_properties:
            
            # Determine additional moment from shear 
            # eccentricity to punch centroid
            if perimeter.center == [0.0,0.0]:
                mxv_inkips = 0
                myv_inkips = 0
                
            else:
                # Vu up produces proper signed Mx moment at the signed distance
                # to the punch centroid
                mxv_inkips = Vu_kips*perimeter.center[1]
                
                # Vu up requires the opposite signed x distance 
                # to the punch centroid for My
                myv_inkips = Vu_kips*-1*perimeter.center[0]
            
            mx_inkips = (mxv_inkips + (12*Mscx_ftkips))*perimeter.gamma_vx
            my_inkips = (myv_inkips + (12*Mscy_ftkips))*perimeter.gamma_vy
            
            # Determine direct shear stress, vug
            # vug = Vu/Ac
            vug_ksi = Vu_kips/perimeter.ac
            
            # Align moments to punch principal axis
            alpha = perimeter.alpha
            s = math.sin(alpha)
            c = math.cos(alpha)
            mxp_inkips = mx_inkips*c+my_inkips*s
            myp_inkips = -1*mx_inkips*s+my_inkips*c
            
            jcxp = perimeter.jcxp
            jcyp = perimeter.jcyp
            
            # determine jcxp/y for each vertice, anlagous to s = I/y
            y = [j[0][1] for j in perimeter.segments]
            y.append(perimeter.segments[-1][1][1])
            
            jcxp_y = [jcxp/j for j in y]  
            
            # determine jcyp/x for each vertice, anlagous to s = I/x
            x = [j[0][0] for j in perimeter.segments]
            x.append(perimeter.segments[-1][1][0])
            jcyp_x = [jcyp/j for j in x]
            
            # determine vertice stresses
            vc_ksi = [vug_ksi-(mxp_inkips/i)+(myp_inkips/j) for i,j in zip(jcxp_y,jcyp_x)]
            
            self.vc_ksi_out.append(vc_ksi)
            
        return self.vc_ksi_out
    
## TESTING ##
InteriorCalc = Corner_Rectangular_Column(24, 18, 12.875, 14, 12, -9)

InteriorCalc.determine_punching_perimeters()
InteriorCalc.determine_punching_properties()

test = InteriorCalc.punch_segments
props = InteriorCalc.punch_properties

vc = InteriorCalc.process_load(24.71,125.6,26.66)

plt.plot(InteriorCalc.x,InteriorCalc.y,'k')
for segment in InteriorCalc.punch_segments:
    x1 = segment[0][0]
    y1 = segment[0][1]
    x2 = segment[1][0]
    y2 = segment[1][1]
    plt.plot([x1,x2],[y1,y2],'k--')
plt.show()
