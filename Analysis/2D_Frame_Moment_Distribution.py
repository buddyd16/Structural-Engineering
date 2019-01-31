# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 14:32:29 2019

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
import pin_pin_beam_equations_classes as ppbeam

class node:
    def __init__(self, x):
        
        self.x = x
        self.K = 0

        
    def sum_node_k(self, beams, columns):
        self.K = 0
        
        for beam in beams:
            if beam.i or beam.j == self:
                self.K += beam.K
        
        for column in columns:
            if column.i or column.j == self:
                self.K += column.K
    
    def sum_node_moments(self, beams, columns):
        self.m_unbalance = 0
        self.m_balance = 0

        for beam in beams:
            if beam.i == self:
                self.m_unbalance += sum(beam.mi)
            elif beam.j == self:
                self.m_unbalance += sum(beam.mj)
            else:
                pass
            
        for column in columns:
            if column.i == self:
                self.m_unbalance += sum(column.mi)
            elif column.j == self:
                self.m_unbalance += sum(column.mj)
            else:
                pass
        
        self.m_balance = -1.0*self.m_unbalance
            
    
class Beam:    
    def __init__(self, i_node, j_node, E, I, Loads_List):
        
        '''
        beam element
        Loads = lists of loads in text form
        E, I, and Loads should have consistent units
        '''
        
        self.i = i_node
        self.j = j_node
        self.E = E
        self.I = I
        self.Load_List = [load for load in Loads_List]
        self.Length = j_node.x - i_node.x
        
        self.mi = [0]
        self.mj = [0]
        self.dfi = 0
        self.dfj = 0
        
        self.K = self.E*self.I / self.Length
        
        step = self.Length/25.0
        
        self.chart_stations = [0]
        
        for i in range(1,25):
            self.chart_stations.append(self.chart_stations[i-1]+step)
        
        self.chart_stations.append(self.Length)
        
    def applied_loads(self):
        
        self.Loads = []
        self.extra_station = []
        
        for load in self.Load_List:
            w1 = float(load[0])
            w2 = float(load[1])
            a = float(load[2])
            b = float(load[3])
            load_type = load[4]
            lc = self.Length
            
            #['Point','Moment','UDL','TRAP','END_DELTA']
            if load_type == 'Point':
                self.Loads.append(ppbeam.pl(w1,a,lc))
                b = min(lc,a + 0.0001)
                c = max(0,a - 0.0001)
                self.extra_station.extend([c,a,b])

            elif load_type == 'Moment':
                self.Loads.append(ppbeam.point_moment(w1,a,lc))
                b = min(lc,a + 0.0001)
                c = max(0,a - 0.0001)
                self.extra_station.extend([c,a,b])

            elif load_type == 'UDL':
                self.Loads.append(ppbeam.udl(w1,a,b,lc))
                self.extra_station.extend([a,b])
                
            elif load_type == 'TRAP':
                self.Loads.append(ppbeam.trap(w1,w2,a,b,lc))
                self.extra_station.extend([a,b])
            
            elif load_type == 'END_DELTA':
                self.Loads.append(ppbeam.end_delta(w1,w2,lc))
                
            else:
                pass
        
        self.chart_stations.extend(self.extra_station)
        
        self.chart_stations = list(set(self.chart_stations))
        
        self.chart_stations.sort()
    
    def fef(self):
        
        for load in self.Loads:
            
            if load.kind == "END_DELTA":
                self.mi[0] += load.fef()[1]*self.E*self.I
                self.mj[0] += load.fef()[3]*self.E*self.I          
            else:
                self.mi[0] += load.fef()[1]
                self.mj[0] += load.fef()[3]
    
    def reactions(self):
        
        self.Loads.append(ppbeam.point_moment(sum(self.mi),0,self.Length))
        self.Loads.append(ppbeam.point_moment(sum(self.mj),self.Length,self.Length))
        
        rl = 0
        rr = 0
        
        for load in self.Loads:
            rl += load.rl
            rr += load.rr
        
        return [rl,rr]
    
    def reset_fem(self):
        self.mi = [0]
        self.mj = [0]
        

class Column_Up:
    def __init__(self, i_node, height, E, I, support='fix'):
        '''
        upper column element
        I is about axis aligned with beams
        E, I, and Height should have consistent units
        '''
              
        self.i = i_node
        self.j = 0
        self.E = E
        self.I = I
        self.Length = height # Use Length to make loop plotting easier
        
        if support == 'fix':
            self.fix = 1
        else:
            self.fix = 0
        
        self.mi = [0]
        self.mj = [0]
        self.dfi = 0
        
        step = self.Length/25.0
        
        self.chart_stations = [0]
        
        for i in range(1,25):
            self.chart_stations.append(self.chart_stations[i-1]+step)
        
        self.chart_stations.append(self.Length)
        
        if self.fix == 1:           
            self.K = self.E*self.I / self.Length
            self.dfj = 0
            self.coi = 0
        else:
            self.K = (3/4.0)*(self.E*self.I / self.Length)
            self.dfj = 1
            self.coi = 0.5
            
    def reset_fem(self):
         self.mi = [0]
         self.mj = [0]       

class Column_Down:
    def __init__(self, j_node, height, E, I, support='fix'):
        '''
        lower column element
        I is about axis aligned with beams
        E, I, and Height should have consistent units
        '''
              
        self.i = 0
        self.j = j_node
        self.E = E
        self.I = I
        self.Length = height # Use Length to make loop plotting easier
        
        if support == 'fix':
            self.fix = 1
        else:
            self.fix = 0
        
        self.mi = [0]
        self.mj = [0]
        self.dfj = 0
        
        step = self.Length/25.0
        
        self.chart_stations = [0]
        
        for i in range(1,25):
            self.chart_stations.append(self.chart_stations[i-1]+step)
        
        self.chart_stations.append(self.Length)
        
        if self.fix == 1:           
            self.K = self.E*self.I / self.Length
            self.dfi = 0
            self.coj = 0
        else:
            self.K = (3/4.0)*(self.E*self.I / self.Length)
            self.dfi = 1
            self.coj = 0.5
        
    def reset_fem(self):
        self.mi = [0]
        self.mj = [0]

def beams_all_same(nodes, E, I, load):
    beams = []
    spans = len(nodes)-1
    
    loads = []
    loads.extend(load)

    for i in range(spans):
        beams.append(Beam(nodes[i],nodes[i+1],E,I,loads))
    
    return beams

def col_up_same(nodes, E, I,height,support):
    columns = []
    
    for node in nodes:
        columns.append(Column_Up(node,height,E,I,support))
    
    return columns

def col_dwn_same(nodes, E, I, height, support):
    columns = []
    
    for node in nodes:
        columns.append(Column_Down(node,height,E,I,support))
    
    return columns

def moment_distribution_cycle(nodes, beams, columns):
    # Moment Distribution Cycle - left to right
    for node in nodes:
        
        node.sum_node_moments(beams, columns)
        
        for beam in beams:
            if beam.i == node:
                beam.mi.append(node.m_balance*beam.dfi)
                beam.mj.append(beam.mi[-1]*0.5)
                
            elif beam.j == node:
                beam.mj.append(node.m_balance*beam.dfi)
                beam.mi.append(beam.mj[-1]*0.5)
            else:
                pass
    
        for column in columns:
            if column.i == node:
                column.mi.append(node.m_balance*column.dfi)
                if column.fix == 1:
                    column.mj.append(column.mi[-1]*0.5)
                else:
                    pass
                
            elif column.j == node:
                column.mj.append(node.m_balance*column.dfj)
                if column.fix == 1:
                    column.mi.append(column.mj[-1]*0.5)
                else:
                    pass
            else:
                pass
    
    # Moment Distribution Cycle - right to left  
    nodes_rev = nodes[::-1]
    for node in nodes_rev:
        node.sum_node_moments(beams, columns)
        
        m_bal = node.m_balance
        
        for beam in beams:
            if beam.i == node:
                beam.mi.append(m_bal*beam.dfi)
                beam.mj.append(beam.mi[-1]*0.5)
                
            elif beam.j == node:
                beam.mj.append(m_bal*beam.dfi)
                beam.mi.append(beam.mj[-1]*0.5)
                    
            else:
                pass
    
        for column in columns:
            if column.i == node:
                column.mi.append(m_bal*column.dfi)
                if column.fix == 1:
                    column.mj.append(column.mi[-1]*0.5)
                else:
                    pass
                
            elif column.j == node:
                column.mj.append(m_bal*column.dfj)
                if column.fix == 1:
                    column.mi.append(column.mj[-1]*0.5)
                else:
                    pass
            else:
                pass
        
    return 0
    
a = node(0)  
b = node(10)
c = node(20)
d = node(30)

nodes = [a,b,c,d]

A_in2 = 12*24.0
E_ksi = 4286.83
I_in4 = 13824

E_ksf = E_ksi*144.0 # k/in^2 * 144 in^2 / 1 ft^2 = 144 k/ft^2
I_ft4 = I_in4 * (1 / 20736.0) # in^4 * 1 ft^4 / 12^4 in^4 = ft^4

bm_load = [[1,0,0,10,'UDL']]

beams = beams_all_same(nodes, E_ksf, I_ft4, bm_load)

support = 'fix' 
col_height = 10

columns_down = col_dwn_same(nodes, E_ksf, I_ft4, col_height, support)

columns_up = col_up_same(nodes, E_ksf, I_ft4, col_height, support)

columns=[]
columns.extend(columns_down)
columns.extend(columns_up)

# Sum of EI/L for members at each Node
for node in nodes:
    node.sum_node_k(beams,columns)

# Beam Distribution Factors at each Node
bmdfs = []
for beam in beams:
    for node in nodes:
        if node == beam.i:
            beam.dfi = beam.K / node.K
            
            bmdfs.append(beam.dfi)
            
        elif node == beam.j:
            beam.dfj = beam.K / node.K
            bmdfs.append(beam.dfj)
        else:
            pass

# Column Distribution Factors at each Node
coldfs = []
for column in columns:
    for node in nodes:
        if node == column.i:
            column.dfi = column.K / node.K
            coldfs.append(column.dfi)
            coldfs.append(column.dfj)
            
        elif node == column.j:
            column.dfj = column.K / node.K
            coldfs.append(column.dfi)
            coldfs.append(column.dfj)
                       
        else:
            pass

# Beam Fixed End Forces
bmfef = []
for beam in beams:
    beam.applied_loads()
    beam.fef()
    bmfef.extend([beam.mi[0],beam.mj[0]])

# Moment Distribution Pass 1 - left to right
moment_distribution_cycle(nodes, beams, columns)        

# Moment Distrubution multiple passes

count = 0
n = 50

while count < n:
    moment_distribution_cycle(nodes, beams, columns)

    count +=1
    
n_m_unbalance = [node.m_unbalance for node in nodes ]
    
Final_bmi = [sum(bm.mi) for bm in beams]
Final_bmj = [sum(bm.mj) for bm in beams]

Final_colmi = [sum(col.mi) for col in columns]
Final_colmj = [sum(col.mj) for col in columns]

# Add final Moments to Beams and Get individual Beam End Reactions
node_r = [0]*len(nodes)
i=0
for beam in beams:
    r = beam.reactions()
    
    node_r[i] = node_r[i] + r[0]
    node_r[i+1] = node_r[i+1] + r[1]
    
    i+=1
    
# Determine column shortening for reactions - PL/AE
node_delta = []
i = 0
for column in columns_down:
    p = node_r[i]
    
    node_delta.append((-1.0*p*column.Length*12.0) / (A_in2 * E_ksi))
    
    i+=1

# Create New Beam Set with the column shortening as loads
delta_load = []
i=0
for beam in beams:
    delta_load.append([node_delta[i]/12.0,node_delta[i+1]/12.0,0,10,'END_DELTA'])
    i+=1

# reset beam end moments
for beam in beams:
    beam.reset_fem()
    
# reset column end moments
for column in columns:
    column.reset_fem()

# add end delta loads to beams
i=0
for beam in beams:
    beam.Load_List.append(delta_load[i])
    i+=1
    
# Beam Fixed End Forces
delta_bmfef = []
for beam in beams:
    beam.applied_loads()
    beam.fef()
    delta_bmfef.extend([beam.mi[0],beam.mj[0]])

# Moment Distribution Pass 1 - left to right
moment_distribution_cycle(nodes, beams, columns)          

# Moment Distrubution multiple passes

count = 0

while count < n:
    moment_distribution_cycle(nodes, beams, columns) 
  
    count +=1
    
Final_bmi_delta = [sum(bm.mi) for bm in beams]
Final_bmj_delta = [sum(bm.mj) for bm in beams]

Final_colmi_delta = [sum(col.mi) for col in columns]
Final_colmj_delta = [sum(col.mj) for col in columns]
   
# Add final Moments to Beams and Get individual Beam End Reactions
delta_node_r = [0]*len(nodes)
i=0
for beam in beams:
    r = beam.reactions()
    
    delta_node_r[i] = delta_node_r[i] + r[0]
    delta_node_r[i+1] = delta_node_r[i+1] + r[1]
    
    i+=1
    
# Determine column shortening for reactions - PL/AE
delta_node_delta = []
i = 0
for column in columns_down:
    p = delta_node_r[i]
    
    delta_node_delta.append((-1.0*p*column.Length*12.0) / (A_in2 * E_ksi))
    
    i+=1   

# Add final Moments to Beams and Get individual Beam End Reactions
delta_node_r = [0]*len(nodes)
i=0
for beam in beams:
    r = beam.reactions()
    
    delta_node_r[i] = delta_node_r[i] + r[0]
    delta_node_r[i+1] = delta_node_r[i+1] + r[1]
    
    i+=1
    
# Determine column shortening for reactions - PL/AE
delta_node_delta = []
i = 0
for column in columns_down:
    p = delta_node_r[i]
    print p
    
    delta_node_delta.append((-1.0*p*column.Length*12.0) / (A_in2 * E_ksi))
    i+=1