# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 15:00:06 2018

@author: DonB
"""

#pin pin beam with point moment
E_ksi = 29000.0
E_ksf = E_ksi * (144.0)
I_in4 = 30.8
I_ft4 = I_in4/(12.0**4)

m_ftkips = 10.0
a_ft = 4
l_ft = 10.0

rr_kips = m_ftkips/l_ft
rl_kips = -1.0*rr_kips

c2 = (-1.0/l_ft) * ((m_ftkips*a_ft**2) - (0.5*m_ftkips*a_ft**2) + (rl_kips * (l_ft**3/6.0)) + (0.5*m_ftkips*l_ft**2))
c1 = m_ftkips*a_ft + c2
c3 = 0
c4 = ((-1.0*rl_kips*l_ft**3)/6.0) - (0.5*m_ftkips*l_ft**2) - (c2*l_ft)

step = l_ft/100
station = []
v = []
m = []
eis = []
eid = []
x=0
for i in range(0,101):
    if i==0:
        x = 0
    else:
        x = x + step
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
    eis.append(eisx/(E_ksf*I_ft4))
    eid.append((eidx/(E_ksf*I_ft4))*12.0)
    station.append(x)