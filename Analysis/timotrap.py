'''
Timoshenko derivation for trapezoidal loading
pin-pin single span beam

w1 - Load left end value
w2 - load right end value
a - load start point from left end of beam
b - load end point from left end of beam
c - load width = b - a
s - slope of load = (w2 - w1) / c
L - beam span

Reactions:
W = (w1 + w2)*c*0.5
sum Fy = 0 
--> RL + RR - W = 0
xbar = (c * ((2 * w2) + w1)) / (3 * (w2 + w1))
sum Mx,rl,cw+ = 0 
--> -RR*L + W*(a+xbar) = 0 
--> RR = W*(a+xbar) / L

RL = W - RR

Load Formulas:
0 < x < a:
w = 0

a < x < c:
w = -1*w1 - s(x-a)

c < x < L:
w = 0

Shear Formulas:
w = dV/dx, therefore V = integral w dx

0 < x < a:
V = c1

a < x < c:
V = -1*w1*x - (s(x-a)^2)/2 + c2

c < x < L:
V = c3

Moment Formulas:
V = dM/dx, therefore M = integral V dx

0 < x < a:
M = c1*x + c4

a < x < c:
M = (-1*w1*x^2)/2 - (s(x-a)^3)/6 + c2*x + c5

c < x < L:
M = c3*x + c6

Timoshenko Relationship for Rotation, theta, and Deflection, delta
M = -E*I d theta/dx
V = kAG (-theta + d delta/dx)

Rotation Formulas:
theta = integral M/-EI dx

0 < x < a:
theta = (-c1*x^2)/(2*EI) - c4*x/EI + c7

a < x < c:
theta = (w1*x^3)/(6*EI) + (s(x-a)^4)/(24*EI) - (c2*x^2)/2*EI - c5*x/EI + c8

c < x < L:
theta = (-c3*x^2)/(2*EI) - c6*x/EI + c9

Delta Formulas:
delta = integral V/kAG + theta dx

0 < x < a:
delta = c1*x/kAG + (-c1*x^3)/(6*EI) - c4*x^2/2*EI + c7*x + c10

a < x < c:
delta = -1*w1*x^2/2*kAG - (s(x-a)^3)/6*kAG + c2*x/kAG + (w1*x^4)/(24*EI) + (s(x-a)^5)/(120*EI) - (c2*x^3)/6*EI - c5*x^2/2*EI + c8*x + c11

c < x < L:
delta = c3*x/kAG + (-c3*x^3)/(6*EI) - c6*x^2/2*EI + c9*x + c12

Solve for Constants using boundary conditions and compatibility:
**Boundary @ x=0, V=RL:**
//c1 = RL

**Boundary @ x=L, V=-RR:**
//c3 = -RR

**Compatibility @ x=a, V=constant:**
c1 = -1*w1*a - (s(a-a)^2)/2 + c2
c1 = -1*w1*a + c2
c1 + 1*w1*a = c2

or

//-c1 + c2 = w1*a + (s(a-a)^2)/2

**Boundary @ x=0, M=0:**
//c4 = 0

**Boundary @ x=L, M=0:**
//c3*L + c6 = 0
c6 = -c3*L

**Compatibility @ x=a, M=constant:**
c1*a = (-1*w1*a^2)/2 - (s(a-a)^3)/6 + c2*a + c5
c1*a = (-1*w1*a^2)/2 + c2*a + c5
c1*a +(w1*a^2)/2 - c2*a = c5

or

//-c1*a + c2*a + c5 = (w1*a^2)/2 + (s(a-a)^3)/6

**Boundary @ x=0, delta=0:**
//c10 = 0

**Boundary @ x=L, delta=0:**
//0 = c3*L/kAG + (-c3*L^3)/(6*EI) - c6*L^2/2*EI + c9*L + c12
c12 = -c3*L/kAG + (c3*L^3)/(6*EI) + c6*L^2/2*EI - c9*L

**Compatibility @ x=a, delta=constant:**
c1*a/kAG + (-c1*a^3)/(6*EI) - c4*a^2/2*EI + c7*a = -1*w1*a^2/2*kAG - (s(a-a)^3)/6*kAG + c2*a/kAG + (w1*a^4)/(24*EI) + (s(a-a)^5)/(120*EI) - (c2*a^3)/6*EI - c5*a^2/2*EI + c8*a + c11
c1*a/kAG + (-c1*a^3)/(6*EI) - c4*a^2/2*EI + c7*a = -1*w1*a^2/2*kAG + c2*a/kAG + (w1*a^4)/(24*EI) - (c2*a^3)/6*EI - c5*a^2/2*EI + c8*a + c11
c11 = c1*a/kAG + (-c1*a^3)/(6*EI) - c4*a^2/2*EI + c7*a + w1*a^2/2*kAG - c2*a/kAG - (w1*a^4)/(24*EI) + (c2*a^3)/6*EI + c5*a^2/2*EI - c8*a

or
//c1*a/kAG + (-c1*a^3)/(6*EI) - c2*a/kAG + (c2*a^3)/6*EI - c4*a^2/2*EI + c5*a^2/2*EI + c7*a - c8*a - c11 = -1*w1*a^2/2*kAG - (s(a-a)^3)/6*kAG  + (w1*a^4)/(24*EI) + (s(a-a)^5)/(120*EI)

backsub of c8:
c11 = c1*a/kAG + (-c1*a^3)/(6*EI) - c4*a^2/2*EI + c7*a + w1*a^2/2*kAG - c2*a/kAG + (-1*w1*a^4)/(24*EI) + (c2*a^3)/6*EI + c5*a^2/2*EI + (w1*a^4)/(6*EI) - (c2*a^3)/2*EI - c5*a^2/EI + (c1*a^3)/(2*EI) + c4*a^2/EI - c7*a
C11 = c1*a/kAG + (c1*a^3)/(3*EI) + c4*a^2/2*EI + w1*a^2/2*kAG - c2*a/kAG + (w1*a^4)/(8*EI) - (c2*a^3)/3*EI - c5*a^2/2*EI

**Compatibility @ x=a, theta=constant:**
(-c1*a^2)/(2*EI) - c4*a/EI + c7 = (w1*a^3)/(6*EI) + (s(a-a)^4)/(24*EI) - (c2*a^2)/2*EI - c5*a/EI + c8
(-c1*a^2)/(2*EI) - c4*a/EI + c7 = (w1*a^3)/(6*EI) - (c2*a^2)/2*EI - c5*a/EI + c8
c7 = (c1*a^2)/(2*EI) + c4*a/EI + (w1*a^3)/(6*EI) - (c2*a^2)/2*EI - c5*a/EI + c8
or
c8 = (-1*w1*a^3)/(6*EI) + (c2*a^2)/2*EI + c5*a/EI + (-c1*a^2)/(2*EI) - c4*a/EI + c7 -- back sub into c11 and solve

or
//(-c1*a^2)/(2*EI) + (c2*a^2)/2*EI - c4*a/EI + c5*a/EI + c7 - c8 = (w1*a^3)/(6*EI) + (s(a-a)^4)/(24*EI)

**Compatibility @ x=c, theta = constant:**
(w1*c^3)/(6*EI) + (s(c-a)^4)/(24*EI) - (c2*c^2)/2*EI - c5*c/EI + c8 = (-c3*c^2)/(2*EI) - c6*c/EI + c9
c9 = (c3*c^2)/(2*EI) + c6*c/EI + (w1*c^3)/(6*EI) + (s(c-a)^4)/(24*EI) - (c2*c^2)/2*EI - c5*c/EI + c8

or
//(-c2*c^2)/2*EI + (c3*c^2)/(2*EI) - c5*c/EI + c6*c/EI + c8 - c9 = (-1*w1*c^3)/(6*EI) - (s(c-a)^4)/(24*EI)


**Compatibility @ x=c, delta = constant:**
c3*c/kAG + (-c3*c^3)/(6*EI) - c6*c^2/2*EI + c9*c + c12 = -1*w1*c^2/2*kAG - (s(c-a)^3)/6*kAG + c2*c/kAG + (w1*c^4)/(24*EI) + (s(c-a)^5)/(120*EI) - (c2*c^3)/6*EI - c5*c^2/2*EI + c8*c + c11
c3*c/kAG + (-c3*c^3)/(6*EI) - c6*c^2/2*EI + c9*c - c3*L/kAG + (c3*L^3)/(6*EI) + c6*L^2/2*EI - c9*L = -1*w1*c^2/2*kAG - (s(c-a)^3)/6*kAG + c2*c/kAG + (w1*c^4)/(24*EI) + (s(c-a)^5)/(120*EI) - (c2*c^3)/6*EI - c5*c^2/2*EI + c8*c + c1*a/kAG + (c1*a^3)/(3*EI) + c4*a^2/2*EI - w1*a^2/2*kAG - c2*a/kAG - (w1*a^4)/(8*EI) - (c2*a^3)/3*EI - c5*a^2/2*EI
c3*c/kAG + (-c3*c^3)/(6*EI) - c6*c^2/2*EI + (c3*c^3)/(2*EI) + c6*c^2/EI + (-w1*c^4)/(6*EI) + (s*c*(c-a)^4)/(24*EI) - (c2*c^3)/2*EI - c5*c^2/EI + c8*c- c3*L/kAG + (c3*L^3)/(6*EI) + c6*L^2/2*EI - c9*L = w1*c^2/2*kAG - (s(c-a)^3)/6*kAG + c2*c/kAG + (-w1*c^4)/(24*EI) + (s(c-a)^5)/(120*EI) - (c2*c^3)/6*EI - c5*c^2/2*EI + c8*c + c1*a/kAG + (c1*a^3)/(3*EI) + c4*a^2/2*EI - w1*a^2/2*kAG - c2*a/kAG - (w1*a^4)/(8*EI) - (c2*a^3)/3*EI - c5*a^2/2*EI

c3*c/kAG - c3*L/kAG - w1*c^2/2*kAG + (s(c-a)^3)/6*kAG - c2*c/kAG + (-c3*c^3)/(6*EI) - c6*c^2/2*EI + (c3*c^3)/(2*EI) + c6*c^2/EI + (-w1*c^4)/(6*EI) + (s*c*(c-a)^4)/(24*EI) - (c2*c^3)/2*EI - c5*c^2/EI + (c3*L^3)/(6*EI) + c6*L^2/2*EI + (w1*c^4)/(24*EI) - (s(c-a)^5)/(120*EI) + (c2*c^3)/6*EI + c5*c^2/2*EI - c1*a/kAG - (c1*a^3)/(3*EI) - c4*a^2/2*EI + w1*a^2/2*kAG + c2*a/kAG + (w1*a^4)/(8*EI) + (c2*a^3)/3*EI + c5*a^2/2*EI = c9*L

or
//-c2*c/kAG + (c2*c^3)/6*EI + c3*c/kAG + (-c3*c^3)/(6*EI) + c5*c^2/2*EI - c6*c^2/2*EI - c8*c + c9*c - c11 + c12 = -1*w1*c^2/2*kAG - (s(c-a)^3)/6*kAG  + (w1*c^4)/(24*EI) + (s(c-a)^5)/(120*EI)

Alterative Matrix formulation for constants:
// above indicates formula in matrix
c1  [1,0,0,0,0,0,0,0,0,0,0,0] [RL]
c2  [-1,1,0,0,0,0,0,0,0,0,0,0] [w1*a]
c3  [0,0,1,0,0,0,0,0,0,0,0,0] [-RR]
c4  [0,0,0,1,0,0,0,0,0,0,0,0] [0]
c5  [-a,a,0,0,1,0,0,0,0,0,0,0] [(w1*a^2)/2]
c6  [0,0,L,0,0,1,0,0,0,0,0,0] [0]
c7  [(-1*a^2)/(2*EI),(a^2)/2*EI,0,-1*a/EI,a/EI,0,1,-1,0,0,0,0] [(w1*a^3)/(6*EI)]
c8  [0,(-1*c^2)/2*EI,(c^2)/(2*EI),0,-1*c/EI,c/EI,0,1,-1,0,0,0] [(-1*w1*c^3)/(6*EI) - (s(c-a)^4)/(24*EI)]
c9  [0,0,L/kAG + (-1*L^3)/(6*EI),0,0,-1*L^2/2*EI,0,0,L,0,0,1] [0]
c10  [0,0,0,0,0,0,0,0,0,1,0,0] [0]
c11  [a/kAG + (-1*a^3)/(6*EI),-1*a/kAG + (a^3)/6*EI,0,-1*a^2/2*EI,a^2/2*EI,0,a,-a,0,0,-1,0] [-1*w1*a^2/2*kAG + (w1*a^4)/(24*EI)]
c12  [0,-1*c/kAG + (c^3)/6*EI,c/kAG + (-1*c^3)/(6*EI),0,c^2/2*EI,-1*c^2/2*EI,0,-1*c,c,0,-1,1] [-1*w1*c^2/2*kAG - (s(c-a)^3)/6*kAG  + (w1*c^4)/(24*EI) + (s(c-a)^5)/(120*EI)]
'''

from __future__ import division
import numpy as np
import math

w1= 1
w2= 0.5
a= 3
b= 7
d= b - a
s= (w2 - w1) / d
L=10

W = (w1 + w2)*d*0.5
xbar = (d * ((2 * w2) + w1)) / (3 * (w2 + w1))

RR = W*(a+xbar) / L
RL = W - RR

print RL,RR

#Material and Cross section data
E = 29000*math.pow(12,2)
I = 30.8 * 1/math.pow(12,4)
kA = 1.34 * 1/math.pow(12,2)
#kA = 10000000000000000
G = E /(2+(2*0.3))

#Boundary and Compatibility equation
#Lists of coefficients and lists of associated equalities

bc1_coeff = [1,0,0,0,0,0,0,0,0,0,0,0] 
bc1_eq = [RL]

bc2_coeff = [-1,1,0,0,0,0,0,0,0,0,0,0] 
bc2_eq = [w1*a]

bc3_coeff = [0,0,1,0,0,0,0,0,0,0,0,0]
bc3_eq = [-1*RR]

bc4_coeff = [0,0,0,1,0,0,0,0,0,0,0,0] 
bc4_eq = [0]

bc5_coeff = [-1*a,a,0,0,1,0,0,0,0,0,0,0]
bc5_eq = [(w1*math.pow(a,2))/2.0]

bc6_coeff = [0,0,L,0,0,1,0,0,0,0,0,0]
bc6_eq = [0]

bc7_coeff = [(-1*math.pow(a,2))/(2*E*I),(math.pow(a,2))/(2*E*I),0,-1*a/(E*I),a/(E*I),0,1,-1,0,0,0,0] 
bc7_eq = [(w1*math.pow(a,3))/(6*E*I)]

bc8_coeff = [0,
             (-1*math.pow(d,2))/(2*E*I),
             (math.pow(d,2))/(2*E*I),
             0,
             -1*d/(E*I),
             d/(E*I),
             0,
             1,
             -1,
             0,
             0,
             0] 
bc8_eq = [(-1*w1*math.pow(d,3))/(6*E*I) - (s*math.pow((d-a),4))/(24*E*I)]
 
bc9_coeff = [0,0,(L/(kA*G)) + ((-1*math.pow(L,3))/(6*E*I)),0,0,-1*math.pow(L,2)/(2*E*I),0,0,L,0,0,1]
bc9_eq = [0]

bc10_coeff = [0,0,0,0,0,0,0,0,0,1,0,0] 
bc10_eq = [0]

bc11_coeff = [(a/(kA*G)) + ((-1*math.pow(a,3))/(6*E*I)),(-1*a/(kA*G)) + ((math.pow(a,3))/(6*E*I)),0,((-1*math.pow(a,2))/(2*E*I)),(math.pow(a,2)/(2*E*I)),0,a,-1*a,0,0,-1,0]
bc11_eq = [(-1*w1*math.pow(a,2)/(2*kA*G)) + ((w1*math.pow(a,4))/(24*E*I))]

bc12_coeff = [0,(-1*d/(kA*G)) + ((math.pow(d,3))/(6*E*I)),(d/(kA*G)) + ((-1*math.pow(d,3))/(6*E*I)),0,math.pow(d,2)/(2*E*I),-1*math.pow(d,2)/(2*E*I),0,-1*d,d,0,-1,1] 
bc12_eq = [((-1*w1*math.pow(d,2))/(2*kA*G)) - ((s*math.pow((d-a),3))/(6*kA*G)) + ((w1*math.pow(d,4))/(24*E*I)) + ((s*math.pow((d-a),5))/(120*E*I))]


bceq = [bc1_coeff,bc2_coeff,bc3_coeff,bc4_coeff,bc5_coeff,bc6_coeff,bc7_coeff,bc8_coeff,bc9_coeff,bc10_coeff,bc11_coeff,bc12_coeff]
bcs = [bc1_eq,bc2_eq,bc3_eq,bc4_eq,bc5_eq,bc6_eq,bc7_eq,bc8_eq,bc9_eq,bc10_eq,bc11_eq,bc12_eq]

bceq = np.array(bceq)
bcs = np.array(bcs)

c = np.linalg.solve(bceq,bcs)


x=5.0
delta5 = ((-1*w1*math.pow(x,2)/(2*kA*G)) - 
        ((s*math.pow((x-a),3))/(6*kA*G)) + 
        ((c[1]*x)/(kA*G)) + 
        ((w1*math.pow(x,4))/(24*E*I)) + 
        ((s*math.pow((x-a),5))/(120*E*I)) - 
        ((c[1]*math.pow(x,3))/(6*E*I)) - 
        (c[4]*math.pow(x,2)/(2*E*I)) + 
        c[7]*x + 
        c[10]) * 12.0

Moment5 = (((-1*w1*math.pow(x,2))/2.0) - 
            ((s*math.pow((x-a),3))/6.0) + 
            (c[1]*x) + 
            c[4])
            
x2 = 2.0

delta2 = ((((c[0]*x2)/(kA*G)) + 
        ((-1*c[0]*math.pow(x2,3))/(6*E*I)) - 
        ((c[3]*math.pow(x2,2))/(2*E*I)) + 
        (c[6]*x2) + 
        c[9])) * 12.0

Moment2 = c[0]*x2 + c[3]