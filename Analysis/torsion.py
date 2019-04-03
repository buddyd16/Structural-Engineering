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
import math as m

#Torsion Equitions from AISC Design Guide 9 Appendix C

#Case 1 - Concentrated End Torques with Free Ends
#T = Applied Concentrated Torsional Moment, Kip-in
#G = Shear Modulus of Elasticity, Ksi, 11200 for steel
#J = Torsinal Constant of Cross Section, in^4
class torsion_case1:
    def __init__(self, T_k_in, G_ksi, J_in4):
        self.T_k_in = T_k_in
        self.G_ksi = G_ksi 
        self.J_in4 = J_in4
        
    def theta(self,z_in):
        T = self.T_k_in
        G = self.G_ksi
        J = self.J_in4
        z = z_in

        thet = (T*z) / (G*J)

        return thet
        
    def thetap(self,z_in):

        theta_prime = T / (G*J)

        return theta_prime
       
    def thetapp(self,z_in):

        theta_doubleprime = 0

        return theta_doubleprime
       
#Case 2 - Concentrated End Torques with Fixed Ends
#T = Applied Concentrated Torsional Moment, Kip-in
#G = Shear Modulus of Elasticity, Ksi, 11200 for steel
#J = Torsinal Constant of Cross Section, in^4
#l = Span Lenght, in
#a = Torsional Constant
class torsion_case2:
    def __init__(self, T_k_in, G_ksi, J_in4, l_in, a):
        self.T_k_in = T_k_in
        self.G_ksi = G_ksi 
        self.J_in4 = J_in4
        self.l_in = l_in
        self.a = a
        
    def theta(self,z_in):
        T = self.T_k_in
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        z = z_in
        
        thet = ((T*a) / (G*J))*((m.tanh(l/(2*a))*m.cosh(z/a))-(m.tanh(l/(2*a)))+(z/a)-(m.sinh(z/a)))
        
        return thet
        
    def thetap(self,z_in):
        T = self.T_k_in
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        z = z_in
        theta_prime = (T - T*m.cosh(z/a) + T*m.sinh(z/a)*m.tanh(l/(2*a)))/(G*J)

        return theta_prime
       
    def thetapp(self,z_in):
        T = self.T_k_in
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        z = z_in
        theta_doubleprime = (-(T*m.sinh(z/a)) + T*m.cosh(z/a)*m.tanh(l/(2*a)))/(a*G*J)

        return theta_doubleprime
       
    def thetappp(self,z_in):
        T = self.T_k_in
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        z = z_in
        theta_tripleprime = (-(T*m.cosh(z/a)) + T*m.sinh(z/a)*m.tanh(l/(2*a)))/(G*J*a**2)

        return theta_tripleprime  

#Case 3 - Concentrated Torque at alpha*l with Pinned Ends
#T = Applied Concentrated Torsional Moment, Kip-in
#G = Shear Modulus of Elasticity, Ksi, 11200 for steel
#J = Torsinal Constant of Cross Section, in^4
#l = Span Lenght, in
#a = Torsional Constant
#alpa = load application point/l
class torsion_case3:
    def __init__(self, T_k_in, G_ksi, J_in4, l_in, a, alpha):
        self.T_k_in = T_k_in
        self.G_ksi = G_ksi 
        self.J_in4 = J_in4
        self.l_in = l_in
        self.a = a
        self.alpha = alpha
        
    def theta(self,z_in):
        T = self.T_k_in
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        alpha = self.alpha
        z = z_in
        
        if 0 <= z_in <= (alpha*l):
            thet = ((T*l) / (G*J))*(((1.0-alpha)*(z/l))+(((a/l)*((m.sinh((alpha*l)/a)/m.tanh(l/a)) - m.cosh((alpha*l)/a)))*m.sinh(z/a)))
        else:
            thet = ((T*l) / (G*J))*(((l-z)*(alpha/l))+((a/l)*(((m.sinh((alpha*l)/a) / m.tanh(l/a))*m.sinh(z/a)) - (m.sinh((alpha*l)/a)*m.cosh(z/a)))))
            
        return thet

    def thetap(self,z_in):
        T = self.T_k_in
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        alpha = self.alpha
        z = z_in
        if 0 <= z_in <= (alpha*l):
            theta_prime = ((-1.0*T)/(G*J))*(alpha - 1.0 + (m.cosh(z/a)*((m.cosh((l*alpha)/a) - (m.sinh((l*alpha)/a)/m.tanh(l/a))))))
        else:
            theta_prime = -1.0*((T*(alpha - m.cosh(z/a)*m.sinh((l*alpha)/a)/m.tanh(l/a) + m.sinh(z/a)*m.sinh((l*alpha)/a))/(G*J)))
        return theta_prime
       
    def thetapp(self,z_in):
        T = self.T_k_in
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        alpha = self.alpha
        z = z_in
        if 0 <= z_in <= (alpha*l):
            theta_doubleprime = -((T*m.sinh(z/a)*(m.cosh((l*alpha)/a) - m.sinh((l*alpha)/a)/m.tanh(l/a)))/(a*G*J))
        else:
            theta_doubleprime = (T*(-1.0*m.cosh(z/a) + m.sinh(z/a)/m.tanh(l/a))*m.sinh((l*alpha)/a))/(a*G*J)
        return theta_doubleprime
       
    def thetappp(self,z_in):
        T = self.T_k_in
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        alpha = self.alpha
        z = z_in
        if 0 <= z_in <= (alpha*l):
            theta_tripleprime = -((T*m.cosh(z/a)*(m.cosh((l*alpha)/a) - m.sinh((l*alpha)/a)/m.tanh(l/a)))/(G*J*a**2))
        else:
            theta_tripleprime = (T*(m.cosh(z/a)/m.tanh(l/a) - m.sinh(z/a))*m.sinh((l*alpha)/a))/(G*J*a**2)
        return theta_tripleprime       

#Case 4 - Uniformly Distributed Torque with Pinned Ends
#t = Distributed torque, Kip-in / in
#G = Shear Modulus of Elasticity, Ksi, 11200 for steel
#J = Torsinal Constant of Cross Section, in^4
#l = Span Lenght, in
#a = Torsional Constant
class torsion_case4:
    def __init__(self, t_k_inpin, G_ksi, J_in4, l_in, a):
        self.t_k_inpin = t_k_inpin
        self.G_ksi = G_ksi 
        self.J_in4 = J_in4
        self.l_in = l_in
        self.a = a
        
    def theta(self,z_in):
        t = self.t_k_inpin
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        z = z_in
        
        thet = ((t*a**2) / (G*J))*(((l**2 / (2*a**2))*((z/l) - ((z**2)/(l**2))))+m.cosh(z/a)-(m.tanh(l/(2*a))*m.sinh(z/a))-1.0)
        
        return thet
        
    def thetap(self,z_in):
        t = self.t_k_inpin
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        z = z_in
        theta_prime = (t*(l - 2*z + 2*a*m.sinh(z/a) - 2*a*m.cosh(z/a)*m.tanh(l/(2*a))))/(2*G*J)

        return theta_prime
       
    def thetapp(self,z_in):
        t = self.t_k_inpin
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        z = z_in
        theta_doubleprime = (t*(-1 + m.cosh(z/a) - m.sinh(z/a)*m.tanh(l/(2*a))))/(G*J)

        return theta_doubleprime
       
    def thetappp(self,z_in):
        t = self.t_k_inpin
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        z = z_in
        theta_tripleprime = (t*(m.sinh(z/a) - m.cosh(z/a)*m.tanh(l/(2*a))))/(a*G*J)

        return theta_tripleprime

#Case 5 - Linearly Varying Torque with Pinned Ends - 0 at left to t at right
#t = Distributed torque, Kip-in / in
#G = Shear Modulus of Elasticity, Ksi, 11200 for steel
#J = Torsinal Constant of Cross Section, in^4
#l = Span Lenght, in
#a = Torsional Constant
class torsion_case5:
    def __init__(self, t_k_inpin, G_ksi, J_in4, l_in, a):
        self.t_k_inpin = t_k_inpin
        self.G_ksi = G_ksi 
        self.J_in4 = J_in4
        self.l_in = l_in
        self.a = a
        
    def theta(self,z_in):
        t = self.t_k_inpin
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        z = z_in

          
        
        thet = ((t*l**2) / (G*J))*((z/(6*l)) + ((a**2)/(l**2)*((m.sinh(z/a)/m.sinh(l/a))-(z/l)))-((z**3)/(6*l**3)))
        
        return thet
        
    def thetap(self,z_in):
        t = self.t_k_inpin
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        z = z_in
        theta_prime = (t*(-6.0*a**2 + l**2 - 3*z**2 + 6*a*l*(m.cosh(z/a)/m.sinh(l/a))))/(6*G*J*l)
        
        return theta_prime
       
    def thetapp(self,z_in):
        t = self.t_k_inpin
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        z = z_in
        theta_doubleprime = (t*(-1.0*z + l*(m.sinh(z/a)/m.sinh(l/a))))/(G*J*l)

        return theta_doubleprime
       
    def thetappp(self,z_in):
        t = self.t_k_inpin
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        z = z_in
        theta_tripleprime = (t*(-1 + (l*(m.cosh(z/a)/m.sinh(l/a)))/a))/(G*J*l)

        return theta_tripleprime

#Case 6 - Concentrated Torque at alpha*l with Fixed Ends
#T = Applied Concentrated Torsional Moment, Kip-in
#G = Shear Modulus of Elasticity, Ksi, 11200 for steel
#J = Torsinal Constant of Cross Section, in^4
#l = Span Lenght, in
#a = Torsional Constant
#alpa = load application point/l
class torsion_case6:
    def __init__(self, T_k_in, G_ksi, J_in4, l_in, a, alpha):
        self.T_k_in = T_k_in
        self.G_ksi = G_ksi 
        self.J_in4 = J_in4
        self.l_in = l_in
        self.a = a
        self.alpha = alpha
        self.H = (((1.0-m.cosh((alpha*l)/a)) / m.tanh(l/a)) + ((m.cosh((alpha*l)/a)-1.0) / m.sinh(l/a)) + m.sinh((alpha*l)/a) - ((alpha*l)/a)) / \
                    (((m.cosh(l/a)+(m.cosh((alpha*l)/a)*m.cosh(l/a))-m.cosh((alpha*l)/a)-1.0)/m.sinh(l/a))+((l/a)*(alpha-1.0))-m.sinh((alpha*l)/a))
        
    def theta(self,z_in):
        T = self.T_k_in
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        alpha = self.alpha
        H = self.H
        z = z_in
        
        if 0 <= z_in <= (alpha*l):
            thet = ((T*a) / ((H+1.0)*G*J))*\
                    ((((H*((1.0/m.sinh(l/a))+m.sinh((alpha*l)/a)-(m.cosh((alpha*l)/a)/m.tanh(l/a))))+ \
                    (m.sinh((alpha*l)/a) - (m.cosh((alpha*l)/a)/m.tanh(l/a)) + (1.0/m.tanh(l/a))))* \
                    (m.cosh(z/a)-1.0)) - \
                    m.sinh(z/a) + \
                    (z/a))
            
            
        else:
            thet = (T*a / ((1+(1/H))*G*J))*\
            ((m.cosh((alpha*l)/a) - 1.0/(H*m.sinh(l/a)) +\
            (m.cosh((alpha*l)/a)-m.cosh(l/a)+((l/a)*m.sinh(l/a))) / m.sinh(l/a)) +\
            m.cosh(z/a)*\
            ((1.0-m.cosh((alpha*l)/a))/(H*m.tanh(l/a)) +\
            (1.0-(m.cosh((alpha*l)/a)*m.cosh(l/a)))/m.sinh(l/a)) +\
            m.sinh(z/a)*\
            (((m.cosh((alpha*l)/a)-1.0)/H) + m.cosh((alpha*l)/a)) -\
            (z/a))
            
        return thet

    def thetap(self,z_in):
        T = self.T_k_in
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        alpha = self.alpha
        H = self.H
        z = z_in
        
        if 0 <= z_in <= (alpha*l):
            theta_prime = (-1.0*T*(-1.0 + m.cosh(z/a) + (-1.0 + (1.0 + H)*m.cosh((l*alpha)/a))*(m.sinh(z/a)/m.tanh(l/a)) - 1.0*H*(m.sinh(z/a)/m.sinh(l/a)) - 1.0*m.sinh(z/a)*m.sinh((l*alpha)/a) - 1.0*H*m.sinh(z/a)*m.sinh((l*alpha)/a)))/(G*(1.0 + H)*J)
        else:
            theta_prime = 0
        return theta_prime
       
    def thetapp(self,z_in):
        T = self.T_k_in
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        alpha = self.alpha
        H = self.H
        z = z_in
        
        if 0 <= z_in <= (alpha*l):
            theta_doubleprime = -((T*((m.cosh(z/a)*(-1.0 + (1.0 + H)*(m.cosh((l*alpha)/a))/m.tanh(l/a)))/a - (H*(m.cosh(z/a)/m.sinh(l/a)))/a + m.sinh(z/a)/a - (m.cosh(z/a)*m.sinh((l*alpha)/a))/a - (H*m.cosh(z/a)*m.sinh((l*alpha)/a))/a))/(G*(1.0 + H)*J))
        else:
            theta_doubleprime = 0
        return theta_doubleprime
       
    def thetappp(self,z_in):
        T = self.T_k_in
        G = self.G_ksi
        J = self.J_in4
        l = self.l_in
        a = self.a
        alpha = self.alpha
        H = self.H
        z = z_in
        
        if 0 <= z_in <= (alpha*l):
            theta_tripleprime = -((T*(m.cosh(z/a)/a**2 + ((-1.0 + (1.0 + H)*(m.cosh((l*alpha)/a))/m.tanh(l/a))*m.sinh(z/a))/a**2 - (H*(m.sinh(z/a)/m.sinh(l/a)))/a**2 - (m.sinh(z/a)*m.sinh((l*alpha)/a))/a**2 - (H*m.sinh(z/a)*m.sinh((l*alpha)/a))/a**2))/(G*(1.0 + H)*J))
        else:
            theta_tripleprime = 0
        return theta_tripleprime  
#Test Area

T = 90 #k-in
G = 11200 #ksi
J = 1.39 #in4
Cw = 2070 #in6
E = 29000 #ksi
a = ((E*Cw) / (G*J))**0.5 #Torsional Constant
l = 180 #in
alpha = 0.5

test = torsion_case6(T, G, J, l, a, alpha)
check = []

test_theta = test.theta(90)

check.append(test_theta*((G*J)/T)*(1/a))

test_thetap = test.thetap(90)

check.append(test_thetap*((G*J)/(T)))

test_thetapp = test.thetapp(90)

check.append(test_thetapp*((G*J)/T)*a)

test_thetappp = test.thetappp(90)

check.append(test_thetappp * ((G*J)/T)*a*a)


