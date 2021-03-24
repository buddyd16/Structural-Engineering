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
from numpy import sign
from numpy import zeros
import numpy as np
import math

def fixedendmomentsTimoshenko(theta_0,theta_L, L, E, I, G, kA, fed=[1,1]):
    '''
    Given the the start and end cross section rotations
    Return the end moments that produce equal and opposite rotations
    such that the net rotation at the member ends are 0 ie Fixed
    
    Sign convention is clockwise moments are positive
    
    [-Theta_0, -Theta_L] = [M_0,M_1] * [(1/kA G L)+(L/3EI), (1/kA G L)-(L/6EI)
                                        (1/kA G L)-(L/6EI), (1/kA G L)+(L/3EI)]
    
    Using Numpy Linear Algebra to solve the simultaneous equations
    '''
    
    if fed[0] == 1 and fed[1] == 1:
        s = np.array([[-1.0*theta_0],[-1.0*theta_L]])

        ems = np.array([[(1.0/(kA*G*L))+(L/(3.0*E*I)) , (1.0/(kA*G*L))-(L/(6.0*E*I))],
                        [(1.0/(kA*G*L))-(L/(6.0*E*I)) , (1.0/(kA*G*L))+(L/(3.0*E*I))]])

        fem = np.linalg.solve(ems,s)

    elif fed[0] == 1 and fed[1] == 0:
        fel= (-1.0*theta_0) / ((1.0/(kA*G*L))+(L/(3.0*E*I)))
        fem = np.array([[fel],[0]])

    elif fed[0] == 0 and fed[1] == 1:
        fer = (-1.0*theta_L) / ((1.0/(kA*G*L))+(L/(3.0*E*I)))
        fem = np.array([[0],[fer]])

    else:
        fem = np.array([[0],[0]])

    return fem

class TimoshenkoBeam:
    def __init__(L, E, I, G, kA):
        '''
        Timoshenko General form equations for beam stiffness
        and carry over factors

        
        ** Maintain consistent units among the inputs **

        L = beam span
        E = beam modulus of elastacity
        I = beam second moment of area about the axis of bending
        G = beam shear modulus
        kA = beam shear area, typically the beam web area for steel W shapes
        
        '''

        self.L = L
        self.E = E
        self.I = I
        self.G = G
        self.kA = kA
        
    def cof(self, fixed=[1,1]):
        '''
        carry over factor 
        g = 6EI / kAGL^2
        
        '''
        
        g = ((6*self.E*self.I) / (self.kA*self.G*self.L*self.L))
        
        COF_fixed = (1-g) / (2+g)
        
        COF = [i*COF_fixed for i in fixed]
        
        return COF
    
    def k(self, fixed=[1,1]):
        '''
        Stiffness factors
        g = 6EI / kAGL^2
        '''
        g = ((6*self.E*self.I) / (self.kA*self.G*self.L*self.L))
        
        K_farfixed = ((4*self.E*self.I) / self.L) * ((2+g)/(2*(1+(2*g))))
        
        K_farpinned = ((3*self.E*self.I)/self.L) * (2/(2+g))
        
        if fixed == [0,1]:
            return [0,K_farpinned]
        
        elif fixed == [1,0]:
            return [K_farpinned,0]
        
        elif fixed == [0,0]:
            return [0,0]
        
        else:
            return [K_farfixed,K_farfixed]
    
class PointLoad:
    def __init__(self, P, a, L, E, I, G, kA):
        '''
        Timoshenko General form equations for a simply
        supported beam with an applied Point load anywhere
        along the beam span.
        
        Note unlike the Euler-Bernoulli beam formulas
        the beam properties are needed as part of the
        initial inputs.
        
        ** Maintain consistent units among the inputs **
        
        P = load
        a = load location from left end of beam
        L = beam span
        E = beam modulus of elastacity
        I = beam second moment of area about the axis of bending
        G = beam shear modulus
        kA = beam shear area, typically the beam web area for steel W shapes
        
        sign convention:
         (+) positive loads are applied in the (-) negative y direction
         (+) positive reactions are in the (+) positive y direction
        
        '''
        
        self.P = P
        self.a = a
        self.L = L
        self.E = E
        self.I = I
        self.G = G
        self.kA = kA
        
        # b = L-a
        self.b = self.L - self.a
        
        self.kind = 'Point'
        
        self.error = ''

        if self.a > self.L:
            self.error = 'Error a > l'
        
        # Simple End Reactions from statics
        # Sum V = 0 and Sum M = 0
        
        self.rl = (self.P*self.b)/self.L
        self.rr = (self.P*self.a)/self.L
        
        '''
        Integration constants
        resulting from integration of the two formulas
        M = -EI dtheta/dx
        V = kAG (-theta + ddelta/dx)
        
        Initial conditions:
        delta = 0 at x=0 and x = L
        
        Compatibility conditions:
        theta = constant at x = a
        delta = constant at x = a
        '''
        
        self.c1 = ((-1*self.P*math.pow(self.a,2)) / (2*self.E*self.I) +
                    ((self.P*math.pow(self.a,3)) / (6*self.E*self.I*self.L)) +
                    ((self.P*self.a*self.L) / (3*self.E*self.I)))
        
        self.c2 = 0
        
        self.c3 = (((self.P*math.pow(self.a,3))/(6*self.E*self.I*self.L)) +
                    ((self.P*self.a*self.L)/(3*self.E*self.I)))
        
        self.c4 = (((self.P*self.a)/(self.kA*self.G)) - 
                    ((self.P*math.pow(self.a,3))/(6*self.E*self.I)))
        

    def chart_load(self, x_scale=0, y_scale=0, arrows=0):
        '''
        function returns x and y coordinate data to facilitate
        chart plotting
        
        y scaling is applied to the load value
        x scaling only impacts the arrow head if arrows are
        selected to be included
        
        arrows simply places two diagonal lines at the load intersection with
        the beam line.
        
        '''
        
        if arrows == 1:
            arrow_height = (self.P/6.0)
            #30 degree arrow
            arrow_plus= (self.a+(arrow_height*math.tan(math.radians(30))))
            arrow_minus= (self.a-(arrow_height*math.tan(math.radians(30))))

            x=[arrow_minus,self.a,arrow_plus,self.a,self.a]
            x = [i*x_scale for i in x]
            y=[arrow_height,0,arrow_height,0,self.P]
            y = [j*y_scale for j in y]
        else:
            x = [self.a*x_scale, self.a*x_scale]
            y = [0,self.P*y_scale]

        return x,y

    def fef(self):
        '''
        fixed end forces
        g = 6EI / kAGL^2
        
        Sign convention:
        (+) positive moments are clock-wise
        
        '''
        
        # redefine variables from self. to local to
        # make formulas easier to read
        P = self.P
        a = self.a
        b = self.b
        L = self.L
        
        g = ((6*self.E*self.I) / (self.kA*self.G*self.L*self.L))
        
        ML = -1.0 * ((P*a*b*b) / (L*L))*((1+((L/b)*g))/(1+(2*g)))
        MR = ((P*a*a*b) / (L*L))*((1+((L/a)*g))/(1+(2*g)))
        
        # additional vertical reactions caused by fixed end moments
        
        MRL = -1.0*(ML+MR)/L
        MRR = -1.0*MRL
        
        RL = self.rl + MRL
        RR = self.rr + MRR
        
        return [RL, ML, RR, MR]
        
    def v(self,x):
        '''
        function takes an array of x locations along the beam and
        returns the associated internal beam shear
        '''
        
        iters = len(x)
        v=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                if x[i] == 0 and self.a == 0:
                    v[i] = 0
                else:
                    v[i] = self.rl
            else:
                v[i] = -1 * self.rr
        return v

    def m(self,x):
        '''
        function takes an array of x locations along the beam and
        returns the associated internal beam moment
        '''
        
        iters = len(x)
        m=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                m[i] = self.rl * x[i]
            else:
                m[i] = (-1 * self.rr * x[i]) + (self.rr * self.L)
        return m
        
    def theta(self,x):
        '''
        function takes an array of x locations along the beam and
        returns the associated internal rotation of the cross-section vertical
        axis
        '''
        
        iters = len(x)
        theta = zeros(iters)
        
        for i in range(0,iters):
            if x[i] <= self.a:
                theta[i] = (((-1*self.rl*math.pow(x[i],2))/(2*self.E*self.I)) + 
                            self.c1)
            else:
                theta[i] = (((self.P*self.a*math.pow(x[i],2)) / (2*self.E*self.I*self.L)) -
                            ((self.P*self.a*x[i]) / (self.E*self.I)) +
                            self.c3)
        return theta
    
    def delta(self,x):
        '''
        function takes an array of x locations along the beam and
        returns the associated beam vertical deflection
        '''
        
        iters = len(x)
        delta = zeros(iters)
        
        for i in range(0,iters):
            if x[i] <= self.a:
                delta[i] = (((self.rl*x[i])/(self.kA*self.G)) - 
                            ((self.rl*math.pow(x[i],3))/(6*self.E*self.I)) + 
                            (self.c1*x[i]) + self.c2)
                
            else:
                delta[i] = (((-1.0*self.rr*x[i])/(self.kA*self.G)) + 
                            ((self.P*self.a*math.pow(x[i],3))/(6*self.E*self.I*self.L)) - 
                            ((self.P*self.a*math.pow(x[i],2))/(2*self.E*self.I)) + 
                            (self.c3*x[i]) + self.c4)
                
        return delta
    
    '''
    The below functions do the same as above with the exception that they only
    accept a single x location and report a single result.
    '''
    
    def vx(self,x):
        if x <= self.a:
            if x == 0 and self.a == 0:
                vx = 0
            else:
                vx = self.rl
        else:
            vx = -1 * self.rr
        return vx

    def mx(self,x):
        if x <= self.a:
            mx = self.rl * x
        else:
            mx = (-1 * self.rr * x) + (self.rr * self.L)
        return mx
        
    def thetax(self,x):
        if x <= self.a:
            thetax = (((-1*self.rl*math.pow(x,2))/(2*self.E*self.I)) + 
                        self.c1)
        else:
            thetax = (((self.rr*math.pow(x,2)) / (2*self.E*self.I)) -
                        ((self.rr*self.L*x) / (self.E*self.I)) +
                        self.c3)
        return thetax
    
    def deltax(self,x):
        if x <= self.a:
            deltax = (((self.rl*x)/(self.kA*self.G)) - 
                        ((self.rl*math.pow(x,3))/(6*self.E*self.I)) + 
                        (self.c1*x) + self.c2)
            
        else:
            deltax = (((-1.0*self.rr*x)/(self.kA*self.G)) + 
                        ((self.P*self.a*math.pow(x,3))/(6*self.E*self.I*self.L)) - 
                        ((self.P*self.a*math.pow(x,2))/(2*self.E*self.I)) + 
                        (self.c3*x) + self.c4)
                
        return deltax

class PointMoment:
    def __init__(self, M, a, L, E, I, G, kA):
        '''
        Timoshenko General form equations for a simply
        supported beam with an applied Point Moment anywhere
        along the beam span.
        
        Note unlike the Euler-Bernoulli beam formulas
        the beam properties are needed as part of the
        initial inputs.
        
        ** Maintain consistent units among the inputs **
        
        M = moment
        a = load location from left end of beam
        L = beam span
        E = beam modulus of elastacity
        I = beam second moment of area about the axis of bending
        G = beam shear modulus
        kA = beam shear area, typically the beam web area for steel W shapes
        
        sign convention:
         (+) positive moments are applied clockwise
         (+) positive reactions are in the (+) positive y direction
        
        '''
        
        self.M = M
        self.a = a
        self.L = L
        self.E = E
        self.I = I
        self.G = G
        self.kA = kA
        
        # b = L-a
        self.b = self.L - self.a
        
        self.kind = 'Moment'
        
        self.error = ''

        if self.a > self.L:
            self.error = 'Error a > l'
        
        # Simple End Reactions from statics
        # Sum V = 0 and Sum M = 0
        
        self.rl = -1.0*self.M/self.L
        self.rr = self.M/self.L
        
        '''
        Integration constants
        resulting from integration of the two formulas
        M = -EI dtheta/dx
        V = kAG (-theta + ddelta/dx)
        
        Initial conditions:
        delta = 0 at x=0 and x = L
        
        Compatibility conditions:
        theta = constant at x = a
        delta = constant at x = a
        '''
        
        self.c1 = (((-1.0*self.M*self.a) / (self.E*self.I)) +
                    ((self.M*math.pow(self.a,2))/(2*self.E*self.I*self.L)) +
                    (self.M/(self.kA*self.G*self.L)) +
                    ((self.M*self.L)/(3*self.E*self.I)))
        
        self.c2 = 0
        
        self.c3 = (((self.M*math.pow(self.a,2))/(2*self.E*self.I*self.L)) +
                    (self.M/(self.kA*self.G*self.L)) +
                    ((self.M*self.L)/(3*self.E*self.I)))
        
        self.c4 = (-1.0*self.M*math.pow(self.a,2))/(2*self.E*self.I)
        

    def chart_load(self, x_scale=0, y_scale=0, arrows=0):
        '''
        function returns x and y coordinate data to facilitate
        chart plotting
        
        y scaling is applied to the load value
        x scaling only impacts the arrow head if arrows are
        selected to be included
        
        arrows simply places two diagonal lines at the load intersection with
        the beam line.
        
        '''
        
        x=[]
        y=[]
        r = (self.M/2.0) 
        # set radius as M/2 so when centered on beam line the moment symbol
        # total height mathces the moment value

        if arrows == 1:
            arrow_height = r/6.0
            #30 degree arrow
            arrow_minus= (arrow_height*math.tan(math.radians(30)))

            if self.ma <0:
                x = [self.a,self.a,self.a]
                y = [r,0,-r]
                xi=0
                yi=0
                for a in range(-90, 181):
                    xi = (self.a)+((r*math.cos(math.radians(a))))
                    yi = 0+((r*math.sin(math.radians(a))))
                    x.append(xi)
                    y.append(yi)

                x.append(xi-arrow_minus)
                y.append(yi+arrow_height)
                x.append(xi)
                y.append(yi)
                x.append(xi+arrow_minus)
                y.append(yi+arrow_height)
            else:
                x = [self.a-r,self.a,self.a+r, self.a+r-arrow_minus,self.a+r,self.a+r+arrow_minus,self.a+r]
                y = [0,0,0,arrow_height,0,arrow_height,0]

                xi=0
                yi=0
                for a in range(0,271):
                    xi = self.a+(r*math.cos(math.radians(a)))
                    yi = 0+(r*math.sin(math.radians(a)))
                    x.append(xi)
                    y.append(yi)
        else:
            if self.ma <0:
                x = [self.a,self.a,self.a]
                y = [r,0,-r]
                xi=0
                yi=0
                for a in range(-90, 181):
                    xi = self.a+(r*math.cos(math.radians(a)))
                    yi = 0+(r*math.sin(math.radians(a)))
                    x.append(xi)
                    y.append(yi)
            else:
                x = [self.a-r,self.a,self.a+r]
                y = [0,r,0]
                xi=0
                yi=0
                for a in range(0,271):
                    xi = self.a+(r*math.cos(math.radians(a)))
                    yi = 0+(r*math.sin(math.radians(a)))
                    x.append(xi)
                    y.append(yi)

        x = [i*x_scale for i in x]
        y = [j*y_scale for j in y]
        
        return x,y

    def fef(self):
        '''
        fixed end forces
        g = 6EI / kAGL^2
        
        Sign convention:
        (+) positive moments are clock-wise
        
        '''
        
        # redefine variables from self. to local to
        # make formulas easier to read
        M = self.M
        a = self.a
        b = self.b
        L = self.L
        
        g = ((6*self.E*self.I) / (self.kA*self.G*self.L*self.L))
        
        ML = 0
        MR = 0
        
        # additional vertical reactions caused by fixed end moments
        
        MRL = -1.0*(ML+MR)/L
        MRR = -1.0*MRL
        
        RL = self.rl + MRL
        RR = self.rr + MRR
        
        return [RL, ML, RR, MR]
        
    def v(self,x):
        '''
        function takes an array of x locations along the beam and
        returns the associated internal beam shear
        '''
        
        iters = len(x)
        v=zeros(iters)

        for i in range(0,iters):
            v[i] = self.rl
            
        return v

    def m(self,x):
        '''
        function takes an array of x locations along the beam and
        returns the associated internal beam moment
        '''
        
        iters = len(x)
        m=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                m[i] = self.rl * x[i]
            else:
                m[i] = self.rl * x[i] + self.M
        return m
        
    def theta(self,x):
        '''
        function takes an array of x locations along the beam and
        returns the associated internal rotation of the cross-section vertical
        axis
        '''
        
        iters = len(x)
        theta = zeros(iters)
        
        for i in range(0,iters):
            if x[i] <= self.a:
                theta[i] = ((self.M*math.pow(x[i],2))/(2*self.E*self.I*self.L)) + self.c1
            else:
                theta[i] = (((self.M*math.pow(x[i],2))/(2*self.E*self.I*self.L)) - 
                            ((self.M*x[i])/(self.E*self.I)) +
                            self.c3)
                
        return theta
    
    def delta(self,x):
        '''
        function takes an array of x locations along the beam and
        returns the associated beam vertical deflection
        '''
        
        iters = len(x)
        delta = zeros(iters)
        
        for i in range(0,iters):
            if x[i] <= self.a:
                delta[i] = (((-1.0*self.M*x[i])/(self.kA*self.G*self.L))+
                            ((self.M*math.pow(x[i],3))/(6*self.E*self.I*self.L))+
                            (self.c1*x[i])+
                            self.c2)
                
            else:
                delta[i] = (((-1.0*self.M*x[i])/(self.kA*self.G*self.L))+
                            ((self.M*math.pow(x[i],3))/(6*self.E*self.I*self.L))-
                            ((self.M*math.pow(x[i],2))/(2*self.E*self.I))+
                            (self.c3*x[i])+
                            self.c4)
                
        return delta
    
    '''
    The below functions do the same as above with the exception that they only
    accept a single x location and report a single result.
    '''
    
    def vx(self,x):
        vx = self.rl
        
        return vx

    def mx(self,x):
        if x <= self.a:
            mx = self.rl * x
        else:
            mx = self.rl * x + self.M
        return mx
        
    def thetax(self,x):
        if x <= self.a:
            thetax = ((self.M*math.pow(x,2))/(2*self.E*self.I*self.L)) + self.c1
        else:
            thetax = (((self.M*math.pow(x,2))/(2*self.E*self.I*self.L)) - 
                            ((self.M*x)/(self.E*self.I)) +
                            self.c3)
        return thetax
    
    def deltax(self,x):
        if x <= self.a:
            deltax = (((-1.0*self.M*x)/(self.kA*self.G*self.L))+
                        ((self.M*math.pow(x,3))/(6*self.E*self.I*self.L))+
                        (self.c1*x)+
                        self.c2)
            
        else:
            deltax = (((-1.0*self.M*x)/(self.kA*self.G*self.L))+
                        ((self.M*math.pow(x,3))/(6*self.E*self.I*self.L))-
                        ((self.M*math.pow(x,2))/(2*self.E*self.I))+
                        (self.c3*x)+
                        self.c4)
                
        return deltax

class UniformLoad:
    def __init__(self, w, a, b, L, E, I, G, kA):
        '''
        Timoshenko derivation for uniform loading
        pin-pin single span beam
        
        w - Load left end value
        a - load start point from left end of beam
        b - load end point from left end of beam
        d - load width = b - a
        L - beam span
        E = beam modulus of elastacity
        I = beam second moment of area about the axis of bending
        G = beam shear modulus
        kA = beam shear area, typically the beam web area for steel W shapes
    
        sign convention:
         (+) positive moments are applied clockwise
         (+) positive reactions are in the (+) positive y direction
        '''
        self.w = w
        self.a = a
        self.b = b
        self.L = L
        self.E = E
        self.I = I
        self.G = G
        self.kA = kA
        
        d= b - a
        self.d = d
        
        '''
        Reactions:
        W = w*d
        sum Fy = 0 
        --> RL + RR - W = 0
        xbar = (a + d/2)
        sum Mx,rl,cw+ = 0 
        --> -RR*L + W*(xbar) = 0 
        --> RR = W*(xbar) / L
        
        RL = W - RR
        '''
    
        W = w*d
        self.W = W
        xbar = a + (d/2.0)
        self.xbar = xbar
    
        RR = (W*xbar) / L
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
        c1 = -1*w*a + c2
        
        //-c1 + c2 = w*a
        
        **Boundary @ x=0, M=0:**
        //c4 = 0
        
        **Boundary @ x=L, M=0:**
        //c3*L + c6 = 0
        c6 = -c3*L
        
        **Compatibility @ x=a, M=constant:**
        c1*a = (-1*w*a^2)/2 + c2*a + c5
        
        //c1*a - c2*a - c5 = (-1*w*a^2)/2
        
        **Boundary @ x=0, delta=0:**
        //c10 = 0
        
        **Boundary @ x=L, delta=0:**
        //0 = c3*L/kAG + (-c3*L^3)/(6*EI) - c6*L^2/2*EI + c9*L + c12
        
        **Compatibility @ x=a, delta=constant:**
        c1*a/kAG + (-c1*a^3)/(6*EI) - c4*a^2/2*EI + c7*a = 
        -1*w*a^2/2*kAG + c2*a/kAG + (w*a^4)/(24*EI) - (c2*a^3)/6*EI - c5*a^2/2*EI + c8*a + c11
        
        //c1*a/kAG + (-c1*a^3)/(6*EI) - c2*a/kAG + (c2*a^3)/6*EI - c4*a^2/2*EI + c5*a^2/2*EI + c7*a - c8*a - c11 = 
        -1*w*a^2/2*kAG + (w*a^4)/(24*EI)
        
        **Compatibility @ x=b, delta = constant:**
        c3*b/kAG + (-c3*b^3)/(6*EI) - c6*b^2/2*EI + c9*b + c12 = 
        -1*w*b^2/2*kAG + c2*b/kAG + (w*b^4)/(24*EI) - (c2*b^3)/6*EI - c5*b^2/2*EI + c8*b + c11
        
        //-c2*b/kAG + (c2*b^3)/6*EI + c3*b/kAG + (-c3*b^3)/(6*EI) + c5*b^2/2*EI - c6*b^2/2*EI - c8*b + c9*b - c11 + c12 = 
        -1*w1*b^2/2*kAG + (w1*b^4)/(24*EI)
        
        **Compatibility @ x=a, theta=constant:**
        (-c1*a^2)/(2*EI) - c4*a/EI + c7 = (w*a^3)/(6*EI) - (c2*a^2)/2*EI - c5*a/EI + c8
        
        //(-c1*a^2)/(2*EI) + (c2*a^2)/2*EI - c4*a/EI + c5*a/EI + c7 - c8 = (w*a^3)/(6*EI)
        
        **Compatibility @ x=b, theta = constant:**
        (w*b^3)/(6*EI) - (c2*b^2)/2*EI - c5*b/EI + c8 = (-c3*b^2)/(2*EI) - c6*b/EI + c9
        
        //(-c2*b^2)/2*EI + (c3*b^2)/(2*EI) - c5*b/EI + c6*b/EI + c8 - c9 = (-1*w*b^3)/(6*EI)
        
        '''
        bc1_coeff = [1,0,0,0,0,0,0,0,0,0,0,0] 
        bc1_eq = [RL]
        
        bc2_coeff = [-1,1,0,0,0,0,0,0,0,0,0,0] 
        bc2_eq = [w*a]
        
        bc3_coeff = [0,0,1,0,0,0,0,0,0,0,0,0]
        bc3_eq = [-1*RR]
        
        bc4_coeff = [0,0,0,1,0,0,0,0,0,0,0,0] 
        bc4_eq = [0]
        
        bc5_coeff = [-1*a,a,0,0,1,0,0,0,0,0,0,0]
        bc5_eq = [(w*math.pow(a,2))/2.0]
        
        bc6_coeff = [0,0,L,0,0,1,0,0,0,0,0,0]
        bc6_eq = [0]
        
        bc7_coeff = [(-1*math.pow(a,2))/(2*E*I),(math.pow(a,2))/(2*E*I),0,0,a/(E*I),0,1,-1,0,0,0,0] 
        bc7_eq = [(w*math.pow(a,3))/(6*E*I)]
        
        bc8_coeff = [0,
                     (math.pow(b,2))/(2*E*I),
                     (-1*math.pow(b,2))/(2*E*I),
                     0,
                     b/(E*I),
                     (-1*b)/(E*I),
                     0,
                     -1,
                     1,
                     0,
                     0,
                     0]
                     
        bc8_eq = [((w*math.pow(b,3))/(6*E*I))]
         
        bc9_coeff = [0,0,(L/(kA*G)) + ((-1*math.pow(L,3))/(6*E*I)),0,0,-1*math.pow(L,2)/(2*E*I),0,0,L,0,0,1]
        bc9_eq = [0]
        
        bc10_coeff = [0,0,0,0,0,0,0,0,0,1,0,0] 
        bc10_eq = [0]
        
        bc11_coeff = [(a/(kA*G)) + ((-1*math.pow(a,3))/(6*E*I)),
                      (-1*a/(kA*G)) + ((math.pow(a,3))/(6*E*I)),
                        0,
                        0,
                        (math.pow(a,2)/(2*E*I)),
                        0,
                        a,
                        -1*a,
                        0,
                        0,
                        -1,
                        0]
                        
        bc11_eq = [(-1*w*math.pow(a,2)/(2*kA*G)) + ((w*math.pow(a,4))/(24*E*I))]
        
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
                        
        bc12_eq = [((-1*w*math.pow(b,2))/(2*kA*G)) + ((w*math.pow(b,4))/(24*E*I))]
        
        
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
    w = -1*w
    
    b < x < L:
    w = 0
    
    Shear Formulas:
    w = dV/dx, therefore V = integral w dx
    
    0 < x < a:
    V = c1
    
    a < x < b:
    V = -1*w*x + c2
    
    c < x < L:
    V = c3
    '''
    def vx(self,x):
        
        # redefine variables from self. to local to
        # make formulas easier to read
        w = self.w
        a = self.a
        c = self.c
        b = self.b
        L = self.L
                
        if 0 <= x <= a:
            v = c[0][0]
        elif a < x <= b:
            v = (-1*w*x) + c[1][0]       
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
    M = (-1*w*x^2)/2 + c2*x + c5
    
    b < x < L:
    M = c3*x + c6
    '''
    def mx(self,x):
        # redefine variables from self. to local to
        # make formulas easier to read
        w = self.w
        a = self.a
        c = self.c
        b = self.b
        L = self.L
        
        if 0 <= x <= a:
            m = c[0][0]*x + c[3][0]
        elif a < x <= b:
            m = (((-1*w*math.pow(x,2))/2.0) + 
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
    theta = (w1*x^3)/(6*EI) - (c2*x^2)/2*EI - c5*x/EI + c8
    
    b < x < L:
    theta = (-c3*x^2)/(2*EI) - c6*x/EI + c9
    '''
    
    def thetax(self,x):
        
        # redefine variables from self. to local to
        # make formulas easier to read
        w = self.w
        a = self.a
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
            theta = (((w*math.pow(x,3))/(6.0*E*I)) - 
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
    delta = -1*w1*x^2/2*kAG + c2*x/kAG + (w1*x^4)/(24*EI) - (c2*x^3)/6*EI - c5*x^2/2*EI + c8*x + c11
    
    b < x < L:
    delta = c3*x/kAG + (-c3*x^3)/(6*EI) - c6*x^2/2*EI + c9*x + c12
    '''
    def deltax(self,x):
        # redefine variables from self. to local to
        # make formulas easier to read
        w = self.w
        a = self.a
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
            delta = (((-1*w*math.pow(x,2))/(2.0*kA*G)) + 
                    ((c[1][0]*x)/(kA*G)) + 
                    ((w*math.pow(x,4))/(24.0*E*I)) - 
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

        fem = fixedendmomentsTimoshenko(self.thetax(0), self.thetax(L), L, E, I, G, kA, [1,1])
        
        ML = fem[0][0]
        MR = fem[1][0]
        
        mo = timoforms.PointMoment(ML,0,L,E,I,G,kA)
        ml = timoforms.PointMoment(MR,L,L,E,I,G,kA)
        
        RL = self.RL + mo.rl + ml.rl
        RR = self.RR + mo.rr + ml.rr
        
        return [RL,ML,RR,MR]
        
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
            delta = (((c[0][0]*x)/(kA*G))
                    + (-1*c[0][0]*math.pow(x,3))/(6.0*E*I))
                    - ((c[3][0]*math.pow(x,2))/(2.0*E*I))
                    + (c[6][0]*x)
                    + c[9][0])
        elif a < x <= b:
            delta = (((-1*w1*math.pow(x,2))/(2.0*kA*G))
                    - ((s*math.pow((x-a),3))/(6.0*kA*G))
                    + ((c[1][0]*x)/(kA*G))
                    + ((w1*math.pow(x,4))/(24.0*E*I))
                    + ((s*math.pow((x-a),5))/(120.0*E*I))
                    - ((c[1][0]*math.pow(x,3))/(6.0*E*I))
                    - ((c[4][0]*math.pow(x,2))/(2.0*E*I))
                    + (c[7][0]*x)
                    + c[10][0])
        elif b < x <= L:
            delta = (((c[2][0]*x)/(kA*G))
                    + ((-1*c[2][0]*math.pow(x,3))/(6.0*E*I))
                    - ((c[5][0]*math.pow(x,2))/(2*E*I))
                    + (c[8][0]*x)
                    + c[11][0])
        else:
            delta = 0
        
        return delta

    def fef(self):
        L = self.L
        E = self.E
        I = self.I
        G = self.G
        kA = self.kA

        fem = fixedendmomentsTimoshenko(self.thetax(0), self.thetax(L), L, E, I, G, kA, [1,1])
        
        ML = fem[0][0]
        MR = fem[1][0]
        
        mo = timoforms.PointMoment(ML,0,L,E,I,G,kA)
        ml = timoforms.PointMoment(MR,L,L,E,I,G,kA)
        
        RL = self.RL + mo.rl + ml.rl
        RR = self.RR + mo.rr + ml.rr
        
        return [RL,ML,RR,MR]