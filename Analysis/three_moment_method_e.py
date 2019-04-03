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
import numpy as np
from numpy.linalg import inv
import scipy as sci
import scipy.integrate
import pin_pin_beam_equations_classes as ppbeam
import math

import time

class three_moment_method(object):

    def __init__(self,beam_spans=[120.00], beam_momentofinertia=[120.00], cant='N', beam_loads_raw=[[1000.00,1000.00,60.00,60.00,'POINT',0]], E=29000000.00, iters=20, displace=[0,0]):
        # Implementation of the Theory of Three Momements, https://en.wikipedia.org/wiki/Theorem_of_three_moments
        #   Inputs:
        #   beam_spans = a list of span lengths -- Expected Units: in -- Example: [120,120]
        #   beam_momentofinteria = a list of Moment of Inertias per span -- Expected Units: in^4 -- Example: [118,118]
        #   cant = cantilever designation as a string either 'L','R','B', or 'N'
        #           L = Left
        #           R = Right
        #           B = Both
        #           N = None
        #
        #   beam_loads_raw = a list of loads (see examples of Loads below), for single applied load expects [[load per below]]
        #
        #           Point Loads:
        #           [P,P,a,a,'POINT',span]
        #               P = Load -- Expected Units: lbs
        #               a = Load location from left support -- Expected Units: in
        #               'POINT' = Loading type as string and in all caps options are: 'POINT', 'POINT_MOMENT', 'UDL', or 'TRAP'
        #               span = integer indicating what span the load is in -- 0 for first span
        #                     P+
        #               ___a__|_____
        #               ^           ^
        #
        #           Point Moments:
        #           [M,M,a,a,'POINT_MOMENT',span]
        #               M = Moment -- Expected Units: in-lbs
        #               a = Moment location from left support -- Expected Units: in
        #               'POINT_MOMENT' = Loading type as string and in all caps options are: 'POINT', 'POINT_MOMENT', 'UDL', or 'TRAP'
        #               span = integer indicating what span the load is in -- 0 for first span
        #                     --->M+
        #               ___a__|___|___
        #               ^     <---     ^
        #
        #           Uniform loads:
        #           [w,w,a,b,'UDL',span]
        #               w = Load -- Expected Units: lbs per in
        #               a = Load start location from left support -- Expected Units: in
        #               b = Load end location from left support -- Expected Units: in
        #               'UDL' = Loading type as string and in all caps options are: 'POINT', 'POINT_MOMENT', 'UDL', or 'TRAP'
        #               span = integer indicating what span the load is in -- 0 for first span
        #                    ___w+__
        #               ___a_|_____|_____
        #               ^          |     ^
        #               |----b-----|
        #
        #           Trapezoidal Loads:
        #           [w1,w2,a,b,'TRAP',span]
        #               w1 = Start Load -- Expected Units: lbs per in
        #               w2 = End Load -- Expected Units: lbs per in
        #               a = Load start location from left support -- Expected Units: in
        #               b = Load end location from left support -- Expected Units: in
        #               'TRAP' = Loading type as string and in all caps options are: 'POINT', 'POINT_MOMENT', 'UDL', or 'TRAP'
        #               span = integer indicating what span the load is in -- 0 for first span
        #                     w1+
        #                     |     w2+
        #               ___a__|_____|___
        #               ^           |    ^
        #               |------b----|

        #   E = modulus of elasticity assumed to be constant over all spans as a float -- Expected Units: psi
        #   iters = Integer number of stations to create per span
        #   displace = list of support displacements -- Expected Units: in -- Example: if you have N spans you should have N+1 displacement values inclusive of cantilever ends
        #               take care to make sure values are 0 for cantilever ends. 4 span total both cantilever list would be [0,1,0,0,0]

        N = len(beam_spans)                       # number of spans

        sumL = np.cumsum(beam_spans)              # cumulative sum of beam lengths
        sumL = sumL.tolist()
        
        #Additional calculation stations at point loads +/-0.0001 and start and end of line loads
        xs_add = []#create a list of 0's x N - to add additional stations per span
        
        for s in range(0,N):
            xs_add.append([])
        
        for load in beam_loads_raw:
            if load[4] == 'POINT' or load[4] == "POINT_MOMENT":
                inspan = int(load[5])
                xs_add[inspan].append(load[2])
                if load[2]+0.0001 > beam_spans[inspan]:
                    pass
                else:
                    xs_add[inspan].append(load[2]+0.0001)
                if load[2]-0.0001 < beam_spans[inspan]:
                    pass
                else:
                    xs_add[inspan].append(load[2]-0.0001)
            else:
                inspan = int(load[5])
                xs_add[inspan].append(load[2])
                xs_add[inspan].append(load[3])
                
        xs_add = [list(set(i)) for i in xs_add]
        max_plus = max([len(i) for i in xs_add])
        [i.extend([0]*(max_plus-len(i))) for i in xs_add if len(i) < max_plus]
        
        self.add_stations = xs_add
        
        #Create calculation stations
        new_iters = iters+max_plus+1
        xs = np.zeros((new_iters, N))
        j = 0
        for j in range(0, N):
            xs[0, j] = 0
            xs[iters, j] = beam_spans[j]
            i = 0
            for i in range(1, iters):
                xs[i, j] = xs[i-1, j] + beam_spans[j]/iters
            
            z=0
            for i in range((iters+1),(new_iters)):
                xs[i,j] = xs_add[j][z]
                z+=1
                j = 0
        for j in range(0, N):
            to_sort = xs[:,j].tolist()
            to_sort.sort()
            xs[:,j] = np.asarray(to_sort)
            
        self.stations = xs
        v_diag = np.zeros((new_iters, N))
        v_diag_cantL = np.zeros((new_iters, N))
        v_diag_cantR = np.zeros((new_iters, N))
        m_diag = np.zeros((new_iters, N))
        m_diag_cantL = np.zeros((new_iters, N))
        m_diag_cantR = np.zeros((new_iters, N))
        s_diag = np.zeros((new_iters, N))
        d_diag = np.zeros((new_iters, N))
        r_span = np.zeros((2, N))

        # Span as simple support Moment, Shears, and Reactions
        j = 0
        for j in range(0, N):
            for loads in beam_loads_raw:
                if loads[5] == j:
                    if loads[4] == "POINT":
                        load = ppbeam.pl(loads[0], loads[2], beam_spans[j])
                        v = load.v(xs[:,j])
                        m = load.m(xs[:,j])
                        s = load.eis(xs[:,j]) / (beam_momentofinertia[j]*E)
                        d = load.eid(xs[:,j]) / (beam_momentofinertia[j]*E)
                        v_diag[:, j] = v_diag[:, j]+v
                        m_diag[:, j] = m_diag[:, j]+m
                        s_diag[:, j] = s_diag[:, j]+s
                        d_diag[:, j] = d_diag[:, j]+d
                        r_span[0, j] = r_span[0, j]+load.rl
                        r_span[1, j] = r_span[1, j]+load.rr

                    elif loads[4] == "POINT_MOMENT":
                        load = ppbeam.point_moment(loads[0], loads[2], beam_spans[j])
                        v = load.v(xs[:,j])
                        m = load.m(xs[:,j])
                        s = load.eis(xs[:,j]) / (beam_momentofinertia[j]*E)
                        d = load.eid(xs[:,j]) / (beam_momentofinertia[j]*E)
                        v_diag[:, j] = v_diag[:, j]+v
                        m_diag[:, j] = m_diag[:, j]+m
                        s_diag[:, j] = s_diag[:, j]+s
                        d_diag[:, j] = d_diag[:, j]+d
                        r_span[0, j] = r_span[0, j]+load.rl
                        r_span[1, j] = r_span[1, j]+load.rr

                    elif loads[4] == "UDL":
                        load = ppbeam.udl(loads[0], loads[2], loads[3], beam_spans[j])
                        v = load.v(xs[:,j])
                        m = load.m(xs[:,j])
                        s = load.eis(xs[:,j]) / (beam_momentofinertia[j]*E)
                        d = load.eid(xs[:,j]) / (beam_momentofinertia[j]*E)
                        v_diag[:, j] = v_diag[:, j]+v
                        m_diag[:, j] = m_diag[:, j]+m
                        s_diag[:, j] = s_diag[:, j]+s
                        d_diag[:, j] = d_diag[:, j]+d
                        r_span[0, j] = r_span[0, j]+load.rl
                        r_span[1, j] = r_span[1, j]+load.rr

                    elif loads[4] == "TRAP":
                        load = ppbeam.trap(loads[0], loads[1], loads[2], loads[3], beam_spans[j])
                        v = load.v(xs[:,j])
                        m = load.m(xs[:,j])
                        s = load.eis(xs[:,j]) / (beam_momentofinertia[j]*E)
                        d = load.eid(xs[:,j]) / (beam_momentofinertia[j]*E)
                        v_diag[:, j] = v_diag[:, j]+v
                        m_diag[:, j] = m_diag[:, j]+m
                        s_diag[:, j] = s_diag[:, j]+s
                        d_diag[:, j] = d_diag[:, j]+d
                        r_span[0, j] = r_span[0, j]+load.rl
                        r_span[1, j] = r_span[1, j]+load.rr
                        
                    elif loads[4] == "NL":
                        load = ppbeam.no_load()
                        v = load.v(xs[:,j])
                        m = load.m(xs[:,j])
                        s = load.eis(xs[:,j]) / (beam_momentofinertia[j]*E)
                        d = load.eid(xs[:,j]) / (beam_momentofinertia[j]*E)
                        v_diag[:, j] = v_diag[:, j]+v
                        m_diag[:, j] = m_diag[:, j]+m
                        s_diag[:, j] = s_diag[:, j]+s
                        d_diag[:, j] = d_diag[:, j]+d
                        r_span[0, j] = r_span[0, j]+load.rl
                        r_span[1, j] = r_span[1, j]+load.rr
                    else:
                        pass
                else:
                    pass

        # Horizontal center of moment region
        j = 0
        a_xl_xr = np.zeros((3, N))
        m_xx = np.zeros((new_iters, N))
        for j in range(0, N):

            m_xx[:, j] = m_diag[:, j]*xs[:, j]
            A = sci.integrate.cumtrapz(m_diag[:, j], xs[:, j])
            A = A[-1]
            print A
            a_xl_xr[0, j] = A
            if A == 0:
                a_xl_xr[1, j] = 0
                a_xl_xr[2, j] = 0
            else:
                xl_A = sci.integrate.cumtrapz(m_xx[:, j], xs[:, j])
                xl = (1/A)*xl_A[-1]
                a_xl_xr[1, j] = xl
                a_xl_xr[2, j] = beam_spans[j] - xl
        
        # Cantilever Moments, Shears, and reactions
        mr_cant = 0
        ml_cant = 0
        rr_cant = 0
        rl_cant = 0
        if cant[0] == 'L' or cant[0] == 'B':
            v_diag[:, 0] = 0
            m_diag[:, 0] = 0
            s_diag[:, 0] = 0
            d_diag[:, 0] = 0
            for loads in beam_loads_raw:
                    if loads[5] == 0:
                        if loads[4] == "POINT":
                            load = ppbeam.cant_left_point(loads[0], loads[2], beam_spans[0], 0)
                            v = load.v(xs[:,0])
                            m = load.m(xs[:,0])
                            s = load.eis(xs[:,0]) / (beam_momentofinertia[j]*E)
                            d = load.eid(xs[:,0]) / (beam_momentofinertia[j]*E)
                            v_diag[:, 0] = v_diag[:, 0]+v
                            m_diag[:, 0] = m_diag[:, 0]+m
                            s_diag[:, 0] = s_diag[:, 0]+s
                            d_diag[:, 0] = d_diag[:, 0]+d
                            rr_cant = rr_cant+load.rr
                            mr_cant = mr_cant+load.mr

                        if loads[4] == "POINT_MOMENT":
                            load = ppbeam.cant_left_point_moment(loads[0], loads[2], beam_spans[0], 0)
                            v = load.v(xs[:,0])
                            m = load.m(xs[:,0])
                            s = load.eis(xs[:,0]) / (beam_momentofinertia[j]*E)
                            d = load.eid(xs[:,0]) / (beam_momentofinertia[j]*E)
                            v_diag[:, 0] = v_diag[:, 0]+v
                            m_diag[:, 0] = m_diag[:, 0]+m
                            s_diag[:, 0] = s_diag[:, 0]+s
                            d_diag[:, 0] = d_diag[:, 0]+d
                            rr_cant = rr_cant+load.rr
                            mr_cant = mr_cant+load.mr

                        elif loads[4] == "UDL":
                            load = ppbeam.cant_left_udl(loads[0], loads[2], loads[3], beam_spans[0], 0)
                            v = load.v(xs[:,0])
                            m = load.m(xs[:,0])
                            s = load.eis(xs[:,0]) / (beam_momentofinertia[j]*E)
                            d = load.eid(xs[:,0]) / (beam_momentofinertia[j]*E)
                            v_diag[:, 0] = v_diag[:, 0]+v
                            m_diag[:, 0] = m_diag[:, 0]+m
                            s_diag[:, 0] = s_diag[:, 0]+s
                            d_diag[:, 0] = d_diag[:, 0]+d
                            rr_cant = rr_cant+load.rr
                            mr_cant = mr_cant+load.mr

                        elif loads[4] == "TRAP":
                            load = ppbeam.cant_left_trap(loads[0], loads[1], loads[2], loads[3], beam_spans[0], 0)
                            v = load.v(xs[:,0])
                            m = load.m(xs[:,0])
                            s = load.eis(xs[:,0]) / (beam_momentofinertia[j]*E)
                            d = load.eid(xs[:,0]) / (beam_momentofinertia[j]*E)
                            v_diag[:, 0] = v_diag[:, 0]+v
                            m_diag[:, 0] = m_diag[:, 0]+m
                            s_diag[:, 0] = s_diag[:, 0]+s
                            d_diag[:, 0] = d_diag[:, 0]+d
                            rr_cant = rr_cant+load.rr
                            mr_cant = mr_cant+load.mr
                        elif loads[4] == "NL":
                            load = ppbeam.no_load()
                            v = load.v(xs[:,j])
                            m = load.m(xs[:,j])
                            s = load.eis(xs[:,j]) / (beam_momentofinertia[j]*E)
                            d = load.eid(xs[:,j]) / (beam_momentofinertia[j]*E)
                            v_diag[:, j] = v_diag[:, j]+v
                            m_diag[:, j] = m_diag[:, j]+m
                            s_diag[:, j] = s_diag[:, j]+s
                            d_diag[:, j] = d_diag[:, j]+d
                            rr_cant = 0
                            mr_cant = 0
                        else:
                            pass

        else:
            pass

        if cant[0] == 'R' or cant[0] == 'B':
            v_diag[:, N-1] = 0
            m_diag[:, N-1] = 0
            s_diag[:, N-1] = 0
            d_diag[:, N-1] = 0
            for loads in beam_loads_raw:
                    if loads[5] == N-1:
                        if loads[4] == "POINT":
                            load = ppbeam.cant_right_point(loads[0], loads[2], beam_spans[N-1], 0)
                            v = load.v(xs[:,N-1])
                            m = load.m(xs[:,N-1])
                            s = load.eis(xs[:,N-1]) / (beam_momentofinertia[j]*E)
                            d = load.eid(xs[:,N-1]) / (beam_momentofinertia[j]*E)
                            v_diag[:, N-1] = v_diag[:, N-1]+v
                            m_diag[:, N-1] = m_diag[:, N-1]+m
                            s_diag[:, N-1] = s_diag[:, N-1]+s
                            d_diag[:, N-1] = d_diag[:, N-1]+d
                            rl_cant = rl_cant+load.rl
                            ml_cant = ml_cant+load.ml

                        if loads[4] == "POINT_MOMENT":
                            load = ppbeam.cant_right_point_moment(loads[0], loads[2], beam_spans[N-1], 0)
                            v = load.v(xs[:,N-1])
                            m = load.m(xs[:,N-1])
                            s = load.eis(xs[:,N-1]) / (beam_momentofinertia[j]*E)
                            d = load.eid(xs[:,N-1]) / (beam_momentofinertia[j]*E)
                            v_diag[:, N-1] = v_diag[:, N-1]+v
                            m_diag[:, N-1] = m_diag[:, N-1]+m
                            s_diag[:, N-1] = s_diag[:, N-1]+s
                            d_diag[:, N-1] = d_diag[:, N-1]+d
                            rl_cant = rl_cant+load.rl
                            ml_cant = ml_cant+load.ml

                        elif loads[4] == "UDL":
                            load = ppbeam.cant_right_udl(loads[0], loads[2], loads[3], beam_spans[N-1], 0)
                            v = load.v(xs[:,N-1])
                            m = load.m(xs[:,N-1])
                            s = load.eis(xs[:,N-1]) / (beam_momentofinertia[j]*E)
                            d = load.eid(xs[:,N-1]) / (beam_momentofinertia[j]*E)
                            v_diag[:, N-1] = v_diag[:, N-1]+v
                            m_diag[:, N-1] = m_diag[:, N-1]+m
                            s_diag[:, N-1] = s_diag[:, N-1]+s
                            d_diag[:, N-1] = d_diag[:, N-1]+d
                            rl_cant = rl_cant+load.rl
                            ml_cant = ml_cant+load.ml

                        elif loads[4] == "TRAP":
                            load = ppbeam.cant_right_trap(loads[0], loads[1], loads[2], loads[3], beam_spans[N-1], 0)
                            v = load.v(xs[:,N-1])
                            m = load.m(xs[:,N-1])
                            s = load.eis(xs[:,N-1]) / (beam_momentofinertia[j]*E)
                            d = load.eid(xs[:,N-1]) / (beam_momentofinertia[j]*E)
                            v_diag[:, N-1] = v_diag[:, N-1]+v
                            m_diag[:, N-1] = m_diag[:, N-1]+m
                            s_diag[:, N-1] = s_diag[:, N-1]+s
                            d_diag[:, N-1] = d_diag[:, N-1]+d
                            rl_cant = rl_cant+load.rl
                            ml_cant = ml_cant+load.ml

                        elif loads[4] == "NL":
                            load = ppbeam.no_load()
                            v = load.v(xs[:,j])
                            m = load.m(xs[:,j])
                            s = load.eis(xs[:,j]) / (beam_momentofinertia[j]*E)
                            d = load.eid(xs[:,j]) / (beam_momentofinertia[j]*E)
                            v_diag[:, j] = v_diag[:, j]+v
                            m_diag[:, j] = m_diag[:, j]+m
                            s_diag[:, j] = s_diag[:, j]+s
                            d_diag[:, j] = d_diag[:, j]+d
                            rl_cant = 0
                            ml_cant = 0

                        else:
                            pass

        else:
            pass


        self.F = np.zeros((N+1,N+1))
        j=0
        for j in range(1,N):
            self.F[j,j-1] = beam_spans[j-1]/beam_momentofinertia[j-1]
            self.F[j,j] = 2*((beam_spans[j-1]/beam_momentofinertia[j-1])+(beam_spans[j]/beam_momentofinertia[j]))
            self.F[j,j+1] = beam_spans[j]/beam_momentofinertia[j]

        if cant[0]=='L':

            self.F[0,0] = 1
            self.F[1,:] = 0
            self.F[1,1] = 1
            self.F[N,N] = 1

        elif cant[0]=='R':
            self.F[0,0] = 1
            self.F[N,N] = 1
            self.F[N-1,:] = 0
            self.F[N-1,N-1] = 1

        elif cant[0]=='B':
            self.F[0,0] = 1
            self.F[1,:] = 0
            self.F[1,1] = 1
            self.F[N,N] = 1
            self.F[N-1,:] = 0
            self.F[N-1,N-1] = 1

        else:
            self.F[0,0] = 1
            self.F[N,N] = 1

        self.delta = np.zeros((N+1,1))
        j=0
        for j in range(1,N):

            l = j-1
            r = j
            #support settlement delta
            self.delta[j] = ((-6*a_xl_xr[1,l]*a_xl_xr[0,l])/(beam_spans[l]*beam_momentofinertia[l])+(-6*a_xl_xr[2,r]*a_xl_xr[0,r])/(beam_spans[r]*beam_momentofinertia[r]))+(6*E*(((displace[l]-displace[r])/beam_spans[l])+((displace[r+1]-displace[r])/beam_spans[r])))

        if cant[0]=='L':

            self.delta[0] = 0
            self.delta[1] = mr_cant

        elif cant[0]=='R':
            self.delta[N] = 0
            self.delta[N-1] = ml_cant

        elif cant[0]=='B':
            self.delta[0] = 0
            self.delta[1] = mr_cant
            self.delta[N] = 0
            self.delta[N-1] = ml_cant

        else:
            pass

        #Moments @ Interior Supports
        M = np.dot(inv(self.F),self.delta)

        #Reactions @ interior Supports
        R = np.zeros((N+1,1))

        j=0
        for j in range(0,N+1):

            l = j-1
            r = j

            if j == 0:
                R[j] = (r_span[0,r]) - (M[j]/beam_spans[r]) + (M[j+1]/beam_spans[r])

            elif j == N:
                R[j] = (r_span[1,l]) - (M[j]/beam_spans[l]) + (M[j-1]/beam_spans[l])

            elif j > 0 and j < N:
                R[j] = (r_span[0,r]+r_span[1,l]) - (M[j]/beam_spans[r]) - (M[j]/beam_spans[l])  + (M[j+1]/beam_spans[r]) + (M[j-1]/beam_spans[l])
            else:
                pass

        #Support Moment response on spans
        j=0
        for j in range(0,N):
            if j==0 and cant[0]=='L':
                j+=1

            elif j==0 and cant[0]=='B':
                j+=1

            elif j==N-1 and cant[0]=='R':
                j+=1

            elif j==N-1 and cant[0]=='B':
                j+=1

            else:
                load1 = ppbeam.point_moment(M[j],0,beam_spans[j])
                load2 = ppbeam.point_moment(-1.0*M[j+1],beam_spans[j],beam_spans[j])
                v = load1.v(xs[:,j]) + load2.v(xs[:,j])
                m = load1.m(xs[:,j]) + load2.m(xs[:,j])
                s = (load1.eis(xs[:,j]) + load2.eis(xs[:,j])) / (beam_momentofinertia[j]*E)
                d = (load1.eid(xs[:,j]) + load2.eid(xs[:,j])) / (beam_momentofinertia[j]*E)
                v_diag[:, j] = v_diag[:, j]+v
                m_diag[:, j] = m_diag[:, j]+m
                s_diag[:, j] = s_diag[:, j]+s
                d_diag[:, j] = d_diag[:, j]+d

        run = 0
        for con in displace:
            if con == 0:
                run = run + 0
            else:
                run = run + 1

        if run == 1:
            #correct d for support displacement
            for j in range(0,N):
                span = beam_spans[j]

                slope_i = math.atan(-1.0*(displace[j]-displace[j+1])/span)
                s_diag[:,j] = s_diag[:,j] + slope_i

                for i in range(0,len(xs[:,j])):
                    delt_i = displace[j] + (((displace[j+1]-displace[j])/span)*xs[i,j])
                    d_diag[i,j] = d_diag[i,j] + delt_i

            #correct cantilever d for support displacement
            if cant[0]=='L' or cant[0] =='B':
                if displace[2] == 0 and displace[1] == 0:
                    pass
                else:
                    d_diag[:,0] = d_diag[:,0]+displace[1]


            if cant[0]=='R' or cant[0] =='B':
                if displace[N-2] == 0 and displace[N-1] == 0:
                    pass
                else:
                   d_diag[:,-1] = d_diag[:,-1]+displace[-2]
        else:
            pass
        
        #correct cantilever slope and deflection for interior span end slopes
        if cant[0]=='L' or cant[0]=='B':
            cant_l_fix = ppbeam.cant_left_nl(s_diag[0,1], beam_spans[0])
            s = cant_l_fix.eis(xs[:,0])
            d = cant_l_fix.eid(xs[:,0])
            s_diag[:, 0] = s_diag[:, 0]+s
            d_diag[:, 0] = d_diag[:, 0]+d
        else:
            pass

        if cant[0]=='R' or cant[0]=='B':
            cant_r_fix = ppbeam.cant_right_nl(s_diag[-1,-2])
            s = cant_r_fix.eis(xs[:,-1])
            d = cant_r_fix.eid(xs[:,-1])
            s_diag[:, -1] = s_diag[:, -1]+s
            d_diag[:, -1] = d_diag[:, -1]+d
        else:
            pass

        j=0
        for j in range(1,N):
            xs[:,j] = xs[:,j] + sumL[j-1]   #converts lengths to global rather than local ie span 2 x[0] now = span 1 x[-1] or length in lieu of 0

        xs = xs/12
        for j in range(0,N):
            v_diag[:,j] = v_diag[:,j]/1000       #assumes input of lbs and converts output to kips
            m_diag[:,j] = m_diag[:,j]/(12*1000)     #assumes input of in and lbs and converts output to ft-kips

        self.xs = xs
        self.v_diag = v_diag
        self.m_diag = m_diag
        self.s_diag = s_diag
        self.d_diag = d_diag
        self.R = R
        self.M = M

    def res(self):
        return self.xs, self.v_diag, self.m_diag, self.s_diag, self.d_diag, self.R, self.M


start = time.time()
loads = [[1000.00,1000.00,30.0,30.0,'POINT',0],[1000.00,1000.00,0,120.0,'UDL',1],[1000.00,1000.00,60.0,60.0,'POINT_MOMENT',2],[1000.00,1000.00,45.0,45.0,'POINT',2],[1000.00,1000.00,0,60.0,'UDL',3]]
test = three_moment_method([60.0,120.0,120.0,60.0],[30.8,30.8,30.8,30.8],'B',loads, 29000000.00, 20, [0,0,0,0,0])
end = time.time()
t = end-start
m = test.m_diag
s = test.s_diag
s1 = s[:,1]

stations = test.stations
add_stations = test.add_stations
len_add = max([len(i) for i in add_stations])
Mo = test.M
Re = test.R