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


import Tkinter as tk
import tkFont
import tkMessageBox

class Master_window:

    def __init__(self, master):
        
        self.shape_types = ['C', 'MC', 'HSS','HSS - ROUND', 'HP', 'M', 'L', 'ST', 'PIPE', 'MT', 'S', 'WT', 'W', '2L']
        self.values_list = ['T_F', 'W', 'A', 'd', 'ddet', 'Ht', 'h', 'OD', 'bf', 'bfdet', 'B', 'b', 'ID', 'tw', 'twdet', 'twdet/2', 'tf', 'tfdet', 't', 'tnom', 'tdes', 'kdes', 'kdet', 'k1', 'x', 'y', 'eo', 'xp', 'yp', 'bf/2tf', 'b/t', 'b/tdes', 'h/tw', 'h/tdes', 'D/t', 'Ix', 'Zx', 'Sx', 'rx', 'Iy', 'Zy', 'Sy', 'ry', 'Iz', 'rz', 'Sz', 'J', 'Cw', 'C', 'Wno', 'Sw1', 'Sw2', 'Sw3', 'Qf', 'Qw', 'ro', 'H', 'tan(alpha)', 'Qs', 'Iw', 'zA', 'zB', 'zC', 'wA', 'wB', 'wC', 'SwA', 'SwB', 'SwC', 'SzA', 'SzB', 'SzC', 'rts', 'ho', 'PA', 'PB']
        self.values_units = ['', 'lbs/ft', 'in^2', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', '', '', '', '', '', '', 'in^4', 'in^3', 'in^3', 'in', 'in^4', 'in^3', 'in^3', 'in', 'in^4', 'in', 'in^3', 'in^4', 'in^6', 'in^3', 'in^2', 'in^4', 'in^4', 'in^4', 'in^3', 'in^3', 'in', '', '', '', 'in^4', 'in', 'in', 'in', 'in', 'in', 'in', 'in^3', 'in^3', 'in^3', 'in^3', 'in^3', 'in^3', 'in', 'in', 'in', 'in']
        self.shape_special_note = ['', '', '', '','', 'Section has sloped flanges', '', '', '', 'Section has sloped flanges', '', 'Flange thickness greater than 2 in.', 'Flange thickness greater than 2 in.', '']
        self.values_help = ['T_F - A true/false variable. A value of T (true) indicates that there is a special note for that shape (see below). A value of F (false) indicates that there is not a special note for that shape.', 'W - Nominal weight lb/ft (kg/m)', 'A - Cross-sectional area in^2 (mm2)', 'd - Overall depth of member or width of shorter leg for angles or width of the outstanding legs of long legs back-to-back double angles or the width of the back-to-back legs of short legs back-to-back double angles in. (mm)', 'ddet - Detailing value of member depth in. (mm)', 'Ht - Overall depth of square or rectangular HSS in. (mm)', 'h - Depth of the flat wall of square or rectangular HSS in. (mm)', 'OD - Outside diameter of round HSS or pipe in. (mm)', 'bf - Flange width in. (mm)', 'bfdet - Detailing value of flange width in. (mm)', 'B - Overall width of square or rectangular HSS (the same as B per the 2010 AISC Specification) in. (mm)', 'b - Width of the flat wall of square or rectangular HSS or width of the longer leg for angles or width of the back-to-back legs of long legs back-to-back double angles or width of the outstanding legs of short legs back-to-back double angles in. (mm)', 'ID - Inside diameter of round HSS or pipe in. (mm)', 'tw - Web thickness in. (mm)', 'twdet - Detailing value of web thickness in. (mm)', 'twdet/2 - Detailing value of tw/2 in. (mm)', 'tf - Flange thickness in. (mm)', 'tfdet - Detailing value of flange thickness in. (mm)', 't - Thickness of angle leg in. (mm)', 'tnom - HSS and pipe nominal wall thickness in. (mm)', 'tdes - HSS and pipe design wall thickness in. (mm)', 'kdes - Design distance from outer face of flange to web toe of fillet in. (mm)', 'kdet - Detailing distance from outer face of flange to web toe of fillet in. (mm)', 'k1 - Detailing distance from center of web to flange toe of fillet in. (mm)', 'x - Horizontal distance from designated member edge as defined in the AISC Steel Construction Manual to member centroidal axis in. (mm)', 'y - Vertical distance from designated member edge as defined in the AISC Steel Construction Manual to member centroidal axis in. (mm)', 'eo - Horizontal distance from designated member edge as defined in the AISC Steel Construction Manual to member shear center in. (mm)', 'xp - Horizontal distance from designated member edge as defined in the AISC Steel Construction Manual to member plastic neutral axis in. (mm)', 'yp - Vertical distance from designated member edge as defined in the AISC Steel Construction Manual to member plastic neutral axis in. (mm)', 'bf/2tf - Slenderness ratio', 'b/t - Slenderness ratio for single angles', 'b/tdes - Slenderness ratio for square or rectangular HSS', 'h/tw - Slenderness ratio', 'h/tdes - Slenderness ratio for square or rectangular HSS', 'D/t - Slenderness ratio for round HSS and pipe or tee shapes', 'Ix - Moment of inertia about the x-axis in^4 (mm^4 /10^6)', 'Zx - Plastic section modulus about the x-axis in^3 (mm^3 /10^3)', 'Sx - Elastic section modulus about the x-axis in^3 (mm^3 /10^3)', 'rx - Radius of gyration about the x-axis in. (mm)', 'Iy - Moment of inertia about the y-axis in^4 (mm^4 /10^6)', 'Zy - Plastic section modulus about the y-axis in^3 (mm^3 /10^3)', 'Sy - Elastic section modulus about the y-axis in^3 (mm^3 /10^3)', 'ry - Radius of gyration about the y-axis (with no separation for double angles back-to-back) in. (mm)', 'Iz - Moment of inertia about the z-axis in^4 (mm^3 /10^6)', 'rz - Radius of gyration about the z-axis in. (mm)', 'Sz - Elastic section modulus about the z-axis in^3 (mm^3 /10^3)', 'J - Torsional moment of inertia in^4 (mm^4 /10^3)', 'Cw - Warping constant in^6 (mm^6 /10^9)', 'C - HSS torsional constant in^3 (mm^3 /10^3)', 'Wno - Normalized warping function as used in Design Guide 9 in^2 (mm^2)', 'Sw1 - Warping statical moment at point 1 on cross section as used in Design Guide 9 and shown in Figures 1 and 2 in^4 (mm^4 /10^6)', 'Sw2 - Warping statical moment at point 2 on cross section as used in Design Guide 9 and shown in Figure 2 in^4 (mm^4 /10^6)', 'Sw3 - Warping statical moment at point 3 on cross section as used in Design Guide 9 and shown in Figure 2 in^4 (mm^4 /10^6)', 'Qf - Statical moment for a point in the flange directly above the vertical edge of the web as used in Design Guide 9 in^3 (mm^3 /10^3)', 'Qw - Statical moment for a point at mid-depth of the cross section as used in Design Guide 9 in^3 (mm^3 /10^3)', 'ro - Polar radius of gyration about the shear center in. (mm)', 'H - Flexural constant', 'tan(alpha) - Tangent of the angle between the y-y and z-z axes for single angles where alpga is shown in Figure 3', 'Qs - Reduction factor for slender unstiffened compression elements', 'Iw - Moment of inertia about the w-axis in^4 (mm^4 /10^6)', 'zA - Distance from point A to center of gravity along z-axis as shown in Figure 3 in. (mm)', 'zB - Distance from point B to center of gravity along z-axis as shown in Figure 3 in. (mm)', 'zC - Distance from point C to center of gravity along z-axis as shown in Figure 3 in. (mm)', 'wA - Distance from point A to center of gravity along w-axis as shown in Figure 3 in. (mm)', 'wB - Distance from point B to center of gravity along w-axis as shown in Figure 3 in. (mm)', 'wC - Distance from point C to center of gravity along w-axis as shown in Figure 3 in. (mm)', 'SwA - Elastic section modulus about the w-axis at point A on cross section as shown in Figure 3 in^3 (mm^3 /10^3)', 'SwB - Elastic section modulus about the w-axis at point B on cross section as shown in Figure 3 in^3 (mm^3 /10^3)', 'SwC - Elastic section modulus about the w-axis at point C on cross section as shown in Figure 3 in^3 (mm^3 /10^3)', 'SzA - Elastic section modulus about the z-axis at point A on cross section as shown in Figure 3 in^3 (mm^3 /10^3)', 'SzB - Elastic section modulus about the z-axis at point B on cross section as shown in Figure 3 in^3 (mm^3 /10^3)', 'SzC - Elastic section modulus about the z-axis at point C on cross section as shown in Figure 3 in^3 (mm^3 /10^3)', 'rts - Effective radius of gyration in. (mm)', 'ho - Distance between the flange centroids in. (mm)', 'PA - Shape perimeter minus one flange surface as used in Design Guide 19 in. (mm)', 'PB - Shape perimeter as used in Design Guide 19 in. (mm)']
        
        self.widgets = []
        ## Build master shapes dictionaries from CSV file
        shapes_file = open('aisc_shapes.csv','r')
    
        shape_data_raw = shapes_file.readlines()
    
        shapes_file.close()
        self.shape_sets = []
        for i in range(0,len(self.shape_types)):
            self.shape_sets.append({})
        
        for line in shape_data_raw:
                shape_data_split = line.split(',')
                if shape_data_split[0] == 'Type' or shape_data_split[0]=='':
                    pass
                else:
                    shape_set_index = self.shape_types.index(shape_data_split[0])
                    if shape_data_split[9] == "-" and shape_set_index == 2:
                        shape_set_index = 3
                    else:
                        pass
                    shape = shape_data_split[2]
                    shape_data_split[-1]=shape_data_split[-1].rstrip('\n')
                    shape_data_holder = shape_data_split[3:]
                    temp_shape_dict = {shape: shape_data_holder}
                    self.shape_sets[shape_set_index].update(temp_shape_dict)
        
        self.master = master
        self.f_size = 8
        helv = tkFont.Font(family='Helvetica',size=self.f_size, weight='bold')
        self.menubar = tk.Menu(self.master)
        self.menu = tk.Menu(self.menubar, tearoff=0)
        self.menu_props = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label = "File", menu=self.menu)
        self.menu.add_command(label="Quit", command=self.quit_app)
        self.menubar.add_cascade(label = "Window Properties", menu=self.menu_props)
        self.menu_props.add_command(label="Increase Font Size", command=self.font_size_up)
        self.menu_props.add_command(label="Decrease Font Size", command=self.font_size_down)
        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            self.master.tk.call(master, "config", "-menu", self.menubar)
        
        #Main Frames
        self.main_frame = tk.Frame(master, bd=2, relief='sunken', padx=5,pady=5)
        self.main_frame.pack(anchor='c', padx= 5, pady= 5, fill=tk.BOTH, expand=1)
        self.base_frame = tk.Frame(master, bd=2, relief='sunken', padx=5,pady=5)
        self.base_frame.pack(side=tk.BOTTOM, padx= 5, pady= 5, fill=tk.X, expand=1)

        #Picker Frame
        self.picker_frame = tk.Frame(self.main_frame, padx=2, pady=2)
        self.shape_type = tk.StringVar()
        self.shape_type.set(self.shape_types[0])
        self.shape_type_label = tk.Label(self.picker_frame, text="Steel Shape Type : ", font=helv)
        self.widgets.append(self.shape_type_label)
        self.shape_type_label.pack(side=tk.TOP, fill=tk.X, expand=True)
        self.shape_type_menu = tk.OptionMenu(self.picker_frame, self.shape_type, *self.shape_types, command=self.shape_change)
        self.shape_type_menu.config(font=helv)
        self.shape_type_menu.pack(side=tk.TOP, fill=tk.X, expand=True)
        

        self.shape_frame = tk.LabelFrame(self.picker_frame, text="Section:", bd=1, relief='sunken', padx=5, pady=5, font=helv)
        self.widgets.append(self.shape_frame)
        
        self.shape_menu = tk.Listbox(self.shape_frame, height = 20, width = 40, font=helv)
        self.widgets.append(self.shape_menu)
        for section in sorted(self.shape_sets[0].keys()):
            self.shape_menu.insert(tk.END, section)
        self.shape_menu.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        
        self.shape_scrollbar = tk.Scrollbar(self.shape_frame, orient="vertical")
        self.shape_menu.config(yscrollcommand=self.shape_scrollbar.set)
        self.shape_scrollbar.config(command=self.shape_menu.yview)
        self.shape_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.shape_menu.bind("<<ListboxSelect>>",self.shape_click)
        self.shape_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.picker_frame.pack(side=tk.LEFT)
        
        self.data_frame = tk.LabelFrame(self.main_frame, text="Section Properties - AISC 14th Edition:", bd=1, relief='sunken', padx=5, pady=5, font=helv)
        self.widgets.append(self.data_frame)
        self.properties_labels = []
        for i in range(1,len(self.values_list)):
            self.properties_labels.append(tk.Label(self.data_frame, text='{0}({1}):\n--'.format(self.values_list[i],self.values_units[i]), font=helv, justify=tk.LEFT))
        j=0
        z=0
        for i in range(0,len(self.properties_labels)):
            self.widgets.append(self.properties_labels[i])
            self.properties_labels[i].grid(row = j, column = z, padx=1, pady=1)
            if z<10:
                z+=1
            else:
                z=0
                j+=1
        self.data_frame.pack(side=tk.LEFT)
        
        self.f_size_frame = tk.Frame(self.base_frame, padx=5,pady=5)
        self.f_size_label = tk.Label(self.f_size_frame, text='Font Size ('+str(self.f_size)+'):', font=helv)
        self.widgets.append(self.f_size_label)
        self.f_size_label.grid(row=0,column=0)
        self.b_f_size_minus = tk.Button(self.f_size_frame,text="-", command=self.font_size_down, font=helv)
        self.widgets.append(self.b_f_size_minus)
        self.b_f_size_minus.grid(row=0, column=1, padx=1, pady=1)
        self.b_f_size_plus = tk.Button(self.f_size_frame,text="+", command=self.font_size_up, font=helv)
        self.widgets.append(self.b_f_size_plus)
        self.b_f_size_plus.grid(row=0, column=2, padx=1, pady=1)
        self.f_size_frame.pack(side=tk.LEFT)
        
        self.value_def_frame = tk.Frame(self.base_frame, padx=5,pady=5)
        self.value_def = tk.StringVar()
        self.value_def.set(self.values_list[1])
        self.value_def_menu = tk.OptionMenu(self.value_def_frame, self.value_def, *self.values_list[1:], command=self.value_definitions)
        self.value_def_menu.config(font=helv)
        self.value_def_menu.grid(row=0, column=0, padx=1, pady=1)
        self.value_def_label = tk.Label(self.value_def_frame, text=self.values_help[1], font=helv, wraplength=400, justify=tk.LEFT)
        self.widgets.append(self.value_def_label)
        self.value_def_label.grid(row=0, column=1, padx=10, pady=1)
        filters = ['=','<','>','Between']
        self.value_filter = tk.StringVar()
        self.value_filter.set('=')
        self.value_filter_menu = tk.OptionMenu(self.value_def_frame, self.value_filter, *filters, command=self.value_filter_menu_switch)
        self.value_filter_menu.config(font=helv)
        self.value_filter_menu.grid(row=1, column=0, padx=1, pady=1)
        self.filter_a = tk.StringVar()
        self.entry_filter_a = tk.Entry(self.value_def_frame,textvariable=self.filter_a, font = helv, width = 15)
        self.widgets.append(self.entry_filter_a)
        self.entry_filter_a.grid(row=1, column=1, padx=1, pady=1)
        self.filter_b = tk.StringVar()
        self.entry_filter_b = tk.Entry(self.value_def_frame,textvariable=self.filter_b, font = helv, width = 15)
        self.widgets.append(self.entry_filter_b)
        self.entry_filter_b.grid(row=2, column=1, padx=1, pady=1)
        self.entry_filter_b.configure(state="disabled")
        self.b_value_filter = tk.Button(self.value_def_frame,text="Filter By Selected Value", command=self.value_filter_function)
        self.b_value_filter.grid(row=1, column=2, padx=1, pady=1)
        self.widgets.append(self.b_value_filter)
        self.b_reset_filter = tk.Button(self.value_def_frame,text="Reset Shape List", command=self.shape_change)
        self.b_reset_filter.grid(row=1, column=3, padx=1, pady=1)
        self.widgets.append(self.b_reset_filter)
        self.b_export_csv = tk.Button(self.value_def_frame,text="Export Current List to CSV", command=self.export_to_csv)
        self.b_export_csv.grid(row=2, column=2, padx=1, pady=1)
        self.widgets.append(self.b_export_csv)
        self.value_def_frame.pack(side=tk.LEFT, padx= 5, pady= 5)
        
        self.b_quit = tk.Button(self.base_frame,text="Quit", command=self.quit_app, font=helv)
        self.widgets.append(self.b_quit)
        self.b_quit.pack(side=tk.RIGHT)
        self.license_display()
    
    def license_display(self, *event):
        license_string = ("Copyright (c) 2019, Donald N. Bockoven III\n"
                            "All rights reserved.\n\n"
                            "THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\""
                            " AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE"
                            " IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE"
                            " DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE"
                            " FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL"
                            " DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR"
                            " SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER"
                            " CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,"
                            " OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE"
                            " OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n\n"
                            "https://github.com/buddyd16/Structural-Engineering/blob/master/LICENSE"
                            )
        tkMessageBox.showerror("License Information",license_string)
        self.master.focus_force()
        
    def value_filter_menu_switch(self, *event):
        option = self.value_filter.get()
        if option == 'Between':
            self.entry_filter_b.configure(state="normal")
        else:
            self.entry_filter_b.configure(state="disabled")
            
    def quit_app(self):
        self.master.destroy()
        self.master.quit()
    
    def shape_change(self, *event):
        self.shape_menu.delete(0,tk.END)
        new_shape_type = self.shape_type.get()
        new_shape_type_index = self.shape_types.index(new_shape_type)

        if new_shape_type_index == 2:
            d = self.shape_sets[new_shape_type_index]
            new_section_list = sorted(d, key=lambda k: (float(d[k][5]),(float(d[k][10])),(float(d[k][19]))))
            string = 'Section: - Sorted By: {0} then {1} then {2}'.format(self.values_list[5],self.values_list[10],self.values_list[19])
        elif new_shape_type_index == 3:
            d = self.shape_sets[new_shape_type_index]
            new_section_list = sorted(d, key=lambda k: (float(d[k][7]),(float(d[k][19]))))
            string = 'Section: - Sorted By: {0} then {1}'.format(self.values_list[7],self.values_list[19])
        elif new_shape_type_index == 6 or new_shape_type_index == 13:
            d = self.shape_sets[new_shape_type_index]
            new_section_list = sorted(d, key=lambda k: (float(d[k][11]),(float(d[k][3])),(float(d[k][18]))))
            string = 'Section: - Sorted By: {0} then {1} then {2}'.format(self.values_list[11],self.values_list[3],self.values_list[18])
        elif new_shape_type_index == 8:
            d = self.shape_sets[new_shape_type_index]
            new_section_list = sorted(d, key=lambda k: (float(d[k][1]),(float(d[k][12]))))
            string = 'Section: - Sorted By: {0} then {1}'.format(self.values_list[1],self.values_list[12])
        else:
            d = self.shape_sets[new_shape_type_index]
            new_section_list = sorted(d, key=lambda k: (float(d[k][3]),(float(d[k][1]))))
            string = 'Section: - Sorted By: {0} then {1}'.format(self.values_list[3],self.values_list[1])
        for section in new_section_list:
            self.shape_menu.insert(tk.END, section)
        self.shape_menu.selection_set(0)
        self.shape_click()
        self.shape_frame.configure(text=string)
    
    def shape_click(self, *event):
        shape = self.shape_menu.get(self.shape_menu.curselection())
        shape_index = self.shape_types.index(self.shape_type.get())
        section_props = self.shape_sets[shape_index].get(shape)

        if section_props[0] == 'F':
            self.data_frame.configure(text="Section Properties - AISC 14th Edition:  --  Selected Shape: "+shape)
        else:
            note = self.shape_special_note[shape_index]
            self.data_frame.configure(text="Section Properties - AISC 14th Edition:  --  Selected Shape: "+shape+" -- Note: "+note)
        for labels in self.properties_labels:
            labels.configure( text=' ')

        props_counter = 0
        props_list = []
        for i in range(1,len(self.values_list)):
            if section_props[i] == '-':
               pass
            else:
                if self.values_units[i] == '':
                    string = '{0}{1}:\n{2}'.format(self.values_list[i],self.values_units[i],section_props[i])
                else:
                    string = '{0}({1}):\n{2}'.format(self.values_list[i],self.values_units[i],section_props[i])
                    props_list.append(self.values_list[i])
                    
                self.properties_labels[props_counter].configure( text=string)                
                props_counter+=1

        self.value_def_menu.destroy()
        self.value_def_menu = tk.OptionMenu(self.value_def_frame, self.value_def, *props_list, command=self.value_definitions)
        helv = tkFont.Font(family='Helvetica',size=self.f_size, weight='bold')
        self.value_def_menu.config(font=helv)
        self.value_def_menu.grid(row=0, column=0, padx=1, pady=1)
        self.value_def.set(props_list[0])
        self.value_definitions()
    
    def font_size_up(self, *event):
        self.f_size = self.f_size+1
        helv = tkFont.Font(family='Helvetica',size=self.f_size, weight='bold')
        self.f_size_label.configure(text='Font Size ('+str(self.f_size)+'):')
        self.value_def_menu.config(font=helv)
        self.shape_type_menu.config(font=helv)
        self.value_filter_menu.config(font=helv)
        for widget in self.widgets:
            widget.configure(font=helv)
    
    def font_size_down(self, *event):
        if self.f_size-1 < 6:
            self.f_size = 6
        else:
            self.f_size = self.f_size-1
            
        helv = tkFont.Font(family='Helvetica',size=self.f_size, weight='bold')
        self.f_size_label.configure(text='Font Size ('+str(self.f_size)+'):')
        self.value_def_menu.config(font=helv)
        self.shape_type_menu.config(font=helv)
        self.value_filter_menu.config(font=helv)
        for widget in self.widgets:
            widget.configure(font=helv)
        
    def value_definitions(self, *event):
        index = self.values_list.index(self.value_def.get())
        self.value_def_label.configure(text = self.values_help[index])
    
    def value_filter_function(self, *event):
        value_index = self.values_list.index(self.value_def.get())
        a = self.filter_a.get()
        b = self.filter_b.get()
        filter_type = self.value_filter.get()
        self.shape_menu.delete(0,tk.END)
        
        new_shape_type = self.shape_type.get()
        new_shape_type_index = self.shape_types.index(new_shape_type)
        
        filtered_section_list = []

        if new_shape_type_index == 2:
            d = self.shape_sets[new_shape_type_index]
            new_section_list = sorted(d, key=lambda k: (float(d[k][value_index])))
        elif new_shape_type_index == 3:
            d = self.shape_sets[new_shape_type_index]
            new_section_list = sorted(d, key=lambda k: (float(d[k][value_index])))
        elif new_shape_type_index == 6 or new_shape_type_index == 13:
            d = self.shape_sets[new_shape_type_index]
            new_section_list = sorted(d, key=lambda k: (float(d[k][value_index])))
        elif new_shape_type_index == 8:
            d = self.shape_sets[new_shape_type_index]
            new_section_list = sorted(d, key=lambda k: (float(d[k][value_index])))
        else:
            d = self.shape_sets[new_shape_type_index]
            new_section_list = sorted(d, key=lambda k: (float(d[k][value_index])))
        
        if a == '':
            pass
        
        else:
            if filter_type == 'Between' and b == '':
                pass
                
            elif filter_type == 'Between':
                string = 'Section: - Sorted By: {0} Between {1} and {2}'.format(self.values_list[value_index],a,b)
                for key in new_section_list:
                    if float(a) > float(b):
                        a = self.filter_b.get()
                        b = self.filter_a.get()
                    else:
                        pass
                    if float(d[key][value_index]) >= float(a) and float(d[key][value_index]) <= float(b):
                        filtered_section_list.append(key)
                    else:
                        pass
            elif filter_type == '<':
                string = 'Section: - Sorted By: {0} < {1}'.format(self.values_list[value_index],a)
                for key in new_section_list:
                    if float(d[key][value_index]) <= float(a):
                        filtered_section_list.append(key)
                    else:
                        pass
            elif filter_type == '>':
                string = 'Section: - Sorted By: {0} > {1}'.format(self.values_list[value_index],a)
                for key in new_section_list:
                    if float(d[key][value_index]) >= float(a):
                        filtered_section_list.append(key)
                    else:
                        pass
            elif filter_type == '=':
                string = 'Section: - Sorted By: {0} = {1}'.format(self.values_list[value_index],a)
                for key in new_section_list:
                    if float(d[key][value_index]) == float(a):
                        filtered_section_list.append(key)
                    else:
                        pass
        if len(filtered_section_list) == 0:
            self.shape_menu.delete(0,tk.END)
            
        else:
            for section in filtered_section_list:
                 self.shape_menu.insert(tk.END, section)
        self.shape_frame.configure(text=string)

    def export_to_csv(self, *events):
        shapes = self.shape_menu.get(0,tk.END)
        shape_index = self.shape_types.index(self.shape_type.get())
        section_props = self.shape_sets[shape_index].get(shapes[0])
        string = 'Section'
        for i in range(1,len(self.values_list)):
            if section_props[i] == '-':
                pass
            else:
                if self.values_units[i] == '':
                    string =string+ ',{0}{1}:'.format(self.values_list[i],self.values_units[i])
                else:
                    string =string+ ',{0}({1}):'.format(self.values_list[i],self.values_units[i])

        export_file = open(self.shape_type.get()+'_sorted.csv','w')
        export_file.write(string)
        for shape in shapes:
            shape_string = '\n' + shape
            section_props = self.shape_sets[shape_index].get(shape)
            for i in range(1,len(self.values_list)):
                if section_props[i] == '-':
                    pass
                else:
                    if self.values_units[i] == '':
                        shape_string =shape_string+ ',{0}'.format(section_props[i])
                    else:
                        shape_string =shape_string+ ',{0}'.format(section_props[i])
            export_file.write(shape_string)
        export_file.close()

		
def main():
    root = tk.Tk()
    root.title("AISC 14th Edition - Shape Database")
    app = Master_window(root)
    root.minsize(800,600)
    root.mainloop()

if __name__ == '__main__':
    main()   

            

