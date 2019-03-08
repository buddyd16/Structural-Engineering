#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 20:20:20 2019

@author: donaldbockoven
"""

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
        patterns = [pat1,pat3,pat3]
    
    elif n==3:
        patterns = [pat1,pat2,pat3,pat4,pat5]
        
    else:
        patterns = [pat1,pat2,pat3,pat4,pat5,pat6]
    
    if byspan == True:
        patterns_transpose = map(list, zip(*patterns))

        return patterns_transpose
    else:
        return patterns

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
