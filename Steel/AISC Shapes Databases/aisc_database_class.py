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

labels = db.labels