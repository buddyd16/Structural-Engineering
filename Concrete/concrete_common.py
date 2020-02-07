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
import math
import matplotlib.pyplot as plt

def stress_strain_pca(fprimec, ultimate_strain, concrete_modulus, strain):
    '''
    PCA Stress-Strain Relationship
    formula presented in the PCA notes to ACI 318-05
    '''
    
    e = strain
    Ec = concrete_modulus
    eu = ultimate_strain
    fc = fprimec
    
    eo = (2*0.85*fc)/(Ec)
    
    if e <= 0:
        stress = 0
    
    elif 0<=e and e<=eo:
        stress = 0.85*fc*((2*(e/eo))-((e/eo)*(e/eo)))
    
    elif e<=eu:
        stress = 0.85*fc
    else:
        stress = 0
    
    return stress
    
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
    if strain <=0:
        return 0
    
    elif strain > ultimate_strain:
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

        return f*0.85

def stress_strain_collins_et_all(fprimec, ultimate_strain, strain):
    '''
    method for a parabolic stress-strain relationship for concrete in compression
    Collins, M.P., Mitchell D. and MacGregor, J.G., Structural Consideration for High-Strength
    Concrete, Concrete International, V. 15, No. 5, May 1993, pp. 27-34.
    '''
    if strain <=0:
        return 0
    elif strain > ultimate_strain:
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

        return f*0.85

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

    if strain <= (ultimate_strain - (ultimate_strain*beta1)):
        return [0, beta1]

    elif strain <= ultimate_strain:
        return [0.85*fprimec, beta1]
        
    else:
        return [0, beta1]
        
def stress_strain_steel(fy, yield_strain, Es, strain):
    '''
    Linear stress strain definition that will return
    a linear value between 0 and +/- the yield strain
    or Fy is the strain is above or below the yield strain
    '''
    if Es == 0:
        if abs(strain) >= yield_strain:
            return (strain/abs(strain)) * fy
    
        else:
            return (strain*fy)/yield_strain       
    else:
        if abs(strain)*Es >= fy:
            return (strain/abs(strain)) * fy
    
        else:
            return (strain*Es)


def strain_at_depth(eu,neutral_axis_depth,depth_of_interest):
    '''
    Given and Neutral Axis Depth and the maximum compressive strain
    at the extreme compression fiber

    return the associated strain at the depth of interest

    assumptions:
        the strain varies linearly along the elevation axis (y-axis)
        0 depth is the point max compression strain, eu.

    will return a (+) strain for areas in compression and a (-) negative
    strain when area is in tension
    '''

    c = neutral_axis_depth
    d = depth_of_interest

    if c == 0:
        c = 0.000001
    else:
        c = c
    if c-d > 0:

        e  = ((c-d)/c)*eu

    else:
        e = ((c-d)/c)*eu

    return e

def plastic_center(bars_x=[1], bars_y=[1], fy=60000, As=[0.31], fc=3000, eu=0.003, k=0.85, conc_area=1, conc_centroid=[0,0]):
    '''
    given the ulitmate strain, f'c (28-day) strength and k for concrete
    return a the plastic centroid for the three stress-strain equations
    of the concrete

    accounting for the bar area subtracting from the concrete area by (fy/fc@eu - 1)
    similar approach to transformed sections using n = Es/Ec
    '''

    fc_collins = stress_strain_collins_et_all(fc,eu,eu)
    fc_desayi = stress_strain_desayi_krishnan(fc,eu,k,eu)
    fc_whitney = stress_strain_whitney(fc,eu,eu)

    fc = [fc_collins, fc_desayi, fc_whitney[0]]

    cc = [i*conc_area for i in fc]
    cc_mx = [i*conc_centroid[1] for i in cc]
    cc_my = [i*conc_centroid[0] for i in cc]

    C = []
    C_mx = []
    C_my = []
    cb = []
    cb_mx = []
    cb_my = []
    pc = []

    count = 0
    for c in fc:
        cb.append([i * (fy-c) for i in As])

        C.append(cc[count] + sum(cb[-1]))

        cb_mx.append([(cb[-1][i] * bars_y[i]) for i in range(len(bars_x))])
        cb_my.append([(cb[-1][i] * bars_x[i]) for i in range(len(bars_x))])


        C_mx.append(cc_mx[count]+sum(cb_mx[-1]))
        C_my.append(cc_my[count]+sum(cb_my[-1]))

        yp = C_mx[-1]/C[-1]
        xp = C_my[-1]/C[-1]

        pc.append([xp,yp])

        count +=1
    
    return pc,[fc,cc,cc_mx,cc_my,cb,cb_mx,cb_my,C,C_mx,C_my]


#----- START UNI-AXIAL COLUMN EXAMPLE DIAGRAM -----#
# Test the strain at depth function
# assume a 12"x24" section with the na located at 16"
# above the base. The section if oriented with the 24"
# vertical.
b=20
h=30
#na = 12
##lets create a list of y dstances from the top lets say 1 per 0.25"
#count = int(24/0.25)+1
#y = [0+(i*0.25) for i in range(0,count)]
#
#x = [strain_at_depth(0.003,na,j) for j in y]
#
#plt.close('all')
#plt.plot(x, y, 'r-')
#plt.plot(x,[na]*len(x),'b-')
#plt.plot([0]*len(y),y,'k-')
#plt.set_ylim([-70,70])
#plt.set_xlim([-0.005,0.005])
#plt.show()

# expand on the 12x24 column test subject and generate a P-M value
# for it's strong axis using all three stress block methods at a given
# Neutral-Axis Depth
# Say F'c = 5000 psi and Fy = 60,000 psi
# notice units here axial force will be in pounds
# and moment will be in in-lbs
fc = 5000
Ec = 57000*math.sqrt(fc)
fy = 60000
Es = 29000000
eu = 0.003
es = 0.002
k = 0.85
# lets add a non-symetric steel layout
# with (2)#8 bars in the bottom and (3)#8 bars at the top
# cover = 2" to each corner bar
xb = [4,16,16,10,4]
yb = [4,4,26,26,26]
ab = [1.27]*len(xb)

acm = (b*h)-sum(ab)
P_max = 0.8*0.65*((0.85*fc*acm)+(fy*sum(ab)))/1000.0

xc = b/2.0
yc = h/2.0

# set a point to sum moments about
# lets try the plastic centroid

pc, pc_backup = plastic_center(xb,yb,fy,ab,fc,eu,k,b*h,[b/2.0,h/2.0])

#yc_collins = pc[0][1]
#yc_desayi = pc[0][1]
#yc_whitney = pc[0][1]
#yc_pca = pc[0][1]

yc_collins = yc
yc_desayi = yc
yc_whitney = yc
yc_pca = yc


# Define some empty lists to dump data into for plotting
P_collins_plot = []
M_collins_plot = []
P_desayi_plot = []
M_desayi_plot = []
P_whitney_plot = []
M_whitney_plot = []
P_pca_plot = []
M_pca_plot = []
aci_reduction = []

e_checks = []

#list neutral axis depths
step = (h+400)/500.0
nas = [(h+400)-(i*step) for i in range(0,499)]

nas.append(0.000001)
print([nas[0],nas[-1]])
#nas = [400]

for na in nas:
    # determine the bar strains and stresses
    # since this is a unixial check only care
    # about the bar Y coordinate
    # also remember we need the bar depth
    # so we need H-y
    b_depths = [h-j for j in yb]
    if na > 0:
        bstrains = [strain_at_depth(eu, na, j) for j in b_depths]
    else:
        bstrains = [-0.005]*len(b_depths)

    bstresses = [stress_strain_steel(fy, es, Es, i) for i in bstrains]

    b_strain_phi = min(bstrains)
    if b_strain_phi > -0.002:
        aci = 0.65

    elif b_strain_phi <= -0.005:
        aci = 0.9

    else:
        aci = 0.65-((b_strain_phi+0.002)*(250/3.0))

    aci_reduction.append(aci)

    # Bar force is now just Bar Area * Stress
    bforce = [i*j for i,j in zip(ab,bstresses)]

    # Remove a component of concrete compression force from
    # area coincident with the bars in the compression zone

    bforce_collins = [(q*stress_strain_collins_et_all(fc,eu,j)) if i>0 else 0 for i,j,q in zip(bforce,bstrains,ab)]
    bforce_desayi = [(q*stress_strain_desayi_krishnan(fc,eu,k,j)) if i>0 else 0  for i,j,q in zip(bforce,bstrains,ab)]
    bforce_whitney = [(q*stress_strain_whitney(fc,eu,j)[0]) if i>0 else 0  for i,j,q in zip(bforce,bstrains,ab)]
    bforce_pca = [(q*stress_strain_pca(fc,eu,Ec,j)) if i>0 else 0  for i,j,q in zip(bforce,bstrains,ab)]

    #bforce_whitney = [0]*len(ab)

    # Bar Momments - using right hand rule tensile forces below
    # the point we are summing momments about should be positive
    # therefore use the signed distance from the bar to the
    # point of interest
    bmomentarm_collins = [j-yc_collins for j in yb]
    bmoment_collins = [i*j for i,j in zip(bforce,bmomentarm_collins)]
    bmomentarm_desayi = [j-yc_desayi for j in yb]
    bmoment_desayi = [i*j for i,j in zip(bforce,bmomentarm_desayi)]
    bmomentarm_whitney = [j-yc_whitney for j in yb]
    bmoment_whitney = [i*j for i,j in zip(bforce,bmomentarm_whitney)]
    bmomentarm_pca = [j-yc_pca for j in yb]
    bmoment_pca = [i*j for i,j in zip(bforce,bmomentarm_pca)]

    bnegmoment_collins = [i*j for i,j in zip(bforce_collins,bmomentarm_collins)]
    bnegmoment_desayi = [i*j for i,j in zip(bforce_desayi,bmomentarm_desayi)]
    bnegmoment_whitney = [i*j for i,j in zip(bforce_whitney,bmomentarm_whitney)]
    bnegmoment_pca = [i*j for i,j in zip(bforce_pca,bmomentarm_pca)]

    # Concrete force
    # lets get a list of 200 points between the NA
    # and the top of the shape
    iter_points = 200
    if 0 < na < h:
        yce = [0+(na/iter_points*i) for i in range(0,iter_points+1)]
        yce.reverse()
    else:
        yce = [0+(h/iter_points*i) for i in range(0,iter_points+1)]
        yce.reverse()


    # Get the strains at those points
    if na < h:
        ce = [strain_at_depth(eu,na,j) for j in yce]
    else:
        ce = [eu]*len(yce)

#    plt.close('all')
#    plt.plot(ce, yce)
#    plt.show()

    # Get the stress at each strain for the three stress-strain functions
    cs_collins = [stress_strain_collins_et_all(fc,eu,i) for i in ce]
    cs_desayi = [stress_strain_desayi_krishnan(fc,eu,k,i) for i in ce]
    cs_pca = [stress_strain_pca(fc,eu,Ec,i) for i in ce]

    # to be able to easily the area and center of the 2 parabolic distributions
    # lets close of there shape
    yce.append(yce[-1])
    yce.append(yce[0])
    yce.append(yce[0])
    cs_collins.extend([0,0,cs_collins[0]])
    cs_desayi.extend([0,0,cs_desayi[0]])
    cs_pca.extend([0,0,cs_pca[0]])

    #plt.close('all')
    #plt.plot(yce,cs_collins)
    #plt.show()

    # Area=P and center under each curve
    p_collins = sum([(yce[i]*cs_collins[i+1])-(yce[i+1]*cs_collins[i]) for i in range(len(yce[:-1]))])/2.0
    if p_collins == 0:
        p_collinsy = 0
    else:
        p_collinsy = sum([(yce[i]+yce[i+1])*((yce[i]*cs_collins[i+1])-(yce[i+1]*cs_collins[i])) for i in range(len(yce[:-1]))])/(6*p_collins)

    p_desayi = sum([(yce[i]*cs_desayi[i+1])-(yce[i+1]*cs_desayi[i]) for i in range(len(yce[:-1]))])/2.0
    if p_desayi == 0:
        p_desayiy = 0
    else:
        p_desayiy = sum([(yce[i]+yce[i+1])*((yce[i]*cs_desayi[i+1])-(yce[i+1]*cs_desayi[i])) for i in range(len(yce[:-1]))])/(6*p_desayi)
    
    p_pca = sum([(yce[i]*cs_pca[i+1])-(yce[i+1]*cs_pca[i]) for i in range(len(yce[:-1]))])/2.0
    if p_pca == 0:
        p_pcay = 0
    else:
        p_pcay = sum([(yce[i]+yce[i+1])*((yce[i]*cs_pca[i+1])-(yce[i+1]*cs_pca[i])) for i in range(len(yce[:-1]))])/(6*p_pca)

    # note the y values are from the top of the beam down
    # convert them back to there normal coordinate
    p_collinsy = h-p_collinsy
    p_desayiy = h-p_desayiy
    p_pcay = h-p_pcay

    collins_momentarm = p_collinsy - yc
    desayi_momentarm = p_desayiy - yc
    pca_momentarm = p_pcay - yc

    # because the shape is square the surface slice for both Collins and Desayi
    # describe the volume for the full width so the total force is the area of the
    # surface slice times the width of the colmn **note units used so far
    C_collins = p_collins*b
    C_desayi = p_desayi*b
    C_pca = p_pca*b


    # since the whitney block is rectangular all we need is beta1 value
    # and the peak stress
    cs_whitney = stress_strain_whitney(fc,eu,eu)

    # the whitney block applies 0.85F'c over beta1*c
    if cs_whitney[1]*na < h:
        C_whitney = cs_whitney[0]*cs_whitney[1]*na*b
        whitneyy = cs_whitney[1]*(na) / 2.0
    else:
        C_whitney = cs_whitney[0]*h*b
        whitneyy = (h) / 2

    whitneyy = h - whitneyy
    whitney_momentarm = whitneyy - yc

    #Sum Forces
    P_bars = sum(bforce)
    p_bars_neg = [sum(bforce_collins),sum(bforce_desayi),sum(bforce_whitney),sum(bforce_pca)]
    
    Axial_collins = P_bars + C_collins - p_bars_neg[0]
    Axial_desayi = P_bars + C_desayi - p_bars_neg[1]
    
    Axial_whitney = P_bars + C_whitney - p_bars_neg[2]
    
    Axial_pca = P_bars + C_pca - p_bars_neg[3]
    
    # Concrete Moments
    M_collins = C_collins*collins_momentarm
    M_desayi = C_desayi*desayi_momentarm
    M_whitney = C_whitney*whitney_momentarm
    M_pca = C_pca*pca_momentarm

    m_bars_collins = sum(bmoment_collins)
    m_bars_desayi = sum(bmoment_desayi)
    m_bars_whitney = sum(bmoment_whitney)
    m_bars_pca = sum(bmoment_pca)

    m_bars_neg = [sum(bnegmoment_collins), sum(bnegmoment_desayi), sum(bnegmoment_whitney), sum(bnegmoment_pca)]

    Mx_collins = m_bars_collins + M_collins - m_bars_neg[0]
    Mx_desayi = m_bars_desayi + M_desayi - m_bars_neg[1]
    Mx_whitney = m_bars_whitney + M_whitney - m_bars_neg[2]
    Mx_pca = m_bars_pca + M_pca - m_bars_neg[3]
    
    # Moments from Eccentricy of Axial applied at geometric center to
    # plastic center
    Mx_collins += Axial_collins * (yc-yc_collins)
    Mx_desayi += Axial_desayi * (yc-yc_desayi)
    Mx_whitney += Axial_whitney * (yc-yc_whitney)
    Mx_pca += Axial_pca *(yc-yc_pca)
    
    # Determine the centroid of the eccentricity of the axial load
    e_collins = Mx_collins / Axial_collins
    e_desayi = Mx_desayi / Axial_desayi
    e_whitney = Mx_whitney / Axial_whitney
    e_pca = Mx_pca / Axial_pca

    e_checks.append([e_collins,e_desayi,e_whitney,e_pca])

    P_collins_plot.append(Axial_collins/1000.0)
    M_collins_plot.append(Mx_collins/(1000*12.0))
    P_desayi_plot.append(Axial_desayi/1000.0)
    M_desayi_plot.append(Mx_desayi/(1000*12.0))
    P_whitney_plot.append(Axial_whitney/1000)
    M_whitney_plot.append(Mx_whitney/(1000*12.0))
    P_pca_plot.append(Axial_pca/1000)
    M_pca_plot.append(Mx_pca/(1000*12.0))


plt.close('all')

ax5 = plt.subplot2grid((2, 2), (0, 0), rowspan=2)
ax1 = plt.subplot2grid((2, 2), (0, 1))
ax2 = plt.subplot2grid((2, 2), (1, 1))
ax5.plot(M_collins_plot,P_collins_plot,'r--')
ax5.plot([i*j for i,j in zip(M_collins_plot,aci_reduction)],[i*j if i<P_max else P_max*j for i,j in zip(P_collins_plot,aci_reduction)],'r-')
ax5.plot(M_desayi_plot,P_desayi_plot,'g--')
ax5.plot([i*j for i,j in zip(M_desayi_plot,aci_reduction)],[i*j if i<P_max else P_max*j for i,j in zip(P_desayi_plot,aci_reduction)],'g-')
ax5.plot(M_whitney_plot,P_whitney_plot,'b--')
ax5.plot([i*j for i,j in zip(M_whitney_plot,aci_reduction)],[i*j if i<P_max else P_max*j for i,j in zip(P_whitney_plot,aci_reduction)],'b-')
ax5.plot(M_pca_plot,P_pca_plot,'y--')
ax5.plot([i*j for i,j in zip(M_pca_plot,aci_reduction)],[i*j if i<P_max else P_max*j for i,j in zip(P_pca_plot,aci_reduction)],'y-')
ax5.plot([0,max(M_desayi_plot)],[0,0],'k-')
string = 'P-M - 20x30 - fc = 5000 - (5)#10'
ax5.set_title(string)
ax5.minorticks_on()
ax5.grid(b=True, which='major', color='k', linestyle='-', alpha=0.5)
ax5.grid(b=True, which='minor', color='k', linestyle='-', alpha=0.2)


#----- END UNI-AXIAL COLUMN EXAMPLE DIAGRAM -----#

#----- Stress-Strain Curve Plots -----#
# Example plots of the above stress strain curves
# uncomment between #----# as well as the import for
# matplotlib at the head of the file
#----#
x = [-0.004+(i*0.00005) for i in range(0,161)]
y = [stress_strain_steel(60000, 0.002, Es, i) for i in x]
#
y2 = [stress_strain_collins_et_all(fc,0.003,i) for i in x]
y3 = [stress_strain_desayi_krishnan(fc,0.003,0.85,i) for i in x]
y4 = [stress_strain_whitney(fc,0.003,i)[0] for i in x]
y5 = [stress_strain_pca(fc,0.003,Ec,i) for i in x]
y6 = [i/0.85 for i in y2]
y7 = [i/0.85 for i in y3]
y8 = [i/0.85 for i in y5]
y9 = [i/0.85 for i in y4]
#
#plt.close('all')
#f, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
ax1.plot(x, y, 'c-')
ax1.plot(x, [0]*len(x),'k-')
ax1.set_title('Steel Stress-Strain')
ax1.set_ylim([-70000,70000])
ax1.set_xlim([-0.005,0.005])
ax2.plot(x, y6, 'r--')
ax2.plot(x, y2, 'r-', label='Concrete Stress-Strain (Collins)')
ax2.plot(x, y7, 'g--')
ax2.plot(x, y3, 'g-', label='Concrete Stress-Strain (Desayi & Krishnan)')
ax2.plot(x, y9, 'b--')
ax2.plot(x, y4, 'b-', label='Concrete Stress-Strain (Whitney ACI318)')
ax2.plot(x, y8, 'y--')
ax2.plot(x, y5, 'y-', label='Concrete Stress-Strain (PCA Notes on ACI318-05)')
ax2.plot(x, [0]*len(x),'k-')
ax2.set_title('Concrete Stress-Strain Curves - Dashed Lines are curve/0.85')
ax2.set_ylim([-1000,(fc+1000)])
ax2.set_xlim([-0.001,0.005])
#ax2.legend()

#plt.tight_layout()

plt.show()
#----#