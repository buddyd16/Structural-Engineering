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
from numpy import sign
from numpy import zeros
import numpy as np
import math

class no_load:
    def __init__(self):
        self.p = 0
        self.rl = 0
        self.rr = 0
        
        self.kind = 'NL'
        
    def v(self,x):
        iters = len(x)
        v=zeros(iters)
        return v

    def m(self,x):
        iters = len(x)
        m=zeros(iters)
        return m

    def eis(self,x):
        iters = len(x)
        eis=zeros(iters)
        return eis

    def eid(self,x):
        iters = len(x)
        eid=zeros(iters)
        return eid

    def vx(self,x):
        v = 0
        return v

    def mx(self,x):
        m = 0
        return m

    def eisx(self,x):
        eisx = 0
        return eisx

    def eidx(self,x):
        eid = 0
        return eid

class pl:
    def __init__(self, p, a, L):

        self.p = float(p)
        self.a = float(a)
        self.L = float(L)
        self.b = self.L - self.a
        
        self.kind = 'Point'
        
        self.error = ''
        
        if self.a > self.L:
            self.error = 'Error a > l'
            self.error = 'Error a > l'

        self.rl = (self.p*self.b)/self.L
        self.rr = (self.p*self.a)/self.L
        self.c4 = ((-1*self.rl * self.a ** 3) / 3) - ((self.rr * self.a ** 3) / 3) + ((self.rr * self.L * self.a ** 2) / 2)
        self.c2 = (-1 / self.L) * ((self.c4) + ((self.rr * self.L ** 3) / 3))
        self.c1 = ((-1*self.rr * self.a ** 2) / 2) - ((self.rl * self.a ** 2) / 2) + (self.rr * self.L * self.a) + self.c2

        arrow_height = self.p/6.0
        #30 degree arrow
        arrow_plus= self.a+(arrow_height*math.tan(math.radians(30)))
        arrow_minus= self.a-(arrow_height*math.tan(math.radians(30)))

        self.x_graph=[arrow_minus,self.a,arrow_plus,self.a,self.a]
        self.y_graph=[arrow_height,0,arrow_height,0,self.p]
    
    def fef(self):
        # Fixed End Forces
        RL = ((self.p*self.b*self.b) / (self.L*self.L*self.L))*((3*self.a)+self.b)
        RR = ((self.p*self.a*self.a) / (self.L*self.L*self.L))*(self.a+(3*self.b))
        ML = -1*(self.p*self.a*self.b*self.b) / (self.L*self.L)
        MR = (self.p*self.a*self.a*self.b) / (self.L*self.L)
        
        return [RL,ML,RR,MR]
        
    def v(self,x):
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
        iters = len(x)
        m=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                m[i] = self.rl * x[i]
            else:
                m[i] = (-1 * self.rr * x[i]) + (self.rr * self.L)
        return m

    def eis(self,x):
        iters = len(x)
        eis=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eis[i] = ((self.rl * x[i] ** 2)  / 2) + self.c1
            else:
                eis[i] = ((-1.0 * self.rr * x[i] ** 2)/2.0) + (self.rr * self.L * x[i]) + self.c2
        return eis

    def eid(self,x):
        iters = len(x)
        eid=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eid[i] = ((self.rl * x[i] ** 3) / 6) + (self.c1 * x[i])
            else:
                eid[i] = ((-1*self.rr * x[i] ** 3) / 6) + ((self.rr * self.L * x[i] ** 2) / 2) + (self.c2 * x[i]) + self.c4
        return eid

    def vx(self,x):
        x = float(x)
        if x <= self.a:
            if x==0 and self.a==0:
                v = 0
            else:
                v = self.rl
        else:
            v = -1 * self.rr
        return v

    def mx(self,x):
        x = float(x)
        if x <= self.a:
            m = self.rl * x
        else:
            m = (-1 * self.rr * x) + (self.rr * self.L)
        return m

    def eisx(self,x):
        x = float(x)
        if x <= self.a:
            eisx = ((self.rl * x ** 2)  / 2) + self.c1
        else:
            eisx = ((-1.0 * self.rr * x ** 2)/2.0) + (self.rr * self.L * x) + self.c2
        return eisx

    def eidx(self,x):
        x = float(x)
        if x <= self.a:
            eid = ((self.rl * x ** 3) / 6) + (self.c1 * x)
        else:
            eid = ((-1*self.rr * x ** 3) / 6) + ((self.rr * self.L * x ** 2) / 2) + (self.c2 * x) + self.c4
        return eid

class point_moment:
    def __init__(self, ma, a, L):
        self.ma = float(ma)
        self.a = float(a)
        self.L = float(L)
        
        self.kind = 'Moment'
        
        self.error = ''
        
        if a > self.L:
            self.error = 'Error a > L'
            
        self.rr = self.ma/self.L
        self.rl = -1.0*self.rr

        self.c2 = (-1.0/self.L) * ((self.ma*self.a**2) - (0.5*self.ma*self.a**2) + (self.rl * (self.L**3/6.0)) + (0.5*self.ma*self.L**2))
        self.c1 = ma*a + self.c2
        self.c3 = 0
        self.c4 = ((-1.0*self.rl*self.L**3)/6.0) - (0.5*self.ma*self.L**2) - (self.c2*self.L)

        r = (self.ma/8.0)
        arrow_height = r/6.0
        #30 degree arrow
        arrow_minus= (arrow_height*math.tan(math.radians(30)))

        if self.ma <0:
            self.x_graph = [self.a,self.a,self.a]
            self.y_graph = [r,0,-r]
            x=0
            y=0
            for a in range(-90, 181):
                x = self.a+(r*math.cos(math.radians(a)))
                y = 0+(r*math.sin(math.radians(a)))
                self.x_graph.append(x)
                self.y_graph.append(y)

            self.x_graph.append(x-arrow_minus)
            self.y_graph.append(y+arrow_height)
            self.x_graph.append(x)
            self.y_graph.append(y)
            self.x_graph.append(x+arrow_minus)
            self.y_graph.append(y+arrow_height)
        else:
            self.x_graph = [self.a-r,self.a,self.a+r, self.a+r-arrow_minus,self.a+r,self.a+r+arrow_minus,self.a+r]
            self.y_graph = [0,0,0,arrow_height,0,arrow_height,0]
            x=0
            y=0
            for a in range(0,271):
                x = self.a+(r*math.cos(math.radians(a)))
                y = 0+(r*math.sin(math.radians(a)))
                self.x_graph.append(x)
                self.y_graph.append(y)

    def fef(self):
        # Fixed End Forces
        RL = ((-6.0*self.ma*self.a) / (self.L*self.L*self.L)) * (self.L-self.a)
        RR = -1.0*RL
        ML = ((-1.0*self.ma) / (self.L*self.L))*((self.L*self.L)-(4*self.L*self.a)+(3*self.a*self.a))
        MR = -1.0*(self.ma / (self.L*self.L))*((3*self.a*self.a)-(2*self.a*self.L))
        
        return [RL,ML,RR,MR]
        
    def v(self,x):
        iters = len(x)
        v=zeros(iters)

        for i in range(0,iters):
            v[i] = self.rl

        return v

    def m(self,x):
        iters = len(x)
        m=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                if x[i] == 0 and self.a == 0:
                    m[i] = self.ma
                elif x[i] == self.L and self.a == self.L:
                    m[i] = -1.0*self.ma
                else:
                    m[i] = self.rl * x[i]
            else:
                m[i] = (self.rl * x[i]) + self.ma
        return m

    def eis(self,x):
        iters = len(x)
        eis=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eis[i] = (0.5*self.rl*x[i]**2) + self.c1
            else:
                eis[i] = (0.5*self.rl*x[i]**2) + (self.ma*x[i]) + self.c2
        return eis

    def eid(self,x):
        iters = len(x)
        eid=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eid[i] = ((1/6.0)*self.rl*x[i]**3) + (self.c1*x[i]) + self.c3
            else:
                eid[i] = (1/6.0)*self.rl*x[i]**3 + (0.5*self.ma*x[i]**2) + (self.c2*x[i]) + self.c4
        return eid

    def vx(self,x):
        x = float(x)
        v = self.rl

        return v

    def mx(self,x):
        x = float(x)
        if x <= self.a:
            if x == 0 and self.a == 0:
                m = self.ma
            elif x == self.L and self.a == self.L:
                m = -1.0*self.ma
            else:
                m = self.rl * x
        else:
            m = (self.rl * x) + self.ma
        return m

    def eisx(self,x):
        x = float(x)
        if x <= self.a:
            eis = (0.5*self.rl*x**2) + self.c1
        else:
            eis = (0.5*self.rl*x**2) + (self.ma*x) + self.c2
        return eis

    def eidx(self,x):
        x = float(x)
        if x <= self.a:
            eid = ((1/6.0)*self.rl*x**3) + (self.c1*x) + self.c3
        else:
            eid = (1/6.0)*self.rl*x**3 + (0.5*self.ma*x**2) + (self.c2*x) + self.c4
        return eid

class udl:
    def __init__(self, w1, a, b, L):

        self.w1 = float(w1)
        self.a = float(a)
        self.L = float(L)
        self.b = float(b)
        self.c = b-a
        
        self.kind = 'UDL'
        
        self.error = ''
        
        if self.a > self.b:
            self.error = 'Error a > b'
            self.error = 'Error a > b'
        elif self.a > self.L:
            self.error = 'Error a > l'
            self.error = 'Error a > l'
        elif self.b > self.L:
            self.error = 'Error b > l'
            self.error = 'Error b > l'
        else:
            pass
            
        self.rl = (self.w1 * self.c) - (((self.w1 * self.c) * (self.a + (self.c / 2))) / self.L)
        self.rr = (((self.w1 * self.c) * (self.a + (self.c / 2))) / self.L)
        self.c1 = 0
        self.c2 = ((-1 * self.w1 * self.a ** 2) / 2)
        self.c3 = self.rr * self.L
        self.c7 = 0
        self.c8 = ((-1 * self.c1 * self.a ** 2) / 2) + ((self.c2 * self.a ** 2) / 2) + ((5 * self.w1 * self.a ** 4) / 24) + self.c7
        self.c9 = ((-1 * self.rl * self.b ** 3) / 3) - ((self.rr * self.b ** 3) / 3) + ((self.w1 * self.b ** 4) / 8) - ((self.w1 * self.a * self.b ** 3) / 3) - ((self.c2 * self.b ** 2) / 2) + ((self.c3 * self.b ** 2) / 2) + self.c8
        self.c6 = ((self.rr * self.L ** 2) / 6) - ((self.c3 * self.L) / 2) - (self.c9 / self.L)
        self.c5 = ((-1 * self.rl * self.b ** 2) / 2) + ((self.w1 * self.b ** 3) / 6) - ((self.w1 * self.a * self.b ** 2) / 2) - ((self.rr * self.b ** 2) / 2) + (self.c3 * self.b) - (self.c2 * self.b) + self.c6
        self.c4 = ((self.w1 * self.a ** 3) / 3) + (self.c2 * self.a) + self.c5 - (self.c1 * self.a)

        arrow_height = self.w1/12.0
        #30 degree arrow
        arrow_plus_start= self.a+(arrow_height*math.tan(math.radians(30)))
        arrow_minus_start= self.a-(arrow_height*math.tan(math.radians(30)))
        arrow_plus_end= self.b+(arrow_height*math.tan(math.radians(30)))
        arrow_minus_end= self.b-(arrow_height*math.tan(math.radians(30)))

        self.x_graph=[arrow_minus_start,self.a,arrow_plus_start,self.a,self.a,self.b,self.b,arrow_minus_end,self.b,arrow_plus_end]
        self.y_graph=[arrow_height,0,arrow_height,0,self.w1,self.w1,0,arrow_height,0,arrow_height]

    def v(self,x):
        iters = len(x)
        v=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                v[i] = self.rl
            elif x[i]<=self.b:
                v[i] = self.rl - (self.w1 * (x[i] - self.a))
            else:
                v[i] = -1 * self.rr
        return v

    def m(self,x):
        iters = len(x)
        m=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                m[i] = (self.rl * x[i]) + self.c1
            elif x[i] <= self.b:
                m[i] = (self.rl * x[i]) - ((self.w1 * x[i] ** 2) / 2) + (self.w1 * self.a * x[i]) + self.c2
            else:
                m[i] = (-1 * self.rr * x[i]) + self.c3
        return m

    def eis(self,x):
        iters = len(x)
        eis=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eis[i] = ((self.rl * x[i] ** 2) / 2.0) + (self.c1 * x[i]) + self.c4
            elif x[i] <= self.b:
                eis[i] = ((self.rl * x[i] **2) / 2.0) - ((self.w1 * x[i] ** 3) / 6.0) + ((self.w1 * self.a * x[i] **2) / 2.0) + (self.c2 * x[i]) + self.c5
            else:
                eis[i] = ((-1.0 * self.rr * x[i] ** 2) / 2.0) + (self.c3 * x[i]) + self.c6
        return eis

    def eid(self,x):
        iters = len(x)
        eid=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eid[i] = ((self.rl * x[i] ** 3) / 6) + ((self.c1 * x[i] ** 2) / 2) + (self.c4 * x[i]) + self.c7
            elif x[i]<=self.b:
                eid[i] = ((self.rl * x[i] ** 3) / 6) - ((self.w1 * x[i] ** 4) / 24) + ((self.w1 * self.a * x[i] ** 3) / 6) + ((self.c2 * x[i] ** 2) / 2) + (self.c5 * x[i]) + self.c8
            else:
                eid[i] = ((-1 * self.rr * x[i] ** 3) / 6) + ((self.c3 * x[i] ** 2) / 2) + (self.c6 * x[i]) + self.c9
        return eid

    def vx(self,x):
        x = float(x)
        if x <= self.a:
            v = self.rl
        elif x<=self.b:
            v = self.rl - (self.w1 * (x - self.a))
        else:
            v = -1 * self.rr
        return v

    def mx(self,x):
        x = float(x)
        if x <= self.a:
            m = (self.rl * x) + self.c1
        elif x <= self.b:
            m = (self.rl * x) - ((self.w1 * x ** 2) / 2) + (self.w1 * self.a * x) + self.c2
        else:
            m = (-1 * self.rr * x) + self.c3
        return m

    def eisx(self,x):
        x = float(x)
        if x <= self.a:
            eis = ((self.rl * x ** 2) / 2.0) + (self.c1 * x) + self.c4
        elif x <= self.b:
            eis = ((self.rl * x **2) / 2.0) - ((self.w1 * x ** 3) / 6.0) + ((self.w1 * self.a * x **2) / 2.0) + (self.c2 * x) + self.c5
        else:
            eis = ((-1.0 * self.rr * x ** 2) / 2.0) + (self.c3 * x) + self.c6
        return eis

    def eidx(self,x):
        x = float(x)
        if x <= self.a:
            eid = ((self.rl * x ** 3) / 6) + ((self.c1 * x ** 2) / 2) + (self.c4 * x) + self.c7
        elif x<=self.b:
            eid = ((self.rl * x ** 3) / 6) - ((self.w1 * x ** 4) / 24) + ((self.w1 * self.a * x ** 3) / 6) + ((self.c2 * x ** 2) / 2) + (self.c5 * x) + self.c8
        else:
            eid = ((-1 * self.rr * x ** 3) / 6) + ((self.c3 * x ** 2) / 2) + (self.c6 * x) + self.c9
        return eid

    def fef(self):
        eis0 = self.eisx(0)
        eisL = self.eisx(self.L)
        
        s = np.array([[-1.0*eis0],[-1.0*eisL]])
        
        ems = np.array([[-1.0*self.L/3.0 , self.L/6.0],[self.L/6.0 , -1.0*self.L/3.0]])
        
        fem = np.linalg.solve(ems,s)
        
        mo = point_moment(fem[0][0],0,self.L)
        ml = point_moment(fem[1][0],self.L,self.L)
        
        RL = self.rl+mo.rl+ml.rl
        RR = self.rr+mo.rr+ml.rr
        ML = fem[0][0]
        MR = fem[1][0]
        
        return [RL,ML,RR,MR]
        
class trap:
    def __init__(self, w1, w2, a, b, L):

        self.w1 = float(w1)
        self.w2 = float(w2)
        self.a = float(a)
        self.L = float(L)
        self.b = float(b)
        self.c = self.b-self.a
        
        self.kind = 'TRAP'
        
        
        self.error = ''
        
        if self.a > self.b:
            self.error = 'Error a > b'
            self.error = 'Error a > b'
        elif self.a > self.L:
            self.error = 'Error a > l'
            self.error = 'Error a > l'
        elif self.b > self.L:
            self.error = 'Error b > l'
            self.error = 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            self.error = 'Error w1 and w2 change direction'
            self.error = 'Error w1 and w2 change direction'
        else:
            pass
            
        self.s = (self.w2 -self.w1)/self.c
        self.xbar = (self.c * ((2 * self.w2) + self.w1)) / (3 * (self.w2 + self.w1))
        self.W = self.c * ((self.w1 + self.w2) / 2)
        self.rr = (self.W * (self.a + self.xbar)) / self.L
        self.rl = self.W - self.rr
        self.c1 = 0
        self.c2 = self.c1 + ((self.a ** 3 * self.s) / 6) + ((self.a ** 2 * (self.w1 - (self.s * self.a))) / 2) + ((((self.s * self.a) - (2 * self.w1)) * self.a ** 2) / 2)
        self.c3 = self.rr * self.L
        self.c7 = 0
        self.c8 = ((-1 * self.c1 * self.a ** 2) / 2) - ((self.a ** 5 * self.s) / 30) - ((self.a ** 4 * (self.w1 - (self.s * self.a))) / 8) - ((((self.s * self.a) - (2 * self.w1)) * self.a ** 4) / 6) + ((self.c2 * self.a ** 2) / 2) + self.c7
        self.c9 = ((-1 * self.rl * self.b ** 3) / 3) + ((self.b ** 5 * self.s) / 30) + ((self.b ** 4 * (self.w1 - (self.s * self.a))) / 8) + ((((self.s * self.a) - (2 * self.w1)) * self.a * self.b ** 3) / 6) - ((self.c2 * self.b ** 2) / 2) + self.c8 - ((self.rr * self.b ** 3) / 3) + ((self.c3 * self.b ** 2) / 2)
        self.c6 = (((self.rr * self.L ** 3) / 6) - ((self.c3 * self.L ** 2) / 2) - self.c9) / self.L
        self.c5 = ((-1 * self.rr * self.b ** 2) / 2) + (self.c3 * self.b) + self.c6 - ((self.rl * self.b ** 2) / 2) + ((self.b ** 4 * self.s) / 24) + ((self.b ** 3 * (self.w1 - (self.s * self.a))) / 6) + ((((self.s * self.a) - (2 * self.w1)) * self.a * self.b ** 2) / 4) - (self.c2 * self.b)
        self.c4 = ((-1 * self.a ** 4 * self.s) / 24) - ((self.a ** 3 * (self.w1 - (self.s * self.a))) / 6) - ((((self.s * self.a) - (2 * self.w1)) * self.a ** 3) / 4) + (self.c2 * self.a) + self.c5 - (self.c1 * self.a)

        arrow_height = self.w1/6.0
        arrow_height2 = self.w2/6.0
        #30 degree arrow
        arrow_plus_start= self.a+(arrow_height*math.tan(math.radians(30)))
        arrow_minus_start= self.a-(arrow_height*math.tan(math.radians(30)))
        arrow_plus_end= self.b+(arrow_height2*math.tan(math.radians(30)))
        arrow_minus_end= self.b-(arrow_height2*math.tan(math.radians(30)))

        self.x_graph=[arrow_minus_start,self.a,arrow_plus_start,self.a,self.a,self.b,self.b,arrow_minus_end,self.b,arrow_plus_end]
        self.y_graph=[arrow_height,0,arrow_height,0,self.w1,self.w2,0,arrow_height2,0,arrow_height2]

    def v(self,x):
        iters = len(x)
        v=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                v[i] = self.rl
            elif x[i]<=self.b:
                v[i] = self.rl - ((x[i] ** 2 * self.s) / 2) - (x[i] * (self.w1 - (self.s * self.a))) - ((((self.s * self.a) - (2 * self.w1)) * self.a) / 2)
            else:
                v[i] = -1 * self.rr
        return v

    def m(self,x):
        iters = len(x)
        m=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                m[i] = (self.rl * x[i]) + self.c1
            elif x[i] <= self.b:
                m[i] = (self.rl * x[i]) - ((x[i] ** 3 * self.s) / 6) - ((x[i] ** 2 * (self.w1 - (self.s * self.a))) / 2) - ((((self.s * self.a) - (2 * self.w1)) * self.a * x[i]) / 2) + self.c2
            else:
                m[i] = (-1 * self.rr * x[i]) + self.c3
        return m

    def eis(self,x):
        iters = len(x)
        eis=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eis[i] = ((self.rl * x[i] ** 2) / 2) + (self.c1 * x[i]) + self.c4
            elif x[i] <= self.b:
                eis[i] = ((self.rl * x[i] ** 2) / 2) - ((x[i] ** 4 * self.s) / 24) - ((x[i] ** 3 * (self.w1 - (self.s * self.a))) / 6) - ((((self.s * self.a) - (2 * self.w1)) * self.a * x[i] ** 2) / 4) + (self.c2 * x[i]) + self.c5
            else:
                eis[i] = ((-1 * self.rr * x[i] ** 2) / 2) + (self.c3 * x[i]) + self.c6
        return eis

    def eid(self,x):
        iters = len(x)
        eid=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eid[i] = ((self.rl * x[i] ** 3) / 6) + ((self.c1 * x[i] ** 2) / 2) + (self.c4 * x[i]) + self.c7
            elif x[i]<=self.b:
                eid[i] = ((self.rl * x[i] ** 3) / 6) - ((x[i] ** 5 * self.s) / 120) - ((x[i] ** 4 * (self.w1 - (self.s * self.a))) / 24) - ((((self.s * self.a) - (2 * self.w1)) * self.a * x[i] ** 3) / 12) + ((self.c2 * x[i] ** 2) / 2) + (self.c5 * x[i]) + self.c8
            else:
                eid[i] = ((-1 * self.rr * x[i] ** 3) / 6) + ((self.c3 * x[i] ** 2) / 2) + (self.c6 * x[i]) + self.c9
        return eid

    def vx(self,x):
        x = float(x)
        if x <= self.a:
            v = self.rl
        elif x<=self.b:
            v = self.rl - ((x ** 2 * self.s) / 2) - (x * (self.w1 - (self.s * self.a))) - ((((self.s * self.a) - (2 * self.w1)) * self.a) / 2)
        else:
            v = -1 * self.rr
        return v

    def mx(self,x):
        x = float(x)
        if x <= self.a:
            m = (self.rl * x) + self.c1
        elif x <= self.b:
            m = (self.rl * x) - ((x ** 3 * self.s) / 6) - ((x ** 2 * (self.w1 - (self.s * self.a))) / 2) - ((((self.s * self.a) - (2 * self.w1)) * self.a * x) / 2) + self.c2
        else:
            m = (-1 * self.rr * x) + self.c3
        return m

    def eisx(self,x):
        x = float(x)
        if x <= self.a:
            eis = ((self.rl * x ** 2) / 2) + (self.c1 * x) + self.c4
        elif x <= self.b:
            eis = ((self.rl * x ** 2) / 2) - ((x ** 4 * self.s) / 24) - ((x ** 3 * (self.w1 - (self.s * self.a))) / 6) - ((((self.s * self.a) - (2 * self.w1)) * self.a * x ** 2) / 4) + (self.c2 * x) + self.c5
        else:
            eis = ((-1 * self.rr * x ** 2) / 2) + (self.c3 * x) + self.c6
        return eis

    def eidx(self,x):
        x = float(x)
        if x <= self.a:
            eid = ((self.rl * x ** 3) / 6) + ((self.c1 * x ** 2) / 2) + (self.c4 * x) + self.c7
        elif x<=self.b:
            eid = ((self.rl * x ** 3) / 6) - ((x ** 5 * self.s) / 120) - ((x ** 4 * (self.w1 - (self.s * self.a))) / 24) - ((((self.s * self.a) - (2 * self.w1)) * self.a * x ** 3) / 12) + ((self.c2 * x ** 2) / 2) + (self.c5 * x) + self.c8
        else:
            eid = ((-1 * self.rr * x ** 3) / 6) + ((self.c3 * x ** 2) / 2) + (self.c6 * x) + self.c9
        return eid

    def fef(self):
        eis0 = self.eisx(0)
        eisL = self.eisx(self.L)
        
        s = np.array([[-1.0*eis0],[-1.0*eisL]])
        
        ems = np.array([[-1.0*self.L/3.0 , self.L/6.0],[self.L/6.0 , -1.0*self.L/3.0]])
        
        fem = np.linalg.solve(ems,s)
        
        mo = point_moment(fem[0][0],0,self.L)
        ml = point_moment(fem[1][0],self.L,self.L)
        
        RL = self.rl+mo.rl+ml.rl
        RR = self.rr+mo.rr+ml.rr
        ML = fem[0][0]
        MR = fem[1][0]
        
        return [RL,ML,RR,MR]
        
class cant_right_nl:
    def __init__(self, slope):
        self.slope = slope

        self.rl = 0
        self.ml = 0
        
        self.kind = 'NL'

    def v(self,x):
        iters = len(x)
        v=zeros(iters)

        return v

    def m(self,x):
        iters = len(x)
        m=zeros(iters)

        return m

    def eis(self,x):
        iters = len(x)
        eis=zeros(iters)
        for i in range(0,iters):
            eis[i] = self.slope

        return eis

    def eid(self,x):
        iters = len(x)
        eid=zeros(iters)
        for i in range(0,iters):
            eid[i] = self.slope * x[i]

        return eid

    def vx(self,x):
        v=0

        return v

    def mx(self,x):
        m=0

        return m

    def eisx(self,x):
        eis = self.slope

        return eis

    def eidx(self,x):
        eid = self.slope * x

        return eid

class cant_right_point:
    def __init__(self, p, a, L, Lb):

        self.p = float(p)
        self.a = float(a)
        self.L = float(L)
        self.Lb = float(Lb)
        self.b = self.L - self.a
        
        self.kind = 'Point'
        
        self.error = ''
        
        if self.a > self.L:
            self.error = 'Error a > l'
            self.error = 'Error a > l'

        self.rl = self.p
        self.ml = -1.0*self.p*self.a

        # 0 length backspan indicates fixed-free beam initialize slope to 0
        if Lb == 0:
            self.backspan = no_load()
            self.c1 = 0
        else:
            self.backspan = point_moment(-1.0*self.ml,self.Lb,self.Lb)
            self.c1 = self.backspan.eisx(self.Lb)

        self.c2 = 0
        self.c3 = 0.5*self.rl*self.a**2 + self.ml*self.a + self.c1
        self.c4 = -1.0*self.c3*self.a + (1.0/6.0)*self.rl*self.a**3 + 0.5*self.ml*self.a**2 + self.c1*self.a + self.c2

        arrow_height = self.p/6.0
        #30 degree arrow
        arrow_plus= self.a+(arrow_height*math.tan(math.radians(30)))
        arrow_minus= self.a-(arrow_height*math.tan(math.radians(30)))

        self.x_graph=[arrow_minus,self.a,arrow_plus,self.a,self.a]
        self.y_graph=[arrow_height,0,arrow_height,0,self.p]

    def v(self,x):
        iters = len(x)
        v=zeros(iters)

        for i in range(0,iters):
            if x[i]<=self.a:
                if x[i] == 0 and self.a == 0:
                    v[i] == 0
                else:
                    v[i] = self.p
            else:
                v[i] = 0
        return v

    def m(self,x):
        iters = len(x)
        m=zeros(iters)

        for i in range(0,iters):
            if x[i]<=self.a:
                m[i] = self.rl*x[i] + self.ml
            else:
                m[i] = 0
        return m

    def eis(self,x):
        iters = len(x)
        eis=zeros(iters)

        for i in range(0,iters):
            if x[i]<=self.a:
                eis[i] = 0.5*self.rl*x[i]**2 + self.ml*x[i] + self.c1
            else:
                eis[i] = self.c3
        return eis

    def eid(self,x):
        iters = len(x)
        eid=zeros(iters)

        for i in range(0,iters):
            if x[i]<=self.a:
                eid[i] = (1.0/6.0)*self.rl*x[i]**3 + 0.5*self.ml*x[i]**2 + self.c1*x[i] + self.c2
            else:
                eid[i] = self.c3*x[i] + self.c4
        return eid

    def vx(self,x):
        if x<=self.a:
            if x == 0 and self.a ==0:
                v = 0
            else:
                v = self.p
        else:
            v = 0
        return v

    def mx(self,x):
        if x<=self.a:
            m = self.rl*x + self.ml
        else:
            m = 0
        return m

    def eisx(self,x):
        if x<=self.a:
            eis = 0.5*self.rl*x**2 + self.ml*x + self.c1
        else:
            eis = self.c3
        return eis

    def eidx(self,x):
        if x<=self.a:
            eid = (1.0/6.0)*self.rl*x**3 + 0.5*self.ml*x**2 + self.c1*x + self.c2
        else:
            eid = self.c3*x + self.c4
        return eid

class cant_right_point_moment:
    def __init__(self, ma, a, L, Lb):

        self.ma = float(ma)
        self.a = float(a)
        self.L = float(L)
        self.Lb = float(Lb)
        self.b = self.L - self.a
        
        self.kind = 'Moment'

        self.error = ''
        
        if self.a > self.L:
            self.error = 'Error a > l'
            self.error = 'Error a > l'

        self.rl = 0
        self.ml = -1.0*self.ma

        # 0 length backspan indicates fixed-free beam initialize slope to 0
        if Lb == 0:
            self.backspan = no_load()
            self.c1 = 0
        else:
            self.backspan = point_moment(-1.0*self.ml,self.Lb,self.Lb)
            self.c1 = self.backspan.eisx(self.Lb)

        self.c2 = 0
        self.c3 = self.ml*self.a + self.c1
        self.c4 = 0.5*self.ml*self.a**2 + self.c1 * self.a + self.c2 - self.c3 * self.a

        r = (self.ma/8.0)
        arrow_height = r/6.0
        #30 degree arrow
        arrow_minus= (arrow_height*math.tan(math.radians(30)))

        if self.ma <0:
            self.x_graph = [self.a,self.a,self.a]
            self.y_graph = [r,0,-r]
            x=0
            y=0
            for a in range(-90, 181):
                x = self.a+(r*math.cos(math.radians(a)))
                y = 0+(r*math.sin(math.radians(a)))
                self.x_graph.append(x)
                self.y_graph.append(y)

            self.x_graph.append(x-arrow_minus)
            self.y_graph.append(y+arrow_height)
            self.x_graph.append(x)
            self.y_graph.append(y)
            self.x_graph.append(x+arrow_minus)
            self.y_graph.append(y+arrow_height)
        else:
            self.x_graph = [self.a-r,self.a,self.a+r, self.a+r-arrow_minus,self.a+r,self.a+r+arrow_minus,self.a+r]
            self.y_graph = [0,0,0,arrow_height,0,arrow_height,0]
            x=0
            y=0
            for a in range(0,271):
                x = self.a+(r*math.cos(math.radians(a)))
                y = 0+(r*math.sin(math.radians(a)))
                self.x_graph.append(x)
                self.y_graph.append(y)

    def v(self,x):
        iters = len(x)
        v=zeros(iters)

        for i in range(0,iters):
            if x[i]<=self.a:
                v[i] = 0
            else:
                v[i] = 0
        return v

    def m(self,x):
        iters = len(x)
        m=zeros(iters)

        for i in range(0,iters):
            if x[i]<=self.a:
                m[i] = self.ml
            else:
                m[i] = 0
        return m

    def eis(self,x):
        iters = len(x)
        eis=zeros(iters)

        for i in range(0,iters):
            if x[i]<=self.a:
                eis[i] = self.ml*x[i] + self.c1
            else:
                eis[i] = self.c3
        return eis

    def eid(self,x):
        iters = len(x)
        eid=zeros(iters)

        for i in range(0,iters):
            if x[i]<=self.a:
                eid[i] = 0.5*self.ml*x[i]**2 + self.c1*x[i] + self.c2
            else:
                eid[i] = self.c3*x[i] + self.c4
        return eid

    def vx(self,x):
        if x<=self.a:
            v = 0
        else:
            v = 0
        return v

    def mx(self,x):
        if x<=self.a:
            m = self.ml
        else:
            m = 0
        return m

    def eisx(self,x):
        if x<=self.a:
            eis = self.ml*x + self.c1
        else:
            eis = self.c3
        return eis

    def eidx(self,x):
        if x<=self.a:
            eid = 0.5*self.ml*x**2 + self.c1*x + self.c2
        else:
            eid = self.c3*x + self.c4
        return eid

class cant_right_udl:
    def __init__(self, w1, a, b, L, Lb):

        self.w1 = float(w1)
        self.a = float(a)
        self.L = float(L)
        self.b = float(b)
        self.c = self.b - self.a
        self.w_tot = self.w1*self.c
        self.Lb = float(Lb)
        
        self.kind = 'UDL'
        
        self.error = ''
        
        if self.a > self.b:
            self.error = 'Error a > b'
            self.error = 'Error a > b'
        elif self.a > self.L:
            self.error = 'Error a > l'
            self.error = 'Error a > l'
        elif self.b > self.L:
            self.error = 'Error b > l'
            self.error = 'Error b > l'
        else:
            pass
            
        self.rl = self.w_tot
        self.ml = -1.0*self.w_tot*(self.b-(self.c/2))

        # 0 length backspan indicates fixed-free beam initialize slope to 0
        if Lb == 0:
            self.backspan = no_load()
            self.c1 = 0
        else:
            self.backspan = point_moment(-1.0*self.ml,self.Lb,self.Lb)
            self.c1 = self.backspan.eisx(self.Lb)

        self.c2 = 0

        self.c3 = self.c1
        self.c4 = self.c1*self.a + self.c2 - self.c3*a

        self.c5 = 0.5*self.w_tot*self.b**2 + self.ml*self.b - (1.0/6.0)*self.w1*(self.b-self.a)**3 + self.c3
        self.c6 = (1.0/6.0)*self.w_tot*self.b**3 + 0.5*self.ml*self.b**2 - (1.0/24.0)*self.w1*(self.b-self.a)**4 + self.c3*self.b + self.c4 - self.c5*self.b

        arrow_height = self.w1/12.0
        #30 degree arrow
        arrow_plus_start= self.a+(arrow_height*math.tan(math.radians(30)))
        arrow_minus_start= self.a-(arrow_height*math.tan(math.radians(30)))
        arrow_plus_end= self.b+(arrow_height*math.tan(math.radians(30)))
        arrow_minus_end= self.b-(arrow_height*math.tan(math.radians(30)))

        self.x_graph=[arrow_minus_start,self.a,arrow_plus_start,self.a,self.a,self.b,self.b,arrow_minus_end,self.b,arrow_plus_end]
        self.y_graph=[arrow_height,0,arrow_height,0,self.w1,self.w1,0,arrow_height,0,arrow_height]

    def v(self,x):
        iters = len(x)
        v=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                v[i] = self.rl
            elif x[i]<=self.b:
                v[i] = self.rl - self.w1*(x[i]-self.a)
            else:
                v[i] = 0
        return v

    def m(self,x):
        iters = len(x)
        m=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                m[i] = self.rl*x[i] + self.ml
            elif x[i] <= self.b:
                m[i] = self.rl*x[i] + self.ml - (self.w1*(x[i]-self.a)*((x[i]-self.a)/2))
            else:
                m[i] = 0
        return m

    def eis(self,x):
        iters = len(x)
        eis=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eis[i] = 0.5*self.rl*x[i]**2 + self.ml*x[i] + self.c1
            elif x[i] <= self.b:
                eis[i] = 0.5*self.rl*x[i]**2 + self.ml*x[i] - ((1.0/6.0) * self.w1 * (x[i]-self.a)**3) + self.c3
            else:
                eis[i] = self.c5
        return eis

    def eid(self,x):
        iters = len(x)
        eid=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eid[i] = (1.0/6.0)*self.rl*x[i]**2 + 0.5*self.ml*x[i]**2 + self.c1 * x[i] + self.c2
            elif x[i] <= self.b:
                eid[i] = (1.0/6.0)*self.rl*x[i]**3 + 0.5*self.ml*x[i]**2 - (1.0/24.0)*self.w1*(x[i]-self.a)**4 + self.c3*x[i] + self.c4
            else:
                eid[i] = self.c5*x[i] + self.c6
        return eid

    def vx(self,x):
        x = float(x)
        if x <= self.a:
            v = self.w_tot
        elif x<=self.b:
            v = self.w_tot - self.w1*(x-self.a)
        else:
            v = 0
        return v

    def mx(self,x):
        x = float(x)
        if x <= self.a:
            m = self.rl*x + self.ml
        elif x <= self.b:
            m = self.rl*x + self.ml - (self.w1*(x-self.a)*((x-self.a)/2))
        else:
            m = 0
        return m

    def eisx(self,x):
        if x <= self.a:
            eis = 0.5*self.rl*x**2 + self.ml*x + self.c1
        elif x <= self.b:
            eis = 0.5*self.rl*x**2 + self.ml*x - ((1.0/6.0) * self.w1 * (x-self.a)**3) + self.c3
        else:
            eis = self.c5
        return eis

    def eidx(self,x):
        if x <= self.a:
            eid = (1.0/6.0)*self.rl*x**2 + 0.5*self.ml*x**2 + self.c1 * x + self.c2
        elif x <= self.b:
            eid = (1.0/6.0)*self.rl*x**3 + 0.5*self.ml*x**2 - (1.0/24.0)*self.w1*(x-self.a)**4 + self.c3*x + self.c4
        else:
            eid = self.c5*x + self.c6
        return eid

class cant_right_trap:
    def __init__(self, w1, w2, a, b, L, Lb):

        self.w1 = float(w1)
        self.w2 = float(w2)
        self.a = float(a)
        self.L = float(L)
        self.b = float(b)
        self.Lb = float(Lb)
        self.c = self.b-self.a
        
        self.kind = 'TRAP'

        self.error = ''
        
        if self.a > self.b:
            self.error = 'Error a > b'
            self.error = 'Error a > b'
        elif self.a > self.L:
            self.error = 'Error a > l'
            self.error = 'Error a > l'
        elif self.b > self.L:
            self.error = 'Error b > l'
            self.error = 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            self.error = 'Error w1 and w2 change direction'
            self.error = 'Error w1 and w2 change direction'
        else:
            pass
            
        self.w = 0.5*(self.w1+self.w2)*self.c
        self.d = self.a+(((self.w1+(2*self.w2))/(3*(self.w2+self.w1)))*self.c)
        self.s = (self.w1-self.w2)/self.c
        self.rl = self.w
        self.ml = -1*self.w*self.d

        # 0 length backspan indicates fixed-free beam initialize slope to 0
        if Lb == 0:
            self.backspan = no_load()
            self.c1 = 0
        else:
            self.backspan = point_moment(-1.0*self.ml,self.Lb,self.Lb)
            self.c1 = self.backspan.eisx(self.Lb)

        self.c2 = 0

        self.c3 = self.ml - (1.0/6.0)*self.s*self.a**3 + 0.5*(self.s*self.a + self.w1)*self.a**2 - 0.5*(self.s*self.a + 2*self.w1)*self.a**2

        self.c4 = self.c1 - (1.0/24.0)*self.s*self.a**4 + (1.0/6.0)*((self.s*self.a)+self.w1)*self.a**3 - 0.25*((self.s*self.a)+(2*self.w1))*self.a**3 - self.c3*self.a + self.ml*self.a
        self.c5 = self.c1*self.a + self.c2 - self.c4*self.a - (1.0/120.0)*self.s*self.a**5 + (1.0/24.0)*((self.s*self.a)+self.w1)*self.a**4 - (1.0/12.0)*((self.s*self.a)+(2*self.w1))*self.a**4 + 0.5*self.ml*self.a**2 - 0.5*self.c3*self.a**2

        self.c6 = (0.5*self.rl*self.b**2)+self.c3*self.b + (1.0/24.0)*self.s*self.b**4 - (1.0/6.0)*((self.s*self.a)+self.w1)*self.b**3 + 0.25*((self.s*self.a)+(2*self.w1))*self.a*self.b**2 + self.c4
        self.c7 = ((1.0/6.0)*self.rl*self.b**3) + 0.5*self.c3*self.b**2 + (1.0/120.0)*self.s*self.b**5 - (1.0/24.0)*((self.s*self.a)+self.w1)*self.b**4 + (1.0/12.0)*((self.s*self.a)+(2*self.w1))*self.a*self.b**3 + self.c4*self.b + self.c5 - self.c6*self.b

        arrow_height = self.w1/6.0
        arrow_height2 = self.w2/6.0
        #30 degree arrow
        arrow_plus_start= self.a+(arrow_height*math.tan(math.radians(30)))
        arrow_minus_start= self.a-(arrow_height*math.tan(math.radians(30)))
        arrow_plus_end= self.b+(arrow_height2*math.tan(math.radians(30)))
        arrow_minus_end= self.b-(arrow_height2*math.tan(math.radians(30)))

        self.x_graph=[arrow_minus_start,self.a,arrow_plus_start,self.a,self.a,self.b,self.b,arrow_minus_end,self.b,arrow_plus_end]
        self.y_graph=[arrow_height,0,arrow_height,0,self.w1,self.w2,0,arrow_height2,0,arrow_height2]

    def v(self,x):
        iters = len(x)
        v=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                v[i] = self.rl
            elif x[i]<=self.b:
                v[i] = self.rl + 0.5*self.s*x[i]**2 - x[i]*((self.s*self.a)+self.w1) + 0.5*self.a*((self.s*self.a)+(2*self.w1))
            else:
                v[i] =0
        return v

    def m(self,x):
        iters = len(x)
        m=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                m[i] = self.rl*x[i] + self.ml
            elif x[i] <= self.b:
                m[i] = self.rl*x[i] + self.c3 + (1.0/6.0)*self.s*x[i]**3 - 0.5*((self.s*self.a)+self.w1)*x[i]**2 + 0.5*((self.s*self.a)+(2*self.w1))*self.a*x[i]
            else:
                m[i] = 0
        return m

    def eis(self,x):
        iters = len(x)
        eis=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eis[i] = (0.5*self.rl*x[i]**2)+self.ml*x[i]+self.c1
            elif x[i] <= self.b:
                eis[i] = (0.5*self.rl*x[i]**2)+self.c3*x[i] + (1.0/24.0)*self.s*x[i]**4 - (1.0/6.0)*((self.s*self.a)+self.w1)*x[i]**3 + 0.25*((self.s*self.a)+(2*self.w1))*self.a*x[i]**2 + self.c4
            else:
                eis[i] = self.c6
        return eis

    def eid(self,x):
        iters = len(x)
        eid=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eid[i] = ((1.0/6.0)*self.rl*x[i]**3)+ 0.5*self.ml*x[i]**2 + self.c1*x[i] + self.c2
            elif x[i] <= self.b:
                eid[i] = ((1.0/6.0)*self.rl*x[i]**3) + 0.5*self.c3*x[i]**2 + (1.0/120.0)*self.s*x[i]**5 - (1.0/24.0)*((self.s*self.a)+self.w1)*x[i]**4 + (1.0/12.0)*((self.s*self.a)+(2*self.w1))*self.a*x[i]**3 + self.c4*x[i] + self.c5
            else:
                eid[i] = self.c6*x[i] + self.c7
        return eid

    def vx(self,x):
        if x <= self.a:
            v= self.rl
        elif x<=self.b:
            v= self.rl + 0.5*self.s*x**2 - x*((self.s*self.a)+self.w1) + 0.5*self.a*((self.s*self.a)+(2*self.w1))
        else:
            v =0
        return v

    def mx(self,x):
        if x <= self.a:
            m = self.rl*x + self.ml
        elif x <= self.b:
            m = self.rl*x + self.c3 + (1.0/6.0)*self.s*x**3 - 0.5*((self.s*self.a)+self.w1)*x**2 + 0.5*((self.s*self.a)+(2*self.w1))*self.a*x
        else:
            m = 0
        return m

    def eisx(self,x):
        if x <= self.a:
            eis = (0.5*self.rl*x**2)+self.ml*x+self.c1
        elif x <= self.b:
            eis = (0.5*self.rl*x**2)+self.c3*x + (1.0/24.0)*self.s*x**4 - (1.0/6.0)*((self.s*self.a)+self.w1)*x**3 + 0.25*((self.s*self.a)+(2*self.w1))*self.a*x**2 + self.c4
        else:
            eis = self.c6
        return eis

    def eidx(self,x):
        if x <= self.a:
            eid = ((1.0/6.0)*self.rl*x**3)+ 0.5*self.ml*x**2 + self.c1*x + self.c2
        elif x <= self.b:
            eid = ((1.0/6.0)*self.rl*x**3) + 0.5*self.c3*x**2 + (1.0/120.0)*self.s*x**5 - (1.0/24.0)*((self.s*self.a)+self.w1)*x**4 + (1.0/12.0)*((self.s*self.a)+(2*self.w1))*self.a*x**3 + self.c4*x + self.c5
        else:
            eid = self.c6*x + self.c7
        return eid

class cant_left_nl:
    def __init__(self, slope, L):
        self.L = float(L)
        self.slope = float(slope)
        self.c1 = self.slope
        self.c2 = -1.0*self.c1*self.L
        
        self.kind = 'NL'

        self.rr = 0
        self.mr = 0

    def v(self,x):
        iters = len(x)
        v=zeros(iters)

        return v

    def m(self,x):
        iters = len(x)
        m=zeros(iters)

        return m

    def eis(self,x):
        iters = len(x)
        eis=zeros(iters)
        for i in range(0,iters):
            eis[i] = self.c1

        return eis

    def eid(self,x):
        iters = len(x)
        eid=zeros(iters)
        for i in range(0,iters):
            eid[i] = self.c1* x[i] + self.c2

        return eid

    def vx(self,x):
        v=0

        return v

    def mx(self,x):
        m=0

        return m

    def eisx(self,x):
        eis = self.c1

        return eis

    def eidx(self,x):
        eid = self.c1 * x + self.c2

        return eid

class cant_left_point:
    def __init__(self, p, a, L,Lb):

        self.p = float(p)
        self.a = float(a)
        self.L = float(L)
        self.Lb = float(Lb)

        self.kind = 'Point'

        self.error = ''
        
        if self.a > self.L:
            self.error = 'Error a > l'
            self.error = 'Error a > l'

        self.rr = self.p
        self.mr = -1*self.p*(self.L-self.a)

        # 0 length backspan indicates fixed-free beam initialize slope to 0
        if self.Lb == 0:
            self.backspan = no_load()
            self.c3 = 0 + (0.5*self.p * (self.L-self.a)**2)
        else:
            self.backspan = point_moment(self.mr,0,self.Lb)
            self.c3 = self.backspan.eisx(0) + (0.5*self.p * (self.L-self.a)**2)

        self.c4 = ((1/6.0)*self.p*(self.L-self.a)**3) - (self.c3*self.L)
        self.c1 = self.c3
        self.c2 = (self.c3*self.a) + self.c4 - (self.c1*self.a)

        arrow_height = self.p/6.0
        #30 degree arrow
        arrow_plus= self.a+(arrow_height*math.tan(math.radians(30)))
        arrow_minus= self.a-(arrow_height*math.tan(math.radians(30)))

        self.x_graph=[arrow_minus,self.a,arrow_plus,self.a,self.a]
        self.y_graph=[arrow_height,0,arrow_height,0,self.p]

    def v(self,x):
        iters = len(x)
        v=zeros(iters)

        for i in range(0,iters):
            if x[i]<=self.a:
                v[i] = 0
            else:
                v[i] = -1*self.p
        return v

    def m(self,x):
        iters = len(x)
        m=zeros(iters)

        for i in range(0,iters):
            if x[i]<=self.a:
                m[i] = 0
            else:
                m[i] = -1*self.p * (x[i] - self.a)
        return m

    def eis(self,x):
        iters = len(x)
        eis=zeros(iters)

        for i in range(0,iters):
            if x[i]<=self.a:
                eis[i] = self.c1
            else:
                eis[i] = (-0.5*self.p * (x[i]-self.a)**2) + self.c3
        return eis

    def eid(self, x):
        iters = len(x)
        eid=zeros(iters)

        for i in range(0,iters):
            if x[i]<=self.a:
                eid[i] = self.c1*x[i] + self.c2
            else:
                eid[i] = (-1/6.0)*self.p*(x[i]-self.a)**3 + self.c3*x[i] + self.c4
        return eid

    def vx(self,x):
        if x<=self.a:
            v = 0
        else:
            v = -1*self.p
        return v

    def mx(self,x):
        if x<=self.a:
            m = 0
        else:
            m = -1*self.p * (x - self.a)
        return m

    def eisx(self,x):
        if x<=self.a:
            eis = self.c1
        else:
            eis  = (-0.5*self.p * (x-self.a)**2) + self.c3
        return eis

    def eidx(self, x):
        if x<=self.a:
            eid = self.c1*x + self.c2
        else:
            eid = (-1/6.0)*self.p*(x-self.a)**3 + self.c3*x + self.c4

        return eid

class cant_left_point_moment:
    def __init__(self, ma, a, L,Lb):

        self.ma = float(ma)
        self.a = float(a)
        self.L = float(L)
        self.Lb = float(Lb)

        self.kind = 'Moment'
        
        self.error = ''
        
        if self.a > self.L:
            self.error = 'Error a > l'
            self.error = 'Error a > l'

        self.rr = 0
        self.mr = self.ma

        # 0 length backspan indicates fixed-free beam initialize slope to 0
        if Lb == 0:
            self.backspan = no_load()
            self.c3 = 0 - (self.ma*self.L)
        else:
            self.backspan = point_moment(self.mr,0,Lb)
            self.c3 = self.backspan.eisx(0) - (self.ma*self.L)

        self.c4 = (-0.5*self.ma*self.L**2) - self.c3*self.L
        self.c1 = (1.0*self.ma*self.a) + self.c3
        self.c2 = 0.5*self.ma*self.a**2 + self.c3*self.a + self.c4 - self.c1*self.a

        r = (self.ma/8.0)
        arrow_height = r/6.0
        #30 degree arrow
        arrow_minus= (arrow_height*math.tan(math.radians(30)))

        if self.ma <0:
            self.x_graph = [self.a,self.a,self.a]
            self.y_graph = [r,0,-r]
            x=0
            y=0
            for a in range(-90, 181):
                x = self.a+(r*math.cos(math.radians(a)))
                y = 0+(r*math.sin(math.radians(a)))
                self.x_graph.append(x)
                self.y_graph.append(y)

            self.x_graph.append(x-arrow_minus)
            self.y_graph.append(y+arrow_height)
            self.x_graph.append(x)
            self.y_graph.append(y)
            self.x_graph.append(x+arrow_minus)
            self.y_graph.append(y+arrow_height)
        else:
            self.x_graph = [self.a-r,self.a,self.a+r, self.a+r-arrow_minus,self.a+r,self.a+r+arrow_minus,self.a+r]
            self.y_graph = [0,0,0,arrow_height,0,arrow_height,0]
            x=0
            y=0
            for a in range(0,271):
                x = self.a+(r*math.cos(math.radians(a)))
                y = 0+(r*math.sin(math.radians(a)))
                self.x_graph.append(x)
                self.y_graph.append(y)

    def v(self,x):
        iters = len(x)
        v=zeros(iters)

        for i in range(0,iters):
            if x[i]<=self.a:
                v[i] = 0
            else:
                v[i] = 0
        return v

    def m(self,x):
        iters = len(x)
        m=zeros(iters)

        for i in range(0,iters):
            if x[i]<=self.a:
                m[i] = 0
            else:
                m[i] = self.ma
        return m

    def eis(self,x):
        iters = len(x)
        eis=zeros(iters)

        for i in range(0,iters):
            if x[i]<=self.a:
                eis[i] = self.c1
            else:
                eis[i] = (self.ma * x[i]) + self.c3
        return eis

    def eid(self, x):
        iters = len(x)
        eid=zeros(iters)

        for i in range(0,iters):
            if x[i]<=self.a:
                eid[i] = self.c1*x[i] + self.c2
            else:
                eid[i] = (0.5)*self.ma*x[i]**2 + self.c3*x[i] + self.c4
        return eid

    def vx(self,x):
        if x<=self.a:
            v = 0
        else:
            v = 0
        return v

    def mx(self,x):
        if x<=self.a:
            m = 0
        else:
            m = self.ma
        return m

    def eisx(self,x):
        if x<=self.a:
            eis = self.c1
        else:
            eis = (self.ma * x) + self.c3
        return eis

    def eidx(self, x):
        if x<=self.a:
            eid = self.c1*x + self.c2
        else:
            eid = (0.5)*self.ma*x**2 + self.c3*x + self.c4
        return eid

class cant_left_udl:
    def __init__(self, w1, a, b, L, Lb):

        self.w1 = float(w1)
        self.a = float(a)
        self.L = float(L)
        self.Lb = float(Lb)
        self.b = float(b)
        self.c = self.b-self.a
        self.w_tot = self.w1*self.c
        
        self.kind = 'UDL'

        self.error = ''
        
        if self.a > self.b:
            self.error = 'Error a > b'
            self.error = 'Error a > b'
        elif self.a > self.L:
            self.error = 'Error a > l'
            self.error = 'Error a > l'
        elif self.b > self.L:
            self.error = 'Error b > l'
            self.error = 'Error b > l'
        else:
            pass
            
        self.rr = self.w_tot
        self.mr = -1.0*self.w_tot*(self.L-(a+(self.c/2.0)))

        # 0 length backspan indicates fixed-free beam initialize slope to 0
        if Lb == 0:
            self.backspan = no_load()
            self.c5 = 0 + (0.5 * self.w_tot * (self.L - (self.a + (0.5*self.c)))**2)
        else:
            self.backspan = point_moment(self.mr,0,Lb)
            self.c5 = self.backspan.eisx(0) + (0.5 * self.w_tot * (self.L - (self.a + (0.5*self.c)))**2)

        self.c6 = ((1.0/6.0)*self.w_tot * (self.L - (self.a + (0.5*self.c)))**3) - (self.c5*self.L)
        self.c3 =((-0.5)*self.w_tot * (self.b - (self.a + (0.5*self.c)))**2) + self.c5 + ((1.0/6.0)*self.w1*(b-a)**3)
        self.c1 = self.c3
        self.c4 = ((-1.0/6.0)*self.w_tot * (self.b - (self.a + (0.5*self.c)))**3) + (self.c5*self.b) + self.c6 + ((1.0/24.0)*self.w1*(self.b-self.a)**4) - (self.c3*self.b)
        self.c2 = (self.c3*self.a) + self.c4 - (self.c1*self.a)

        arrow_height = self.w1/12.0
        #30 degree arrow
        arrow_plus_start= self.a+(arrow_height*math.tan(math.radians(30)))
        arrow_minus_start= self.a-(arrow_height*math.tan(math.radians(30)))
        arrow_plus_end= self.b+(arrow_height*math.tan(math.radians(30)))
        arrow_minus_end= self.b-(arrow_height*math.tan(math.radians(30)))

        self.x_graph=[arrow_minus_start,self.a,arrow_plus_start,self.a,self.a,self.b,self.b,arrow_minus_end,self.b,arrow_plus_end]
        self.y_graph=[arrow_height,0,arrow_height,0,self.w1,self.w1,0,arrow_height,0,arrow_height]

    def v(self,x):
        iters = len(x)
        v=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                v[i] = 0
            elif x[i]<=self.b:
                v[i] = -1*self.w1*(x[i]-self.a)
            else:
                v[i] = -1*self.w_tot
        return v

    def m(self,x):
        iters = len(x)
        m=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                m[i] = 0
            elif x[i] <= self.b:
                m[i] = -0.5*self.w1*(x[i]-self.a)**2
            else:
                m[i] = -1.0 * self.w_tot * (x[i]-(self.a+(0.5*self.c)))
        return m

    def eis(self,x):
        iters = len(x)
        eis=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eis[i] = self.c1
            elif x[i] <= self.b:
                eis[i] = (-1.0/6.0)*self.w1*(x[i]-self.a)**3 + self.c3
            else:
                eis[i] = (-0.5 * self.w_tot * (x[i]-(self.a+(0.5*self.c)))**2) + self.c5
        return eis

    def eid(self,x):
        iters = len(x)
        eid=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eid[i] = self.c1*x[i] + self.c2
            elif x[i] <= self.b:
                eid[i] = (-1.0/24.0)*self.w1*(x[i]-self.a)**4 + self.c3*x[i] + self.c4
            else:
                eid[i] = ((-1.0/6.0) * self.w_tot * (x[i]-(self.a+(0.5*self.c)))**3) + self.c5*x[i] + self.c6
        return eid

    def vx(self,x):
        if x <= self.a:
            v = 0
        elif x<=self.b:
            v = -1*self.w1*(x-self.a)
        else:
            v = -1*self.w_tot
        return v

    def mx(self,x):
        if x <= self.a:
            m = 0
        elif x <= self.b:
            m = -0.5*self.w1*(x-self.a)**2
        else:
            m = -1.0 * self.w_tot * (x-(self.a+(0.5*self.c)))
        return m

    def eisx(self,x):
        if x <= self.a:
            eis = self.c1
        elif x <= self.b:
            eis = (-1.0/6.0)*self.w1*(x-self.a)**3 + self.c3
        else:
            eis = (-0.5 * self.w_tot * (x-(self.a+(0.5*self.c)))**2) + self.c5
        return eis

    def eidx(self,x):
        if x <= self.a:
            eid = self.c1*x+ self.c2
        elif x <= self.b:
            eid = (-1.0/24.0)*self.w1*(x-self.a)**4 + self.c3*x + self.c4
        else:
            eid = ((-1.0/6.0) * self.w_tot * (x-(self.a+(0.5*self.c)))**3) + self.c5*x + self.c6
        return eid

class cant_left_trap:

    def __init__(self, w1, w2, a, b, L, Lb):

        self.w1 = float(w1)
        self.w2 = float(w2)
        self.a = float(a)
        self.L = float(L)
        self.b = float(b)
        self.Lb = float(Lb)
        self.c = self.b-self.a
        
        self.kind = 'TRAP'
        
        self.error = ''
        
        if self.a > self.b:
            self.error = 'Error a > b'
            self.error = 'Error a > b'
        elif self.a > self.L:
            self.error = 'Error a > l'
            self.error = 'Error a > l'
        elif self.b > self.L:
            self.error = 'Error b > l'
            self.error = 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            self.error = 'Error w1 and w2 change direction'
            self.error = 'Error w1 and w2 change direction'
        else:
            pass
            
        self.w = 0.5*(self.w1+self.w2)*self.c
        self.dl = self.a+(((self.w1+(2*self.w2))/(3*(self.w2+self.w1)))*self.c)
        self.dr = self.L-self.dl
        self.s = (self.w1-self.w2)/self.c
        self.cc = (((self.w1+(2*self.w2))/(3*(self.w2+self.w1)))*self.c) + self.a
        self.rr = self.w
        self.mr = -1*self.rr*(self.L-self.cc)

        # 0 length backspan indicates fixed-free beam initialize slope to 0
        if Lb == 0:
            self.backspan = no_load()
            self.c6 = 0 + (0.5*self.w*(self.L-self.cc)**2)
        else:
            self.backspan = point_moment(self.mr,0,Lb)
            self.c6 = self.backspan.eisx(0) + (0.5*self.w*(self.L-self.cc)**2)

        self.c7 = ((1.0/6.0)*self.w*(self.L-self.cc)**3) - (self.c6*self.L)
        self.c3 = -1.0*((1.0/6.0)*self.a*((self.a**2 * self.s) - (3*self.a*((self.a*self.s) + self.w1)) + (3*self.a*((self.a*self.s) + (2*self.w1)))))
        self.c4 = (-0.5*self.w*(self.b-self.cc)**2) + self.c6 - (self.c3*self.b) - ((1.0/24.0)*self.b**2 *((self.b**2 * self.s) - (4*self.b*((self.a*self.s) + self.w1)) + (6*self.a*((self.a*self.s) + (2*self.w1)))))
        self.c5 = ((-1.0/6.0)*self.w*(self.b-self.cc)**3) + (self.c6*self.b)+self.c7-(0.5*self.c3*self.b**2)-(self.c4*self.b)-((1.0/120.0)*self.b**3 *((self.b**2 * self.s) - (5*self.b*((self.a*self.s) + self.w1)) + (10*self.a*((self.a*self.s) + (2*self.w1)))))
        self.c1 = ((1.0/24.0)*self.a**2 *((self.a**2 * self.s) - (4*self.a*((self.a*self.s) + self.w1)) + (6*self.a*((self.a*self.s) + (2*self.w1))))) + (self.c3*self.a) + self.c4
        self.c2 = ((1.0/120.0)*self.a**3 *((self.a**2 * self.s) - (5*self.a*((self.a*self.s) + self.w1)) + (10*self.a*((self.a*self.s) + (2*self.w1))))) + (0.5*self.c3*self.a**2) + (self.c4*self.a) + self.c5 - (self.c1*self.a)

        arrow_height = self.w1/6.0
        arrow_height2 = self.w2/6.0
        #30 degree arrow
        arrow_plus_start= self.a+(arrow_height*math.tan(math.radians(30)))
        arrow_minus_start= self.a-(arrow_height*math.tan(math.radians(30)))
        arrow_plus_end= self.b+(arrow_height2*math.tan(math.radians(30)))
        arrow_minus_end= self.b-(arrow_height2*math.tan(math.radians(30)))

        self.x_graph=[arrow_minus_start,self.a,arrow_plus_start,self.a,self.a,self.b,self.b,arrow_minus_end,self.b,arrow_plus_end]
        self.y_graph=[arrow_height,0,arrow_height,0,self.w1,self.w2,0,arrow_height2,0,arrow_height2]

    def v(self,x):
        iters = len(x)
        v=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                v[i] = 0
            elif x[i]<=self.b:
                v[i] = (-0.5*((2*self.w1)-(self.s*(x[i]-self.a))))*(x[i]-self.a)
            else:
                v[i] = -1*self.rr
        return v

    def m(self,x):
        iters = len(x)
        m=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                m[i] = 0
            elif x[i] <= self.b:
                m[i] = ((1.0/6.0)*x[i]*((x[i]**2 * self.s) - (3*x[i]*((self.a*self.s) + self.w1)) + (3*self.a*((self.a*self.s) + (2*self.w1))))) + self.c3
            else:
                m[i] = -1*self.w*(x[i]-self.cc)
        return m

    def eis(self,x):
        iters = len(x)
        eis=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eis[i] = self.c1
            elif x[i] <= self.b:
                eis[i] = ((1.0/24.0)*x[i]**2 *((x[i]**2 * self.s) - (4*x[i]*((self.a*self.s) + self.w1)) + (6*self.a*((self.a*self.s) + (2*self.w1))))) + (self.c3 * x[i]) + self.c4
            else:
                eis[i] = (-0.5*self.w*(x[i]-self.cc)**2) + self.c6
        return eis

    def eid(self,x):
        iters = len(x)
        eid=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eid[i] = self.c1*x[i] + self.c2
            elif x[i] <= self.b:
                eid[i] = ((1.0/120.0)*x[i]**3 *((x[i]**2 * self.s) - (5*x[i]*((self.a*self.s) + self.w1)) + (10*self.a*((self.a*self.s) + (2*self.w1))))) + (0.5*self.c3 * x[i]**2) + (self.c4*x[i]) + self.c5
            else:
                eid[i] = ((-1.0/6.0)*self.w*(x[i]-self.cc)**3) + (self.c6*x[i]) + self.c7
        return eid

    def vx(self,x):
        if x <= self.a:
            v = 0
        elif x<=self.b:
            v= (-0.5*((2*self.w1)-(self.s*(x-self.a))))*(x-self.a)
        else:
            v = -1*self.rr
        return v

    def mx(self,x):
        if x <= self.a:
            m = 0
        elif x <= self.b:
            m = ((1.0/6.0)*x*((x**2 * self.s) - (3*x*((self.a*self.s) + self.w1)) + (3*self.a*((self.a*self.s) + (2*self.w1))))) + self.c3
        else:
            m = -1*self.w*(x-self.cc)
        return m

    def eisx(self,x):
        if x <= self.a:
            eis = self.c1
        elif x <= self.b:
            eis = ((1.0/24.0)*x**2 *((x**2 * self.s) - (4*x*((self.a*self.s) + self.w1)) + (6*self.a*((self.a*self.s) + (2*self.w1))))) + (self.c3 * x) + self.c4
        else:
            eis = (-0.5*self.w*(x-self.cc)**2) + self.c6
        return eis

    def eidx(self,x):
        if x <= self.a:
            eid = self.c1*x + self.c2
        elif x <= self.b:
            eid = ((1.0/120.0)*x**3 *((x**2 * self.s) - (5*x*((self.a*self.s) + self.w1)) + (10*self.a*((self.a*self.s) + (2*self.w1))))) + (0.5*self.c3 * x**2) + (self.c4*x) + self.c5
        else:
            eid = ((-1.0/6.0)*self.w*(x-self.cc)**3) + (self.c6*x) + self.c7
        return eid

def fixed_free_left_by_stations(loads, number_of_stations):
    
    # Take a list of loads and integer ammount of stations and return 
    # lists of stations, shears, moments,E*I*Slopes, and E*I*Deflections
    #
    # loads should already be defined using the classes in this file
    #
    # Assumptions:
    # - all loads coming in will have the same span length
    # defined. Validation of this will be added at a later date.
    #
    # -Consistent unit definitions across load values and lengths
    
    L = loads[0].L
    
    iters = int(number_of_stations)
    
    # Review loads and add additional stations to capture load start
    # and end points. For Point/Point Moments add station directly before
    # and directly after load.
    extra_stations = np.array([0])
    
    for load in loads:
        if load.kind == 'Point':
            a = load.a
            b = min(load.L,a + 0.0001)
            c = max(0,a - 0.0001)
            extra_stations = np.append(extra_stations, [c,a,b])

        elif load.kind == 'Moment':
            a = load.a
            b = min(load.L,a + 0.0001)
            c = max(0,a - 0.0001)
            extra_stations = np.append(extra_stations, [c,a,b])

        elif load.kind == 'UDL':
            extra_stations = np.append(extra_stations, [load.a,load.b])
        
        elif load.kind == 'TRAP':
            extra_stations = np.append(extra_stations, [load.a,load.b])
            
        else:
            pass
    
    extra_stations = np.unique(extra_stations)
    
    # Generate station coordinates based on a step size of l / number of stations
    
    step = L / (number_of_stations * 1.00) # multply by 1.00 to force Float division
    
    xs = zeros(iters+1)
    
    xs[0] = 0
    
    for i in range(1,(iters+1)):
        if xs[i-1] + step > L:
            xs[i] = L
        else:
            xs[i] = xs[i-1] + step
    
    xs = np.append(xs, extra_stations)
    
    xs = np.sort(xs)
    
    xs = np.unique(xs)
    
    i = xs.shape[0]
    
    r = 0
    mr = 0
    v = zeros(i)
    m = zeros(i)
    eis = zeros(i)
    eid = zeros(i)
    
    for load in loads:
        r = r + load.rr
        mr = mr + load.mr
        v = v + load.v(xs)
        m = m + load.m(xs)
        eis = eis + load.eis(xs)
        eid = eid + load.eid(xs)
    
    result_list = [xs,r,mr,v,m,eis,eid]
    
    return result_list
    
def fixed_free_right_by_stations(loads, number_of_stations):
    
    # Take a list of loads and integer ammount of stations and return 
    # lists of stations, shears, moments,E*I*Slopes, and E*I*Deflections
    #
    # loads should already be defined using the classes in this file
    #
    # Assumptions:
    # - all loads coming in will have the same span length
    # defined. Validation of this will be added at a later date.
    #
    # -Consistent unit definitions across load values and lengths
    
    L = loads[0].L
    
    iters = int(number_of_stations)
    
    # Review loads and add additional stations to capture load start
    # and end points. For Point/Point Moments add station directly before
    # and directly after load.
    extra_stations = np.array([0])
    
    for load in loads:
        if load.kind == 'Point':
            a = load.a
            b = min(load.L,a + 0.0001)
            c = max(0,a - 0.0001)
            extra_stations = np.append(extra_stations, [c,a,b])

        elif load.kind == 'Moment':
            a = load.a
            b = min(load.L,a + 0.0001)
            c = max(0,a - 0.0001)
            extra_stations = np.append(extra_stations, [c,a,b])

        elif load.kind == 'UDL':
            extra_stations = np.append(extra_stations, [load.a,load.b])
        
        elif load.kind == 'TRAP':
            extra_stations = np.append(extra_stations, [load.a,load.b])
            
        else:
            pass
    
    extra_stations = np.unique(extra_stations)
    
    # Generate station coordinates based on a step size of l / number of stations
    
    step = L / (number_of_stations * 1.00) # multply by 1.00 to force Float division
    
    xs = zeros(iters+1)
    
    xs[0] = 0
    
    for i in range(1,(iters+1)):
        if xs[i-1] + step > L:
            xs[i] = L
        else:
            xs[i] = xs[i-1] + step
    
    xs = np.append(xs, extra_stations)
    
    xs = np.sort(xs)
    
    xs = np.unique(xs)
    
    i = xs.shape[0]
    
    r = 0
    ml = 0
    v = zeros(i)
    m = zeros(i)
    eis = zeros(i)
    eid = zeros(i)
    
    
    for load in loads:
        r = r + load.rl
        ml = ml + load.ml
        v = v + load.v(xs)
        m = m + load.m(xs)
        eis = eis + load.eis(xs)
        eid = eid + load.eid(xs)
    
    result_list = [xs,r,ml,v,m,eis,eid]
    
    return result_list

def fixed_free_at_x(loads, x):
    # Take a list of loads and x location in span and return 
    # shear, moment,E*I*Slope, and E*I*Deflection
    #
    # loads should already be defined using the classes in this file
    #
    # Assumptions:
    # - all loads coming in will have the same span length
    # defined. Validation of this will be added at a later date.
    #
    # -Consistent unit definitions across load values and lengths
    
    v = 0
    m = 0
    eis = 0
    eid = 0
    
    for load in loads:
        v = v + load.vx(x)
        m = m + load.mx(x)
        eis = eis + load.eisx(x)
        eid = eid + load.eidx(x)
    
    result_list = [v,m,eis,eid]
    
    return result_list

def pin_pin_single_span_at_x(loads, x):
    # Take a list of loads and x locatoin in span and return 
    # shear, moment,E*I*Slope, and E*I*Deflection
    #
    # loads should already be defined using the classes in this file
    #
    # Assumptions:
    # - all loads coming in will have the same span length
    # defined. Validation of this will be added at a later date.
    #
    # -Consistent unit definitions across load values and lengths
    
    v = 0
    m = 0
    eis = 0
    eid = 0
    
    for load in loads:
        v = v + load.vx(x)
        m = m + load.mx(x)
        eis = eis + load.eisx(x)
        eid = eid + load.eidx(x)
    
    result_list = [v,m,eis,eid]
    
    return result_list
    
def pin_pin_single_span_by_stations(loads, number_of_stations):
    
    # Take a list of loads and integer ammount of stations and return 
    # lists of stations, shears, moments,E*I*Slopes, and E*I*Deflections
    #
    # loads should already be defined using the classes in this file
    #
    # Assumptions:
    # - all loads coming in will have the same span length
    # defined. Validation of this will be added at a later date.
    #
    # -Consistent unit definitions across load values and lengths
    
    L = loads[0].L
    
    iters = int(number_of_stations)
    
    # Review loads and add additional stations to capture load start
    # and end points. For Point/Point Moments add station directly before
    # and directly after load.
    extra_stations = np.array([0])
    
    for load in loads:
        if load.kind == 'Point':
            a = load.a
            b = min(load.L,a + 0.0001)
            c = max(0,a - 0.0001)
            extra_stations = np.append(extra_stations, [c,a,b])

        elif load.kind == 'Moment':
            a = load.a
            b = min(load.L,a + 0.0001)
            c = max(0,a - 0.0001)
            extra_stations = np.append(extra_stations, [c,a,b])

        elif load.kind == 'UDL':
            extra_stations = np.append(extra_stations, [load.a,load.b])
        
        elif load.kind == 'TRAP':
            extra_stations = np.append(extra_stations, [load.a,load.b])
            
        else:
            pass
    
    extra_stations = np.unique(extra_stations)
    
    # Generate station coordinates based on a step size of l / number of stations
    
    step = L / (number_of_stations * 1.00) # multply by 1.00 to force Float division
    
    xs = zeros(iters+1)
    
    xs[0] = 0
    
    for i in range(1,(iters+1)):
        if xs[i-1] + step > L:
            xs[i] = L
        else:
            xs[i] = xs[i-1] + step
    
    xs = np.append(xs, extra_stations)
    
    xs = np.sort(xs)
    
    xs = np.unique(xs)
    
    i = xs.shape[0]
    
    rl = 0
    rr = 0
    v = zeros(i)
    m = zeros(i)
    eis = zeros(i)
    eid = zeros(i)
    
    
    for load in loads:
        rl = rl + load.rl
        rr = rr + load.rr
        v = v + load.v(xs)
        m = m + load.m(xs)
        eis = eis + load.eis(xs)
        eid = eid + load.eid(xs)
    
    result_list = [xs,rl,rr,v,m,eis,eid]
    
    return result_list

def fixed_end_moments_from_end_slopes(eis0, eisL, fed, L):
    #######################################################################################################
    #
    # Solve Simultaneous equation for fixed end moments knowing 
    # end slopes of simple beam at support points:
    #
    # By compatibility for fixed ends initial and final slope should be 0.
    #
    # Function expects consistent units for values, should produce accurate results for
    # both metric and imperial units.
    #
    #[s0, sL] = [M0,ML]*[eis0_M0, eis0_ML
    #                    eisL_M0, eisL_ML]
    # Where:
    # s0 = slope at 0 ft, or left end of beam, calculated for the single span simply supported beam
    # sL = slope at L ft, or right end of beam, calculated for the single span simply supported beam
    #
    # s's are to be independant of E, modulus of elasticity, and I, moment of inertia, therefore
    # either need to divide by E*I or provide s in terms of E*I*s
    #
    # M0 = fixed end moment at 0 ft, or left end
    # Ml = fixed end moment at L ft, or right end
    #
    # eis0_M0 = slope coefficient for M0 at 0 ft, or left end
    # eis0_Ml = slope coefficient for ML at 0 ft, or left end
    #
    # eisL_M0 = slope coefficient for M0 at L ft, or right end
    # eisL_Ml = slope coefficient for ML at L ft, or right end
    #
    # eis0 = E*I*Slope @ 0 ft or beam left end
    # eisL = E*I*Slope @ L ft or beam right end
    # fed = [1,1], where a 1 signifies the location is fixed
    # L = span length 
    #
    # Assumptions:
    # 1. consistent units are used for the inputs
    # 2. the slopes entered are the actual slope not 
    #    the inverse ie not the restoring slope
    #
    #######################################################################################################
    
    if fed[0] == 1 and fed[1] == 1:
        s = np.array([[-1.0*eis0],[-1.0*eisL]])
        
        ems = np.array([[-1.0*L/3.0 , L/6.0],[L/6.0 , -1.0*L/3.0]])
        
        fem = np.linalg.solve(ems,s)
        
    elif fed[0] == 1 and fed[1] == 0:
        fel= ((-1.0*eis0 * -3.0) / L)
        fem = np.array([[fel],[0]])
    
    elif fed[0] == 0 and fed[1] == 1:
        fer = ((-1.0*eisL * -3.0) / L)
        fem = np.array([[0],[fer]])
    
    else:
        fem = np.array([[0],[0]])
    
    return fem

def single_span_solve_fixed_ends_and_redundant_interiors(delta, reaction_points, L, fem):
    
    #######################################################################################################
    #
    # Solve Simultaneous equation for internal reactions and fixed end moments knowing 
    # deflection and end slopes of simple beam at support points:
    #
    # By compatibility for fixed ends initial and final slope should be 0, and deflection
    # at each interior support location should be 0.
    #
    # Function expects consistent units for values, should produce accurate results for
    # both metric and imperial units.
    #
    #[s0, sL, d1....di] = [M0,ML,p1....pi]*[eis0_M0, eis0_ML, eis0_p1......eis0_pi
    #                                       eisL_M0, eisL_ML, eisL_p1......eisL_pi
    #                                       eid_M0_p1,  eid_ML_p1, eid_p11.....eid_pi1
    #                                       eid_M0_pi,  eid_ML_pi, eid_p1i.....eid_pii]
    # Where:
    # s0 = slope at 0 ft, or left end of beam, calculated for the single span simply supported beam
    # sL = slope at L ft, or right end of beam, calculated for the single span simply supported beam
    # d1 = deflection at first interior support 1 location calculated for the single span simply supported beam
    # di = deflection at ith interior support i location calculated for the single span simply supported beam
    #
    # s and d are to be independant of E, modulus of elasticity, and I, moment of inertia, therefore
    # either need to divide by E*I or provide s and d in terms of E*I*s and E*I*d
    #
    # M0 = fixed end moment at 0 ft, or left end
    # Ml = fixed end moment at L ft, or right end
    # p1 = reaction at first interior support
    # pi = reaction at ith interior support
    #
    # eis0_M0 = slope coefficient for M0 at 0 ft, or left end
    # eis0_Ml = slope coefficient for ML at 0 ft, or left end
    # eis0_p1 = slope coefficient for first interior support at 0 ft, or left end
    # eis0_pi = slope coefficient for ith interior support at 0 ft, or left end
    #
    # eisL_M0 = slope coefficient for M0 at L ft, or right end
    # eisL_Ml = slope coefficient for ML at L ft, or right end
    # eisL_p1 = slope coefficient for first interior support at L ft, or right end
    # eisL_pi = slope coefficient for ith interior support at L ft, or right end
    #
    # eid_M0_p1 = deflection coefficient at first interior support for M0
    # eid_M0_p1 = deflection coefficient at first interior support for ML
    # eid_p11 = deflection coefficient at first interior support for first interior reaction
    # eid_pi1 = deflection coefficient at first interior support for ith interior reaction
    #
    # eid_M0_pi = deflection coefficient at ith interior support for M0
    # eid_M0_pi = deflection coefficient at ith interior support for ML
    # eid_p1i = deflection coefficient at ith interior support for first interior reaction
    # eid_pii = deflection coefficient at ith interior support for ith interior reaction
    #
    # Inputs:
    # delta = [eis0, eisL, eid1,...,eidi], list of deformation results for pin-pin beam from loading
    #   --note: deformation results must be in the order shown--
    # reaction_points = [p1,....,pi], list of locations of redundant interior supports
    # L = beam span
    # fem = [1,1], where a 1 signifies the location is fixed
    #
    # Assumptions:
    # 1. consistent units are used for the inputs
    # 2. the deformations entered are the actual deformations not 
    #    the inverse ie not the restoring deformation.
    #
    #######################################################################################################
    
    #build the coefficient matrix rows and the deflection values
    coeff_matrix = []
    
    delta = [-1.0*x for x in delta]
    
    #Start Moment Component
    mo = point_moment(1,0,L)
    ml = point_moment(1,L,L)
    
    coeff_matrix.append([mo.eisx(0)*fem[0],ml.eisx(0)*fem[1]])
    coeff_matrix.append([mo.eisx(L)*fem[0],ml.eisx(L)*fem[1]])
    
    for support in reaction_points:
        a = support
        
        point_load = pl(1,a,L)
        
        coeff_row = []
        
        coeff_row.append(mo.eidx(a)*fem[0])
        coeff_row.append(ml.eidx(a)*fem[1])
            
        for point in reaction_points:
                    
            x = point
            new_pl = pl(1,x,L)
            eid_p = new_pl.eidx(a)
            
            coeff_row.append(eid_p)
                   
        coeff_matrix[0].append(point_load.eisx(0))
        coeff_matrix[1].append(point_load.eisx(L))
            
        
        coeff_matrix.append(coeff_row)
        
    d = np.array(delta)
    coeff = np.array(coeff_matrix)
    
    if fem == [0,1]:
        d = np.delete(d, (0), axis=0)
        coeff = np.delete(coeff, (0), axis=0)
        coeff = np.delete(coeff, (0), axis=1)
        
        reaction_points = [0] + reaction_points
    
    elif fem == [1,0]:
        d = np.delete(d, (1), axis=0)
        coeff = np.delete(coeff, (1), axis=0)
        coeff = np.delete(coeff, (1), axis=1)
        
        reaction_points = [0] + reaction_points
        
    elif fem == [0,0]:
        d = np.delete(d, (0), axis=0)
        coeff = np.delete(coeff, (0), axis=0)
        coeff = np.delete(coeff, (0), axis=1)
        
        d = np.delete(d, (0), axis=0)
        coeff = np.delete(coeff, (0), axis=0)
        coeff = np.delete(coeff, (0), axis=1)
    else:
        reaction_points = [0,0] + reaction_points
        
    R = np.linalg.solve(coeff,d)
    
    #List of reactions defined as loads from class types above
    reactions_as_loads = []

    i = 0
    for reaction in R:
        if (fem == [1,0] or fem == [1,1]) and i == 0:
            m = reaction
            reactions_as_loads.append(point_moment(m,0,L))
        
        elif fem == [0,1] and i == 0:
            m = reaction
            reactions_as_loads.append(point_moment(m,L,L))
            
        elif fem == [1,1] and i == 1:
            m = reaction
            reactions_as_loads.append(point_moment(m,L,L))
            
        else:
            p = reaction
            a = reaction_points[i]
            reactions_as_loads.append(pl(p,a,L))
        
        i+=1

    return R, reactions_as_loads

