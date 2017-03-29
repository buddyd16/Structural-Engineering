#!/usr/bin/env python

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


def three_moment_method(beam_spans, beam_momentofinertia, cant, beam_loads_raw, E, iters):
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

        delta[j] = (-6*a_xl_xr[1,l]*a_xl_xr[0,l])/(beam_spans[l]*beam_momentofinertia[l])+(-6*a_xl_xr[2,r]*a_xl_xr[0,r])/(beam_spans[r]*beam_momentofinertia[r])

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

    #Cantilever Diagram Corrections

    if cant[0]=='L' or cant[0] =='B':
        v_diag[:,0] = -1*v_diag_cantL[:,0]
        m_diag[:,0] = m_diag_cantL[:,0]
        s_diag[:,0] = (sci.integrate.cumtrapz(m_diag[::-1,0],xs[:,0], initial = 0)/(E*beam_momentofinertia[0]))-slope[1,0]
        d_diag[:,0] = sci.integrate.cumtrapz(s_diag[:,0],xs[:,0], initial = 0)
        s_diag[:,0] = -1*s_diag[::-1,0]
        d_diag[:,0] = d_diag[::-1,0]

    else:
        pass

    if cant[0]=='R' or cant[0] =='B':
        v_diag[:,N-1] = -1*v_diag_cantR[:,N-1]
        m_diag[:,N-1] = m_diag_cantR[:,N-1]
        s_diag[:,N-1] = (sci.integrate.cumtrapz(m_diag[:,N-1],xs[:,N-1], initial = 0)/(E*beam_momentofinertia[N-1]))+slope[N-1,0]
        d_diag[:,N-1] = sci.integrate.cumtrapz(s_diag[:,N-1],xs[:,N-1], initial = 0)

    else:
        pass

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
        self.customfont = tkFont.Font(family="Helvetica", size=8)
        ## Main Frame
        self.main_frame = tk.Frame(self.master, bd=2, relief='sunken', padx=5,pady=5)
        self.main_frame.pack(anchor=tk.CENTER, padx= 10, pady= 5, fill=tk.BOTH)

        ## results selection Frame
        self.frame_selection = tk.Frame(self.main_frame, padx=5, pady=5)

        self.type_frame_select = tk.Frame(self.frame_selection, padx=1, pady=1)

        self.combo_type = tk.IntVar()
        self.base_type = tk.Radiobutton(self.type_frame_select, text = "Base Loads", variable=self.combo_type, value=3, command=self.base).pack(side=tk.TOP, anchor=tk.NW, padx= 5, pady= 1)
        self.asd_type = tk.Radiobutton(self.type_frame_select, text = "ASD/Basic", variable=self.combo_type, value=1, command=self.asd).pack(side=tk.TOP, anchor=tk.NW, padx= 5, pady= 1)
        self.lrfd_type = tk.Radiobutton(self.type_frame_select, text = "LRFD", variable=self.combo_type, value=2, command= self.lrfd).pack(side=tk.TOP, anchor=tk.NW, padx= 5, pady= 1)

        self.type_frame_select.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.BOTH)

        self.type_frame_select_env = tk.Frame(self.frame_selection, padx=1, pady=1)

        self.asd_envelope = tk.Radiobutton(self.type_frame_select_env, text = "ASD/Basic Envelope", variable=self.combo_type, value=4, command=self.asdenv).pack(side=tk.TOP, anchor=tk.NW, padx= 5, pady= 1)
        self.lrfd_envelope = tk.Radiobutton(self.type_frame_select_env, text = "LRFD Envelope", variable=self.combo_type, value=5, command= self.lrfdenv).pack(side=tk.TOP, anchor=tk.NW, padx= 5, pady= 1)

        self.type_frame_select_env.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.BOTH)

        self.combo_frame = tk.Frame(self.frame_selection, relief='sunken', padx=5, pady=5)

        self.asd_combo_btns = []
        self.lrfd_combo_btns = []
        self.base_btns = []
        self.asd_combo_btn = tk.IntVar()
        self.lrfd_combo_btn = tk.IntVar()
        self.base_combo_btn = tk.IntVar()

        asd_combos = Main_window.basic_combos
        lrfd_combos = Main_window.lrfd_combos
        load_types = ['D', 'Ex', 'Ey', 'F', 'H', 'L', 'Lr', 'R', 'S', 'Wx', 'Wy']

        self.base_frame = tk.Frame(self.combo_frame, padx=5, pady=5)

        for i in range(len(load_types)):
            self.base_btns.append(tk.Radiobutton(self.base_frame, text = load_types[i], variable=self.base_combo_btn, value=i+1, font=self.customfont, command= self.graph_start))
            self.base_btns[i].pack(side=tk.TOP, anchor=tk.NW, fill=tk.BOTH, padx= 5, pady= 5)

        self.base_frame.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.BOTH)
        self.asd_frame = tk.Frame(self.combo_frame, padx=1, pady=1)
        for i in range(len(asd_combos)):
            lbl = asd_combos[i]
            if asd_combos[i] == Main_window.asd_m_max[1]:
                lbl = lbl + '(M+)'
            else:
                pass
            if asd_combos[i] == Main_window.asd_m_min[1]:
                lbl = lbl + '(M-)'
            else:
                pass
            if asd_combos[i] == Main_window.asd_v_max[1]:
                lbl = lbl + '(V+)'
            else:
                pass
            if asd_combos[i] == Main_window.asd_v_min[1]:
                lbl = lbl + '(V-)'
            else:
                pass
            if asd_combos[i] == Main_window.asd_d_max[1]:
                lbl = lbl + '(D+)'
            else:
                pass
            if asd_combos[i] == Main_window.asd_d_min[1]:
                lbl = lbl + '(D-)'
            else:
                pass
            self.asd_combo_btns.append(tk.Radiobutton(self.asd_frame, text = lbl, variable=self.asd_combo_btn, value=i+1, font=self.customfont, command= self.graph_start))
            self.asd_combo_btns[i].pack(side=tk.TOP, anchor=tk.NW, fill=tk.BOTH, padx= 1, pady= 1)
        self.asd_frame.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.BOTH)

        self.lrfd_frame = tk.Frame(self.combo_frame, padx=5, pady=5)
        for i in range(len(lrfd_combos)):
            lbl = lrfd_combos[i]
            if lrfd_combos[i] == Main_window.lrfd_m_max[1]:
                lbl = lbl + '(M+)'
            else:
                pass
            if lrfd_combos[i] == Main_window.lrfd_m_min[1]:
                lbl = lbl + '(M-)'
            else:
                pass
            if lrfd_combos[i] == Main_window.lrfd_v_max[1]:
                lbl = lbl + '(V+)'
            else:
                pass
            if lrfd_combos[i] == Main_window.lrfd_v_min[1]:
                lbl = lbl + '(V-)'
            else:
                pass
            self.lrfd_combo_btns.append(tk.Radiobutton(self.lrfd_frame, text = lbl, variable=self.lrfd_combo_btn, value=i+1, font=self.customfont, command= self.graph_start))
            self.lrfd_combo_btns[i].pack(side=tk.TOP, anchor=tk.NW, fill=tk.BOTH, padx= 1, pady= 1)
        self.lrfd_frame.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.BOTH)

        self.combo_frame.pack(side=tk.TOP, anchor=tk.SE, fill=tk.BOTH)
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
        self.res_min_max = tk.Label(self.vmsd_frame, text="")
        self.res_min_max.pack(side=tk.LEFT)
        self.vmsd_frame.pack(side=tk.TOP)
        self.chart_frame = tk.Frame(self.selection_frame, padx=5, pady=5)

        self.Fig = matplotlib.figure.Figure(figsize=(9,5),dpi=100)
        self.FigSubPlot = self.Fig.add_subplot(111)
        self.FigSubPlot.grid(True)

        self.linevmsd = []
        self.lineenvmin = []
        self.linebm = []
        self.clabels = []
        self.clabels_pts = []
        for i in range(Main_window.xs.shape[1]):
            self.linebm.append(self.FigSubPlot.plot(Main_window.xs[:,i],Main_window.bm[:,i]))
            self.linevmsd.append(self.FigSubPlot.plot(Main_window.xs[:,i],Main_window.bm[:,i]))
            self.lineenvmin.append(self.FigSubPlot.plot(Main_window.xs[:,i],Main_window.bm[:,i]))

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

        self.label_error = tk.Label(self.master, text='Error Info')
        self.label_error.pack(side=tk.LEFT, anchor=tk.SE, padx=5, pady=5)

    def save_graph(self):
        self.Fig.savefig(self.path, dpi=150)

    def close_win(self):
        self.master.destroy()

    def graph_start(self):
        self.vmsd.set(1)


        combo = self.combo_type.get()

        #Main_window.LRFD_factors
        #Main_window.lrfd_combos
        #Main_window.basic_factors
        #Main_window.basic_combos
        load_types = ['D', 'Ex', 'Ey', 'F', 'H', 'L', 'Lr', 'R', 'S', 'Wx', 'Wy']

        if combo == 1:

            asd_combo = self.asd_combo_btn.get() - 1

            R = Main_window.asd_R[asd_combo]
            M = Main_window.asd_M[asd_combo]

            self.combo_string = Main_window.basic_combos[asd_combo] + ' - '
            for i in range(len(self.base_btns)):
                if len(Main_window.load_results[i][1]) == 0:
                    pass
                else:
                    self.combo_string = self.combo_string + ' {0:.2f}*{1} +'.format(Main_window.basic_factors[asd_combo][i],load_types[i])

        elif combo ==2:
            lrfd_combo = self.lrfd_combo_btn.get() - 1

            R = Main_window.lrfd_R[lrfd_combo]
            M = Main_window.lrfd_M[lrfd_combo]
            self.combo_string = Main_window.lrfd_combos[lrfd_combo] + ' - '
            for i in range(len(self.base_btns)):
                if len(Main_window.load_results[i][1]) == 0:
                    pass
                else:
                    self.combo_string = self.combo_string + ' {0:.2f}*{1} +'.format(Main_window.LRFD_factors[lrfd_combo][i],load_types[i])
        elif combo ==3:
            basic_combo = self.base_combo_btn.get() - 1

            R = Main_window.load_results[basic_combo][6]
            M = Main_window.load_results[basic_combo][7]

            self.combo_string = load_types[basic_combo] + '-'
        elif combo ==4:
            self.combo_string = 'ASD/BASIC Envelopes'
        elif combo ==5:
            self.combo_string = 'LRFD Envelopes'
        else:
            pass

        if combo ==4 or combo==5:
            r_string = ''
            m_string = ''
        else:
            r_string = 'Reactions (kips) : '
            for reaction in R:
                r_string = r_string + ' {0:.2f}  '.format(reaction[0]/1000)
            m_string = 'Support Moments (ft-kips) : '
            for moment in M:
                m_string = m_string + ' {0:.2f}  '.format(moment[0]/(1000*12))

        self.res_R.configure(text=r_string)
        self.res_M.configure(text=m_string)
        self.res_combo.configure(text=self.combo_string[:-1])
        self.vrun()


    def refreshFigure(self, x, y, yenv, dia, dec):
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
        dp = int(x.shape[0]/6)
        num_anno = int((x.shape[0])/dp)+1

        for j in range(x.shape[1]):
             for z in range(0,num_anno):
                 if z==0:
                     k=0
                 else:
                     if z*dp > x.shape[0]+1:
                         k=x.shape[0]+1
                     else:
                         k=z*dp

                 if dec == 3:
                    self.clabels.append(self.FigSubPlot.annotate('{0:.3f}'.format(y[k,j]),xy=(x[k,j],y[k,j]), xytext=(2.5,1), textcoords='offset points',fontsize=fsi))
                    if combo == 4 or combo == 5:
                        self.clabels.append(self.FigSubPlot.annotate('{0:.3f}'.format(yenv[k,j]),xy=(x[k,j],yenv[k,j]), xytext=(2.5,1), textcoords='offset points',fontsize=fsi))
                    else:
                        pass
                 elif dec ==4:
                    self.clabels.append(self.FigSubPlot.annotate('{0:.4f}'.format(y[k,j]),xy=(x[k,j],y[k,j]), xytext=(2.5,1), textcoords='offset points',fontsize=fsi))
                 else:
                    self.clabels.append(self.FigSubPlot.annotate('{0:.2f}'.format(y[k,j]),xy=(x[k,j],y[k,j]), xytext=(2.5,1), textcoords='offset points',fontsize=fsi))
                    if combo == 4 or combo == 5:
                        self.clabels.append(self.FigSubPlot.annotate('{0:.2f}'.format(yenv[k,j]),xy=(x[k,j],yenv[k,j]), xytext=(2.5,1), textcoords='offset points',fontsize=fsi))
                    else:
                        pass
                 self.clabels_pts.append(self.FigSubPlot.plot(x[k,j],y[k,j], 'ko', markersize=msi))
                 if combo == 4 or combo == 5:
                    self.clabels_pts.append(self.FigSubPlot.plot(x[k,j],yenv[k,j], 'ko', markersize=msi))
                 else:
                    pass
        ax = self.canvas.figure.axes[0]
        ax.set_xlim(x.min()+(x.min()*0.125), x.max()+(x.max()*0.125))
        if combo == 4 or combo == 5:
            ax.set_ylim(yenv.min()+(yenv.min()*0.125), y.max()+(y.max()*0.125))
        else:
            ax.set_ylim(y.min()+(y.min()*0.125), y.max()+(y.max()*0.125))
        self.FigSubPlot.set_xlabel('L (ft)')
        self.FigSubPlot.set_ylabel(dia)
        if combo == 4:
            self.FigSubPlot.set_title('ASD/BASIC Envelope')
        if combo == 5:
            self.FigSubPlot.set_title('LRFD Envelope')
        else:
            self.FigSubPlot.set_title(Main_window.calc_label+'\n'+self.combo_string[:-1])
        self.canvas.draw()

    def asd(self):
        for i in range(len(self.lrfd_combo_btns)):
            self.lrfd_combo_btns[i].config(state='disabled')
        for i in range(len(self.asd_combo_btns)):
            self.asd_combo_btns[i].config(state='normal')
        for i in range(len(self.base_btns)):
            self.base_btns[i].config(state='disabled')
        self.lrfd_combo_btn.set(0)
        self.base_combo_btn.set(0)
        self.s.config(state='normal')
        self.d.config(state='normal')

    def asdenv(self):
        for i in range(len(self.lrfd_combo_btns)):
            self.lrfd_combo_btns[i].config(state='disabled')
        for i in range(len(self.asd_combo_btns)):
            self.asd_combo_btns[i].config(state='disabled')
        for i in range(len(self.base_btns)):
            self.base_btns[i].config(state='disabled')
        self.lrfd_combo_btn.set(0)
        self.base_combo_btn.set(0)
        self.asd_combo_btn.set(0)
        self.s.config(state='disabled')
        self.d.config(state='normal')
        self.graph_start()

    def lrfdenv(self):
        for i in range(len(self.lrfd_combo_btns)):
            self.lrfd_combo_btns[i].config(state='disabled')
        for i in range(len(self.asd_combo_btns)):
            self.asd_combo_btns[i].config(state='disabled')
        for i in range(len(self.base_btns)):
            self.base_btns[i].config(state='disabled')
        self.lrfd_combo_btn.set(0)
        self.base_combo_btn.set(0)
        self.asd_combo_btn.set(0)
        self.s.config(state='disabled')
        self.d.config(state='disabled')
        self.graph_start()

    def lrfd(self):
        for i in range(len(self.lrfd_combo_btns)):
            self.lrfd_combo_btns[i].config(state='normal')
        for i in range(len(self.asd_combo_btns)):
            self.asd_combo_btns[i].config(state='disabled')
        for i in range(len(self.base_btns)):
            self.base_btns[i].config(state='disabled')

        self.asd_combo_btn.set(0)
        self.base_combo_btn.set(0)
        self.s.config(state='disabled')
        self.d.config(state='disabled')

    def base(self):
        for i in range(len(self.lrfd_combo_btns)):
            self.lrfd_combo_btns[i].config(state='disabled')
        for i in range(len(self.asd_combo_btns)):
            self.asd_combo_btns[i].config(state='disabled')
        for i in range(len(self.base_btns)):
            if len(Main_window.load_results[i][1]) == 0:
                self.base_btns[i].config(state='disabled')
            else:
                self.base_btns[i].config(state='normal')
        self.lrfd_combo_btn.set(0)
        self.asd_combo_btn.set(0)
        self.s.config(state='normal')
        self.d.config(state='normal')

    def vrun(self):
        combo = self.combo_type.get()
        dia = 'Shear (Kips)'

        if combo == 1:

            asd_combo = self.asd_combo_btn.get() - 1

            y = Main_window.basic_results_v[asd_combo]
            ymin = Main_window.bm
            x = Main_window.xs

            self.res_min_max.configure(text='   Max. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),y.min()))

            self.refreshFigure(x,y,ymin,dia,2)
        elif combo ==2:
            lrfd_combo = self.lrfd_combo_btn.get() - 1

            y = Main_window.lrfd_results_v[lrfd_combo]
            ymin = Main_window.bm
            x = Main_window.xs

            self.res_min_max.configure(text='   Max. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),y.min()))

            self.refreshFigure(x,y,ymin,dia,2)
        elif combo ==3:
            basic_combo = self.base_combo_btn.get() - 1

            y = Main_window.load_results[basic_combo][2]
            ymin = Main_window.bm
            x = Main_window.xs

            self.res_min_max.configure(text='   Max. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),y.min()))

            self.refreshFigure(x,y,ymin,dia,2)
        elif combo ==4:
            y = Main_window.asd_v_max_diag
            x = Main_window.xs
            ymin = Main_window.asd_v_min_diag

            self.res_min_max.configure(text='   Max. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),ymin.min()))
            self.refreshFigure(x,y,ymin,dia,2)
        elif combo ==5:
            y = Main_window.lrfd_v_max_diag
            x = Main_window.xs
            ymin = Main_window.lrfd_v_min_diag

            self.res_min_max.configure(text='   Max. V: {0:.2f} kips  Min. V: {1:.2f} kips'.format(y.max(),ymin.min()))
            self.refreshFigure(x,y,ymin,dia,2)
        else:
            pass

    def mrun(self):
        combo = self.combo_type.get()
        dia = 'Moment (Ft-Kips)'
        if combo == 1:

            asd_combo = self.asd_combo_btn.get() - 1

            y = Main_window.basic_results_m[asd_combo]
            ymin = Main_window.bm
            x = Main_window.xs

            self.res_min_max.configure(text='   Max. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),y.min()))

            self.refreshFigure(x,y,ymin,dia,2)
        elif combo ==2:
            lrfd_combo = self.lrfd_combo_btn.get() - 1

            y = Main_window.lrfd_results_m[lrfd_combo]
            ymin = Main_window.bm
            x = Main_window.xs

            self.res_min_max.configure(text='   Max. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),y.min()))

            self.refreshFigure(x,y,ymin,dia,2)
        elif combo ==3:
            basic_combo = self.base_combo_btn.get() - 1

            y = Main_window.load_results[basic_combo][3]
            ymin = Main_window.bm
            x = Main_window.xs

            self.res_min_max.configure(text='   Max. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),y.min()))

            self.refreshFigure(x,y,ymin,dia,2)
        elif combo ==4:
            y = Main_window.asd_m_max_diag
            x = Main_window.xs
            ymin = Main_window.asd_m_min_diag

            self.res_min_max.configure(text='   Max. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),ymin.min()))
            self.refreshFigure(x,y,ymin,dia,2)
        elif combo ==5:
            y = Main_window.lrfd_m_max_diag
            x = Main_window.xs
            ymin = Main_window.lrfd_m_min_diag

            self.res_min_max.configure(text='   Max. M: {0:.2f} ft-kips  Min. M: {1:.2f} ft-kips'.format(y.max(),ymin.min()))
            self.refreshFigure(x,y,ymin,dia,2)
        else:
            pass

    def srun(self):
        combo = self.combo_type.get()
        dia ='Slope (Rad)'
        if combo == 1:

            asd_combo = self.asd_combo_btn.get() - 1

            y = Main_window.basic_results_s[asd_combo]
            ymin = Main_window.bm
            x = Main_window.xs

            self.res_min_max.configure(text='   Max. S: {0:.4f} rad  Min. S: {1:.4f} rad'.format(y.max(),y.min()))

            self.refreshFigure(x,y,ymin,dia,4)
        elif combo ==2:
            pass
        elif combo ==3:
            basic_combo = self.base_combo_btn.get() - 1

            y = Main_window.load_results[basic_combo][4]
            ymin = Main_window.bm
            x = Main_window.xs

            self.res_min_max.configure(text='   Max. S: {0:.4f} rad  Min. S: {1:.4f} rad'.format(y.max(),y.min()))

            self.refreshFigure(x,y,ymin,dia,4)
        else:
            pass

    def drun(self):
        combo = self.combo_type.get()
        dia = 'Deflection (in)'
        if combo == 1:

            asd_combo = self.asd_combo_btn.get() - 1

            y = Main_window.basic_results_d[asd_combo]
            ymin = Main_window.bm
            x = Main_window.xs

            self.res_min_max.configure(text='   Max. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),y.min()))

            self.refreshFigure(x,y,ymin,dia,3)
        elif combo ==2:
            pass
        elif combo ==3:
            basic_combo = self.base_combo_btn.get() - 1

            y = Main_window.load_results[basic_combo][5]
            ymin = Main_window.bm
            x = Main_window.xs

            self.res_min_max.configure(text='   Max. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),y.min()))

            self.refreshFigure(x,y,ymin,dia,3)
        elif combo ==4:
            y = Main_window.asd_d_max_diag
            x = Main_window.xs
            ymin = Main_window.asd_d_min_diag

            self.res_min_max.configure(text='   Max. D: {0:.4f} in.  Min. D: {1:.4f} in.'.format(y.max(),ymin.min()))
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
        self.bminfol.grid(row=0,column=0, pady=10)
        self.e_bminfo = tk.Entry(self.main_frame,textvariable=self.bminfo)
        self.e_bminfo.grid(row=0,column=1, pady=10)

        self.E = tk.StringVar()
        self.El = tk.Label(self.main_frame, text="E (ksi) : \nGlobal = All Spans ")
        self.El.grid(row=1,column=0, pady=10)
        self.e_E = tk.Entry(self.main_frame,textvariable=self.E)
        self.e_E.grid(row=1,column=1, pady=10)

        self.span = tk.StringVar()
        self.spanl = tk.Label(self.main_frame, text="Span (ft) : ")
        self.spanl.grid(row=2,column=0)
        self.e_span = tk.Entry(self.main_frame,textvariable=self.span)
        self.e_span.grid(row=2,column=1)

        self.I = tk.StringVar()
        self.Il = tk.Label(self.main_frame, text="I (In^4) : ")
        self.Il.grid(row=3,column=0)
        self.e_I = tk.Entry(self.main_frame,textvariable=self.I)
        self.e_I.grid(row=3,column=1)

        self.cantl = tk.Label(self.main_frame, text="Cantilever L,R,B,N : ")
        self.cantl.grid(row=4,column=0)
        self.cant_in = tk.StringVar()
        self.cant_in.set('N')
        self.e_cant = tk.OptionMenu(self.main_frame,self.cant_in, 'L','R','B','N')
        self.e_cant.grid (row=4,column=1, padx= 10, sticky=tk.W)

        self.p_w1 = tk.StringVar()
        self.p_w1l = tk.Label(self.main_frame, text="P or w1 (kips/klf) : ")
        self.p_w1l.grid(row=5,column=0)
        self.e_p = tk.Entry(self.main_frame,textvariable=self.p_w1)
        self.e_p.grid(row=5,column=1)

        self.w2 = tk.StringVar()
        self.w2l = tk.Label(self.main_frame, text="w2 (klf) : ")
        self.w2l.grid(row=6,column=0)
        self.e_w2 = tk.Entry(self.main_frame,textvariable=self.w2)
        self.e_w2.grid(row=6,column=1)

        self.a = tk.StringVar()
        self.al = tk.Label(self.main_frame, text="a (ft) : ")
        self.al.grid(row=7,column=0)
        self.e_a = tk.Entry(self.main_frame,textvariable=self.a)
        self.e_a.grid(row=7,column=1)

        self.b =tk. StringVar()
        self.bl = tk.Label(self.main_frame, text="b (ft) : ")
        self.bl.grid(row=8,column=0)
        self.e_b = tk.Entry(self.main_frame,textvariable=self.b)
        self.e_b.grid(row=8,column=1)

        self.load_type = tk.StringVar()
        self.load_type.set('POINT')
        self.applied_loads_allow = ['POINT','UDL','TRAP']
        self.ltl = tk.Label(self.main_frame, text="Load Type (POINT, UDL, TRAP) : ")
        self.ltl.grid(row=9,column=0)
        self.e_load_type = tk.OptionMenu(self.main_frame,self.load_type,'POINT','UDL','TRAP')
        self.e_load_type.grid(row=9,column=1, padx= 10, sticky=tk.W)

        self.load_span = tk.IntVar()
        self.lsl = tk.Label(self.main_frame, text="Load in span : ")
        self.lsl.grid(row=10,column=0)
        self.e_load_span = tk.OptionMenu(self.main_frame, self.load_span, 1)
        self.e_load_span.grid(row=10,column=1, padx= 10, sticky=tk.W)

        self.load_types = ['D', 'Ex', 'Ey', 'F', 'H', 'L', 'Lr', 'R', 'S', 'Wx', 'Wy']
        self.load_kind = tk.StringVar()
        self.load_kind.set('D')
        self.lkl = tk.Label(self.main_frame, text='Load Type: ' + ','.join(self.load_types))
        self.lkl.grid(row=11,column=0)
        self.e_load_kind = tk.OptionMenu(self.main_frame, self.load_kind, 'D', 'Ex', 'Ey', 'F', 'H', 'L', 'Lr', 'R', 'S', 'Wx', 'Wy')
        self.e_load_kind.grid(row=11, column=1, padx= 10, sticky=tk.W)

        self.point_gif = PhotoImage(file="point.gif")
        self.point_key = tk.Label(self.main_frame,image=self.point_gif)
        self.point_key.point_gif = self.point_gif
        self.point_key.grid(row=13, column = 0, padx=5, pady=5)

        self.udl_gif = PhotoImage(file="udl.gif")
        self.udl_key = tk.Label(self.main_frame,image=self.udl_gif)
        self.udl_key.udl_gif = self.udl_gif
        self.udl_key.grid(row=13, column = 1, padx=5, pady=5)

        self.descript = tk.Label(self.main_frame, text= "Instructions:\n1. Input a Modulus of Elastiticity (E) this applies to all spans\n2. Input a span length and associated Moment of Inertia (I) for the span and click the 'Add Span' button\n     If needed the 'Remove Span' button deletes the last span entry and the 'Change Selected Span' button allows you to change the span selected in the table\n3. Enter Loading Data. The images provide a reference for the load input values.  and click the 'Add Load' button\n     Note: Wind and Seismic loads should be entered as ulitmate values - Load Combinations are based on IBC 2012\n     If needed the 'Remove Load' button deletes the last load entry and the 'Change Selected Load' button allows you to change the load selected in the table\n4. Click the 'Save Inputs' button, inputs are saved to 'Calculation Label_00_beam_info.txt' in a RESULTS folder on the users desktop in a subfolder with the Calculation Label\n5. Press the 'Run' button. During the calculation process results are saved in text files (.txt) to individual sub folders for all load combination and a final envelope results file is created in the main folder.\n     In addition DXF files are generated for all combinations, envelope conditions, and applied load types.\n6. Once 'Run' an independant results window becomes available which will display per combination or per load type results including reactions, support moments, shear, moment, slope, and deflection.\n     The controlling combinations will be labled as to what responce they control '(m+)(m-)' indicate positive and negative moment respectively similarly '(v+)(v-)' indicate positive and negative shear respectively", anchor='w', justify='left', width = 100, wraplength=750)
        self.descript.grid(row=13, column=4, columnspan=15, padx=5, pady=5)

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

        self.b1 = tk.Button(self.main_frame,text="Close", command=self.quit_app)
        self.b1.grid(row=14, column=19, padx=5, pady=5)
        self.bprint = tk.Button(self.main_frame,text="Save Inputs", command=self.print_ins)
        self.bprint.grid(row=14, column =18, padx=5, pady=5)
        self.b_span_add = tk.Button(self.main_frame,text="Add Span/I +", command=self.add_span)
        self.b_span_min = tk.Button(self.main_frame,text="Remove Span/I -", command=self.remove_span)
        self.b_span_change = tk.Button(self.main_frame, text="Change Selected Span", command=self.change_span)
        self.b_span_change.configure(state="disabled")
        self.b_load_add = tk.Button(self.main_frame,text="Add Load +", command=self.add_load)
        self.b_load_min = tk.Button(self.main_frame,text="Remove Load -", command=self.remove_load)
        self.b_load_change = tk.Button(self.main_frame, text="Change Selected Load", command=self.change_load)
        self.b_load_change.configure(state="disabled")
        self.b_span_add.grid(row=1, column=3, padx=5, pady=5)
        self.b_span_min.grid(row=2, column=3, padx=5, pady=5)
        self.b_span_change.grid(row=3, column=3, padx=5, pady=5)
        self.b_load_add.grid(row=5, column=3, padx=5, pady=5)
        self.b_load_min.grid(row=6, column=3, padx=5, pady=5)
        self.b_load_change.grid(row=7, column=3, padx=5, pady=5)

        self.brun = tk.Button(self.main_frame, text="Run", command= self.run_file)
        self.brun.configure(state="disabled", bg='red')
        self.brun.grid(row = 14, column=17, padx=5, pady=5)

        self.bresults = tk.Button(self.main_frame, text="Results", command= self.res_window)
        self.bresults.grid(row = 14, column=16, padx=5, pady=5)
        self.bresults.configure(state="disabled", bg='red')

        self.ins_validate()

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
        print filename
        calc_file = open(filename,'r')

        calc_data = calc_file.readlines()

        calc_file.close()

        beam_spans = []
        beam_momentofinertia=[]
        beam_elasticmodulus=[]
        beam_loads_raw = []
        cant = []

        i=0
        for line in calc_data:
            if i == 0:
                beam_label = line.rstrip('\n')
            elif i<5:
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
            elif i>6:
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

            file = open(os.path.join(path,label + '_00_beam_info.txt'),'w')
            file.write(label + '\n')
            file.write('L_ft')
            for line in p_spans:
                file.write(','+line)
            file.write('\nI_in4')
            for line in p_I:
                file.write(','+line)
            file.write('\nE_ksi,'+p_E+'\ncant,'+self.cant_in.get()+'\n**Loads**\n''p1(kips or klf)'',''p2(kips or klf)'',a,b,''POINT,UDL,TRAP'' **Do Not Delete This Line, Caps Matter for Load Type**,span\n')
            for line in p_loads:
                file.write(line + '\n')
            file.close()

            self.brun.configure(state="normal", bg='yellow')
            self.bprint.configure(state="normal", bg='green')
            self.menu.entryconfig(3, state="normal")

    def add_load(self):
        if self.e_p.get()=='' or self.e_w2.get()=='' or self.e_a.get()=='' or self.e_b.get()=='' or self.load_type.get()=='' or self.load_span.get() =='' or self.load_kind.get()=='':
            pass
        else:
            if self.load_type.get() in self.applied_loads_allow and self.load_kind.get() in self.load_types:
                load = '{0},{1},{2},{3},{4},{5},{6}'.format(self.e_p.get(),self.e_w2.get(),self.e_a.get(),self.e_b.get(),self.load_type.get(),self.load_span.get(),self.load_kind.get())
                self.lb_loads.insert(tk.END,load)
            else:
                pass

        self.ins_validate()

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

    def change_load(self):
        if self.e_p.get()=='' or self.e_w2.get()=='' or self.e_a.get()=='' or self.e_b.get()=='' or self.load_type.get()=='' or self.load_span.get() =='' or self.load_kind.get()=='':
            pass
        else:
            if self.load_type.get() in self.applied_loads_allow and self.load_kind.get() in self.load_types:
                load = '{0},{1},{2},{3},{4},{5},{6}'.format(self.e_p.get(),self.e_w2.get(),self.e_a.get(),self.e_b.get(),self.load_type.get(),self.load_span.get(),self.load_kind.get())
                self.lb_loads.delete(self.load_change_index)
                self.lb_loads.insert(self.load_change_index,load)
                self.b_load_change.configure(state="disabled")
            else:
                pass

        self.ins_validate()

    def add_span(self):
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
        self.ins_validate()

    def remove_span(self):
        self.lb_spans.delete(tk.END)
        self.lb_I.delete(tk.END)
        if self.e_span.get()=='' or self.lb_spans.size()==1:
            self.load_span.set(1)
            self._reset_option_menu([1])
        else:
            self._reset_option_menu(range(1,self.lb_spans.size()+1))
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
            elif i>6:
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
                holder.append((float(p[3])-float(p[2]))*12)
                holder.append(p[4])
                holder.append(int(p[5].replace('\n',''))-1)
                # load_types = ['D', 'Ex', 'Ey', 'F', 'H', 'L', 'Lr', 'R', 'S', 'Wx', 'Wy']
                if p[6].replace('\n','') == 'D':
                    dead.append(holder)
                elif p[6].replace('\n','') == 'Ex':
                    seismic_x.append(holder)
                elif p[6].replace('\n','') == 'Ey':
                    seismic_y.append(holder)
                elif p[6].replace('\n','') == 'F':
                    fluid.append(holder)
                elif p[6].replace('\n','') == 'H':
                    earth.append(holder)
                elif p[6].replace('\n','') == 'L':
                    live.append(holder)
                elif p[6].replace('\n','') == 'Lr':
                    live_roof.append(holder)
                elif p[6].replace('\n','') == 'R':
                    rain.append(holder)
                elif p[6].replace('\n','') == 'S':
                    snow.append(holder)
                elif p[6].replace('\n','') == 'Wx':
                    wind_x.append(holder)
                elif p[6].replace('\n','') == 'Wy':
                    wind_y.append(holder)
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
        iters = 1300
        N = len(beam_spans)
        live_deflection_goal = []
        total_deflection_goal = []

        for span in beam_spans:
            live_deflection_goal.append(span/360)
            total_deflection_goal.append(span/240)

        print 'Perform analysis for all load types defined....'

        for i in range(0,11):
            if len(loads[i][1]) == 0:
                pass
            else:
                Main_window.xs,loads[i][2],loads[i][3],loads[i][4],loads[i][5], loads[i][6], loads[i][7] = three_moment_method(beam_spans, beam_momentofinertia, cant, loads[i][1], E, iters)

        print '**Analysis Complete**'
        Main_window.load_results = loads
        Main_window.bm = np.zeros((iters+1,N))
        # ['D', 'Ex', 'Ey', 'F', 'H', 'L', 'Lr', 'R', 'S', 'Wx', 'Wy']

        print 'Factoring Loads and Generating Graphs...'

        fi = 1.0
        fy = 0.7
        Main_window.LRFD_factors = np.array([[1.4, 0.0, 0.0, 1.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
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
                                [1.2, 1.0, 0.0, 1.2, 1.6, fi, 0.0, fy, 0.0, 0.0, 0.0],
                                [1.2, 0.0, 1.0, 1.2, 1.6, fi, 0.0, fy, 0.0, 0.0, 0.0],
                                [0.9, 0.0, 0.0, 0.0, 1.6, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                                [0.9, 0.0, 0.0, 0.0, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                                [0.9, 1.0, 0.0, 0.9, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                [0.9, 0.0, 1.0, 0.9, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],])

        Main_window.lrfd_combos =['IBC_16_1','IBC_16_2_Lr','IBC_16_2_R','IBC_16_2_S','IBC_16_3_f1L_Lr',
                    'IBC_16_3_f1L_R','IBC_16_3_f1L_S','IBC_16_3_Wx_Lr','IBC_16_3_Wx_R',
                    'IBC_16_3_Wx_S','IBC_16_3_Wy_Lr','IBC_16_3_Wy_R','IBC_16_3_Wy_S',
                    'IBC_16_4_Wx_Lr','IBC_16_4_Wx_R','IBC_16_4_Wx_S','IBC_16_4_Wy_Lr',
                    'IBC_16_4_Wy_R','IBC_16_4_Wy_S','IBC_16_5_Ex','IBC_16_5_Ey','IBC_16_6_Wx',
                    'IBC_16_6_Wy','IBC_16_7_Ex','IBC_16_7_Ey' ]

        Main_window.basic_factors = np.array([[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                                [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
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
                                [0.6, 0.0, 0.7, 0.6, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])

        Main_window.basic_combos =['D','L_and_Lr','IBC_16_8','IBC_16_9','IBC_16_10_Lr',
                    'IBC_16_10_R','IBC_16_10_S','IBC_16_11_Lr','IBC_16_11_R',
                    'IBC_16_11_S','IBC_16_12_Wx','IBC_16_12_Wy','IBC_16_12_Ex',
                    'IBC_16_12_Ey','IBC_16_13_Wx_Lr','IBC_16_13_Wx_R','IBC_16_13_Wx_S',
                    'IBC_16_13_Wy_Lr','IBC_16_13_Wy_R','IBC_16_13_Wy_S','IBC_16_14_Ex','IBC_16_14_Ey',
                    'IBC_16_15_Wx','IBC_16_15_Wy','IBC_16_16_Ex', 'IBC_16_16_Ey']

        Main_window.lrfd_m_max = [0,0]
        Main_window.lrfd_m_min = [0,0]
        Main_window.lrfd_v_max = [0,0]
        Main_window.lrfd_v_min = [0,0]
        Main_window.asd_m_max = [0,0]
        Main_window.asd_m_min = [0,0]
        Main_window.asd_v_max = [0,0]
        Main_window.asd_v_min = [0,0]
        Main_window.asd_d_max = [0,0]
        Main_window.asd_d_min = [0,0]
        Main_window.lrfd_results_v = []
        Main_window.lrfd_results_m = []
        Main_window.basic_results_v = []
        Main_window.basic_results_m = []
        Main_window.basic_results_s = []
        Main_window.basic_results_d = []
        Main_window.lrfd_R=[]
        Main_window.lrfd_M=[]
        Main_window.asd_R=[]
        Main_window.asd_M=[]
        # Factor and combine loads and Print Results to text File
        print 'LRFD Combinations...'

        for i in range(0,25):
            combo = Main_window.lrfd_combos[i]
            path = os.path.join(os.path.expanduser('~'),'Desktop','RESULTS', bmlabel, 'LRFD', combo)

            path_exists(path)

            # ['D', 'Ex', 'Ey', 'F', 'H', 'L', 'Lr', 'R', 'S', 'Wx', 'Wy']

            v_diag = np.zeros((iters+1, N))
            m_diag = np.zeros((iters+1, N))

            R = np.zeros((N+1,1))
            M = np.zeros((N+1,1))

            for z in range(0,11):
                if type(loads[z][2]) == type(v_diag):
                    v_diag = v_diag + (loads[z][2]*Main_window.LRFD_factors[i,z])
                    m_diag = m_diag + (loads[z][3]*Main_window.LRFD_factors[i,z])

                    if m_diag.max() > Main_window.lrfd_m_max[0]:
                        Main_window.lrfd_m_max[0] = m_diag.max()
                        Main_window.lrfd_m_max[1] = combo
                    else:
                        pass
                    if m_diag.min() < Main_window.lrfd_m_min[0]:
                        Main_window.lrfd_m_min[0] = m_diag.min()
                        Main_window.lrfd_m_min[1] = combo
                    else:
                        pass
                    if v_diag.max() > Main_window.lrfd_v_max[0]:
                        Main_window.lrfd_v_max[0] = v_diag.max()
                        Main_window.lrfd_v_max[1] = combo
                    else:
                        pass
                    if v_diag.min() < Main_window.lrfd_v_min[0]:
                        Main_window.lrfd_v_min[0] = v_diag.min()
                        Main_window.lrfd_v_min[1] = combo
                    else:
                        pass

                else:
                    pass
            for j in range(0,N+1):
                z=0
                for z in range(0,11):
                    if type(loads[z][2]) == type(v_diag):
                        R[j] = R[j] + (loads[z][6][j]*Main_window.LRFD_factors[i,z])
                        M[j] = M[j] + (loads[z][7][j]*Main_window.LRFD_factors[i,z])
                    else:
                        pass
            Main_window.lrfd_results_v.append(v_diag)
            Main_window.lrfd_results_m.append(m_diag)
            Main_window.lrfd_R.append(R)
            Main_window.lrfd_M.append(M)

            vim,vjm = np.unravel_index(v_diag.argmax(),v_diag.shape)
            vin,vjn = np.unravel_index(v_diag.argmin(),v_diag.shape)
            mim,mjm = np.unravel_index(m_diag.argmax(),m_diag.shape)
            mi,mjn = np.unravel_index(m_diag.argmin(),m_diag.shape)


            file = open(os.path.join(path,bmlabel+combo+'_01_Results.txt'),'w')
            file.write('Beam Label: {0} \n\n'.format(bmlabel))
            file.write('IBC Combination: {0} \n\n'.format(combo))
            file.write('Reactions:\n')
            for j in range(0,N+1):
                file.write('{0:.3f} kips   '.format(float(R[j])/1000))
            file.write('\n\nSupport Moments:\n')
            for j in range(0,N+1):
                file.write('{0:.3f} ft-kips   '.format(float(M[j])/(1000*12)))
            file.write('\n\nMax/Min Shear:\n')
            file.write('Max: {0:.3f} kips @ {2:.3f} ft\nMin: {1:.3f} kips @ {3:.3f} ft   '.format(v_diag.max(),v_diag.min(), Main_window.xs[vim,vjm],Main_window.xs[vin,vjn]))
            file.write('\n\nMax/Min Moment:\n')
            file.write('Max: {0:.3f} ft-kips @ {2:.3f} ft\nMin: {1:.3f} ft-kips @ {3:.3f} ft   '.format(m_diag.max(),m_diag.min(), Main_window.xs[mim,mjm],Main_window.xs[mi,mjn]))
            file.write('\n\nPer Span Results:\n')
            for j in range(0,N):
                file.write('\nSpan {0:.1F}:\n\n'.format(j+1))
                file.write('{0:^20}{1:^20}{2:^20}\n'.format('x (ft)', 'v (kips)', 'M (ft-kips)'))
                for z in range(0,int(iters/25)+1):
                    if z==0:
                        k=0
                    else:
                        if z*25 > iters:
                            k=iters
                        else:
                            k=z*25
                    file.write('{0:^20.3f}{1:^20.3f}{2:^20.3f}\n'.format(Main_window.xs[k,j], v_diag[k,j],m_diag[k,j]))
            file.close()

            file = open(os.path.join(path,bmlabel+combo+'_02_Results_CAD.dxf'),'w')
            file.write('  0\nSECTION\n  2\nENTITIES\n')
            file.write('  0\nPOLYLINE\n  8\nspans\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            for j in range(0,N):
                file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n0.0\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)))
                file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n0.0\n 30\n0.0\n'.format((Main_window.xs[-1,j]*12)))
            file.write('  0\nSEQEND\n')
            for j in range(0,N):
                file.write('  0\nPOLYLINE\n 62\n16\n  8\nspans\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
                file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),m_diag.min()))
                file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),m_diag.max()))
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
            file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),m_diag.min()))
            file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),m_diag.max()))
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
                file.write('  0\nPOLYLINE\n 62\n8\n  8\nreactions\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),0.0))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0-(float(R[0])/1000))))
                file.write('  0\nSEQEND\n')
                file.write('  0\nPOLYLINE\n 62\n8\n  8\nreactions\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12)-(float(R[0])/10000),(0.0-(float(R[0])/10000))))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0)))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12)+(float(R[0])/10000),(0.0-(float(R[0])/10000))))
                file.write('  0\nSEQEND\n')
                file.write('  0\nTEXT\n 62\n9\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0-(float(R[0])/1000)), (float(R[0])/1000)))
            for j in range(1,N):
                file.write('  0\nPOLYLINE\n 62\n8\n  8\nreactions\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),0.0))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0-(float(R[j])/1000))))
                file.write('  0\nSEQEND\n')
                file.write('  0\nPOLYLINE\n 62\n8\n  8\nreactions\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)-(float(R[j])/10000),(0.0-(float(R[j])/10000))))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0)))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)+(float(R[j])/10000),(0.0-(float(R[j])/10000))))
                file.write('  0\nSEQEND\n')
                file.write('  0\nTEXT\n 62\n9\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0-(float(R[j])/1000)), (float(R[j])/1000)))
            if cant[0] == 'R' or cant[0] == 'B':
                pass
            else:
                file.write('  0\nPOLYLINE\n 62\n8\n  8\nreactions\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),0.0))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0-(float(R[N])/1000))))
                file.write('  0\nSEQEND\n')
                file.write('  0\nPOLYLINE\n 62\n8\n  8\nreactions\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12)-(float(R[N])/10000),(0.0-(float(R[N])/10000))))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0)))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12)+(float(R[N])/10000),(0.0-(float(R[N])/10000))))
                file.write('  0\nSEQEND\n')
                file.write('  0\nTEXT\n 62\n9\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0-(float(R[N])/1000)), (float(R[N])/1000)))
            file.write('  0\nPOLYLINE\n 62\n3\n  8\nshear\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            for j in range(0,N):
                for z in range(0,51):
                    if z==0:
                        k=0
                    else:
                        if z*int(iters/50) > iters:
                            k=iters
                        else:
                            k=z*int(iters/50)
                    file.write('  0\nVERTEX\n  8\nshear\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[k,j]*12), v_diag[k,j]))
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
                    if v_diag[l,j] > v_diag[k,j]:
                        file.write('  0\nTEXT\n 62\n3\n  8\nshear\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n-45.0\n'.format((Main_window.xs[k,j]*12), v_diag[k,j]))
                    else:
                        file.write('  0\nTEXT\n 62\n3\n  8\nshear\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n45.0\n'.format((Main_window.xs[k,j]*12), v_diag[k,j]))
            file.write('  0\nPOLYLINE\n 62\n5\n  8\nmoment\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            for j in range(0,N):
                for z in range(0,51):
                    if z==0:
                        k=0
                    else:
                        if z*int(iters/50) > iters:
                            k=iters
                        else:
                            k=z*int(iters/50)
                    file.write('  0\nVERTEX\n  8\nmoment\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[k,j]*12), m_diag[k,j]))
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
                    if m_diag[l,j] > m_diag[k,j]:
                        file.write('  0\nTEXT\n 62\n5\n  8\nmoment\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} ft-kips\n 50\n-45.0\n'.format((Main_window.xs[k,j]*12), m_diag[k,j]))
                    else:
                        file.write('  0\nTEXT\n 62\n5\n  8\nmoment\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} ft-kips\n 50\n45.0\n'.format((Main_window.xs[k,j]*12), m_diag[k,j]))
            file.write('  0\nENDSEC\n  0\nEOF')
            file.close()
            #Create and Print Graphs

            fsi = 5
            msi = 2
            dp = int(iters/6)
            num_anno = int((iters)/dp)+1

        # Basic Factor and combine loads and Print Results to text File
        print 'ASD/Basic Combinations...'

        for i in range(0,26):
            combo = Main_window.basic_combos[i]
            path = os.path.join(os.path.expanduser('~'),'Desktop','RESULTS', bmlabel, 'Basic_ASD', combo)

            path_exists(path)


            # ['D', 'Ex', 'Ey', 'F', 'H', 'L', 'Lr', 'R', 'S', 'Wx', 'Wy']

            v_diag = np.zeros((iters+1, N))
            m_diag = np.zeros((iters+1, N))
            s_diag = np.zeros((iters+1, N))
            d_diag = np.zeros((iters+1, N))
            R = np.zeros((N+1,1))
            M = np.zeros((N+1,1))

            for z in range(0,11):
                if type(loads[z][2]) == type(v_diag):
                    v_diag = v_diag + (loads[z][2]*Main_window.basic_factors[i,z])
                    m_diag = m_diag + (loads[z][3]*Main_window.basic_factors[i,z])
                    s_diag = s_diag + (loads[z][4]*Main_window.basic_factors[i,z])
                    d_diag = d_diag + (loads[z][5]*Main_window.basic_factors[i,z])
                else:
                    pass

                if m_diag.max() > Main_window.asd_m_max[0]:
                    Main_window.asd_m_max[0] = m_diag.max()
                    Main_window.asd_m_max[1] = combo
                else:
                    pass
                if m_diag.min() < Main_window.asd_m_min[0]:
                    Main_window.asd_m_min[0] = m_diag.min()
                    Main_window.asd_m_min[1] = combo
                else:
                    pass
                if v_diag.max() > Main_window.asd_v_max[0]:
                    Main_window.asd_v_max[0] = v_diag.max()
                    Main_window.asd_v_max[1] = combo
                else:
                    pass
                if v_diag.min() < Main_window.asd_v_min[0]:
                    Main_window.asd_v_min[0] = v_diag.min()
                    Main_window.asd_v_min[1] = combo
                else:
                    pass
                if d_diag.max() > Main_window.asd_d_max[0]:
                    Main_window.asd_d_max[0] = d_diag.max()
                    Main_window.asd_d_max[1] = combo
                else:
                    pass
                if d_diag.min() < Main_window.asd_d_min[0]:
                    Main_window.asd_d_min[0] = d_diag.min()
                    Main_window.asd_d_min[1] = combo
                else:
                    pass

            for j in range(0,N+1):
                z=0
                for z in range(0,11):
                    if type(loads[z][2]) == type(v_diag):
                        R[j] = R[j] + (loads[z][6][j]*Main_window.basic_factors[i,z])
                        M[j] = M[j] + (loads[z][7][j]*Main_window.basic_factors[i,z])
                    else:
                        pass

            Main_window.basic_results_v.append(v_diag)
            Main_window.basic_results_m.append(m_diag)
            Main_window.basic_results_s.append(s_diag)
            Main_window.basic_results_d.append(d_diag)
            Main_window.asd_R.append(R)
            Main_window.asd_M.append(M)

            vim,vjm = np.unravel_index(v_diag.argmax(),v_diag.shape)
            vin,vjn = np.unravel_index(v_diag.argmin(),v_diag.shape)
            mim,mjm = np.unravel_index(m_diag.argmax(),m_diag.shape)
            mi,mjn = np.unravel_index(m_diag.argmin(),m_diag.shape)
            dim,djm = np.unravel_index(d_diag.argmax(),d_diag.shape)
            din,djn = np.unravel_index(d_diag.argmin(),d_diag.shape)

            file = open(os.path.join(path,bmlabel+combo+'_01_Results.txt'),'w')
            file.write('Beam Label: {0} \n\n'.format(bmlabel))
            file.write('IBC Combination: {0} \n\n'.format(combo))
            file.write('Reactions:\n')
            for j in range(0,N+1):
                file.write('{0:.3f} kips   '.format(float(R[j])/1000))
            file.write('\n\nSupport Moments:\n')
            for j in range(0,N+1):
                file.write('{0:.3f} ft-kips   '.format(float(M[j])/(1000*12)))
            file.write('\n\nMax/Min Shear:\n')
            file.write('Max: {0:.3f} kips @ {2:.3f} ft\nMin: {1:.3f} kips @ {3:.3f} ft   '.format(v_diag.max(),v_diag.min(), Main_window.xs[vim,vjm],Main_window.xs[vin,vjn]))
            file.write('\n\nMax/Min Moment:\n')
            file.write('Max: {0:.3f} ft-kips @ {2:.3f} ft\nMin: {1:.3f} ft-kips @ {3:.3f} ft   '.format(m_diag.max(),m_diag.min(), Main_window.xs[mim,mjm],Main_window.xs[mi,mjn]))
            file.write('\n\nMax/Min Deflection:\n')
            file.write('Max: {0:.3f} in @ {2:.3f} ft\nMin: {1:.3f} in @ {3:.3f} ft   '.format(d_diag.max(),d_diag.min(), Main_window.xs[dim,djm],Main_window.xs[din,djn]))
            file.write('\n\nPer Span Results:\n')
            for j in range(0,N):
                file.write('\nSpan {0:.1F}:\n\n'.format(j+1))
                file.write('{0:^20}{1:^20}{2:^20}{3:^20}{4:^20}\n'.format('x (ft)', 'v (kips)', 'M (ft-kips)','S (rad)', 'D (in)'))
                for z in range(0,int(iters/25)+1):
                    if z==0:
                        k=0
                    else:
                        if z*25 > iters:
                            k=iters
                        else:
                            k=z*25
                    file.write('{0:^20.3f}{1:^20.3f}{2:^20.3f}{3:^20.3f}{4:^20.3f}\n'.format(Main_window.xs[k,j], v_diag[k,j],m_diag[k,j],s_diag[k,j],d_diag[k,j]))
            file.close()

            file = open(os.path.join(path,bmlabel+combo+'_02_Results_CAD.dxf'),'w')
            file.write('  0\nSECTION\n  2\nENTITIES\n')
            file.write('  0\nPOLYLINE\n  8\nspans\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            for j in range(0,N):
                file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n0.0\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)))
                file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n0.0\n 30\n0.0\n'.format((Main_window.xs[-1,j]*12)))
            file.write('  0\nSEQEND\n')
            for j in range(0,N):
                file.write('  0\nPOLYLINE\n 62\n16\n  8\nspans\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
                file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),m_diag.min()))
                file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),m_diag.max()))
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
            file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),m_diag.min()))
            file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),m_diag.max()))
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
                file.write('  0\nPOLYLINE\n 62\n8\n  8\nreactions\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),0.0))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0-(float(R[0])/1000))))
                file.write('  0\nSEQEND\n')
                file.write('  0\nPOLYLINE\n 62\n8\n  8\nreactions\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12)-(float(R[0])/10000),(0.0-(float(R[0])/10000))))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0)))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,0]*12)+(float(R[0])/10000),(0.0-(float(R[0])/10000))))
                file.write('  0\nSEQEND\n')
                file.write('  0\nTEXT\n 62\n9\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[0,0]*12),(0.0-(float(R[0])/1000)), (float(R[0])/1000)))
            for j in range(1,N):
                file.write('  0\nPOLYLINE\n 62\n8\n  8\nreactions\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),0.0))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0-(float(R[j])/1000))))
                file.write('  0\nSEQEND\n')
                file.write('  0\nPOLYLINE\n 62\n8\n  8\nreactions\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)-(float(R[j])/10000),(0.0-(float(R[j])/10000))))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0)))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)+(float(R[j])/10000),(0.0-(float(R[j])/10000))))
                file.write('  0\nSEQEND\n')
                file.write('  0\nTEXT\n 62\n9\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[0,j]*12),(0.0-(float(R[j])/1000)), (float(R[j])/1000)))
            if cant[0] == 'R' or cant[0] == 'B':
                pass
            else:
                file.write('  0\nPOLYLINE\n 62\n8\n  8\nreactions\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),0.0))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0-(float(R[N])/1000))))
                file.write('  0\nSEQEND\n')
                file.write('  0\nPOLYLINE\n 62\n8\n  8\nreactions\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12)-(float(R[N])/10000),(0.0-(float(R[N])/10000))))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0)))
                file.write('  0\nVERTEX\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12)+(float(R[N])/10000),(0.0-(float(R[N])/10000))))
                file.write('  0\nSEQEND\n')
                file.write('  0\nTEXT\n 62\n9\n  8\nreactions\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n0.0\n'.format((Main_window.xs[-1,N-1]*12),(0.0-(float(R[N])/1000)), (float(R[N])/1000)))
            file.write('  0\nPOLYLINE\n 62\n3\n  8\nshear\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            for j in range(0,N):
                for z in range(0,51):
                    if z==0:
                        k=0
                    else:
                        if z*int(iters/50) > iters:
                            k=iters
                        else:
                            k=z*int(iters/50)
                    file.write('  0\nVERTEX\n  8\nshear\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[k,j]*12), v_diag[k,j]))
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
                    if v_diag[l,j] > v_diag[k,j]:
                        file.write('  0\nTEXT\n 62\n3\n  8\nshear\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n-45.0\n'.format((Main_window.xs[k,j]*12), v_diag[k,j]))
                    else:
                        file.write('  0\nTEXT\n 62\n3\n  8\nshear\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} kips\n 50\n45.0\n'.format((Main_window.xs[k,j]*12), v_diag[k,j]))
            file.write('  0\nPOLYLINE\n 62\n5\n  8\nmoment\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            for j in range(0,N):
                for z in range(0,51):
                    if z==0:
                        k=0
                    else:
                        if z*int(iters/50) > iters:
                            k=iters
                        else:
                            k=z*int(iters/50)
                    file.write('  0\nVERTEX\n  8\nmoment\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[k,j]*12), m_diag[k,j]))
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
                    if m_diag[l,j] > m_diag[k,j]:
                        file.write('  0\nTEXT\n 62\n5\n  8\nmoment\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} ft-kips\n 50\n-45.0\n'.format((Main_window.xs[k,j]*12), m_diag[k,j]))
                    else:
                        file.write('  0\nTEXT\n 62\n5\n  8\nmoment\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{1:.3f} ft-kips\n 50\n45.0\n'.format((Main_window.xs[k,j]*12), m_diag[k,j]))
            file.write('  0\nPOLYLINE\n 62\n6\n  8\ndeflection\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            for j in range(0,N):
                for z in range(0,51):
                    if z==0:
                        k=0
                    else:
                        if z*int(iters/50) > iters:
                            k=iters
                        else:
                            k=z*int(iters/50)
                    file.write('  0\nVERTEX\n  8\ndeflection\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[k,j]*12), (d_diag[k,j]*100)))
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
                    if d_diag[l,j] > d_diag[k,j]:
                        file.write('  0\nTEXT\n 62\n6\n  8\ndeflection\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{2:.4f} in\n 50\n-45.0\n'.format((Main_window.xs[k,j]*12), (d_diag[k,j]*100),d_diag[k,j]))
                    else:
                        file.write('  0\nTEXT\n 62\n6\n  8\ndeflection\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{2:.4f} in\n 50\n45.0\n'.format((Main_window.xs[k,j]*12), (d_diag[k,j]*100),d_diag[k,j]))
            file.write('  0\nENDSEC\n  0\nEOF')
            file.close()
            #Create and Print Graphs
            fsi = 5
            msi = 2
            dp = int(iters/6)
            num_anno = int((iters)/dp)+1

        path = os.path.join(os.path.expanduser('~'),'Desktop','RESULTS', bmlabel)
        Main_window.lrfd_Rmax_print = np.maximum.reduce(Main_window.lrfd_R)
        Main_window.lrfd_Rmin_print = np.minimum.reduce(Main_window.lrfd_R)
        Main_window.lrfd_Mmax_print = np.maximum.reduce(Main_window.lrfd_M)
        Main_window.lrfd_Mmin_print = np.minimum.reduce(Main_window.lrfd_M)
        Main_window.asd_Rmax_print = np.maximum.reduce(Main_window.asd_R)
        Main_window.asd_Rmin_print = np.minimum.reduce(Main_window.asd_R)
        Main_window.asd_Mmax_print = np.maximum.reduce(Main_window.asd_M)
        Main_window.asd_Mmin_print = np.minimum.reduce(Main_window.asd_M)
        file = open(os.path.join(path,bmlabel+'_01_Max_Min_Results.txt'),'w')
        file.write('Beam Label: {0} \n\n'.format(bmlabel))
        file.write('Max Support Reactions - LRFD:\n')
        for j in range(0,N+1):
                file.write('{0:.3f} kips   '.format(float(Main_window.lrfd_Rmax_print[j])/1000))
        file.write('\n\nMax Support Moments - LRFD:\n')
        for j in range(0,N+1):
            file.write('{0:.3f} ft-kips   '.format(float(Main_window.lrfd_Mmax_print[j])/(1000*12)))
        file.write('\n\nMin Support Reactions - LRFD:\n')
        for j in range(0,N+1):
                file.write('{0:.3f} kips   '.format(float(Main_window.lrfd_Rmin_print[j])/1000))
        file.write('\n\nMin Support Moments - LRFD:\n')
        for j in range(0,N+1):
            file.write('{0:.3f} ft-kips   '.format(float(Main_window.lrfd_Mmin_print[j])/(1000*12)))
        file.write('\n\nMax Support Reactions - ASD/Basic:\n')
        for j in range(0,N+1):
                file.write('{0:.3f} kips   '.format(float(Main_window.asd_Rmax_print[j])/1000))
        file.write('\n\nMax Support Moments - ASD/Basic:\n')
        for j in range(0,N+1):
            file.write('{0:.3f} ft-kips   '.format(float(Main_window.asd_Mmax_print[j])/(1000*12)))
        file.write('\n\nMin Support Reactions - ASD/Basic:\n')
        for j in range(0,N+1):
                file.write('{0:.3f} kips   '.format(float(Main_window.asd_Rmin_print[j])/1000))
        file.write('\n\nMin Support Moments - ASD/Basic:\n')
        for j in range(0,N+1):
            file.write('{0:.3f} ft-kips   '.format(float(Main_window.asd_Mmin_print[j])/(1000*12)))
        file.write('\n\nMax/Min Shear :\n\nLRFD :\nMax: {0:.3f} Combo: {1}\nMin: {2:0.3f} Combo: {3}\n\n'.format(Main_window.lrfd_v_max[0],Main_window.lrfd_v_max[1],Main_window.lrfd_v_min[0],Main_window.lrfd_v_min[1]))
        file.write('ASD/Basic :\nMax: {0:.3f} Combo: {1}\nMin: {2:0.3f} Combo: {3}\n\n'.format(Main_window.asd_v_max[0],Main_window.asd_v_max[1],Main_window.asd_v_min[0],Main_window.asd_v_min[1]))
        file.write('Max/Min Moment :\n\nLRFD :\nMax: {0:.3f} Combo: {1}\nMin: {2:0.3f} Combo: {3}\n\n'.format(Main_window.lrfd_m_max[0],Main_window.lrfd_m_max[1],Main_window.lrfd_m_min[0],Main_window.lrfd_v_min[1]))
        file.write('ASD/Basic :\nMax: {0:.3f} Combo: {1}\nMin: {2:0.3f} Combo: {3}\n\n'.format(Main_window.asd_m_max[0],Main_window.asd_m_max[1],Main_window.asd_m_min[0],Main_window.asd_m_min[1]))
        file.write('Max/Min Deflection (ASD/Basic Only) :\n\nMax: {0:.3f} Combo: {1}\nMin: {2:0.3f} Combo: {3}\n\n'.format(Main_window.asd_d_max[0],Main_window.asd_d_max[1], Main_window.asd_d_min[0],Main_window.asd_d_min[1]))
        file.close()

        Main_window.lrfd_v_max_diag = np.maximum.reduce(Main_window.lrfd_results_v)
        Main_window.lrfd_v_min_diag = np.minimum.reduce(Main_window.lrfd_results_v)
        Main_window.lrfd_m_max_diag = np.maximum.reduce(Main_window.lrfd_results_m)
        Main_window.lrfd_m_min_diag = np.minimum.reduce(Main_window.lrfd_results_m)

        print 'Creating Envelope Graphs...'

        Main_window.asd_v_max_diag = np.maximum.reduce(Main_window.basic_results_v)
        Main_window.asd_v_min_diag = np.minimum.reduce(Main_window.basic_results_v)
        Main_window.asd_m_max_diag = np.maximum.reduce(Main_window.basic_results_m)
        Main_window.asd_m_min_diag = np.minimum.reduce(Main_window.basic_results_m)
        self.asd_s_max_diag = np.maximum.reduce(Main_window.basic_results_s)
        self.asd_s_min_diag = np.minimum.reduce(Main_window.basic_results_s)
        Main_window.asd_d_max_diag = np.maximum.reduce(Main_window.basic_results_d)
        Main_window.asd_d_min_diag = np.minimum.reduce(Main_window.basic_results_d)

        print 'DONE'

        #Create DXF of Envelope Results
        file = open(os.path.join(path,bmlabel+'_02_Envelope_Results.dxf'),'w')
        file.write('  0\nSECTION\n  2\nENTITIES\n')
        file.write('  0\nPOLYLINE\n  8\nspans\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
        for j in range(0,N):
            file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n0.0\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)))
            file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n0.0\n 30\n0.0\n'.format((Main_window.xs[-1,j]*12)))
        file.write('  0\nSEQEND\n')
        for j in range(0,N):
            file.write('  0\nPOLYLINE\n 62\n16\n  8\nspans\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),m_diag.min()))
            file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),m_diag.max()))
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
        file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),m_diag.min()))
        file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),m_diag.max()))
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
            for z in range(0,51):
                if z==0:
                    k=0
                else:
                    if z*int(iters/50) > iters:
                        k=iters
                    else:
                        k=z*int(iters/50)
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
            for z in range(0,51):
                if z==0:
                    k=0
                else:
                    if z*int(iters/50) > iters:
                        k=iters
                    else:
                        k=z*int(iters/50)
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
            for z in range(0,51):
                if z==0:
                    k=0
                else:
                    if z*int(iters/50) > iters:
                        k=iters
                    else:
                        k=z*int(iters/50)
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
            for z in range(0,51):
                if z==0:
                    k=0
                else:
                    if z*int(iters/50) > iters:
                        k=iters
                    else:
                        k=z*int(iters/50)
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
            for z in range(0,51):
                if z==0:
                    k=0
                else:
                    if z*int(iters/50) > iters:
                        k=iters
                    else:
                        k=z*int(iters/50)
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
            for z in range(0,51):
                if z==0:
                    k=0
                else:
                    if z*int(iters/50) > iters:
                        k=iters
                    else:
                        k=z*int(iters/50)
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
            for z in range(0,51):
                if z==0:
                    k=0
                else:
                    if z*int(iters/50) > iters:
                        k=iters
                    else:
                        k=z*int(iters/50)
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
            for z in range(0,51):
                if z==0:
                    k=0
                else:
                    if z*int(iters/50) > iters:
                        k=iters
                    else:
                        k=z*int(iters/50)
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
            for z in range(0,51):
                if z==0:
                    k=0
                else:
                    if z*int(iters/50) > iters:
                        k=iters
                    else:
                        k=z*int(iters/50)
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
            for z in range(0,51):
                if z==0:
                    k=0
                else:
                    if z*int(iters/50) > iters:
                        k=iters
                    else:
                        k=z*int(iters/50)
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

        #print loads[0][1][0]
        file = open(os.path.join(path,bmlabel+'_03_Loads.dxf'),'w')
        file.write('  0\nSECTION\n  2\nENTITIES\n')
        file.write('  0\nPOLYLINE\n  8\nspans\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
        for j in range(0,N):
            file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n0.0\n 30\n0.0\n'.format((Main_window.xs[0,j]*12)))
            file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n0.0\n 30\n0.0\n'.format((Main_window.xs[-1,j]*12)))
        file.write('  0\nSEQEND\n')
        for j in range(0,N):
            file.write('  0\nPOLYLINE\n 62\n16\n  8\nspans\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n')
            file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),m_diag.min()))
            file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[0,j]*12),m_diag.max()))
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
        file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),m_diag.min()))
        file.write('  0\nVERTEX\n  8\nspans\n 10\n{0:.3f}\n 20\n{1:.3f}\n 30\n0.0\n'.format((Main_window.xs[-1,N-1]*12),m_diag.max()))
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
        z=0
        colors = [10,40,50,80,130,160,190,210,7,8,16]
        for z in range(0,11):
            if type(loads[z][2]) == type(v_diag):
                layer = loads[z][0]
                item_count = 0
                for items in loads[z][1]:
                    p = items[0]
                    w2 = items[1]
                    if items[5]==0:
                        a = items[2]
                        b = items[3]+a
                    else:
                        a = items[2]+(Main_window.xs[-1,items[5]-1]*12)
                        b = items[3]+a
                    load_type = items[4]
                    item_count +=1
                    layerplot = layer + '_' + str(item_count)
                    if load_type == "POINT":
                        file.write('  0\nPOLYLINE\n 62\n{1}\n  8\n{0}\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n'.format(layerplot,colors[z]))
                        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layerplot,a,0.0))
                        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layerplot,a,(p/1000)))
                        file.write('  0\nSEQEND\n')
                        file.write('  0\nPOLYLINE\n 62\n{1}\n  8\n{0}\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n'.format(layerplot,colors[z]))
                        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layerplot,(a)-(float(p)/10000),(float(p)/10000)))
                        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layerplot,(a),(0.0)))
                        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layerplot,(a)+(float(p)/10000),(float(p)/10000)))
                        file.write('  0\nSEQEND\n')
                        file.write('  0\nTEXT\n 62\n{3}\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{2:.3f} kips\n 50\n0.0\n'.format(layerplot,a,(float(p)/1000),colors[z]))
                    elif load_type == "UDL":
                        file.write('  0\nPOLYLINE\n 62\n{1}\n  8\n{0}\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n'.format(layerplot,colors[z]))
                        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layerplot,a,0.0))
                        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layerplot,a,(p/(1000))*12))
                        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layerplot,b,(p/(1000))*12))
                        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layerplot,b,0.0))
                        file.write('  0\nSEQEND\n')
                        file.write('  0\nTEXT\n 62\n{3}\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{2:.3f} klf\n 50\n0.0\n'.format(layerplot,0.5*(a+b),(float(p)/1000)*12,colors[z]))
                    elif load_type == "TRAP":
                        file.write('  0\nPOLYLINE\n 62\n{1}\n  8\n{0}\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n'.format(layerplot,colors[z]))
                        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layerplot,a,0.0))
                        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layerplot,a,(p/(1000))*12))
                        #print('{0},{1}'.format(items[3],b))
                        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layerplot,b,(w2/(1000))*12))
                        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layerplot,b,0.0))
                        file.write('  0\nSEQEND\n')
                        file.write('  0\nTEXT\n 62\n{3}\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{2:.3f} klf\n 50\n45.0\n'.format(layerplot,a,(float(p)/1000)*12,colors[z]))
                        file.write('  0\nTEXT\n 62\n{3}\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{2:.3f} klf\n 50\n45.0\n'.format(layerplot,b,(float(w2)/1000)*12,colors[z]))
                    else:
                        pass
            
                if cant[0] == 'L' or cant[0] == 'B':
                    pass
                else:
                    file.write('  0\nPOLYLINE\n 62\n8\n  8\n{0}\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n'.format(layer+'_reactions'))
                    file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_reactions',(Main_window.xs[0,0]*12),0.0))
                    file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_reactions',(Main_window.xs[0,0]*12),(0.0-(float(loads[z][6][0])/1000))))
                    file.write('  0\nSEQEND\n')
                    file.write('  0\nPOLYLINE\n 62\n8\n  8\n{0}\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n'.format(layer+'_reactions'))
                    file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_reactions',(Main_window.xs[0,0]*12)-(float(loads[z][6][0])/10000),(0.0-(float(loads[z][6][0])/10000))))
                    file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_reactions',(Main_window.xs[0,0]*12),(0.0)))
                    file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_reactions',(Main_window.xs[0,0]*12)+(float(loads[z][6][0])/10000),(0.0-(float(loads[z][6][0])/10000))))
                    file.write('  0\nSEQEND\n')
                    file.write('  0\nTEXT\n 62\n9\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{3:.3f} kips\n 50\n0.0\n'.format(layer+'_reactions',(Main_window.xs[0,0]*12),(0.0-(float(loads[z][6][0])/1000)), (float(loads[z][6][0])/1000)))
                for j in range(1,N):
                    file.write('  0\nPOLYLINE\n 62\n8\n  8\n{0}\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n'.format(layer+'_reactions'))
                    file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_reactions',(Main_window.xs[0,j]*12),0.0))
                    file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_reactions',(Main_window.xs[0,j]*12),(0.0-(float(loads[z][6][j])/1000))))
                    file.write('  0\nSEQEND\n')
                    file.write('  0\nPOLYLINE\n 62\n8\n  8\n{0}\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n'.format(layer+'_reactions'))
                    file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_reactions',(Main_window.xs[0,j]*12)-(float(loads[z][6][j])/10000),(0.0-(float(loads[z][6][j])/10000))))
                    file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_reactions',(Main_window.xs[0,j]*12),(0.0)))
                    file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_reactions',(Main_window.xs[0,j]*12)+(float(loads[z][6][j])/10000),(0.0-(float(loads[z][6][j])/10000))))
                    file.write('  0\nSEQEND\n')
                    file.write('  0\nTEXT\n 62\n9\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{3:.3f} kips\n 50\n0.0\n'.format(layer+'_reactions',(Main_window.xs[0,j]*12),(0.0-(float(loads[z][6][j])/1000)), (float(loads[z][6][j])/1000)))
                if cant[0] == 'R' or cant[0] == 'B':
                    pass
                else:
                    file.write('  0\nPOLYLINE\n 62\n8\n  8\n{0}\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n'.format(layer+'_reactions'))
                    file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_reactions',(Main_window.xs[-1,N-1]*12),0.0))
                    file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_reactions',(Main_window.xs[-1,N-1]*12),(0.0-(float(loads[z][6][N])/1000))))
                    file.write('  0\nSEQEND\n')
                    file.write('  0\nPOLYLINE\n 62\n8\n  8\n{0}\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n'.format(layer+'_reactions'))
                    file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_reactions',(Main_window.xs[-1,N-1]*12)-(float(loads[z][6][N])/10000),(0.0-(float(loads[z][6][N])/10000))))
                    file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_reactions',(Main_window.xs[-1,N-1]*12),(0.0)))
                    file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_reactions',(Main_window.xs[-1,N-1]*12)+(float(loads[z][6][N])/10000),(0.0-(float(loads[z][6][N])/10000))))
                    file.write('  0\nSEQEND\n')
                    file.write('  0\nTEXT\n 62\n9\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{3:.3f} kips\n 50\n0.0\n'.format(layer+'_reactions',(Main_window.xs[-1,N-1]*12),(0.0-(float(loads[z][6][N])/1000)), (float(loads[z][6][N])/1000)))
                
                file.write('  0\nPOLYLINE\n 62\n3\n  8\n{0}\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n'.format(layer+'_shear'))
                for j in range(0,N):
                    for y in range(0,51):
                        if y==0:
                            k=0
                        else:
                            if y*int(iters/50) > iters:
                                k=iters
                            else:
                                k=y*int(iters/50)
                        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_shear',(Main_window.xs[k,j]*12), loads[z][2][k,j]))
                file.write('  0\nSEQEND\n')
                for j in range(0,N):
                    for y in range(0,5):
                        if y==0:
                            k=0
                            l=k+1
                        else:
                            if y*int(iters/4) >= iters:
                                k=iters
                                l=k
                            else:
                                k=y*int(iters/4)
                                l=k+1
                        if loads[z][2][l,j] > loads[z][2][k,j]:
                            file.write('  0\nTEXT\n 62\n3\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{2:.3f} kips\n 50\n-45.0\n'.format(layer+'_shear',(Main_window.xs[k,j]*12), loads[z][2][k,j]))
                        else:
                            file.write('  0\nTEXT\n 62\n3\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{2:.3f} kips\n 50\n45.0\n'.format(layer+'_shear',(Main_window.xs[k,j]*12), loads[z][2][k,j]))
                file.write('  0\nPOLYLINE\n 62\n5\n  8\n{0}\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n'.format(layer+'_moment'))
                for j in range(0,N):
                    for y in range(0,51):
                        if y==0:
                            k=0
                        else:
                            if y*int(iters/50) > iters:
                                k=iters
                            else:
                                k=y*int(iters/50)
                        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_moment',(Main_window.xs[k,j]*12), loads[z][3][k,j]))
                file.write('  0\nSEQEND\n')
                for j in range(0,N):
                    for y in range(0,5):
                        if y==0:
                            k=0
                            l=k+1
                        else:
                            if y*int(iters/4) >= iters:
                                k=iters
                                l=k
                            else:
                                k=y*int(iters/4)
                                l=k+1
                        if loads[z][3][l,j] > loads[z][3][k,j]:
                            file.write('  0\nTEXT\n 62\n5\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{2:.3f} ft-kips\n 50\n-45.0\n'.format(layer+'_moment',(Main_window.xs[k,j]*12), loads[z][3][k,j]))
                        else:
                            file.write('  0\nTEXT\n 62\n5\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{2:.3f} ft-kips\n 50\n45.0\n'.format(layer+'_moment',(Main_window.xs[k,j]*12), loads[z][3][k,j]))
                file.write('  0\nPOLYLINE\n 62\n6\n  8\n{0}\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n8\n'.format(layer+'_deflection'))
                for j in range(0,N):
                    for y in range(0,51):
                        if y==0:
                            k=0
                        else:
                            if y*int(iters/50) > iters:
                                k=iters
                            else:
                                k=y*int(iters/50)
                        file.write('  0\nVERTEX\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n'.format(layer+'_deflection',(Main_window.xs[k,j]*12), (loads[z][5][k,j]*100)))
                file.write('  0\nSEQEND\n')
                for j in range(0,N):
                    for y in range(0,5):
                        if y==0:
                            k=0
                            l=k+1
                        else:
                            if y*int(iters/4) >= iters:
                                k=iters
                                l=k
                            else:
                                k=y*int(iters/4)
                                l=k+1
                        if loads[z][5][l,j] > loads[z][5][k,j]:
                            file.write('  0\nTEXT\n 62\n6\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{3:.4f} in\n 50\n-45.0\n'.format(layer+'_deflection',(Main_window.xs[k,j]*12), (loads[z][5][k,j]*100),loads[z][5][k,j]))
                        else:
                            file.write('  0\nTEXT\n 62\n6\n  8\n{0}\n 10\n{1:.3f}\n 20\n{2:.3f}\n 30\n0.0\n 40\n1.0\n  1\n{3:.4f} in\n 50\n45.0\n'.format(layer+'_deflection',(Main_window.xs[k,j]*12), (loads[z][5][k,j]*100),loads[z][5][k,j]))
            else:
                pass
        file.write('  0\nENDSEC\n  0\nEOF')
        file.close()

        self.brun.configure(bg='green')
        self.bresults.configure(state="normal", bg='green')
        self.menu.entryconfig(4, state="normal")

def main():
    root = tk.Tk()
    root.title("Structura Beam - Continuous Beam Analysis by the 3 Moment Method")
    app = Main_window(root)
    root.minsize(1400,600)
    root.mainloop()

if __name__ == '__main__':
    main()
