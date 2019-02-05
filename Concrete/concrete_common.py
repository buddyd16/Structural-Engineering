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
import math
import matplotlib.pyplot as plt

def stress_strain_desayi_krishnan(fprimec, ultimate_strain, k, strain):
    '''
    method for a parabolic stress-strain relationship for concrete in compression
    Desayi, P. and Krishnan, S., Equation for the Stress-Strain Curve of Concrete, ACI
    Journal, Proceedings V. 61, No. 3, Mar. 1964, pp. 345-350
    
    fprimec = f'c = 28-day compressive strength of concrete -- type: float
    ultimate_strain = eu = strain at failure -- type: float  ACI: 0.003 (English Units)
    k = k*f'c = stress at ultimate strain -- type: float  ACI: 0.85 (English Units)
    strain_report = e = strain at location where stress is desired -- type: float
    '''
    if strain <=0 or strain> ultimate_strain:
        return 0
    
    else:
        fo = fprimec
        
        # solve for eo = strain at fo
        # E = 2*fo / eo
        # eo has two possible solutions
        # eo = eu - sqrt(-1*(k^2 - 1) * eu^2) / k or sqrt(-1*(k^2 - 1) * eu^2) + eu / k
        
        eo1 = (ultimate_strain - math.sqrt(-1*(math.pow(k,2) - 1)*math.pow(ultimate_strain,2))) / k
        eo2 = (math.sqrt(-1*(math.pow(k,2) - 1)*math.pow(ultimate_strain,2))+ultimate_strain) / k
        
        eo = min(eo1,eo2)
        
        E = 2*fo / eo
        
        f = (E*strain) / (1+math.pow(strain/eo,2))
        
        return f

def stress_strain_collins_et_all(fprimec, ultimate_strain, strain):
    '''
    method for a parabolic stress-strain relationship for concrete in compression
    Collins, M.P., Mitchell D. and MacGregor, J.G., Structural Consideration for High-Strength
    Concrete, Concrete International, V. 15, No. 5, May 1993, pp. 27-34. 
    '''
    if strain <=0 or strain> ultimate_strain:
        return 0
    
    else:
        k = 0.67 + (fprimec / 9000.0) # for PSI units
        n = 0.8 + (fprimec / 2500.0) # for PSI units
        Ec = (40000*math.sqrt(fprimec)) + 1000000 # for PSI units
        
        ecprime = (fprimec / Ec)*(n/(n-1))
        
        e = strain/ecprime
        
        if e <= 1:
            f = ((e) * (n / (n-1+math.pow(e,n)))) * fprimec
        else:
            f = ((e) * (n / (n-1+math.pow(e,n*k)))) * fprimec
        
        return f

def stress_strain_whitney(fprimec, ultimate_strain, strain):
    '''
    method for the Whitney Stress block used in ACI 318
    '''
  
    if fprimec <= 4000:
        beta1 = 0.85
    elif fprimec <= 8000:
        beta1 = 0.85 - ((0.05*(fprimec-4000))/1000)
    else:
        beta1 = 0.65
     
    if strain <= (ultimate_strain - (ultimate_strain*beta1)) or strain > ultimate_strain:
        return [0, beta1]
        
    else:
        return [0.85*fprimec, beta1]

def stress_strain_steel(fy, yield_strain, strain):
    '''
    Linear stress strain definition that will return
    a linear value between 0 and +/- the yield strain
    or Fy is the strain is above or below the yield strain
    '''
    
    if abs(strain) >= yield_strain:
        return (strain/abs(strain)) * fy
    
    else:
        return (strain*fy)/yield_strain
    

def strain_at_depth_from_top(eu,na_depth,depth):
    
    return (eu/na_depth)*depth
    
x = [-0.004+(i*0.00005) for i in range(0,161)]
y = [stress_strain_steel(60,0.002,i) for i in x]

y2 = [stress_strain_collins_et_all(4500,0.003,i) for i in x]
y3 = [stress_strain_desayi_krishnan(4500,0.003,0.85,i) for i in x]
y4 = [stress_strain_whitney(4500,0.003,i)[0] for i in x]

f, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
ax1.plot(x, y, 'r-')
ax1.plot(x, [0]*len(x),'k-')
ax1.set_title('Steel Stress-Strain')
ax1.set_ylim([-70,70])
ax1.set_xlim([-0.005,0.005])
ax2.plot(x, y2, 'b-')
ax2.plot(x, [0]*len(x),'k-')
ax2.set_title('Concrete Stress-Strain (Collins)')
ax2.set_ylim([-1000,5000])
ax2.set_xlim([-0.005,0.005])
ax3.plot(x, y3, 'b-')
ax3.plot(x, [0]*len(x),'k-')
ax3.set_title('Concrete Stress-Strain (Desayi & Krishnan)')
ax3.set_ylim([-1000,5000])
ax3.set_xlim([-0.005,0.005])
ax4.plot(x, y4, 'b-')
ax4.plot(x, [0]*len(x),'k-')
ax4.set_title('Concrete Stress-Strain (Whitney ACI318)')
ax4.set_ylim([-1000,5000])
ax4.set_xlim([-0.005,0.005])
   

plt.tight_layout()

plt.show()
