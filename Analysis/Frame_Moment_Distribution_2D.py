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
import pin_pin_beam_equations_classes as ppbeam
#import matplotlib.pyplot as plt
import time


class node:
    def __init__(self, x):

        self.x = x
        self.K = 0
        self.ry = 0

    def sum_node_k(self, beams, columns):
        self.K = 0

        for beam in beams:
            if beam.i == self or beam.j == self:
                self.K += beam.K

        for column in columns:
            if column.i == self or column.j == self:
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
        
        self.m_balance = -1.0*(self.m_unbalance)

    def sum_node_reactions(self, beams):
        node_reaction = 0

        for beam in beams:
            r = beam.reactions()

            if self == beam.i:
                node_reaction += r[0]

            elif self == beam.j:
                node_reaction += r[1]

            else:
                pass
        
        self.ry = node_reaction

        return node_reaction

class CantBeam:
    def __init__(self, ij, E=1, I=1, Length=1, Loads_list=1, left=1, label=''):
        '''
        beam element
        Loads = lists of loads in text form
        E, I, and Loads should have consistent units
        '''
        self.isleft = left
        self.type = 'cantilever'
        self.label = label
        self.Length = Length
        
        
        if self.isleft==1:
            self.i = node(0)
            self.j = ij
        else:
            self.i = ij
            self.j = node(self.i.x + self.Length)

        self.E = E
        self.I = I
        self.Load_list = [load for load in Loads_list]
        

        self.mi = [0]
        self.mj = [0]
        self.dfi = 0
        self.dfj = 0

        self.K = 0

        step = self.Length/20.0

        self.chart_stations = [0]

        for i in range(1,20):
            self.chart_stations.append(self.chart_stations[i-1]+step)

        self.chart_stations.append(self.Length)

        self.loads_built = 0

    def new_load_list(self, load_list):
        del self.Load_list[:]
        self.Load_List = [load for load in load_list]

    def applied_loads(self):

        if self.isleft == 1:
            self.applied_loads_left()
        else:
            self.applied_loads_right()

    def applied_loads_left(self):
        self.Loads = []
        self.extra_station = []

        for load in self.Load_List:
            w1 = float(load[1])
            w2 = float(load[2])
            a = float(load[3])
            b = float(load[4])
            load_type = load[-2]
            lc = self.Length

            #['Point','Moment','UDL','TRAP','SLOPE']
            if load_type == 'Point':
                self.Loads.append(ppbeam.cant_left_point(w1,a,lc,0))
                b = min(lc,a + 0.01)
                c = max(0,a - 0.01)
                self.extra_station.extend([c,a,b])

            elif load_type == 'Moment':
                self.Loads.append(ppbeam.cant_left_point_moment(w1,a,lc,0))
                b = min(lc,a + 0.01)
                c = max(0,a - 0.01)
                self.extra_station.extend([c,a,b])

            elif load_type == 'UDL':
                self.Loads.append(ppbeam.cant_left_udl(w1,a,b,lc,0))
                self.extra_station.extend([a,b])

            elif load_type == 'TRAP':
                self.Loads.append(ppbeam.cant_left_trap(w1,w2,a,b,lc,0))
                self.extra_station.extend([a,b])

            elif load_type == 'SLOPE':
                self.Loads.append(ppbeam.cant_left_nl(w1,lc))

            else:
                pass

        self.chart_stations.extend(self.extra_station)

        self.chart_stations = list(set(self.chart_stations))

        self.chart_stations.sort()

    def applied_loads_right(self):

        self.Loads = []
        self.extra_station = []

        for load in self.Load_List:
            w1 = float(load[1])
            w2 = float(load[2])
            a = float(load[3])
            b = float(load[4])
            load_type = load[-2]
            lc = self.Length

            #['Point','Moment','UDL','TRAP','SLOPE']
            if load_type == 'Point':
                self.Loads.append(ppbeam.cant_right_point(w1,a,lc,0))
                b = min(lc,a + 0.01)
                c = max(0,a - 0.01)
                self.extra_station.extend([c,a,b])

            elif load_type == 'Moment':
                self.Loads.append(ppbeam.cant_right_point_moment(w1,a,lc,0))
                b = min(lc,a + 0.01)
                c = max(0,a - 0.01)
                self.extra_station.extend([c,a,b])

            elif load_type == 'UDL':
                self.Loads.append(ppbeam.cant_right_udl(w1,a,b,lc,0))
                self.extra_station.extend([a,b])

            elif load_type == 'TRAP':
                self.Loads.append(ppbeam.cant_right_trap(w1,w2,a,b,lc,0))
                self.extra_station.extend([a,b])

            elif load_type == 'SLOPE':
                self.Loads.append(ppbeam.cant_right_nl(w1,lc))

            else:
                pass

        self.chart_stations.extend(self.extra_station)

        self.chart_stations = list(set(self.chart_stations))

        self.chart_stations.sort()

    def fef(self):

        for load in self.Loads:

            if load.kind == "SLOPE":
                pass
            else:
                if self.isleft == 1:
                    self.mi[0] += -1*load.fef()[1]
                    self.mj[0] += -1*load.fef()[3]
                else:
                    self.mi[0] += load.fef()[1]
                    self.mj[0] += load.fef()[3]

    def reactions(self):

        rl = 0
        rr = 0

        for load in self.Loads:
            rl += load.rl
            rr += load.rr

        return [rl,rr]

    def add_starting_slope(self, slope):
        '''
        given the actual required starting slope
        convert it to an EIS and add it to the cantilever
        loads.

        cnoverting the slope will allow the cantilever
        and adjacent beam span to have different E and I
        but insure that the rotation is consistent between
        the two
        '''

        slope_load = slope*self.E*self.I

        if self.isleft == 1:
            self.Loads.append(ppbeam.cant_left_nl(slope_load,self.Length))
        else:
            self.Loads.append(ppbeam.cant_right_nl(slope_load,self.Length))

    def build_load_function(self):
        
        self.equations, self.equation_strings = ppbeam.center_span_piecewise_function(self.Loads)

        self.loads_built = 1

    def station_values(self):
        v = []
        m = []
        eis = []
        eid = []
        end_delta_d = [0]*len(self.chart_stations)
        if self.loads_built == 1:

            for x in self.chart_stations:
                res = ppbeam.eval_beam_piece_function(self.equations,x)

                v.append(res[0])
                m.append(res[1])
                eis.append(res[2])
                eid.append(res[3])

            return [self.chart_stations, v, m, eis, eid],end_delta_d

        else:
            zero_out = [0]*len(self.chart_stations)

            return [self.chart_stations, zero_out, zero_out, zero_out, zero_out],end_delta_d

class Beam:
    def __init__(self, i_node, j_node, E, I, Loads_List=[], label=''):

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
        self.type = 'span'
        self.label = label

        self.mi = [0]
        self.mj = [0]
        self.dfi = 0
        self.dfj = 0

        self.K = self.E*self.I / self.Length

        step = self.Length/20.0

        self.chart_stations = [0]

        for i in range(1,20):
            self.chart_stations.append(self.chart_stations[i-1]+step)

        self.chart_stations.append(self.Length)

        self.loads_built = 0

    def new_load_list(self, load_list):
        del self.Load_List[:]
        self.Load_List = [load for load in load_list]

    def applied_loads(self):
        self.Loads = []
        self.extra_station = []

        for load in self.Load_List:
            w1 = float(load[1])
            w2 = float(load[2])
            a = float(load[3])
            b = float(load[4])
            load_type = load[-2]
            lc = self.Length

            #['Point','Moment','UDL','TRAP','END_DELTA']
            if load_type == 'Point':
                self.Loads.append(ppbeam.pl(w1,a,lc))
                b = min(lc,a + 0.01)
                c = max(0,a - 0.01)
                self.extra_station.extend([c,a,b])

            elif load_type == 'Moment':
                self.Loads.append(ppbeam.point_moment(w1,a,lc))
                b = min(lc,a + 0.01)
                c = max(0,a - 0.01)
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

    def add_end_moments(self):
        self.Loads.append(ppbeam.point_moment(sum(self.mi),0,self.Length))
        self.Loads.append(ppbeam.point_moment(sum(self.mj),self.Length,self.Length))

    def reactions(self):

        rl = 0
        rr = 0

        for load in self.Loads:
            rl += load.rl
            rr += load.rr

        return [rl,rr]

    def end_delta_fem(self):
        '''
        update the beam end moments
        for the support deflection
        '''
        for load in self.Loads:

            if load.kind == "END_DELTA":
                
                self.mi.append(load.fef()[1])
                self.mj.append(load.fef()[3])
                
            else:
                pass

    def reset_fem(self):
        self.mi = [0]
        self.mj = [0]

    def build_load_function(self):

        self.loads_nodelta = [load for load in self.Loads if load.kind != "END_DELTA"]
        self.loads_delta = [load for load in self.Loads if load.kind == "END_DELTA"]

        self.equations, self.equation_strings = ppbeam.center_span_piecewise_function(self.loads_nodelta)

        if len(self.loads_delta) == 0:
            pass
        else:
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

                if len(self.loads_delta) == 0:
                    v.append(res[0])
                    m.append(res[1])
                    eis.append(res[2])
                    eid.append(res[3])
                else:
                    res_d = ppbeam.eval_beam_piece_function(self.equations_delta,x)
                    end_delta_d.append(res_d[3])

                    v.append(res[0])
                    m.append(res[1])
                    eis.append(res[2]+res_d[2])
                    eid.append(res[3]+res_d[3])

            return [self.chart_stations, v, m, eis, eid],end_delta_d


class Column_Up:
    def __init__(self, i_node, height=1, E=1, I=1,A=1,support=1, hinge_near=0):
        '''
        upper column element
        I is about axis aligned with beams
        E, I, and Height should have consistent units
        '''

        self.i = i_node
        self.j = 0
        self.E = E
        self.I = I
        self.A = A
        self.Length = height # Use Length to make loop plotting easier
        self.orig_Length = height
        self.type = 'UP'
        self.rix = 0
        self.rjx = 0
        self.loads_built = 0

        if support == 1:
            self.fix = 1
        else:
            self.fix = 0

        self.hinge = hinge_near

        self.mi = [0]
        self.mj = [0]
        self.dfi = 0

        step = self.Length/20.0

        self.chart_stations = [0]

        for i in range(1,20):
            self.chart_stations.append(self.chart_stations[i-1]+step)

        self.chart_stations.append(self.Length)

        if self.hinge == 1:
            self.K = 0
            self.dfj = 0
            self.dfi = 0
            self.coi = 0
        else:
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

    def new_height(self, height):

        self.Length = height
        
        step = self.Length/20.0

        self.chart_stations = [0]

        for i in range(1,20):
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

                v.append(-1*res[0])
                m.append(res[1])
                eis.append(res[2])
                eid.append(res[3])
            
            self.rix = v[0]
            self.rjx = -1*v[-1]
            
            return [self.chart_stations, v, m, eis, eid]
        
        else:
            zero_out = [0]*len(self.chart_stations)
            return [self.chart_stations, zero_out, zero_out, zero_out, zero_out]
            

class Column_Down:
    def __init__(self, j_node, height=1, E=1, I=1, A=1, support=1, hinge_near=0):
        '''
        lower column element
        I is about axis aligned with beams
        E, I, and Height should have consistent units
        '''

        self.i = 0
        self.j = j_node
        self.E = E
        self.I = I
        self.A = A
        self.Length = height # Use Length to make loop plotting easier
        self.orig_Length = height
        self.type = 'DOWN'
        self.rix = 0
        self.rjx = 0
        self.riy = 0
        self.loads_built = 0

        if support == 1:
            self.fix = 1
        else:
            self.fix = 0

        self.hinge = hinge_near

        self.mi = [0]
        self.mj = [0]
        self.dfj = 0

        step = self.Length/20.0

        self.chart_stations = [0]

        for i in range(1,20):
            self.chart_stations.append(self.chart_stations[i-1]+step)

        self.chart_stations.append(self.Length)

        if self.hinge == 1:
            self.K = 0
            self.dfj = 0
            self.dfi = 0
            self.coi = 0
        else:
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

    def new_height(self, height):

        self.Length = height
        step = self.Length/20.0

        self.chart_stations = [0]

        for i in range(1,20):
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

                v.append(-1*res[0])
                m.append(res[1])
                eis.append(res[2])
                eid.append(res[3])
                
            self.rix = v[0]
            self.rjx = -1*v[-1]
            
            return [self.chart_stations, v, m, eis, eid]
        else:
            zero_out = [0]*len(self.chart_stations)
            return [self.chart_stations, zero_out, zero_out, zero_out, zero_out]
            
    def base_reaction(self):
        self.riy = self.j.ry
    

def beams_all_same(nodes, E, I, load):
    beams = []
    spans = len(nodes)-1

    loads = []
    loads.extend(load)

    for i in range(spans):
        beams.append(Beam(nodes[i],nodes[i+1],E,I,loads))

    return beams

def col_up_same(nodes, E, I, A, height,support, hinge_near):
    columns = []

    for node in nodes:
        columns.append(Column_Up(node,height,E,I,A,support,hinge_near))

    return columns

def col_dwn_same(nodes, E, I, A, height, support, hinge_near):
    columns = []

    for node in nodes:
        columns.append(Column_Down(node,height,E,I,A,support,hinge_near))

    return columns

def moment_distribution_cycle(nodes, beams, columns, tolerance=1e-11):
    # Moment Distribution Cycle - left to right
    for node in nodes:

        node.sum_node_moments(beams, columns)

        for beam in beams:
            if beam.type == 'span':
                if beam.i == node:
                    beam.mi.append(node.m_balance*beam.dfi)
                    beam.mj.append(beam.mi[-1]*0.5)

                elif beam.j == node:
                    beam.mj.append(node.m_balance*beam.dfj)
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
            if beam.type == 'span':
                if beam.i == node:
                    beam.mi.append(m_bal*beam.dfi)
                    beam.mj.append(beam.mi[-1]*0.5)

                elif beam.j == node:
                    beam.mj.append(m_bal*beam.dfj)
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

    check = all(abs(node.m_balance) < tolerance for node in nodes)

    return check

def member_distribution_factors(nodes, beams, columns):
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

def beam_fef(beams):
    # Beam Fixed End Forces
    bmfef = []
    for beam in beams:
        beam.applied_loads()
        beam.fef()
        bmfef.extend([beam.mi[0],beam.mj[0]])


def moment_distribution(nodes, beams, columns, shortening=0, tolerance=1e-11):
    member_distribution_factors(nodes, beams, columns)

    beam_fef(beams)
    # Moment Distribution Pass 1 - left to right
    moment_distribution_cycle(nodes, beams, columns, tolerance)

    # Moment Distrubution multiple passes
    count = 0
    count_max = 100
    n_previous = []
    kick = 0
    test = False
    while test == False and count < count_max and kick<1:
        test = moment_distribution_cycle(nodes, beams, columns, tolerance)

        if count <=1:
            n_m_unbalance = [node.m_unbalance for node in nodes]
            n_previous.append(n_m_unbalance)
        else:
            n_m_unbalance = [node.m_unbalance for node in nodes]

            if n_m_unbalance == n_previous[-1]:
                kick = 1
            else:
                n_previous.append(n_m_unbalance)

        count +=1

    print count

    # Add final Moments to Beams and Get individual Beam End Reactions
    node_r = []
    for beam in beams:
        if beam.type=='span':
            beam.add_end_moments()

    for node in nodes:
        node_r.append(node.sum_node_reactions(beams))

    node_delta = []
    
    if shortening == 1:
        # Determine column shortening for reactions - PL/AE
        i = 0
        for column in columns:
            if column.type == 'DOWN':
                p = node_r[i]

                node_delta.append((-1.0*p*column.Length) / (column.A * column.E))

                i+=1

        # Create New Beam Set with the column shortening as loads
        delta_load = []
        i=0
        for beam in beams:
            if beam.type == 'span':
                load = ['a',(node_delta[i]*beam.I*beam.E),(node_delta[i+1]*beam.I*beam.E),0,10,'END_DELTA','a']
                delta_load.append(load)
                beam.Load_List.append(load)
                i+=1
            else:
                delta_load.append([])

            

        '''
        #going to try not reseting the FEF to see if it speeds
        #up the second pass
        # reset beam end moments
        for beam in beams:
            beam.reset_fem()

        # reset column end moments
        for column in columns:
            column.reset_fem()
        '''

        # Beam Fixed End Forces
        delta_bmfef = []
        for beam in beams:
            beam.applied_loads()
            #beam.fef()
            #delta_bmfef.extend([beam.mi[0],beam.mj[0]])
            if beam.type == 'span':
                beam.end_delta_fem()
                delta_bmfef.append([beam.mi,beam.mj])
            else:
                pass

        # Moment Distribution Pass 1
        moment_distribution_cycle(nodes, beams, columns, tolerance)

        # Moment Distrubution multiple passes

        count_delta = 0
        test_delta = False
        n_delta_previous = []
        delta_kick = 0

        while test_delta == False and count_delta < count_max and delta_kick<1:
            test_delta = moment_distribution_cycle(nodes, beams, columns, tolerance)
            
            
            if count_delta <=1:
                n_m_unbalance_delta = [node.m_unbalance for node in nodes]
                n_delta_previous.append(n_m_unbalance_delta)
            else:
                n_m_unbalance_delta = [node.m_unbalance for node in nodes]

                if n_m_unbalance_delta == n_delta_previous[-1]:
                    delta_kick = 1
                else:
                    n_delta_previous.append(n_m_unbalance_delta)
            

            count_delta +=1

        print count_delta

        # Add final Moments to Beams and Get individual Beam End Reactions
        delta_node_r = []
        for beam in beams:
            if beam.type=='span':
                beam.add_end_moments()
        for node in nodes:
            delta_node_r.append(node.sum_node_reactions(beams))

    else:
        delta_node_r = [0 for node in nodes]
    
    return [node_r, delta_node_r]


# tolerance = 1e-6

# n1 = node(0)
# n2 = node(10)
# n3 = node(20)
# n4 = node(30)
# n5 = node(40)
# n6 = node(50)
# n7 = node(60)
# n8 = node(70)
# n9 = node(80)
# n10 = node(90)
# n11 = node(100)


# nodes = [n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11]

# start = time.time()

# time_count = 0

# A_in2 = 2.96
# A_ft2 = A_in2/144.0

# E_ksi = 29000.0
# I_in4 = 30.8

# E_ksf = E_ksi*144.0 # k/in^2 * 144 in^2 / 1 ft^2 = 144 k/ft^2
# I_ft4 = I_in4 * (1 / 20736.0) # in^4 * 1 ft^4 / 12^4 in^4 = ft^4


# bm_load = ([[1,0,1,0,10,'Point'],[1,0,2,0,10,'Point'],[1,0,3,0,10,'Point'],
            # [1,0,4,0,10,'Point'],[1,0,5,0,10,'Point'],[1,0,6,0,10,'Point'],
            # [1,0,7,0,10,'Point'],[1,0,8,0,10,'Point'],[1,0,9,0,10,'Point'],
            # [1,0,1,9,10,'UDL'],[1,0,2,8,'UDL'],
            # [1,0.5,3,7,'TRAP'],[0.5,1,3,7,'TRAP']])


# #bm_load = []

# cant_left = CantBeam(nodes[0],E_ksf,I_ft4,5,[[3,0,0,5,0,'UDL']],1)
# cant_right = CantBeam(nodes[-1],E_ksf,I_ft4,5,[[3,0,0,5,0,'UDL']],0)

# beams = beams_all_same(nodes, E_ksf, I_ft4, bm_load)

# beams.append(cant_left)
# beams.append(cant_right)

# cantilevers = [bm for bm in beams if bm.type=='cantilever']

# Consider_shortening = 1
# support = 1
# support_dwn = 1
# up_hinge = 0
# down_hinge = 0
# col_height = 10

# columns_down = col_dwn_same(nodes, E_ksf, I_ft4, A_ft2, col_height, support_dwn, down_hinge)

# columns_up = col_up_same(nodes, E_ksf, I_ft4, A_ft2, col_height, support, up_hinge)

# columns=[]
# columns.extend(columns_down)
# columns.extend(columns_up)

# member_distribution_factors(nodes,beams,columns)

# beam_fef(beams)

# node_delta = moment_distribution(nodes,beams,columns,Consider_shortening,tolerance)

# Build Beam Load Functions
# funcs = []
# delta_func = []
# for beam in beams:
    # beam.build_load_function()
    # funcs.append(beam.equation_strings)

    # if Consider_shortening == 1 and beam.type=='span':
        # delta_func.append(beam.equations_delta)
    # else:
        # pass

# Beam Max/Min Moments and EIDeltas
# and Beam charting values
# final_end_moments_bms = []
# moments = []
# EIdeltas = []
# beam_charts = []
# for beam in beams:
    # final_end_moments_bms.extend([sum(beam.mi),sum(beam.mj)])
    # if beam.type == 'span':
        # moments.append(beam.max_min_moment())
        # EIdeltas.append(beam.max_min_eidelta())

    # if beam.type=='cantilever' and beam.isleft == 1:
        # start_slope = beam_charts[0][0][3][0]/(beams[0].E*beams[0].I)

        # beam.add_starting_slope(start_slope)
        # beam.build_load_function()

    # elif beam.type=='cantilever' and beam.isleft == 0:
        # start_slope = beams[-3].station_values()[0][3][-1]/(beams[-1].E*beams[-1].I)
        # beam.add_starting_slope(start_slope)
        # beam.build_load_function()

    # beam_charts.append(beam.station_values())

# Column Load Function - only loads on columns = end moments
# if Consider_shortening == 1:
    # i=0
    # for column in columns_down:
        # h = column.Length+node_delta[i]
        # column.new_height(h)
        # i+=1

# final_end_moments_cols = []
# col_funcs = []
# for column in columns:
    # final_end_moments_cols.extend([sum(column.mi),sum(column.mj)])
    # column.build_load_function()
    # col_funcs.append(column.equation_strings)

# Column - Charts
# column_charts = []
# for column in columns:
    # column_charts.append(column.station_values())


# end = time.time()
# t = end-start
# print t

#Beam plots - will show one at a time
#i = 1
#for chart in beam_charts:
#    plt.close('all')
#
#    if Consider_shortening == 1:
#        delta = [((delt*12.0)/(E_ksf*I_ft4))+supdelt for delt,supdelt in zip(chart[0][4],chart[1])]
#        s = [sl/(E_ksf*I_ft4) for sl in chart[0][3]]
#    else:
#        delta = [((delt*12.0)/(E_ksf*I_ft4)) for delt in chart[0][4]]
#        s = [sl/(E_ksf*I_ft4) for sl in chart[0][3]]
#
#    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
#    ax1.plot(chart[0][0], chart[0][1], 'r-')
#    ax1.plot(chart[0][0], [0]*len(chart[0][0]), 'k-')
#    ax1.set_title('Shear - kips')
#    ax2.plot(chart[0][0], chart[0][2], 'b-')
#    ax2.plot(chart[0][0], [0]*len(chart[0][0]), 'k-')
#    ax2.set_title('Moment - ft-kips')
#    ax3.plot(chart[0][0], s, 'g-')
#    ax3.plot(chart[0][0], [0]*len(chart[0][0]), 'k-')
#    ax3.set_title('Slope - Rad')
#    ax3.ticklabel_format(axis='y',style='sci',scilimits=(1,3))
#    ax4.plot(chart[0][0], delta, 'c-')
#    ax4.plot(chart[0][0], [0]*len(chart[0][0]), 'k-')
#    ax4.set_title('Deflection - in')
#    ax4.ticklabel_format(axis='y',style='sci',scilimits=(1,3))
#
#    f.suptitle('Beam {0}'.format(i))
#
#    plt.tight_layout()
#
#    plt.show()
#
#    i+=1

#Column plots - will show one at a time
#i = 1
#for chart in column_charts:
#    plt.close('all')
#
#    delta = [((delt*12.0)/(E_ksf*I_ft4)) for delt in chart[4]]
#    s = [sl/(E_ksf*I_ft4) for sl in chart[3]]
#
#    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
#    ax1.plot(chart[1], chart[0], 'r-')
#    ax1.plot([0]*len(chart[0]), chart[0],'k-')
#    ax1.set_title('Shear - kips')
#    ax2.plot(chart[2], chart[0], 'b-')
#    ax2.plot([0]*len(chart[0]), chart[0],'k-')
#    ax2.set_title('Moment - ft-kips')
#    ax3.plot(s, chart[0], 'g-')
#    ax3.plot([0]*len(chart[0]),chart[0], 'k-')
#    ax3.set_title('Slope - Rad')
#    ax3.ticklabel_format(axis='x',style='sci',scilimits=(1,3))
#    ax4.plot(delta, chart[0], 'c-')
#    ax4.plot([0]*len(chart[0]), chart[0], 'k-')
#    ax4.set_title('Deflection - in')
#    ax4.ticklabel_format(axis='x',style='sci',scilimits=(1,3))
#
#    f.suptitle('Column {0}'.format(i))
#
#    plt.tight_layout()
#
#    plt.show()
#
#    i+=1
