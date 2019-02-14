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

def load_patterns_by_span_ACI(n):
    pat1 = [1 for i in range(1,n+1)]
    pat2 = [1 if i % 2 == 0 else 0 for i in range(1,n+1)]
    pat3 = [0 if i % 2 == 0 else 1 for i in range(1,n+1)]
    
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
    
    patterns = [pat1,pat2,pat3,pat4,pat5,pat6]
    
    patterns_trans = map(list, zip(*patterns))
    
    return patterns_trans

class LoadType:
    def __init__(self, pattern=False, off_pattern_factor=0, title='Dead',symbol='DL'):
        '''
        A class to house loads to facilitate
        performing load factoring, paterning, and combinations
        
        NOTE: unless a function notes otherwise everything expects to
        be a getting list in the form of:
            [w1,w2,a,b,L,span #,'Load Type'] or
            [w1,w2,a,b,L,L,span #,'Load Type'] in the case of a load on a cantilever
            
            'Load Type' should always be the last item
            'Span #' should always be the second to last item
            
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
            w1 = load[0]
            w2 = load[1]
            
            if w1*load_factor ==0 and w2*load_factor==0:
                pass
            
            else:
                w1_factored = w1*load_factor
                w2_factored = w2*load_factor
                
                factored_loads.append([w1_factored,w2_factored]+load[2:])
        
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
        
        if self.pattern == False:
            return []
        
        else:
            
            for pattern in patterns:
                patterned_loads.append(self.factor_loads(factor,pattern))
            
            self.patterned_factored_loads = patterned_loads
            
            return patterned_loads
    
    def multi_pattern_and_factor(self,factors=[1,1],patterns = [1,0,1]):
        
        factored_patterned = []
        
        del self.all_patterned_factored_loads[:]
        
        if self.pattern == False:
            for factor in factors:              
                patterned = []
                
                for pattern in patterns:
                    patterned.append(self.factor_loads(factor,1))
                factored_patterned.append(patterned)
        
        else:
            
            for factor in factors:
                patterned = []
                
                for pattern in patterns:
                    patterned.append(self.factor_loads(factor,pattern))
                
                factored_patterned.append(patterned)
                
        self.all_patterned_factored_loads = factored_patterned
        
        return factored_patterned
                

def load_combination(load_types, factors, patterns):
    
    load_set = []
    
    for pattern in patterns:
        pat_set = []
        for i,load in enumerate(load_types):
            pat_set.extend(load.factor_loads(factors[i], pattern))
        load_set.append(pat_set)
           
    return load_set

def load_combination_multi(load_types, factors, patterns):
    
    load_set = []
    for j, factor in enumerate(factors):
        for pattern in patterns[j]:
            pat_set = []
            for i,load in enumerate(load_types):
                pat_set.extend(load.factor_loads(factor[i], pattern))
            load_set.append(pat_set)
           
    return load_set
    
            
Dead = LoadType(False,1,'Dead','DL')
Live = LoadType(True,0,'Live','LL')


Dead.add_single_load([1,0,0,10,10,10,'UDL'])
Dead.add_multi_loads([[1,0,5,10,10,10,'PL'],[1,0,0,10,10,10,'TRAP']])

test = Dead.multiple_factor_loads([1,1.4,1.2],1)


Live.add_single_load([1,0,0,10,10,10,'UDL'])
Live.add_multi_loads([[1,0,5,10,10,10,'PL'],[1,0,0,10,10,10,'TRAP']])

pattern = [1,0,0,1,1]
lfD = [1.4,1.2,1.2]
lfL = [0,1.6,0.5*1.6]
test_pattern = Live.multi_pattern_and_factor(lfL,pattern)
test_dead_pattern = Dead.multi_pattern_and_factor(lfD,pattern)

combo = load_combination([Dead,Live],[1.2,1.6],pattern)
combos = load_combination_multi([Dead,Live],[[1.4,0],[1.2,1.6]],[[1],pattern])

pats = load_patterns_by_span_ACI(20)

