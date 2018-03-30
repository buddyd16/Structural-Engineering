from __future__ import division
from numpy import sign
from numpy import zeros


#def pl( p, a, l, x):
#    b = l - a
#    rl = (p * b) / l    
#    rr = (p * a) / l
#    c4 = ((-rl * a ** 3) / 3) - ((rr * a ** 3) / 3) + ((rr * l * a ** 2) / 2)    
#    c2 = (-1 / l) * ((c4) + ((rr * l ** 3) / 3))    
#    c1 = ((-rr * a ** 2) / 2) - ((rl * a ** 2) / 2) + (rr * l * a) + c2
#    if x <= a:
#        v = rl
#        m = rl * x
#        d = ((rl * x ** 3) / 6) + (c1 * x)
#    else:
#        v = -1 * rr
#        m = (-1 * rr * x) + (rr * l)
#        d = ((-rr * x ** 3) / 6) + ((rr * l * x ** 2) / 2) + (c2 * x) + c4
#    return (rl, rr, v, m, d)
    

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
    
    
    def v(self,x):
        if self.a > self.l:
            return 'Error a > l'
        else:
            iters = len(x)            
            v=zeros(iters)
            
            for i in range(0,iters):
                if x[i] <= self.a:
                    v[i] = self.rl           
                else:
                    v[i] = -1 * self.rr
            return v
    
    def m(self,x):
        if self.a > self.l:
            return 'Error a > l'
        else:
            iters = len(x)            
            m=zeros(iters)
            
            for i in range(0,iters):
                if x[i] <= self.a:
                    m[i] = self.rl * x[i]           
                else:
                    m[i] = (-1 * self.rr * x[i]) + (self.rr * self.l)
            return m

    def eis(self,x):
        if self.a > self.l:
            return 'Error a > l'
        else:
            iters = len(x)            
            eis=zeros(iters)
            
            for i in range(0,iters):
                if x[i] <= self.a:
                    eis[i] = ((self.rl * x[i] ** 2)  / 2) + self.c1       
                else:
                    eis[i] = ((-1.0 * self.rr * x[i] ** 2)/2.0) + (self.rr * self.l * x[i]) + self.c2
            return eis
    
    def eid(self,x):
        if self.a > self.l:
            return 'Error a > l'
        else:
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
        if self.a > self.l:
            return 'Error a > l'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                v = self.rl           
            else:
                v = -1 * self.rr
            return v
    
    def mx(self,x):
        x = float(x)
        if self.a > self.l:
            return 'Error a > l'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                m = self.rl * x           
            else:
                m = (-1 * self.rr * x) + (self.rr * self.l)
            return m

    def eisx(self,x):
        x = float(x)
        if self.a > self.l:
            return 'Error a > l'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                eisx = ((self.rl * x ** 2)  / 2) + self.c1       
            else:
                eisx = ((-1.0 * self.rr * x ** 2)/2.0) + (self.rr * self.l * x) + self.c2
            return eisx
    
    def eidx(self,x):
        x = float(x)
        if self.a > self.l:
            return 'Error a > l'
        elif x > self.l:
            return 'Error x > l'
        else:                        
            if x <= self.a:
                eid = ((self.rl * x ** 3) / 6) + (self.c1 * x)           
            else:
                eid = ((-1*self.rr * x ** 3) / 6) + ((self.rr * self.l * x ** 2) / 2) + (self.c2 * x) + self.c4
            return eid

class point_moment:
    def __init__(self, m, a, l):
        self.m = m
        self.a = a
        self.l = l
        
        self.rr = m/l
        self.rl = -1.0*self.rr
        
        self.c2 = (-1.0/l) * ((m*a**2) - (0.5*m*a**2) + (self.rl * (l**3/6.0)) + (0.5*m*l**2))
        self.c1 = m*a + self.c2
        self.c3 = 0
        self.c4 = ((-1.0*self.rl*l**3)/6.0) - (0.5*m*l**2) - (self.c2*l)

    def v(self,x):
        if self.a > self.l:
            return 'Error a > l'
        else:
            iters = len(x)
            v=zeros(iters)
            
            for i in range(0,iters):
                v[i] = self.rl

            return v

    def mo(self,x):
        if self.a > self.l:
            return 'Error a > l'
        else:
            iters = len(x)            
            mo=zeros(iters)
            
            for i in range(0,iters):
                if x[i] < self.a:
                    mo[i] = self.rl * x[i]
                else:
                    mo[i] = (self.rl * x[i]) + self.m
            return mo
    
    def eis(self,x):
        if self.a > self.l:
            return 'Error a > l'
        else:
            iters = len(x)            
            eis=zeros(iters)
            
            for i in range(0,iters):
                if x[i] <= self.a:
                    eis[i] = (0.5*self.rl*x[i]**2) + self.c1
                else:
                    eis[i] = (0.5*self.rl*x[i]**2) + (self.m*x[i]) + self.c2
            return eis
            
    def eid(self,x):
        if self.a > self.l:
            return 'Error a > l'
        else:
            iters = len(x)            
            eid=zeros(iters)
            
            for i in range(0,iters):
                if x[i] <= self.a:
                    eid[i] = ((1/6.0)*self.rl*x[i]**3) + (self.c1*x[i]) + self.c3
                else:
                    eid[i] = (1/6.0)*self.rl*x[i]**3 + (0.5*self.m*x[i]**2) + (self.c2*x[i]) + self.c4
            return eid
            
    def vx(self,x):
        x = float(x)
        if self.a > self.l:
            return 'Error a > l'
        elif x > self.l:
            return 'Error x > l'
        else:
            v = self.rl
        
        return v
        
    def mx(self,x):
        x = float(x)
        if self.a > self.l:
            return 'Error a > l'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                m = self.rl * x
            else:
                m = (self.rl * x) + self.m
            return m
    
    def eisx(self,x):
        x = float(x)
        if self.a > self.l:
            return 'Error a > l'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                eis = (0.5*self.rl*x**2) + self.c1
            else:
                eis = (0.5*self.rl*x**2) + (self.m*x) + self.c2
            return eis
    
    def eidx(self,x):
        x = float(x)
        if self.a > self.l:
            return 'Error a > l'
        elif x > self.l:
            return 'Error x > l'
        else:                        
            if x <= self.a:
                eid = ((1/6.0)*self.rl*x**3) + (self.c1*x) + self.c3
            else:
                eid = (1/6.0)*self.rl*x**3 + (0.5*self.m*x**2) + (self.c2*x) + self.c4
            return eid
        
#def udl( W, a, b, l, x):
#    c = a + b
#    rl = (W * b) - (((W * b) * (a + (b / 2))) / l)
#    rr = (((W * b) * (a + (b / 2))) / l)
#    c1 = 0
#    c2 = ((-1 * W * a ** 2) / 2)
#    c3 = rr * l
#    c7 = 0
#    c8 = ((-1 * c1 * a ** 2) / 2) + ((c2 * a ** 2) / 2) + ((5 * W * a ** 4) / 24) + c7
#    c9 = ((-1 * rl * c ** 3) / 3) - ((rr * c ** 3) / 3) + ((W * c ** 4) / 8) - ((W * a * c ** 3) / 3) - ((c2 * c ** 2) / 2) + ((c3 * c ** 2) / 2) + c8
#    c6 = ((rr * l ** 2) / 6) - ((c3 * l) / 2) - (c9 / l)
#    c5 = ((-1 * rl * c ** 2) / 2) + ((W * c ** 3) / 6) - ((W * a * c ** 2) / 2) - ((rr * c ** 2) / 2) + (c3 * c) - (c2 * c) + c6
#    c4 = ((W * a ** 3) / 3) + (c2 * a) + c5 - (c1 * a)  
#    if x <= a:
#        v = rl
#        m = (rl * x) + c1
#        d = ((rl * x ** 3) / 6) + ((c1 * x ** 2) / 2) + (c4 * x) + c7
#    elif x<c:
#        v = rl - (W * (x - a))
#        m = (rl * x) - ((W * x ** 2) / 2) + (W * a * x) + c2
#        d = ((rl * x ** 3) / 6) - ((W * x ** 4) / 24) + ((W * a * x ** 3) / 6) + ((c2 * x ** 2) / 2) + (c5 * x) + c8
#    else:
#        v = -rr
#        m = (-1 * rr * x) + c3
#        d = ((-1 * rr * x ** 3) / 6) + ((c3 * x ** 2) / 2) + (c6 * x) + c9
#    return (rl, rr, v, m ,d)


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
    
    
    def v(self,x):
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        else:
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
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        else:
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
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        else:
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
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        else:
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
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                v = self.rl           
            elif x<=self.b:
                v = self.rl - (self.w1 * (x - self.a))
            else:
                v = -1 * self.rr
        return v
    
    def mx(self,x):
        x = float(x)
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                m = (self.rl * x) + self.c1
            elif x <= self.b:
                m = (self.rl * x) - ((self.w1 * x ** 2) / 2) + (self.w1 * self.a * x) + self.c2
            else:
                m = (-1 * self.rr * x) + self.c3
        return m

    def eisx(self,x):
        x = float(x)
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                eis = ((self.rl * x ** 2) / 2.0) + (self.c1 * x) + self.c4
            elif x <= self.b:
                eis = ((self.rl * x **2) / 2.0) - ((self.w1 * x ** 3) / 6.0) + ((self.w1 * self.a * x **2) / 2.0) + (self.c2 * x) + self.c5
            else:
                eis = ((-1.0 * self.rr * x ** 2) / 2.0) + (self.c3 * x) + self.c6
        return eis
    
    def eidx(self,x):
        x = float(x)
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif x > self.l:
            return 'Error x > l'
        else:                       
            if x <= self.a:
                eid = ((self.rl * x ** 3) / 6) + ((self.c1 * x ** 2) / 2) + (self.c4 * x) + self.c7
            elif x<=self.b:
                eid = ((self.rl * x ** 3) / 6) - ((self.w1 * x ** 4) / 24) + ((self.w1 * self.a * x ** 3) / 6) + ((self.c2 * x ** 2) / 2) + (self.c5 * x) + self.c8
            else:
                eid = ((-1 * self.rr * x ** 3) / 6) + ((self.c3 * x ** 2) / 2) + (self.c6 * x) + self.c9
        return eid

#def trapl( w1, w2, a, b, l, x):
#    d = a + b
#    s = (w2 - w1) / b
#    if w2 == -1*w1:
#        xbar = b/2
#    else:
#        xbar = (b * ((2 * w2) + w1)) / (3 * (w2 + w1))
#    W = b * ((w1 + w2) / 2)
#    rr = (W * (a + xbar)) / l
#    rl = W - rr
#    c1 = 0
#    c2 = c1 + ((a ** 3 * s) / 6) + ((a ** 2 * (w1 - (s * a))) / 2) + ((((s * a) - (2 * w1)) * a ** 2) / 2)
#    c3 = rr * l
#    c7 = 0
#    c8 = ((-1 * c1 * a ** 2) / 2) - ((a ** 5 * s) / 30) - ((a ** 4 * (w1 - (s * a))) / 8) - ((((s * a) - (2 * w1)) * a ** 4) / 6) + ((c2 * a ** 2) / 2) + c7
#    c9 = ((-1 * rl * d ** 3) / 3) + ((d ** 5 * s) / 30) + ((d ** 4 * (w1 - (s * a))) / 8) + ((((s * a) - (2 * w1)) * a * d ** 3) / 6) - ((c2 * d ** 2) / 2) + c8 - ((rr * d ** 3) / 3) + ((c3 * d ** 2) / 2)
#    c6 = (((rr * l ** 3) / 6) - ((c3 * l ** 2) / 2) - c9) / l
#    c5 = ((-1 * rr * d ** 2) / 2) + (c3 * d) + c6 - ((rl * d ** 2) / 2) + ((d ** 4 * s) / 24) + ((d ** 3 * (w1 - (s * a))) / 6) + ((((s * a) - (2 * w1)) * a * d ** 2) / 4) - (c2 * d)
#    c4 = ((-1 * a ** 4 * s) / 24) - ((a ** 3 * (w1 - (s * a))) / 6) - ((((s * a) - (2 * w1)) * a ** 3) / 4) + (c2 * a) + c5 - (c1 * a)
#    if x<=a:
#        v = rl
#        m = (rl * x) + c1
#        d = ((rl * x ** 3) / 6) + ((c1 * x ** 2) / 2) + (c4 * x) + c7
#    elif x<d:
#        v = rl - ((x ** 2 * s) / 2) - (x * (w1 - (s * a))) - ((((s * a) - (2 * w1)) * a) / 2)
#        m = (rl * x) - ((x ** 3 * s) / 6) - ((x ** 2 * (w1 - (s * a))) / 2) - ((((s * a) - (2 * w1)) * a * x) / 2) + c2
#        d = ((rl * x ** 3) / 6) - ((x ** 5 * s) / 120) - ((x ** 4 * (w1 - (s * a))) / 24) - ((((s * a) - (2 * w1)) * a * x ** 3) / 12) + ((c2 * x ** 2) / 2) + (c5 * x) + c8
#    else:
#        v = -1 * rr
#        m = (-1 * rr * x) + c3
#        d = ((-1 * rr * x ** 3) / 6) + ((c3 * x ** 2) / 2) + (c6 * x) + c9
#    return (rl, rr, v, m, d)

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
    
    
    def v(self,x):
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            return 'Error w1 and w2 change direction'
            return 'Error w1 and w2 change direction'
        else:
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
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            return 'Error w1 and w2 change direction'
            return 'Error w1 and w2 change direction'
        else:
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
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            return 'Error w1 and w2 change direction'
            return 'Error w1 and w2 change direction'
        else:
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
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            return 'Error w1 and w2 change direction'
            return 'Error w1 and w2 change direction'
        else:
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
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            return 'Error w1 and w2 change direction'
            return 'Error w1 and w2 change direction'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                v = self.rl
            elif x<=self.b:
                v = self.rl - ((x ** 2 * self.s) / 2) - (x * (self.w1 - (self.s * self.a))) - ((((self.s * self.a) - (2 * self.w1)) * self.a) / 2)
            else:
                v = -1 * self.rr
        return v
    
    def mx(self,x):
        x = float(x)
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            return 'Error w1 and w2 change direction'
            return 'Error w1 and w2 change direction'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                m = (self.rl * x) + self.c1
            elif x <= self.b:
                m = (self.rl * x) - ((x ** 3 * self.s) / 6) - ((x ** 2 * (self.w1 - (self.s * self.a))) / 2) - ((((self.s * self.a) - (2 * self.w1)) * self.a * x) / 2) + self.c2
            else:
                m = (-1 * self.rr * x) + self.c3
        return m

    def eisx(self,x):
        x = float(x)
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            return 'Error w1 and w2 change direction'
            return 'Error w1 and w2 change direction'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                eis = ((self.rl * x ** 2) / 2) + (self.c1 * x) + self.c4
            elif x <= self.b:
                eis = ((self.rl * x ** 2) / 2) - ((x ** 4 * self.s) / 24) - ((x ** 3 * (self.w1 - (self.s * self.a))) / 6) - ((((self.s * self.a) - (2 * self.w1)) * self.a * x ** 2) / 4) + (self.c2 * x) + self.c5
            else:
                eis = ((-1 * self.rr * x ** 2) / 2) + (self.c3 * x) + self.c6
        return eis
    
    def eidx(self,x):
        x = float(x)
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            return 'Error w1 and w2 change direction'
            return 'Error w1 and w2 change direction'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                eid = ((self.rl * x ** 3) / 6) + ((self.c1 * x ** 2) / 2) + (self.c4 * x) + self.c7
            elif x<=self.b:
                eid = ((self.rl * x ** 3) / 6) - ((x ** 5 * self.s) / 120) - ((x ** 4 * (self.w1 - (self.s * self.a))) / 24) - ((((self.s * self.a) - (2 * self.w1)) * self.a * x ** 3) / 12) + ((self.c2 * x ** 2) / 2) + (self.c5 * x) + self.c8
            else:
                eid = ((-1 * self.rr * x ** 3) / 6) + ((self.c3 * x ** 2) / 2) + (self.c6 * x) + self.c9 
        return eid

#def cant_right_point(p,a,l,x):
#    
#    rl = p
#    ml = -1*p*a
#    
#    if x<=a:
#        v = p
#        m = rl*x + ml
#    
#    if x>a:
#        v = 0
#        m = 0
#    
#    return(rl,ml,v,m)

class cant_right_point:
    def __init__(self, p, a, l):
        
        self.p = float(p)
        self.a = float(a)
        self.l = float(l)
        self.b = self.l - self.a
        
        if self.a > self.l:
            self.rl = 'Error a > l'
            self.ml = 'Error a > l'
            
        else:
            self.rl = self.p
            self.ml = -1*self.p*self.a
    
    def v(self,x):
        if self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        else:
            iters = len(x)
            v=zeros(iters)
            
            for i in range(0,iters):
                if x[i]<=self.a:
                    v[i] = self.p
                else:
                    v[i] = 0
        return v
    
    def m(self,x):
        if self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        else:
            iters = len(x)
            m=zeros(iters)
            
            for i in range(0,iters):
                if x[i]<=self.a:
                    m[i] = self.rl*x[i] + self.ml
                else:
                    m[i] = 0
        return m

    def vx(self,x):
        if self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        else:            
            if x<=self.a:
                v = self.p
            else:
                v = 0
        return v
    
    def mx(self,x):
        if self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        else:
            if x<=self.a:
                m = self.rl*x + self.ml
            else:
                m = 0
        return m
               

#def cant_right_udl(w,a,b,l,x):
#    c = a+b
#    w_tot = w*c
#    
#    rl = w_tot
#    ml = -1*w_tot*(b-(c/2))
#    
#    if x<=a:
#        v = w_tot
#        m = rl*x + ml
#    
#    elif a<x<=b:
#        v = w_tot - w*(x-a)
#        m = rl*x + ml - (w*(x-a)*((x-a)/2))
#    
#    else:
#        v = 0
#        m = 0
#    
#    return(rl,ml,v,m)

class cant_right_udl:
    def __init__(self, w1, a, b, l):
        
        self.w1 = float(w1)
        self.a = float(a)
        self.l = float(l)
        self.b = float(b)
        self.c = self.a+self.b
        self.w_tot = self.w1*self.c
        
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
            self.ml = -1*self.w_tot*(self.b-(self.c/2))
            
    
    
    def v(self,x):
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        else:
            iters = len(x)
            v=zeros(iters)
            
            for i in range(0,iters):
                if x[i] <= self.a:
                    v[i] = self.w_tot
                elif x[i]<=self.b:
                    v[i] = self.w_tot - self.w1*(x[i]-self.a)
                else:
                    v[i] = 0
            return v
    
    def m(self,x):
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        else:
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

    
    def vx(self,x):
        x = float(x)
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                v = self.w_tot 
            elif x<=self.b:
                v = self.w_tot - self.w1*(x-self.a)
            else:
                v = 0
        return v
    
    def mx(self,x):
        x = float(x)
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                m = self.rl*x + self.ml
            elif x <= self.b:
                m = self.rl*x + self.ml - (self.w1*(x-self.a)*((x-self.a)/2)) 
            else:
                m = 0
        return m
  

#def cant_left_point(p,a,l,x):
#    
#    rr = p
#    mr = -1*p*(l-a)
#    
#    if x<=a:
#        v = 0
#        m = 0
#    
#    if x>a:
#        v = -1*rr
#        m = -1*rr*(x-a)
#    
#    return(rr,mr,v,m)

class cant_left_point:
    def __init__(self, p, a, l):
        
        self.p = float(p)
        self.a = float(a)
        self.l = float(l)
        
        
        if self.a > self.l:
            self.rr = 'Error a > l'
            self.mr = 'Error a > l'
            
        else:
            self.rr = self.p
            self.mr = -1*self.p*(self.l-self.a)
    
    def v(self,x):
        if self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        else:
            iters = len(x)
            v=zeros(iters)
            
            for i in range(0,iters):
                if x[i]<=self.a:
                    v[i] = 0
                else:
                    v[i] = -1*self.rr
        return v
    
    def m(self,x):
        if self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        else:
            iters = len(x)            
            m=zeros(iters)
            
            for i in range(0,iters):
                if x[i]<=self.a:
                    m[i] = 0
                else:
                    m[i] = -1*self.rr*(x[i]-self.a)
        return m

    def vx(self,x):
        if self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'            
        else:            
            if x<=self.a:
                v = 0
            else:
                v = -1*self.rr
        return v
    
    def mx(self,x):
        if self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'            
        else:
            if x<=self.a:
                m = 0
            else:
                m = -1*self.rr*(x-self.a)
        return m
                   

#def cant_left_udl(w,a,b,l,x):
#    c = a+b
#    w_tot = w*c
#    
#    rr = w_tot
#    mr = -1*w_tot*(l-b+(c/2))
#    
#    if x<=a:
#        v = 0
#        m = 0
#    
#    elif a<x<=b:
#        v = - w*(x-a)
#        m = -1*(w*(x-a)*((x-a)/2))
#    
#    else:
#        v = w_tot
#        m = -1*w_tot(x-b+(c/2))
#    
#    return(rr,mr,v,m)

class cant_left_udl:
    def __init__(self, w1, a, b, l):
        
        self.w1 = float(w1)
        self.a = float(a)
        self.l = float(l)
        self.b = float(b)
        self.c = self.a+self.b
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
            self.mr = -1*self.w_tot*(self.l-self.b+(self.c/2))
            
    
    
    def v(self,x):
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        else:
            iters = len(x)            
            v=zeros(iters)
            
            for i in range(0,iters):
                if x[i] <= self.a:
                    v[i] = 0
                elif x[i]<=self.b:
                    v[i] = -1*self.w1*(x[i]-self.a)
                else:
                    v[i] = self.w_tot
            return v
    
    def m(self,x):
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        else:
            iters = len(x)            
            m=zeros(iters)
            
            for i in range(0,iters):
                if x[i] <= self.a:
                    m[i] = 0
                elif x[i] <= self.b:
                    m[i] = -1*(self.w1*(x[i]-self.a)*((x[i]-self.a)/2))
                else:
                    m[i] = -1*self.w_tot(x[i]-self.b+(self.c/2))
            return m

    
    def vx(self,x):
        x = float(x)
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                v = 0 
            elif x<=self.b:
                v =  -1*self.w1*(x-self.a)
            else:
                v = self.w_tot
        return v
    
    def mx(self,x):
        x = float(x)
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                m = 0
            elif x <= self.b:
                m =  -1*(self.w1*(x-self.a)*((x-self.a)/2))
            else:
                m =  -1*self.w_tot(x-self.b+(self.c/2))
        return m

#def cant_right_trap(w1, w2, a, b, l, x):
#    c = a+b    
#    w = 0.5*(w1+w2)*b
#    d = a+(((w1+(2*w2))/(3*(w2+w1)))*b)
#    s = (w1-w2)/b
#    rl = w
#    ml = -1*w*d       
#    
#    if x<=a:
#        v=w
#        m=(w*x)+ml
#    elif a<x<c:
#        cx = x-a        
#        wx = w1-(s*cx)
#        dx = x - (a+(((w1+(2*wx))/(3*(wx+w1)))*cx))
#        wwx = 0.5*(w1+wx)*cx       
#        v=w-wwx
#        m=(w*x+ml)-(wwx*dx)
#    else:
#        v=0
#        m=0
#    
#    return(rl,ml,v,m)

class cant_right_trap:
    def __init__(self, w1, w2, a, b, l):
        
        self.w1 = float(w1)
        self.w2 = float(w2)
        self.a = float(a)
        self.l = float(l)
        self.b = float(b)
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
            
    
    
    def v(self,x):
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            return 'Error w1 and w2 change direction'
            return 'Error w1 and w2 change direction'
        else:
            iters = len(x)            
            v=zeros(iters)
            
            for i in range(0,iters):
                if x[i] <= self.a:
                    v[i] = self.w
                elif x[i]<=self.b:
                    cx = x[i]-self.a        
                    wx = self.w1-(self.s*cx)
                    wwx = 0.5*(self.w1+wx)*cx                    
                    v[i] = self.w-wwx
                else:
                    v[i] =0
        return v
    
    def m(self,x):
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            return 'Error w1 and w2 change direction'
            return 'Error w1 and w2 change direction'
        else:           
            iters = len(x)            
            m=zeros(iters)
            
            for i in range(0,iters):
                if x[i] <= self.a:
                    m[i] = (self.w*x[i])+self.ml
                elif x[i] <= self.b:
                    cx = x[i]-self.a        
                    wx = self.w1-(self.s*cx)
                    dx = x[i] - (self.a+(((self.w1+(2*wx))/(3*(wx+self.w1)))*cx))
                    wwx = 0.5*(self.w1+wx)*cx                    
                    m[i] = (self.w*x[i]+self.ml)-(wwx*dx)
                else:
                    m[i] = 0
        return m
    
    def vx(self,x):
        x = float(x)
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            return 'Error w1 and w2 change direction'
            return 'Error w1 and w2 change direction'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                v = self.w
            elif x<=self.b:
                cx = x-self.a        
                wx = self.w1-(self.s*cx)
                wwx = 0.5*(self.w1+wx)*cx                    
                v = self.w-wwx
            else:
                v =0
        return v
    
    def mx(self,x):
        x = float(x)
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            return 'Error w1 and w2 change direction'
            return 'Error w1 and w2 change direction'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                m = (self.w*x)+self.ml
            elif x <= self.b:
                cx = x-self.a        
                wx = self.w1-(self.s*cx)
                dx = x - (self.a+(((self.w1+(2*wx))/(3*(wx+self.w1)))*cx))
                wwx = 0.5*(self.w1+wx)*cx                    
                m = (self.w*x+self.ml)-(wwx*dx)
            else:
                m = 0
        return m

   
#def cant_left_trap(w1, w2, a, b, l, x):
#    c = a+b    
#    w = 0.5*(w1+w2)*b
#    dl = a+(((w1+(2*w2))/(3*(w2+w1)))*b)
#    dr = l-dl
#    s = (w1-w2)/b
#    rr = w
#    mr = -1*w*dr        
#    
#    if x<=a:
#        v=0
#        m=0
#    elif a<x<c:
#        cx = x-a
#        wx = w1-(s*cx)
#        dlx = a+(((w1+(2*wx))/(3*(wx+w1)))*cx)
#        drx = x-dlx
#        wwx = 0.5*(w1+wx)*cx        
#        v=-1*wwx
#        m=-1*wwx*drx
#    else:
#        v=-1*w
#        m=-1*w*(x-dl)
#    
#    return(rr,mr,v,m)

class cant_left_trap:
    def __init__(self, w1, w2, a, b, l):
        
        self.w1 = float(w1)
        self.w2 = float(w2)
        self.a = float(a)
        self.l = float(l)
        self.b = float(b)
        self.c = b-a        
        
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
            self.w = 0.5*(self.w1+self.w2)*self.c
            self.dl = self.a+(((self.w1+(2*self.w2))/(3*(self.w2+self.w1)))*self.c)
            self.dr = self.l-self.dl
            self.s = (self.w1-self.w2)/self.c
            self.rr = self.w
            self.mr = -1*self.w*self.d    
    
    def v(self,x):
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            return 'Error w1 and w2 change direction'
            return 'Error w1 and w2 change direction'
        else:
            iters = len(x)            
            v=zeros(iters)
            
            for i in range(0,iters):
                if x[i] <= self.a:
                    v[i] = 0
                elif x[i]<=self.b:
                    cx = x[i]-self.a
                    wx = self.w1-(self.s*cx)
                    wwx = 0.5*(self.w1+wx)*cx                   
                    v[i] = -1*wwx
                else:
                    v[i] = -1*self.w
        return v
    
    def m(self,x):
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            return 'Error w1 and w2 change direction'
            return 'Error w1 and w2 change direction'
        else:           
            iters = len(x)            
            m=zeros(iters)
            
            for i in range(0,iters):
                if x[i] <= self.a:
                    m[i] = 0
                elif x[i] <= self.b:
                    cx = x[i]-self.a
                    wx = self.w1-(self.s*cx)
                    dlx = self.a+(((self.w1+(2*wx))/(3*(wx+self.w1)))*cx)
                    drx = x[i]-dlx
                    wwx = 0.5*(self.w1+wx)*cx                    
                    m[i] = -1*wwx*drx
                else:
                    m[i] = -1*self.w*(x[i]-self.dl)
        return m
    
    def vx(self,x):
        x = float(x)
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            return 'Error w1 and w2 change direction'
            return 'Error w1 and w2 change direction'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                v = 0
            elif x<=self.b:
                cx = x-self.a
                wx = self.w1-(self.s*cx)
                wwx = 0.5*(self.w1+wx)*cx                   
                v = -1*wwx
            else:
                v = -1*self.w
        return v
    
    def mx(self,x):
        x = float(x)
        if self.a > self.b:
            return 'Error a > b'
            return 'Error a > b'
        elif self.a > self.l:
            return 'Error a > l'
            return 'Error a > l'
        elif self.b > self.l:
            return 'Error b > l'
            return 'Error b > l'
        elif sign(self.w1) != sign(self.w2) and self.w1 !=0 and self.w2 !=0:
            return 'Error w1 and w2 change direction'
            return 'Error w1 and w2 change direction'
        elif x > self.l:
            return 'Error x > l'
        else:
            if x <= self.a:
                m = 0
            elif x <= self.b:
                cx = x-self.a
                wx = self.w1-(self.s*cx)
                dlx = self.a+(((self.w1+(2*wx))/(3*(wx+self.w1)))*cx)
                drx = x-dlx
                wwx = 0.5*(self.w1+wx)*cx                    
                m = -1*wwx*drx
            else:
                m = -1*self.w*(x-self.dl)
        return m

    