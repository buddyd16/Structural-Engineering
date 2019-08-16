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
w = w1 - s(x-a)

c < x < L:
w = 0

Shear Formulas:
w = dV/dx, therefore V = integral w dx

0 < x < a:
V = c1

a < x < c:
V = w1*x - (s(x-a)^2)/2 + c2

c < x < L:
V = c3

Moment Formulas:
V = dM/dx, therefore M = integral V dx

0 < x < a:
M = c1*x + c4

a < x < c:
M = (w1*x^2)/2 - (s(x-a)^3)/6 + c2*x + c5

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
theta = (-w1*x^3)/(6*EI) + (s(x-a)^4)/(24*EI) - (c2*x^2)/2*EI - c5*x/EI + c8

c < x < L:
theta = (-c3*x^2)/(2*EI) - c6*x/EI + c9

Delta Formulas:
delta = integral V/kAG + theta dx

0 < x < a:
delta = c1*x/kAG + (-c1*x^3)/(6*EI) - c4*x^2/2*EI + c7*x + c10

a < x < c:
delta = w1*x^2/2*kAG - (s(x-a)^3)/6*kAG + c2*x/kAG + (-w1*x^4)/(24*EI) + (s(x-a)^5)/(120*EI) - (c2*x^3)/6*EI - c5*x^2/2*EI + c8*x + c11

c < x < L:
delta = c3*x/kAG + (-c3*x^3)/(6*EI) - c6*x^2/2*EI + c9*x + c12

Solve for Constants using boundary conditions and compatibility:
**Boundary @ x=0, V=RL:**
//c1 = RL

**Boundary @ x=L, V=-RR:**
//c3 = -RR

**Compatibility @ x=a, V=constant:**
c1 = w1*a - (s(a-a)^2)/2 + c2
c1 = w1*a + c2
c1 / w1*a = c2

or

//-c1 + c2 = -w1*a + (s(a-a)^2)/2

**Boundary @ x=0, M=0:**
//c4 = 0

**Boundary @ x=L, M=0:**
//c3*L + c6 = 0
c6 = -c3*L

**Compatibility @ x=a, M=constant:**
c1*a = (w1*a^2)/2 - (s(a-a)^3)/6 + c2*a + c5
c1*a = (w1*a^2)/2 + c2*a + c5
c1*a -(w1*a^2)/2 - c2*a = c5

or

//-c1*a + c2*a + c5 = (-w1*a^2)/2 + (s(a-a)^3)/6

**Boundary @ x=0, delta=0:**
//c10 = 0

**Boundary @ x=L, delta=0:**
//0 = c3*L/kAG + (-c3*L^3)/(6*EI) - c6*L^2/2*EI + c9*L + c12
c12 = -c3*L/kAG + (c3*L^3)/(6*EI) + c6*L^2/2*EI - c9*L

**Compatibility @ x=a, delta=constant:**
c1*a/kAG + (-c1*a^3)/(6*EI) - c4*a^2/2*EI + c7*a = w1*a^2/2*kAG - (s(a-a)^3)/6*kAG + c2*a/kAG + (-w1*a^4)/(24*EI) + (s(a-a)^5)/(120*EI) - (c2*a^3)/6*EI - c5*a^2/2*EI + c8*a + c11
c1*a/kAG + (-c1*a^3)/(6*EI) - c4*a^2/2*EI + c7*a = w1*a^2/2*kAG + c2*a/kAG + (-w1*a^4)/(24*EI) - (c2*a^3)/6*EI - c5*a^2/2*EI + c8*a + c11
c11 = c1*a/kAG + (-c1*a^3)/(6*EI) - c4*a^2/2*EI + c7*a - w1*a^2/2*kAG - c2*a/kAG + (w1*a^4)/(24*EI) + (c2*a^3)/6*EI + c5*a^2/2*EI - c8*a

or
//c1*a/kAG + (-c1*a^3)/(6*EI) - c2*a/kAG + (c2*a^3)/6*EI - c4*a^2/2*EI + c5*a^2/2*EI + c7*a - c8*a - c11 = w1*a^2/2*kAG - (s(a-a)^3)/6*kAG  + (-w1*a^4)/(24*EI) + (s(a-a)^5)/(120*EI)

backsub of c8:
c11 = c1*a/kAG + (-c1*a^3)/(6*EI) - c4*a^2/2*EI + c7*a - w1*a^2/2*kAG - c2*a/kAG + (w1*a^4)/(24*EI) + (c2*a^3)/6*EI + c5*a^2/2*EI - (w1*a^4)/(6*EI) - (c2*a^3)/2*EI - c5*a^2/EI + (c1*a^3)/(2*EI) + c4*a^2/EI - c7*a
C11 = c1*a/kAG + (c1*a^3)/(3*EI) + c4*a^2/2*EI - w1*a^2/2*kAG - c2*a/kAG - (w1*a^4)/(8*EI) - (c2*a^3)/3*EI - c5*a^2/2*EI

**Compatibility @ x=a, theta=constant:**
(-c1*a^2)/(2*EI) - c4*a/EI + c7 = (-w1*a^3)/(6*EI) + (s(a-a)^4)/(24*EI) - (c2*a^2)/2*EI - c5*a/EI + c8
(-c1*a^2)/(2*EI) - c4*a/EI + c7 = (-w1*a^3)/(6*EI) - (c2*a^2)/2*EI - c5*a/EI + c8
c7 = (c1*a^2)/(2*EI) + c4*a/EI + (-w1*a^3)/(6*EI) - (c2*a^2)/2*EI - c5*a/EI + c8
or
c8 = (w1*a^3)/(6*EI) + (c2*a^2)/2*EI + c5*a/EI + (-c1*a^2)/(2*EI) - c4*a/EI + c7 -- back sub into c11 and solve

or
//(-c1*a^2)/(2*EI) + (c2*a^2)/2*EI - c4*a/EI + c5*a/EI + c7 - c8 = (-w1*a^3)/(6*EI) + (s(a-a)^4)/(24*EI)

**Compatibility @ x=c, theta = constant:**
(-w1*c^3)/(6*EI) + (s(c-a)^4)/(24*EI) - (c2*c^2)/2*EI - c5*c/EI + c8 = (-c3*c^2)/(2*EI) - c6*c/EI + c9
c9 = (c3*c^2)/(2*EI) + c6*c/EI + (-w1*c^3)/(6*EI) + (s(c-a)^4)/(24*EI) - (c2*c^2)/2*EI - c5*c/EI + c8

or
//(-c2*c^2)/2*EI + (c3*c^2)/(2*EI) - c5*c/EI + c6*c/EI + c8 - c9 = (w1*c^3)/(6*EI) - (s(c-a)^4)/(24*EI)


**Compatibility @ x=c, delta = constant:**
c3*c/kAG + (-c3*c^3)/(6*EI) - c6*c^2/2*EI + c9*c + c12 = w1*c^2/2*kAG - (s(c-a)^3)/6*kAG + c2*c/kAG + (-w1*c^4)/(24*EI) + (s(c-a)^5)/(120*EI) - (c2*c^3)/6*EI - c5*c^2/2*EI + c8*c + c11
c3*c/kAG + (-c3*c^3)/(6*EI) - c6*c^2/2*EI + c9*c - c3*L/kAG + (c3*L^3)/(6*EI) + c6*L^2/2*EI - c9*L = w1*c^2/2*kAG - (s(c-a)^3)/6*kAG + c2*c/kAG + (-w1*c^4)/(24*EI) + (s(c-a)^5)/(120*EI) - (c2*c^3)/6*EI - c5*c^2/2*EI + c8*c + c1*a/kAG + (c1*a^3)/(3*EI) + c4*a^2/2*EI - w1*a^2/2*kAG - c2*a/kAG - (w1*a^4)/(8*EI) - (c2*a^3)/3*EI - c5*a^2/2*EI
c3*c/kAG + (-c3*c^3)/(6*EI) - c6*c^2/2*EI + (c3*c^3)/(2*EI) + c6*c^2/EI + (-w1*c^4)/(6*EI) + (s*c*(c-a)^4)/(24*EI) - (c2*c^3)/2*EI - c5*c^2/EI + c8*c- c3*L/kAG + (c3*L^3)/(6*EI) + c6*L^2/2*EI - c9*L = w1*c^2/2*kAG - (s(c-a)^3)/6*kAG + c2*c/kAG + (-w1*c^4)/(24*EI) + (s(c-a)^5)/(120*EI) - (c2*c^3)/6*EI - c5*c^2/2*EI + c8*c + c1*a/kAG + (c1*a^3)/(3*EI) + c4*a^2/2*EI - w1*a^2/2*kAG - c2*a/kAG - (w1*a^4)/(8*EI) - (c2*a^3)/3*EI - c5*a^2/2*EI

c3*c/kAG - c3*L/kAG - w1*c^2/2*kAG + (s(c-a)^3)/6*kAG - c2*c/kAG + (-c3*c^3)/(6*EI) - c6*c^2/2*EI + (c3*c^3)/(2*EI) + c6*c^2/EI + (-w1*c^4)/(6*EI) + (s*c*(c-a)^4)/(24*EI) - (c2*c^3)/2*EI - c5*c^2/EI + (c3*L^3)/(6*EI) + c6*L^2/2*EI + (w1*c^4)/(24*EI) - (s(c-a)^5)/(120*EI) + (c2*c^3)/6*EI + c5*c^2/2*EI - c1*a/kAG - (c1*a^3)/(3*EI) - c4*a^2/2*EI + w1*a^2/2*kAG + c2*a/kAG + (w1*a^4)/(8*EI) + (c2*a^3)/3*EI + c5*a^2/2*EI = c9*L

or
//-c2*c/kAG + (c2*c^3)/6*EI + c3*c/kAG + (-c3*c^3)/(6*EI) + c5*c^2/2*EI - c6*c^2/2*EI - c8*c + c9*c - c11 + c12 = w1*c^2/2*kAG - (s(c-a)^3)/6*kAG  + (-w1*c^4)/(24*EI) + (s(c-a)^5)/(120*EI)

Alterative Matrix formulation for constants:
// above indicates formula in matrix
c1  [1,0,0,0,0,0,0,0,0,0,0,0] [RL]
c2  [-1,1,0,0,0,0,0,0,0,0,0,0] [-w1*a]
c3  [0,0,1,0,0,0,0,0,0,0,0,0] [-RR]
c4  [0,0,0,1,0,0,0,0,0,0,0,0] [0]
c5  [-a,a,0,0,1,0,0,0,0,0,0,0] [(-w1*a^2)/2]
c6  [0,0,L,0,0,1,0,0,0,0,0,0] [0]
c7  [(-1*a^2)/(2*EI),(a^2)/2*EI,0,-1*a/EI,a/EI,0,1,-1,0,0,0,0] [(-w1*a^3)/(6*EI)]
c8  [0,(-1*c^2)/2*EI,(c^2)/(2*EI),0,-1*c/EI,c/EI,0,1,-1,0,0,0] [(w1*c^3)/(6*EI) - (s(c-a)^4)/(24*EI)]
c9  [0,0,L/kAG + (-1*L^3)/(6*EI),0,0,-1*L^2/2*EI,0,0,L,0,0,1] [0]
c10  [0,0,0,0,0,0,0,0,0,1,0,0] [0]
c11  [a/kAG + (-1*a^3)/(6*EI),-1*a/kAG + (a^3)/6*EI,0,-1*a^2/2*EI,a^2/2*EI,0,a,-a,0,0,-1,0] [w1*a^2/2*kAG + (-w1*a^4)/(24*EI)]
c12  [0,-1*c/kAG + (c^3)/6*EI,c/kAG + (-1*c^3)/(6*EI),0,c^2/2*EI,-1*c^2/2*EI,0,-1*c,c,0,-1,1] [w1*c^2/2*kAG - (s(c-a)^3)/6*kAG  + (-w1*c^4)/(24*EI) + (s(c-a)^5)/(120*EI)]
