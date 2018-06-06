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
import math

class no_load:
    def __init__(self):
        self.p = 0
        self.rl = 0
        self.rr = 0
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
    def __init__(self, p, a, l):

        self.p = float(p)
        self.a = float(a)
        self.l = float(l)
        self.b = self.l - self.a

        if self.a > self.l:
            self.rl = 'Error a > l'
            self.rr = 'Error a > l'

        else:
            self.rl = (self.p*self.b)/self.l
            self.rr = (self.p*self.a)/self.l
            self.c4 = ((-1*self.rl * self.a ** 3) / 3) - ((self.rr * self.a ** 3) / 3) + ((self.rr * self.l * self.a ** 2) / 2)
            self.c2 = (-1 / self.l) * ((self.c4) + ((self.rr * self.l ** 3) / 3))
            self.c1 = ((-1*self.rr * self.a ** 2) / 2) - ((self.rl * self.a ** 2) / 2) + (self.rr * self.l * self.a) + self.c2

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
                m[i] = (-1 * self.rr * x[i]) + (self.rr * self.l)
        return m

    def eis(self,x):
        iters = len(x)
        eis=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eis[i] = ((self.rl * x[i] ** 2)  / 2) + self.c1
            else:
                eis[i] = ((-1.0 * self.rr * x[i] ** 2)/2.0) + (self.rr * self.l * x[i]) + self.c2
        return eis

    def eid(self,x):
        iters = len(x)
        eid=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                eid[i] = ((self.rl * x[i] ** 3) / 6) + (self.c1 * x[i])
            else:
                eid[i] = ((-1*self.rr * x[i] ** 3) / 6) + ((self.rr * self.l * x[i] ** 2) / 2) + (self.c2 * x[i]) + self.c4
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
            m = (-1 * self.rr * x) + (self.rr * self.l)
        return m

    def eisx(self,x):
        x = float(x)
        if x <= self.a:
            eisx = ((self.rl * x ** 2)  / 2) + self.c1
        else:
            eisx = ((-1.0 * self.rr * x ** 2)/2.0) + (self.rr * self.l * x) + self.c2
        return eisx

    def eidx(self,x):
        x = float(x)
        if x <= self.a:
            eid = ((self.rl * x ** 3) / 6) + (self.c1 * x)
        else:
            eid = ((-1*self.rr * x ** 3) / 6) + ((self.rr * self.l * x ** 2) / 2) + (self.c2 * x) + self.c4
        return eid

class point_moment:
    def __init__(self, ma, a, l):
        self.ma = ma
        self.a = a
        self.l = l

        self.rr = ma/l
        self.rl = -1.0*self.rr

        self.c2 = (-1.0/l) * ((ma*a**2) - (0.5*ma*a**2) + (self.rl * (l**3/6.0)) + (0.5*ma*l**2))
        self.c1 = ma*a + self.c2
        self.c3 = 0
        self.c4 = ((-1.0*self.rl*l**3)/6.0) - (0.5*ma*l**2) - (self.c2*l)

        r = (self.ma/2.0)
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
            v[i] = self.rl

        return v

    def m(self,x):
        iters = len(x)
        m=zeros(iters)

        for i in range(0,iters):
            if x[i] <= self.a:
                if x[i] == 0 and self.a == 0:
                    m[i] = self.ma
                elif x[i] == self.l and self.a == self.l:
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
            elif x == self.l and self.a == self.l:
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
    def __init__(self, w1, a, b, l):

        self.w1 = float(w1)
        self.a = float(a)
        self.l = float(l)
        self.b = float(b)
        self.c = b-a

        if self.a > self.b:
            self.rl = 'Error a > b'
            self.rr = 'Error a > b'
        elif self.a > self.l:
            self.rl = 'Error a > l'
            self.rr = 'Error a > l'
        elif self.b > self.l:
            self.rl = 'Error b > l'
            self.rr = 'Error b > l'
        else:
            self.rl = (self.w1 * self.c) - (((self.w1 * self.c) * (self.a + (self.c / 2))) / self.l)
            self.rr = (((self.w1 * self.c) * (self.a + (self.c / 2))) / self.l)
            self.c1 = 0
            self.c2 = ((-1 * self.w1 * self.a ** 2) / 2)
            self.c3 = self.rr * self.l
            self.c7 = 0
            self.c8 = ((-1 * self.c1 * self.a ** 2) / 2) + ((self.c2 * self.a ** 2) / 2) + ((5 * self.w1 * self.a ** 4) / 24) + self.c7
            self.c9 = ((-1 * self.rl * self.b ** 3) / 3) - ((self.rr * self.b ** 3) / 3) + ((self.w1 * self.b ** 4) / 8) - ((self.w1 * self.a * self.b ** 3) / 3) - ((self.c2 * self.b ** 2) / 2) + ((self.c3 * self.b ** 2) / 2) + self.c8
            self.c6 = ((self.rr * self.l ** 2) / 6) - ((self.c3 * self.l) / 2) - (self.c9 / self.l)
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

class trap:
    def __init__(self, w1, w2, a, b, l):

        self.w1 = float(w1)
        self.w2 = float(w2)
        self.a = float(a)
        self.l = float(l)
        self.b = float(b)
        self.c = self.b-self.a

        if self.a > self.b:
            self.rl = 'Error a > b'
            self.rr = 'Error a > b'
        elif self.a > self.l:
            self.rl = 'Error a > l'
            self.rr = 'Error a > l'
        elif self.b > self.l:
            self.rl = 'Error b > l'
            self.rr = 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            self.rl = 'Error w1 and w2 change direction'
            self.rr = 'Error w1 and w2 change direction'
        else:
            self.s = (self.w2 -self.w1)/self.c
            self.xbar = (self.c * ((2 * self.w2) + self.w1)) / (3 * (self.w2 + self.w1))
            self.W = self.c * ((self.w1 + self.w2) / 2)
            self.rr = (self.W * (self.a + self.xbar)) / self.l
            self.rl = self.W - self.rr
            self.c1 = 0
            self.c2 = self.c1 + ((self.a ** 3 * self.s) / 6) + ((self.a ** 2 * (self.w1 - (self.s * self.a))) / 2) + ((((self.s * self.a) - (2 * self.w1)) * self.a ** 2) / 2)
            self.c3 = self.rr * self.l
            self.c7 = 0
            self.c8 = ((-1 * self.c1 * self.a ** 2) / 2) - ((self.a ** 5 * self.s) / 30) - ((self.a ** 4 * (self.w1 - (self.s * self.a))) / 8) - ((((self.s * self.a) - (2 * self.w1)) * self.a ** 4) / 6) + ((self.c2 * self.a ** 2) / 2) + self.c7
            self.c9 = ((-1 * self.rl * self.b ** 3) / 3) + ((self.b ** 5 * self.s) / 30) + ((self.b ** 4 * (self.w1 - (self.s * self.a))) / 8) + ((((self.s * self.a) - (2 * self.w1)) * self.a * self.b ** 3) / 6) - ((self.c2 * self.b ** 2) / 2) + self.c8 - ((self.rr * self.b ** 3) / 3) + ((self.c3 * self.b ** 2) / 2)
            self.c6 = (((self.rr * self.l ** 3) / 6) - ((self.c3 * self.l ** 2) / 2) - self.c9) / self.l
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

class cant_right_nl:
    def __init__(self, slope):
        self.slope = slope

        self.rl = 0
        self.ml = 0

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
    def __init__(self, p, a, l, lb):

        self.p = float(p)
        self.a = float(a)
        self.l = float(l)
        self.lb = float(lb)
        self.b = self.l - self.a

        if self.a > self.l:
            self.rl = 'Error a > l'
            self.ml = 'Error a > l'

        else:
            self.rl = self.p
            self.ml = -1.0*self.p*self.a

        # 0 length backspan indicates fixed-free beam initialize slope to 0
        if lb == 0:
            self.backspan = no_load()
            self.c1 = 0
        else:
            self.backspan = point_moment(-1.0*self.ml,self.lb,self.lb)
            self.c1 = self.backspan.eisx(self.lb)

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
    def __init__(self, ma, a, l, lb):

        self.ma = float(ma)
        self.a = float(a)
        self.l = float(l)
        self.lb = float(lb)
        self.b = self.l - self.a

        if self.a > self.l:
            self.rl = 'Error a > l'
            self.ml = 'Error a > l'

        else:
            self.rl = 0
            self.ml = -1.0*self.ma

        # 0 length backspan indicates fixed-free beam initialize slope to 0
        if lb == 0:
            self.backspan = no_load()
            self.c1 = 0
        else:
            self.backspan = point_moment(-1.0*self.ml,self.lb,self.lb)
            self.c1 = self.backspan.eisx(self.lb)

        self.c2 = 0
        self.c3 = self.ml*self.a + self.c1
        self.c4 = 0.5*self.ml*self.a**2 + self.c1 * self.a + self.c2 - self.c3 * self.a

        r = (self.ma/2.0)
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
    def __init__(self, w1, a, b, l, lb):

        self.w1 = float(w1)
        self.a = float(a)
        self.l = float(l)
        self.b = float(b)
        self.c = self.b - self.a
        self.w_tot = self.w1*self.c
        self.lb = float(lb)

        if self.a > self.b:
            self.rl = 'Error a > b'
            self.ml = 'Error a > b'
        elif self.a > self.l:
            self.rl = 'Error a > l'
            self.ml = 'Error a > l'
        elif self.b > self.l:
            self.rl = 'Error b > l'
            self.ml = 'Error b > l'
        else:
            self.rl = self.w_tot
            self.ml = -1.0*self.w_tot*(self.b-(self.c/2))

        # 0 length backspan indicates fixed-free beam initialize slope to 0
        if lb == 0:
            self.backspan = no_load()
            self.c1 = 0
        else:
            self.backspan = point_moment(-1.0*self.ml,self.lb,self.lb)
            self.c1 = self.backspan.eisx(self.lb)

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
    def __init__(self, w1, w2, a, b, l, lb):

        self.w1 = float(w1)
        self.w2 = float(w2)
        self.a = float(a)
        self.l = float(l)
        self.b = float(b)
        self.lb = float(lb)
        self.c = self.b-self.a

        if self.a > self.b:
            self.rl = 'Error a > b'
            self.ml = 'Error a > b'
        elif self.a > self.l:
            self.rl = 'Error a > l'
            self.ml = 'Error a > l'
        elif self.b > self.l:
            self.rl = 'Error b > l'
            self.ml = 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            self.rl = 'Error w1 and w2 change direction'
            self.ml = 'Error w1 and w2 change direction'
        else:
            self.w = 0.5*(self.w1+self.w2)*self.c
            self.d = self.a+(((self.w1+(2*self.w2))/(3*(self.w2+self.w1)))*self.c)
            self.s = (self.w1-self.w2)/self.c
            self.rl = self.w
            self.ml = -1*self.w*self.d

        # 0 length backspan indicates fixed-free beam initialize slope to 0
        if lb == 0:
            self.backspan = no_load()
            self.c1 = 0
        else:
            self.backspan = point_moment(-1.0*self.ml,self.lb,self.lb)
            self.c1 = self.backspan.eisx(self.lb)

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
    def __init__(self, slope, l):
        self.l = l
        self.slope = slope
        self.c1 = self.slope
        self.c2 = -1.0*self.c1*self.l

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
    def __init__(self, p, a, l,lb):

        self.p = float(p)
        self.a = float(a)
        self.l = float(l)


        if self.a > self.l:
            self.rr = 'Error a > l'
            self.mr = 'Error a > l'

        else:
            self.rr = self.p
            self.mr = -1*self.p*(self.l-self.a)

        # 0 length backspan indicates fixed-free beam initialize slope to 0
        if lb == 0:
            self.backspan = no_load()
            self.c3 = 0 + (0.5*self.p * (self.l-self.a)**2)
        else:
            self.backspan = point_moment(self.mr,0,lb)
            self.c3 = self.backspan.eisx(0) + (0.5*self.p * (self.l-self.a)**2)

        self.c4 = ((1/6.0)*self.p*(self.l-self.a)**3) - (self.c3*self.l)
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
    def __init__(self, ma, a, l,lb):

        self.ma = float(ma)
        self.a = float(a)
        self.l = float(l)
        self.lb = float(lb)


        if self.a > self.l:
            self.rr = 'Error a > l'
            self.mr = 'Error a > l'

        else:
            self.rr = 0
            self.mr = self.ma

        # 0 length backspan indicates fixed-free beam initialize slope to 0
        if lb == 0:
            self.backspan = no_load()
            self.c3 = 0 - (self.ma*self.l)
        else:
            self.backspan = point_moment(self.mr,0,lb)
            self.c3 = self.backspan.eisx(0) - (self.ma*self.l)

        self.c4 = (-0.5*self.ma*self.l**2) - self.c3*self.l
        self.c1 = (1.0*self.ma*self.a) + self.c3
        self.c2 = 0.5*self.ma*self.a**2 + self.c3*self.a + self.c4 - self.c1*self.a

        r = (self.ma/2.0)
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
    def __init__(self, w1, a, b, l, lb):

        self.w1 = float(w1)
        self.a = float(a)
        self.l = float(l)
        self.lb = float(lb)
        self.b = float(b)
        self.c = self.b-self.a
        self.w_tot = self.w1*self.c

        if self.a > self.b:
            self.rr = 'Error a > b'
            self.mr = 'Error a > b'
        elif self.a > self.l:
            self.rr = 'Error a > l'
            self.mr = 'Error a > l'
        elif self.b > self.l:
            self.rr = 'Error b > l'
            self.mr = 'Error b > l'
        else:
            self.rr = self.w_tot
            self.mr = -1.0*self.w_tot*(self.l-(a+(self.c/2.0)))

        # 0 length backspan indicates fixed-free beam initialize slope to 0
        if lb == 0:
            self.backspan = no_load()
            self.c5 = 0 + (0.5 * self.w_tot * (self.l - (self.a + (0.5*self.c)))**2)
        else:
            self.backspan = point_moment(self.mr,0,lb)
            self.c5 = self.backspan.eisx(0) + (0.5 * self.w_tot * (self.l - (self.a + (0.5*self.c)))**2)

        self.c6 = ((1.0/6.0)*self.w_tot * (self.l - (self.a + (0.5*self.c)))**3) - (self.c5*self.l)
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
    def __init__(self, w1, w2, a, b, l, lb):

        self.w1 = float(w1)
        self.w2 = float(w2)
        self.a = float(a)
        self.l = float(l)
        self.b = float(b)
        self.lb = float(lb)
        self.c = self.b-self.a

        self.w = 0.5*(self.w1+self.w2)*self.c
        self.dl = self.a+(((self.w1+(2*self.w2))/(3*(self.w2+self.w1)))*self.c)
        self.dr = self.l-self.dl
        self.s = (self.w1-self.w2)/self.c
        self.cc = (((self.w1+(2*self.w2))/(3*(self.w2+self.w1)))*self.c) + self.a

        if self.a > self.b:
            self.rr = 'Error a > b'
            self.mr = 'Error a > b'
        elif self.a > self.l:
            self.rr = 'Error a > l'
            self.mr = 'Error a > l'
        elif self.b > self.l:
            self.rr = 'Error b > l'
            self.mr = 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            self.rr = 'Error w1 and w2 change direction'
            self.mr = 'Error w1 and w2 change direction'
        else:
            self.rr = self.w
            self.mr = -1*self.rr*(self.l-self.cc)

        # 0 length backspan indicates fixed-free beam initialize slope to 0
        if lb == 0:
            self.backspan = no_load()
            self.c6 = 0 + (0.5*self.w*(self.l-self.cc)**2)
        else:
            self.backspan = point_moment(self.mr,0,lb)
            self.c6 = self.backspan.eisx(0) + (0.5*self.w*(self.l-self.cc)**2)

        self.c7 = ((1.0/6.0)*self.w*(self.l-self.cc)**3) - (self.c6*self.l)
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
