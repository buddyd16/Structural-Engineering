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
import Tkinter as tk
import ttk
import tkFont
import welds_elastic_method as wem

class Master_window:

    def __init__(self, master):
        
        self.master = master
        
        self.weld_segments = []
        self.group_result_labels = []
        self.analysis_result_labels = []
        self.design_result_label = []
        self.group_built = 0
        self.forces_run = 0
        
        self.f_size = 8
        self.f_type = tkFont.Font(family=' Courier New',size=self.f_size)
        self.f_type_b_big = tkFont.Font(family=' Courier New',size=12, weight='bold')
        self.f_type_b = tkFont.Font(family=' Courier New',size=self.f_size, weight='bold')
        self.f_type_bu = tkFont.Font(family=' Courier New',size=self.f_size, weight='bold', underline = True)
        
        self.menubar = tk.Menu(self.master)
        self.menu = tk.Menu(self.menubar, tearoff=0)
        self.menu_props = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label = "File", menu=self.menu)
        self.menu.add_command(label="Quit", command=self.quit_app)
        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            self.master.tk.call(master, "config", "-menu", self.menubar)
        
        # Frames
        self.main_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.main_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        
        self.input_frame = tk.Frame(self.main_frame, bd=2, relief='sunken', padx=1,pady=1)
        self.input_frame.pack(side=tk.LEFT, anchor='ne', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        
        self.output_frame = tk.Frame(self.main_frame, bd=2, relief='sunken', padx=1,pady=1)
        self.output_frame.pack(side=tk.RIGHT, anchor='nw', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        
        self.output_canvas_frame = tk.Frame(self.output_frame, bd=2, relief='sunken', padx=1,pady=1)
        self.output_canvas_frame.pack(padx= 1, pady= 1)
        
        self.output_data_frame = tk.Frame(self.output_frame, bd=2, relief='sunken', padx=1,pady=1)
        self.output_data_frame.pack(padx= 1, pady= 1, fill=tk.X, expand=1)
        
        # Canvas
        self.weld_canvas = tk.Canvas(self.output_canvas_frame, width=300, height=300, bd=2, relief='sunken', background="black")
        self.weld_canvas.pack(side = tk.LEFT, anchor='c', padx= 1, pady= 1)
        self.weld_canvas.bind("<Configure>", self.draw_weld)
        
        # Input/output Notebooks
        self.nb_inputs = ttk.Notebook(self.input_frame)
        self.nb_inputs.pack(fill=tk.BOTH, expand=1)

        self.nb_output_data = ttk.Notebook(self.output_data_frame)
        self.nb_output_data.pack(fill=tk.BOTH, expand=1)
        
        # Input Notebooks
        self.tab_license  = ttk.Frame(self.nb_inputs)
        self.nb_inputs.add(self.tab_license , text='License')
        
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
                            
        tk.Label(self.tab_license, text=license_string,font=self.f_type, justify=tk.LEFT).grid(row=0, column=0)
        
        self.tab_geometry  = ttk.Frame(self.nb_inputs)
        self.nb_inputs.add(self.tab_geometry , text='Weld Group Geometry - Input')
        
        self.tab_loads = ttk.Frame(self.nb_inputs)
        self.nb_inputs.add(self.tab_loads , text='Applied Loads and Base Materials - Input')
        
        # Output Notebooks
        self.tab_group_properties  = ttk.Frame(self.nb_output_data, height=300)
        self.nb_output_data.add(self.tab_group_properties , text='Weld Group Properties')
        
        self.group_textbox = tk.Text(self.tab_group_properties, font=self.f_type)
        self.group_textbox.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
        
        self.tab_load_analysis  = ttk.Frame(self.nb_output_data, height=300)
        self.nb_output_data.add(self.tab_load_analysis , text='Load Analysis Results')
        
        self.load_textbox = tk.Text(self.tab_load_analysis, font=self.f_type)
        self.load_textbox.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
        
        self.load_scroll = tk.Scrollbar(self.tab_load_analysis, command=self.load_textbox.yview)
        self.load_scroll.grid(row=0, column=1, sticky='ns')
        self.load_textbox['yscrollcommand'] = self.load_scroll.set
        
        self.tab_aisc_design = ttk.Frame(self.nb_output_data, height=300)
        self.nb_output_data.add(self.tab_aisc_design , text='AISC Design')
        
        self.aisc_textbox = tk.Text(self.tab_aisc_design, font=self.f_type)
        self.aisc_textbox.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
        
        self.aisc_scroll = tk.Scrollbar(self.tab_aisc_design, command=self.aisc_textbox.yview)
        self.aisc_scroll.grid(row=0, column=1, sticky='ns')
        self.aisc_textbox['yscrollcommand'] = self.aisc_scroll.set
        
        self.geometry_input_gui()
        self.loads_base_material_input_gui()

    def geometry_input_gui(self):
        tk.Label(self.tab_geometry, text="Weld Segment:", font=self.f_type_b).grid(row=0,column=0, sticky = tk.W)
        
        tk.Label(self.tab_geometry, text="Start x (in):", font=self.f_type).grid(row=1,column=0, sticky = tk.E)
        self.start_x_in = tk.StringVar()
        tk.Entry(self.tab_geometry, textvariable=self.start_x_in, width=10).grid(row=1,column=1, sticky = tk.W)
        
        tk.Label(self.tab_geometry, text="Start y (in):", font=self.f_type).grid(row=1,column=2, sticky = tk.E, padx=5)
        self.start_y_in = tk.StringVar()
        tk.Entry(self.tab_geometry, textvariable=self.start_y_in, width=10).grid(row=1,column=3, sticky = tk.W)
        
        tk.Label(self.tab_geometry, text="End x (in):", font=self.f_type).grid(row=2,column=0, sticky = tk.E)
        self.end_x_in = tk.StringVar()
        tk.Entry(self.tab_geometry, textvariable=self.end_x_in, width=10).grid(row=2,column=1, sticky = tk.W)
        
        tk.Label(self.tab_geometry, text="End y (in):", font=self.f_type).grid(row=2,column=2, sticky = tk.E, padx=5)
        self.end_y_in = tk.StringVar()
        tk.Entry(self.tab_geometry, textvariable=self.end_y_in, width=10).grid(row=2,column=3, sticky = tk.W)
        
        self.add_segment_button = tk.Button(self.tab_geometry,text = "Add Weld Segment", command = self.add_segment, font=self.f_type_b)
        self.add_segment_button.grid(row=1,column=4, padx=5)
        
        self.remove_last_segment_button = tk.Button(self.tab_geometry,text = "Remove Last\nWeld Segment", command = self.remove_last_segment, font=self.f_type_b)
        self.remove_last_segment_button.grid(row=2,column=4, padx=5)
        
        self.remove_all_segment_button = tk.Button(self.tab_geometry,text = "Remove All\nWeld Segments", command = self.remove_all, font=self.f_type_b)
        self.remove_all_segment_button.grid(row=3,column=4, padx=5)
        
        tk.Label(self.tab_geometry, text="Weld Segment List:", font=self.f_type_b).grid(row=3,column=0, sticky = tk.W)
        self.segment_list_scrollbar = tk.Scrollbar(self.tab_geometry, orient="vertical", command=self.segment_list_scroll)
        self.segment_list_scrollbar.grid(row=4, column=6, sticky='wns', pady=10)
        
        self.segment_list = tk.Listbox(self.tab_geometry, height = 30, width = 130, font=self.f_type, yscrollcommand=self.segment_list_scrollbar.set)
        self.segment_list.grid(row=4, column=0, columnspan=6, sticky='nsew', pady=10)
        
        segment_label_key = """i = weld start coord.  j = segment end coord.  A = segment area = segment length\nIxo = x-axis moment of inertia about segment center   Iyo = y-axis moment of inertia about segment center\nCenter = segment center coords.   Cx = x distance to group centroid   Cy = y distance to group centroid\nIx = x-axis moment of inertia about  group center   Iy = y-axis moment of inertia about group center"""
                                   
        tk.Label(self.tab_geometry, text=segment_label_key, font=self.f_type, justify=tk.LEFT).grid(row=5,column=0,columnspan=6, sticky = tk.W, padx=5)
        
        self.add_circle_button = tk.Button(self.tab_geometry, text='Add a Circular Weld', command = self.add_circle_function, font=self.f_type_b)
        self.add_circle_button.grid(row=0,column=5, sticky = tk.W, padx=5)
        tk.Label(self.tab_geometry, text='center x (in):',font=self.f_type).grid(row=1,column=5, sticky = tk.E, padx=5)
        tk.Label(self.tab_geometry, text='center y (in):',font=self.f_type).grid(row=2,column=5, sticky = tk.E, padx=5)
        tk.Label(self.tab_geometry, text='radius (in):',font=self.f_type).grid(row=3,column=5, sticky = tk.E, padx=5)
        tk.Label(self.tab_geometry, text='start (deg.):',font=self.f_type).grid(row=1,column=7, sticky = tk.E, padx=5)
        tk.Label(self.tab_geometry, text='end (deg.):',font=self.f_type).grid(row=2,column=7, sticky = tk.E, padx=5)
        
        self.add_circle_ins = [tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()]
        
        i=0
        for circle_info in self.add_circle_ins:
            r = 1+i
            if r<4:
                tk.Entry(self.tab_geometry, textvariable=circle_info, width=10).grid(row=r,column=6, sticky = tk.W)
            else:
                tk.Entry(self.tab_geometry, textvariable=circle_info, width=10).grid(row=r-3,column=8, sticky = tk.W)
            i+=1

    def loads_base_material_input_gui(self):
        tk.Label(self.tab_loads, text="** All Loads Assumed to Act at the Weld Group Centroid**", font=self.f_type_b_big).grid(row=0,column=0,columnspan=6, sticky = tk.W)
        tk.Label(self.tab_loads, text="Loading:", font=self.f_type_b).grid(row=1,column=0, sticky = tk.W)
        tk.Label(self.tab_loads, text="Materials:", font=self.f_type_b).grid(row=1,column=3, sticky = tk.W)
        
        load_labels = ['Fz (lbs)= \nAxial', 'Fx (lbs)= \nShear X', 'Fy (lbs)= \nShear Y', 'Mx (in-lbs)= \nMoment About X', 'My (in-lbs)= \nMoment About Y', 'Mz = (in-lbs)\nMoment About Z']
        self.loads_in = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        
        for load in self.loads_in:
            load.set('0.00')
        
        i=0
        for label, load in zip(load_labels, self.loads_in):
            current_load_row_count = 2+i
            tk.Label(self.tab_loads, text=label, font=self.f_type, justify=tk.RIGHT).grid(row=current_load_row_count,column=0, sticky = tk.E)
            tk.Entry(self.tab_loads, textvariable=load, width=20).grid(row=current_load_row_count,column=1, sticky = tk.W)
            i+=1
            
        material_labels = ['Fexx,weld (ksi)= ','Fy,base 1 (ksi) = ','Fu,base 1 (ksi)= ','t,base 1 (in) = ','Fy,base 2 (ksi) = ','Fu,base 2 (ksi)= ','t,base 2 (in) = ']
        self.material_in = [tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()]
        
        default_material = ['70.00','36.00','58.00','0.375','36.00','58.00','0.375']
        for material, default in zip(self.material_in, default_material):
            material.set(default)
        
        y=0
        for material_label, material in zip(material_labels,self.material_in):
            current_material_row_count = 2+y
            tk.Label(self.tab_loads, text=material_label, font=self.f_type, justify=tk.RIGHT).grid(row=current_material_row_count,column=3, sticky = tk.E)
            tk.Entry(self.tab_loads, textvariable=material, width=15).grid(row=current_material_row_count,column=4, sticky = tk.W)
            y+=1
        
        self.run_analysis_button = tk.Button(self.tab_loads,text = "Run Analysis (Quadrant)", command = self.force_analysis, font=self.f_type_b)
        self.run_analysis_button.grid(row=current_load_row_count+1, column=0, columnspan=2, pady=10)
        
        self.run_analysis_segment_button = tk.Button(self.tab_loads,text = "Run Analysis (Segment)", command = self.force_analysis_segment, font=self.f_type_b)
        self.run_analysis_segment_button.grid(row=current_load_row_count+2, column=0, columnspan=2, pady=10)
        
        self.run_analysis_conservative_button = tk.Button(self.tab_loads,text = "Run Analysis (Conservative)", command = self.force_analysis_conservative, font=self.f_type_b)
        self.run_analysis_conservative_button.grid(row=current_load_row_count+3, column=0, columnspan=2, pady=10)
        
        self.design_asd = tk.IntVar()
        tk.Checkbutton(self.tab_loads , text=' : Loads are Nominal (ASD)', variable=self.design_asd, font=self.f_type_b).grid(row=current_material_row_count+1, column=4, sticky = tk.W)
        
        self.run_design_button = tk.Button(self.tab_loads,text = "Run AISC Design", command = self.aisc_design, font=self.f_type_b)
        self.run_design_button.grid(row=current_material_row_count+2, column=3, columnspan=2, pady=10)
        
    def quit_app(self):
        self.master.destroy()
        self.master.quit()
        
    def segment_list_scroll(self, *args):
        self.segment_list.yview(*args)
        
    def add_segment(self):
        x0 = float(self.start_x_in.get())
        y0 = float(self.start_y_in.get())
        x1 = float(self.end_x_in.get())
        y1 = float(self.end_y_in.get())
        start = [x0,y0]
        end = [x1,y1]
        weld = wem.weld_segment(start,end)
        
        self.weld_segments.append(weld)
        self.build_weld_group()
        
        self.fill_segment_list()
    
    def remove_last_segment(self):
        del self.weld_segments[-1]
        self.build_weld_group()
        self.fill_segment_list()
       
    def remove_all(self):
        del self.weld_segments[:]
        self.segment_list.delete(0,tk.END)
    
    def fill_segment_list(self):
        color = "pale green"
        self.segment_list.delete(0,tk.END)
       
        i=0
        for segment in self.weld_segments:
            self.segment_list.insert(tk.END, segment.info_text+segment.global_info_text)
            if i % 2 == 0:
                self.segment_list.itemconfigure(i, background=color)
            else:
                pass
            i+=1
        self.draw_weld()
    
    def draw_weld(self,*event):
        self.weld_canvas.delete("all")
        w = self.weld_canvas.winfo_width()
        h = self.weld_canvas.winfo_height()
        
        # x y arrows
        coord_start = 10
        self.weld_canvas.create_line(coord_start,h-coord_start,coord_start+50,h-coord_start, fill='green', width=1, arrow=tk.LAST)
        self.weld_canvas.create_text(coord_start+50,h-(coord_start+8), text='x', fill='green')
        self.weld_canvas.create_line(coord_start,h-coord_start,coord_start,h-(coord_start+50), fill='green', width=1, arrow=tk.LAST)
        self.weld_canvas.create_text(coord_start+8,h-(coord_start+50), text='y', fill='green')
        
        if len(self.weld_segments)<1:
            pass
        else:
            min_x = min(min([weld.start[0] for weld in self.weld_segments]), min([weld.end[0] for weld in self.weld_segments]))
            min_y = min(min([weld.start[1] for weld in self.weld_segments]), min([weld.end[1] for weld in self.weld_segments]))
            
            max_x = max(max([weld.start[0] for weld in self.weld_segments]), max([weld.end[0] for weld in self.weld_segments])) - min_x
            max_y = max(max([weld.start[1] for weld in self.weld_segments]), max([weld.end[1] for weld in self.weld_segments])) - min_y
            
            max_dim_for_scale = max(max_x, max_y)
           
            initial = 50
           
            
            if max_x == 0:
                sf_x = (w - (2*initial))
            else:
                sf_x = (w - (2*initial)) / max_dim_for_scale
            
            if max_y == 0:
                sf_y = (h - (2*initial))
            else:
                sf_y = (h - (2*initial)) / max_dim_for_scale
            
            for weld in self.weld_segments:
                x0 = ((weld.x_coords[0] - min_x) * sf_x) + initial
                y0 = h - (((weld.y_coords[0] - min_y) * sf_y) + initial)
                x1 = ((weld.x_coords[1] - min_x) * sf_x) + initial
                y1 = h - (((weld.y_coords[1] - min_y) * sf_y) + initial)
                
                self.weld_canvas.create_line(x0,y0,x1,y1, fill='red', width=2)
            
            if self.group_built == 1:
                
                xc = ((self.weld_group.group_center[0] - min_x) * sf_x) + initial
                yc = h - (((self.weld_group.group_center[1]-min_y) * sf_y) + initial)
                
                extension = initial/2
                self.weld_canvas.create_line(extension,yc,w-extension,yc, fill='blue', width=1, dash=(6,6))
                self.weld_canvas.create_line(xc,h-extension,xc,extension, fill='blue', width=1, dash=(6,6))
    
    def build_weld_group(self):
        if len(self.weld_segments) > 1:
            del self.group_result_labels[:]
            self.weld_group = wem.elastic_weld_group(self.weld_segments)
            self.group_built = 1
            self.group_textbox.delete(1.0,tk.END)
            i=0
            for label, equation, value in zip(self.weld_group.gui_output_labels,self.weld_group.gui_output_equations,self.weld_group.gui_output_values):
                self.group_textbox.insert(tk.END,'{0}{1}{2:.3f}\n'.format(label, equation, value))
                i+=1
            self.draw_weld()
        else:
            self.group_built = 0
    
    def force_analysis(self):
        del self.analysis_result_labels[:]
        forces = []
        for load in self.loads_in:
            forces.append(float(load.get()))
        if self.group_built == 1:
            self.weld_group.force_analysis(forces[0],forces[1],forces[2],forces[3],forces[4],forces[5])
            self.forces_run = 1
            self.resultant = self.weld_group.resultant
            self.load_textbox.delete(1.0,tk.END)
            i=0
            for label, equation, value in zip(self.weld_group.component_forces_key,self.weld_group.component_forces_eqs,self.weld_group.component_forces):
                self.load_textbox.insert(tk.END,'{0} = {1} = {2:.3f} lbs/in\n'.format(label, equation, value))
                i+=1
                
    def force_analysis_segment(self):
        forces = []
        for load in self.loads_in:
            forces.append(float(load.get()))
        if self.group_built == 1:
            self.weld_group.force_analysis_segment(forces[0],forces[1],forces[2],forces[3],forces[4],forces[5])
            self.forces_run = 1
            self.resultant = self.weld_group.segment_resultant
            self.load_textbox.delete(1.0,tk.END)
            self.load_textbox.insert(tk.END,'Resultant = {0:.3f} \n'.format(self.resultant))
            
            for label, result in zip(self.weld_group.gui_forces_segment,self.weld_group.gui_forces_stresses):
                self.load_textbox.insert(tk.END,'{0} : {1}\n'.format(label, result))
            
    def force_analysis_conservative(self):
        del self.analysis_result_labels[:]
        forces = []
        for load in self.loads_in:
            forces.append(float(load.get()))
        if self.group_built == 1:
            self.weld_group.force_analysis_conservative(forces[0],forces[1],forces[2],forces[3],forces[4],forces[5])
            self.forces_run = 1
            self.resultant = self.weld_group.resultant_conservative
            self.load_textbox.delete(1.0,tk.END)
            i=0
            for label, equation, value in zip(self.weld_group.component_forces_key_conservative,self.weld_group.component_forces_eqs_conservative,self.weld_group.component_forces_conservative):
                self.load_textbox.insert(tk.END,'{0} = {1} = {2:.3f} lbs/in\n'.format(label, equation, value))
                i+=1
            
    def aisc_design(self):
        if self.group_built == 1 and self.forces_run == 1:
            resultant = self.resultant
            Fexx = 1000 * float(self.material_in[0].get())
            Fy_base1 = 1000 * float(self.material_in[1].get())
            Fu_base1 = 1000 * float(self.material_in[2].get())
            base_thickness1 = float(self.material_in[3].get())
            Fy_base2 = 1000 * float(self.material_in[4].get())
            Fu_base2 =1000 * float(self.material_in[5].get())
            base_thickness2= float(self.material_in[6].get())
            asd = self.design_asd.get()
            self.weld_group.aisc_weld_check(resultant,Fexx, Fy_base1, Fu_base1, base_thickness1, Fy_base2, Fu_base2, base_thickness2, asd)
            self.aisc_textbox.delete(1.0,tk.END)
            self.aisc_textbox.insert(tk.END, self.weld_group.aisclog)

    def add_circle_function(self):
        x = float(self.add_circle_ins[0].get())
        y = float(self.add_circle_ins[1].get())
        r = float(self.add_circle_ins[2].get())
        start = int(self.add_circle_ins[3].get())
        end = int(self.add_circle_ins[4].get())
        
        for a in range(start,end):
            x0 = r*math.cos(math.radians(a))
            y0 = r*math.sin(math.radians(a))
            x1 = r*math.cos(math.radians(a+1))
            y1 = r*math.sin(math.radians(a+1))
            
            start = [x0+x,y0+y]
            end = [x1+x,y1+y]
            weld = wem.weld_segment(start,end)
        
            self.weld_segments.append(weld)
            
        self.build_weld_group()
        
        self.fill_segment_list()
            
def main():
    root = tk.Tk()
    root.title("Elastic Weld Analysis and AISC Design - Alpha v1")
    Master_window(root)
    root.minsize(1280,720)
    root.mainloop()

if __name__ == '__main__':
    main()  