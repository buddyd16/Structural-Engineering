# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 21:39:19 2017

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
import scipy as sci
import scipy.integrate
import numpy as np

def udl_m(w,x,l):
    return (w*x)*(l-x)*(1/2.0)

l = 1       #ft
w = 1000     #kip per ft
E = 1.0
I = 1.0

n = max(int(round((l*12)/1.0)),500)     #intervals
step = (l*12)/n
xs = np.zeros(n+1)
ms = np.zeros(n+1)
m_ei = np.zeros(n+1)

for x in range(0,n+1):
    if x==0:
        xs[x] = 0
    else:
        xs[x] = (xs[x-1]+step)
    
    ms[x] = (udl_m(w/12.0,xs[x],l*12.0))
    m_ei[x] = (ms[x]/(E*I))
    
s_initial = ((w/12.0)*((l*12.0)**3))/(24*E*I)

s_cumtrapz = sci.integrate.cumtrapz(m_ei[:], xs[:], initial = 0) - [s_initial]

s_simps = np.zeros(n+1)

for x in range(0,n+1):
    if x == 0:
        s = 0
    else:
        if x == 1:
            s = sci.integrate.simps(m_ei[:x+1], xs[:x+1], even='avg')
        else:
            s = sci.integrate.simps(m_ei[:x+1], xs[:x+1], even='avg')
  
    s_simps[x] = s - s_initial


d_cumtrapz = sci.integrate.cumtrapz(s_cumtrapz[:], xs[:], initial = 0)

d_simps = np.zeros(n+1)

for x in range(0,n+1):
    if x == 0:
        d = 0
    else:
        if x == 1:
            d = sci.integrate.simps(s_simps[:x+1], xs[:x+1], even='avg')
        else:
            d = sci.integrate.simps(s_simps[:x+1], xs[:x+1], even='avg')
  
    d_simps[x] = d
