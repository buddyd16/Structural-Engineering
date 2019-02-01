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
import matplotlib.pyplot as plt


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
        
        self.loads_built = 0
        
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
    
    def build_load_function(self):
        
        self.loads_nodelta = [load for load in self.Loads if load.kind != "END_DELTA"]
        self.loads_delta = [load for load in self.Loads if load.kind == "END_DELTA"]
        
        self.equations, self.equation_strings = ppbeam.center_span_piecewise_function(self.loads_nodelta)
        
        self.equations_delta, self.equations_strings_delta = ppbeam.center_span_piecewise_function(self.loads_delta)
        
        # points of inflection
        self.zero_shear_loc = ppbeam.points_of_zero_shear(self.equations[0])
        
        self.zero_moment_loc = ppbeam.points_of_zero_shear(self.equations[1])

        self.zero_slope_loc = ppbeam.points_of_zero_shear(self.equations[2])
        
        # add points of inflection to the charting stations
        self.chart_stations.extend(self.zero_shear_loc)
        self.chart_stations.extend(self.zero_moment_loc)
        self.chart_stations.extend(self.zero_slope_loc)
        self.chart_stations = list(set(self.chart_stations))       
        self.chart_stations.sort()
        
        self.loads_built = 1
    
    def max_min_moment(self):
        
        if self.loads_built == 1:
            m_out = []
            for x in self.zero_shear_loc:
                m_res = ppbeam.eval_beam_piece_function(self.equations,x)
                
                m_out.append([x,m_res[1]])
            
            return m_out
        else:
            return [[0,0]]
        
    def max_min_eidelta(self):
        if self.loads_built == 1:
            eid_out = []
            for x in self.zero_slope_loc:
                eid_res = ppbeam.eval_beam_piece_function(self.equations,x)
                
                eid_out.append([x,eid_res[3]])
            
            return eid_out        
        else:
            return [[0,0]]
    
    def station_values(self):
        v = []
        m = []
        eis = []
        eid = []
        end_delta_d = []
        if self.loads_built == 1:
            
            for x in self.chart_stations:
                res = ppbeam.eval_beam_piece_function(self.equations,x)
  
                res_d = ppbeam.eval_beam_piece_function(self.equations_delta,x)

                
                end_delta_d.append(res_d[3])
                v.append(res[0])
                m.append(res[1])
                eis.append(res[2])
                eid.append(res[3])
        
            return [self.chart_stations, v, m, eis, eid],end_delta_d
                
            
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
            self.K = (0.75)*(self.E*self.I / self.Length)
            self.dfj = 1
            self.coi = 0.5
            
    def reset_fem(self):
        self.mi = [0]
        self.mj = [0]

    def build_load_function(self):
        Mi = sum(self.mi)
        Mj = sum(self.mj)
        
        L1 = ppbeam.point_moment(Mi,0,self.Length)
        L2 = ppbeam.point_moment(Mj,self.Length,self.Length)
        
        self.equations, self.equation_strings = ppbeam.center_span_piecewise_function([L1,L2])
        
        # points of inflection
        self.zero_shear_loc = ppbeam.points_of_zero_shear(self.equations[0])
        
        self.zero_moment_loc = ppbeam.points_of_zero_shear(self.equations[1])

        self.zero_slope_loc = ppbeam.points_of_zero_shear(self.equations[2])
        
        # add points of inflection to the charting stations
        self.chart_stations.extend(self.zero_shear_loc)
        self.chart_stations.extend(self.zero_moment_loc)
        self.chart_stations.extend(self.zero_slope_loc)
        self.chart_stations = list(set(self.chart_stations))       
        self.chart_stations.sort()
        
        self.loads_built = 1
    
    def station_values(self):
        v = []
        m = []
        eis = []
        eid = []

        if self.loads_built == 1:
            
            for x in self.chart_stations:
                res = ppbeam.eval_beam_piece_function(self.equations,x)
                
                v.append(res[0])
                m.append(res[1])
                eis.append(res[2])
                eid.append(res[3])
        
            return [self.chart_stations, v, m, eis, eid]
        
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
            self.K = (0.75)*(self.E*self.I / self.Length)
            self.dfi = 1
            self.coj = 0.5
        
    def reset_fem(self):
        self.mi = [0]
        self.mj = [0]
        
    def build_load_function(self):
        Mi = sum(self.mi)
        Mj = sum(self.mj)
        
        L1 = ppbeam.point_moment(Mi,0,self.Length)
        L2 = ppbeam.point_moment(Mj,self.Length,self.Length)
        
        self.equations, self.equation_strings = ppbeam.center_span_piecewise_function([L1,L2])
        
        # points of inflection
        self.zero_shear_loc = ppbeam.points_of_zero_shear(self.equations[0])
        
        self.zero_moment_loc = ppbeam.points_of_zero_shear(self.equations[1])

        self.zero_slope_loc = ppbeam.points_of_zero_shear(self.equations[2])
        
        # add points of inflection to the charting stations
        self.chart_stations.extend(self.zero_shear_loc)
        self.chart_stations.extend(self.zero_moment_loc)
        self.chart_stations.extend(self.zero_slope_loc)
        self.chart_stations = list(set(self.chart_stations))       
        self.chart_stations.sort()
        
        self.loads_built = 1
    
    def station_values(self):
        v = []
        m = []
        eis = []
        eid = []

        if self.loads_built == 1:
            
            for x in self.chart_stations:
                res = ppbeam.eval_beam_piece_function(self.equations,x)
                
                v.append(res[0])
                m.append(res[1])
                eis.append(res[2])
                eid.append(res[3])
        
            return [self.chart_stations, v, m, eis, eid]
            
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
    check = all(abs(node.m_balance) < 1e-10 for node in nodes)
    
    return check
    
a = node(0)  
b = node(10)
c = node(20)
d = node(30)



nodes = [a,b,c,d]

A_in2 = 12*24.0
A_ft2 = A_in2/144.0

E_ksi = 4286.83
I_in4 = 13824

E_ksf = E_ksi*144.0 # k/in^2 * 144 in^2 / 1 ft^2 = 144 k/ft^2
I_ft4 = I_in4 * (1 / 20736.0) # in^4 * 1 ft^4 / 12^4 in^4 = ft^4

bm_load = [[1,0,0,10,'UDL']]

beams = beams_all_same(nodes, E_ksf, I_ft4, bm_load)

support = 'fix'
support_dwn = 'fix'
col_height = 10

columns_down = col_dwn_same(nodes, E_ksf, I_ft4, col_height, support_dwn)

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
n = 100
test = False
while test == False:
    test = moment_distribution_cycle(nodes, beams, columns)

    count +=1

print count
  
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
    
    node_delta.append((-1.0*p*column.Length) / (A_ft2 * E_ksf))
    
    i+=1

# Create New Beam Set with the column shortening as loads
delta_load = []
i=0
for beam in beams:
    delta_load.append([node_delta[i],node_delta[i+1],0,10,'END_DELTA'])

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

count_delta = 0
test_delta = False
while test_delta == False:
    test_delta = moment_distribution_cycle(nodes, beams, columns) 
  
    count_delta +=1
    
print count_delta
    
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
    
# Build Beam Load Functions
funcs = []
delta_func = []
for beam in beams:
    beam.build_load_function()
    funcs.append(beam.equation_strings)
    delta_func.append(beam.equations_delta)

# Beam Max/Min Moments and EIDeltas
# and Beam charting values
moments = []
EIdeltas = []
beam_charts = []
for beam in beams:
    moments.append(beam.max_min_moment())
    EIdeltas.append(beam.max_min_eidelta())
    beam_charts.append(beam.station_values())

# Column Load Function - only loads on columns = end moments
col_funcs = []
for column in columns:
    column.build_load_function()
    col_funcs.append(column.equation_strings)
    
# Column - Charts
column_charts = []
for column in columns:
    column_charts.append(column.station_values())
    
# Beam plots - will show one at a time
i = 1
for chart in beam_charts:
    plt.close('all')
    
    delta = [((delt*12.0)/(E_ksf*I_ft4))+supdelt for delt,supdelt in zip(chart[0][4],chart[1])]
    s = [sl/(E_ksf*I_ft4) for sl in chart[0][3]]
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1.plot(chart[0][0], chart[0][1], 'r-')
    ax1.plot(chart[0][0], [0]*len(chart[0][0]), 'k-')
    ax1.set_title('Shear - kips')
    ax2.plot(chart[0][0], chart[0][2], 'b-')
    ax2.plot(chart[0][0], [0]*len(chart[0][0]), 'k-')
    ax2.set_title('Moment - ft-kips')
    ax3.plot(chart[0][0], s, 'g-')
    ax3.plot(chart[0][0], [0]*len(chart[0][0]), 'k-')
    ax3.set_title('Slope - Rad')
    ax3.ticklabel_format(axis='y',style='sci',scilimits=(1,3))
    ax4.plot(chart[0][0], delta, 'c-')
    ax4.plot(chart[0][0], [0]*len(chart[0][0]), 'k-')
    ax4.set_title('Deflection - in')
    ax4.ticklabel_format(axis='y',style='sci',scilimits=(1,3))
    
    f.suptitle('Beam {0}'.format(i))
    
    plt.tight_layout()
    
    plt.show()
    
    i+=1

# Column plots - will show one at a time
i = 1
for chart in column_charts:
    plt.close('all')
    
    delta = [((delt*12.0)/(E_ksf*I_ft4)) for delt in chart[4]]
    s = [sl/(E_ksf*I_ft4) for sl in chart[3]]
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1.plot(chart[1], chart[0], 'r-')
    ax1.plot([0]*len(chart[0]), chart[0],'k-')
    ax1.set_title('Shear - kips')
    ax2.plot(chart[2], chart[0], 'b-')
    ax2.plot([0]*len(chart[0]), chart[0],'k-')
    ax2.set_title('Moment - ft-kips')
    ax3.plot(s, chart[0], 'g-')
    ax3.plot([0]*len(chart[0]),chart[0], 'k-')
    ax3.set_title('Slope - Rad')
    ax3.ticklabel_format(axis='x',style='sci',scilimits=(1,3))
    ax4.plot(delta, chart[0], 'c-')
    ax4.plot([0]*len(chart[0]), chart[0], 'k-')
    ax4.set_title('Deflection - in')
    ax4.ticklabel_format(axis='x',style='sci',scilimits=(1,3))
    
    f.suptitle('Column {0}'.format(i))
    
    plt.tight_layout()
    
    plt.show()
    
    i+=1
    