# -*- coding: utf-8 -*-
"""
Created on Tue May 01 12:07:54 2018

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

import numpy as np

def fixed_end_moment_from_end_slope(eis0, eisL, L_in, end=[1,1]):
    
    if end[0] == 1 and end[1] == 1:
        s = np.array([[eis0],[eisL]])
        
        ems = np.array([[-1.0*L_in/3.0 , L_in/6.0],[L_in/6.0 , -1.0*L_in/3.0]])
        
        fem = np.linalg.solve(ems,s)
        
        fem_kft = fem / (-1.0 * 12.0)
        
    elif end[0] == 1 and end[1] == 0:
        fel_kft = ((eis0 * -3.0) / L_in)/ ( -1.0*12.0)
        fem_kft = np.array([[fel_kft],[0]])
    
    elif end[0] == 0 and end[1] == 1:
        fer_kft = ((eisL * -3.0) / L_in)/(-1.0*12.0)
        fem_kft = np.array([[0],[fer_kft]])
    
    else:
        fem_kft = np.array([[0],[0]])
    
    return fem_kft


E = 29000 #ksi
I = 30.8 #in4

#multiply end slopes in RAD by EI in ksi and In4
eis0 = E * I * -0.00321
eisL = E * I * 0.00266

L_ft = 10 #ft
L_in = L_ft * 12.0 #in

end_cond  = [1,1]

fem = fixed_end_moment_from_end_slope(eis0, eisL, L_in, end_cond)