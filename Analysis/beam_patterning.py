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
import matplotlib
matplotlib.use('TKAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Tkinter as tk
from Tkinter import PhotoImage
import tkFileDialog
import tkFont
import numpy as np
from numpy.linalg import inv
from numpy import unravel_index
import scipy as sci
import scipy.integrate
import matplotlib.pyplot as plt
import os
import itertools
import math
import tkMessageBox
import time

def load_pattern(num_spans):
    test = []
    n = num_spans
    for r in range(n):
       for item in itertools.combinations(range(n), r):
           check = [1]*n
           for i in item:
               check[i] = 0
           test.append(check)
    return test
    
def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    adjust_yaxis(ax2, (y1-y2)/2, v2)
    adjust_yaxis(ax1, (y2-y1)/2, v1)


def adjust_yaxis(ax, ydif, v):
    """shift axis ax by ydiff, maintaining point v at the same location"""
    inv = ax.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, ydif))
    miny, maxy = ax.get_ylim()
    miny, maxy = miny - v, maxy - v
    if -miny > maxy or (-miny == maxy and dy > 0):
        nminy = miny
        nmaxy = miny*(maxy+dy)/(miny+dy)
    else:
        nmaxy = maxy
        nminy = maxy*(miny+dy)/(maxy+dy)
    ax.set_ylim(nminy+v, nmaxy+v)


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
        eis = ((rl * x ** 2)  / 2) + c1
        eid = ((rl * x ** 3) / 6) + (c1 * x)
    else:
        v = -1 * rr
        m = (-1 * rr * x) + (rr * l)
        eis = ((-1.0 * rr * x ** 2)/2.0) + (rr * l * x) + c2
        eid = ((-rr * x ** 3) / 6) + ((rr * l * x ** 2) / 2) + (c2 * x) + c4
    return (rl, rr, v, m, eid)


def udl(W, a, b, l, x):
    c = b-a
    rl = (W * c) - (((W * c) * (a + (c / 2))) / l)
    rr = (((W * c) * (a + (c / 2))) / l)
    c1 = 0
    c2 = ((-1 * W * a ** 2) / 2)
    c3 = rr * l
    c7 = 0
    c8 = ((-1 * c1 * a ** 2) / 2) + ((c2 * a ** 2) / 2) + ((5 * W * a ** 4) / 24) + c7
    c9 = ((-1 * rl * b ** 3) / 3) - ((rr * b ** 3) / 3) + ((W * b ** 4) / 8) - ((W * a * b ** 3) / 3) - ((c2 * b ** 2) / 2) + ((c3 * b ** 2) / 2) + c8
    c6 = ((rr * l ** 2) / 6) - ((c3 * l) / 2) - (c9 / l)
    c5 = ((-1 * rl * b ** 2) / 2) + ((W * b ** 3) / 6) - ((W * a * b ** 2) / 2) - ((rr * b ** 2) / 2) + (c3 * b) - (c2 * b) + c6
    c4 = ((W * a ** 3) / 3) + (c2 * a) + c5 - (c1 * a)
    if x <= a:
        v = rl
        m = (rl * x) + c1
        eis = ((rl * x ** 2) / 2) + (c1 * x) + c4
        eid = ((rl * x ** 3) / 6) + ((c1 * x ** 2) / 2) + (c4 * x) + c7
    elif x < b:
        v = rl - (W * (x - a))
        m = (rl * x) - ((W * x ** 2) / 2) + (W * a * x) + c2
        eis = ((rl * x **2) / 2) - ((W * x ** 3) / 6) + ((W * a * x **2) / 2) + (c2 * x) + c5
        eid = ((rl * x ** 3) / 6) - ((W * x ** 4) / 24) + ((W * a * x ** 3) / 6) + ((c2 * x ** 2) / 2) + (c5 * x) + c8
    else:
        v = -rr
        m = (-1 * rr * x) + c3
        eis = ((-1 * rr * x ** 2) / 2) + (c3 * x) + c6
        eid = ((-1 * rr * x ** 3) / 6) + ((c3 * x ** 2) / 2) + (c6 * x) + c9
    return (rl, rr, v, m, eid)


def trapl(w1, w2, a, b, l, x):
    d = b-a
    s = (w2 - w1) / d
    if w2 == -1*w1:
        xbar = d/2
    else:
        xbar = (d * ((2 * w2) + w1)) / (3 * (w2 + w1))
    W = d * ((w1 + w2) / 2)
    rr = (W * (a + xbar)) / l
    rl = W - rr
    c1 = 0
    c2 = c1 + ((a ** 3 * s) / 6) + ((a ** 2 * (w1 - (s * a))) / 2) + ((((s * a) - (2 * w1)) * a ** 2) / 2)
    c3 = rr * l
    c7 = 0
    c8 = ((-1 * c1 * a ** 2) / 2) - ((a ** 5 * s) / 30) - ((a ** 4 * (w1 - (s * a))) / 8) - ((((s * a) - (2 * w1)) * a ** 4) / 6) + ((c2 * a ** 2) / 2) + c7
    c9 = ((-1 * rl * b ** 3) / 3) + ((b ** 5 * s) / 30) + ((b ** 4 * (w1 - (s * a))) / 8) + ((((s * a) - (2 * w1)) * a * b ** 3) / 6) - ((c2 * b ** 2) / 2) + c8 - ((rr * b ** 3) / 3) + ((c3 * b ** 2) / 2)
    c6 = (((rr * l ** 3) / 6) - ((c3 * l ** 2) / 2) - c9) / l
    c5 = ((-1 * rr * b ** 2) / 2) + (c3 * b) + c6 - ((rl * b ** 2) / 2) + ((b ** 4 * s) / 24) + ((b ** 3 * (w1 - (s * a))) / 6) + ((((s * a) - (2 * w1)) * a * b ** 2) / 4) - (c2 * b)
    c4 = ((-1 * a ** 4 * s) / 24) - ((a ** 3 * (w1 - (s * a))) / 6) - ((((s * a) - (2 * w1)) * a ** 3) / 4) + (c2 * a) + c5 - (c1 * a)
    if x <= a:
        v = rl
        m = (rl * x) + c1
        eis = ((rl * x ** 2) / 2) + (c1 * x) + c4
        eid = ((rl * x ** 3) / 6) + ((c1 * x ** 2) / 2) + (c4 * x) + c7
    elif x < b:
        v = rl - ((x ** 2 * s) / 2) - (x * (w1 - (s * a))) - ((((s * a) - (2 * w1)) * a) / 2)
        m = (rl * x) - ((x ** 3 * s) / 6) - ((x ** 2 * (w1 - (s * a))) / 2) - ((((s * a) - (2 * w1)) * a * x) / 2) + c2
        eis = ((rl * x ** 2) / 2) - ((x ** 4 * s) / 24) - ((x ** 3 * (w1 - (s * a))) / 6) - ((((s * a) - (2 * w1)) * a * x ** 2) / 4) + (c2 * x) + c5
        eid = ((rl * x ** 3) / 6) - ((x ** 5 * s) / 120) - ((x ** 4 * (w1 - (s * a))) / 24) - ((((s * a) - (2 * w1)) * a * x ** 3) / 12) + ((c2 * x ** 2) / 2) + (c5 * x) + c8
    else:
        v = -1 * rr
        m = (-1 * rr * x) + c3
        eis = ((-1 * rr * x ** 2) / 2) + (c3 * x) + c6
        eid = ((-1 * rr * x ** 3) / 6) + ((c3 * x ** 2) / 2) + (c6 * x) + c9
    return (rl, rr, v, m, eid)


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
    c = b-a
    w_tot = w*c
    rl = w_tot
    ml = -1*w_tot*(a + (c/2))
    if x <= a:
        v = w_tot
        m = rl*x + ml
    elif x <= b:
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
    c = b-a
    w_tot = w*c
    rr = w_tot
    mr = -1*w_tot*(l-b+(c/2))
    if x <= a:
        v = 0
        m = 0
    elif a < x <= b:
        v = -1*w*(x-a)
        m = -1*(w*(x-a)*((x-a)/2))
    else:
        v = -1*w_tot
        m = -1*w_tot*(x-b+(c/2))
    return(rr, mr, v, m)


def cant_right_trap(w1, w2, a, b, l, x):
    c = b-a
    w = 0.5*(w1+w2)*c
    d = a+(((w1+(2*w2))/(3*(w2+w1)))*c)
    s = (w1-w2)/c
    rl = w
    ml = -1*w*d
    if x <= a:
        v = w
        m = (w*x)+ml
    elif a < x < b:
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
    c = b-a
    w = 0.5*(w1+w2)*c
    dl = a+(((w1+(2*w2))/(3*(w2+w1)))*c)
    dr = l-dl
    s = (w1-w2)/c
    rr = w
    mr = -1*w*dr
    if x <= a:
        v = 0
        m = 0
    elif a < x < b:
        cx = x-a
        wx = w1-(s*cx)
        dlx = a+(((w1+(2*wx))/(3*(wx+w1)))*cx)
        drx = x-dlx
        wwx = 0.5*(w1+wx)*cx
        v = (-0.5*((2*w1)-(s*(x-a))))*(x-a)
        m = -1*wwx*drx
    else:
        v = -1*w
        m = -1*w*(x-dl)
    return(rr, mr, v, m)


def three_moment_method(beam_spans, beam_momentofinertia, cant, beam_loads_raw, E, iters, displace):
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


    F = np.zeros((N+1,N+1))
    j=0
    for j in range(1,N):
        F[j,j-1] = beam_spans[j-1]/beam_momentofinertia[j-1]
        F[j,j] = 2*((beam_spans[j-1]/beam_momentofinertia[j-1])+(beam_spans[j]/beam_momentofinertia[j]))
        F[j,j+1] = beam_spans[j]/beam_momentofinertia[j]

    if cant[0]=='L':

        F[0,0] = 1
        F[1,:] = 0
        F[1,1] = 1
        F[N,N] = 1

    elif cant[0]=='R':
        F[0,0] = 1
        F[N,N] = 1
        F[N-1,:] = 0
        F[N-1,N-1] = 1

    elif cant[0]=='B':
        F[0,0] = 1
        F[1,:] = 0
        F[1,1] = 1
        F[N,N] = 1
        F[N-1,:] = 0
        F[N-1,N-1] = 1

    else:
        F[0,0] = 1
        F[N,N] = 1

    delta = np.zeros((N+1,1))
    j=0
    for j in range(1,N): 

        l = j-1
        r = j
        #support settlement delta
        delta[j] = ((-6*a_xl_xr[1,l]*a_xl_xr[0,l])/(beam_spans[l]*beam_momentofinertia[l])+(-6*a_xl_xr[2,r]*a_xl_xr[0,r])/(beam_spans[r]*beam_momentofinertia[r]))+(6*E*(((displace[l]-displace[r])/beam_spans[l])+((displace[r+1]-displace[r])/beam_spans[r])))
        #delta[j] = (-6*a_xl_xr[1,l]*a_xl_xr[0,l])/(beam_spans[l]*beam_momentofinertia[l])+(-6*a_xl_xr[2,r]*a_xl_xr[0,r])/(beam_spans[r]*beam_momentofinertia[r])

    if cant[0]=='L':

        delta[0] = 0
        delta[1] = mr_cant

    elif cant[0]=='R':
        delta[N]=0
        delta[N-1]=ml_cant

    elif cant[0]=='B':
        delta[0] = 0
        delta[1] = mr_cant
        delta[N]=0
        delta[N-1]=ml_cant

    else:
        pass
    #print F
    #print delta
    M = np.dot(inv(F),delta)

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
        #m_diag[:,j] = M[j,0] + sci.integrate.cumtrapz(-1*v_diag[:,j],xs[:,j], initial = 0)
        x=0
        for x in range(0,iters+1):
            m_diag[x,j] = m_diag[x,j]-(((M[j]-M[j+1])/beam_spans[j])*xs[x,j])+M[j]
        s_diag[:,j] = (sci.integrate.cumtrapz(m_diag[:,j],xs[:,j], initial = 0)/(E*beam_momentofinertia[j]))+slope[j,0]
        d_diag[:,j] = sci.integrate.cumtrapz(s_diag[:,j],xs[:,j], initial = 0)
        
        
    #correct d for support displacement
    for j in range(0,N):
        span = beam_spans[j]
        
        #test slope correction
        slope_i = math.atan(-1.0*(displace[j]-displace[j+1])/span)
        s_diag[:,j] = s_diag[:,j] + slope_i
        #slope_i = 0
        
        for i in range(0,len(xs[:,j])):
            delt_i = displace[j] + (((displace[j+1]-displace[j])/span)*xs[i,j])
            d_diag[i,j] = d_diag[i,j] + delt_i

    #Cantilever Diagram Corrections
    if cant[0]=='L' or cant[0] =='B':
        v_diag[:,0] = -1*v_diag_cantL[:,0]
        m_diag[:,0] = m_diag_cantL[:,0]
        s_diag[:,0] = (sci.integrate.cumtrapz(m_diag[::-1,0],xs[:,0], initial = 0)/(E*beam_momentofinertia[0]))-s_diag[0,1]
        d_diag[:,0] = sci.integrate.cumtrapz(s_diag[:,0],xs[:,0], initial = 0)
        s_diag[:,0] = -1*s_diag[::-1,0]
        d_diag[:,0] = d_diag[::-1,0]

    else:
        pass

    if cant[0]=='R' or cant[0] =='B':
        v_diag[:,N-1] = -1*v_diag_cantR[:,N-1]
        m_diag[:,N-1] = m_diag_cantR[:,N-1]
        s_diag[:,N-1] = (sci.integrate.cumtrapz(m_diag[:,N-1],xs[:,N-1], initial = 0)/(E*beam_momentofinertia[N-1]))+s_diag[-1,N-2]
        d_diag[:,N-1] = sci.integrate.cumtrapz(s_diag[:,N-1],xs[:,N-1], initial = 0)

    else:
        pass
    
    #Below not needed with slope correction above for support displacement
    ''''
    #correct cantilever d for support displacement
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
                    delt_i= -1*(xs[i,N-1] + xr)* (displace[N-2]/xl)
                    d_diag[i,N-1]= d_diag[i,N-1] + delt_i
    '''

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
 
    j=0
    for j in range(1,N):
        xs[:,j] = xs[:,j] + sumL[j-1]

    xs = xs/12
    for j in range(0,N):
        v_diag[:,j] = -1*v_diag[:,j]/1000
        m_diag[:,j] = m_diag[:,j]/(12*1000)

    return(xs,v_diag,m_diag,s_diag,d_diag, R, M)


def path_exists(path):
    res_folder_exist = os.path.isdir(path)

    if res_folder_exist is False:

        os.makedirs(path)

    else:
        pass

    return 'Directory created'

class Results_window():
    def __init__(self, master):

        self.master = master
        self.pattern_index = 0
        self.combo_index = 0
        self.customfont = tkFont.Font(family="Helvetica", size=8)
        ## Main Frame
        self.main_frame = tk.Frame(self.master, bd=2, relief='sunken', padx=5,pady=5)
        self.main_frame.pack(anchor=tk.CENTER, padx= 10, pady= 5, fill=tk.BOTH)

        ## results selection Frame
        self.frame_selection = tk.Frame(self.main_frame, padx=5, pady=5)

        self.type_frame_select = tk.Frame(self.frame_selection, padx=1, pady=1)

        self.combo_type = tk.IntVar()
        self.base_type = tk.Radiobutton(self.type_frame_select, text = "Base Loads", variable=self.combo_type, value=1, command=self.base).pack(side=tk.LEFT, anchor=tk.NW, padx= 5, pady= 1)
        self.asd_type = tk.Radiobutton(self.type_frame_select, text = "ASD/Basic", variable=self.combo_type, value=2, command=self.asd).pack(side=tk.LEFT, anchor=tk.NW, padx= 5, pady= 1)
        self.lrfd_type = tk.Radiobutton(self.type_frame_select, text = "LRFD", variable=self.combo_type, value=3, command= self.lrfd).pack(side=tk.LEFT, anchor=tk.NW, padx= 5, pady= 1)
        self.combo_type.set(1)
        self.type_frame_select.pack(side=tk.TOP, anchor=tk.NW, fill=tk.BOTH)
        
        self.combo_pattern_frame = tk.Frame(self.frame_selection)
        self.combo_frame = tk.LabelFrame(self.combo_pattern_frame, text='Combo', relief='sunken', padx=5, pady=5)

        self.asd_combos = Main_window.basic_combos
        self.lrfd_combos = Main_window.lrfd_combos
        self.load_types = ['D', 'Ex', 'Ey', 'F', 'H', 'L', 'Lr', 'R', 'S', 'Wx', 'Wy']
        self.combo_list = tk.Listbox(self.combo_frame, height = 25, width = 50, exportselection=False)
        self.combo_list.pack(side=tk.LEFT)
        self.combo_list.bind("<<ListboxSelect>>",self.combo_click)
        for i in range(len(self.load_types)):
            if Main_window.load_exist[i]==0:
                self.combo_list.insert(tk.END, self.load_types[i]+'- N/A')
            else:
                self.combo_list.insert(tk.END, self.load_types[i])
        self.combo_list.insert(tk.END, 'Support Displacement')
        self.combo_string = 'D'
        self.combo_scrollbar = tk.Scrollbar(self.combo_frame, orient="vertical")
        self.combo_list.config(yscrollcommand=self.combo_scrollbar.set)
        self.combo_scrollbar.config(command=self.combo_list.yview)
        self.combo_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.combo_frame.pack(side=tk.LEFT)
        self.pattern_frame = tk.LabelFrame(self.combo_pattern_frame, text='Load Pattern', relief='sunken', padx=5, pady=5)
        self.pattern_list = tk.Listbox(self.pattern_frame, height = 25, width = 20, exportselection=False)
        self.pattern_list.pack(side = tk.LEFT)
        self.pattern_list.bind("<<ListboxSelect>>",self.pattern_click)
        i=1        
        for pattern in Main_window.pats:
            pat_string = 'Pattern ' + str(i) +' - '
            for y in pattern:
                pat_string = pat_string + str(y) + ','
            pat_string = pat_string[:-1]
            self.pattern_list.insert(tk.END, pat_string)
            i+=1
        self.pattern_list.insert(tk.END, 'Envelope')
        self.pattern_scrollbar = tk.Scrollbar(self.pattern_frame, orient="vertical")
        self.pattern_list.config(yscrollcommand=self.pattern_scrollbar.set)
        self.pattern_scrollbar.config(command=self.pattern_list.yview)
        self.pattern_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.pattern_frame.pack(side = tk.LEFT)
        self.combo_pattern_frame.pack(side = tk.TOP)
        
        self.per_span_res_frame = tk.Frame(self.frame_selection,relief='sunken')
        stations = Main_window.stations
        print stations
        self.span_res_scale = tk.Scale(self.per_span_res_frame, from_=0, to=stations, orient=tk.HORIZONTAL, label = "Location in Span:", length = 300, command=self.span_res_run)
        self.span_res_scale.pack(side=tk.TOP, padx=5, pady=5)
        self.span_res_b_plus = tk.Button(self.per_span_res_frame,text='+', command = self.set_span_res_plus)
        self.span_res_b_plus.pack(side=tk.RIGHT)
        self.span_res_b_minus = tk.Button(self.per_span_res_frame,text='-', command = self.set_span_res_minus)
        self.span_res_b_minus.pack(side=tk.RIGHT)
        self.span_res_label = tk.Label(self.per_span_res_frame, text="per span results here")
        self.span_res_label.pack(side=tk.TOP)
        self.per_span_res_frame.pack(side = tk.TOP)
        
        self.frame_selection.pack(side=tk.LEFT, fill=tk.BOTH)

        ## Chart Frame and selection frames
        self.selection_frame = tk.Frame(self.main_frame, padx=5, pady=5)
        self.res_reaction_frame = tk.Frame(self.selection_frame, padx=5, pady=5)
        self.res_combo = tk.Label(self.res_reaction_frame, text="")
        self.res_combo.pack(side=tk.TOP)
        self.res_R = tk.Label(self.res_reaction_frame, text="")
        self.res_R.pack(side=tk.TOP)
        self.res_M = tk.Label(self.res_reaction_frame, text="")
        self.res_M.pack(side=tk.TOP)
        self.res_reaction_frame.pack(side=tk.TOP)
        self.vmsd_frame = tk.Frame(self.selection_frame, padx=5, pady=5)
        self.vmsd = tk.IntVar()
        self.v = tk.Radiobutton(self.vmsd_frame, text = 'V', variable=self.vmsd, value=1, command= self.vrun)
        self.v.pack(side=tk.LEFT)
        self.m = tk.Radiobutton(self.vmsd_frame, text = 'M', variable=self.vmsd, value=2, command= self.mrun)
        self.m.pack(side=tk.LEFT)
        self.s = tk.Radiobutton(self.vmsd_frame, text = 'S', variable=self.vmsd, value=3, command= self.srun)
        self.s.pack(side=tk.LEFT)
        self.d = tk.Radiobutton(self.vmsd_frame, text = 'D', variable=self.vmsd, value=4, command= self.drun)
        self.d.pack(side=tk.LEFT)
        self.vmsd.set(1)
        self.res_min_max = tk.Label(self.vmsd_frame, text="", justify=tk.LEFT)
        self.res_min_max.pack(side=tk.LEFT)
        self.vmsd_frame.pack(side=tk.TOP)
        self.chart_frame = tk.Frame(self.selection_frame, padx=5, pady=5)

        self.Fig = matplotlib.figure.Figure(figsize=(9,5),dpi=100)
        self.FigSubPlot = self.Fig.add_subplot(111)
        self.FigSubPlot.minorticks_on()
        self.FigSubPlot.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
        self.FigSubPlot.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)

        self.linevmsd = []
        self.lineenvmin = []
        self.linebm = []
        self.clabels = []
        self.clabels_pts = []
        self.x = 0
        self.y = 0
        self.ymax = 0
        for i in range(Main_window.xs.shape[1]):
            self.linebm.append(self.FigSubPlot.plot(Main_window.xs[:,i],Main_window.bm[:,i]))
            self.linevmsd.append(self.FigSubPlot.plot(Main_window.xs[:,i],Main_window.bm[:,i]))
            self.lineenvmin.append(self.FigSubPlot.plot(Main_window.xs[:,i],Main_window.bm[:,i]))
        self.res_points = self.FigSubPlot.plot(0,0,'k+', markersize=15)
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.Fig, master=self.chart_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.chart_frame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.chart_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.selection_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        ## Outside Main Frame
        self.b1 = tk.Button(self.master,text="Close", command=self.close_win)
        self.b1.pack(side=tk.RIGHT, anchor=tk.SW, padx=5, pady=5)
        self.annos_scale = tk.Scale(self.master, from_=3, to=30, orient=tk.HORIZONTAL, label = "Graph Annotations:", length = 200)
        self.annos_scale.pack(side=tk.RIGHT, anchor=tk.SW, padx=5, pady=5)
        
        self.sup_disp_var = tk.IntVar()
        self.ch_sup_disp = tk.Checkbutton(self.master, text=": Remove Support Displacement\nResponse", justify=tk.LEFT, variable=self.sup_disp_var, command=self.sup_disp_click)
        self.ch_sup_disp.pack(side=tk.RIGHT, anchor=tk.SW, padx=5, pady=5)        

        self.label_error = tk.Label(self.master, text='Error Info')
        self.label_error.pack(side=tk.LEFT, anchor=tk.SE, padx=5, pady=5)

    def combo_click(self, *event):
        self.combo_index = self.combo_list.curselection()
        self.combo_index = self.combo_index[0]
        self.combo_string = self.combo_list.get(self.combo_index)
        # self.pattern_index = self.pattern_list.curselection()
        # self.pattern_index = self.pattern_index[0]
        self.pattern_index = 0
        self.pattern_string = self.pattern_list.get(self.pattern_index)
        self.graph_start()
        dia = self.vmsd.get()
        self.graph_start()
        if dia == 1:
            self.vrun()
        elif dia == 2:
            self.mrun()
        elif dia == 3:
            self.srun()
        elif dia == 4:
            self.drun()
        else:
            pass

    def pattern_click(self, *event):
        self.pattern_index = self.pattern_list.curselection()
        self.pattern_index = self.pattern_index[0]
        self.pattern_string = self.pattern_list.get(self.pattern_index)
        dia = self.vmsd.get()
        self.graph_start()
        if dia == 1:
            self.vrun()
        elif dia == 2:
            self.mrun()
        elif dia == 3:
            self.srun()
        elif dia == 4:
            self.drun()
        else:
            pass
            
    def sup_disp_click(self, *event):
        dia = self.vmsd.get()
        self.graph_start()
        if dia == 1:
            self.vrun()
        elif dia == 2:
            self.mrun()
        elif dia == 3:
            self.srun()
        elif dia == 4:
            self.drun()
        else:
            pass              

    def asd(self):
        self.combo_list.delete(0,tk.END)
        for i in range(0,len(self.asd_combos)):
            combo = self.asd_combos[i] + ' - '
            for y in range(0,len(self.load_types)):
                if Main_window.basic_factors[i][y] == 0.0 or Main_window.load_exist[y]==0:
                    pass
                else:        
                    combo = combo + ' {0:.2f}*{1} +'.format(Main_window.basic_factors[i][y],self.load_types[y])
            self.combo_list.insert(tk.END, combo[:-1])
        self.combo_list.insert(tk.END, 'ASD/Basic Envelope')
        self.s.config(state='normal')
        self.d.config(state='normal')
        self.combo_list.selection_set(0)
        self.pattern_list.selection_set(0)

    def lrfd(self):
        self.combo_list.delete(0,tk.END)
        for i in range(0,len(self.lrfd_combos)):
            combo = self.lrfd_combos[i] + ' - '
            for y in range(0,len(self.load_types)):
                if Main_window.LRFD_factors[i][y] == 0.0 or Main_window.load_exist[y]==0:
                    pass
                else:
                    combo = combo + ' {0:.2f}*{1} +'.format(Main_window.LRFD_factors[i][y],self.load_types[y])
            self.combo_list.insert(tk.END, combo[:-1])
        self.combo_list.insert(tk.END, 'LRFD Envelope')
        self.s.config(state='disabled')
        self.d.config(state='disabled')
        self.combo_list.selection_set(0)
        self.pattern_list.selection_set(0)

    def base(self):
        self.combo_list.delete(0,tk.END)
        for i in range(len(self.load_types)):
            if Main_window.load_exist[i]==0:
                self.combo_list.insert(tk.END, self.load_types[i]+'- N/A')
            else:
                self.combo_list.insert(tk.END, self.load_types[i])
        self.combo_list.insert(tk.END, 'Support Displacement')
        self.s.config(state='normal')
        self.d.config(state='normal')
        self.combo_list.selection_set(0)
        self.pattern_list.selection_set(0)
 
    def save_graph(self):
        self.Fig.savefig(self.path, dpi=150)

    def close_win(self):
        self.master.destroy()

    def graph_start(self, *event):

        combo = self.combo_type.get()
        R= 0
        M= 0
        Rmin= []
        Mmin= []
        #Main_window.LRFD_factors
        #Main_window.lrfd_combos
        #Main_window.basic_factors
        #Main_window.basic_combos

        if combo == 2:
            asd_combo = self.combo_index
            if asd_combo in range(0, len(self.asd_combos)):
                if self.pattern_index in range(0,len(Main_window.pats)):
                    R = Main_window.basic_r[asd_combo][1][self.pattern_index] - (self.sup_disp_var.get() * Main_window.displace_initial_results[4])
                    M = Main_window.basic_m_support[asd_combo][1][self.pattern_index] - (self.sup_disp_var.get()* Main_window.displace_initial_results[5])
                else:
                    R = Main_window.basic_r_env_max[asd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[4])
                    M = Main_window.basic_m_support_env_max[asd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[5])
                    Rmin = Main_window.basic_r_env_min[asd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[4])
                    Mmin = Main_window.basic_m_support_env_min[asd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[5])
            else:
                R = Main_window.asd_Rmax_print - (self.sup_disp_var.get() * Main_window.displace_initial_results[4])
                M = Main_window.asd_Mmax_print - (self.sup_disp_var.get() * Main_window.displace_initial_results[5])
                Rmin = Main_window.asd_Rmin_print - (self.sup_disp_var.get() * Main_window.displace_initial_results[4])
                Mmin = Main_window.asd_Mmin_print - (self.sup_disp_var.get() * Main_window.displace_initial_results[5])

        elif combo == 3:
            lrfd_combo = self.combo_index
            if lrfd_combo in range(0,len(self.lrfd_combos)):
                if self.pattern_index in range(0,len(Main_window.pats)):
                    R = Main_window.lrfd_r[lrfd_combo][1][self.pattern_index] - (self.sup_disp_var.get() * Main_window.displace_initial_results[4])
                    M = Main_window.lrfd_m_support[lrfd_combo][1][self.pattern_index] - (self.sup_disp_var.get() * Main_window.displace_initial_results[5])
                else:
                    R = Main_window.lrfd_r_env_max[lrfd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[4])
                    M = Main_window.lrfd_m_support_env_max[lrfd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[5])
                    Rmin = Main_window.lrfd_r_env_min[lrfd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[4])
                    Mmin = Main_window.lrfd_m_support_env_min[lrfd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[5])
            else:
                R = Main_window.lrfd_Rmax_print - (self.sup_disp_var.get() * Main_window.displace_initial_results[4])
                M = Main_window.lrfd_Mmax_print - (self.sup_disp_var.get() * Main_window.displace_initial_results[5])
                Rmin = Main_window.lrfd_Rmin_print - (self.sup_disp_var.get() * Main_window.displace_initial_results[4])
                Mmin = Main_window.lrfd_Mmin_print - (self.sup_disp_var.get() * Main_window.displace_initial_results[5])

        elif combo == 1:
            basic_combo = self.combo_index
            if basic_combo in range(5,9):
                if self.pattern_index in range(0,len(Main_window.pats)):
                    R = Main_window.load_results[basic_combo][6][1][self.pattern_index]+ Main_window.load_results[basic_combo][6][0]
                    M = Main_window.load_results[basic_combo][7][1][self.pattern_index]+ Main_window.load_results[basic_combo][7][0]
                else:
                    R = np.maximum.reduce(Main_window.load_results[basic_combo][6][1])+ Main_window.load_results[basic_combo][6][0]
                    M = np.maximum.reduce(Main_window.load_results[basic_combo][7][1])+ Main_window.load_results[basic_combo][7][0]
                    Rmin = np.minimum.reduce(Main_window.load_results[basic_combo][6][1])+ Main_window.load_results[basic_combo][6][0]
                    Mmin = np.minimum.reduce(Main_window.load_results[basic_combo][7][1])+ Main_window.load_results[basic_combo][7][0]
            else:
                if basic_combo == 11:
                    R = Main_window.displace_initial_results[4]
                    M = Main_window.displace_initial_results[5]
                else:
                    R = Main_window.load_results[basic_combo][6]
                    M = Main_window.load_results[basic_combo][7]
        else:
            pass
        
        if len(Rmin) == 0:
            r_string = 'Reactions (kips) : '
            for reaction in R:
                r_string = r_string + ' {0:.2f}  '.format(reaction[0]/1000)
            m_string = 'Moments at Supports (ft-kips) : '
            for moment in M:
                m_string = m_string + ' {0:.2f}  '.format(moment[0]/(1000*12))
        else:
            r_string = 'Max Reactions (kips) : '
            for reaction in R:
                r_string = r_string + ' {0:.2f}  '.format(reaction[0]/1000)
            r_string = r_string + '\nMin Reactions (kips) : '
            for reaction in Rmin:
                r_string = r_string + ' {0:.2f}  '.format(reaction[0]/1000)
            m_string = 'Max Moments at Supports (ft-kips) : '
            for moment in M:
                m_string = m_string + ' {0:.2f}  '.format(moment[0]/(1000*12))
            m_string = m_string + '\nMin Moments at Supports (ft-kips) : '
            for moment in Mmin:
                m_string = m_string + ' {0:.2f}  '.format(moment[0]/(1000*12))
    
        self.res_R.configure(text=r_string)
        self.res_M.configure(text=m_string)
        self.res_combo.configure(text=self.combo_string)

    def span_res_run(self, *event):
        dia = self.vmsd.get()
        station = self.span_res_scale.get()
        text_res = ''
        x=[]
        y=[]
        for j in range(self.x.shape[1]):
            if self.combo_string == 'LRFD Envelope' or self.combo_string == 'ASD/Basic Envelope' or self.pattern_string == 'Envelope':
                if j==0:
                    if dia == 1:
                        text_res = text_res + 'Span {2}: Vmax = {0:.3f} kips @ {1} ft\n'.format(self.y[station,j],self.x[station,j], j+1)
                        text_res = text_res + 'Span {2}: Vmin = {0:.3f} kips @ {1} ft\n'.format(self.ymin[station,j],self.x[station,j], j+1)
                    elif dia == 2:
                        text_res = text_res + 'Span {2}: Mmax = {0:.3f} ft-kips @ {1} ft\n'.format(self.y[station,j],self.x[station,j], j+1)
                        text_res = text_res + 'Span {2}: Mmin = {0:.3f} ft-kips @ {1} ft\n'.format(self.ymin[station,j],self.x[station,j], j+1)
                    elif dia == 3:
                        text_res = text_res + 'Span {2}: Smax = {0:.5f} rads @ {1} ft\n'.format(self.y[station,j],self.x[station,j], j+1)
                        text_res = text_res + 'Span {2}: Smin = {0:.5f} rads @ {1} ft\n'.format(self.ymin[station,j],self.x[station,j], j+1)
                    elif dia == 4:
                        text_res = text_res + 'Span {2}: Delta max = {0:.4f} in @ {1} ft\n'.format(self.y[station,j],self.x[station,j], j+1)
                        text_res = text_res + 'Span {2}: Delta min = {0:.4f} in @ {1} ft\n'.format(self.ymin[station,j],self.x[station,j], j+1)
                    else:
                        pass
                else:
                    if dia == 1:
                        text_res = text_res + 'Span {2}: Vmax = {0:.3f} kips @ {1} ft ({3} ft)\n'.format(self.y[station,j],self.x[station,j], j+1,self.x[station,j]-self.x[-1,j-1])
                        text_res = text_res + 'Span {2}: Vmin = {0:.3f} kips @ {1} ft ({3} ft)\n'.format(self.ymin[station,j],self.x[station,j], j+1,self.x[station,j]-self.x[-1,j-1])
                    elif dia == 2:
                        text_res = text_res + 'Span {2}: Mmax = {0:.3f} ft-kips @ {1} ft ({3} ft)\n'.format(self.y[station,j],self.x[station,j], j+1,self.x[station,j]-self.x[-1,j-1])
                        text_res = text_res + 'Span {2}: Mmin = {0:.3f} ft-kips @ {1} ft ({3} ft)\n'.format(self.ymin[station,j],self.x[station,j], j+1,self.x[station,j]-self.x[-1,j-1])
                    elif dia == 3:
                        text_res = text_res + 'Span {2}: Smax = {0:.5f} rads @ {1} ft ({3} ft)\n'.format(self.y[station,j],self.x[station,j], j+1,self.x[station,j]-self.x[-1,j-1])
                        text_res = text_res + 'Span {2}: Smin = {0:.5f} rads @ {1} ft ({3} ft)\n'.format(self.ymin[station,j],self.x[station,j], j+1,self.x[station,j]-self.x[-1,j-1])
                    elif dia == 4:
                        text_res = text_res + 'Span {2}: Delta max = {0:.4f} in @ {1} ft ({3} ft)\n'.format(self.y[station,j],self.x[station,j], j+1,self.x[station,j]-self.x[-1,j-1])
                        text_res = text_res + 'Span {2}: Delta min = {0:.4f} in @ {1} ft ({3} ft)\n'.format(self.ymin[station,j],self.x[station,j], j+1,self.x[station,j]-self.x[-1,j-1])
                    else:
                        pass
                x.append(self.x[station,j])
                y.append(self.y[station,j])
                x.append(self.x[station,j])
                y.append(self.ymin[station,j])
            else:
                if j==0:
                    if dia == 1:
                        text_res = text_res + 'Span {2}: V = {0:.3f} kips @ {1} ft\n'.format(self.y[station,j],self.x[station,j], j+1)
                    elif dia == 2:
                        text_res = text_res + 'Span {2}: M = {0:.3f} ft-kips @ {1} ft\n'.format(self.y[station,j],self.x[station,j], j+1)
                    elif dia == 3:
                        text_res = text_res + 'Span {2}: S = {0:.5f} rads @ {1} ft\n'.format(self.y[station,j],self.x[station,j], j+1)
                    elif dia == 4:
                        text_res = text_res + 'Span {2}: Delta = {0:.4f} in @ {1} ft\n'.format(self.y[station,j],self.x[station,j], j+1)
                    else:
                        pass
                else:
                    if dia == 1:
                        text_res = text_res + 'Span {2}: V = {0:.3f} kips @ {1} ft ({3} ft)\n'.format(self.y[station,j],self.x[station,j], j+1,self.x[station,j]-self.x[-1,j-1])
                    elif dia == 2:
                        text_res = text_res + 'Span {2}: M = {0:.3f} ft-kips @ {1} ft ({3} ft)\n'.format(self.y[station,j],self.x[station,j], j+1,self.x[station,j]-self.x[-1,j-1])
                    elif dia == 3:
                        text_res = text_res + 'Span {2}: S = {0:.5f} rads @ {1} ft ({3} ft)\n'.format(self.y[station,j],self.x[station,j], j+1,self.x[station,j]-self.x[-1,j-1])
                    elif dia == 4:
                        text_res = text_res + 'Span {2}: Delta = {0:.4f} in @ {1} ft ({3} ft)\n'.format(self.y[station,j],self.x[station,j], j+1,self.x[station,j]-self.x[-1,j-1])
                    else:
                        pass
                x.append(self.x[station,j])
                y.append(self.y[station,j])
            
        self.span_res_label.config(text = text_res)
        
        self.res_points[0].set_xdata(x)
        self.res_points[0].set_ydata(y)
        self.canvas.draw()

    def set_span_res_plus(self):
        station = self.span_res_scale.get()
        self.span_res_scale.set(station+1)
        
    def set_span_res_minus(self):
        station = self.span_res_scale.get()
        self.span_res_scale.set(station-1)
        
    def refreshFigure(self, x, y, yenv, dia, dec):
        self.x = x
        self.y = y
        self.ymin = yenv
        combo = self.combo_type.get()
        for i in range(x.shape[1]):
            self.linevmsd[i][0].set_ydata(y[:,i])
            self.lineenvmin[i][0].set_ydata(yenv[:,i])

        for i in range(len(self.clabels)):
            self.clabels[i].remove()

        del self.clabels[:]


        for i in range(len(self.clabels_pts)):
            self.clabels_pts[i][0].remove()

        del self.clabels_pts[:]

        fsi = 8
        msi = 2
        num_annos = self.annos_scale.get()
        for j in range(x.shape[1]):
             for z in range(0,num_annos):
                 if z==0:
                     k=0
                 else:
                     if z*int(Main_window.stations/(num_annos-1)) >= Main_window.stations:
                         k= Main_window.stations
                     else:
                         k=z*int(Main_window.stations/(num_annos-1))

                 if dec == 3:
                    self.clabels.append(self.FigSubPlot.annotate('{0:.3f}'.format(y[k,j]),xy=(x[k,j],y[k,j]), xytext=(2.5,1), textcoords='offset points',fontsize=fsi))
                    if self.combo_string == 'LRFD Envelope' or self.combo_string == 'ASD/Basic Envelope' or self.pattern_string == 'Envelope':
                        self.clabels.append(self.FigSubPlot.annotate('{0:.3f}'.format(yenv[k,j]),xy=(x[k,j],yenv[k,j]), xytext=(2.5,1), textcoords='offset points',fontsize=fsi))
                    else:
                        pass
                 elif dec ==4:
                    self.clabels.append(self.FigSubPlot.annotate('{0:.4f}'.format(y[k,j]),xy=(x[k,j],y[k,j]), xytext=(2.5,1), textcoords='offset points',fontsize=fsi))
                    if self.combo_string == 'LRFD Envelope' or self.combo_string == 'ASD/Basic Envelope' or self.pattern_string == 'Envelope':
                        self.clabels.append(self.FigSubPlot.annotate('{0:.4f}'.format(yenv[k,j]),xy=(x[k,j],yenv[k,j]), xytext=(2.5,1), textcoords='offset points',fontsize=fsi))
                    else:
                        pass
                 else:
                    self.clabels.append(self.FigSubPlot.annotate('{0:.2f}'.format(y[k,j]),xy=(x[k,j],y[k,j]), xytext=(2.5,1), textcoords='offset points',fontsize=fsi))
                    if self.combo_string == 'LRFD Envelope' or self.combo_string == 'ASD/Basic Envelope' or self.pattern_string == 'Envelope':
                        self.clabels.append(self.FigSubPlot.annotate('{0:.2f}'.format(yenv[k,j]),xy=(x[k,j],yenv[k,j]), xytext=(2.5,1), textcoords='offset points',fontsize=fsi))
                    else:
                        pass
                 self.clabels_pts.append(self.FigSubPlot.plot(x[k,j],y[k,j], 'ko', markersize=msi))
                 if self.combo_string == 'LRFD Envelope' or self.combo_string == 'ASD/Basic Envelope' or self.pattern_string == 'Envelope':
                    self.clabels_pts.append(self.FigSubPlot.plot(x[k,j],yenv[k,j], 'ko', markersize=msi))
                 else:
                    pass
        ax = self.canvas.figure.axes[0]
        ax.set_xlim(x.min()+(x.min()*0.125), x.max()+(x.max()*0.125))
        if self.combo_string == 'LRFD Envelope' or self.combo_string == 'ASD/Basic Envelope' or self.pattern_string == 'Envelope':
            ax.set_ylim(yenv.min()+(yenv.min()*0.125), y.max()+(y.max()*0.125))
        else:
            ax.set_ylim(y.min()+(y.min()*0.125), y.max()+(y.max()*0.125))
        self.FigSubPlot.set_xlabel('L (ft)')
        self.FigSubPlot.set_ylabel(dia)
        self.FigSubPlot.set_title(Main_window.calc_label+'\n'+self.combo_string+'\n'+self.pattern_string)
        self.canvas.draw()
        self.span_res_run()

    def vrun(self):
        combo = self.combo_type.get()
        dia = 'Shear (Kips)'

        if combo == 2:

            asd_combo = self.combo_index
            
            if asd_combo in range(0, len(self.asd_combos)):
                if self.pattern_index in range(0,len(Main_window.pats)):
                    y = Main_window.basic_v[asd_combo][1][self.pattern_index] - (self.sup_disp_var.get() * Main_window.displace_initial_results[0])
                    ymin = Main_window.bm
                    x = Main_window.xs
                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. V (kips): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                    line2 = '\n  Min. V (kips): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.2f}  '.format(y[:,i].min())
                        
                    self.res_min_max.configure(text='   Max. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),y.min())+line1+line2)
                    dia = dia+'\nMax. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),y.min())
                else:
                    y = Main_window.basic_v_env_max[asd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[0])
                    ymin = Main_window.basic_v_env_min[asd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[0])
                    x = Main_window.xs
                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. V (kips): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                    line2 = '\n  Min. V (kips): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.2f}  '.format(ymin[:,i].min())
                        
                    self.res_min_max.configure(text='   Max. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),ymin.min())+line1+line2)
                    dia = dia+'\nMax. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),ymin.min())
            else:
                y = Main_window.asd_v_max_diag - (self.sup_disp_var.get() * Main_window.displace_initial_results[0])
                ymin = Main_window.asd_v_min_diag - (self.sup_disp_var.get() * Main_window.displace_initial_results[0])
                x = Main_window.xs
                n = len(y[0])
                line1 = '\n  Per Span Max/Min:\n  Max. V (kips): '
                for i in range(0,n):
                    line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                line2 = '\n  Min. V (kips): '
                for i in range(0,n):
                    line2 = line2 + '{0:.2f}  '.format(ymin[:,i].min())
                    
                self.res_min_max.configure(text='   Max. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),ymin.min())+line1+line2)
                dia = dia+'\nMax. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),ymin.min())           

            self.refreshFigure(x,y,ymin,dia,2)
        
        elif combo ==3:

            lrfd_combo = self.combo_index
            
            if lrfd_combo in range(0, len(self.lrfd_combos)):
                if self.pattern_index in range(0,len(Main_window.pats)):
                    y = Main_window.lrfd_v[lrfd_combo][1][self.pattern_index] - (self.sup_disp_var.get() * Main_window.displace_initial_results[0])
                    ymin = Main_window.bm
                    x = Main_window.xs
                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. V (kips): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                    line2 = '\n  Min. V (kips): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.2f}  '.format(y[:,i].min())
                        
                    self.res_min_max.configure(text='   Max. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),y.min())+line1+line2)
                    dia = dia+'\nMax. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),y.min())
                else:
                    y = Main_window.lrfd_v_env_max[lrfd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[0])
                    ymin = Main_window.lrfd_v_env_min[lrfd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[0])
                    x = Main_window.xs
                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. V (kips): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                    line2 = '\n  Min. V (kips): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.2f}  '.format(ymin[:,i].min())
                        
                    self.res_min_max.configure(text='   Max. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),ymin.min())+line1+line2)
                    dia = dia+'\nMax. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),ymin.min())
            else:
                y = Main_window.lrfd_v_max_diag - (self.sup_disp_var.get() * Main_window.displace_initial_results[0])
                ymin = Main_window.lrfd_v_min_diag - (self.sup_disp_var.get() * Main_window.displace_initial_results[0])
                x = Main_window.xs
                n = len(y[0])
                line1 = '\n  Per Span Max/Min:\n  Max. V (kips): '
                for i in range(0,n):
                    line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                line2 = '\n  Min. V (kips): '
                for i in range(0,n):
                    line2 = line2 + '{0:.2f}  '.format(ymin[:,i].min())
                    
                self.res_min_max.configure(text='   Max. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),ymin.min())+line1+line2)
                dia = dia+'\nMax. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),ymin.min())           

            self.refreshFigure(x,y,ymin,dia,2)
        elif combo ==1:
            basic_combo = self.combo_index

            if self.combo_index in range(5,9):
                if self.pattern_index in range(0,len(Main_window.pats)):
                    y = Main_window.load_results[basic_combo][2][1][self.pattern_index]
                    if len(Main_window.load_results[basic_combo][2][0]) <= 1:
                        pass
                    else:
                        y = y + Main_window.load_results[basic_combo][2][0]
                    ymin = Main_window.bm
                    x = Main_window.xs
                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. V (kips): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                    line2 = '\n  Min. V (kips): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.2f}  '.format(y[:,i].min())
                        
                    self.res_min_max.configure(text='   Max. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),y.min())+line1+line2)
                    dia = dia+'\nMax. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),y.min())
                else:
                    y = np.maximum.reduce(Main_window.load_results[basic_combo][2][1])
                    ymin = np.minimum.reduce(Main_window.load_results[basic_combo][2][1])
                    if len(Main_window.load_results[basic_combo][2][0]) <= 1:
                        pass
                    else:
                        y = y + Main_window.load_results[basic_combo][2][0]
                        ymin = ymin + Main_window.load_results[basic_combo][2][0]
                    x = Main_window.xs
                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. V (kips): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                    line2 = '\n  Min. V (kips): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.2f}  '.format(ymin[:,i].min())
                        
                    self.res_min_max.configure(text='   Max. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),ymin.min())+line1+line2)
                    dia = dia+'\nMax. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),ymin.min())                             
            else:
                if basic_combo == 11:
                    y = Main_window.displace_initial_results[0]
                    ymin = Main_window.bm
                    x = Main_window.xs

                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. V (kips): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                    line2 = '\n  Min. V (kips): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.2f}  '.format(y[:,i].min())
                        
                    self.res_min_max.configure(text='   Max. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),y.min())+line1+line2)
                    dia = dia+'\nMax. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),y.min())
                else:
                    y = Main_window.load_results[basic_combo][2]
                    ymin = Main_window.bm
                    x = Main_window.xs

                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. V (kips): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                    line2 = '\n  Min. V (kips): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.2f}  '.format(y[:,i].min())
                        
                    self.res_min_max.configure(text='   Max. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),y.min())+line1+line2)
                    dia = dia+'\nMax. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),y.min())
            
            self.refreshFigure(x,y,ymin,dia,2)

        else:
            pass

    def mrun(self):
        combo = self.combo_type.get()
        dia = 'Moment (Ft-Kips)'
        if combo == 2:

            asd_combo = self.combo_index
            if asd_combo in range(0, len(self.asd_combos)):
                if self.pattern_index in range(0,len(Main_window.pats)):
                    y = Main_window.basic_m[asd_combo][1][self.pattern_index] - (self.sup_disp_var.get() * Main_window.displace_initial_results[1])
                    ymin = Main_window.bm
                    x = Main_window.xs

                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. M (ft-kips): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                    line2 = '\n  Min. M (ft-kips): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.2f}  '.format(y[:,i].min())
                    
                    self.res_min_max.configure(text='   Max. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),y.min())+line1+line2)
                    dia = dia + '\nMax. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),y.min())
                else:
                    y = Main_window.basic_m_env_max[asd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[1])
                    ymin = Main_window.basic_m_env_min[asd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[1])
                    x = Main_window.xs

                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. M (ft-kips): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                    line2 = '\n  Min. M (ft-kips): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.2f}  '.format(ymin[:,i].min())
                    
                    self.res_min_max.configure(text='   Max. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),ymin.min())+line1+line2)
                    dia = dia + '\nMax. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),ymin.min())
            else:
                y = Main_window.asd_m_max_diag - (self.sup_disp_var.get() * Main_window.displace_initial_results[1])
                ymin = Main_window.asd_m_min_diag - (self.sup_disp_var.get() * Main_window.displace_initial_results[1])
                x = Main_window.xs

                n = len(y[0])
                line1 = '\n  Per Span Max/Min:\n  Max. M (ft-kips): '
                for i in range(0,n):
                    line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                line2 = '\n  Min. M (ft-kips): '
                for i in range(0,n):
                    line2 = line2 + '{0:.2f}  '.format(ymin[:,i].min())
                
                self.res_min_max.configure(text='   Max. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),ymin.min())+line1+line2)
                dia = dia + '\nMax. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),ymin.min())
            self.refreshFigure(x,y,ymin,dia,2)
        elif combo ==3:
            lrfd_combo = self.combo_index
            if lrfd_combo in range(0, len(self.lrfd_combos)):
                if self.pattern_index in range(0,len(Main_window.pats)):
                    y = Main_window.lrfd_m[lrfd_combo][1][self.pattern_index] - (self.sup_disp_var.get() * Main_window.displace_initial_results[1])
                    ymin = Main_window.bm
                    x = Main_window.xs

                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. M (ft-kips): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                    line2 = '\n  Min. M (ft-kips): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.2f}  '.format(y[:,i].min())
                    
                    self.res_min_max.configure(text='   Max. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),y.min())+line1+line2)
                    
                    dia = dia + '\nMax. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),y.min())
                else:
                    y = Main_window.lrfd_m_env_max[lrfd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[1])
                    ymin = Main_window.lrfd_m_env_min[lrfd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[1])
                    x = Main_window.xs

                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. M (ft-kips): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                    line2 = '\n  Min. M (ft-kips): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.2f}  '.format(ymin[:,i].min())
                    
                    self.res_min_max.configure(text='   Max. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),ymin.min())+line1+line2)
                    
                    dia = dia + '\nMax. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),ymin.min())
            else:
                y = Main_window.lrfd_m_max_diag - (self.sup_disp_var.get() * Main_window.displace_initial_results[1])
                ymin = Main_window.lrfd_m_min_diag - (self.sup_disp_var.get() * Main_window.displace_initial_results[1])
                x = Main_window.xs

                n = len(y[0])
                line1 = '\n  Per Span Max/Min:\n  Max. M (ft-kips): '
                for i in range(0,n):
                    line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                line2 = '\n  Min. M (ft-kips): '
                for i in range(0,n):
                    line2 = line2 + '{0:.2f}  '.format(ymin[:,i].min())
                
                self.res_min_max.configure(text='   Max. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),ymin.min())+line1+line2)
                
                dia = dia + '\nMax. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),ymin.min())

            self.refreshFigure(x,y,ymin,dia,2)
        elif combo ==1:
            basic_combo = self.combo_index
            
            if basic_combo in range(5,9):
                if self.pattern_index in range(0,len(Main_window.pats)):
                    y = Main_window.load_results[basic_combo][3][1][self.pattern_index]
                    if len(Main_window.load_results[basic_combo][3][0]) <= 1:
                        pass
                    else:
                        y = y + Main_window.load_results[basic_combo][3][0]
                    ymin = Main_window.bm
                    x = Main_window.xs
                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. M (ft-kips): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                    line2 = '\n  Min. M (ft-kips): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.2f}  '.format(y[:,i].min())
                    
                    self.res_min_max.configure(text='   Max. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),y.min())+line1+line2)
                    dia = dia + '\nMax. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),y.min())
                else:
                    y = np.maximum.reduce(Main_window.load_results[basic_combo][3][1])
                    ymin = np.minimum.reduce(Main_window.load_results[basic_combo][3][1])
                    if len(Main_window.load_results[basic_combo][3][0]) <= 1:
                        pass
                    else:
                        y = y + Main_window.load_results[basic_combo][3][0]
                        ymin = ymin + Main_window.load_results[basic_combo][3][0]
                    x = Main_window.xs
                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. M (ft-kips): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                    line2 = '\n  Min. M (ft-kips): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.2f}  '.format(ymin[:,i].min())
                    
                    self.res_min_max.configure(text='   Max. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),ymin.min())+line1+line2)
                    dia = dia + '\nMax. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),ymin.min())          
            else:
                if basic_combo == 11:
                    y = Main_window.displace_initial_results[1]
                    ymin = Main_window.bm
                    x = Main_window.xs

                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. M (ft-kips): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                    line2 = '\n  Min. M (ft-kips): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.2f}  '.format(y[:,i].min())
                        
                    self.res_min_max.configure(text='   Max. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),y.min())+line1+line2)
                    dia = dia+'\nMax. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),y.min())
                else:
                    y = Main_window.load_results[basic_combo][3]
                    ymin = Main_window.bm
                    x = Main_window.xs

                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. M (ft-kips): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.2f}  '.format(y[:,i].max())
                    line2 = '\n  Min. M (ft-kips): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.2f}  '.format(y[:,i].min())
                    
                    self.res_min_max.configure(text='   Max. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),y.min())+line1+line2)
                    dia = dia + '\nMax. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),y.min())
            self.refreshFigure(x,y,ymin,dia,2)
        else:
            pass

    def srun(self):
        combo = self.combo_type.get()
        dia ='Slope (Rad)'
        if combo == 2:

            asd_combo = self.combo_index
            if asd_combo in range(0, len(self.asd_combos)):
                if self.pattern_index in range(0,len(Main_window.pats)):
                    y = Main_window.basic_s[asd_combo][1][self.pattern_index] - (self.sup_disp_var.get() * Main_window.displace_initial_results[2])
                    ymin = Main_window.bm
                    x = Main_window.xs

                    self.res_min_max.configure(text='   Max. S: {0:.4f} rad  Min. S: {1:.4f} rad'.format(y.max(),y.min()))
                    dia = dia+'\nMax. S: {0:.4f} rad  Min. S: {1:.4f} rad'.format(y.max(),y.min())
                else:
                    y = Main_window.basic_s_env_max[asd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[2])
                    ymin = Main_window.basic_s_env_min[asd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[2])
                    x = Main_window.xs

                    self.res_min_max.configure(text='   Max. S: {0:.4f} rad  Min. S: {1:.4f} rad'.format(y.max(),ymin.min()))
                    dia = dia+'\nMax. S: {0:.4f} rad  Min. S: {1:.4f} rad'.format(y.max(),ymin.min())
            else:
                y = Main_window.asd_s_max_diag - (self.sup_disp_var.get() * Main_window.displace_initial_results[2])
                ymin = Main_window.asd_s_min_diag - (self.sup_disp_var.get() * Main_window.displace_initial_results[2])
                x = Main_window.xs

                self.res_min_max.configure(text='   Max. S: {0:.4f} rad  Min. S: {1:.4f} rad'.format(y.max(),ymin.min()))
                dia = dia+'\nMax. S: {0:.4f} rad  Min. S: {1:.4f} rad'.format(y.max(),ymin.min())           
            self.refreshFigure(x,y,ymin,dia,4)
        elif combo ==3:
            pass
        elif combo ==1:
            basic_combo = self.combo_index
            if basic_combo in range(5,9):
                if self.pattern_index in range(0,len(Main_window.pats)):
                    y = Main_window.load_results[basic_combo][4][1][self.pattern_index]
                    if len(Main_window.load_results[basic_combo][4][0]) <= 1:
                        pass
                    else:
                        y = y + Main_window.load_results[basic_combo][4][0]
                    ymin = Main_window.bm
                    x = Main_window.xs
                    self.res_min_max.configure(text='   Max. S: {0:.4f} rad  Min. S: {1:.4f} rad'.format(y.max(),y.min()))
                    dia = dia+'\nMax. S: {0:.4f} rad  Min. S: {1:.4f} rad'.format(y.max(),y.min())
                else:
                    y = np.maximum.reduce(Main_window.load_results[basic_combo][4][1])
                    ymin = np.minimum.reduce(Main_window.load_results[basic_combo][4][1])
                    if len(Main_window.load_results[basic_combo][5][0]) <= 1:
                        pass
                    else:
                        y = y + Main_window.load_results[basic_combo][4][0]
                        ymin = ymin + Main_window.load_results[basic_combo][4][0]
                    x = Main_window.xs
                    self.res_min_max.configure(text='   Max. S: {0:.4f} rad  Min. S: {1:.4f} rad'.format(y.max(),ymin.min()))
                    dia = dia+'\nMax. S: {0:.4f} rad  Min. S: {1:.4f} rad'.format(y.max(),ymin.min())                             
            else:
                if basic_combo == 11:
                    y = Main_window.displace_initial_results[2]
                    ymin = Main_window.bm
                    x = Main_window.xs
                    self.res_min_max.configure(text='   Max. S: {0:.4f} rad  Min. S: {1:.4f} rad'.format(y.max(),y.min()))
                    dia = dia+'\nMax. S: {0:.4f} rad  Min. S: {1:.4f} rad'.format(y.max(),y.min())
                    
                else:
                    y = Main_window.load_results[basic_combo][4]
                    ymin = Main_window.bm
                    x = Main_window.xs

                    self.res_min_max.configure(text='   Max. S: {0:.4f} rad  Min. S: {1:.4f} rad'.format(y.max(),y.min()))
                    dia = dia+'\nMax. S: {0:.4f} rad  Min. S: {1:.4f} rad'.format(y.max(),y.min())
            self.refreshFigure(x,y,ymin,dia,4)
        else:
            pass

    def drun(self):
        combo = self.combo_type.get()
        dia = 'Deflection (in)'
        if combo == 2:

            asd_combo = self.combo_index
            if asd_combo in range(0, len(self.asd_combos)):
                if self.pattern_index in range(0,len(Main_window.pats)):
                    y = Main_window.basic_d[asd_combo][1][self.pattern_index] - (self.sup_disp_var.get() * Main_window.displace_initial_results[3])
                    ymin = Main_window.bm
                    x = Main_window.xs
                    
                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. D (in): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.4f}  '.format(y[:,i].max())
                    line2 = '\n  Min. D (in): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.4f}  '.format(y[:,i].min())
                    line2 = line2 + '\n  Goal L/240 (in): '
                    for i in range(0,n):
                        line2 = line2 + '+/-{0:.4f}  '.format(Main_window.total_deflection_goal[i])
                    self.res_min_max.configure(text='   Max. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),y.min())+line1+line2)
                    dia = dia+'\nMax. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),y.min())
                else:
                    y = Main_window.basic_d_env_max[asd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[3])
                    ymin = Main_window.basic_d_env_min[asd_combo] - (self.sup_disp_var.get() * Main_window.displace_initial_results[3])
                    x = Main_window.xs
                    
                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. D (in): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.4f}  '.format(y[:,i].max())
                    line2 = '\n  Min. D (in): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.4f}  '.format(ymin[:,i].min())
                    line2 = line2 + '\n  Goal L/240 (in): '
                    for i in range(0,n):
                        line2 = line2 + '+/-{0:.4f}  '.format(Main_window.total_deflection_goal[i])
                    self.res_min_max.configure(text='   Max. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),ymin.min())+line1+line2)
                    dia = dia+'\nMax. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),ymin.min())
            else:
                y = Main_window.asd_d_max_diag - (self.sup_disp_var.get() * Main_window.displace_initial_results[3])
                ymin = Main_window.asd_d_min_diag - (self.sup_disp_var.get() * Main_window.displace_initial_results[3])
                x = Main_window.xs
                
                n = len(y[0])
                line1 = '\n  Per Span Max/Min:\n  Max. D (in): '
                for i in range(0,n):
                    line1 = line1 + '{0:.4f}  '.format(y[:,i].max())
                line2 = '\n  Min. D (in): '
                for i in range(0,n):
                    line2 = line2 + '{0:.4f}  '.format(ymin[:,i].min())
                line2 = line2 + '\n  Goal L/240 (in): '
                for i in range(0,n):
                    line2 = line2 + '+/-{0:.4f}  '.format(Main_window.total_deflection_goal[i])
                self.res_min_max.configure(text='   Max. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),ymin.min())+line1+line2)
                dia = dia+'\nMax. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),ymin.min())
            self.refreshFigure(x,y,ymin,dia,3)
        elif combo ==3:
            pass
        elif combo ==1:
            basic_combo = self.combo_index
            
            if basic_combo in range(5,9):
                if self.pattern_index in range(0,len(Main_window.pats)):
                    y = Main_window.load_results[basic_combo][5][1][self.pattern_index]
                    if len(Main_window.load_results[basic_combo][5][0]) <= 1:
                        pass
                    else:
                        y = y + Main_window.load_results[basic_combo][5][0]
                    ymin = Main_window.bm
                    x = Main_window.xs
                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. D (in): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.4f}  '.format(y[:,i].max())
                    line2 = '\n  Min. D (in): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.4f}  '.format(y[:,i].min())
                    line2 = line2 + '\n  Goal L/360 (in): '
                    for i in range(0,n):
                        line2 = line2 + '+/-{0:.4f}  '.format(Main_window.live_deflection_goal[i])
                    self.res_min_max.configure(text='   Max. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),y.min())+line1+line2)
                    dia = dia+'\nMax. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),y.min())
                else:
                    y = np.maximum.reduce(Main_window.load_results[basic_combo][5][1])
                    ymin = np.minimum.reduce(Main_window.load_results[basic_combo][5][1])
                    if len(Main_window.load_results[basic_combo][5][0]) <= 1:
                        pass
                    else:
                        y = y + Main_window.load_results[basic_combo][5][0]
                        ymin = ymin + Main_window.load_results[basic_combo][5][0]
                    x = Main_window.xs
                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. D (in): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.4f}  '.format(y[:,i].max())
                    line2 = '\n  Min. D (in): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.4f}  '.format(ymin[:,i].min())
                    line2 = line2 + '\n  Goal L/360 (in): '
                    for i in range(0,n):
                        line2 = line2 + '+/-{0:.4f}  '.format(Main_window.live_deflection_goal[i])
                    self.res_min_max.configure(text='   Max. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),ymin.min())+line1+line2)
                    dia = dia+'\nMax. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),ymin.min())
            else:
                if basic_combo == 11:
                    y = Main_window.displace_initial_results[3]
                    ymin = Main_window.bm
                    x = Main_window.xs
                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. D (in): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.4f}  '.format(y[:,i].max())
                    line2 = '\n  Min. D (in): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.4f}  '.format(y[:,i].min())
                    self.res_min_max.configure(text='   Max. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),y.min())+line1+line2)
                    dia = dia+'\nMax. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),y.min())
                
                else:
                    y = Main_window.load_results[basic_combo][5]
                    ymin = Main_window.bm
                    x = Main_window.xs

                    n = len(y[0])
                    line1 = '\n  Per Span Max/Min:\n  Max. D (in): '
                    for i in range(0,n):
                        line1 = line1 + '{0:.4f}  '.format(y[:,i].max())
                    line2 = '\n  Min. D (in): '
                    for i in range(0,n):
                        line2 = line2 + '{0:.4f}  '.format(y[:,i].min())
                    self.res_min_max.configure(text='   Max. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),y.min())+line1+line2)
                    dia = dia+'\nMax. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),y.min())
            self.refreshFigure(x,y,ymin,dia,3)
        else:
            pass

class Main_window:

    def __init__(self, master):
        self.master = master
        self.menubar = tk.Menu(self.master)
        self.menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label = "File", menu=self.menu)
        self.menu.add_command(label="Open", command=self.open_calc)
        self.menu.add_separator()
        self.menu.add_command(label="Save Inputs", command=self.print_ins)
        self.menu.add_command(label="Run", state="disabled", command= self.run_file)
        self.menu.add_command(label="Results", state="disabled", command= self.res_window)
        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=self.quit_app)
        
        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            self.master.tk.call(master, "config", "-menu", self.menubar)

        self.main_frame = tk.Frame(self.master, bd=2, relief='sunken', padx=10,pady=20)
        self.main_frame.pack(anchor='c', padx= 10, pady= 20)
        
        self.bminfo = tk.StringVar()
        self.bminfol = tk.Label(self.main_frame, text="Calculation Label : ")
        self.bminfol.grid(row=0,column=0, pady=10, sticky="E")
        self.e_bminfo = tk.Entry(self.main_frame,textvariable=self.bminfo)
        self.e_bminfo.grid(row=0,column=1, pady=10)

        self.E = tk.StringVar()
        self.El = tk.Label(self.main_frame, text="E (ksi) : \nGlobal = All Spans", justify=tk.RIGHT)
        self.El.grid(row=1,column=0, pady=10, sticky="E")
        self.e_E = tk.Entry(self.main_frame,textvariable=self.E)
        self.e_E.grid(row=1,column=1, pady=10)

        self.span = tk.StringVar()
        self.spanl = tk.Label(self.main_frame, text="Span (ft) : ")
        self.spanl.grid(row=2,column=0, sticky="E")
        self.e_span = tk.Entry(self.main_frame,textvariable=self.span)
        self.e_span.grid(row=2,column=1)

        self.I = tk.StringVar()
        self.Il = tk.Label(self.main_frame, text="I (In^4) : ")
        self.Il.grid(row=3,column=0, sticky="E")
        self.e_I = tk.Entry(self.main_frame,textvariable=self.I)
        self.e_I.grid(row=3,column=1)

        self.cantl = tk.Label(self.main_frame, text="Cantilever L,R,B,N : ")
        self.cantl.grid(row=4,column=0, sticky="E")
        self.cant_in = tk.StringVar()
        self.cant_in.set('N')
        self.e_cant = tk.OptionMenu(self.main_frame,self.cant_in, 'L','R','B','N')
        self.e_cant.grid (row=4,column=1, padx= 10, sticky=tk.W)

        self.p_w1 = tk.StringVar()
        self.p_w1l = tk.Label(self.main_frame, text="P or w1 (kips/klf) : ")
        self.p_w1l.grid(row=5,column=0, sticky="E")
        self.e_p = tk.Entry(self.main_frame,textvariable=self.p_w1)
        self.e_p.grid(row=5,column=1)

        self.w2 = tk.StringVar()
        self.w2l = tk.Label(self.main_frame, text="w2 (klf) : ")
        self.w2l.grid(row=6,column=0, sticky="E")
        self.e_w2 = tk.Entry(self.main_frame,textvariable=self.w2)
        self.e_w2.grid(row=6,column=1)

        self.a = tk.StringVar()
        self.al = tk.Label(self.main_frame, text="a (ft) : ")
        self.al.grid(row=7,column=0, sticky="E")
        self.e_a = tk.Entry(self.main_frame,textvariable=self.a)
        self.e_a.grid(row=7,column=1)

        self.b =tk. StringVar()
        self.bl = tk.Label(self.main_frame, text="b (ft) : ")
        self.bl.grid(row=8,column=0, sticky="E")
        self.e_b = tk.Entry(self.main_frame,textvariable=self.b)
        self.e_b.grid(row=8,column=1)

        self.load_type = tk.StringVar()
        self.load_type.set('POINT')
        self.applied_loads_allow = ['POINT','UDL','TRAP']
        self.ltl = tk.Label(self.main_frame, text="Load Type (POINT, UDL, TRAP) : ")
        self.ltl.grid(row=9,column=0, sticky="E")
        self.e_load_type = tk.OptionMenu(self.main_frame,self.load_type,'POINT','UDL','TRAP')
        self.e_load_type.grid(row=9,column=1, padx= 10, sticky=tk.W)

        self.load_span = tk.IntVar()
        self.lsl = tk.Label(self.main_frame, text="Load in span : ")
        self.lsl.grid(row=10,column=0, sticky="E")
        self.e_load_span = tk.OptionMenu(self.main_frame, self.load_span, 1)
        self.e_load_span.grid(row=10,column=1, padx= 10, sticky=tk.W)

        self.load_types = ['D', 'Ex', 'Ey', 'F', 'H', 'L', 'Lr', 'R', 'S', 'Wx', 'Wy']
        self.load_kind = tk.StringVar()
        self.load_kind.set('D')
        self.lkl = tk.Label(self.main_frame, text='Load Type: ' + ','.join(self.load_types))
        self.lkl.grid(row=11,column=0, sticky="E")
        self.e_load_kind = tk.OptionMenu(self.main_frame, self.load_kind, 'D', 'Ex', 'Ey', 'F', 'H', 'L', 'Lr', 'R', 'S', 'Wx', 'Wy')
        self.e_load_kind.grid(row=11, column=1, padx= 10, sticky=tk.W)
        self.l_pattern_var = tk.IntVar()
        self.ch_l_pattern = tk.Checkbutton(self.main_frame, text=": Pattern Load\n(Only impacts L,Lr,R, and S)", justify=tk.LEFT, variable=self.l_pattern_var)
        self.ch_l_pattern.grid(row=12, column=1, padx= 10, sticky=tk.W)
        self.f_lrfd_frame = tk.Frame(self.main_frame)
        self.fi_lrfd = tk.StringVar()
        self.fi_lrfd.set('1.00')
        self.fi_lrfd_label = tk.Label(self.f_lrfd_frame, text='F1')
        self.fi_lrfd_label.pack(side=tk.LEFT)
        self.e_fi_lrfd = tk.OptionMenu(self.f_lrfd_frame, self.fi_lrfd, '1.00', '0.5')
        self.e_fi_lrfd.pack(side=tk.LEFT)
        self.fy_lrfd = tk.StringVar()
        self.fy_lrfd.set('0.7')
        self.fy_lrfd_label = tk.Label(self.f_lrfd_frame, text='F2')
        self.fy_lrfd_label.pack(side=tk.LEFT)
        self.e_fy_lrfd = tk.OptionMenu(self.f_lrfd_frame, self.fy_lrfd, '0.7', '0.2')
        self.e_fy_lrfd.pack(side=tk.LEFT)
        self.f_lrfd_frame.grid(row=12, column=0, padx= 10, sticky=tk.W)
        
        self.point_gif = PhotoImage(file="point.gif")
        self.point_key = tk.Label(self.main_frame,image=self.point_gif)
        self.point_key.point_gif = self.point_gif
        self.point_key.grid(row=13, column = 0, padx=5, pady=5)

        self.udl_gif = PhotoImage(file="udl.gif")
        self.udl_key = tk.Label(self.main_frame,image=self.udl_gif)
        self.udl_key.udl_gif = self.udl_gif
        self.udl_key.grid(row=13, column = 1, padx=5, pady=5)

        self.spans = tk.Label(self.main_frame, text="Spans (ft)")
        self.I_label = tk.Label(self.main_frame,text="I (in^4)")
        self.loads = tk.Label(self.main_frame, text="Loads")
        self.spans.grid(row=0, column=4)
        self.loads.grid(row=0, column=11)
        self.I_label.grid(row=0, column=6)

        self.lb_spans = tk.Listbox(self.main_frame,height = 10, width = 10)
        self.lb_spans.grid(row=1, column=4, columnspan=2, rowspan = 9, sticky='WENS', padx=5, pady=5)
        self.lb_spans.bind("<<ListboxSelect>>",self.span_click)

        self.lb_I = tk.Listbox(self.main_frame,height = 10, width = 10)
        self.lb_I.grid(row=1, column=6, columnspan=2, rowspan = 9, sticky='WENS', padx=5, pady=5)

        self.lb_loads = tk.Listbox(self.main_frame,height = 10, width = 20)
        self.lb_loads.grid(row=1, column=9, columnspan = 10, rowspan = 9,sticky='WENS', padx=5, pady=5 )
        self.lb_loads.bind("<<ListboxSelect>>",self.load_click)
        
        self.support_displace_label = tk.Label(self.main_frame, text="Support Displacements (in.):\n(+ is upward)")
        self.support_displace_label.grid(row=11, column =3, padx=5, pady=5)
        self.displace_widget = []
        
        self.b1 = tk.Button(self.main_frame,text="Close", command=self.quit_app)
        self.b1.grid(row=13, column=19, padx=5, pady=5)
        self.bprint = tk.Button(self.main_frame,text="Save Inputs", command=self.print_ins)
        self.bprint.grid(row=13, column =18, padx=5, pady=5)
        self.b_span_add = tk.Button(self.main_frame,text="Add Span/I +", command=self.add_span)
        self.b_span_min = tk.Button(self.main_frame,text="Remove Span/I -", command=self.remove_span)
        self.b_span_change = tk.Button(self.main_frame, text="Change Selected Span", command=self.change_span)
        self.b_span_change.configure(state="disabled")
        self.b_load_add = tk.Button(self.main_frame,text="Add Load +", command=self.add_load)
        self.b_load_addtoall = tk.Button(self.main_frame,text="Add UDL to All", command=self.add_udl_to_all)
        self.b_load_addtraptoall = tk.Button(self.main_frame,text="Add Full Length Trap", command=self.add_full_length_trap)
        self.b_load_min = tk.Button(self.main_frame,text="Remove Load -", command=self.remove_load)
        self.b_load_change = tk.Button(self.main_frame, text="Change Selected Load", command=self.change_load)
        self.b_load_change.configure(state="disabled")
        self.b_span_add.grid(row=1, column=3, padx=5, pady=5)
        self.b_span_min.grid(row=2, column=3, padx=5, pady=5)
        self.b_span_change.grid(row=3, column=3, padx=5, pady=5)
        self.b_load_add.grid(row=5, column=3, padx=5, pady=5)
        self.b_load_min.grid(row=6, column=3, padx=5, pady=5)
        self.b_load_change.grid(row=7, column=3, padx=5, pady=5)
        self.b_load_addtoall.grid(row=8, column=3, padx=5, pady=5)
        self.b_load_addtraptoall.grid(row=9, column=3, padx=5, pady=5)

        self.brun = tk.Button(self.main_frame, text="Run", command= self.run_file)
        self.brun.configure(state="disabled", bg='red')
        self.brun.grid(row = 13, column=17, padx=5, pady=5)

        self.bresults = tk.Button(self.main_frame, text="Results", command= self.res_window)
        self.bresults.grid(row = 13, column=16, padx=5, pady=5)
        self.bresults.configure(state="disabled", bg='red')

        self.ins_validate()
        self.license_display()
    
    def license_display(self, *event):
        license_string = ("Copyright (c) 2019, Donald N. Bockoven III\n"
                            "All rights reserved.\n\n"
                            "THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\""
                            " AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE"
                            " IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE"
                            " DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE"
                            " FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL"
                            " DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR"
                            " SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER"
                            " CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,"
                            " OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE"
                            " OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n\n"
                            "https://github.com/buddyd16/Structural-Engineering/blob/master/LICENSE"
                            )
        tkMessageBox.showerror("License Information",license_string)
        self.master.focus_force()
        
    def _reset_option_menu(self, spans):
        '''reset the values in the option menu
        if index is given, set the value of the menu to
        the option at the given index
        '''
        menu = self.e_load_span["menu"]
        menu.delete(0, "end")
        if spans==1:
            menu.add_command(spans)
        else:
            for span in spans:
                menu.add_command(label=span,
                                command=lambda value=span:
                                    self.load_span.set(value))

    def quit_app(self):
        self.master.destroy()
        self.master.quit()

    def open_calc(self):
        filename = tkFileDialog.askopenfilename()
        calc_file = open(filename,'r')

        calc_data = calc_file.readlines()

        calc_file.close()

        beam_spans = []
        beam_momentofinertia=[]
        beam_elasticmodulus=[]
        beam_loads_raw = []
        cant = []
        sup_disp = []

        i=0
        for line in calc_data:
            if i == 0:
                beam_label = line.rstrip('\n')
            elif i<6:
                p = line.split(',')
                for items in p:
                    if i==1:
                        beam_spans.append(items.rstrip('\n'))
                    elif i==2:
                        beam_momentofinertia.append(items.rstrip('\n'))
                    elif i==3:
                        beam_elasticmodulus.append(items.rstrip('\n'))
                    elif i==4:
                        cant.append(items.rstrip('\n'))
                    elif i==5:
                        sup_disp.append(items.rstrip('\n'))
                    else:
                        pass
            elif i>7:
                beam_loads_raw.append(line.rstrip('\n'))
            else:
                pass

            i+=1

        del beam_spans[0]
        del beam_momentofinertia[0]
        del beam_elasticmodulus[0]
        del cant[0]

        self.bminfo.set(beam_label)
        self.cant_in.set(cant[0])
        self.E.set(beam_elasticmodulus[0])

        self.lb_spans.delete(0,tk.END)
        self.lb_I.delete(0,tk.END)
        for i in range(len(beam_spans)):
            self.lb_spans.insert(tk.END,beam_spans[i])
            self.lb_I.insert(tk.END,beam_momentofinertia[i])

        self.lb_loads.delete(0,tk.END)
        for load in beam_loads_raw:
            self.lb_loads.insert(tk.END,load)
        self._reset_option_menu(range(1,self.lb_spans.size()+1))
        self.ins_validate()
        for widget in self.displace_widget:
            widget.destroy()
        del self.displace_widget[:]

        for i in range(0,self.lb_spans.size()+1):
            self.displace_widget.append(tk.Entry(self.main_frame,width = 5, justify=tk.CENTER))
            self.displace_widget[i].insert(tk.END, sup_disp[i])
            self.displace_widget[i].grid(row=11,column=5+i, padx= 2)
        
        if self.cant_in.get() == 'L' or self.cant_in.get() == 'B':
            self.displace_widget[0].configure(state="disabled")
            self.displace_widget[0].delete(0,tk.END)
            self.displace_widget[0].insert(tk.END, '0.0')
        else:
            self.displace_widget[0].configure(state="normal")
        
        if self.cant_in.get() == 'R' or self.cant_in.get() == 'B':
            self.displace_widget[-1].configure(state="disabled")
            self.displace_widget[-1].delete(0,tk.END)
            self.displace_widget[-1].insert(tk.END, '0.0')
        else:
            self.displace_widget[-1].configure(state="normal")
        self.brun.configure(state="normal", bg='yellow')

    def res_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.res_app = Results_window(self.newWindow)

    def ins_validate(self):
        if self.lb_spans.size() == 0 or self.lb_I.size()==0 or self.lb_loads.size()==0:
            self.bprint.configure(state ="disabled", bg='red')
        else:
            self.bprint.configure(state="normal", bg='yellow')

    def print_ins(self):
        if self.lb_spans.size() == 0 or self.lb_I.size()==0 or self.lb_loads.size()==0:
            pass
        else:
            p_loads = self.lb_loads.get(0,tk.END)
            p_spans = self.lb_spans.get(0,tk.END)
            p_I = self.lb_I.get(0,tk.END)
            p_E = self.e_E.get()

            label = self.e_bminfo.get()
            Main_window.calc_label = label
            path = os.path.join(os.path.expanduser('~'),'Desktop','RESULTS', label)

            path_exists(path)
            sup_disp = '' 
            for widget in self.displace_widget:            
                sup_disp = sup_disp + '{0},'.format(widget.get())
            sup_disp = sup_disp[:-1]

            file = open(os.path.join(path,label + '_00_beam_info.txt'),'w')
            file.write(label + '\n')
            file.write('L_ft')
            for line in p_spans:
                file.write(','+line)
            file.write('\nI_in4')
            for line in p_I:
                file.write(','+line)
            file.write('\nE_ksi,'+p_E+'\ncant,'+self.cant_in.get()+'\n'+sup_disp+'\n**Loads**\n''p1(kips or klf)'',''p2(kips or klf)'',a,b,''POINT,UDL,TRAP'' **Do Not Delete This Line, Caps Matter for Load Type**,span\n')
            for line in p_loads:
                file.write(line + '\n')
            file.close()

            self.brun.configure(state="normal", bg='yellow')
            self.bprint.configure(state="normal", bg='green')
            self.menu.entryconfig(3, state="normal")
    def load_input_validation(self):
        if self.e_p.get()=='' or self.e_w2.get()=='' or self.e_a.get()=='' or self.e_b.get()=='' or self.load_type.get()=='' or self.load_span.get() =='' or self.load_kind.get()=='':
            return 0
        else:
            if self.load_type.get() in self.applied_loads_allow and self.load_kind.get() in self.load_types:
                a = float(self.e_a.get())
                b = float(self.e_b.get())
                span = self.load_span.get()
                span_l = float(self.lb_spans.get(span-1))
                w1 = float(self.e_p.get())
                w2 = float(self.e_w2.get())
                if w2 == 0:
                    trap_reversal_check = 1
                else:
                    trap_reversal_check = w1/w2
                
                if a < 0 or a > span_l or b<a or b> span_l or trap_reversal_check < 0:
                    return 0
                else:
                    return 1
    def add_load(self):
        load_test = self.load_input_validation()
        
        if load_test == 0:
            pass
        else:
            load = '{0},{1},{2},{3},{4},{5},{6},{7}'.format(self.e_p.get(),self.e_w2.get(),self.e_a.get(),self.e_b.get(),self.load_type.get(),self.load_span.get(),self.load_kind.get(),self.l_pattern_var.get())
            self.lb_loads.insert(tk.END,load)

        self.ins_validate()
        
    def add_udl_to_all(self):
        spans = self.lb_spans.size()
        a = self.e_a.get()
        b = self.e_b.get()
        w1 = float(self.e_p.get())
        w2 = float(self.e_w2.get())
        
        if w1 == 0:
            pass
        else:
            if w2 != w1:
                pass
            elif spans == 0:
                pass
            else:
                i=0
                for i in range(0,spans):
                    span_l = self.lb_spans.get(i)
                    b = self.e_b.get()
                    if float(a) < 0 or float(a) > float(span_l) or float(b)<float(a):
                        pass
                        self.ins_validate()
                    if float(b) > float(span_l):
                        b = span_l
                        load = '{0},{1},{2},{3},{4},{5},{6},{7}'.format(self.e_p.get(),self.e_w2.get(),self.e_a.get(),b,'UDL',i+1,self.load_kind.get(),self.l_pattern_var.get())
                        self.lb_loads.insert(tk.END,load)
                        self.ins_validate()
                    else:
                        load = '{0},{1},{2},{3},{4},{5},{6},{7}'.format(self.e_p.get(),self.e_w2.get(),self.e_a.get(),self.e_b.get(),'UDL',i+1,self.load_kind.get(),self.l_pattern_var.get())
                        self.lb_loads.insert(tk.END,load)
                        self.ins_validate()
    def add_full_length_trap(self):
        num_spans = self.lb_spans.size()
        w1 = float(self.e_p.get())
        w2 = float(self.e_w2.get())
        span_l = []
        if w1==0 and w2==0 or num_spans == 0 :
            pass
        else:
            if w2 != 0 and w1/w2 < 0:
                runme = 0
            else:
                runme = 1
            
            if runme == 1:
                spans_l_string = self.lb_spans.get(0,tk.END)
                
                for line in spans_l_string:
                    span_l.append(float(line))
                    
                overall_length = sum(span_l)
                slope = (w1-w2)/overall_length
                
                for i in range(0,len(span_l)):
                    if i == 0:
                        w1_out = w1
                        a=0
                        b=span_l[i]
                        w2_out = w1-(slope*span_l[i])
                    else:
                        w1_out = w2_out
                        a=0
                        b=span_l[i]
                        w2_out = w1_out-(slope*span_l[i])
                        if i == len(span_l)-1 and w2 == 0:
                            w2_out = 0
                        else:
                            w2_out = w2_out
                    load = '{0},{1},{2},{3},{4},{5},{6},{7}'.format(w1_out,w2_out,a,b,'TRAP',i+1,self.load_kind.get(),self.l_pattern_var.get())
                    self.lb_loads.insert(tk.END,load)
                    self.ins_validate()
            else:
                pass
            
    def remove_load(self):
        self.lb_loads.delete(tk.END)

        self.ins_validate()

    def load_click(self,*event):
        if self.lb_loads.size()==0:
            pass
        else:
            self.b_load_change.configure(state="normal")
            self.selected_load = self.lb_loads.get(self.lb_loads.curselection()[0]).split(',')
            self.load_change_index = self.lb_loads.curselection()[0]

            self.p_w1.set(self.selected_load[0])
            self.w2.set(self.selected_load[1])
            self.a.set(self.selected_load[2])
            self.b.set(self.selected_load[3])
            self.load_type.set(self.selected_load[4])
            self.load_span.set(self.selected_load[5])
            self.load_kind.set(self.selected_load[6])
            self.l_pattern_var.set(self.selected_load[7])

    def change_load(self):
        if self.e_p.get()=='' or self.e_w2.get()=='' or self.e_a.get()=='' or self.e_b.get()=='' or self.load_type.get()=='' or self.load_span.get() =='' or self.load_kind.get()=='':
            pass
        else:
            if self.load_type.get() in self.applied_loads_allow and self.load_kind.get() in self.load_types:
                load = '{0},{1},{2},{3},{4},{5},{6},{7}'.format(self.e_p.get(),self.e_w2.get(),self.e_a.get(),self.e_b.get(),self.load_type.get(),self.load_span.get(),self.load_kind.get(),self.l_pattern_var.get())
                self.lb_loads.delete(self.load_change_index)
                self.lb_loads.insert(self.load_change_index,load)
                self.b_load_change.configure(state="disabled")
            else:
                pass

        self.ins_validate()

    def add_span(self):
        for widget in self.displace_widget:
            widget.destroy()
        del self.displace_widget[:]
        if self.e_span.get()=='' or self.e_I.get()=='':
            pass
        else:
            self.lb_spans.insert(tk.END,self.e_span.get())
            self.lb_I.insert(tk.END,self.e_I.get())
        if self.e_span.get()=='' or self.lb_spans.size()==1:
            self.load_span.set(1)
            self._reset_option_menu([1])
        else:
            self._reset_option_menu(range(1,self.lb_spans.size()+1))
        
        for i in range(0,self.lb_spans.size()+1):
            self.displace_widget.append(tk.Entry(self.main_frame,width = 5, justify=tk.CENTER))
            self.displace_widget[i].insert(tk.END, '0.0')
            self.displace_widget[i].grid(row=11,column=5+i, padx= 2)
        
        if self.cant_in.get() == 'L' or self.cant_in.get() == 'B':
            self.displace_widget[0].configure(state="disabled")
            self.displace_widget[0].delete(0,tk.END)
            self.displace_widget[0].insert(tk.END, '0.0')
        else:
            self.displace_widget[0].configure(state="normal")
        
        if self.cant_in.get() == 'R' or self.cant_in.get() == 'B':
            self.displace_widget[-1].configure(state="disabled")
            self.displace_widget[-1].delete(0,tk.END)
            self.displace_widget[-1].insert(tk.END, '0.0')
        else:
            self.displace_widget[-1].configure(state="normal")
        
            
        self.ins_validate()

    def remove_span(self):
        self.lb_spans.delete(tk.END)
        self.lb_I.delete(tk.END)
        if self.e_span.get()=='' or self.lb_spans.size()==1:
            self.load_span.set(1)
            self._reset_option_menu([1])
            if self.e_span.get()=='':
                for widget in self.displace_widget:
                    widget.destroy()
                del self.displace_widget[:]
            else:
                self.displace_widget[-1].destroy()
                del self.displace_widget[-1]
        else:
            self._reset_option_menu(range(1,self.lb_spans.size()+1))
            self.displace_widget[-1].destroy()
            del self.displace_widget[-1]

        self.ins_validate()

    def span_click(self,*event):
        if self.lb_spans.size()==0:
            pass
        else:
            self.b_span_change.configure(state="normal")
            self.span_change_index = self.lb_spans.curselection()[0]
            self.selected_span = self.lb_spans.get(self.span_change_index)
            self.selected_I = self.lb_I.get(self.span_change_index)

            self.span.set(self.selected_span)
            self.I.set(self.selected_I)

    def change_span(self):
        if self.e_span.get()=='' or self.e_I.get()=='':
            pass
        else:
            self.lb_spans.delete(self.span_change_index)
            self.lb_I.delete(self.span_change_index)

            self.lb_spans.insert(self.span_change_index,self.e_span.get())
            self.lb_I.insert(self.span_change_index,self.e_I.get())
            self.b_span_change.configure(state="disable")

        self.ins_validate()

    def run_file(self):
        bmlabel = self.e_bminfo.get()
        #--------------
        # Initial Inputs From Text File created by print_ins function
        #--------------
        path = os.path.join(os.path.expanduser('~'),'Desktop','RESULTS', bmlabel)

        path_exists(path)

        f1=open(os.path.join(path,bmlabel+'_00_beam_info.txt'),'r')

        beam_info_raw = f1.readlines()

        f1.close()

        beam_spans = []
        beam_momentofinertia=[]
        beam_elasticmodulus=[]
        beam_loads_raw = []
        dead = []
        seismic_x = []
        seismic_y = []
        fluid = []
        earth = []
        live = []
        live_roof = []
        rain = []
        snow = []
        wind_x = []
        wind_y = []
        cant = []
        Main_window.load_exist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


        i=0
        for line in beam_info_raw:

            if i<5:
                p = line.split(',')
                for items in p:
                    if i==1:
                        beam_spans.append(items.rstrip('\n'))
                    elif i==2:
                        beam_momentofinertia.append(items.rstrip('\n'))
                    elif i==3:
                        beam_elasticmodulus.append(items.rstrip('\n'))
                    elif i==4:
                        cant.append(items.rstrip('\n'))
                    else:
                        pass
            elif i>7:
                p = line.split(',')
                holder=[]
                if p[4]=="POINT":
                    holder.append(float(p[0])*1000)
                    holder.append(float(p[1])*1000)
                elif p[4]=="M":
                    holder.append(float(p[0])*1000*12)
                    holder.append(float(p[1])*1000*12)
                else:
                    holder.append(float(p[0])*1000/12)
                    holder.append(float(p[1])*1000/12)


                holder.append(float(p[2])*12)
                #holder.append((float(p[3])-float(p[2]))*12)
                holder.append((float(p[3]))*12)
                holder.append(p[4])
                holder.append(int(p[5].replace('\n',''))-1)
                holder.append(int(p[7].replace('\n','')))
                # load_types = ['D', 'Ex', 'Ey', 'F', 'H', 'L', 'Lr', 'R', 'S', 'Wx', 'Wy']
                if p[6].replace('\n','') == 'D':
                    dead.append(holder)
                    Main_window.load_exist[0]=1
                elif p[6].replace('\n','') == 'Ex':
                    seismic_x.append(holder)
                    Main_window.load_exist[1]=1
                elif p[6].replace('\n','') == 'Ey':
                    seismic_y.append(holder)
                    Main_window.load_exist[2]=1
                elif p[6].replace('\n','') == 'F':
                    fluid.append(holder)
                    Main_window.load_exist[3]=1
                elif p[6].replace('\n','') == 'H':
                    earth.append(holder)
                    Main_window.load_exist[4]=1
                elif p[6].replace('\n','') == 'L':
                    live.append(holder)
                    Main_window.load_exist[5]=1
                elif p[6].replace('\n','') == 'Lr':
                    live_roof.append(holder)
                    Main_window.load_exist[6]=1
                elif p[6].replace('\n','') == 'R':
                    rain.append(holder)
                    Main_window.load_exist[7]=1
                elif p[6].replace('\n','') == 'S':
                    snow.append(holder)
                    Main_window.load_exist[8]=1
                elif p[6].replace('\n','') == 'Wx':
                    wind_x.append(holder)
                    Main_window.load_exist[9]=1
                elif p[6].replace('\n','') == 'Wy':
                    wind_y.append(holder)
                    Main_window.load_exist[10]=1
                else:
                    print 'no load kind'
            else:
                pass

            i+=1
        del beam_spans[0]
        del beam_momentofinertia[0]
        del beam_elasticmodulus[0]
        del cant[0]
        i=0
        loads = [([0]*8) for i in range(11)]
        load_types = ['D', 'Ex', 'Ey', 'F', 'H', 'L', 'Lr', 'R', 'S', 'Wx', 'Wy']
        applied_loads = [dead, seismic_x, seismic_y, fluid, earth, live, live_roof, rain, snow, wind_x, wind_y]

        i=0
        for i in range(0, 11):
            loads[i][0] = load_types[i]
            loads[i][1] = applied_loads[i]

        beam_spans = [float(x)*12 for x in beam_spans]
        beam_momentofinertia=[float(x) for x in beam_momentofinertia]
        beam_elasticmodulus=[float(x)*1000 for x in beam_elasticmodulus]

        E = beam_elasticmodulus[0]
        #iters = max(int(round(max(beam_spans)/1.0)),500)
        iters = 25
        Main_window.stations = iters
        N = len(beam_spans)
        displace_loads = [0]*(N+1)
        displace_initial = []
        Main_window.displace_initial_results = [0]*6
        for widget in self.displace_widget:
            displace_initial.append(float(widget.get()))
        patterns = load_pattern(N)
        Main_window.pats = patterns
        Main_window.live_deflection_goal = []
        Main_window.total_deflection_goal = []
        pattern_loads = []
        no_pattern_loads = []       
        for y in range(0,4):
            pattern_loads.append([])
            no_pattern_loads.append([])
        for y in range(0,4):
            for i in range(0,N):
                pattern_loads[y].append([])

        pattern_loads_apply = [[0]*len(patterns),[0]*len(patterns),[0]*len(patterns),[0]*len(patterns)]

        
        for i in range(5,9):
            for applied in loads[i][1]:
                index = applied[5]
                if applied[6] == 1:
                    if applied == '':
                        pattern_loads[i-5][index].append(0)
                    else:
                        pattern_loads[i-5][index].append(applied)
                else:
                    no_pattern_loads[i-5].append(applied)
                    
            loads[i][1] = [no_pattern_loads[i-5],pattern_loads[i-5]]
            for y in range(2,8):
                loads[i][y] = [[0],[0]*len(patterns)]

            for z in range(0,len(patterns)):

                pat_holder = []
                for a in range(0,len(patterns[z])):
                    if i == 8:
                        
                        if patterns[z][a] == 1:
                            if len(loads[i][1][1][a]) == 0:
                                pat_holder.append([0.00,0.00,0.00,0.00,'POINT',0,0])
                            else:
                                for load in loads[i][1][1][a]:
                                    pat_holder.append(load)
                        else:
                            if len(loads[i][1][1][a]) == 0:
                                pat_holder.append([0.00,0.00,0.00,0.00,'POINT',0,0])
                            else:
                                for load in loads[i][1][1][a]:
                                    pat_holder.append([load[0]*0.5,load[1]*0.5,load[2],load[3],load[4],load[5],load[6]])
                    else:
                        if patterns[z][a] == 1:
                            if len(loads[i][1][1][a]) == 0:
                                pat_holder.append([0.00,0.00,0.00,0.00,'POINT',0,0])
                            else:
                                for load in loads[i][1][1][a]:
                                    pat_holder.append(load)
                        else:
                            pass
                pattern_loads_apply[i-5][z] = pat_holder
        for span in beam_spans:
            Main_window.live_deflection_goal.append(span/360)
            Main_window.total_deflection_goal.append(span/240)
            
        startt = time.time()
        print 'Perform analysis for all load types defined....'
        for i in range(0,11):
            if i in range(5,9):
                if len(loads[i][1][0]) == 0:
                    pass
                else:
                    Main_window.xs,loads[i][2][0],loads[i][3][0],loads[i][4][0],loads[i][5][0], loads[i][6][0], loads[i][7][0] = three_moment_method(beam_spans, beam_momentofinertia, cant, loads[i][1][0], E, iters, displace_loads)
                
                if len(loads[i][1][1]) == 0:
                    for y in range(0,len(patterns)):
                        loads[i][2][1][y] = 0.0
                        loads[i][3][1][y] = 0.0
                        loads[i][4][1][y] = 0.0
                        loads[i][5][1][y] = 0.0
                        loads[i][6][1][y] = 0.0
                        loads[i][7][1][y] = 0.0
                else:
                    for y in range(0,len(patterns)):
                        Main_window.xs, loads[i][2][1][y], loads[i][3][1][y],  loads[i][4][1][y], loads[i][5][1][y], loads[i][6][1][y], loads[i][7][1][y] = three_moment_method(beam_spans, beam_momentofinertia, cant, pattern_loads_apply[i-5][y], E, iters, displace_loads)
                        
            elif len(loads[i][1]) == 0:
                pass
            
            else:
                Main_window.xs,loads[i][2],loads[i][3],loads[i][4],loads[i][5], loads[i][6], loads[i][7] = three_moment_method(beam_spans, beam_momentofinertia, cant, loads[i][1], E, iters, displace_loads)
        
        #solve for prescribed displacements
        Main_window.xs,Main_window.displace_initial_results[0],Main_window.displace_initial_results[1],Main_window.displace_initial_results[2],Main_window.displace_initial_results[3], Main_window.displace_initial_results[4], Main_window.displace_initial_results[5] = three_moment_method(beam_spans, beam_momentofinertia, cant, [[0.00,0.00,0.00,0.00,'POINT',0,0]], E, iters, displace_initial)
        
        endt = time.time()
        print '**Analysis Complete** in {0:.4f} sec'.format(endt-startt)
        
        Main_window.load_results = loads
        Main_window.bm = np.zeros((iters+1,N))
        # # ['D', 'Ex', 'Ey', 'F', 'H', 'L', 'Lr', 'R', 'S', 'Wx', 'Wy']
        # # data structure for each non patterned load type [['D'],[loads],[shears],[moments],[slopes],[deflections],[Support Reactions],[Moments at supports]]

        print 'Factoring Loads and Generating Graphs...'

        fi = float(self.fi_lrfd.get())
        fy = float(self.fy_lrfd.get())
        
        Main_window.LRFD_factors = [[1.4, 0.0, 0.0, 1.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, 1.6, 0.5, 0.0, 0.0, 0.0, 0.0],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, 1.6, 0.0, 0.5, 0.0, 0.0, 0.0],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, 1.6, 0.0, 0.0, 0.5, 0.0, 0.0],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, fi, 1.6, 0.0, 0.0, 0.0, 0.0],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, fi, 0.0, 1.6, 0.0, 0.0, 0.0],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, fi, 0.0, 0.0, 1.6, 0.0, 0.0],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, 0.0, 1.6, 0.0, 0.0, 0.5, 0.0],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, 0.0, 0.0, 1.6, 0.0, 0.5, 0.0],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, 0.0, 0.0, 0.0, 1.6, 0.5, 0.0],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, 0.0, 1.6, 0.0, 0.0, 0.0, 0.5],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, 0.0, 0.0, 1.6, 0.0, 0.0, 0.5],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, 0.0, 0.0, 0.0, 1.6, 0.0, 0.5],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, fi, 0.5, 0.0, 0.0, 1.0, 0.0],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, fi, 0.0, 0.5, 0.0, 1.0, 0.0],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, fi, 0.0, 0.0, 0.5, 1.0, 0.0],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, fi, 0.5, 0.0, 0.0, 0.0, 1.0],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, fi, 0.0, 0.5, 0.0, 0.0, 1.0],
                                             [1.2, 0.0, 0.0, 1.2, 1.6, fi, 0.0, 0.0, 0.5, 0.0, 1.0],
                                             [1.2, 1.0, 0.0, 1.2, 1.6, fi, 0.0, 0.0, fy, 0.0, 0.0],
                                             [1.2, 0.0, 1.0, 1.2, 1.6, fi, 0.0, 0.0, fy, 0.0, 0.0],
                                             [0.9, 0.0, 0.0, 0.0, 1.6, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                                             [0.9, 0.0, 0.0, 0.0, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                                             [0.9, 1.0, 0.0, 0.9, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                             [0.9, 0.0, 1.0, 0.9, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

        Main_window.lrfd_combos =['IBC_16_1','IBC_16_2_Lr','IBC_16_2_R','IBC_16_2_S','IBC_16_3_f1L_Lr',
                     'IBC_16_3_f1L_R','IBC_16_3_f1L_S','IBC_16_3_Wx_Lr','IBC_16_3_Wx_R',
                     'IBC_16_3_Wx_S','IBC_16_3_Wy_Lr','IBC_16_3_Wy_R','IBC_16_3_Wy_S',
                     'IBC_16_4_Wx_Lr','IBC_16_4_Wx_R','IBC_16_4_Wx_S','IBC_16_4_Wy_Lr',
                     'IBC_16_4_Wy_R','IBC_16_4_Wy_S','IBC_16_5_Ex','IBC_16_5_Ey','IBC_16_6_Wx',
                     'IBC_16_6_Wy','IBC_16_7_Ex','IBC_16_7_Ey' ]

        Main_window.basic_factors = [[1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                                 [1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                                 [1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                                                 [1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                                                 [1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                                                 [1.0, 0.0, 0.0, 1.0, 1.0, 0.75, 0.75, 0.0, 0.0, 0.0, 0.0],
                                                 [1.0, 0.0, 0.0, 1.0, 1.0, 0.75, 0.0, 0.75, 0.0, 0.0, 0.0],
                                                 [1.0, 0.0, 0.0, 1.0, 1.0, 0.75, 0.0, 0.0, 0.75, 0.0, 0.0],
                                                 [1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0],
                                                 [1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6],
                                                 [1.0, 0.70, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                                 [1.0, 0.0, 0.70, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                                 [1.0, 0.0, 0.0, 1.0, 1.0, 0.75, 0.75, 0.0, 0.0, (0.5*0.6), 0.0],
                                                 [1.0, 0.0, 0.0, 1.0, 1.0, 0.75, 0.0, 0.75, 0.0, (0.5*0.6), 0.0],
                                                 [1.0, 0.0, 0.0, 1.0, 1.0, 0.75, 0.0, 0.0, 0.75, (0.5*0.6), 0.0],
                                                 [1.0, 0.0, 0.0, 1.0, 1.0, 0.75, 0.75, 0.0, 0.0, 0.0, (0.5*0.6)],
                                                 [1.0, 0.0, 0.0, 1.0, 1.0, 0.75, 0.0, 0.75, 0.0, 0.0, (0.5*0.6)],
                                                 [1.0, 0.0, 0.0, 1.0, 1.0, 0.75, 0.0, 0.0, 0.75, 0.0, (0.5*0.6)],
                                                 [1.0, (0.75*0.70), 0.0, 1.0, 1.0, 0.75, 0.0, 0.0, 0.75, 0.0, 0.0],
                                                 [1.0, 0.0, (0.75*0.70), 1.0, 1.0, 0.75, 0.0, 0.0, 0.75, 0.0, 0.0],
                                                 [0.6, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0],
                                                 [0.6, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6],
                                                 [0.6, 0.7, 0.0, 0.6, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                                 [0.6, 0.0, 0.7, 0.6, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

        Main_window.basic_combos =['IBC_16_8','IBC_16_9','IBC_16_10_Lr',
                                     'IBC_16_10_R','IBC_16_10_S','IBC_16_11_Lr','IBC_16_11_R',
                                     'IBC_16_11_S','IBC_16_12_Wx','IBC_16_12_Wy','IBC_16_12_Ex',
                                     'IBC_16_12_Ey','IBC_16_13_Wx_Lr','IBC_16_13_Wx_R','IBC_16_13_Wx_S',
                                     'IBC_16_13_Wy_Lr','IBC_16_13_Wy_R','IBC_16_13_Wy_S','IBC_16_14_Ex','IBC_16_14_Ey',
                                     'IBC_16_15_Wx','IBC_16_15_Wy','IBC_16_16_Ex', 'IBC_16_16_Ey']


        #Factor and combine loads and Print Results to text File
        print 'LRFD Combinations...'
        Main_window.lrfd_v = []
        Main_window.lrfd_m = []
        Main_window.lrfd_r = []
        Main_window.lrfd_m_support = []
        Main_window.lrfd_v_env_min = []
        Main_window.lrfd_v_env_max = []
        Main_window.lrfd_m_env_min = []
        Main_window.lrfd_m_env_max = []
        Main_window.lrfd_r_env_min = []
        Main_window.lrfd_r_env_max = []
        Main_window.lrfd_m_support_env_min = []
        Main_window.lrfd_m_support_env_max = []
        
        for i in range(0,len(Main_window.lrfd_combos)):
            combo = Main_window.lrfd_combos[i]
            v_diag = np.zeros((iters+1, N)) + Main_window.displace_initial_results[0]
            m_diag = np.zeros((iters+1, N)) + Main_window.displace_initial_results[1]
            r = np.zeros((N+1,1)) + Main_window.displace_initial_results[4]
            m = np.zeros((N+1,1)) + Main_window.displace_initial_results[5]
            v_diag_pattern=[]
            m_diag_pattern=[]
            r_pattern=[]
            m_pattern=[]
            for pat in range(0,len(patterns)):
                v_diag_pattern.append(np.zeros((iters+1, N)))
                m_diag_pattern.append(np.zeros((iters+1, N)))
                r_pattern.append(np.zeros((N+1,1)))
                m_pattern.append(np.zeros((N+1,1)))
            for y in range(0,len(Main_window.LRFD_factors[i])):
                if y in range(5,9) and Main_window.LRFD_factors[i][y] != 0.0:

                    if len(loads[y][2][0]) <= 1:
                        pass
                    else:
                        v_diag = v_diag + (loads[y][2][0]*Main_window.LRFD_factors[i][y])
                        m_diag = m_diag + (loads[y][3][0]*Main_window.LRFD_factors[i][y])
                    
                        r = r + (loads[y][6][0]*Main_window.LRFD_factors[i][y])
                        m = m + (loads[y][7][0]*Main_window.LRFD_factors[i][y])

                    for z in range(0,len(patterns)):
                        v_diag_pattern[z] = (loads[y][2][1][z]*Main_window.LRFD_factors[i][y]) + v_diag_pattern[z]
                        m_diag_pattern[z] = (loads[y][3][1][z]*Main_window.LRFD_factors[i][y]) + m_diag_pattern[z]
                        r_pattern[z] = (loads[y][6][1][z]*Main_window.LRFD_factors[i][y]) + r_pattern[z]
                        m_pattern[z] = (loads[y][7][1][z]*Main_window.LRFD_factors[i][y]) + m_pattern[z]
                            
                elif y in range(5,9):
                    pass
                else:
                    if type(loads[y][2]) == type(v_diag):
                        v_diag = v_diag + (loads[y][2]*Main_window.LRFD_factors[i][y])
                        m_diag = m_diag + (loads[y][3]*Main_window.LRFD_factors[i][y])
                  
                        r = r + (loads[y][6]*Main_window.LRFD_factors[i][y])
                        m = m + (loads[y][7]*Main_window.LRFD_factors[i][y])
                    else:
                        pass
                        
            for z in range(0,len(patterns)):
                v_diag_pattern[z] = v_diag_pattern[z] + v_diag
                m_diag_pattern[z] = m_diag_pattern[z] + m_diag
                r_pattern[z] = r + r_pattern[z]
                m_pattern[z] = m + m_pattern[z]

            Main_window.lrfd_v.append([v_diag,v_diag_pattern])
            Main_window.lrfd_m.append([m_diag,m_diag_pattern])
            Main_window.lrfd_r.append([r,r_pattern])
            Main_window.lrfd_m_support.append([m,m_pattern])
            Main_window.lrfd_v_env_min.append(np.minimum.reduce(v_diag_pattern))
            Main_window.lrfd_v_env_max.append(np.maximum.reduce(v_diag_pattern))
            Main_window.lrfd_m_env_min.append(np.minimum.reduce(m_diag_pattern))
            Main_window.lrfd_m_env_max.append(np.maximum.reduce(m_diag_pattern))
            Main_window.lrfd_r_env_min.append(np.minimum.reduce(r_pattern))
            Main_window.lrfd_r_env_max.append(np.maximum.reduce(r_pattern))
            Main_window.lrfd_m_support_env_min.append(np.minimum.reduce(m_pattern))
            Main_window.lrfd_m_support_env_max.append(np.maximum.reduce(m_pattern))

        print 'ASD/BASIC Combinations...'
        Main_window.basic_v = []
        Main_window.basic_m = []
        Main_window.basic_s = []
        Main_window.basic_d = []
        Main_window.basic_r = []
        Main_window.basic_m_support = []
        Main_window.basic_v_env_max = []
        Main_window.basic_m_env_max = []
        Main_window.basic_s_env_max = []
        Main_window.basic_d_env_max = []
        Main_window.basic_r_env_max = []
        Main_window.basic_m_support_env_max = [] 
        Main_window.basic_v_env_min = []
        Main_window.basic_m_env_min = []
        Main_window.basic_s_env_min = []
        Main_window.basic_d_env_min = []
        Main_window.basic_r_env_min = []
        Main_window.basic_m_support_env_min = []  
        
        for i in range(0,len(Main_window.basic_combos)):
            combo = Main_window.basic_combos[i]
            v_diag = np.zeros((iters+1, N)) + Main_window.displace_initial_results[0]
            m_diag = np.zeros((iters+1, N)) + Main_window.displace_initial_results[1]
            s_diag = np.zeros((iters+1, N)) + Main_window.displace_initial_results[2]
            d_diag = np.zeros((iters+1, N)) + Main_window.displace_initial_results[3]
            r = np.zeros((N+1,1)) + Main_window.displace_initial_results[4]
            m = np.zeros((N+1,1)) + Main_window.displace_initial_results[5]
            v_diag_pattern=[]
            m_diag_pattern=[]
            s_diag_pattern=[]
            d_diag_pattern=[]
            r_pattern=[]
            m_pattern=[]
            for pat in range(0,len(patterns)):
                v_diag_pattern.append(np.zeros((iters+1, N)))
                m_diag_pattern.append(np.zeros((iters+1, N)))
                s_diag_pattern.append(np.zeros((iters+1, N)))
                d_diag_pattern.append(np.zeros((iters+1, N)))
                r_pattern.append(np.zeros((N+1,1)))
                m_pattern.append(np.zeros((N+1,1)))
            for y in range(0,len(Main_window.basic_factors[i])):
                if y in range(5,9) and Main_window.basic_factors[i][y] != 0.0:
                    if len(loads[y][2][0]) <= 1:                        
                        pass
                    else:
                        v_diag = v_diag + (loads[y][2][0]*Main_window.basic_factors[i][y])
                        m_diag = m_diag + (loads[y][3][0]*Main_window.basic_factors[i][y])
                        s_diag = s_diag + (loads[y][4][0]*Main_window.basic_factors[i][y])
                        d_diag = d_diag + (loads[y][5][0]*Main_window.basic_factors[i][y])
                    
                        r = r + (loads[y][6][0]*Main_window.basic_factors[i][y])
                        m = m + (loads[y][7][0]*Main_window.basic_factors[i][y])

                    for z in range(0,len(patterns)):
                        v_diag_pattern[z] = (loads[y][2][1][z]*Main_window.basic_factors[i][y]) + v_diag_pattern[z]
                        m_diag_pattern[z] = (loads[y][3][1][z]*Main_window.basic_factors[i][y]) + m_diag_pattern[z]
                        s_diag_pattern[z] = (loads[y][4][1][z]*Main_window.basic_factors[i][y]) + s_diag_pattern[z]
                        d_diag_pattern[z] = (loads[y][5][1][z]*Main_window.basic_factors[i][y]) + d_diag_pattern[z]
                        r_pattern[z] = (loads[y][6][1][z]*Main_window.basic_factors[i][y]) + r_pattern[z]
                        m_pattern[z] = (loads[y][7][1][z]*Main_window.basic_factors[i][y]) + m_pattern[z]
                            
                elif y in range(5,9):
                    pass
                else:
                    if type(loads[y][2]) == type(v_diag):
                        v_diag = v_diag + (loads[y][2]*Main_window.basic_factors[i][y])
                        m_diag = m_diag + (loads[y][3]*Main_window.basic_factors[i][y])
                        s_diag = s_diag + (loads[y][4]*Main_window.basic_factors[i][y])
                        d_diag = d_diag + (loads[y][5]*Main_window.basic_factors[i][y])
                    
                        r = r + (loads[y][6]*Main_window.basic_factors[i][y])
                        m = m + (loads[y][7]*Main_window.basic_factors[i][y])
                    else:
                        pass
                        
            for z in range(0,len(patterns)):
                v_diag_pattern[z] = v_diag + v_diag_pattern[z]
                m_diag_pattern[z] = m_diag + m_diag_pattern[z]
                s_diag_pattern[z] = s_diag + s_diag_pattern[z]
                d_diag_pattern[z] = d_diag + d_diag_pattern[z]
                r_pattern[z] = r + r_pattern[z]
                m_pattern[z] = m + m_pattern[z]

            Main_window.basic_v.append([v_diag,v_diag_pattern])
            Main_window.basic_m.append([m_diag,m_diag_pattern])
            Main_window.basic_s.append([s_diag,s_diag_pattern])
            Main_window.basic_d.append([d_diag,d_diag_pattern])
            Main_window.basic_r.append([r,r_pattern])
            Main_window.basic_m_support.append([m,m_pattern])
            Main_window.basic_v_env_max.append(np.maximum.reduce(v_diag_pattern))
            Main_window.basic_m_env_max.append(np.maximum.reduce(m_diag_pattern))
            Main_window.basic_s_env_max.append(np.maximum.reduce(s_diag_pattern))
            Main_window.basic_d_env_max.append(np.maximum.reduce(d_diag_pattern))
            Main_window.basic_r_env_max.append(np.maximum.reduce(r_pattern))
            Main_window.basic_m_support_env_max.append(np.maximum.reduce(m_pattern))
            Main_window.basic_v_env_min.append(np.minimum.reduce(v_diag_pattern))
            Main_window.basic_m_env_min.append(np.minimum.reduce(m_diag_pattern))
            Main_window.basic_s_env_min.append(np.minimum.reduce(s_diag_pattern))
            Main_window.basic_d_env_min.append(np.minimum.reduce(d_diag_pattern))
            Main_window.basic_r_env_min.append(np.minimum.reduce(r_pattern))
            Main_window.basic_m_support_env_min.append(np.minimum.reduce(m_pattern))
        
        print 'Enveloping Results...'

        Main_window.lrfd_Rmax_print = np.maximum.reduce(Main_window.lrfd_r_env_max)
        Main_window.lrfd_Rmin_print = np.minimum.reduce(Main_window.lrfd_r_env_min)
        Main_window.lrfd_Mmax_print = np.maximum.reduce(Main_window.lrfd_m_support_env_max)
        Main_window.lrfd_Mmin_print = np.minimum.reduce(Main_window.lrfd_m_support_env_min)
        Main_window.asd_Rmax_print = np.maximum.reduce(Main_window.basic_r_env_max)
        Main_window.asd_Rmin_print = np.minimum.reduce(Main_window.basic_r_env_min)
        Main_window.asd_Mmax_print = np.maximum.reduce(Main_window.basic_m_support_env_max)
        Main_window.asd_Mmin_print = np.minimum.reduce(Main_window.basic_m_support_env_min)
        
        Main_window.lrfd_v_max_diag = np.maximum.reduce(Main_window.lrfd_v_env_max)
        Main_window.lrfd_v_min_diag = np.minimum.reduce(Main_window.lrfd_v_env_min)
        Main_window.lrfd_m_max_diag = np.maximum.reduce(Main_window.lrfd_m_env_max)
        Main_window.lrfd_m_min_diag = np.minimum.reduce(Main_window.lrfd_m_env_min)

        Main_window.asd_v_max_diag = np.maximum.reduce(Main_window.basic_v_env_max)
        Main_window.asd_v_min_diag = np.minimum.reduce(Main_window.basic_v_env_min)
        Main_window.asd_m_max_diag = np.maximum.reduce(Main_window.basic_m_env_max)
        Main_window.asd_m_min_diag = np.minimum.reduce(Main_window.basic_m_env_min)
        Main_window.asd_s_max_diag = np.maximum.reduce(Main_window.basic_s_env_max)
        Main_window.asd_s_min_diag = np.minimum.reduce(Main_window.basic_s_env_min)
        Main_window.asd_d_max_diag = np.maximum.reduce(Main_window.basic_d_env_max)
        Main_window.asd_d_min_diag = np.minimum.reduce(Main_window.basic_d_env_min)
        
        #Create CSV file of LRFD Envelope Results
        print 'Writing CSV Files...'
        file = open(os.path.join(path,bmlabel+'_04_LRFD_Envelope_Results.csv'),'w')
        file.write('LRFD Envelope Results\n')
        file.write('Spans:,'+str(N))
        file.write('\nStations:,'+str(iters))
        file.write('\nspan,x_local (ft), x_global (ft),V_min (kips),V_max (kips),M_min (ft-kips),M_max (ft-kips)\n')
        for j in range(0,N):
            for k in range(0,iters+1):
                if j ==0:
                    file.write('{0},{1:.6f},{2:.6f},{3:.6f},{4:.6f},{5:.6f},{6:.6f}\n'.format(j+1,Main_window.xs[k,j], Main_window.xs[k,j], Main_window.lrfd_v_min_diag[k,j], Main_window.lrfd_v_max_diag[k,j], Main_window.lrfd_m_min_diag[k,j], Main_window.lrfd_m_max_diag[k,j]))
                else:
                    file.write('{0},{1:.6f},{2:.6f},{3:.6f},{4:.6f},{5:.6f},{6:.6f}\n'.format(j+1,(Main_window.xs[k,j]-Main_window.xs[-1,j-1]), Main_window.xs[k,j], Main_window.lrfd_v_min_diag[k,j], Main_window.lrfd_v_max_diag[k,j], Main_window.lrfd_m_min_diag[k,j], Main_window.lrfd_m_max_diag[k,j]))
        file.close()
        
        #Create CSV file of ASD Envelope Results
        file = open(os.path.join(path,bmlabel+'_05_ASD_Envelope_Results.csv'),'w')
        file.write('ASD Envelope Results\n')
        file.write('Spans:,'+str(N))
        file.write('\nStations:,'+str(iters))
        file.write('\nspan,x_local (ft),x_global (ft),V_min (kips),V_max (kips),M_min (ft-kips),M_max (ft-kips),d_min (in),d_max (in)\n')
        for j in range(0,N):
            for k in range(0,iters+1):
                if j==0:
                    file.write('{0:.6f},{1:.6f},{2:.6f},{3:.6f},{4:.6f},{5:.6f},{6:.6f},{7:.6f},{8:.6f}\n'.format(j+1,Main_window.xs[k,j], Main_window.xs[k,j], Main_window.asd_v_min_diag[k,j], Main_window.asd_v_max_diag[k,j], Main_window.asd_m_min_diag[k,j], Main_window.asd_m_max_diag[k,j], Main_window.asd_d_min_diag[k,j], Main_window.asd_d_max_diag[k,j]))
                else:
                    file.write('{0:.6f},{1:.6f},{2:.6f},{3:.6f},{4:.6f},{5:.6f},{6:.6f},{7:.6f},{8:.6f}\n'.format(j+1,(Main_window.xs[k,j]-Main_window.xs[-1,j-1]), Main_window.xs[k,j], Main_window.asd_v_min_diag[k,j], Main_window.asd_v_max_diag[k,j], Main_window.asd_m_min_diag[k,j], Main_window.asd_m_max_diag[k,j], Main_window.asd_d_min_diag[k,j], Main_window.asd_d_max_diag[k,j]))
        file.close()
        
        #Create CSV file of ASD Envelope Results
        file = open(os.path.join(path,bmlabel+'_05_ASD_Envelope_Results.csv'),'w')
        file.write('ASD Envelope Results\n')
        file.write('Spans:,'+str(N))
        file.write('\nStations:,'+str(iters))
        file.write('\nspan,x_local (ft),x_global (ft),V_min (kips),V_max (kips),M_min (ft-kips),M_max (ft-kips),d_min (in),d_max (in)\n')
        for j in range(0,N):
            for k in range(0,iters+1):
                if j==0:
                    file.write('{0:.6f},{1:.6f},{2:.6f},{3:.6f},{4:.6f},{5:.6f},{6:.6f},{7:.6f},{8:.6f}\n'.format(j+1,Main_window.xs[k,j], Main_window.xs[k,j], Main_window.asd_v_min_diag[k,j], Main_window.asd_v_max_diag[k,j], Main_window.asd_m_min_diag[k,j], Main_window.asd_m_max_diag[k,j], Main_window.asd_d_min_diag[k,j], Main_window.asd_d_max_diag[k,j]))
                else:
                    file.write('{0:.6f},{1:.6f},{2:.6f},{3:.6f},{4:.6f},{5:.6f},{6:.6f},{7:.6f},{8:.6f}\n'.format(j+1,(Main_window.xs[k,j]-Main_window.xs[-1,j-1]), Main_window.xs[k,j], Main_window.asd_v_min_diag[k,j], Main_window.asd_v_max_diag[k,j], Main_window.asd_m_min_diag[k,j], Main_window.asd_m_max_diag[k,j], Main_window.asd_d_min_diag[k,j], Main_window.asd_d_max_diag[k,j]))
        file.close()
        
        cad_points = iters
        #Create DXF of Envelope Results
        print 'Creating DXF of Results ...'
        file = open(os.path.join(path,bmlabel+'_02_Envelope_Results.dxf'),'w')
        file.write('  0\nSECTION\n  2\nENTITIES\n')
        file.write('  0\nPOLYLINE\n  8\nspans\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
        for j in range(0,N):
            file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n0.0\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)))
            file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n0.0\n 30\n0.0\n'.format((Main_window.xs[-1,j]*12)))
        file.write('  0\nSEQEND\n')
        for j in range(0,N):
            file.write('  0\nPOLYLINE\n 62\n16\n  8\nspans\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),Main_window.lrfd_m_min_diag.min()))
            file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),Main_window.lrfd_m_max_diag.max()))
            file.write('  0\nSEQEND\n')
        if cant[0] == 'L' or cant[0] == 'B':
            pass
        else:
            file.write('  0\nPOLYLINE\n 62\n2\n  8\nsupports\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nsupports\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),0.0))
            file.write('  0\nVERTEX\n  8\nsupports\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12)-5,-10.0))
            file.write('  0\nVERTEX\n  8\nsupports\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12)+5,-10.0))
            file.write('  0\nVERTEX\n  8\nsupports\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),0.0))
            file.write('  0\nSEQEND\n')
        for j in range(1,N):
            file.write('  0\nPOLYLINE\n 62\n2\n  8\nsupports\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nsupports\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),0.0))
            file.write('  0\nVERTEX\n  8\nsupports\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)-5,-10.0))
            file.write('  0\nVERTEX\n  8\nsupports\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)+5,-10.0))
            file.write('  0\nVERTEX\n  8\nsupports\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),0.0))
            file.write('  0\nSEQEND\n')
        file.write('  0\nPOLYLINE\n 62\n16\n  8\nspans\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
        file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),Main_window.lrfd_m_min_diag.min()))
        file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),Main_window.lrfd_m_max_diag.max()))
        file.write('  0\nSEQEND\n')
        if cant[0] == 'R' or cant[0] == 'B':
            pass
        else:
            file.write('  0\nPOLYLINE\n 62\n2\n  8\nsupports\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nsupports\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),0.0))
            file.write('  0\nVERTEX\n  8\nsupports\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12)-5,-10.0))
            file.write('  0\nVERTEX\n  8\nsupports\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12)+5,-10.0))
            file.write('  0\nVERTEX\n  8\nsupports\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),0.0))
            file.write('  0\nSEQEND\n')

        if cant[0] == 'L' or cant[0] == 'B':
            pass
        else:
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nLRFD_Reactions_Max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),0.0))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0-(float(Main_window.lrfd_Rmax_print[0])/1000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nLRFD_Reactions_Max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12)-(float(Main_window.lrfd_Rmax_print[0])/10000),(0.0-(float(Main_window.lrfd_Rmax_print[0])/10000))))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0)))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12)+(float(Main_window.lrfd_Rmax_print[0])/10000),(0.0-(float(Main_window.lrfd_Rmax_print[0])/10000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nTEXT\n 62\n9\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0-(float(Main_window.lrfd_Rmax_print[0])/1000)), (float(Main_window.lrfd_Rmax_print[0])/1000)))
        for j in range(1,N):
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nLRFD_Reactions_Max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),0.0))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0-(float(Main_window.lrfd_Rmax_print[j])/1000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nLRFD_Reactions_Max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)-(float(Main_window.lrfd_Rmax_print[j])/10000),(0.0-(float(Main_window.lrfd_Rmax_print[j])/10000))))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0)))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)+(float(Main_window.lrfd_Rmax_print[j])/10000),(0.0-(float(Main_window.lrfd_Rmax_print[j])/10000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nTEXT\n 62\n9\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0-(float(Main_window.lrfd_Rmax_print[j])/1000)), (float(Main_window.lrfd_Rmax_print[j])/1000)))
        if cant[0] == 'R' or cant[0] == 'B':
            pass
        else:
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nLRFD_Reactions_Max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),0.0))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0-(float(Main_window.lrfd_Rmax_print[N])/1000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nLRFD_Reactions_Max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12)-(float(Main_window.lrfd_Rmax_print[N])/10000),(0.0-(float(Main_window.lrfd_Rmax_print[N])/10000))))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0)))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12)+(float(Main_window.lrfd_Rmax_print[N])/10000),(0.0-(float(Main_window.lrfd_Rmax_print[N])/10000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nTEXT\n 62\n9\n  8\nLRFD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0-(float(Main_window.lrfd_Rmax_print[N])/1000)), (float(Main_window.lrfd_Rmax_print[N])/1000)))

        if cant[0] == 'L' or cant[0] == 'B':
            pass
        else:
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nLRFD_Reactions_Min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),0.0))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0-(float(Main_window.lrfd_Rmin_print[0])/1000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nLRFD_Reactions_Min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12)-(float(Main_window.lrfd_Rmin_print[0])/10000),(0.0-(float(Main_window.lrfd_Rmin_print[0])/10000))))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0)))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12)+(float(Main_window.lrfd_Rmin_print[0])/10000),(0.0-(float(Main_window.lrfd_Rmin_print[0])/10000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nTEXT\n 62\n9\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0-(float(Main_window.lrfd_Rmin_print[0])/1000)), (float(Main_window.lrfd_Rmin_print[0])/1000)))
        for j in range(1,N):
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nLRFD_Reactions_Min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),0.0))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0-(float(Main_window.lrfd_Rmin_print[j])/1000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nLRFD_Reactions_Min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)-(float(Main_window.lrfd_Rmin_print[j])/10000),(0.0-(float(Main_window.lrfd_Rmin_print[j])/10000))))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0)))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)+(float(Main_window.lrfd_Rmin_print[j])/10000),(0.0-(float(Main_window.lrfd_Rmin_print[j])/10000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nTEXT\n 62\n9\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0-(float(Main_window.lrfd_Rmin_print[j])/1000)), (float(Main_window.lrfd_Rmin_print[j])/1000)))
        if cant[0] == 'R' or cant[0] == 'B':
            pass
        else:
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nLRFD_Reactions_Min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),0.0))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0-(float(Main_window.lrfd_Rmin_print[N])/1000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nLRFD_Reactions_Min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12)-(float(Main_window.lrfd_Rmin_print[N])/10000),(0.0-(float(Main_window.lrfd_Rmin_print[N])/10000))))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0)))
            file.write('  0\nVERTEX\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12)+(float(Main_window.lrfd_Rmin_print[N])/10000),(0.0-(float(Main_window.lrfd_Rmin_print[N])/10000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nTEXT\n 62\n9\n  8\nLRFD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0-(float(Main_window.lrfd_Rmin_print[N])/1000)), (float(Main_window.lrfd_Rmin_print[N])/1000)))

        if cant[0] == 'L' or cant[0] == 'B':
            pass
        else:
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nASD_Reactions_Max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),0.0))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0-(float(Main_window.asd_Rmax_print[0])/1000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nASD_Reactions_Max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12)-(float(Main_window.asd_Rmax_print[0])/10000),(0.0-(float(Main_window.asd_Rmax_print[0])/10000))))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0)))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12)+(float(Main_window.asd_Rmax_print[0])/10000),(0.0-(float(Main_window.asd_Rmax_print[0])/10000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nTEXT\n 62\n9\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0-(float(Main_window.asd_Rmax_print[0])/1000)), (float(Main_window.asd_Rmax_print[0])/1000)))
        for j in range(1,N):
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nASD_Reactions_Max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),0.0))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0-(float(Main_window.asd_Rmax_print[j])/1000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nASD_Reactions_Max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)-(float(Main_window.asd_Rmax_print[j])/10000),(0.0-(float(Main_window.asd_Rmax_print[j])/10000))))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0)))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)+(float(Main_window.asd_Rmax_print[j])/10000),(0.0-(float(Main_window.asd_Rmax_print[j])/10000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nTEXT\n 62\n9\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0-(float(Main_window.asd_Rmax_print[j])/1000)), (float(Main_window.asd_Rmax_print[j])/1000)))
        if cant[0] == 'R' or cant[0] == 'B':
            pass
        else:
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nASD_Reactions_Max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),0.0))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0-(float(Main_window.asd_Rmax_print[N])/1000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nASD_Reactions_Max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12)-(float(Main_window.asd_Rmax_print[N])/10000),(0.0-(float(Main_window.asd_Rmax_print[N])/10000))))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0)))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12)+(float(Main_window.asd_Rmax_print[N])/10000),(0.0-(float(Main_window.asd_Rmax_print[N])/10000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nTEXT\n 62\n9\n  8\nASD_Reactions_Max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0-(float(Main_window.asd_Rmax_print[N])/1000)), (float(Main_window.asd_Rmax_print[N])/1000)))

        if cant[0] == 'L' or cant[0] == 'B':
            pass
        else:
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nASD_Reactions_Min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),0.0))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0-(float(Main_window.asd_Rmin_print[0])/1000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nASD_Reactions_Min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12)-(float(Main_window.asd_Rmin_print[0])/10000),(0.0-(float(Main_window.asd_Rmin_print[0])/10000))))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0)))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12)+(float(Main_window.asd_Rmin_print[0])/10000),(0.0-(float(Main_window.asd_Rmin_print[0])/10000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nTEXT\n 62\n9\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0-(float(Main_window.asd_Rmin_print[0])/1000)), (float(Main_window.asd_Rmin_print[0])/1000)))
        for j in range(1,N):
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nASD_Reactions_Min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),0.0))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0-(float(Main_window.asd_Rmin_print[j])/1000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nASD_Reactions_Min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)-(float(Main_window.asd_Rmin_print[j])/10000),(0.0-(float(Main_window.asd_Rmin_print[j])/10000))))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0)))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)+(float(Main_window.asd_Rmin_print[j])/10000),(0.0-(float(Main_window.asd_Rmin_print[j])/10000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nTEXT\n 62\n9\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0-(float(Main_window.asd_Rmin_print[j])/1000)), (float(Main_window.asd_Rmin_print[j])/1000)))
        if cant[0] == 'R' or cant[0] == 'B':
            pass
        else:
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nASD_Reactions_Min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),0.0))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0-(float(Main_window.asd_Rmin_print[N])/1000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nPOLYLINE\n 62\n8\n  8\nASD_Reactions_Min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12)-(float(Main_window.asd_Rmin_print[N])/10000),(0.0-(float(Main_window.asd_Rmin_print[N])/10000))))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0)))
            file.write('  0\nVERTEX\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12)+(float(Main_window.asd_Rmin_print[N])/10000),(0.0-(float(Main_window.asd_Rmin_print[N])/10000))))
            file.write('  0\nSEQEND\n')
            file.write('  0\nTEXT\n 62\n9\n  8\nASD_Reactions_Min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0-(float(Main_window.asd_Rmin_print[N])/1000)), (float(Main_window.asd_Rmin_print[N])/1000)))


        file.write('  0\nPOLYLINE\n 62\n3\n  8\nLRFD_shear_max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
        for j in range(0,N):
            for z in range(0,cad_points+1):
                if z==0:
                    k=0
                else:
                    if z*(iters/(cad_points*1.00)) > iters:
                        k=iters
                    else:
                        k=int(round(z*(iters/(cad_points*1.00))))
                file.write('  0\nVERTEX\n  8\nLRFD_shear_max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[k,j]*12), Main_window.lrfd_v_max_diag[k,j]))
        file.write('  0\nSEQEND\n')
        for j in range(0,N):
            for z in range(0,5):
                if z==0:
                    k=0
                    l=k+1
                else:
                    if z*int(iters/4) >= iters:
                        k=iters
                        l=k
                    else:
                        k=z*int(iters/4)
                        l=k+1
                if Main_window.lrfd_v_max_diag[l,j] > Main_window.lrfd_v_max_diag[k,j]:
                    file.write('  0\nTEXT\n 62\n3\n  8\nLRFD_shear_max_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n-45.0\n'.format((Main_window.xs[k,j]*12), Main_window.lrfd_v_max_diag[k,j]))
                else:
                    file.write('  0\nTEXT\n 62\n3\n  8\nLRFD_shear_max_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n45.0\n'.format((Main_window.xs[k,j]*12), Main_window.lrfd_v_max_diag[k,j]))
        file.write('  0\nPOLYLINE\n 62\n2\n  8\nLRFD_shear_min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
        for j in range(0,N):
            for z in range(0,cad_points+1):
                if z==0:
                    k=0
                else:
                    if z*(iters/(cad_points*1.00)) > iters:
                        k=iters
                    else:
                        k=int(round(z*(iters/(cad_points*1.00))))
                file.write('  0\nVERTEX\n  8\nLRFD_shear_min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[k,j]*12), Main_window.lrfd_v_min_diag[k,j]))
        file.write('  0\nSEQEND\n')
        for j in range(0,N):
            for z in range(0,5):
                if z==0:
                    k=0
                    l=k+1
                else:
                    if z*int(iters/4) >= iters:
                        k=iters
                        l=k
                    else:
                        k=z*int(iters/4)
                        l=k+1
                if Main_window.lrfd_v_min_diag[l,j] > Main_window.lrfd_v_min_diag[k,j]:
                    file.write('  0\nTEXT\n 62\n2\n  8\nLRFD_shear_min_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n-45.0\n'.format((Main_window.xs[k,j]*12), Main_window.lrfd_v_min_diag[k,j]))
                else:
                    file.write('  0\nTEXT\n 62\n2\n  8\nLRFD_shear_min_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n45.0\n'.format((Main_window.xs[k,j]*12), Main_window.lrfd_v_min_diag[k,j]))
        file.write('  0\nPOLYLINE\n 62\n5\n  8\nLRFD_moment_max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
        for j in range(0,N):
            for z in range(0,cad_points+1):
                if z==0:
                    k=0
                else:
                    if z*(iters/(cad_points*1.00)) > iters:
                        k=iters
                    else:
                        k=int(round(z*(iters/(cad_points*1.00))))
                file.write('  0\nVERTEX\n  8\nLRFD_moment_max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[k,j]*12), Main_window.lrfd_m_max_diag[k,j]))
        file.write('  0\nSEQEND\n')
        for j in range(0,N):
            for z in range(0,5):
                if z==0:
                    k=0
                    l=k+1
                else:
                    if z*int(iters/4) >= iters:
                        k=iters
                        l=k
                    else:
                        k=z*int(iters/4)
                        l=k+1
                if Main_window.lrfd_m_max_diag[l,j] > Main_window.lrfd_m_max_diag[k,j]:
                    file.write('  0\nTEXT\n 62\n5\n  8\nLRFD_moment_max_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} ft-kips\n 50\n-45.0\n'.format((Main_window.xs[k,j]*12), Main_window.lrfd_m_max_diag[k,j]))
                else:
                    file.write('  0\nTEXT\n 62\n5\n  8\nLRFD_moment_max_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} ft-kips\n 50\n45.0\n'.format((Main_window.xs[k,j]*12), Main_window.lrfd_m_max_diag[k,j]))
        file.write('  0\nPOLYLINE\n 62\n4\n  8\nLRFD_moment_min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
        for j in range(0,N):
            for z in range(0,cad_points+1):
                if z==0:
                    k=0
                else:
                    if z*(iters/(cad_points*1.00)) > iters:
                        k=iters
                    else:
                        k=int(round(z*(iters/(cad_points*1.00))))
                file.write('  0\nVERTEX\n  8\nLRFD_moment_min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[k,j]*12), Main_window.lrfd_m_min_diag[k,j]))
        file.write('  0\nSEQEND\n')
        for j in range(0,N):
            for z in range(0,5):
                if z==0:
                    k=0
                    l=k+1
                else:
                    if z*int(iters/4) >= iters:
                        k=iters
                        l=k
                    else:
                        k=z*int(iters/4)
                        l=k+1
                if Main_window.lrfd_m_min_diag[l,j] > Main_window.lrfd_m_min_diag[k,j]:
                    file.write('  0\nTEXT\n 62\n4\n  8\nLRFD_moment_min_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} ft-kips\n 50\n-45.0\n'.format((Main_window.xs[k,j]*12), Main_window.lrfd_m_min_diag[k,j]))
                else:
                    file.write('  0\nTEXT\n 62\n4\n  8\nLRFD_moment_min_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} ft-kips\n 50\n45.0\n'.format((Main_window.xs[k,j]*12), Main_window.lrfd_m_min_diag[k,j]))
        #Start ASD polygon section
        file.write('  0\nPOLYLINE\n 62\n3\n  8\nASD_shear_max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
        for j in range(0,N):
            for z in range(0,cad_points+1):
                if z==0:
                    k=0
                else:
                    if z*(iters/(cad_points*1.00)) > iters:
                        k=iters
                    else:
                        k=int(round(z*(iters/(cad_points*1.00))))
                file.write('  0\nVERTEX\n  8\nASD_shear_max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[k,j]*12), Main_window.asd_v_max_diag[k,j]))
        file.write('  0\nSEQEND\n')
        for j in range(0,N):
            for z in range(0,5):
                if z==0:
                    k=0
                    l=k+1
                else:
                    if z*int(iters/4) >= iters:
                        k=iters
                        l=k
                    else:
                        k=z*int(iters/4)
                        l=k+1
                if Main_window.asd_v_max_diag[l,j] > Main_window.asd_v_max_diag[k,j]:
                    file.write('  0\nTEXT\n 62\n3\n  8\nASD_shear_max_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n-45.0\n'.format((Main_window.xs[k,j]*12), Main_window.asd_v_max_diag[k,j]))
                else:
                    file.write('  0\nTEXT\n 62\n3\n  8\nASD_shear_max_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n45.0\n'.format((Main_window.xs[k,j]*12), Main_window.asd_v_max_diag[k,j]))
        file.write('  0\nPOLYLINE\n 62\n2\n  8\nASD_shear_min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
        for j in range(0,N):
            for z in range(0,cad_points+1):
                if z==0:
                    k=0
                else:
                    if z*(iters/(cad_points*1.00)) > iters:
                        k=iters
                    else:
                        k=int(round(z*(iters/(cad_points*1.00))))
                file.write('  0\nVERTEX\n  8\nASD_shear_min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[k,j]*12), Main_window.asd_v_min_diag[k,j]))
        file.write('  0\nSEQEND\n')
        for j in range(0,N):
            for z in range(0,5):
                if z==0:
                    k=0
                    l=k+1
                else:
                    if z*int(iters/4) >= iters:
                        k=iters
                        l=k
                    else:
                        k=z*int(iters/4)
                        l=k+1
                if Main_window.asd_v_min_diag[l,j] > Main_window.asd_v_min_diag[k,j]:
                    file.write('  0\nTEXT\n 62\n2\n  8\nASD_shear_min_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n-45.0\n'.format((Main_window.xs[k,j]*12), Main_window.asd_v_min_diag[k,j]))
                else:
                    file.write('  0\nTEXT\n 62\n2\n  8\nASD_shear_min_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n45.0\n'.format((Main_window.xs[k,j]*12), Main_window.asd_v_min_diag[k,j]))
        file.write('  0\nPOLYLINE\n 62\n5\n  8\nASD_moment_max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
        for j in range(0,N):
            for z in range(0,cad_points+1):
                if z==0:
                    k=0
                else:
                    if z*(iters/(cad_points*1.00)) > iters:
                        k=iters
                    else:
                        k=int(round(z*(iters/(cad_points*1.00))))
                file.write('  0\nVERTEX\n  8\nASD_moment_max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[k,j]*12), Main_window.asd_m_max_diag[k,j]))
        file.write('  0\nSEQEND\n')
        for j in range(0,N):
            for z in range(0,5):
                if z==0:
                    k=0
                    l=k+1
                else:
                    if z*int(iters/4) >= iters:
                        k=iters
                        l=k
                    else:
                        k=z*int(iters/4)
                        l=k+1
                if Main_window.asd_m_max_diag[l,j] > Main_window.asd_m_max_diag[k,j]:
                    file.write('  0\nTEXT\n 62\n5\n  8\nASD_moment_max_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} ft-kips\n 50\n-45.0\n'.format((Main_window.xs[k,j]*12), Main_window.asd_m_max_diag[k,j]))
                else:
                    file.write('  0\nTEXT\n 62\n5\n  8\nASD_moment_max_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} ft-kips\n 50\n45.0\n'.format((Main_window.xs[k,j]*12), Main_window.asd_m_max_diag[k,j]))
        file.write('  0\nPOLYLINE\n 62\n4\n  8\nASD_moment_min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
        for j in range(0,N):
            for z in range(0,cad_points+1):
                if z==0:
                    k=0
                else:
                    if z*(iters/(cad_points*1.00)) > iters:
                        k=iters
                    else:
                        k=int(round(z*(iters/(cad_points*1.00))))
                file.write('  0\nVERTEX\n  8\nASD_moment_min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[k,j]*12), Main_window.asd_m_min_diag[k,j]))
        file.write('  0\nSEQEND\n')
        for j in range(0,N):
            for z in range(0,5):
                if z==0:
                    k=0
                    l=k+1
                else:
                    if z*int(iters/4) >= iters:
                        k=iters
                        l=k
                    else:
                        k=z*int(iters/4)
                        l=k+1
                if Main_window.asd_m_min_diag[l,j] > Main_window.asd_m_min_diag[k,j]:
                    file.write('  0\nTEXT\n 62\n4\n  8\nASD_moment_min_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} ft-kips\n 50\n-45.0\n'.format((Main_window.xs[k,j]*12), Main_window.asd_m_min_diag[k,j]))
                else:
                    file.write('  0\nTEXT\n 62\n4\n  8\nASD_moment_min_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} ft-kips\n 50\n45.0\n'.format((Main_window.xs[k,j]*12), Main_window.asd_m_min_diag[k,j]))
        file.write('  0\nPOLYLINE\n 62\n6\n  8\nASD_deflection_max\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
        for j in range(0,N):
            for z in range(0,cad_points+1):
                if z==0:
                    k=0
                else:
                    if z*(iters/(cad_points*1.00)) > iters:
                        k=iters
                    else:
                        k=int(round(z*(iters/(cad_points*1.00))))
                file.write('  0\nVERTEX\n  8\nASD_deflection_max\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[k,j]*12), Main_window.asd_d_max_diag[k,j]*100))
        file.write('  0\nSEQEND\n')
        for j in range(0,N):
            for z in range(0,5):
                if z==0:
                    k=0
                    l=k+1
                else:
                    if z*int(iters/4) >= iters:
                        k=iters
                        l=k
                    else:
                        k=z*int(iters/4)
                        l=k+1
                if Main_window.asd_d_max_diag[l,j] > Main_window.asd_d_max_diag[k,j]:
                    file.write('  0\nTEXT\n 62\n6\n  8\nASD_deflection_max_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{2:.4f} in\n 50\n-45.0\n'.format((Main_window.xs[k,j]*12), (Main_window.asd_d_max_diag[k,j]*100),Main_window.asd_d_max_diag[k,j]))
                else:
                    file.write('  0\nTEXT\n 62\n6\n  8\nASD_deflection_max_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{2:.4f} in\n 50\n45.0\n'.format((Main_window.xs[k,j]*12), (Main_window.asd_d_max_diag[k,j]*100),Main_window.asd_d_max_diag[k,j]))
        file.write('  0\nPOLYLINE\n 62\n241\n  8\nASD_deflection_min\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
        for j in range(0,N):
            for z in range(0,cad_points+1):
                if z==0:
                    k=0
                else:
                    if z*(iters/(cad_points*1.00)) > iters:
                        k=iters
                    else:
                        k=int(round(z*(iters/(cad_points*1.00))))
                file.write('  0\nVERTEX\n  8\nASD_deflection_min\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[k,j]*12), Main_window.asd_d_min_diag[k,j]*100))
        file.write('  0\nSEQEND\n')
        for j in range(0,N):
            for z in range(0,5):
                if z==0:
                    k=0
                    l=k+1
                else:
                    if z*int(iters/4) >= iters:
                        k=iters
                        l=k
                    else:
                        k=z*int(iters/4)
                        l=k+1
                if Main_window.asd_d_min_diag[l,j] > Main_window.asd_d_min_diag[k,j]:
                    file.write('  0\nTEXT\n 62\n241\n  8\nASD_deflection_min_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{2:.4f} in\n 50\n-45.0\n'.format((Main_window.xs[k,j]*12), (Main_window.asd_d_min_diag[k,j]*100),Main_window.asd_d_min_diag[k,j]))
                else:
                    file.write('  0\nTEXT\n 62\n241\n  8\nASD_deflection_min_labels\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{2:.4f} in\n 50\n45.0\n'.format((Main_window.xs[k,j]*12), (Main_window.asd_d_min_diag[k,j]*100),Main_window.asd_d_min_diag[k,j]))
        file.write('  0\nENDSEC\n  0\nEOF')
        file.close()
        
        print 'Done!'
        self.brun.configure(bg='green')
        self.bresults.configure(state="normal", bg='green')
        self.menu.entryconfig(4, state="normal")

def main():
    root = tk.Tk()
    #root.tk_setPalette(background='gray40', foreground='gray90', activeBackground='gray20', activeForeground='green yellow')
    root.title("Continuous Beam Analysis by the 3 Moment Method")
    app = Main_window(root)
    root.minsize(1400,600)
    root.mainloop()

if __name__ == '__main__':
    main()
