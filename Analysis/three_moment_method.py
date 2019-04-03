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

#import time

def pl(p, a, l, x):
    b = l - a
    rl = (p * b) / l
    rr = (p * a) / l
    c4 = ((-rl * a ** 3) / 3) - ((rr * a ** 3) / 3) + ((rr * l * a ** 2) / 2)
    c2 = (-1 / l) * ((c4) + ((rr * l ** 3) / 3))
    c1 = ((-rr * a ** 2) / 2) - ((rl * a ** 2) / 2) + (rr * l * a) + c2
    if x <= a:
        v = rl
        m = rl * x
        d = ((rl * x ** 3) / 6) + (c1 * x)
    else:
        v = -1 * rr
        m = (-1 * rr * x) + (rr * l)
        d = ((-rr * x ** 3) / 6) + ((rr * l * x ** 2) / 2) + (c2 * x) + c4
    return (rl, rr, v, m, d)


def udl(W, a, b, l, x):
    c = a + b
    rl = (W * b) - (((W * b) * (a + (b / 2))) / l)
    rr = (((W * b) * (a + (b / 2))) / l)
    c1 = 0
    c2 = ((-1 * W * a ** 2) / 2)
    c3 = rr * l
    c7 = 0
    c8 = ((-1 * c1 * a ** 2) / 2) + ((c2 * a ** 2) / 2) + ((5 * W * a ** 4) / 24) + c7
    c9 = ((-1 * rl * c ** 3) / 3) - ((rr * c ** 3) / 3) + ((W * c ** 4) / 8) - ((W * a * c ** 3) / 3) - ((c2 * c ** 2) / 2) + ((c3 * c ** 2) / 2) + c8
    c6 = ((rr * l ** 2) / 6) - ((c3 * l) / 2) - (c9 / l)
    c5 = ((-1 * rl * c ** 2) / 2) + ((W * c ** 3) / 6) - ((W * a * c ** 2) / 2) - ((rr * c ** 2) / 2) + (c3 * c) - (c2 * c) + c6
    c4 = ((W * a ** 3) / 3) + (c2 * a) + c5 - (c1 * a)
    if x <= a:
        v = rl
        m = (rl * x) + c1
        d = ((rl * x ** 3) / 6) + ((c1 * x ** 2) / 2) + (c4 * x) + c7
    elif x < c:
        v = rl - (W * (x - a))
        m = (rl * x) - ((W * x ** 2) / 2) + (W * a * x) + c2
        d = ((rl * x ** 3) / 6) - ((W * x ** 4) / 24) + ((W * a * x ** 3) / 6) + ((c2 * x ** 2) / 2) + (c5 * x) + c8
    else:
        v = -rr
        m = (-1 * rr * x) + c3
        d = ((-1 * rr * x ** 3) / 6) + ((c3 * x ** 2) / 2) + (c6 * x) + c9
    return (rl, rr, v, m, d)


def trapl(w1, w2, a, b, l, x):
    d = a + b
    s = (w2 - w1) / b
    if w2 == -1*w1:
        xbar = b/2
    else:
        xbar = (b * ((2 * w2) + w1)) / (3 * (w2 + w1))
    W = b * ((w1 + w2) / 2)
    rr = (W * (a + xbar)) / l
    rl = W - rr
    c1 = 0
    c2 = c1 + ((a ** 3 * s) / 6) + ((a ** 2 * (w1 - (s * a))) / 2) + ((((s * a) - (2 * w1)) * a ** 2) / 2)
    c3 = rr * l
    c7 = 0
    c8 = ((-1 * c1 * a ** 2) / 2) - ((a ** 5 * s) / 30) - ((a ** 4 * (w1 - (s * a))) / 8) - ((((s * a) - (2 * w1)) * a ** 4) / 6) + ((c2 * a ** 2) / 2) + c7
    c9 = ((-1 * rl * d ** 3) / 3) + ((d ** 5 * s) / 30) + ((d ** 4 * (w1 - (s * a))) / 8) + ((((s * a) - (2 * w1)) * a * d ** 3) / 6) - ((c2 * d ** 2) / 2) + c8 - ((rr * d ** 3) / 3) + ((c3 * d ** 2) / 2)
    c6 = (((rr * l ** 3) / 6) - ((c3 * l ** 2) / 2) - c9) / l
    c5 = ((-1 * rr * d ** 2) / 2) + (c3 * d) + c6 - ((rl * d ** 2) / 2) + ((d ** 4 * s) / 24) + ((d ** 3 * (w1 - (s * a))) / 6) + ((((s * a) - (2 * w1)) * a * d ** 2) / 4) - (c2 * d)
    c4 = ((-1 * a ** 4 * s) / 24) - ((a ** 3 * (w1 - (s * a))) / 6) - ((((s * a) - (2 * w1)) * a ** 3) / 4) + (c2 * a) + c5 - (c1 * a)
    if x <= a:
        v = rl
        m = (rl * x) + c1
        d = ((rl * x ** 3) / 6) + ((c1 * x ** 2) / 2) + (c4 * x) + c7
    elif x < d:
        v = rl - ((x ** 2 * s) / 2) - (x * (w1 - (s * a))) - ((((s * a) - (2 * w1)) * a) / 2)
        m = (rl * x) - ((x ** 3 * s) / 6) - ((x ** 2 * (w1 - (s * a))) / 2) - ((((s * a) - (2 * w1)) * a * x) / 2) + c2
        d = ((rl * x ** 3) / 6) - ((x ** 5 * s) / 120) - ((x ** 4 * (w1 - (s * a))) / 24) - ((((s * a) - (2 * w1)) * a * x ** 3) / 12) + ((c2 * x ** 2) / 2) + (c5 * x) + c8
    else:
        v = -1 * rr
        m = (-1 * rr * x) + c3
        d = ((-1 * rr * x ** 3) / 6) + ((c3 * x ** 2) / 2) + (c6 * x) + c9
    return (rl, rr, v, m, d)


def cant_right_point(p, a, l, x):
    rl = p
    ml = -1*p*a
    if x <= a:
        v = p
        m = rl*x + ml
    if x > a:
        v = 0
        m = 0
    return(rl, ml, v, m)


def cant_right_udl(w, a, b, l, x):
    c = a+b
    w_tot = w*c
    rl = w_tot
    ml = -1*w_tot*(b-(c/2))
    if x <= a:
        v = w_tot
        m = rl*x + ml
    elif a < x <= b:
        v = w_tot - w*(x-a)
        m = rl*x + ml - (w*(x-a)*((x-a)/2))
    else:
        v = 0
        m = 0
    return(rl, ml, v, m)


def cant_left_point(p, a, l, x):
    rr = p
    mr = -1*p*(l-a)
    if x < a:
        v = 0
        m = 0
    if x >= a:
        v = -1*rr
        m = -1*rr*(x-a)
    return(rr, mr, v, m)


def cant_left_udl(w, a, b, l, x):
    c = a+b
    w_tot = w*c
    rr = w_tot
    mr = -1*w_tot*(l-b+(c/2))
    if x <= a:
        v = 0
        m = 0
    elif a < x <= b:
        v = - w*(x-a)
        m = -1*(w*(x-a)*((x-a)/2))
    else:
        v = w_tot
        m = -1*w_tot(x-b+(c/2))
    return(rr, mr, v, m)


def cant_right_trap(w1, w2, a, b, l, x):
    c = a+b
    w = 0.5*(w1+w2)*b
    d = a+(((w1+(2*w2))/(3*(w2+w1)))*b)
    s = (w1-w2)/b
    rl = w
    ml = -1*w*d
    if x <= a:
        v = w
        m = (w*x)+ml
    elif a < x < c:
        cx = x-a
        wx = w1-(s*cx)
        dx = x - (a+(((w1+(2*wx))/(3*(wx+w1)))*cx))
        wwx = 0.5*(w1+wx)*cx
        v = w-wwx
        m = (w*x+ml)-(wwx*dx)
    else:
        v = 0
        m = 0
    return(rl, ml, v, m)


def cant_left_trap(w1, w2, a, b, l, x):
    c = a+b
    w = 0.5*(w1+w2)*b
    dl = a+(((w1+(2*w2))/(3*(w2+w1)))*b)
    dr = l-dl
    s = (w1-w2)/b
    rr = w
    mr = -1*w*dr
    if x <= a:
        v = 0
        m = 0
    elif a < x < c:
        cx = x-a
        wx = w1-(s*cx)
        dlx = a+(((w1+(2*wx))/(3*(wx+w1)))*cx)
        drx = x-dlx
        wwx = 0.5*(w1+wx)*cx
        v = -1*wwx
        m = -1*wwx*drx
    else:
        v = -1*w
        m = -1*w*(x-dl)
    return(rr, mr, v, m)

class three_moment_method(object):
    
    def __init__(self,beam_spans=[120.00], beam_momentofinertia=[120.00], cant='N', beam_loads_raw=[[1000.00,1000.00,60.00,60.00,'POINT',0]], E=29000000.00, iters=100, displace=[0,0]):
        # Implementation of the Theory of Three Momements, https://en.wikipedia.org/wiki/Theorem_of_three_moments
        #   Inputs:
        #   beam_spans = a list of span lengths -- Expected Units: in -- Example: [120,120]
        #   beam_momentofinteria = a list of Moment of Inertias per span -- Expected Units: in^4 -- Example: [118,118]
        #   cant = cantilever designation as a string either 'L','R','B', or 'N'
        #           L = Left
        #           R = Right
        #           B = Both
        #           N = None
        #   beam_loads_raw = a list of loads (see examples of Loads below), for single applied load expects [[load per below]]
        #           Point Loads:
        #           [P,P,a,a,'POINT',span]
        #               P = Load -- Expected Units: lbs
        #               a = Load location from left support -- Expected Units: in
        #               'POINT' = Loading type as string and in all caps options are: 'POINT', 'UDL', or 'TRAP'
        #               span = integer indicating what span the load is in -- 0 for first span
        #                     P
        #               ___a__|_____
        #               ^           ^
        #           Uniform loads:
        #           [w,w,a,b,'UDL',span]
        #               w = Load -- Expected Units: lbs per in
        #               a = Load start location from left support -- Expected Units: in
        #               b = Load width -- Expected Units: in -- a + b = end location from left support be careful to make sure this is not greater than the span length
        #               'UDL' = Loading type as string and in all caps options are: 'POINT', 'UDL', or 'TRAP'
        #               span = integer indicating what span the load is in -- 0 for first span
        #                    ____w__
        #               ___a_|__b__|_____
        #               ^               ^
        #           Trapezoidal Loads:
        #           [w1,w2,a,b,'TRAP',span]
        #               w1 = Start Load -- Expected Units: lbs per in
        #               w2 = End Load -- Expected Units: lbs per in
        #               a = Load start location from left support -- Expected Units: in
        #               b = Load width -- Expected Units: in -- a + b = end location from left support be careful to make sure this is not greater than the span length
        #               'TRAP' = Loading type as string and in all caps options are: 'POINT', 'UDL', or 'TRAP'
        #               span = integer indicating what span the load is in -- 0 for first span
        #                     w1
        #                     |     w2
        #               ___a__|__b__|___
        #               ^               ^
        #   E = modulus of elasticity assumed to be constant over all spans as a float -- Expected Units: psi
        #   iters = Integer number of stations to create per span
        #   displace = list of support displacements -- Expected Units: in -- Example: if you have N spans you should have N+1 displacement values inclusive of cantilever ends
        #               take care to make sure values are 0 for cantilever ends. 4 span total both cantilever list would be [0,1,0,0,0]
        
        N = len(beam_spans)                       # number of spans

        sumL = np.cumsum(beam_spans)              # cumulative sum of beam lengths
        sumL = sumL.tolist()

        xs = np.zeros((iters+1, N))
        j = 0
        for j in range(0, N):
            xs[0, j] = 0
            xs[iters, j] = beam_spans[j]
            i = 0
            for i in range(1, iters):
                xs[i, j] = xs[i-1, j] + beam_spans[j]/iters
        v_diag = np.zeros((iters+1, N))
        v_diag_cantL = np.zeros((iters+1, N))
        v_diag_cantR = np.zeros((iters+1, N))
        m_diag = np.zeros((iters+1, N))
        m_diag_cantL = np.zeros((iters+1, N))
        m_diag_cantR = np.zeros((iters+1, N))
        s_diag = np.zeros((iters+1, N))
        d_diag = np.zeros((iters+1, N))
        r_span = np.zeros((2, N))

        # Span as simple support Moment, Shears, and Reactions
        j = 0
        for j in range(0, N):
            i = 0
            for i in range(0, iters+1):
                for load in beam_loads_raw:
                    if load[5] == j:
                        if load[4] == "POINT":
                            rl, rr, v, m, d = pl(load[0], load[2], beam_spans[j], xs[i, j])
                            v_diag[i, j] = v_diag[i, j]+v
                            m_diag[i, j] = m_diag[i, j]+m

                        elif load[4] == "UDL":
                            rl, rr, v, m, d = udl(load[0], load[2], load[3], beam_spans[j], xs[i, j])
                            v_diag[i, j] = v_diag[i, j]+v
                            m_diag[i, j] = m_diag[i, j]+m

                        elif load[4] == "TRAP":
                            rl, rr, v, m, d = trapl(load[0], load[1], load[2], load[3], beam_spans[j], xs[i, j])
                            v_diag[i, j] = v_diag[i, j]+v
                            m_diag[i, j] = m_diag[i, j]+m

                        else:
                            pass
                    else:
                        pass

        for j in range(0, N):
            for load in beam_loads_raw:
                if load[5] == j:
                    if load[4] == "POINT":
                        rl, rr, v, m, d = pl(load[0], load[2], beam_spans[j], xs[0, j])
                        r_span[0, j] = r_span[0, j]+rl
                        r_span[1, j] = r_span[1, j]+rr
                    elif load[4] == "UDL":
                        rl, rr, v, m, d = udl(load[0], load[2], load[3], beam_spans[j], xs[0, j])
                        r_span[0, j] = r_span[0, j]+rl
                        r_span[1, j] = r_span[1, j]+rr
                    elif load[4] == "TRAP":
                        rl, rr, v, m, d = trapl(load[0], load[1], load[2], load[3], beam_spans[j], xs[0, j])
                        r_span[0, j] = r_span[0, j]+rl
                        r_span[1, j] = r_span[1, j]+rr
                    else:
                        pass
                else:
                    pass

        # Horizontal center of moment region
        j = 0
        a_xl_xr = np.zeros((3, N))
        m_xx = np.zeros((iters+1, N))
        for j in range(0, N):

            m_xx[:, j] = m_diag[:, j]*xs[:, j]
            A = sci.integrate.simps(m_diag[:, j], xs[:, j])
            a_xl_xr[0, j] = A
            if A == 0:
                a_xl_xr[1, j] = 0
                a_xl_xr[2, j] = 0
            else:
                xl = (1/A)*sci.integrate.simps(m_xx[:, j], xs[:, j])
                a_xl_xr[1, j] = xl
                a_xl_xr[2, j] = beam_spans[j] - xl

        # Cantilever Moments, Shears, and reactions
        mr_cant = 0
        ml_cant = 0
        rr_cant = 0
        rl_cant = 0
        if cant[0] == 'L' or cant[0] == 'B':
            for i in range(0, iters+1):
                for load in beam_loads_raw:
                        if load[5] == 0:
                            if load[4] == "POINT":
                                rr, mr, v, m = cant_left_point(load[0], load[2], beam_spans[0], xs[i, 0])
                                v_diag_cantL[i, 0] = v_diag_cantL[i, 0]+v
                                m_diag_cantL[i, 0] = m_diag_cantL[i, 0]+m

                            elif load[4] == "UDL":
                                rr, mr, v, m = cant_left_udl(load[0], load[2], load[3], beam_spans[0], xs[i, 0])
                                v_diag_cantL[i, 0] = v_diag_cantL[i, 0]+v
                                m_diag_cantL[i, 0] = m_diag_cantL[i, 0]+m

                            elif load[4] == "TRAP":
                                rr, mr, v, m = cant_left_trap(load[0], load[1], load[2], load[3], beam_spans[0], xs[i, 0])
                                v_diag_cantL[i, 0] = v_diag_cantL[i, 0]+v
                                m_diag_cantL[i, 0] = m_diag_cantL[i, 0]+m

                            else:
                                pass
            for load in beam_loads_raw:
                if load[5] == 0:
                    if load[4] == "POINT":
                        rr, mr, v, m = cant_left_point(load[0], load[2], beam_spans[0], xs[i, 0])

                        rr_cant = rr_cant+rr
                        mr_cant = mr_cant+mr

                    elif load[4] == "UDL":
                        rr, mr, v, m = cant_left_udl(load[0], load[2], load[3], beam_spans[0], xs[i, 0])

                        rr_cant = rr_cant+rr
                        mr_cant = mr_cant+mr

                    elif load[4] == "TRAP":
                        rr, mr, v, m = cant_left_trap(load[0], load[1], load[2], load[3], beam_spans[0], xs[i, 0])

                        rr_cant = rr_cant+rr
                        mr_cant = mr_cant+mr

                    else:
                        pass

        else:
            pass

        if cant[0] == 'R' or cant[0] == 'B':
            v_diag[:, N-1] = 0
            m_diag[:, N-1] = 0
            for i in range(0, iters+1):
                for load in beam_loads_raw:
                        if load[5] == N-1:
                            if load[4] == "POINT":
                                rl, ml, v, m = cant_right_point(load[0], load[2], beam_spans[N-1], xs[i, N-1])
                                v_diag_cantR[i, N-1] = v_diag_cantR[i, N-1]+v
                                m_diag_cantR[i, N-1] = m_diag_cantR[i, N-1]+m

                            elif load[4] == "UDL":
                                rl, ml, v, m = cant_right_udl(load[0], load[2], load[3], beam_spans[N-1], xs[i, N-1])
                                v_diag_cantR[i, N-1] = v_diag_cantR[i, N-1]+v
                                m_diag_cantR[i, N-1] = m_diag_cantR[i, N-1]+m

                            elif load[4] == "TRAP":
                                rl, ml, v, m = cant_right_trap(load[0], load[1], load[2], load[3], beam_spans[N-1], xs[i, N-1])
                                v_diag_cantR[i, N-1] = v_diag_cantR[i, N-1]+v
                                m_diag_cantR[i, N-1] = m_diag_cantR[i, N-1]+m

                            else:
                                pass

            for load in beam_loads_raw:
                if load[5] == N-1:
                    if load[4]=="POINT":
                        rl,ml,v,m = cant_right_point(load[0],load[2],beam_spans[N-1],xs[i,N-1])
                        rl_cant = rl_cant+rl
                        ml_cant = ml_cant+ml

                    elif load[4]=="UDL":
                        rl,ml,v,m = cant_right_udl(load[0],load[2],load[3],beam_spans[N-1],xs[i,N-1])
                        rl_cant=rl_cant+rl
                        ml_cant = ml_cant+ml

                    elif load[4]=="TRAP":
                        rl,ml,v,m = cant_right_trap(load[0],load[1],load[2],load[3],beam_spans[N-1],xs[i,N-1])
                        rl_cant=rl_cant+rl
                        ml_cant = ml_cant+ml

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
            self.delta[N]=0
            self.delta[N-1]=ml_cant

        elif cant[0]=='B':
            self.delta[0] = 0
            self.delta[1] = mr_cant
            self.delta[N]=0
            self.delta[N-1]=ml_cant

        else:
            pass

        M = np.dot(inv(self.F),self.delta)

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

        slope = np.zeros((N,1))
        j=0
        for j in range(0,N):
            r = j

            slope[j] = ((a_xl_xr[2,r]*a_xl_xr[0,r])/beam_spans[r])+((M[j+1]*beam_spans[r])/6)+((M[j]*beam_spans[r])/3)

            slope[j] = -1*slope[j] / (E*beam_momentofinertia[r])

        #Cantilever Slope Corrections
        if cant[0]=='R' or cant[0] =='B':
            slope[N-1] =  ((a_xl_xr[1,N-2]*a_xl_xr[0,N-2])/beam_spans[N-2])+((M[N-2]*beam_spans[N-2])/6)+((M[N-1]*beam_spans[N-2])/3)
            slope[N-1] = slope[N-1] / (E*beam_momentofinertia[N-2])

        else:
            pass

        j=0
        for j in range(0,N):
            v_diag[:,j] = (-1*v_diag[:,j]) + ((M[j]-M[j+1])/beam_spans[j])
            x=0
            for x in range(0,iters+1):
                m_diag[x,j] = m_diag[x,j]-(((M[j]-M[j+1])/beam_spans[j])*xs[x,j])+M[j]
            s_diag[:,j] = (sci.integrate.cumtrapz(m_diag[:,j],xs[:,j], initial = 0)/(E*beam_momentofinertia[j]))+slope[j,0]
            d_diag[:,j] = sci.integrate.cumtrapz(s_diag[:,j],xs[:,j], initial = 0)
            
        #correct d for support displacement
        #based on small angle approximations and similar triangles
        for j in range(0,N):
            span = beam_spans[j]
            for i in range(0,len(xs[:,j])):
                delt_i = displace[j] + (((displace[j+1]-displace[j])/span)*xs[i,j])
                d_diag[i,j] = d_diag[i,j] + delt_i
                
        #Cantilever Diagram Corrections
        #For left side compatibility states slope at right of support should be equal and opposite to slope on cantilever side of support
        #calculate slope and deflection from left to right and then invert results for actual condition.
        if cant[0]=='L' or cant[0] =='B':
            v_diag[:,0] = -1*v_diag_cantL[:,0]
            m_diag[:,0] = m_diag_cantL[:,0]
            s_diag[:,0] = (sci.integrate.cumtrapz(m_diag[::-1,0],xs[:,0], initial = 0)/(E*beam_momentofinertia[0]))-slope[1,0]
            d_diag[:,0] = sci.integrate.cumtrapz(s_diag[:,0],xs[:,0], initial = 0)
            s_diag[:,0] = -1*s_diag[::-1,0]
            d_diag[:,0] = d_diag[::-1,0]

        else:
            pass
        #For Right side compatibility states slope at left of support should be equal and opposite to slope on cantilever side of support
        #calculate slope and deflection from left to right using corrected slope diagram
        if cant[0]=='R' or cant[0] =='B':
            v_diag[:,N-1] = -1*v_diag_cantR[:,N-1]
            m_diag[:,N-1] = m_diag_cantR[:,N-1]
            s_diag[:,N-1] = (sci.integrate.cumtrapz(m_diag[:,N-1],xs[:,N-1], initial = 0)/(E*beam_momentofinertia[N-1]))+slope[N-1,0]
            d_diag[:,N-1] = sci.integrate.cumtrapz(s_diag[:,N-1],xs[:,N-1], initial = 0)

        else:
            pass

        #correct cantilever d for support displacement
        #based on small angle approximations and similar triangles
        if cant[0]=='L' or cant[0] =='B':
            if displace[2] == 0 and displace[1] == 0:
                pass
            else:        
                span_cant = beam_spans[0]
                span_int = beam_spans[1]
                for i in range(0,len(xs[:,0])):
                    if displace[2] == 0 or displace[2]==displace[1]:
                        simt = displace[1]/span_int
                        if displace[2]==displace[1]:
                            delt_i = displace[1]
                        else:
                            delt_i = ((span_cant-xs[i,0])+span_int) * simt

                        d_diag[i,0]= d_diag[i,0]+ delt_i
                    else:
                        xl= (displace[2]/((displace[2]-displace[1])/span_int))
                        xr= span_int - xl
                        delt_i= -1*((span_cant-xs[i,0])+xr) * (displace[2]/xl)
                        d_diag[i,0]= d_diag[i,0]+ delt_i

        if cant[0]=='R' or cant[0] =='B':
            if displace[N-2] == 0 and displace[N-1] == 0:
                pass
            else: 
                span_cant= beam_spans[N-1]
                span_int= beam_spans[N-2]
                for i in range(0,len(xs[:,0])):
                    if displace[N-2] == 0 or displace[N-2] == displace[N-1]:
                        simt = displace[N-1]/span_int
                        if displace[N-2] == displace[N-1]:
                            delt_i = displace[N-1]
                        else:
                            delt_i = (xs[i,0]+span_int) * simt
                        d_diag[i,N-1]= d_diag[i,N-1] + delt_i
                    else:
                        xl= displace[N-2]/((displace[N-2]-displace[N-1])/span_int)
                        xr= span_int - xl
                        delt_i= -1*(xs[i,N-1] + xr)* displace[N-2]/xl
                        d_diag[i,N-1]= d_diag[i,N-1] + delt_i

        j=0
        for j in range(1,N):
            xs[:,j] = xs[:,j] + sumL[j-1]           #converts lengths to global rather than local ie span 2 x[0] now = span 1 x[-1] or length in lieu of 0

        xs = xs/12
        for j in range(0,N):
            v_diag[:,j] = -1*v_diag[:,j]/1000       #assumes input of lbs and converts output to kips
            m_diag[:,j] = m_diag[:,j]/(12*1000)     #assumes input of in and lbs and converts output to ft-kips
            
        self.xs = xs
        self.v_diag = v_diag
        self.m_diag = m_diag
        self.s_diag = s_diag
        self.d_diag = d_diag
        self.R = R
        self.M = M

'''
start = time.time()
test = three_moment_method([60,120,120,60],[30.8,30.8,30.8,30.8],'B',[[1000.00,1000.00,60.0,60.0,'POINT',1]], 29000000.00, 20, [0,0,0,0,0])
end = time.time()
t = end-start
m = test.m_diag
'''