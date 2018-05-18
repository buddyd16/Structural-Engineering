# -*- coding: utf-8 -*-
"""
Created on Fri May 04 16:09:57 2018

@author: DonB
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



class aisc_15th_database:
    def __init__(self):
        
        ## BUILD SHAPE DICTIONARY AND ATTRIBUTE LISTS
        ## NOTE THE STANDARD DATABADE PROVIDED BY AISC NEEDS TO BE CLEANED UP
        ## ALL - FIELDS NEED TO BE REPLACED BY 0's
        
        file = open('aisc_shapes_database_v15.0.csv','r')
        
        data_raw = file.readlines()
        
        file.close()
        
        file = open('aisc_v15_units.csv','r')
        units_raw = file.readlines()
        file.close()
        
        file = open('aisc_v15_defs.csv','r')
        defs_raw = file.readlines()
        file.close()
        
        self.units = units_raw[0].split(',')
        self.units[-1] = self.units[-1].rstrip('\n')
        
        self.definitions = []
        for prop_def in defs_raw:
            prop_def = prop_def.split(',')
            prop_def[-1] = prop_def[-1].rstrip('\n')
            self.definitions.append(prop_def)
        
        self.labels = data_raw[0].split(',')
        self.labels[-1] = self.labels[-1].rstrip('\n')
        
        self.shapes = []
        self.shape_types = []
        
        for shape in data_raw[1:]:
            shape = shape.split(',')
            shape[-1] = shape[-1].rstrip('\n')
            if shape[0] == 'HSS':
                if float(shape[10]) > 0:
                    shape[0] = 'HSS-RND'
                elif shape[8] == shape[13]:
                    shape[0] = 'HSS-SQR'
                else:
                    shape[0] = 'HSS-RECT'
            else:
                pass
            
            self.shapes.append(shape)
            self.shape_types.append(shape[0])
        
        self.shape_types = list(set(self.shape_types))
        
    def WF(self):
        shape_selection_list = []
        filtered_shape_list = []
        
        for shape in self.shapes:
            if shape[0] == 'W':
                shape_selection_list.append(shape[1])
                filtered_shape_list.append(shape)
            else:
                pass
        
        return shape_selection_list,filtered_shape_list
    
    def PIPE(self):
        shape_selection_list = []
        filtered_shape_list = []
        
        for shape in self.shapes:
            if shape[0] == 'PIPE':
                shape_selection_list.append(shape[1])
                filtered_shape_list.append(shape)
            else:
                pass
        
        return shape_selection_list,filtered_shape_list
        
    def C(self):
        shape_selection_list = []
        filtered_shape_list = []
        
        for shape in self.shapes:
            if shape[0] == 'C':
                shape_selection_list.append(shape[1])
                filtered_shape_list.append(shape)
            else:
                pass
        
        return shape_selection_list,filtered_shape_list

    def HSS_RND(self):
        shape_selection_list = []
        filtered_shape_list = []
        
        for shape in self.shapes:
            if shape[0] == 'HSS-RND':
                shape_selection_list.append(shape[1])
                filtered_shape_list.append(shape)
            else:
                pass
        
        return shape_selection_list,filtered_shape_list

    def MC(self):
        shape_selection_list = []
        filtered_shape_list = []
        
        for shape in self.shapes:
            if shape[0] == 'MC':
                shape_selection_list.append(shape[1])
                filtered_shape_list.append(shape)
            else:
                pass
        
        return shape_selection_list,filtered_shape_list

    def HSS_RECT(self):
        shape_selection_list = []
        filtered_shape_list = []
        
        for shape in self.shapes:
            if shape[0] == 'HSS-RECT':
                shape_selection_list.append(shape[1])
                filtered_shape_list.append(shape)
            else:
                pass
        
        return shape_selection_list,filtered_shape_list
        
    def HP(self):
        shape_selection_list = []
        filtered_shape_list = []
        
        for shape in self.shapes:
            if shape[0] == 'HP':
                shape_selection_list.append(shape[1])
                filtered_shape_list.append(shape)
            else:
                pass
        
        return shape_selection_list,filtered_shape_list
        
    def M(self):
        shape_selection_list = []
        filtered_shape_list = []
        
        for shape in self.shapes:
            if shape[0] == 'M':
                shape_selection_list.append(shape[1])
                filtered_shape_list.append(shape)
            else:
                pass
        
        return shape_selection_list,filtered_shape_list
        
    def L(self):
        shape_selection_list = []
        filtered_shape_list = []
        
        for shape in self.shapes:
            if shape[0] == 'L':
                shape_selection_list.append(shape[1])
                filtered_shape_list.append(shape)
            else:
                pass
        
        return shape_selection_list,filtered_shape_list
        
    def ST(self):
        shape_selection_list = []
        filtered_shape_list = []
        
        for shape in self.shapes:
            if shape[0] == 'ST':
                shape_selection_list.append(shape[1])
                filtered_shape_list.append(shape)
            else:
                pass
        
        return shape_selection_list,filtered_shape_list
        
    def HSS_SQR(self):
        shape_selection_list = []
        filtered_shape_list = []
        
        for shape in self.shapes:
            if shape[0] == 'HSS-SQR':
                shape_selection_list.append(shape[1])
                filtered_shape_list.append(shape)
            else:
                pass
        
        return shape_selection_list,filtered_shape_list
        
    def MT(self):
        shape_selection_list = []
        filtered_shape_list = []
        
        for shape in self.shapes:
            if shape[0] == 'MT':
                shape_selection_list.append(shape[1])
                filtered_shape_list.append(shape)
            else:
                pass
        
        return shape_selection_list,filtered_shape_list
        
    def S(self):
        shape_selection_list = []
        filtered_shape_list = []
        
        for shape in self.shapes:
            if shape[0] == 'S':
                shape_selection_list.append(shape[1])
                filtered_shape_list.append(shape)
            else:
                pass
        
        return shape_selection_list,filtered_shape_list
        
    def WT(self):
        shape_selection_list = []
        filtered_shape_list = []
        
        for shape in self.shapes:
            if shape[0] == 'WT':
                shape_selection_list.append(shape[1])
                filtered_shape_list.append(shape)
            else:
                pass
        
        return shape_selection_list,filtered_shape_list
        
    def LL(self):
        shape_selection_list = []
        filtered_shape_list = []
        
        for shape in self.shapes:
            if shape[0] == '2L':
                shape_selection_list.append(shape[1])
                filtered_shape_list.append(shape)
            else:
                pass
        
        return shape_selection_list,filtered_shape_list
        
db = aisc_15th_database()

defs = db.definitions

sections = db.shapes