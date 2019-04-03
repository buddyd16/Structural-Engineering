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
import pin_pin_beam_equations_classes as ppbeam

def load_patterns_by_span_ACI(n, byspan=True):
    pat1 = [1 for i in range(1,n+1)] # all spans loaded
    pat2 = [1 if i % 2 == 0 else 0 for i in range(1,n+1)] # even spans loaded
    pat3 = [0 if i % 2 == 0 else 1 for i in range(1,n+1)] # odd spans loaded

    count = 0
    pat4 = []
    pat5 = []
    pat6 = []
    for i in range(1,n+1):

        if count<=1:
            if count == 0:
                pat4.append(1)
                pat5.append(0)
                pat6.append(1)
            else:
                pat4.append(1)
                pat5.append(1)
                pat6.append(0)
            count+=1
        else:
            pat4.append(0)
            pat5.append(1)
            pat6.append(1)
            count=0
    
    if n==1:
        patterns = [pat1]
        
    elif n==2:
        patterns = [pat1,pat2,pat3]
    
    elif n==3:
        patterns = [pat1,pat2,pat3,pat4,pat5]
        
    else:
        patterns = [pat1,pat2,pat3,pat4,pat5,pat6]
    
    if byspan == True:
        patterns_transpose = map(list, zip(*patterns))

        return patterns_transpose
    else:
        return patterns

class Load:
    def __init__(self, span=0, span_label='0', w1=0, w2=0, a=0, b=0, span_length=0, backspan_length=0, cantilever_side=0, load_kind = 'NL'):
        '''
        A class to define loads vs using a list or dictionary 
        to allow for more consistent property definitions 
        and future embeded functions for things such as
        fixed end forces
        '''
        
        self.span = span
        self.span_label = span_label
        self.w1 = w1
        self.w2 = w2
        self.a = a
        self.b = b
        self.span_length = span_length
        self.backspan_length = backspan_length
        self.cantilever_side = cantilever_side
        self.load_kind = load_kind

    def make_analytical(self):
        
        if self.cantilever_side == 1:
            
            if self.load_kind == 'Point':
                self.analytical = ppbeam.cant_left_point(self.w1,self.a,self.span_length,self.backspan_length)

            elif self.load_kind == 'Moment':
                self.analytical = ppbeam.cant_left_point_moment(self.w1,self.a,self.span_length,self.backspan_length)

            elif self.load_kind == 'UDL':
                self.analytical = ppbeam.cant_left_udl(self.w1,self.a,self.b,self.span_length,self.backspan_length)

            elif self.load_kind == 'TRAP':
                self.analytical = ppbeam.cant_left_trap(self.w1, self.w2, self.a, self.b, self.span_length, self.backspan_length)

            elif self.load_kind == 'SLOPE':
                self.analytical = ppbeam.cant_left_nl(self.w1,self.span_length)

            else:
                self.analytical = ppbeam.no_load(0)
            
        elif self.cantilever_side == 2:
            
            if self.load_kind == 'Point':
                self.analytical = ppbeam.cant_right_point(self.w1,self.a,self.span_length,self.backspan_length)

            elif self.load_kind == 'Moment':
                self.analytical = ppbeam.cant_right_point_moment(self.w1,self.a,self.span_length,self.backspan_length)

            elif self.load_kind == 'UDL':
                self.analytical = ppbeam.cant_right_udl(self.w1,self.a,self.b,self.span_length,self.backspan_length)

            elif self.load_kind == 'TRAP':
                self.analytical = ppbeam.cant_right_trap(self.w1, self.w2, self.a, self.b, self.span_length, self.backspan_length)

            elif self.load_kind == 'SLOPE':
                self.analytical = ppbeam.cant_right_nl(self.w1,self.span_length)

            else:
                self.analytical = ppbeam.no_load(0)
        else:
            if self.load_kind == 'Point':
                self.analytical = ppbeam.pl(self.w1,self.a,self.span_length)

            elif self.load_kind == 'Moment':
                self.analytical = ppbeam.point_moment(self.w1,self.a,self.span_length)

            elif self.load_kind == 'UDL':
                self.analytical = ppbeam.udl(self.w1,self.a,self.b,self.span_length)

            elif self.load_kind == 'TRAP':
                self.analytical = ppbeam.trap(self.w1,self.w2,self.a,self.b,self.span_length)

            elif self.load_kind == 'END_DELTA':
               self.analytical = ppbeam.end_delta(self.w1,self.w2,self.span_length)

            else:
                self.analytical = ppbeam.no_load(0)          
        
                
    def fixed_end_forces(self):
        self.make_analytical()
        
        self.fef = self.analytical.fef()
    
    def load_as_list(self):
        
        return [self.span, self.w1, self.w2, self.a, self.b, self.span_length, self.backspan_length, self.load_kind]


        
class LoadType:
    def __init__(self, pattern=False, off_pattern_factor=0, title='Dead',symbol='DL'):
        '''
        A class to house loads to facilitate
        performing load factoring, paterning, and combinations

        NOTE: unless a function notes otherwise everything expects to
        be a getting list in the form of:
            [span, w1,w2,a,b,L,'Load Type'] or
            [span, w1,w2,a,b,L,L,'Load Type'] in the case of a load on a cantilever

            'Load Type' should always be the last item
            'Span' should always be the first item

        '''

        self.title = title
        self.symbol = symbol
        self.load_list = []
        self.pattern = pattern
        self.off_pattern_factor = off_pattern_factor
        self.factored_loads = 0
        self.all_factored_loads = []
        self.patterned_factored_loads = []
        self.all_patterned_factored_loads = []

    def add_single_load(self,load=[0,0,0,10,10,10,'NL']):
        self.load_list.append(load)

    def add_multi_loads(self,loads=[[0,0,0,10,10,10,'NL'],[0,0,0,10,10,10,'NL']]):
        self.load_list.extend(loads)

    def remove_load_by_index(self, index):
        num_loads = len(self.load_list)

        if num_loads == 0 or index > num_loads:
            pass
        else:
            del self.load_list[index]

    def clear_loads(self):

        del self.load_list[:]

    def factor_loads(self,factor,on=1):
        factored_loads = []

        if self.pattern==False:
            load_factor = factor
        elif on == 1:
            load_factor = factor
        else:
            load_factor = factor*self.off_pattern_factor

        for load in self.load_list:
            w1 = load[1]
            w2 = load[2]

            if w1*load_factor ==0 and w2*load_factor==0:
                pass

            else:
                w1_factored = w1*load_factor
                w2_factored = w2*load_factor

                factored_loads.append([load[0],w1_factored,w2_factored]+load[3:])

                self.factored_loads = factored_loads

        return factored_loads

    def multiple_factor_loads(self, factors=[1,1], on=1):
        all_factored_loads = []

        del self.all_factored_loads[:]

        for factor in factors:
            all_factored_loads.append(self.factor_loads(factor,on))

        self.all_factored_loads= all_factored_loads

        return all_factored_loads

    def pattern_and_factor_loads(self,factor,patterns = [1,0,1,1,0,1]):

        patterned_loads = []
        del self.patterned_factored_loads[:]

        for i, pattern in enumerate(patterns):
            
            for load in self.load_list:
                
                if load[0] == i:

                    on = pattern

                    if self.pattern==False:
                        load_factor = factor
                    elif on == 1:
                        load_factor = factor
                    else:
                        load_factor = factor*self.off_pattern_factor

                    w1 = load[1]
                    w2 = load[2]

                    if w1*load_factor ==0 and w2*load_factor==0:
                        pass

                    else:
                        w1_factored = w1*load_factor
                        w2_factored = w2*load_factor

                        patterned_loads.append([load[0],w1_factored,w2_factored]+load[3:])

                else:
                    pass

        self.patterned_factored_loads = patterned_loads

        return patterned_loads


def load_combination(load_types, factors, patterns):

    load_set = []

    for pattern in patterns:
        pat_set = []
        for i,load in enumerate(load_types):
            pat_set.extend(load.pattern_and_factor_loads(factors[i], pattern))
        load_set.append(pat_set)

    return load_set

def load_combination_multi(load_types, factors, patterns):

    load_set = []
    
    for factor in factors:
        for pattern in patterns:
            pat_set = []
            for i,load in enumerate(load_types):
                pat_set.extend(load.pattern_and_factor_loads(factor[i], pattern))
            load_set.append(pat_set)

    return load_set

Self = LoadType(False,1,'Self','SW')
Dead = LoadType(False,1,'Dead','DL')
Live = LoadType(False,0,'Live','LL')
Live_pat = LoadType(True,0,'Live_pat','LL_pat')

Self.add_multi_loads([[0,1,0,0,10,30,0,'UDL'],[1,1,0,10,20,30,0,'UDL'],[2,1,0,20,30,30,0,'UDL']])
Dead.add_multi_loads([[0,1,0,0,10,30,0,'UDL'],[1,1,0,10,20,30,0,'UDL'],[2,1,0,20,30,30,0,'UDL']])

Live.add_multi_loads([[0,1,0,0,10,30,0,'UDL'],[1,1,0,10,20,30,0,'UDL'],[2,1,0,20,30,30,0,'UDL']])
Live_pat.add_multi_loads([[0,1,0,0,10,30,0,'UDL'],[1,1,0,10,20,30,0,'UDL'],[2,1,0,20,30,30,0,'UDL']])

patterns = load_patterns_by_span_ACI(3, False)

combos = [[1,1,0,0],[0,0,1,1],[1,1,1,1],[3,3,1,1],[1.4,1.4,0,0],[1.2,1.2,1.6,1.6]]

combined_loads = load_combination_multi([Self,Dead,Live,Live_pat],combos,patterns)

unique_combo = []

for i, combined in enumerate(combined_loads):
    if i == 0 or combined != combined_loads[i-1]:
        unique_combo.append(combined)
    else:
        pass

pat_live = []
for i,pat in enumerate(patterns):
    pat_live.append([])          
    f = 1
    out = Live_pat.pattern_and_factor_loads(f,pat)
    pat_live[i].extend(out)

test_load = Load(0,'BM_1',1,0,0,10,10,0,0,'UDL')

test_load.fixed_end_forces()

print test_load.fef
print test_load.load_as_list()