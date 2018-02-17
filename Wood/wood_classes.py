# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 09:37:43 2018

@author: DonB
"""
from __future__ import division
import matplotlib.pyplot as plt

class wood_stud_wall:
    def __init__(self,b_in=1.5,d_in=3.5,height_ft=10, spacing_in=12, grade="No.2", fb_psi=875, fc_psi=1150, E_psi=1400000, Emin_psi=510000, fc_perp_pl_psi=565, moisture_percent = 19, temp = 90, incised = 0,  num_plates = 0):
        self.b_in = b_in
        self.d_in = d_in
        
        #Compute wall height either inlcusive or exclusive of wall plates
        self.height_in = height_ft * 12.0
        if num_plates == 0:
            self.height_in = self.height_in
            self.assumptions = '--ASSUMPTIONS--\n Wall Height inclusive of top and bottom plates\n'
        else:
            self.height_in = self.height_in - (num_plates * 1.5)
            self.assumptions = '--ASSUMPTIONS--\n Wall Height - ({1}) 1.5" wall plates\n'.format(num_plates)
            
        self.spacing_in = spacing_in
        self.fb_psi = fb_psi
        self.fc_psi = fc_psi
        self.Emin_psi = Emin_psi
        self.E_psi = E_psi
        self.fc_perp_pl_psi = fc_perp_pl_psi
        self.defl_180 = self.height_in/180.0
        self.defl_240 = self.height_in/240.0
        self.defl_360 = self.height_in/360.0
        

        #initialize warning log
        self.warning = ''
        
        #Stud Section Properties
        self.I_in4 = (self.b_in * self.d_in**3)/12.0
        self.area_in2 = self.b_in * self.d_in
        self.s_in3 = (self.b_in * self.d_in**2)/6.0
        
        #Repetitive Member Factor, CR
        #NDS 2005 section 4.3.9
        if self.spacing_in > 24:
            self.cr = 1.0
        else:
            self.cr = 1.15
    
        #Size Factor, Cf
        #NDS 2005 section 4.3.6 and Table 4A
        #NOTE ASSUMES STUDS ARE VISUALLY GRADED DIMENSION LUMBER 2"-4" AND NOT SOUTHERN PINE AND NORTH AMERICAN SPECIES
        self.assumptions = self.assumptions + 'Size Factor,Cf - Wall Studs are visually graded dimensional lumber 2" to 4" North American Species and not Southern Pine\n'
        if grade == "Stud":
            if self.d_in > 5.5:
                pass
            elif self.d_in > 3.5:
                self.cf_fb = 1.0
                self.cf_fc = 1.0
            else:
                self.cf_fc = 1.05
                self.cf_fb = 1.1
        elif grade == "Construction":
            self.cf_fb = 1.0
            self.cf_fc = 1.0
        elif grade == "Utility":
            if self.d_in > 2.5:
                self.cf_fb = 1.0
                self.cf_fc = 1.0
            else:
                self.cf_fc = 0.6
                if self.b_in>2.5:
                    self.cf_fb = 1.0
                else:
                    self.cf_fb = 0.4
        else:
            if self.d_in>11.25:
                self.cf_fc = 0.9
                if self.b_in>2.5:
                    self.cf_fb = 1.0
                else:
                    self.cf_fb = 0.9
            elif self.d_in>9.25:
                self.cf_fc = 1.0
                if self.b_in>2.5:
                    self.cf_fb = 1.1
                else:
                    self.cf_fb = 1.0
            elif self.d_in>7.25:
                self.cf_fc = 1.0
                if self.b_in>2.5:
                    self.cf_fb = 1.2
                else:
                    self.cf_fb = 1.1
            elif self.d_in>5.5:
                self.cf_fc = 1.05
                if self.b_in>2.5:
                    self.cf_fb = 1.3
                else:
                    self.cf_fb = 1.2
            elif self.d_in>4.5:
                self.cf_fc = 1.1
                self.cf_fb = 1.3
            elif self.d_in>3.5:
                self.cf_fc = 1.1
                self.cf_fb = 1.4
            else:
                self.cf_fc = 1.15
                self.cf_fb = 1.5
                
        #Wet Service Factor, Cm
        #NDS 2005 section 4.3.3 and Table 4A
        #NOTE ASSUMES STUDS ARE VISUALLY GRADED DIMENSION LUMBER 2"-4" AND NOT SOUTHERN PINE AND NORTH AMERICAN SPECIES
        self.assumptions = self.assumptions + 'Wet Service Factor,Cm - Wall Studs are visually graded dimensional lumber 2" to 4" North American Species and not Southern Pine\n'
        if moisture_percent > 19:
            self.cm_fc_perp = 0.67
            self.cm_E = 0.9
            if self.fb_psi*self.cf_fb <= 1150:
                self.cm_fb = 1.0
            else:
                self.cm_fb = 0.85
            
            if self.fc_psi*self.cf_fc <= 750:
                self.cm_fc = 1.0
            else:
                self.cm_fc = 0.8
        else:
            self.cm_fb = 1.0
            self.cm_fc = 1.0
            self.cm_fc_perp = 1.0
            self.cm_E = 1.0

        #Temperature Factor, Ct
        #NDS 2005 section 4.3.4
        if temp > 150:
            self.warning = self.warning + "Ct not valid see NDS 2005 Appendix C\n"
            self.ct_E = 0.01
            self.ct_fb = 0.01
            self.ct_fc = 0.01
            self.ct_fc_perp = 0.01
        elif temp <= 100:
            self.ct_E = 1.0
            self.ct_fb = 1.0
            self.ct_fc = 1.0
            self.ct_fc_perp = 1.0
        elif temp <= 125:
            self.ct_E = 0.9
            if moisture_percent > 19:           
                self.ct_fb = 0.7
                self.ct_fc = 0.7
                self.ct_fc_perp = 0.7
            else:
                self.ct_fb = 0.8
                self.ct_fc = 0.8
                self.ct_fc_perp = 0.8
        else:
            self.ct_E = 0.9
            if moisture_percent > 19:           
                self.ct_fb = 0.5
                self.ct_fc = 0.5
                self.ct_fc_perp = 0.5
            else:
                self.ct_fb = 0.7
                self.ct_fc = 0.7
                self.ct_fc_perp = 0.7
                
        #Beam Stability Factor, CL
        #NDS 2005 section 4.3.5
        self.cl = 1.0 #Assumes stud walls are sheathed on the compression face
        self.assumptions = self.assumptions + 'Beam Stability Factor, CL - Wall studs are continuously sheathed on the compression face\n'
        
        #Flat Use Factor, Cfu
        #NDS 2005 section 4.3.7
        self.cfu = 1.0 #Wall studs generally not loaded on flat face
        self.assumptions = self.assumptions + 'Flat Use Factor, Cfu - Wall studs are not loaded on the flat face\n'
        
        #Incising Factor, Ci
        #NDS 2005 section 4.3.8
        if incised == 1:
            self.ci_E = 0.95
            self.ci_fb = 0.8
            self.ci_fc = 0.8
            self.ci_fc_perp = 1.0
        else:
            self.ci_E = 1.0
            self.ci_fb = 1.0
            self.ci_fc = 1.0
            self.ci_fc_perp = 1.0
        
        #Buckling Siffness Factor, CT
        #NDS 2005 4.3.11
        self.cT = 1.0 #Not a truss
        self.assumptions = self.assumptions + 'Buckling Siffness Factor, CT - Not Applicable for stud walls\n'
        
        #Bearing Area Factor, Cb
        #NDS 2005 4.3.12 and 3.10.4
        if self.b_in < 6 : 
            self.cb_fc_perp = (self.b_in + 0.375) / self.b_in
            self.assumptions = self.assumptions + 'Bearing Area Factor, Cb - Stud greater than 3" from bottom plate end\n'
        else:
            self.cb_fc_perp = 1.0
        
        #Emin' = Emin * Cm * Ct * Ci * CT - NDS 2005 Table 4.3.1
        self.Emin_prime_psi = self.Emin_psi * self.cm_E * self.ct_E * self.ci_E * self.cT
        
        #E' = E * Cm * Ct * Ci - NDS 2005 Table 4.3.1
        self.E_prime_psi = self.E_psi * self.cm_E * self.ct_E * self.ci_E
        
        #Pressure to reach deflection limits
        self.defl_180_w_psf = ((self.defl_180 * 384 * self.E_prime_psi * self.I_in4) / (1728 * 5 * (self.height_in/12.0)**4))/(self.spacing_in/12.0)
        self.defl_240_w_psf= ((self.defl_240 * 384 * self.E_prime_psi * self.I_in4) / (1728 * 5 * (self.height_in/12.0)**4))/(self.spacing_in/12.0)
        self.defl_360_w_psf = ((self.defl_360 * 384 * self.E_prime_psi * self.I_in4) / (1728 * 5 * (self.height_in/12.0)**4))/(self.spacing_in/12.0)
        
        #Fc,perp' = Fc,perp * Cm * Ct * Ci * Cb- NDS 2005 Table 4.3.1
        self.fc_perp_pl_prime_psi = self.fc_perp_pl_psi * self.cm_fc_perp * self.ct_fc_perp * self.ci_fc_perp * self.cb_fc_perp
        
        self.crushing_limit_lbs = self.area_in2 * self.fc_perp_pl_prime_psi
        self.crushing_limit_lbs_no_cb = self.area_in2 * (self.fc_perp_pl_prime_psi/self.cb_fc_perp)
        
    def fc_prime_calc(self, cd):
        #Fc* = reference compression design value parallel to grain multiplied by all applicable adjusment factors except Cp
        self.fc_star_psi = self.fc_psi * cd * self.cm_fc * self.ct_fc * self.cf_fc * self.ci_fc
        
        self.c_cp = 0.8
        self.assumptions = self.assumptions + 'c for Cp calc based on sawn lumber - NDS 2005 3.7.1\n'
        
        #Slenderness Ration check per NDS 2005 sections 3.7.1.2 thru 3.7.1.4
        kb = 1.0
        kd = 1.0
        self.assumptions = self.assumptions + 'Ke = 1.0 for both depth and breadth of studs, Ref NDS 2005 appendix G pin top and bottom\n'
        leb = 12 * kb
        self.assumptions = self.assumptions + 'Le,b = 12.0, continously braced by sheathing 12" field nailing assumed\n'
        led = self.height_in * kd
        
        #Check Le/d,b ratios less than 50 - NDS 2005 Section 3.7.1.4
        if leb / self.b_in > 50 or led/self.d_in > 50:
            ratio_status = 0
        else:
            ratio_status = 1.0
        
        if ratio_status == 1.0:
            #FcE = 0.822 * Emin' / (Le/d)^2 - NDS 2005 Section 3.7.1
            self.fcE_psi = (0.822 * self.Emin_prime_psi)/(max(leb/self.b_in,led/self.d_in))**2
            
            #Cp = ([1 + (FcE / Fc*)] / 2c ) - sqrt[ [1 + (FcE / Fc*) / 2c]^2 - (FcE / Fc*) / c] - NDS 2005 Section 3.7.1
            self.cp = ((1+(self.fcE_psi/self.fc_star_psi))/(2*self.c_cp))-((((1+(self.fcE_psi/self.fc_star_psi))/(2*self.c_cp))**2)-((self.fcE_psi/self.fc_star_psi)/self.c_cp))**0.5
            
            self.fc_prime_psi = self.fc_star_psi * self.cp
            self.assumptions = self.assumptions + 'Wall studs are not tapered and not subject to NDS 2005 - 3.7.2\n'
        else:
            self.fc_prime_psi = 0
            self.warning=self.warning + 'Slenderness ratio greater than 50, suggest increase stud size or reducing wall height'
    
        return self.fc_prime_psi
    
    def fb_prime_calc(self, cd):
        self.fb_prime_psi = self.fb_psi * cd * self.cm_fb * self.ct_fb * self.cl * self.cf_fb * self.cfu * self.ci_fb * self.cr
        
        return self.fb_prime_psi
    
    def axial_and_bending(self, cd, p_lbs, m_inlbs):
        fc_psi = p_lbs / self.area_in2
        fb_psi = m_inlbs/self.s_in3
        
        fc_prime = self.fc_prime_calc(cd)       
        fb_prime = self.fb_prime_calc(cd)
        
        #Check that fc is less than FcE per NDS 2005 - Section 3.9.2
        if fc_psi < self.fcE_psi:
            #Combine ration per NDS 2005 equation (3.9-3)
            #[fc/Fc]'^2 + fb / Fb' [ 1- (fc / FcE)] <= 1.0
            ratio = (fc_psi/fc_prime)**2 + (fb_psi / (fb_prime*(1-(fc_psi/self.fcE_psi))))
            if ratio > 1.0:
                self.warning=self.warning + 'Combined Axial and Bending ratio > 1.0'
                return 'NG'
            else:
                return 'OK'
        else:
            self.warning=self.warning + 'fc is greater than FcE'
            return 'NG'
        
    def axial_capacity_w_moment(self,cd,m_inlbs):
        #solve for the allowable axial load using the bisection method
        a=0
        b=self.area_in2 * self.fc_prime_calc(cd) #upper bound limit on axial strength
        c=0
        
        loop_max = 500
        tol = 0.00001
        loop = 0
        p_lbs = 0
        while loop<loop_max:
            c = (a+b)/2.0
            
            fc_psi = c / self.area_in2
            fb_psi = m_inlbs/self.s_in3
          
            fc_prime = self.fc_prime_calc(cd)       
            fb_prime = self.fb_prime_calc(cd)
            
            #Check that fc is less than FcE per NDS 2005 - Section 3.9.2
            if fc_psi < self.fcE_psi:
                #Combine ration per NDS 2005 equation (3.9-3)
                #[fc/Fc]'^2 + fb / Fb' [ 1- (fc / FcE)] <= 1.0
                ratio = (fc_psi/fc_prime)**2 + (fb_psi / (fb_prime*(1-(fc_psi/self.fcE_psi))))
            else:
                ratio = 2.0
            
            if ratio > 1.0:
                b = c
            else:
                a = c
            
            if (b-a)/2.0 <= tol:
                loop = loop_max
                p_lbs = c
            else:
                loop+=1
        
        return p_lbs
    
    def wall_interaction_diagram_cd(self, cd):
        
        # Find bending limit pressure for each Cd ie where fb = Fb'
        # fb = M/s , M in in-lbs and s in in^3
        # M = w * stud height^2 / 8
        # w = Fb' * s * 8 / stud height^2 * (12 in / 1 ft)
        
        self.w_plf_limit = ((self.fb_prime_calc(cd) * self.s_in3 * 8.0) / (self.height_in**2)) * 12.0
        self.w_psf_limit = self.w_plf_limit/(self.spacing_in/12.0)

        # Determine pure axial compression capacity ie where fc = Fc' - withou consideration for plate crushing
        # fc = P/a
        # P = a * Fc'
        
        self.p_lbs_limit = self.area_in2 * self.fc_prime_calc(cd)
        
        points = 50
        step = self.w_psf_limit/points
        
        w=0
        x=[0] #pressure on x-axis
        y=[self.p_lbs_limit] #axial force on y-axis
        d=[0] #deflection at pressure x
        
        for i in range(1,points):
            w = step*i
            x.append(w)
            w_plf = w * (self.spacing_in/12)
            moment_inlbs = (((w_plf) * (self.height_in/12)**2) / 8.0)*12
            deflection = (5 * (w_plf) * (self.height_in/12)**4)/(384*self.E_prime_psi*self.I_in4)*1728
            d.append(deflection)
            
            p_lbs = self.axial_capacity_w_moment(cd,moment_inlbs)
            y.append(p_lbs)
        
        x.append(self.w_psf_limit)
        y.append(0)
        d.append((5 * (self.w_plf_limit) * (self.height_in/12)**4)/(384*self.E_prime_psi*self.I_in4)*1728)
        return x,y,d
            
       
#Cd - NDS 2005 Table 2.3.2
cd = [0.9,1.0,1.15,1.25,1.6,2.0]        

wall = wood_stud_wall(1.5,5.5,18,16,"No.2",875,1150,1400000,510000,200,19,90,0,0)
fc_prime = wall.fc_prime_calc(1.0)
cp = wall.cp

print '---Warnings--\n'
print wall.warning
print wall.assumptions

fig, ax1 = plt.subplots()
ax1.minorticks_on()
ax1.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
ax1.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
ax2 = ax1.twinx()
for x in cd: 
    w,p,d = wall.wall_interaction_diagram_cd(x)
    ax1.plot(w,p)

ax1.plot([0,max(w)],[wall.crushing_limit_lbs,wall.crushing_limit_lbs])
ax1.plot([0,max(w)],[wall.crushing_limit_lbs_no_cb,wall.crushing_limit_lbs_no_cb])
ax2.plot(w,d)
ax2.plot([wall.defl_180_w_psf,wall.defl_180_w_psf],[0,max(d)])
ax2.plot([wall.defl_240_w_psf,wall.defl_240_w_psf],[0,max(d)])
ax2.plot([wall.defl_360_w_psf,wall.defl_360_w_psf],[0,max(d)])
ax1.set_ylabel('Axial (lbs)')
ax1.set_xlabel('Pressure (psf)')
ax2.set_ylabel('Deflection (in)')

plt.title('2x6 SPF No.2 - 18 ft tall - 16" spacing')
fig.tight_layout()
plt.show()


