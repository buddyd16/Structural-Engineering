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
        
        arrows simply places to diagonal lines at the laad intersection with
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
        
        arrows simply places to diagonal lines at the laad intersection with
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