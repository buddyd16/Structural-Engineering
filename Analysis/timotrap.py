
from __future__ import division
import numpy as np
import math
import TimoshenkoFormulas as timoforms

class VariableLoad:
    def __init__(self, w1, w2, a, b, L, E, I, G, kA):
        '''
        Timoshenko derivation for trapezoidal/variable loading
        pin-pin single span beam
        
        w1 - Load left end value
        w2 - load right end value
        a - load start point from left end of beam
        b - load end point from left end of beam
        d - load width = b - a
        s - slope of load = (w2 - w1) / d
        L - beam span
        E = beam modulus of elastacity
        I = beam second moment of area about the axis of bending
        G = beam shear modulus
        kA = beam shear area, typically the beam web area for steel W shapes
    
        sign convention:
         (+) positive moments are applied clockwise
         (+) positive reactions are in the (+) positive y direction
        '''
        self.w1 = w1
        self.w2 = w2
        self.a = a
        self.b = b
        self.L = L
        self.E = E
        self.I = I
        self.G = G
        self.kA = kA     
        
        d= b - a
        self.d = d
        s= (w2 - w1) / d
        self.s = s
        
        
        '''
        Reactions:
        W = (w1 + w2)*d*0.5
        sum Fy = 0 
        --> RL + RR - W = 0
        xbar = (d * ((2 * w2) + w1)) / (3 * (w2 + w1))
        sum Mx,rl,cw+ = 0 
        --> -RR*L + W*(a+xbar) = 0 
        --> RR = W*(a+xbar) / L
        
        RL = W - RR
        '''
    
        W = (w1 + w2)*d*0.5
        self.W = W
        xbar = (d * ((2 * w2) + w1)) / (3 * (w2 + w1))
        self.xbar = xbar
    
        RR = W*(a+xbar) / L
        RL = W - RR
        
        self.RR = RR
        self.RL = RL
    
        #Boundary and Compatibility equation
        #Lists of coefficients and lists of associated equalities
        '''
        Solve for Constants using boundary conditions and compatibility:
        **Boundary @ x=0, V=RL:**
        //c1 = RL
        
        **Boundary @ x=L, V=-RR:**
        //c3 = -RR
        
        **Compatibility @ x=a, V=constant:**
        c1 = -1*w1*a - (s(a-a)^2)/2 + c2
        
        //-c1 + c2 = w1*a
        
        **Boundary @ x=0, M=0:**
        //c4 = 0
        
        **Boundary @ x=L, M=0:**
        //c3*L + c6 = 0
        c6 = -c3*L
        
        **Compatibility @ x=a, M=constant:**
        c1*a = (-1*w1*a^2)/2 - (s(a-a)^3)/6 + c2*a + c5
        
        //-c1*a + c2*a + c5 = (w1*a^2)/2 + (s(a-a)^3)/6
        
        **Boundary @ x=0, delta=0:**
        //c10 = 0
        
        **Boundary @ x=L, delta=0:**
        //0 = c3*L/kAG + (-c3*L^3)/(6*EI) - c6*L^2/2*EI + c9*L + c12
        
        **Compatibility @ x=a, delta=constant:**
        c1*a/kAG + (-c1*a^3)/(6*EI) - c4*a^2/2*EI + c7*a = 
        -1*w1*a^2/2*kAG - (s(a-a)^3)/6*kAG + c2*a/kAG + (w1*a^4)/(24*EI) + (s(a-a)^5)/(120*EI) - (c2*a^3)/6*EI - c5*a^2/2*EI + c8*a + c11
        
        //c1*a/kAG + (-c1*a^3)/(6*EI) - c2*a/kAG + (c2*a^3)/6*EI - c4*a^2/2*EI + c5*a^2/2*EI + c7*a - c8*a - c11 = 
        -1*w1*a^2/2*kAG + (w1*a^4)/(24*EI)
        
        **Compatibility @ x=a, theta=constant:**
        (-c1*a^2)/(2*EI) - c4*a/EI + c7 = (w1*a^3)/(6*EI) + (s(a-a)^4)/(24*EI) - (c2*a^2)/2*EI - c5*a/EI + c8
        
        //(-c1*a^2)/(2*EI) + (c2*a^2)/2*EI - c4*a/EI + c5*a/EI + c7 - c8 = (w1*a^3)/(6*EI)
        
        **Compatibility @ x=b, theta = constant:**
        (w1*b^3)/(6*EI) + (s(b-a)^4)/(24*EI) - (c2*b^2)/2*EI - c5*b/EI + c8 = (-c3*b^2)/(2*EI) - c6*b/EI + c9
        
        //(-c2*b^2)/2*EI + (c3*b^2)/(2*EI) - c5*b/EI + c6*b/EI + c8 - c9 = (-1*w1*b^3)/(6*EI) - (s(b-a)^4)/(24*EI)
        
        
        **Compatibility @ x=b, delta = constant:**
        c3*b/kAG + (-c3*b^3)/(6*EI) - c6*b^2/2*EI + c9*b + c12 = 
        -1*w1*b^2/2*kAG - (s(b-a)^3)/6*kAG + c2*b/kAG + (w1*b^4)/(24*EI) + (s(b-a)^5)/(120*EI) - (c2*b^3)/6*EI - c5*b^2/2*EI + c8*b + c11
        
        //-c2*b/kAG + (c2*b^3)/6*EI + c3*b/kAG + (-c3*b^3)/(6*EI) + c5*b^2/2*EI - c6*b^2/2*EI - c8*b + c9*b - c11 + c12 = -1*w1*b^2/2*kAG - (s(b-a)^3)/6*kAG  + (w1*b^4)/(24*EI) + (s(b-a)^5)/(120*EI)
        
        Matrix formulation for constants:
        // above indicates formula in matrix
        c1  [1,0,0,0,0,0,0,0,0,0,0,0] [RL]
        c2  [-1,1,0,0,0,0,0,0,0,0,0,0] [w1*a]
        c3  [0,0,1,0,0,0,0,0,0,0,0,0] [-RR]
        c4  [0,0,0,1,0,0,0,0,0,0,0,0] [0]
        c5  [-a,a,0,0,1,0,0,0,0,0,0,0] [(w1*a^2)/2]
        c6  [0,0,L,0,0,1,0,0,0,0,0,0] [0]
        c7  [(-1*a^2)/(2*EI),(a^2)/2*EI,0,-1*a/EI,a/EI,0,1,-1,0,0,0,0] [(w1*a^3)/(6*EI)]
        c8  [0,(-1*b^2)/2*EI,(b^2)/(2*EI),0,-1*b/EI,b/EI,0,1,-1,0,0,0] [(-1*w1*b^3)/(6*EI) - (s(b-a)^4)/(24*EI)]
        c9  [0,0,L/kAG + (-1*L^3)/(6*EI),0,0,-1*L^2/2*EI,0,0,L,0,0,1] [0]
        c10  [0,0,0,0,0,0,0,0,0,1,0,0] [0]
        c11  [a/kAG + (-1*a^3)/(6*EI),-1*a/kAG + (a^3)/6*EI,0,-1*a^2/2*EI,a^2/2*EI,0,a,-a,0,0,-1,0] [-1*w1*a^2/2*kAG + (w1*a^4)/(24*EI)]
        c12  [0,-1*b/kAG + (b^3)/6*EI,d/kAG + (-1*b^3)/(6*EI),0,b^2/2*EI,-1*b^2/2*EI,0,-1*b,b,0,-1,1] [-1*w1*b^2/2*kAG - (s(b-a)^3)/6*kAG  + (w1*b^4)/(24*EI) + (s(b-a)^5)/(120*EI)]
        '''
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
                     (-1*math.pow(b,2))/(2*E*I),
                     (math.pow(b,2))/(2*E*I),
                     0,
                     -1*b/(E*I),
                     b/(E*I),
                     0,
                     1,
                     -1,
                     0,
                     0,
                     0]
                     
        bc8_eq = [((-1*w1*math.pow(b,3))/(6*E*I)) - ((s*math.pow((b-a),4))/(24*E*I))]
         
        bc9_coeff = [0,0,(L/(kA*G)) + ((-1*math.pow(L,3))/(6*E*I)),0,0,-1*math.pow(L,2)/(2*E*I),0,0,L,0,0,1]
        bc9_eq = [0]
        
        bc10_coeff = [0,0,0,0,0,0,0,0,0,1,0,0] 
        bc10_eq = [0]
        
        bc11_coeff = [(a/(kA*G)) + ((-1*math.pow(a,3))/(6*E*I)),
                      (-1*a/(kA*G)) + ((math.pow(a,3))/(6*E*I)),
                        0,
                        ((-1*math.pow(a,2))/(2*E*I)),
                        (math.pow(a,2)/(2*E*I)),
                        0,
                        a,
                        -1*a,
                        0,
                        0,
                        -1,
                        0]
                        
        bc11_eq = [(-1*w1*math.pow(a,2)/(2*kA*G)) + ((w1*math.pow(a,4))/(24*E*I))]
        
        bc12_coeff = [0,
                      (-1*b/(kA*G)) + ((math.pow(b,3))/(6*E*I)),
                        (b/(kA*G)) + ((-1*math.pow(b,3))/(6*E*I)),
                        0,
                        math.pow(b,2)/(2*E*I),
                        -1*math.pow(b,2)/(2*E*I),
                        0,
                        -1*b,
                        b,
                        0,
                        -1,
                        1]
                        
        bc12_eq = [((-1*w1*math.pow(b,2))/(2*kA*G)) - ((s*math.pow((b-a),3))/(6*kA*G)) + ((w1*math.pow(b,4))/(24*E*I)) + ((s*math.pow((b-a),5))/(120*E*I))]
        
        
        bceq = [bc1_coeff,bc2_coeff,bc3_coeff,bc4_coeff,bc5_coeff,bc6_coeff,bc7_coeff,bc8_coeff,bc9_coeff,bc10_coeff,bc11_coeff,bc12_coeff]
        bcs = [bc1_eq,bc2_eq,bc3_eq,bc4_eq,bc5_eq,bc6_eq,bc7_eq,bc8_eq,bc9_eq,bc10_eq,bc11_eq,bc12_eq]
        
        bceq = np.array(bceq)
        bcs = np.array(bcs)
        
        c = np.linalg.solve(bceq,bcs)  
        self.c = c
        
    '''
    Load Formulas:
    0 < x < a:
    w = 0
    
    a < x < b:
    w = -1*w1 - s(x-a)
    
    b < x < L:
    w = 0
    
    Shear Formulas:
    w = dV/dx, therefore V = integral w dx
    
    0 < x < a:
    V = c1
    
    a < x < b:
    V = -1*w1*x - (s(x-a)^2)/2 + c2
    
    c < x < L:
    V = c3
    '''
        
    def vx(self,x):
        
        # redefine variables from self. to local to
        # make formulas easier to read
        w1 = self.w1
        a = self.a
        s = self.s
        c = self.c
        b = self.b
        L = self.L
                
        if 0 <= x <= a:
            v = c[0][0]
        elif a < x <= b:
            v = (-1*w1*x) - ((s*math.pow((x-a),2))/2.0) + c[1][0]       
        elif b < x <= L:
            v = c[2][0]
        else:
            v = 0
        
        return v
            
    '''
    Moment Formulas:
    V = dM/dx, therefore M = integral V dx
    
    0 < x < a:
    M = c1*x + c4
    
    a < x < b:
    M = (-1*w1*x^2)/2 - (s(x-a)^3)/6 + c2*x + c5
    
    b < x < L:
    M = c3*x + c6
    '''
    def mx(self,x):
        # redefine variables from self. to local to
        # make formulas easier to read
        w1 = self.w1
        a = self.a
        s = self.s
        c = self.c
        b = self.b
        L = self.L
        
        if 0 <= x <= a:
            m = c[0][0]*x + c[3][0]
        elif a < x <= b:
            m = (((-1*w1*math.pow(x,2))/2.0) - 
                ((s*math.pow((x-a),3))/6.0) + 
                c[1][0]*x + 
                c[4][0])    
        elif b < x <= L:
            m = c[2][0]*x + c[5][0]
        else:
            m = 0   
        return m
        
    '''
    Timoshenko Relationship for Rotation, theta, and Deflection, delta
    M = -E*I d theta/dx
    V = kAG (-theta + d delta/dx)
    
    Rotation Formulas:
    theta = integral M/-EI dx
    
    0 < x < a:
    theta = (-c1*x^2)/(2*EI) - c4*x/EI + c7
    
    a < x < b:
    theta = (w1*x^3)/(6*EI) + (s(x-a)^4)/(24*EI) - (c2*x^2)/2*EI - c5*x/EI + c8
    
    b < x < L:
    theta = (-c3*x^2)/(2*EI) - c6*x/EI + c9
    '''
    
    def thetax(self,x):
        
        # redefine variables from self. to local to
        # make formulas easier to read
        w1 = self.w1
        a = self.a
        s = self.s
        c = self.c
        b = self.b
        L = self.L
        E = self.E
        I = self.I
        
        if 0 <= x <= a:
            theta = (((-1*c[0][0]*math.pow(x,2))/(2.0*E*I)) - 
                    ((c[3][0]*x)/(E*I)) + 
                    c[6][0])
        elif a < x <= b:
            theta = (((w1*math.pow(x,3))/(6.0*E*I)) + 
                    ((s*math.pow((x-a),4))/(24.0*E*I)) - 
                    ((c[1][0]*math.pow(x,2))/(2.0*E*I)) - 
                    ((c[4][0]*x)/(E*I)) + 
                    c[7][0])    
        elif b < x <= L:
            theta = (((-1*c[2][0]*math.pow(x,2))/(2.0*E*I)) - 
                    ((c[5][0]*x)/(E*I)) + 
                    c[8][0])
        else:
            theta = 0     
        
        return theta
        
    '''
    Delta Formulas:
    delta = integral V/kAG + theta dx
    
    0 < x < a:
    delta = c1*x/kAG + (-c1*x^3)/(6*EI) - c4*x^2/2*EI + c7*x + c10
    
    a < x < b:
    delta = -1*w1*x^2/2*kAG - (s(x-a)^3)/6*kAG + c2*x/kAG + (w1*x^4)/(24*EI) + (s(x-a)^5)/(120*EI) - (c2*x^3)/6*EI - c5*x^2/2*EI + c8*x + c11
    
    b < x < L:
    delta = c3*x/kAG + (-c3*x^3)/(6*EI) - c6*x^2/2*EI + c9*x + c12
    '''
    def deltax(self,x):
        # redefine variables from self. to local to
        # make formulas easier to read
        w1 = self.w1
        a = self.a
        s = self.s
        c = self.c
        b = self.b
        L = self.L
        E = self.E
        I = self.I
        G = self.G
        kA = self.kA
        
        if 0 <= x <= a:
            delta = (((c[0][0]*x)/(kA*G)) + 
                    ((-1*c[0][0]*math.pow(x,3))/(6.0*E*I)) - 
                    ((c[3][0]*math.pow(x,2))/(2.0*E*I)) + 
                    (c[6][0]*x) + 
                    c[9][0])
        elif a < x <= b:
            delta = (((-1*w1*math.pow(x,2))/(2.0*kA*G)) - 
                    ((s*math.pow((x-a),3))/(6.0*kA*G)) + 
                    ((c[1][0]*x)/(kA*G)) + 
                    ((w1*math.pow(x,4))/(24.0*E*I)) + 
                    ((s*math.pow((x-a),5))/(120.0*E*I)) - 
                    ((c[1][0]*math.pow(x,3))/(6.0*E*I)) - 
                    ((c[4][0]*math.pow(x,2))/(2.0*E*I)) + 
                    (c[7][0]*x) + 
                    c[10][0])    
        elif b < x <= L:
            delta = (((c[2][0]*x)/(kA*G)) + 
                    ((-1*c[2][0]*math.pow(x,3))/(6.0*E*I)) - 
                    ((c[5][0]*math.pow(x,2))/(2*E*I)) + 
                    (c[8][0]*x) + 
                    c[11][0])
        else:
            delta = 0     
        
        return delta   

    def fef(self):
        L = self.L
        E = self.E
        I = self.I
        G = self.G
        kA = self.kA

        fem = timoforms.fixedendmomentsTimoshenko(self.thetax(0), self.thetax(L), L, E, I, G, kA, [1,1])
        
        ML = fem[0][0]
        MR = fem[1][0]
        
        mo = timoforms.PointMoment(ML,0,L,E,I,G,kA)
        ml = timoforms.PointMoment(MR,L,L,E,I,G,kA)
        
        RL = self.RL + mo.rl + ml.rl
        RR = self.RR + mo.rr + ml.rr
        
        return [RL,ML,RR,MR]




w1= 1
w2= 0.5
a= 3
b= 7
L=10

#Material and Cross section data
E = 29000*math.pow(12,2)
I = 30.8 * 1/math.pow(12,4)
kA = 1.34 * 1/math.pow(12,2)
#kA = 10000000000000000000.0
G = E /(2+(2*0.3))

load = VariableLoad(w1, w2, a, b, L, E, I, G, kA)

fef = load.fef()

res0 = [load.vx(0),load.mx(0),load.thetax(0),load.deltax(0)*12.0]
res2 = [load.vx(2),load.mx(2),load.thetax(2),load.deltax(2)*12.0]
res5 = [load.vx(5),load.mx(5),load.thetax(5),load.deltax(5)*12.0]
res8 = [load.vx(8),load.mx(8),load.thetax(8),load.deltax(8)*12.0]
resL = [load.vx(L),load.mx(L),load.thetax(L),load.deltax(L)*12.0]