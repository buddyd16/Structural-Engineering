# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 15:00:06 2018

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

import scipy as sci
import scipy.integrate

#pin pin beam with point moment
E_ksi = 29000.0
E_ksf = E_ksi * (144.0)
I_in4 = 30.8
I_ft4 = I_in4/(12.0**4)

m_ftkips = 2.0
a_ft = 3
l_ft = 10.0

rr_kips = m_ftkips/l_ft
rl_kips = -1.0*rr_kips

c2 = (-1.0/l_ft) * ((m_ftkips*a_ft**2) - (0.5*m_ftkips*a_ft**2) + (rl_kips * (l_ft**3/6.0)) + (0.5*m_ftkips*l_ft**2))
c1 = m_ftkips*a_ft + c2
c3 = 0
c4 = ((-1.0*rl_kips*l_ft**3)/6.0) - (0.5*m_ftkips*l_ft**2) - (c2*l_ft)

step = l_ft/1000
station = []
v = []
m = []
eis = []
eid = []
x=0
xs=[0]
for i in range(0,1001):
    if i==0:
        x = 0
    else:
        x = x + step
        xs.append(x)
    v.append(rl_kips)
    
    if x <= a_ft:
        mx = rl_kips * x
        eisx = (0.5*rl_kips*x**2) + c1
        eidx = ((1/6.0)*rl_kips*x**3) + (c1*x) + c3
        
    else:
        mx = (rl_kips * x) + m_ftkips
        eisx = (0.5*rl_kips*x**2) + (m_ftkips*x) + c2
        eidx = (1/6.0)*rl_kips*x**3 + (0.5*m_ftkips*x**2) + (c2*x) + c4   
    
    m.append(mx)
    eis.append(eisx)
    eid.append(eidx)
    station.append(x)

m_xx=[]
A = sci.integrate.simps(m, xs)    
for i in range(len(xs)):
    m_xx.append(m[i]*xs[i])
    
xl = (1/A)*sci.integrate.simps(m_xx, xs)
xr = l_ft - xl

Aal = (6.0*A*xl / l_ft)
Aar = (6.0*A*xr / l_ft)