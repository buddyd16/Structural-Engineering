# -*- coding: utf-8 -*-
"""
Created on Tue Apr 03 14:02:16 2018

@author: DonB
"""
import numpy as np
import pin_pin_beam_equations_classes as ppb
import matplotlib.pyplot as plt

l = 10.0
l_step = l/500.0
xs = np.zeros(501)

xs[0] = 0

for i in range(1,501):
    xs[i] = xs[i-1] + l_step

D = ppb.pl(1,5,l).m(xs)
Ex = ppb.pl(0.1,5,l).m(xs)
Ey = ppb.pl(-0.1,5,l).m(xs)
F = ppb.pl(0.2,5,l).m(xs)
H = ppb.pl(0.3,5,l).m(xs)
L = ppb.pl(0.5,5,l).m(xs)
Lr = ppb.pl(0.4,5,l).m(xs)
R = ppb.pl(0.6,5,l).m(xs)
S = ppb.pl(0.7,5,l).m(xs)
Wx = ppb.pl(0.1,5,l).m(xs)
Wy = ppb.pl(-0.1,5,l).m(xs)

loads = np.array([[D],[Ex],[Ey],[F],[H],[L],[Lr],[R],[S],[Wx],[Wy]])

loads_not_squeeze = loads

loads = loads.squeeze()

basic_factors = np.array([[1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
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

basic_combos =['IBC_16_8','IBC_16_9','IBC_16_10_Lr',
                                     'IBC_16_10_R','IBC_16_10_S','IBC_16_11_Lr','IBC_16_11_R',
                                     'IBC_16_11_S','IBC_16_12_Wx','IBC_16_12_Wy','IBC_16_12_Ex',
                                     'IBC_16_12_Ey','IBC_16_13_Wx_Lr','IBC_16_13_Wx_R','IBC_16_13_Wx_S',
                                     'IBC_16_13_Wy_Lr','IBC_16_13_Wy_R','IBC_16_13_Wy_S','IBC_16_14_Ex','IBC_16_14_Ey',
                                     'IBC_16_15_Wx','IBC_16_15_Wy','IBC_16_16_Ex', 'IBC_16_16_Ey']

#combined = np.tensordot(basic_factors, loads, axes=([-1],[0]))
combined = np.dot(basic_factors, loads)

#combined = combined.squeeze()

max_ind = np.unravel_index(np.argmax(combined), combined.shape)

print (basic_combos[max_ind[0]])
print (xs[max_ind[1]])

max_flat = np.max(combined, axis=0).reshape(501,1)
min_flat = np.min(combined, axis=0).reshape(501,1)


for res in combined:
    plt.plot(xs, res, 'r--')
    
plt.plot(xs,max_flat)
plt.plot(xs,min_flat)

plt.show()
