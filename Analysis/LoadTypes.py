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

class LoadType:
    def __init__(self, pattern=False, off_pattern_factor=0, title='Dead',symbol='DL'):
        '''
        A class to house loads to facilitate
        performing load factoring, paterning, and combinations
        
        NOTE: unless a function notes otherwise everything expects to
        be a getting list in the form of:
            [w1,w2,a,b,L,'Load Type'] or
            [w1,w2,a,b,L,L,'Load Type']
            
            'Load Type' should always be the last item
            
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
        
        if on == 1:
            load_factor = factor
        else:
            load_factor = factor*self.off_pattern_factor
            
        for load in self.load_list:
            w1 = load[0]
            w2 = load[1]
            
            if w1 ==0 and w2==0:
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
    
    def multi_pattern_and_factor(self,factors=[1,1],patterns = [1,0,1,1,0,1]):
        
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
                
            
Dead = LoadType()

Dead.add_single_load([1,0,0,10,10,10,'UDL'])
Dead.add_multi_loads([[1,0,5,10,10,10,'PL'],[1,0,0,10,10,10,'TRAP']])

test = Dead.multiple_factor_loads([1,1.4,1.2],1)

Live = LoadType(True,0,'Live','LL')
Live.add_single_load([1,0,0,10,10,10,'UDL'])
Live.add_multi_loads([[1,0,5,10,10,10,'PL'],[1,0,0,10,10,10,'TRAP']])

pattern = [1,0,0,1,1]
lfD = [1.4,1.2,1.2]
lfL = [0,1.6,0.5*1.6]
test_pattern = Live.multi_pattern_and_factor(lfL,pattern)
test_dead_pattern = Dead.multi_pattern_and_factor(lfD,pattern)



