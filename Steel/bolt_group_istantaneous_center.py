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
import math as m

def build_bolt_group(numCols, numRows, Colspacing, Rowspacing):
    # Given a number of rows and columns
    # return the x and y coordinate lists
    # starting with the first bolt at (0,0)
    
    xloc = [0]
    yloc = [0]
    
    i=0
    y=0
    for i in range(numCols):
        if i == 0:
            y=0
            for y in range(numRows-1):
                xloc.append(xloc[-1])
                yloc.append(yloc[-1]+Rowspacing)
        else:
            x = xloc[-1] + Colspacing
            xloc.append(x)
            yloc.append(0)
            y=0
            for y in range(numRows-1):
                xloc.append(x)
                yloc.append(yloc[-1]+Rowspacing)
    return xloc, yloc
    
def bolt_group_center(xloc, yloc):
    #Bolt Group Centroid
    if len(xloc)<3:
        anchor_x_bar = (xloc[0]+xloc[1])/2.00
        anchor_y_bar = (yloc[0]+yloc[1])/2.00
    
    else:
        j=0
        x_tot=0
        y_tot=0
        
        for i in xloc:
            x_tot = x_tot+xloc[j]
            y_tot = y_tot+yloc[j]    
            j+=1
        
        anchor_x_bar = x_tot/len(xloc)
        anchor_y_bar = y_tot/len(yloc)
     
    cg_anchors = [anchor_x_bar, anchor_y_bar]
    
    return cg_anchors
    
def ic_brandt(IC, xloc, yloc, Mp):
    num_bolts = len(xloc)
    
    deltamax = 0.34
 
    ICx = IC[0]
    ICy = IC[1]
    xIC = []
    yIC = []
    di = []
    deltai = []
    ri = []
    
    fx = []
    fy = []
    moment = []
    
    for x in xloc:
        xICtemp = x - ICx
        xIC.append(xICtemp)
        
    for y in yloc:
        yICtemp = y - ICy
        yIC.append(yICtemp)
    
    i=0
    for i in range(num_bolts):
        ditemp = m.sqrt((xIC[i]*xIC[i])+(yIC[i]*yIC[i]))
        if ditemp == 0:
            ditemp = 0.00000001
        else:
            pass
        di.append(ditemp)
    
    dmax = max(di)
    
    i=0
    for i in range(num_bolts):
        deltaitemp = (di[i]/dmax)*deltamax
        deltai.append(deltaitemp)
        
    i=0
    for i in range(num_bolts):
        ritemp = m.pow(1-m.pow(m.e,-10.0*deltai[i]),0.55)
        ri.append(ritemp)
        
    i=0
    for i in range(num_bolts):    
        momenttemp = ri[i]*di[i]
        moment.append(momenttemp)
    
    Mi = sum(moment)
    Rult = -1*Mp/Mi

    i=0
    for i in range(num_bolts):    
        fxtemp = -1*(yIC[i]*ri[i])/di[i]
        fxtemp = fxtemp * Rult
        fx.append(fxtemp)
        
    i=0

    for i in range(num_bolts):     
        fytemp = (xIC[i]*ri[i])/di[i]
        fytemp = fytemp * Rult
        fy.append(fytemp)
    
    Rx = sum(fx) 
    Ry = sum(fy)
    
    
    table = [["Bolt x to IC",xIC],["Bolt y to IC", yIC],["di", di],["deltai", deltai],["ri", ri],["Mi", moment],["Fxi", fx],["Fyi", fy]]
    
    return Rx, Ry, Mi, table
    
def brandt(xloc, yloc, P_xloc, P_yloc, P_angle, tol=0.000001):
    # Bolt Group Instantaneous Center using method by G. Donald Brandt
    # Rapid Determiniation of Ultimate Strength Of Eccentrically Loaded Bolt Groups
    # AISC Journal 1982 2nd Quarter
    
    detailed_output = []
    
    num_bolts = len(xloc)
    
    n = num_bolts
    
    detailed_output.append(num_bolts)
    
    #Bolt Group Centroid
    if len(xloc)<3:
        anchor_x_bar = (xloc[0]+xloc[1])/2.00
        anchor_y_bar = (yloc[0]+yloc[1])/2.00
    
    else:
        j=0
        x_tot=0
        y_tot=0
        
        for i in xloc:
            x_tot = x_tot+xloc[j]
            y_tot = y_tot+yloc[j]    
            j+=1
        
        anchor_x_bar = x_tot/len(xloc)
        anchor_y_bar = y_tot/len(yloc)
     
    cg_anchors = [anchor_x_bar, anchor_y_bar]
    detailed_output.append(["Anchor Group C.G.",cg_anchors])
    
    # J - Polar Moment of Inertial of Bolt Group
    # sum(x^2+y^2)
    sum_x_square = 0
    sum_y_square = 0
    
    i=0
    for i in range(num_bolts):
        sum_x_square = sum_x_square + (xloc[i]-anchor_x_bar)**2
        sum_y_square = sum_y_square + (yloc[i]-anchor_y_bar)**2
    
    J = sum_x_square + sum_y_square
    detailed_output.append(['Anchor Group J',J])
    
    Px = -1*m.cos(m.radians(P_angle))
    Py = -1*m.sin(m.radians(P_angle))
    
    detailed_output.append(["Unit Forces",Px,Py])
    
    Mo = (-1*Px*(P_yloc-anchor_y_bar))+(Py*(P_xloc-anchor_x_bar))
    
    detailed_output.append(["Mo",Mo])
    
    ax = (-1*Py*J) / (n * Mo)
    ay = (Px*J) / (n*Mo)
    
    detailed_output.append(["ax",ax,"ay",ay])
    
    Mp = (-1*Px*(P_yloc-anchor_y_bar-ay))+(Py*(P_xloc-anchor_x_bar-ax))
    
    detailed_output.append(["Mp",Mp])
    
    IC_initial = [anchor_x_bar+ax,anchor_y_bar+ay]
    
    Rx, Ry, Mi, table = ic_brandt(IC_initial,xloc,yloc, Mp)
    
    detailed_output.append(["Rx",Rx,"Ry", Ry,"Mi", Mi,"Per Bolt Table", table,"First IC pass"])
    
    fxx = Px + Rx
    fyy = Py + Ry
    F = m.sqrt(fxx*fxx+fyy*fyy)
    
    detailed_output.append(["fxx",fxx,"fyy",fyy,"F",F])
    
    ax_new = (-1*fyy*J)/(n*Mo)
    ay_new = (fxx*J) / (n*Mo)
    
    detailed_output.append(["ax",ax_new,"ay",ay_new])
    
    IC_new = IC_initial
    
    Cu = abs(Mi/Mp)
    
    count = 0
    iterations = 0
    f_track = [F]
    cu_track = [Cu]
    while count<5000:

        IC_new = [IC_new[0]+ax_new,IC_new[1]+ay_new]
        Mp_new = (-1*Px*(P_yloc-IC_new[1]))+(Py*(P_xloc-IC_new[0]))
        
        Rx, Ry, Mi, table = ic_brandt(IC_new,xloc,yloc, Mp_new)
        
        fxx = Px + Rx
        fyy = Py + Ry
        F = m.sqrt(fxx*fxx+fyy*fyy)
        
        f_track.append(F)
        
        Cu = abs(Mi/Mp_new)
        
        cu_track.append(Cu)
        
        ax_new = ((-1*fyy*J)/(n*Mo))/10.0
        ay_new = ((fxx*J) / (n*Mo))/10.0
             
        if F <= tol:
            iterations = count
            count = 5000          
            solution = 'yes'
        else:   
            iterations = count
            count +=1
            solution = 'no'
    
    detailed_output.append(["fxx",fxx,"fyy",fyy,"F",F])        
    detailed_output.append(["I.C.",IC_new])
    detailed_output.append(["Solution:",solution,"# Iterations:",iterations,count])
    
    detailed_output.append(["Rx",Rx,"Ry", Ry,"Mi", Mi,"Per Bolt Table", table])  
    
    Cu = abs(Mi/Mp_new)
    
    F_old = f_track[-2]
    F = f_track[-1]
    Cu_old = cu_track[-2]
    try:
        Cu_predict = ((F_old*F_old*Cu) - (F*F*Cu_old)) / ((F_old*F_old) - (F*F))
    except:
        Cu_predict = 0
        
    detailed_output.append(["Mi",Mi,"Mp",Mp_new,"Cu",Cu])
    detailed_output.append(["Predicted Cu", Cu_predict])
    detailed_output.append([F_old,F,Cu_old,Cu])
    detailed_output.append([f_track,cu_track])
    detailed_output.append([ax_new,ay_new])
    
    
    return detailed_output, IC_new, Cu


# Brandt's Method Testing Zone
#x_b = [-1.5,-1.5,-1.5,-1.5,1.5,1.5,1.5,1.5]
#y_b = [-4.5,-1.5,1.5,4.5,4.5,1.5,-1.5,-4.5]
#P_xloc = 3
#P_yloc = 0
#P_angle = 15
#
#brandt = brandt(x_b, y_b, P_xloc, P_yloc, P_angle) 

#Cu = brandt[2]

#x,y = build_bolt_group(4,4,3,3)    
