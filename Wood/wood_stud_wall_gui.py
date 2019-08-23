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
import tkMessageBox
import ttk
import tkFont
import wood_classes as wood
import matplotlib
matplotlib.use('TKAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkFileDialog
import os
import math

class Master_window:

    def __init__(self, master):
        self.master = master
        self.f_size = 8
        helv = tkFont.Font(family='Helvetica',size=self.f_size, weight='bold')
        self.menubar = tk.Menu(self.master)
        self.menu = tk.Menu(self.menubar, tearoff=0)
        self.menu_props = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label = "File", menu=self.menu)
        self.menu.add_command(label="Open", command=self.file_open)
        self.menu.add_separator()
        self.menu.add_command(label="Calc", command=self.run)
        self.menu.add_command(label="Build P-lateral Pressure", command=self.generate_interaction_graph)
        self.menu.add_command(label="Build P-M Chart", command=self.generate_pm_graph)
        self.menu.add_separator()
        self.menu.add_command(label="Quit", command=self.quit_app)
        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            self.master.tk.call(master, "config", "-menu", self.menubar)

        #Main Frames
        self.main_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.main_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        self.base_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.base_frame.pack(side=tk.BOTTOM, padx= 1, pady= 1, fill=tk.X, expand=1)
        
        self.nb = ttk.Notebook(self.main_frame)
        self.nb.pack(fill=tk.BOTH, expand=1)
        
        #Tab 1
        self.page1 = ttk.Frame(self.nb)
        self.nb.add(self.page1, text='Wall and Stud Information and Inputs - Find Axial Capacity Per Stud')
        
        self.pg1_frame = tk.Frame(self.page1, bd=2, relief='sunken', padx=1,pady=1)
        self.pg1_frame.pack(fill=tk.BOTH,expand=1, padx=2, pady=2)
        
        #user input frame
        self.input_frame = tk.LabelFrame(self.pg1_frame, text="Inputs", bd=2, relief='sunken', padx=2, pady=2, font=helv)
        
        #Wall Geometry Frame
        self.geo_frame = tk.LabelFrame(self.input_frame, text="Wall Stud Geometry: ", bd=2, relief='sunken', padx=2, pady=2, font=helv)

        #stud dimensions - nominal
        tk.Label(self.geo_frame, text='Nominal Stud Size:', font=helv).grid(row=1,column=1)
        self.b_nom = tk.StringVar()
        self.b_nom.set('2')
        self.b_nom_selection = tk.OptionMenu(self.geo_frame, self.b_nom, '2','3','4','(2)2','(3)2', command=self.actual_stud_size)
        self.b_nom_selection.grid(row=2,column=1)
        tk.Label(self.geo_frame, text='x', font=helv).grid(row=2,column=2)
        self.d_nom = tk.StringVar()
        self.d_nom.set('6')
        self.d_nom_selection = tk.OptionMenu(self.geo_frame, self.d_nom, '3','4','5','6','8','10','12','14','16', command=self.actual_stud_size)
        self.d_nom_selection.grid(row=2,column=3)
        
        #stud dimensions - actual
        tk.Label(self.geo_frame, text='Actual Stud Size:', font=helv).grid(row=1,column=4)
        self.b_actual_label = tk.Label(self.geo_frame, text='1.5', font=helv)
        self.b_actual_label.grid(row=2,column=4)
        tk.Label(self.geo_frame, text='x', font=helv).grid(row=2,column=5)
        self.d_actual_label = tk.Label(self.geo_frame, text='5.5', font=helv)
        self.d_actual_label.grid(row=2,column=6)
        
        #stud Spacing
        self.spacing_label = tk.Label(self.geo_frame, text='Stud Spacing: ', font=helv)
        self.spacing_label.grid(row=3,column=1, sticky=tk.E)
        self.stud_spacing = tk.StringVar()
        self.stud_spacing.set('16')
        self.spacing_entry = tk.Entry(self.geo_frame, textvariable=self.stud_spacing, width=10, font=helv)
        self.spacing_entry.grid(row=3,column=2, sticky=tk.W)
        tk.Label(self.geo_frame, text='in', font=helv).grid(row=3,column=3)
        
        #Wall Height
        self.height_label = tk.Label(self.geo_frame, text='Wall Height: ', font=helv)
        self.height_label.grid(row=4,column=1, sticky=tk.E)
        self.wall_height = tk.StringVar()
        self.wall_height.set('10')
        self.height_entry = tk.Entry(self.geo_frame, textvariable=self.wall_height, width=10, font=helv)
        self.height_entry.grid(row=4,column=2, sticky=tk.W)
        tk.Label(self.geo_frame, text='ft', font=helv).grid(row=4,column=3)
        
        #subtract wall plates from height
        self.sub_plates = tk.IntVar()
        tk.Checkbutton(self.geo_frame, text=': Subtract Wall Plates from Height (y/n)', variable=self.sub_plates, font=helv).grid(row=3, column=4, sticky=tk.W)
        self.plates_label = tk.Label(self.geo_frame, text='# of 1.5" Plates to subtract: ', font=helv)
        self.plates_label.grid(row=4,column=4, sticky=tk.E)        
        self.num_plates = tk.StringVar()
        self.num_plates.set(0)
        self.num_plates_entry = tk.Entry(self.geo_frame, textvariable=self.num_plates, width=5, font=helv)
        self.num_plates_entry.grid(row=4,column=5, sticky=tk.W)
        
        #Consider plate crushing for common capacities
        self.consider_crushing = tk.IntVar()
        tk.Checkbutton(self.geo_frame, text=': Consider plate crushing for common capacities (y/n)', variable=self.consider_crushing, font=helv).grid(row=5, column=4, sticky=tk.W)
        
        self.geo_frame.pack(fill=tk.X, padx=2, pady=2)
        
        #Reference Stud Design Values - Frame
        self.ref_stud_properties_frame = tk.LabelFrame(self.input_frame, text="Reference Stud Design Values : ", bd=2, relief='sunken', padx=2, pady=2, font=helv)
        
        #Wall Stud Grade
        self.grade_label = tk.Label(self.ref_stud_properties_frame,text = 'Grade :', font=helv)
        self.grade_label.grid(row=1, column=1, sticky=tk.E)
        self.grade = tk.StringVar()
        self.grade.set('No.1/No.2')
        grades = ['Select Structural','No.1 & Better','No.1/No.2','No.1','No.2','No.3','Stud','Construction','Utility']
        self.grade_selection = tk.OptionMenu(self.ref_stud_properties_frame, self.grade, *grades)
        self.grade_selection.grid(row=1,column=2)        
        
        #Fb
        self.fb_label = tk.Label(self.ref_stud_properties_frame,text = 'Fb :', font=helv)
        self.fb_label.grid(row=2, column=1, sticky=tk.E)
        self.fb_psi = tk.StringVar()
        self.fb_psi.set(875)
        self.fb_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.fb_psi, width=10, font=helv)
        self.fb_entry.grid(row=2, column=2, sticky=tk.W)
        tk.Label(self.ref_stud_properties_frame, text='psi', font=helv).grid(row=2,column=3, sticky=tk.W)
        
        #Fv
        self.fv_label = tk.Label(self.ref_stud_properties_frame,text = 'Fv :', font=helv)
        self.fv_label.grid(row=3, column=1, sticky=tk.E)
        self.fv_psi = tk.StringVar()
        self.fv_psi.set(135)
        self.fv_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.fv_psi, width=10, font=helv)
        self.fv_entry.grid(row=3, column=2, sticky=tk.W)
        tk.Label(self.ref_stud_properties_frame, text='psi', font=helv).grid(row=3,column=3, sticky=tk.W)

        #Fc
        self.fc_label = tk.Label(self.ref_stud_properties_frame,text = 'Fc :', font=helv)
        self.fc_label.grid(row=4, column=1, sticky=tk.E)
        self.fc_psi = tk.StringVar()
        self.fc_psi.set(1150)
        self.fc_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.fc_psi, width=10, font=helv)
        self.fc_entry.grid(row=4, column=2, sticky=tk.W)
        tk.Label(self.ref_stud_properties_frame, text='psi', font=helv).grid(row=4,column=3, sticky=tk.W) 

        #E
        self.E_label = tk.Label(self.ref_stud_properties_frame,text = 'E :', font=helv)
        self.E_label.grid(row=5, column=1, sticky=tk.E)
        self.E_psi = tk.StringVar()
        self.E_psi.set(1400000)
        self.E_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.E_psi, width=15, font=helv)
        self.E_entry.grid(row=5, column=2, sticky=tk.W)
        tk.Label(self.ref_stud_properties_frame, text='psi', font=helv).grid(row=5,column=3, sticky=tk.W)

        #Emin
        self.Emin_label = tk.Label(self.ref_stud_properties_frame,text = 'Emin :', font=helv)
        self.Emin_label.grid(row=6, column=1, sticky=tk.E)
        self.Emin_psi = tk.StringVar()
        self.Emin_psi.set(510000)
        self.Emin_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.Emin_psi, width=15, font=helv)
        self.Emin_entry.grid(row=6, column=2, sticky=tk.W)
        tk.Label(self.ref_stud_properties_frame, text='psi', font=helv).grid(row=6,column=3, sticky=tk.W)
        
        #Fc_perp_pl
        self.fc_perp_label = tk.Label(self.ref_stud_properties_frame,text = 'Fc_perp,bottom pl :', font=helv)
        self.fc_perp_label.grid(row=7, column=1, sticky=tk.E)
        self.fc_perp_psi = tk.StringVar()
        self.fc_perp_psi.set(425)
        self.fc_perp_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.fc_perp_psi, width=10, font=helv)
        self.fc_perp_entry.grid(row=7, column=2, sticky=tk.W)
        tk.Label(self.ref_stud_properties_frame, text='psi', font=helv).grid(row=7,column=3, sticky=tk.W)
        
        #FRT?
        self.frt_yn = tk.IntVar()
        tk.Checkbutton(self.ref_stud_properties_frame, text=': FRT (y/n)', variable=self.frt_yn, font=helv).grid(row=1, column=4)
        self.frt_fb_label = tk.Label(self.ref_stud_properties_frame,text = 'Cfrt,fb :', font=helv)
        self.frt_fb_label.grid(row=2,column=4, sticky=tk.E)
        self.frt_fb = tk.StringVar()
        self.frt_fb.set(0.88)
        self.frt_fb_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.frt_fb, width=10, font=helv)
        self.frt_fb_entry.grid(row=2,column=5, sticky=tk.W)
        self.frt_fv_label = tk.Label(self.ref_stud_properties_frame,text = 'Cfrt,fv :', font=helv)
        self.frt_fv_label.grid(row=3,column=4, sticky=tk.E)
        self.frt_fv = tk.StringVar()
        self.frt_fv.set(0.93)
        self.frt_fv_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.frt_fv, width=10, font=helv)
        self.frt_fv_entry.grid(row=3,column=5, sticky=tk.W)
        self.frt_fc_label = tk.Label(self.ref_stud_properties_frame,text = 'Cfrt,fc :', font=helv)
        self.frt_fc_label.grid(row=4,column=4, sticky=tk.E)
        self.frt_fc = tk.StringVar()
        self.frt_fc.set(0.94)
        self.frt_fc_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.frt_fc, width=10, font=helv)
        self.frt_fc_entry.grid(row=4,column=5, sticky=tk.W)
        self.frt_fc_perp_label = tk.Label(self.ref_stud_properties_frame,text = 'Cfrt,fc_perp :', font=helv)
        self.frt_fc_perp_label.grid(row=5,column=4, sticky=tk.E)
        self.frt_fc_perp = tk.StringVar()
        self.frt_fc_perp.set(0.95)
        self.frt_fc_perp_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.frt_fc_perp, width=10, font=helv)
        self.frt_fc_perp_entry.grid(row=5,column=5, sticky=tk.W)
        self.frt_E_label = tk.Label(self.ref_stud_properties_frame,text = 'Cfrt,E :', font=helv)
        self.frt_E_label.grid(row=6,column=4, sticky=tk.E)
        self.frt_E = tk.StringVar()
        self.frt_E.set(0.94)
        self.frt_E_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.frt_E, width=10, font=helv)
        self.frt_E_entry.grid(row=6,column=5, sticky=tk.W)
        self.frt_Emin_label = tk.Label(self.ref_stud_properties_frame,text = 'Cfrt,Emin :', font=helv)
        self.frt_Emin_label.grid(row=7,column=4, sticky=tk.E)
        self.frt_Emin = tk.StringVar()
        self.frt_Emin.set(0.94)
        self.frt_Emin_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.frt_Emin, width=10, font=helv)
        self.frt_Emin_entry.grid(row=7,column=5, sticky=tk.W)         
        
        self.species_label = tk.Label(self.ref_stud_properties_frame,text = 'Species :', font=helv)
        self.species_label.grid(row=8,column=1, sticky=tk.E)
        self.species = tk.StringVar()
        self.species.set('Spruce-Pine-Fur')
        self.species_entry = tk.Entry(self.ref_stud_properties_frame, textvariable=self.species, width=50, font=helv)
        self.species_entry.grid(row=8,column=2,columnspan=3)
        
        self.is_syp = tk.IntVar()
        tk.Checkbutton(self.ref_stud_properties_frame, text=': Southern Pine (y/n)', variable=self.is_syp, font=helv).grid(row=8, column=5)
        
        self.ref_stud_properties_frame.pack(fill=tk.X, padx=2, pady=2)
        
        self.enviro_treatment_frame = tk.LabelFrame(self.input_frame, text="Enviroment and Treatment : ", bd=2, relief='sunken', padx=2, pady=2, font=helv)
        
        #Moisture %
        self.moisture_label = tk.Label(self.enviro_treatment_frame,text = 'Moisture % :', font=helv)
        self.moisture_label.grid(row=1,column=1, sticky=tk.E)
        self.moisture = tk.StringVar()
        self.moisture.set(19.0)
        self.moisture_entry = tk.Entry(self.enviro_treatment_frame, textvariable=self.moisture, width=10, font=helv)
        self.moisture_entry.grid(row=1,column=2, sticky=tk.W)   
        
        #Temp F
        self.temp_label = tk.Label(self.enviro_treatment_frame,text = 'Temperature (F) - <= 150 :', font=helv)
        self.temp_label.grid(row=2,column=1, sticky=tk.E)
        self.temp = tk.StringVar()
        self.temp.set(90.0)
        self.temp_entry = tk.Entry(self.enviro_treatment_frame, textvariable=self.temp, width=10, font=helv)
        self.temp_entry.grid(row=2,column=2, sticky=tk.W)
        
        #Incised?
        self.incised_yn = tk.IntVar()
        tk.Checkbutton(self.enviro_treatment_frame, text=': Incised (y/n)', variable=self.incised_yn, font=helv).grid(row=3, column=1, sticky=tk.W)       
        
        self.enviro_treatment_frame.pack(fill=tk.X, padx=2, pady=2)

        self.lateral_frame = tk.LabelFrame(self.input_frame, text="Lateral Pressure : ", bd=2, relief='sunken', padx=2, pady=2, font=helv) 
        
        #Pressure
        self.pressure_label = tk.Label(self.lateral_frame,text = 'Pressure (psf) :', font=helv)
        self.pressure_label.grid(row=1,column=1, sticky=tk.E)
        self.pressure = tk.StringVar()
        self.pressure.set("5.0")
        self.pressure_entry = tk.Entry(self.lateral_frame, textvariable=self.pressure, width=10, font=helv)
        self.pressure_entry.grid(row=1,column=2, sticky=tk.W)
        
        #Cd
        self.cd_label = tk.Label(self.lateral_frame,text = 'Cd :', font=helv)
        self.cd_label.grid(row=2,column=1, sticky=tk.E)
        self.cd = tk.StringVar()
        self.cd.set('1.0')
        cds = ['0.9','1.0','1.15','1.25','1.6','2.0']
        self.cd_selection = tk.OptionMenu(self.lateral_frame, self.cd, *cds)
        self.cd_selection.grid(row=2, column=2)
        
        #Min Eccentricity?
        self.min_ecc_yn = tk.IntVar()
        tk.Checkbutton(self.lateral_frame, text=': Min. Eccentricty of d/6 (y/n)', variable=self.min_ecc_yn, font=helv).grid(row=3, column=1, sticky=tk.W) 
        
        #Stud Lateral Braced on Compression Face
        self.com_lat_brace_yn = tk.IntVar()
        self.com_lat_brace_yn.set(1)
        tk.Checkbutton(self.lateral_frame, text=': Stud laterally braced on compression face (y/n)', variable=self.com_lat_brace_yn, command=self.com_lat_brace_func, font=helv).grid(row=4, column=1, sticky=tk.W)
        self.no_sheathing_yn = tk.IntVar()
        self.no_sheathing_yn.set(0)
        tk.Checkbutton(self.lateral_frame, text=': No Sheathing (y/n)', variable=self.no_sheathing_yn, command=self.no_sheating_func, font=helv).grid(row=5, column=1, sticky=tk.W)
        self.blocking_label = tk.Label(self.lateral_frame, text = 'Blocking (ft):', font=helv).grid(row=6, column=1, sticky=tk.E)
        self.blocking_ft = tk.StringVar()
        self.blocking_ft.set("4.0")
        self.blocking_entry = tk.Entry(self.lateral_frame, textvariable = self.blocking_ft, width=10, font=helv)
        self.blocking_entry.grid(row=6, column=2)
        self.lateral_frame.pack(fill=tk.X, padx=2, pady=2)
        
        self.b_run = tk.Button(self.input_frame,text="Calc", command=self.run, font=helv)
        self.b_run.pack(side=tk.RIGHT)
        self.b_build_chart = tk.Button(self.input_frame,text="Build P-Lateral Pressure Chart", command=self.generate_interaction_graph, font=helv, state = tk.DISABLED)
        self.b_build_chart.pack(side=tk.RIGHT)
        self.b_build_pm = tk.Button(self.input_frame,text="Build P-M Chart", command=self.generate_pm_graph, font=helv, state = tk.DISABLED)
        self.b_build_pm.pack(side=tk.RIGHT) 
        
        self.input_frame.pack(side=tk.LEFT, padx=2, pady=2)
                
        #results frame
        self.results_frame = tk.LabelFrame(self.pg1_frame, text="Results", bd=2, relief='sunken', padx=2, pady=2)
        self.nds_table_frame = tk.LabelFrame(self.results_frame, text="NDS 2005 - Table 4.3.1", bd=2, relief='sunken', padx=2, pady=2)
        self.res_labels = []
        self.res_nds_table_output = []
        for y in range(0,7):
            for i in range(0,16):
                label = tk.Label(self.nds_table_frame, text='--')
                label.grid(row=y+1,column=i+1)
                self.res_labels.append(label)
                self.res_nds_table_output.append('-')
        self.res_labels[0].configure(text='')
        self.res_nds_table_output[0] = ''
        self.res_labels[1].configure(text='')
        self.res_nds_table_output[1] = ','
        self.res_labels[14].configure(text='')
        self.res_nds_table_output[14] = ','
        self.res_labels[15].configure(text='')
        self.res_nds_table_output[15] = '\n'
        factors = ['Cd','Cm','Ct','CL','Cf','Cfu','Ci','Cr','Cp','CT','Cb','Cfrt']
        i=2
        for c in factors:
            self.res_labels[i].configure(text=c)
            self.res_nds_table_output[i] = c
            i+=1
        row_headers = ["Fb' = Fb ","Fv' = Fv ","Fc' = Fc ","Fc_perp' = Fc_perp ","E' = E ","Emin' = Emin "]
        i=16
        for header in row_headers:
            self.res_labels[i].configure(text=header)
            self.res_nds_table_output[i] = header
            i+=16
        
        i=31
        for y in range(1,7):
            self.res_labels[i].configure(text='psi')
            self.res_nds_table_output[i] = 'psi\n'
            i+=16
        self.nds_table_frame.pack(side=tk.TOP, padx=2, pady=2)
        
        ## Text Results Frame
        self.text_results_frame = tk.LabelFrame(self.results_frame, text="Calculation Results: ", bd=2, relief='sunken', padx=2, pady=2, font=helv)

        self.results_text_box = tk.Text(self.text_results_frame, height = 10, width = 10, bg= "grey90", font= tkFont.Font(family='Helvetica',size=8, weight='normal'), wrap=tk.WORD)
        self.results_text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.restxt_scroll = tk.Scrollbar(self.text_results_frame, command=self.results_text_box.yview)
        self.restxt_scroll.pack(side=tk.LEFT, fill=tk.Y)
        
        self.results_text_box['yscrollcommand'] = self.restxt_scroll.set

        self.text_results_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.b_output_res= tk.Button(self.results_frame,text="Export Results", command=self.write_text_results_to_file, font=helv, state = tk.DISABLED)
        self.b_output_res.pack(side=tk.RIGHT)
        self.b_output_pp= tk.Button(self.results_frame,text="Export P-Pressure Curves", command=self.print_pp_graph_common, font=helv, state = tk.DISABLED)
        self.b_output_pp.pack(side=tk.RIGHT)
        self.b_output_pm= tk.Button(self.results_frame,text="Export P-M Curves", command=self.print_pm_graph_common, font=helv, state = tk.DISABLED)
        self.b_output_pm.pack(side=tk.RIGHT)
        self.results_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        #Tab 2 -P vs Pressure Curve
        self.page2 = ttk.Frame(self.nb)
        self.nb.add(self.page2, text='P-Lateral Pressure Diagram', state = tk.DISABLED)
        
        self.pg2_frame = tk.Frame(self.page2, bd=2, relief='sunken', padx=1,pady=1)
        self.pg2_frame.pack(fill=tk.BOTH,expand=1, padx=2, pady=2)
        
        self.chart_frame = tk.Frame(self.pg2_frame, padx=2, pady=2)

        self.Fig = matplotlib.figure.Figure(figsize=(12,6),dpi=96)
        self.ax1 = self.Fig.add_subplot(111)
        self.ax1.minorticks_on()
        self.ax1.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
        self.ax1.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
        self.ax2=self.ax1.twinx()
        #Prebuild chart lines so data can be refreshed to cut down on render time
        #['0.9','1.0','1.15','1.25','1.6','2.0']
        self.line_cd009, = self.ax1.plot([0,10],[10,0], label='Cd = 0.9')
        self.line_cd100, = self.ax1.plot([0,15],[15,0], label='Cd = 1.0')
        self.line_cd115, = self.ax1.plot([0,25],[25,0], label='Cd = 1.15')
        self.line_cd125, = self.ax1.plot([0,35],[35,0], label='Cd = 1.25')
        self.line_cd160, = self.ax1.plot([0,50],[50,0], label='Cd = 1.6')
        self.line_cd200, = self.ax1.plot([0,75],[75,0], label='Cd = 2.0')
        self.line_pl_cb, = self.ax1.plot([0,10],[3,3], label='PL Crushing')
        self.line_pl_wo_cb, = self.ax1.plot([0,10],[1.5,1.5], label='PL Crushing w/o Cb')
        self.line_delta_cd009, = self.ax2.plot([0,10],[0,13], label='D - Cd = 0.9')
        self.line_delta_cd100, = self.ax2.plot([0,15],[15,0], label='D - Cd = 1.0')
        self.line_delta_cd115, = self.ax2.plot([0,25],[25,0], label='D - Cd = 1.15')
        self.line_delta_cd125, = self.ax2.plot([0,35],[35,0], label='D - Cd = 1.25')
        self.line_delta_cd160, = self.ax2.plot([0,50],[50,0], label='D - Cd = 1.6')
        self.line_delta_cd200, = self.ax2.plot([0,75],[75,0], label='D - Cd = 2.0')
        self.line_delta_180, = self.ax2.plot([6,6],[0,13], label='H/180', linestyle=':')
        self.line_delta_240, = self.ax2.plot([4,4],[0,13], label='H/240', linestyle=':')
        self.line_delta_360, = self.ax2.plot([1,1],[0,13], label='H/360', linestyle=':')
        self.line_delta_600, = self.ax2.plot([1,1],[0,13], label='H/600', linestyle=':')
        
        self.legend_ax1 = self.ax1.legend(loc=1, fontsize='x-small')
        self.legend_ax2 = self.ax2.legend(loc=4, fontsize='x-small')        
        
        self.ax1.set_ylabel('Axial (lbs)')
        self.ax1.set_xlabel('Lateral Pressure (psf)')
        self.ax2.set_ylabel('Mid Height Deflection (in)')
        
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.Fig, master=self.chart_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.chart_frame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.chart_frame.pack(side=tk.TOP,expand=1, fill=tk.BOTH)
        
        #Tab 3 -P vs M Curve
        self.page3 = ttk.Frame(self.nb)
        self.nb.add(self.page3, text='P-M Diagram', state = tk.DISABLED)
        
        self.pg3_frame = tk.Frame(self.page3, bd=2, relief='sunken', padx=1,pady=1)
        self.pg3_frame.pack(fill=tk.BOTH,expand=1, padx=2, pady=2)
        
        self.chart_frameB = tk.Frame(self.pg3_frame, padx=2, pady=2)

        self.FigB = matplotlib.figure.Figure(figsize=(12,6),dpi=96)
        self.ax1B = self.FigB.add_subplot(111)
        self.ax1B.minorticks_on()
        self.ax1B.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
        self.ax1B.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
        self.ax2B=self.ax1B.twinx()
        #Prebuild chart lines so data can be refreshed to cut down on render time
        #['0.9','1.0','1.15','1.25','1.6','2.0']
        self.line_cd009B, = self.ax1B.plot([0,10],[10,0], label='Cd = 0.9')
        self.line_cd100B, = self.ax1B.plot([0,15],[15,0], label='Cd = 1.0')
        self.line_cd115B, = self.ax1B.plot([0,25],[25,0], label='Cd = 1.15')
        self.line_cd125B, = self.ax1B.plot([0,35],[35,0], label='Cd = 1.25')
        self.line_cd160B, = self.ax1B.plot([0,50],[50,0], label='Cd = 1.6')
        self.line_cd200B, = self.ax1B.plot([0,75],[75,0], label='Cd = 2.0')
        self.line_pl_cbB, = self.ax1B.plot([0,10],[3,3], label='PL Crushing')
        self.line_pl_wo_cbB, = self.ax1B.plot([0,10],[1.5,1.5], label='PL Crushing w/o Cb')
        self.line_delta_cd009B, = self.ax2B.plot([0,10],[0,13], label='D - Cd = 0.9')
        self.line_delta_cd100B, = self.ax2B.plot([0,15],[15,0], label='D - Cd = 1.0')
        self.line_delta_cd115B, = self.ax2B.plot([0,25],[25,0], label='D - Cd = 1.15')
        self.line_delta_cd125B, = self.ax2B.plot([0,35],[35,0], label='D - Cd = 1.25')
        self.line_delta_cd160B, = self.ax2B.plot([0,50],[50,0], label='D - Cd = 1.6')
        self.line_delta_cd200B, = self.ax2B.plot([0,75],[75,0], label='D - Cd = 2.0')
        self.line_delta_180B, = self.ax2B.plot([6,6],[0,13], label='H/180', linestyle=':')
        self.line_delta_240B, = self.ax2B.plot([4,4],[0,13], label='H/240', linestyle=':')
        self.line_delta_360B, = self.ax2B.plot([1,1],[0,13], label='H/360', linestyle=':')
        self.line_delta_600B, = self.ax2B.plot([1,1],[0,13], label='H/600', linestyle=':')

        
        self.legend_ax1B = self.ax1B.legend(loc=1, fontsize='x-small')
        self.legend_ax2B = self.ax2B.legend(loc=4, fontsize='x-small')        
        
        self.ax1B.set_ylabel('Axial (lbs)')
        self.ax1B.set_xlabel('Moment (in-lbs)')
        self.ax2B.set_ylabel('Mid Height Deflection (in)')
        
        self.canvasB = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.FigB, master=self.chart_frameB)
        self.canvasB.show()
        self.canvasB.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbarB = NavigationToolbar2TkAgg(self.canvasB, self.chart_frameB)
        self.toolbarB.update()
        self.canvasB._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.chart_frameB.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        #Tab 4 -P vs M Curve
        self.page4 = ttk.Frame(self.nb)
        self.nb.add(self.page4, text='P-M Diagram - Stud', state = tk.DISABLED)
        
        self.pg4_frame = tk.Frame(self.page4, bd=2, relief='sunken', padx=1,pady=1)
        self.pg4_frame.pack(fill=tk.BOTH,expand=1, padx=2, pady=2)
        
        self.chart_frameD = tk.Frame(self.pg4_frame, padx=2, pady=2)

        self.FigD = matplotlib.figure.Figure(figsize=(12,6),dpi=96)
        self.ax1D = self.FigD.add_subplot(111)
        self.ax1D.minorticks_on()
        self.ax1D.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
        self.ax1D.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
        self.ax2D=self.ax1D.twinx()
        #Prebuild chart lines so data can be refreshed to cut down on render time
        #['0.9','1.0','1.15','1.25','1.6','2.0']
        self.line_cd009D, = self.ax1D.plot([0,10],[10,0], label='Cd = 0.9')
        self.line_cd100D, = self.ax1D.plot([0,15],[15,0], label='Cd = 1.0')
        self.line_cd115D, = self.ax1D.plot([0,25],[25,0], label='Cd = 1.15')
        self.line_cd125D, = self.ax1D.plot([0,35],[35,0], label='Cd = 1.25')
        self.line_cd160D, = self.ax1D.plot([0,50],[50,0], label='Cd = 1.6')
        self.line_cd200D, = self.ax1D.plot([0,75],[75,0], label='Cd = 2.0')
        self.line_pl_cbD, = self.ax1D.plot([0,10],[3,3], label='PL Crushing')
        self.line_pl_wo_cbD, = self.ax1D.plot([0,10],[1.5,1.5], label='PL Crushing w/o Cb')
        self.line_delta_cd009D, = self.ax2D.plot([0,10],[0,13], label='D - Cd = 0.9')
        self.line_delta_cd100D, = self.ax2D.plot([0,15],[15,0], label='D - Cd = 1.0')
        self.line_delta_cd115D, = self.ax2D.plot([0,25],[25,0], label='D - Cd = 1.15')
        self.line_delta_cd125D, = self.ax2D.plot([0,35],[35,0], label='D - Cd = 1.25')
        self.line_delta_cd160D, = self.ax2D.plot([0,50],[50,0], label='D - Cd = 1.6')
        self.line_delta_cd200D, = self.ax2D.plot([0,75],[75,0], label='D - Cd = 2.0')
        self.line_delta_180D, = self.ax2D.plot([6,6],[0,13], label='H/180', linestyle=':')
        self.line_delta_240D, = self.ax2D.plot([4,4],[0,13], label='H/240', linestyle=':')
        self.line_delta_360D, = self.ax2D.plot([1,1],[0,13], label='H/360', linestyle=':')
        self.line_delta_600D, = self.ax2D.plot([1,1],[0,13], label='H/600', linestyle=':')
        
        self.user_pmD, = self.ax1D.plot([1,1],[2,2], linestyle='None', marker= 'o')
        self.user_mdD, = self.ax2D.plot([1,1],[2,2], linestyle='None', marker= 'x')

        
        self.legend_ax1D = self.ax1D.legend(loc=1, fontsize='x-small')
        self.legend_ax2D = self.ax2D.legend(loc=4, fontsize='x-small')        
        
        self.ax1D.set_ylabel('Axial (lbs)')
        self.ax1D.set_xlabel('Moment (in-lbs)')
        self.ax2D.set_ylabel('Mid Height Deflection (in)')
        
        self.canvasD = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.FigD, master=self.chart_frameD)
        self.canvasD.show()
        self.canvasD.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbarD = NavigationToolbar2TkAgg(self.canvasD, self.chart_frameD)
        self.toolbarD.update()
        self.canvasD._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.chart_frameD.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        #Tab 5 - User Loads
        self.page5 = ttk.Frame(self.nb)
        self.nb.add(self.page5, text='User Loads', state = tk.DISABLED)
        
        self.pg5_frame = tk.Frame(self.page5, bd=2, relief='sunken', padx=1,pady=1)
        self.pg5_frame.pack(fill=tk.BOTH,expand=1, padx=2, pady=2)
        
        #user Loads input frame
        self.user_ins_top_frame = tk.Frame(self.pg5_frame)
        self.input_frame_loads = tk.LabelFrame(self.user_ins_top_frame, text="Loads Inputs (IBC 2012):", bd=2, relief='sunken', padx=2, pady=2)
        #Vertical Loads - [DL,LL,Lr,S,R]
        tk.Label(self.input_frame_loads, text='Vertical Loads: ').grid(column=1, row=1)
        self.user_vert_load_labels = ['D: ','L: ','Lr: ','S: ','R: ']
        self.user_load_trib_plf_label = []
        tk.Label(self.input_frame_loads, text='Self Weight: ').grid(column=1, row=2)
        self.user_sw = tk.StringVar()
        self.user_sw.set(0.0)
        self.user_sw_psf_entry = tk.Entry(self.input_frame_loads, textvariable=self.user_sw, width=15).grid(column=2, row=2)
        tk.Label(self.input_frame_loads, text='psf x ').grid(column=3, row=2)
        self.user_sw_height_ft = tk.StringVar()
        self.user_sw_height_ft.set(0.0)
        self.user_sw_height_ft_entry = tk.Entry(self.input_frame_loads, textvariable=self.user_sw_height_ft, width=15).grid(column=4, row=2)
        self.user_sw_label = tk.Label(self.input_frame_loads, text='ft = x plf')
        self.user_sw_label.grid(column=5, row=2)
        
        i=2
        for label in self.user_vert_load_labels:
            tk.Label(self.input_frame_loads, text=label).grid(column=1, row=i+1)
            tk.Label(self.input_frame_loads, text='psf x ').grid(column=3, row=i+1)
            self.user_load_trib_plf_label.append(tk.Label(self.input_frame_loads, text='ft = x plf'))
            self.user_load_trib_plf_label[i-2].grid(column=5, row=i+1)
            i+=1
            
        self.user_vert_loads_psf = [tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()]
        self.user_vert_loads_trib = [tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()]
        i=2
        for load in self.user_vert_loads_psf:
            load.set(0.0)
            self.user_vert_loads_trib[i-2].set(0.0)
            tk.Entry(self.input_frame_loads, textvariable=load, width=15).grid(column=2, row=i+1)
            tk.Entry(self.input_frame_loads, textvariable=self.user_vert_loads_trib[i-2], width=15).grid(column=4, row=i+1)
            i+=1
        #Lateral Pressures
        #Lateral Loads - [L,W,ultimate]
        tk.Label(self.input_frame_loads, text='Lateral Loads: ').grid(column=7, row=1, padx=10)
        self.user_lat_load_labels = ['L: ','W_ultimate: ']
        i=1
        for label in self.user_lat_load_labels:
            tk.Label(self.input_frame_loads, text=label).grid(column=7, row=i+1, padx=10)
            tk.Label(self.input_frame_loads, text='psf').grid(column=9, row=i+1)
            i+=1
        
        self.user_lat_loads_psf = [tk.StringVar(),tk.StringVar()]
        i=1
        for load in self.user_lat_loads_psf:
            load.set(0.0)
            tk.Entry(self.input_frame_loads, textvariable=load, width=15).grid(column=8, row=i+1)
            i+=1

        self.input_frame_loads.pack(side=tk.LEFT, padx=2, pady=2)
        
        #user Loads input frame
        self.input_frame_user_wall = tk.LabelFrame(self.user_ins_top_frame, text="Wall Information:", bd=2, relief='sunken', padx=2, pady=2)
        tk.Label(self.input_frame_user_wall, text='Wall Height: ').grid(column=1, row=1)
        self.user_calc_wall_ht_ft = tk.Label(self.input_frame_user_wall, text='--')
        self.user_calc_wall_ht_ft.grid(column=2, row=1)
        tk.Label(self.input_frame_user_wall, text=' ft').grid(column=3, row=1)
        self.user_calc_spacing = tk.StringVar()
        self.user_calc_spacing.set(12.0)
        tk.Label(self.input_frame_user_wall, text='Spacing: ').grid(column=1, row=2)
        tk.Entry(self.input_frame_user_wall, textvariable=self.user_calc_spacing, width=15).grid(column=2, row=2)
        tk.Label(self.input_frame_user_wall, text=' in o.c.').grid(column=3, row=2)
        
        self.b_user_run = tk.Button(self.input_frame_user_wall,text="Check User loads", command=self.run_user_loads, font=helv)
        self.b_user_run.grid(column=4, row = 1, padx=10)
        
        self.b_user_solve = tk.Button(self.input_frame_user_wall,text="Optimize Spacing", command=self.solve_user_loads, font=helv)
        self.b_user_solve.grid(column=4, row = 2, padx=10)
        
        self.b_user_export = tk.Button(self.input_frame_user_wall,text="Export User Load Results", command=self.export_user_load_results, font=helv)
        self.b_user_export.grid(column=4, row = 3, padx=10)
        
        self.input_frame_user_wall.pack(side=tk.LEFT, padx=2, pady=2)
        self.user_ins_top_frame.pack(side=tk.TOP)
        
        self.user_res_bottom_frame = tk.LabelFrame(self.pg5_frame, text="Results (IBC 2012 - ASD):", bd=2, relief='sunken', padx=2, pady=2)
        res_headings = ['Combo:','Cd','P (lbs)', 'fc (psi)','Ke Le_d/d','FcE (psi)','c','Cp',"Fc' (psi)","fc/Fc'",'M_lat (in-lbs)','fb_lat (psi)',"Fb' (psi)","fb/Fb'",'V (lbs)','fv (psi)',"Fv' (psi)","fv/Fv'",'Ratio','D (H/--)','Status']
        self.load_combos = [['D',0.9,1,0,0,0,0,0],
                            ['D+L',1,1,1,0,0,0,0],
                            ['D+Lr',1,1,0,1,0,0,0], 
                            ['D+S',1.15,1,0,0,1,0,0],
                            ['D+R',1.15,1,0,0,0,1,0],
                            ['D+.75L+.75Lr',1,1,0.75,0.75,0,0,0],
                            ['D+.75L+.75S',1.15,1,0.75,0,0.75,0,0],
                            ['D+.75L+.75R',1.15,1,0.75,0,0,0.75,0],
                            ['D+.6W',1.6,1,0,0,0,0,0.6],
                            ['D+.75(.6W)+.75L+.75Lr',1.6,1,0.75,0.75,0,0,0.45],
                            ['D+.75(.6W)+.75L+.75S',1.6,1,0.75,0,0.75,0,0.45],
                            ['D+.75(.6W)+.75L+.75R',1.6,1,0.75,0,0,0.75,0.45],
                            ['.6D + .6W',1.6,0.6,0,0,0,0,0.6]]
        i=1
        for heading in res_headings:
            tk.Label(self.user_res_bottom_frame, text = heading).grid(column=i, row=1, padx=4)
            i+=1
        
        i=0
        
        self.user_p_res_labels=[]
        self.user_fc_res_labels=[]
        self.user_kel_res_labels=[]
        self.user_FcE_res_labels=[]
        self.user_c_labels=[]
        self.user_cp_labels=[]
        self.user_fcprime_res_labels=[]
        self.user_fc_fc_res_labels=[]
        self.user_m_res_labels=[]
        self.user_fb_res_labels=[]
        self.user_fbprime_res_labels=[]
        self.user_fb_fb_res_labels=[]
        self.user_v_res_labels=[]
        self.user_fv_res_labels=[]
        self.user_fvprime_res_labels=[]
        self.user_fv_fv_res_labels=[]
        self.user_ratio_res_labels=[]
        self.user_deltaratio_res_labels=[]
        self.user_status_res_labels=[]
        for combo in self.load_combos:
            tk.Label(self.user_res_bottom_frame, text = combo[0]).grid(column=1, row=i+2, padx=4)
            tk.Label(self.user_res_bottom_frame, text = combo[1]).grid(column=2, row=i+2, padx=4)
            self.user_p_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_p_res_labels[i].grid(column=3, row=i+2, padx=4)
            self.user_fc_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_fc_res_labels[i].grid(column=4, row=i+2, padx=4)
            self.user_kel_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_kel_res_labels[i].grid(column=5, row=i+2, padx=4)
            self.user_FcE_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_FcE_res_labels[i].grid(column=6, row=i+2, padx=4)
            self.user_c_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_c_labels[i].grid(column=7, row=i+2, padx=4)
            self.user_cp_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_cp_labels[i].grid(column=8, row=i+2, padx=4)
            self.user_fcprime_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_fcprime_res_labels[i].grid(column=9, row=i+2, padx=4)
            self.user_fc_fc_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_fc_fc_res_labels[i].grid(column=10, row=i+2, padx=4)
            self.user_m_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_m_res_labels[i].grid(column=11, row=i+2, padx=4)
            self.user_fb_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_fb_res_labels[i].grid(column=12, row=i+2, padx=4)
            self.user_fbprime_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_fbprime_res_labels[i].grid(column=13, row=i+2, padx=4)
            self.user_fb_fb_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_fb_fb_res_labels[i].grid(column=14, row=i+2, padx=4)
            self.user_v_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_v_res_labels[i].grid(column=15, row=i+2, padx=4)
            self.user_fv_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_fv_res_labels[i].grid(column=16, row=i+2, padx=4)
            self.user_fvprime_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_fvprime_res_labels[i].grid(column=17, row=i+2, padx=4)
            self.user_fv_fv_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_fv_fv_res_labels[i].grid(column=18, row=i+2, padx=4)
            self.user_ratio_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_ratio_res_labels[i].grid(column=19, row=i+2, padx=4)
            self.user_deltaratio_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_deltaratio_res_labels[i].grid(column=20, row=i+2, padx=4)
            self.user_status_res_labels.append(tk.Label(self.user_res_bottom_frame, text = '--'))
            self.user_status_res_labels[i].grid(column=21, row=i+2, padx=4)
            i+=1
            
        self.user_res_bottom_frame.pack(side=tk.TOP)
        
        self.b_quit = tk.Button(self.base_frame,text="Quit", command=self.quit_app, font=helv)
        self.b_quit.pack(side=tk.RIGHT)
        self.b_save = tk.Button(self.base_frame,text="Save Inputs", command=self.save_inputs, font=helv, state = tk.DISABLED)
        self.b_save.pack(side=tk.RIGHT)
        
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
        
    def quit_app(self):
        self.master.destroy()
        self.master.quit()
        
    def enable_tab2(self):
        self.nb.tab(1,state=tk.NORMAL)
        self.nb.tab(2,state=tk.NORMAL)
        self.nb.tab(3,state=tk.NORMAL)
        self.nb.tab(4,state=tk.NORMAL)
    
    def com_lat_brace_func(self, *event):
        if self.com_lat_brace_yn.get() == 1:
            self.no_sheathing_yn.set(0)
        else:
            pass
            
    def no_sheating_func(self, *event):
        if self.no_sheathing_yn.get() == 1:
            self.com_lat_brace_yn.set(0)
        else:
            pass
    
    def actual_stud_size(self, *event):
        w = self.b_nom.get()
        
        if w == '2' or w== '3' or w=='4':
            b = float(self.b_nom.get())
            self.b_actual = b - 0.5
        elif w == '(2)2':
            self.b_actual = 2.0*1.5
        else:
            self.b_actual = 3.0*1.5
        d = float(self.d_nom.get())
        
        
        if d > 6.0:
            self.d_actual = d - 0.75
        else:
            self.d_actual = d - 0.5
        
        self.b_actual_label.configure(text=self.b_actual)
        self.d_actual_label.configure(text=self.d_actual)
    
    def run(self, *event):
        self.results_text_box.delete(1.0,tk.END)
        self.actual_stud_size()
        self.enable_tab2()
        # (self,b_in=1.5,d_in=3.5,height_ft=10, spacing_in=12, grade="No.2", fb_psi=875, fv_psi= 150, fc_psi=1150, E_psi=1400000, Emin_psi=510000, fc_perp_pl_psi=565, moisture_percent = 19, temp = 90, incised = 0,  num_plates = 0, c_frt=[1,1,1,1,1,1]):
        b = self.b_actual
        d = self.d_actual
        height = float(self.wall_height.get())
        spacing = float(self.stud_spacing.get())
        grade = self.grade.get()
        self.title = '{0}x{1} ({2:.2f}x{3:.2f})- Height:{4} ft - Species: {7} - Grade: {5} - Spacing: {6} in'.format(self.b_nom.get(),self.d_nom.get(),b,d,height,grade,spacing, self.species.get())
        self.title_pm_stud = '{0}x{1} ({2:.2f}x{3:.2f})- Height:{4} ft - Species: {6} - Grade: {5}'.format(self.b_nom.get(),self.d_nom.get(),b,d,height,grade, self.species.get())
        self.results_text_box.insert(tk.END, self.title)
        
        fb = float(self.fb_psi.get())
        fv = float(self.fv_psi.get())
        fc = float(self.fc_psi.get())
        E = float(self.E_psi.get())
        Emin = float(self.Emin_psi.get())
        fc_perp = float(self.fc_perp_psi.get())
        moisture = float(self.moisture.get())
        temp = float(self.temp.get())
        incise = self.incised_yn.get()
        
        sub_plates = self.sub_plates.get()
        if sub_plates == 1:
            num_pl = float(self.num_plates.get())
        else:
            num_pl = 0
            
        frt = self.frt_yn.get()
        if frt ==1:
            cfrt = [float(self.frt_fb.get()),float(self.frt_fv.get()),float(self.frt_fc.get()),float(self.frt_fc_perp.get()),float(self.frt_E.get()),float(self.frt_Emin.get())]
        else:
            cfrt =[1,1,1,1,1,1]
        
        min_ecc = self.min_ecc_yn.get()
        if min_ecc == 1:
            self.e_in = d/6.0
            e_string = ' at min d/6 = {0:.3f} in eccentricity '.format(self.e_in)
        else:
            self.e_in = 0
            e_string =''
        
        self.wall = wood.wood_stud_wall(b,d,height,spacing,grade,fb,fv,fc,E,Emin,fc_perp,moisture,temp,incise,num_pl, cfrt, self.com_lat_brace_yn.get(), float(self.blocking_ft.get()), self.no_sheathing_yn.get(),self.is_syp.get())
        
            
        pressure_psf = float(self.pressure.get())
        
        self.pressure_moment_inlbs = (((pressure_psf*(self.wall.spacing_in/12.0))*(self.wall.height_in/12.0)**2)/8.0) * 12.0
        self.pressure_shear_lbs = (((pressure_psf*(self.wall.spacing_in/12.0))*(self.wall.height_in/12.0))/2.0)
        
        ##Solve for maximum axial capacity
        cd = float(self.cd.get())
        p_lbs = self.wall.axial_capacity_w_moment(cd,self.pressure_moment_inlbs,self.e_in)
        
        ##Create Text String and write Axial result to text box        
        axial_string = '\n\n-- Pmax_allow = {0:.2f} lbs ({2:.2f} plf) {1} --'.format(p_lbs,e_string, p_lbs/(self.wall.spacing_in/12.0))
        axial_string = axial_string + '\n-- PL Crushing (Cb): {0:.2f} lbs ({2:.2f} plf) --\n-- PL Crushing (w/o Cb): {1:.2f} lbs ({3:.2f} plf) --'.format(self.wall.crushing_limit_lbs,self.wall.crushing_limit_lbs_no_cb,self.wall.crushing_limit_lbs/(self.wall.spacing_in/12.0),self.wall.crushing_limit_lbs_no_cb/(self.wall.spacing_in/12.0))
        
        ##Write out any warnings that occured during the wall creation or axial run
        if self.wall.warning == '':
            pass
        else:
            self.results_text_box.insert(tk.END, "\n*** ERROR/WARNING ***\n")
            self.results_text_box.insert(tk.END, self.wall.warning)
            
        common_capacities = self.wall.cap_at_common_spacing(cd,pressure_psf,self.e_in,self.consider_crushing.get())
        axial_string = axial_string + '\n\n--Common Spacing Capacities--\n' + common_capacities
        
            
        self.results_text_box.insert(tk.END, axial_string)
        
        ##Pull Section properties from wall class and write out to results text box
        section_props_string = '\n\n--Section Properties--\nA = {0:.3f} in^2 -- S = {1:.3f} in^3 -- I = {2:.3f} in^4'.format(self.wall.area_in2,self.wall.s_in3,self.wall.I_in4)
        self.results_text_box.insert(tk.END, section_props_string)
        
        #Applied Loads - Axial
        self.loads_string = '\n\n--Applied Loads--\nPressure: {0:.2f} psf x Spacing x 1 ft / 12 in = {1:.2f} plf'.format(pressure_psf,pressure_psf * (spacing/12.0))
        w_plf = pressure_psf * (spacing/12.0)            
        deflection_lat = (5 * (w_plf) * (self.wall.height_in/12)**4)/(384*self.wall.E_prime_psi*self.wall.I_in4)*1728        
        if min_ecc == 1:
            self.ecc_moment_inlbs = p_lbs * self.e_in
            self.ecc_shear_lbs = self.ecc_moment_inlbs / self.wall.height_in
            deflection_axial = (((self.ecc_moment_inlbs)*self.wall.height_in**2)/(16.0*self.wall.E_prime_psi*self.wall.I_in4))
            deflection = deflection_lat + deflection_axial
            applied_shear_string = '\nLateral Shear: {0:.2f} lbs + Gravity Shear: {1:.2f} lbs = Total Shear: {2:.2f} lbs'.format(self.pressure_shear_lbs, self.ecc_shear_lbs,self.pressure_shear_lbs+self.ecc_shear_lbs)
            applied_moment_string = '\nLateral Moment: {0:.2f} in-lbs + Gravity Moment: {1:.2f} in-lbs = Total Moment: {2:.2f} in-lbs'.format(self.pressure_moment_inlbs, self.ecc_moment_inlbs,self.pressure_moment_inlbs+self.ecc_moment_inlbs)
            deflection_string = '\nLateral Delta: {0:.3f} in + Gravity Delta: {1:.3f} in = Delta: {2:.3f} in - H / {3:.1f}'.format(deflection_lat, deflection_axial, deflection, self.wall.height_in/deflection)
        else:
            self.ecc_moment_inlbs = 0.0
            self.ecc_shear_lbs = 0.0
            applied_shear_string = '\nLateral Shear: {0:.2f} lbs'.format(self.pressure_shear_lbs)
            applied_moment_string = '\nLateral Moment: {0:.2f} in-lbs'.format(self.pressure_moment_inlbs)
            deflection_string = '\nLateral Delta: {0:.3f} - H / {1:.1f}'.format(deflection_lat, self.wall.height_in/deflection_lat)
        self.loads_string = self.loads_string + applied_shear_string + applied_moment_string + deflection_string
        self.results_text_box.insert(tk.END, self.loads_string)
        
        ##Stresses
        self.stress_string = '\n\n--Stresses--'
        axial_stress = p_lbs/self.wall.area_in2
        self.stress_string = self.stress_string+'\nfc = P/A = {0:.3f} psi'.format(axial_stress)
        shear = self.pressure_shear_lbs + self.ecc_shear_lbs
        shear_stress = (3.0*shear)/(2.0*b*d)
        self.stress_string = self.stress_string+'\nfv = VQ/Ib = 3V/2bd = {0:.3f} psi'.format(shear_stress)
        if self.e_in == 0:
            moment = self.pressure_moment_inlbs + self.ecc_moment_inlbs
            bending_stress_lat = self.pressure_moment_inlbs/self.wall.s_in3
            bending_stress = moment/self.wall.s_in3
            self.stress_string = self.stress_string+'\nfb = Mc/I = M/s = 6M/bd^2 = {0:.3f} psi'.format(bending_stress_lat)
            #Combine ratio per NDS 2005 equation (3.9-3)
            #[fc/Fc]'^2 + fb / Fb' [ 1- (fc / FcE)] <= 1.0
            ratio = (axial_stress/self.wall.fc_prime_psi)**2 + (bending_stress / (self.wall.fb_prime_calc(cd)*(1-(axial_stress/self.wall.fcE_psi))))
            self.stress_string = self.stress_string+"\nCombined Axial+Bending:\n[fc/Fc]'^2 + fb / Fb' [ 1- (fc / FcE)] = {0:.3f} <= 1.0".format(ratio)
        else:
            moment = self.pressure_moment_inlbs + self.ecc_moment_inlbs
            bending_stress_ecc = self.ecc_moment_inlbs/self.wall.s_in3
            bending_stress_lat = self.pressure_moment_inlbs/self.wall.s_in3
            bending_stress = moment/self.wall.s_in3
            self.stress_string = self.stress_string+'\nfb_lat = Mc/I = M/s = 6M/bd^2 = {0:.3f} psi + fb_gravity = {1:.3f} = {2:.3f}'.format(bending_stress_lat,bending_stress_ecc,bending_stress)
            #Combined Ratio per NDS 2005 equation 15.4-1
            #[fc/Fc]'^2 + (fb + fc(6e/d)[1 + 0.234 (fc / FcE)])/ Fb' [ 1- (fc / FcE)] <= 1.0
            b1 = self.pressure_moment_inlbs/self.wall.s_in3
            ratio = (axial_stress/self.wall.fc_prime_psi)**2 + ((b1+(axial_stress*(6*self.e_in/d)*(1+(0.234*(axial_stress/self.wall.fcE_psi)))))/ (self.wall.fb_prime_calc(cd)*(1-(axial_stress/self.wall.fcE_psi))))
            self.stress_string = self.stress_string+"\nCombined Axial+Bending w/ Eccentricity:\n[fc/Fc]'^2 + (fb_lat + fc(6e/d)[1 + 0.234 (fc / FcE)])/ Fb' [ 1- (fc / FcE)] = {0:.3f} <= 1.0".format(ratio)
        self.results_text_box.insert(tk.END, self.stress_string)
        
        ##Calculation of Cp
        self.cp_string = '\n\n--Calculation of Cp--'
        self.cp_string=self.cp_string + '\nFc* = reference compression design value parallel to grain multiplied by all applicable adjusment factors except Cp\nFc* = Fc*Cd*Cm*Ct*Cf*Ci = {1:.2f}*{2:.2f}*{3:.2f}*{4:.2f}*{5:.2f}*{6:.2f} = {0:.2f} psi\nc = 0.8 - NDS 2005 3.7.1'.format(self.wall.fc_star_psi,self.wall.fc_psi,cd,self.wall.cm_fc,self.wall.ct_fc,self.wall.cf_fc,self.wall.ci_fc)
        self.cp_string=self.cp_string + self.wall.assumptions_ke + self.wall.assumptions_leb
        self.cp_string = self.cp_string + 'Ke * Le_d / d = {0:.3f} in < 50'.format(self.wall.height_in/d)
        self.cp_string = self.cp_string + '\nKe * Le_b / b = {0:.3f} in < 50'.format(self.wall.le_b/b)
        self.cp_string = self.cp_string + "\nFcE = 0.822 * Emin' / (max[Le_d/d,Le_b/b])^2 - NDS 2005 Section 3.7.1\nFcE = {0:.3f} psi".format(self.wall.fcE_psi)
        self.cp_string = self.cp_string + "\nCp = ([1 + (FcE / Fc*)] / 2c ) - sqrt[ [1 + (FcE / Fc*) / 2c]^2 - (FcE / Fc*) / c] = {0:.3f} - NDS 2005 Section 3.7.1".format(self.wall.cp)
        self.results_text_box.insert(tk.END, self.cp_string)
        
        ##Calculation of CL
        if self.com_lat_brace_yn.get() == 1:
            pass
        else:
            self.results_text_box.insert(tk.END, self.wall.cl_calc_text)
        
        ##write out assumption from wall creation - see wood_classes.py
        assumptions_string = self.wall.assumptions + self.wall.assumptions_c+self.wall.assumptions_cp
        self.results_text_box.insert(tk.END, assumptions_string)
        
        ##Fill in reduction factor table
        #Fb
        self.res_labels[17].configure(text='{0:.2f}'.format(fb))
        self.res_nds_table_output[17] = '{0:.2f}'.format(fb)
        self.res_labels[18].configure(text='{0:.2f}'.format(cd))
        self.res_nds_table_output[18] = '{0:.2f}'.format(cd)
        self.res_labels[19].configure(text='{0:.2f}'.format(self.wall.cm_fb))
        self.res_nds_table_output[19] = '{0:.2f}'.format(self.wall.cm_fb)
        self.res_labels[20].configure(text='{0:.2f}'.format(self.wall.ct_fb))
        self.res_nds_table_output[20] = '{0:.2f}'.format(self.wall.ct_fb)
        self.res_labels[21].configure(text='{0:.2f}'.format(self.wall.cl))
        self.res_nds_table_output[21] = '{0:.2f}'.format(self.wall.cl)        
        self.res_labels[22].configure(text='{0:.2f}'.format(self.wall.cf_fb))
        self.res_nds_table_output[22] = '{0:.2f}'.format(self.wall.cf_fb)
        self.res_labels[23].configure(text='{0:.2f}'.format(self.wall.cfu))
        self.res_nds_table_output[23] = '{0:.2f}'.format(self.wall.cfu)
        self.res_labels[24].configure(text='{0:.2f}'.format(self.wall.ci_fb))
        self.res_nds_table_output[24] = '{0:.2f}'.format(self.wall.ci_fb)
        self.res_labels[25].configure(text='{0:.2f}'.format(self.wall.cr))
        self.res_nds_table_output[25] = '{0:.2f}'.format(self.wall.cr)
        self.res_labels[29].configure(text='{0:.2f}'.format(cfrt[0]))
        self.res_nds_table_output[29] = '{0:.2f}'.format(cfrt[0])
        self.res_labels[30].configure(text='{0:.2f}'.format(self.wall.fb_prime_calc(cd)))
        self.res_nds_table_output[30] = '{0:.2f}'.format(self.wall.fb_prime_calc(cd))
        
        #Fv
        self.res_labels[33].configure(text='{0:.2f}'.format(fv))
        self.res_nds_table_output[33] = '{0:.2f}'.format(fv)
        self.res_labels[34].configure(text='{0:.2f}'.format(cd))
        self.res_nds_table_output[34] = '{0:.2f}'.format(cd)
        self.res_labels[35].configure(text='{0:.2f}'.format(self.wall.cm_fv))
        self.res_nds_table_output[35] = '{0:.2f}'.format(self.wall.cm_fv)
        self.res_labels[36].configure(text='{0:.2f}'.format(self.wall.ct_fv))
        self.res_nds_table_output[36] = '{0:.2f}'.format(self.wall.ct_fv)
        self.res_labels[40].configure(text='{0:.2f}'.format(self.wall.ci_fv))
        self.res_nds_table_output[40] = '{0:.2f}'.format(self.wall.ci_fv)
        self.res_labels[45].configure(text='{0:.2f}'.format(cfrt[1]))
        self.res_nds_table_output[45] = '{0:.2f}'.format(cfrt[1])
        self.res_labels[46].configure(text='{0:.2f}'.format(self.wall.fv_prime_psi_cd))
        self.res_nds_table_output[46] = '{0:.2f}'.format(self.wall.fv_prime_psi_cd)
        
        #Fc
        self.res_labels[49].configure(text='{0:.2f}'.format(fc))
        self.res_nds_table_output[49] = '{0:.2f}'.format(fc)
        self.res_labels[50].configure(text='{0:.2f}'.format(cd))
        self.res_nds_table_output[50] = '{0:.2f}'.format(cd)
        self.res_labels[51].configure(text='{0:.2f}'.format(self.wall.cm_fc))
        self.res_nds_table_output[51] = '{0:.2f}'.format(self.wall.cm_fc)
        self.res_labels[52].configure(text='{0:.2f}'.format(self.wall.ct_fc))
        self.res_nds_table_output[52] = '{0:.2f}'.format(self.wall.ct_fc)
        self.res_labels[54].configure(text='{0:.2f}'.format(self.wall.cf_fc))
        self.res_nds_table_output[54] = '{0:.2f}'.format(self.wall.cf_fc)
        self.res_labels[56].configure(text='{0:.2f}'.format(self.wall.ci_fc))
        self.res_nds_table_output[56] = '{0:.2f}'.format(self.wall.ci_fc)
        self.res_labels[58].configure(text='{0:.3f}'.format(self.wall.cp))
        self.res_nds_table_output[58] = '{0:.3f}'.format(self.wall.cp)
        self.res_labels[61].configure(text='{0:.2f}'.format(cfrt[2]))
        self.res_nds_table_output[61] = '{0:.2f}'.format(cfrt[2])
        self.res_labels[62].configure(text='{0:.2f}'.format(self.wall.fc_prime_psi))
        self.res_nds_table_output[62] = '{0:.2f}'.format(self.wall.fc_prime_psi)
        
        #fc_perp
        self.res_labels[65].configure(text='{0:.2f}'.format(fc_perp))
        self.res_nds_table_output[65] = '{0:.2f}'.format(fc_perp)
        self.res_labels[67].configure(text='{0:.2f}'.format(self.wall.cm_fc_perp))
        self.res_nds_table_output[67] = '{0:.2f}'.format(self.wall.cm_fc_perp)
        self.res_labels[68].configure(text='{0:.2f}'.format(self.wall.ct_fc_perp))
        self.res_nds_table_output[68] = '{0:.2f}'.format(self.wall.ct_fc_perp)
        self.res_labels[72].configure(text='{0:.2f}'.format(self.wall.ci_fc_perp))
        self.res_nds_table_output[72] = '{0:.2f}'.format(self.wall.ci_fc_perp)
        self.res_labels[76].configure(text='{0:.2f}'.format(self.wall.cb_fc_perp))
        self.res_nds_table_output[76] = '{0:.2f}'.format(self.wall.cb_fc_perp)
        self.res_labels[77].configure(text='{0:.2f}'.format(cfrt[3]))
        self.res_nds_table_output[77] = '{0:.2f}'.format(cfrt[3])
        self.res_labels[78].configure(text='{0:.2f}'.format(self.wall.fc_perp_pl_prime_psi))
        self.res_nds_table_output[78] = '{0:.2f}'.format(self.wall.fc_perp_pl_prime_psi)
        
        #E
        self.res_labels[81].configure(text='{0:.2f}'.format(E))
        self.res_nds_table_output[81] = '{0:.2f}'.format(E)
        self.res_labels[83].configure(text='{0:.2f}'.format(self.wall.cm_E))
        self.res_nds_table_output[83] = '{0:.2f}'.format(self.wall.cm_E)
        self.res_labels[84].configure(text='{0:.2f}'.format(self.wall.ct_E))
        self.res_nds_table_output[84] = '{0:.2f}'.format(self.wall.ct_E)
        self.res_labels[88].configure(text='{0:.2f}'.format(self.wall.ci_E))
        self.res_nds_table_output[88] = '{0:.2f}'.format(self.wall.ci_E)
        self.res_labels[93].configure(text='{0:.2f}'.format(cfrt[4]))
        self.res_nds_table_output[93] = '{0:.2f}'.format(cfrt[4])
        self.res_labels[94].configure(text='{0:.2f}'.format(self.wall.E_prime_psi))
        self.res_nds_table_output[94] = '{0:.2f}'.format(self.wall.E_prime_psi)
        
        #Emin
        self.res_labels[97].configure(text='{0:.2f}'.format(Emin))
        self.res_nds_table_output[97] = '{0:.2f}'.format(Emin)
        self.res_labels[99].configure(text='{0:.2f}'.format(self.wall.cm_E))
        self.res_nds_table_output[99] = '{0:.2f}'.format(self.wall.cm_E)
        self.res_labels[100].configure(text='{0:.2f}'.format(self.wall.ct_E))
        self.res_nds_table_output[100] = '{0:.2f}'.format(self.wall.ct_E)
        self.res_labels[104].configure(text='{0:.2f}'.format(self.wall.ci_E))
        self.res_nds_table_output[104] = '{0:.2f}'.format(self.wall.ci_E)
        self.res_labels[107].configure(text='{0:.2f}'.format(self.wall.cT))
        self.res_nds_table_output[107] = '{0:.2f}'.format(self.wall.cT)
        self.res_labels[109].configure(text='{0:.2f}'.format(cfrt[5]))
        self.res_nds_table_output[109] = '{0:.2f}'.format(cfrt[5])
        self.res_labels[110].configure(text='{0:.2f}'.format(self.wall.Emin_prime_psi))
        self.res_nds_table_output[110] = '{0:.2f}'.format(self.wall.Emin_prime_psi)
        
        self.b_build_chart.configure(state=tk.NORMAL)
        self.b_build_pm.configure(state=tk.NORMAL)
        self.b_output_res.configure(state=tk.NORMAL)
        self.b_output_pm.configure(state=tk.NORMAL)
        self.b_output_pp.configure(state=tk.NORMAL)
        self.b_save.configure(state=tk.NORMAL)
        
        #Fill consistant wall information in user laod calc tab
        #set wall height
        self.user_calc_wall_ht_ft.configure(text='{0:.3f}'.format(self.wall.height_in/12.0))
        self.user_sw_height_ft.set(self.wall.height_in/12.0)
        tk.Label(self.user_res_bottom_frame, text = '* - indicates load greater than wall plate crushing w/o Cb - {0:.3f} lbs'.format(self.wall.crushing_limit_lbs_no_cb)).grid(column=1, row=15, columnspan=10)
        tk.Label(self.user_res_bottom_frame, text = '** - indicates load greater than wall plate crushing w/ Cb - {0:.3f} lbs'.format(self.wall.crushing_limit_lbs)).grid(column=1, row=16, columnspan=10)
        
    def generate_interaction_graph(self,*event):        
        e_in = self.e_in
        #Refresh chart data for each Cd
        #Cd - NDS 2005 Table 2.3.2
        #cd = [0.9,1.0,1.15,1.25,1.6,2.0]
        w,p,d = self.wall.wall_interaction_diagram_cd(0.9,e_in,0)
        self.line_cd009.set_data(w,p)
        self.line_delta_cd009.set_data(w,d)
        
        w,p,d = self.wall.wall_interaction_diagram_cd(1.0,e_in,0)
        self.line_cd100.set_data(w,p)
        self.line_delta_cd100.set_data(w,d)
        
        w,p,d = self.wall.wall_interaction_diagram_cd(1.15,e_in,0)
        self.line_cd115.set_data(w,p)
        self.line_delta_cd115.set_data(w,d)
        
        w,p,d = self.wall.wall_interaction_diagram_cd(1.25,e_in,0)
        self.line_cd125.set_data(w,p)
        self.line_delta_cd125.set_data(w,d)
        
        w,p,d = self.wall.wall_interaction_diagram_cd(1.6,e_in,0)
        self.line_cd160.set_data(w,p)
        self.line_delta_cd160.set_data(w,d)
        
        w,p,d = self.wall.wall_interaction_diagram_cd(2.0,e_in,0)
        self.line_cd200.set_data(w,p)
        self.line_delta_cd200.set_data(w,d)
        
        if (self.wall.crushing_limit_lbs/(self.wall.spacing_in/12.0)) > 1.2*max(p):
            self.line_pl_cb.set_data([0,0],[0,0])
            self.line_pl_wo_cb.set_data([0,0],[0,0])        
        else:
            self.line_pl_cb.set_data([0,max(w)],[self.wall.crushing_limit_lbs/(self.wall.spacing_in/12.0),self.wall.crushing_limit_lbs/(self.wall.spacing_in/12.0)])
            self.line_pl_wo_cb.set_data([0,max(w)],[self.wall.crushing_limit_lbs_no_cb/(self.wall.spacing_in/12.0),self.wall.crushing_limit_lbs_no_cb/(self.wall.spacing_in/12.0)])
        
        self.line_delta_180.set_data([0,max(w)],[self.wall.height_in/180.0,self.wall.height_in/180.0])
        self.line_delta_240.set_data([0,max(w)],[self.wall.height_in/240.0,self.wall.height_in/240.0])
        self.line_delta_360.set_data([0,max(w)],[self.wall.height_in/360.0,self.wall.height_in/360.0])
        self.line_delta_600.set_data([0,max(w)],[self.wall.height_in/600.0,self.wall.height_in/600.0])
        
        self.ax1.set_xlim(0, max(w)+20)
        self.ax1.set_ylim(0, max(p)+200)
        self.ax2.set_ylim(0, max(d)+0.75)
        
        min_ecc = self.min_ecc_yn.get()
        if min_ecc == 1:
            e_string = ' at min d/6 = {0:.3f} in eccentricity '.format(self.e_in)
        else:
            e_string =''        
        
        self.ax1.set_ylabel('Axial (plf)'+e_string)
        
        self.ax1.set_title(self.title)
        self.canvas.draw()
        
    def generate_pm_graph(self,*event):        
        e_in = self.e_in
        #Refresh chart data for each Cd
        #Cd - NDS 2005 Table 2.3.2
        #cd = [0.9,1.0,1.15,1.25,1.6,2.0]
        w,p,d = self.wall.wall_pm_diagram_cd(0.9,e_in,0)
        self.line_cd009B.set_data(w,p)
        self.line_delta_cd009B.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd(1.0,e_in,0)
        self.line_cd100B.set_data(w,p)
        self.line_delta_cd100B.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd(1.15,e_in,0)
        self.line_cd115B.set_data(w,p)
        self.line_delta_cd115B.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd(1.25,e_in,0)
        self.line_cd125B.set_data(w,p)
        self.line_delta_cd125B.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd(1.6,e_in,0)
        self.line_cd160B.set_data(w,p)
        self.line_delta_cd160B.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd(2.0,e_in,0)
        self.line_cd200B.set_data(w,p)
        self.line_delta_cd200B.set_data(w,d)
        
        if (self.wall.crushing_limit_lbs/(self.wall.spacing_in/12.0)) > 1.2*max(p):
            self.line_pl_cbB.set_data([0,0],[0,0])
            self.line_pl_wo_cbB.set_data([0,0],[0,0])        
        else:
            self.line_pl_cbB.set_data([0,max(w)],[self.wall.crushing_limit_lbs/(self.wall.spacing_in/12.0),self.wall.crushing_limit_lbs/(self.wall.spacing_in/12.0)])
            self.line_pl_wo_cbB.set_data([0,max(w)],[self.wall.crushing_limit_lbs_no_cb/(self.wall.spacing_in/12.0),self.wall.crushing_limit_lbs_no_cb/(self.wall.spacing_in/12.0)])
        
        self.line_delta_180B.set_data([0,max(w)],[self.wall.height_in/180.0,self.wall.height_in/180.0])
        self.line_delta_240B.set_data([0,max(w)],[self.wall.height_in/240.0,self.wall.height_in/240.0])
        self.line_delta_360B.set_data([0,max(w)],[self.wall.height_in/360.0,self.wall.height_in/360.0])
        self.line_delta_600B.set_data([0,max(w)],[self.wall.height_in/600.0,self.wall.height_in/600.0])
        
        self.ax1B.set_xlim(0, max(w)+500)
        self.ax1B.set_ylim(0, max(p)+200)
        self.ax2B.set_ylim(0, max(d)+0.75)
        
        min_ecc = self.min_ecc_yn.get()
        if min_ecc == 1:
            e_string = ' at min d/6 = {0:.3f} in eccentricity '.format(self.e_in)
        else:
            e_string =''        
        
        self.ax1B.set_ylabel('Axial (plf)'+e_string)
        
        self.ax1B.set_title(self.title)
        self.canvasB.draw()
        
        w,p,d = self.wall.wall_pm_diagram_cd_stud(0.9,e_in)
        self.line_cd009D.set_data(w,p)
        self.line_delta_cd009D.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd_stud(1.0,e_in)
        self.line_cd100D.set_data(w,p)
        self.line_delta_cd100D.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd_stud(1.15,e_in)
        self.line_cd115D.set_data(w,p)
        self.line_delta_cd115D.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd_stud(1.25,e_in)
        self.line_cd125D.set_data(w,p)
        self.line_delta_cd125D.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd_stud(1.6,e_in)
        self.line_cd160D.set_data(w,p)
        self.line_delta_cd160D.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd_stud(2.0,e_in)
        self.line_cd200D.set_data(w,p)
        self.line_delta_cd200D.set_data(w,d)
        
        if (self.wall.crushing_limit_lbs) > 1.2*max(p):
            self.line_pl_cbD.set_data([0,0],[0,0])
            self.line_pl_wo_cbD.set_data([0,0],[0,0])        
        else:
            self.line_pl_cbD.set_data([0,max(w)],[self.wall.crushing_limit_lbs,self.wall.crushing_limit_lbs])
            self.line_pl_wo_cbD.set_data([0,max(w)],[self.wall.crushing_limit_lbs_no_cb,self.wall.crushing_limit_lbs_no_cb])
        
        self.line_delta_180D.set_data([0,max(w)],[self.wall.height_in/180.0,self.wall.height_in/180.0])
        self.line_delta_240D.set_data([0,max(w)],[self.wall.height_in/240.0,self.wall.height_in/240.0])
        self.line_delta_360D.set_data([0,max(w)],[self.wall.height_in/360.0,self.wall.height_in/360.0])
        self.line_delta_600D.set_data([0,max(w)],[self.wall.height_in/600.0,self.wall.height_in/600.0])
        
        self.ax1D.set_xlim(0, max(w)+500)
        self.ax1D.set_ylim(0, max(p)+200)
        self.ax2D.set_ylim(0, max(d)+0.75)
        
        min_ecc = self.min_ecc_yn.get()
        if min_ecc == 1:
            e_string = ' at min d/6 = {0:.3f} in eccentricity '.format(self.e_in)
        else:
            e_string =''        
        
        self.ax1D.set_ylabel('Axial (lbs)'+e_string)
        
        self.ax1D.set_title(self.title_pm_stud)
        self.canvasD.draw()
        
    def path_exists(self,path):
        res_folder_exist = os.path.isdir(path)

        if res_folder_exist is False:

            os.makedirs(path)

        else:
            pass

        return 'Directory created'
        
    def save_inputs(self,*event):
        self.run()        
        ##Create a file containing user inputs to be read back in
        #all inputs are single values so write a single input per line
        string = ''
        #Gather inputs
        #geometry
        b = self.b_nom.get()
        string = string + '{0}\n'.format(b)
        d = self.d_nom.get()
        string = string + '{0}\n'.format(d)
        spacing = self.stud_spacing.get()
        string = string + '{0}\n'.format(spacing)
        h = self.wall_height.get()
        string = string + '{0}\n'.format(h)
        sub_pl = self.sub_plates.get()
        string = string + '{0}\n'.format(sub_pl)
        plates = self.num_plates.get()
        string = string + '{0}\n'.format(plates)
        
        #Reference Stud Values
        grade = self.grade.get()
        string = string + '{0}\n'.format(grade)

        #Fb
        fb = self.fb_psi.get()
        string = string + '{0}\n'.format(fb)
        #Fv
        fv = self.fv_psi.get()
        string = string + '{0}\n'.format(fv)
        #Fc
        fc = self.fc_psi.get()
        string = string + '{0}\n'.format(fc)
        #E
        E = self.E_psi.get()
        string = string + '{0}\n'.format(E)
        #Emin
        Emin = self.Emin_psi.get()
        string = string + '{0}\n'.format(Emin)        
        #Fc_perp_pl
        fcperp = self.fc_perp_psi.get()
        string = string + '{0}\n'.format(fcperp)       
        #FRT?
        frtyn = self.frt_yn.get()
        string = string + '{0}\n'.format(frtyn)
        frtfb = self.frt_fb.get()
        string = string + '{0}\n'.format(frtfb)
        frtfv = self.frt_fv.get()
        string = string + '{0}\n'.format(frtfv)
        frtfc = self.frt_fc.get()
        string = string + '{0}\n'.format(frtfc)
        frtfperp = self.frt_fc_perp.get()
        string = string + '{0}\n'.format(frtfperp)
        frtE = self.frt_E.get()
        string = string + '{0}\n'.format(frtE)
        frtEmin = self.frt_Emin.get()
        string = string + '{0}\n'.format(frtEmin)
        species = self.species .get()
        string = string + '{0}\n'.format(species)
        #Moisture %
        moist = self.moisture.get()   
        string = string + '{0}\n'.format(moist)       
        #Temp F
        temp= self.temp.get()
        string = string + '{0}\n'.format(temp)        
        #Incised?
        inc = self.incised_yn.get()
        string = string + '{0}\n'.format(inc)
        
        p = self.pressure.get()
        string = string + '{0}\n'.format(p)
        cd = self.cd.get()
        string = string + '{0}\n'.format(cd)
        e = self.min_ecc_yn.get()
        string = string + '{0}\n'.format(e)
        
        label = '{0}x{1}_height-{2}_ft_pressure-{3}_psf_Cd-{4}'.format(b,d,h,p,cd)
        path = os.path.join(os.path.expanduser('~'),'Desktop','RESULTS','Wood_Walls', label)
        self.path_exists(path)
        
        name = label+'_inputs.wdwall'
        
        file = open(os.path.join(path,name),'w')
        file.write(string)
        file.close()
        
    def file_open(self):
        filename = tkFileDialog.askopenfilename()
        in_file = open(filename,'r')
        in_data = in_file.readlines()
        in_file.close()
        
        b = in_data[0].rstrip('\n')
        self.b_nom.set(b)
        d = in_data[1].rstrip('\n')
        self.d_nom.set(d)
        spacing = in_data[2].rstrip('\n')
        self.stud_spacing.set(spacing)
        h = in_data[3].rstrip('\n')
        self.wall_height.set(h)
        sub_pl = in_data[4].rstrip('\n')
        self.sub_plates.set(sub_pl)
        plates = in_data[5].rstrip('\n')
        self.num_plates.set(plates)
        
        #Reference Stud Values
        grade = in_data[6].rstrip('\n')
        self.grade.set(grade)

        #Fb
        fb = in_data[7].rstrip('\n')
        self.fb_psi.set(fb)
        #Fv
        fv = in_data[8].rstrip('\n')
        self.fv_psi.set(fv)
        #Fc
        fc = in_data[9].rstrip('\n')
        self.fc_psi.set(fc)
        #E
        E = in_data[10].rstrip('\n')
        self.E_psi.set(E)

        #Emin
        Emin = in_data[11].rstrip('\n')
        self.Emin_psi.set(Emin)        
        #Fc_perp_pl
        fcperp = in_data[12].rstrip('\n')
        self.fc_perp_psi.set(fcperp)
       
        #FRT?
        frtyn = in_data[13].rstrip('\n')
        self.frt_yn.set(frtyn)

        frtfb = in_data[14].rstrip('\n')
        self.frt_fb.set(frtfb)

        frtfv = in_data[15].rstrip('\n')
        self.frt_fv.set(frtfv)

        frtfc = in_data[16].rstrip('\n')
        self.frt_fc.set(frtfc)

        frtfperp = in_data[17].rstrip('\n')
        self.frt_fc_perp.set(frtfperp)

        frtE = in_data[18].rstrip('\n')
        self.frt_E.set(frtE)

        frtEmin = in_data[19].rstrip('\n')
        self.frt_Emin.set(frtEmin)

        species = in_data[20].rstrip('\n')
        self.species.set(species)

        #Moisture %
        moist = in_data[21].rstrip('\n')
        self.moisture.set(moist)   
       
        #Temp F
        temp= in_data[22].rstrip('\n')
        self.temp.set(temp)
       
        #Incised?
        inc = in_data[23].rstrip('\n')
        self.incised_yn.set(inc)

        
        p = in_data[24].rstrip('\n')
        self.pressure.set(p)

        cd = in_data[25].rstrip('\n')
        self.cd.set(cd)

        e = in_data[26].rstrip('\n')
        self.min_ecc_yn.set(e)
        
        self.run()
        
    def write_text_results_to_file(self,*event):
        #generate file name and confirm path exists if not create it
        b = self.b_nom.get()
        d = self.d_nom.get()
        h = self.wall_height.get()
        p = self.pressure.get()
        cd = self.cd.get()
        min_ecc = self.min_ecc_yn.get()
        if min_ecc == 1:
            e_string_file = '-Axial_Ecc_Included'
        else:
            e_string_file =''
            
        label = '{0}x{1}_height-{2}_ft_pressure-{3}_psf_Cd-{4}'.format(b,d,h,p,cd)
        path = os.path.join(os.path.expanduser('~'),'Desktop','RESULTS','Wood_Walls', label)
        self.path_exists(path)
        
        name = label+e_string_file+'_results.txt'
        output = self.results_text_box.get(1.0,tk.END)
        #file = open(os.path.join(path,name),'w')
        #file.write(output)
        #file.close()
        
        name_nds_table = label+e_string_file+'_nds_load_factor_table.csv'
        string = ''
        for i in range(len(self.res_nds_table_output)):
            string = string + '{0},'.format(self.res_nds_table_output[i])
        file = open(os.path.join(path,name_nds_table),'w')
        file.write(string)
        file.write('\n')
        file.write(output)
        file.close()
    
    def print_pm_graph_common(self,*event):
        b = self.b_actual
        d = self.d_actual
        h = self.wall_height.get()
        p = self.pressure.get()
        cd = self.cd.get()
        grade = self.grade.get()
        label = '{0}x{1}_height-{2}_ft_pressure-{3}_psf_Cd-{4}'.format(self.b_nom.get(),self.d_nom.get(),h,p,cd)
        path = os.path.join(os.path.expanduser('~'),'Desktop','RESULTS','Wood_Walls', label,'PvM_Charts')
        self.path_exists(path)
        
        #initialize plot
        pmfig, ax1C = plt.subplots(figsize=(17,11), dpi=600)
        ax1C.minorticks_on()
        ax1C.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
        ax1C.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
        ax2C=ax1C.twinx()
        #Prebuild chart lines so data can be refreshed to cut down on render time
        #['0.9','1.0','1.15','1.25','1.6','2.0']
        line_cd009C, = ax1C.plot([0,10],[10,0], label='Cd = 0.9')
        line_cd100C, = ax1C.plot([0,15],[15,0], label='Cd = 1.0')
        line_cd115C, = ax1C.plot([0,25],[25,0], label='Cd = 1.15')
        line_cd125C, = ax1C.plot([0,35],[35,0], label='Cd = 1.25')
        line_cd160C, = ax1C.plot([0,50],[50,0], label='Cd = 1.6')
        line_cd200C, = ax1C.plot([0,75],[75,0], label='Cd = 2.0')
        line_pl_cbC, = ax1C.plot([0,10],[3,3], label='PL Crushing')
        line_pl_wo_cbC, = ax1C.plot([0,10],[1.5,1.5], label='PL Crushing w/o Cb')
        line_delta_cd009C, = ax2C.plot([0,10],[0,13], label='D - Cd = 0.9')
        line_delta_cd100C, = ax2C.plot([0,15],[15,0], label='D - Cd = 1.0')
        line_delta_cd115C, = ax2C.plot([0,25],[25,0], label='D - Cd = 1.15')
        line_delta_cd125C, = ax2C.plot([0,35],[35,0], label='D - Cd = 1.25')
        line_delta_cd160C, = ax2C.plot([0,50],[50,0], label='D - Cd = 1.6')
        line_delta_cd200C, = ax2C.plot([0,75],[75,0], label='D - Cd = 2.0')
        self.line_delta_180C, = ax2C.plot([6,6],[0,13], label='H/180', linestyle=':')
        self.line_delta_240C, = ax2C.plot([4,4],[0,13], label='H/240', linestyle=':')
        self.line_delta_360C, = ax2C.plot([1,1],[0,13], label='H/360', linestyle=':')
        self.line_delta_600C, = ax2C.plot([1,1],[0,13], label='H/600', linestyle=':')

        legend_ax1C = ax1C.legend(loc=1, fontsize='x-small')
        legend_ax2C = ax2C.legend(loc=4, fontsize='x-small')
        
        min_ecc = self.min_ecc_yn.get()
        if min_ecc == 1:
            e_string = ' at min d/6 = {0:.3f} in eccentricity '.format(self.e_in)
            e_string_file = '-Axial_Ecc_Included'
        else:
            e_string =''
            e_string_file =''
            
        ax1C.set_ylabel('Axial (plf)'+e_string)
        ax1C.set_xlabel('Moment (in-lbs)')
        ax2C.set_ylabel('Mid Height Deflection (in)')
        
        
        spacings = [4,6,8,12,16,24]
        for s in spacings:
            file = '{0}x{1}_height-{2}_ft_Spacing_{3}_in-PvM_chart_11x17{4}.pdf'.format(self.b_nom.get(),self.d_nom.get(),h,s,e_string_file)
            title = '{0}x{1} ({2:.2f}x{3:.2f})- Height:{4} ft - Species: {7} - Grade: {5} - Spacing: {6} in'.format(self.b_nom.get(),self.d_nom.get(),self.b_actual,self.d_actual,h,grade,s, self.species.get())
            e_in = self.e_in
            #Refresh chart data for each Cd
            #Cd - NDS 2005 Table 2.3.2
            #cd = [0.9,1.0,1.15,1.25,1.6,2.0]
            w,p,d = self.wall.wall_pm_diagram_cd(0.9,e_in,s)
            line_cd009C.set_data(w,p)
            line_delta_cd009C.set_data(w,d)
            
            w,p,d = self.wall.wall_pm_diagram_cd(1.0,e_in,s)
            line_cd100C.set_data(w,p)
            line_delta_cd100C.set_data(w,d)
            
            w,p,d = self.wall.wall_pm_diagram_cd(1.15,e_in,s)
            line_cd115C.set_data(w,p)
            line_delta_cd115C.set_data(w,d)
            
            w,p,d = self.wall.wall_pm_diagram_cd(1.25,e_in,s)
            line_cd125C.set_data(w,p)
            line_delta_cd125C.set_data(w,d)
            
            w,p,d = self.wall.wall_pm_diagram_cd(1.6,e_in,s)
            line_cd160C.set_data(w,p)
            line_delta_cd160C.set_data(w,d)
            
            w,p,d = self.wall.wall_pm_diagram_cd(2.0,e_in,s)
            line_cd200C.set_data(w,p)
            line_delta_cd200C.set_data(w,d)
            
            if (self.wall.crushing_limit_lbs/(s/12.0)) > 1.2*max(p):
                line_pl_cbC.set_data([0,0],[0,0])
                line_pl_wo_cbC.set_data([0,0],[0,0])        
            else:
                line_pl_cbC.set_data([0,max(w)],[self.wall.crushing_limit_lbs/(s/12.0),self.wall.crushing_limit_lbs/(s/12.0)])
                line_pl_wo_cbC.set_data([0,max(w)],[self.wall.crushing_limit_lbs_no_cb/(s/12.0),self.wall.crushing_limit_lbs_no_cb/(s/12.0)])
            
            self.line_delta_180C.set_data([0,max(w)],[self.wall.height_in/180.0,self.wall.height_in/180.0])
            self.line_delta_240C.set_data([0,max(w)],[self.wall.height_in/240.0,self.wall.height_in/240.0])
            self.line_delta_360C.set_data([0,max(w)],[self.wall.height_in/360.0,self.wall.height_in/360.0])
            self.line_delta_600C.set_data([0,max(w)],[self.wall.height_in/600.0,self.wall.height_in/600.0])
            
            ax1C.set_xlim(0, max(w)+500)
            ax1C.set_ylim(0, max(p)+200)
            ax2C.set_ylim(0, max(d)+0.75)
            
            ax1C.set_title(title)
            
            pmfig.savefig(os.path.join(path,file))
            
        file = '{0}x{1}_height-{2}_ft-PvM_chart_per_Stud_11x17{3}.pdf'.format(self.b_nom.get(),self.d_nom.get(),h,e_string_file)
        title = '{0}x{1} ({2:.2f}x{3:.2f})- Height:{4} ft - Species: {6} - Grade: {5}'.format(self.b_nom.get(),self.d_nom.get(),self.b_actual,self.d_actual,h,grade, self.species.get())
        e_in = self.e_in
        #Refresh chart data for each Cd
        #Cd - NDS 2005 Table 2.3.2
        #cd = [0.9,1.0,1.15,1.25,1.6,2.0]
        w,p,d = self.wall.wall_pm_diagram_cd_stud(0.9,e_in)
        line_cd009C.set_data(w,p)
        line_delta_cd009C.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd_stud(1.0,e_in)
        line_cd100C.set_data(w,p)
        line_delta_cd100C.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd_stud(1.15,e_in)
        line_cd115C.set_data(w,p)
        line_delta_cd115C.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd_stud(1.25,e_in)
        line_cd125C.set_data(w,p)
        line_delta_cd125C.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd_stud(1.6,e_in)
        line_cd160C.set_data(w,p)
        line_delta_cd160C.set_data(w,d)
        
        w,p,d = self.wall.wall_pm_diagram_cd_stud(2.0,e_in)
        line_cd200C.set_data(w,p)
        line_delta_cd200C.set_data(w,d)
        
        if (self.wall.crushing_limit_lbs) > 1.2*max(p):
            line_pl_cbC.set_data([0,0],[0,0])
            line_pl_wo_cbC.set_data([0,0],[0,0])        
        else:
            line_pl_cbC.set_data([0,max(w)],[self.wall.crushing_limit_lbs,self.wall.crushing_limit_lbs])
            line_pl_wo_cbC.set_data([0,max(w)],[self.wall.crushing_limit_lbs_no_cb,self.wall.crushing_limit_lbs_no_cb])
        
        self.line_delta_180C.set_data([0,max(w)],[self.wall.height_in/180.0,self.wall.height_in/180.0])
        self.line_delta_240C.set_data([0,max(w)],[self.wall.height_in/240.0,self.wall.height_in/240.0])
        self.line_delta_360C.set_data([0,max(w)],[self.wall.height_in/360.0,self.wall.height_in/360.0])
        self.line_delta_600C.set_data([0,max(w)],[self.wall.height_in/600.0,self.wall.height_in/600.0])
        
        ax1C.set_xlim(0, max(w)+500)
        ax1C.set_ylim(0, max(p)+200)
        ax2C.set_ylim(0, max(d)+0.75)
        
        ax1C.set_ylabel('Axial (lbs)'+e_string)
        ax1C.set_title(title)
        
        pmfig.savefig(os.path.join(path,file))       
        plt.close('all')
        
    def print_pp_graph_common(self,*event):
        b = self.b_actual
        d = self.d_actual
        h = self.wall_height.get()
        p = self.pressure.get()
        cd = self.cd.get()
        grade = self.grade.get()
        label = '{0}x{1}_height-{2}_ft_pressure-{3}_psf_Cd-{4}'.format(self.b_nom.get(),self.d_nom.get(),h,p,cd)
        path = os.path.join(os.path.expanduser('~'),'Desktop','RESULTS','Wood_Walls', label,'PvPressure_Charts')
        self.path_exists(path)
        
        #initialize plot
        pmfig, ax1C = plt.subplots(figsize=(17,11), dpi=600)
        ax1C.minorticks_on()
        ax1C.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
        ax1C.grid(b=True, which='minor', color='g', linestyle='-', alpha=0.1)
        ax2C=ax1C.twinx()
        #Prebuild chart lines so data can be refreshed to cut down on render time
        #['0.9','1.0','1.15','1.25','1.6','2.0']
        line_cd009C, = ax1C.plot([0,10],[10,0], label='Cd = 0.9')
        line_cd100C, = ax1C.plot([0,15],[15,0], label='Cd = 1.0')
        line_cd115C, = ax1C.plot([0,25],[25,0], label='Cd = 1.15')
        line_cd125C, = ax1C.plot([0,35],[35,0], label='Cd = 1.25')
        line_cd160C, = ax1C.plot([0,50],[50,0], label='Cd = 1.6')
        line_cd200C, = ax1C.plot([0,75],[75,0], label='Cd = 2.0')
        line_pl_cbC, = ax1C.plot([0,10],[3,3], label='PL Crushing')
        line_pl_wo_cbC, = ax1C.plot([0,10],[1.5,1.5], label='PL Crushing w/o Cb')
        line_delta_cd009C, = ax2C.plot([0,10],[0,13], label='D - Cd = 0.9')
        line_delta_cd100C, = ax2C.plot([0,15],[15,0], label='D - Cd = 1.0')
        line_delta_cd115C, = ax2C.plot([0,25],[25,0], label='D - Cd = 1.15')
        line_delta_cd125C, = ax2C.plot([0,35],[35,0], label='D - Cd = 1.25')
        line_delta_cd160C, = ax2C.plot([0,50],[50,0], label='D - Cd = 1.6')
        line_delta_cd200C, = ax2C.plot([0,75],[75,0], label='D - Cd = 2.0')
        self.line_delta_180C, = ax2C.plot([6,6],[0,13], label='H/180', linestyle=':')
        self.line_delta_240C, = ax2C.plot([4,4],[0,13], label='H/240', linestyle=':')
        self.line_delta_360C, = ax2C.plot([1,1],[0,13], label='H/360', linestyle=':')
        self.line_delta_600C, = ax2C.plot([1,1],[0,13], label='H/600', linestyle=':')

        legend_ax1C = ax1C.legend(loc=1, fontsize='x-small')
        legend_ax2C = ax2C.legend(loc=4, fontsize='x-small')
        
        min_ecc = self.min_ecc_yn.get()
        if min_ecc == 1:
            e_string = ' at min d/6 = {0:.3f} in eccentricity '.format(self.e_in)
            e_string_file = '-Axial_Ecc_Included'
        else:
            e_string =''
            e_string_file =''
            
        ax1C.set_ylabel('Axial (plf)'+e_string)
        ax1C.set_xlabel('Pressure (psf)')
        ax2C.set_ylabel('Mid Height Deflection (in)')
        
        
        spacings = [4,6,8,12,16,24]
        for s in spacings:
            file = '{0}x{1}_height-{2}_ft_Spacing_{3}_in-PvP_chart_11x17{4}.pdf'.format(self.b_nom.get(),self.d_nom.get(),h,s,e_string_file)
            title = '{0}x{1} ({2:.2f}x{3:.2f})- Height:{4} ft - Species: {7} - Grade: {5} - Spacing: {6} in'.format(self.b_nom.get(),self.d_nom.get(),self.b_actual,self.d_actual,h,grade,s, self.species.get())
            e_in = self.e_in
            #Refresh chart data for each Cd
            #Cd - NDS 2005 Table 2.3.2
            #cd = [0.9,1.0,1.15,1.25,1.6,2.0]
            w,p,d = self.wall.wall_interaction_diagram_cd(0.9,e_in,s)
            line_cd009C.set_data(w,p)
            line_delta_cd009C.set_data(w,d)
            
            w,p,d = self.wall.wall_interaction_diagram_cd(1.0,e_in,s)
            line_cd100C.set_data(w,p)
            line_delta_cd100C.set_data(w,d)
            
            w,p,d = self.wall.wall_interaction_diagram_cd(1.15,e_in,s)
            line_cd115C.set_data(w,p)
            line_delta_cd115C.set_data(w,d)
            
            w,p,d = self.wall.wall_interaction_diagram_cd(1.25,e_in,s)
            line_cd125C.set_data(w,p)
            line_delta_cd125C.set_data(w,d)
            
            w,p,d = self.wall.wall_interaction_diagram_cd(1.6,e_in,s)
            line_cd160C.set_data(w,p)
            line_delta_cd160C.set_data(w,d)
            
            w,p,d = self.wall.wall_interaction_diagram_cd(2.0,e_in,s)
            line_cd200C.set_data(w,p)
            line_delta_cd200C.set_data(w,d)
            
            if (self.wall.crushing_limit_lbs/(s/12.0)) > 1.2*max(p):
                line_pl_cbC.set_data([0,0],[0,0])
                line_pl_wo_cbC.set_data([0,0],[0,0])        
            else:
                line_pl_cbC.set_data([0,max(w)],[self.wall.crushing_limit_lbs/(s/12.0),self.wall.crushing_limit_lbs/(s/12.0)])
                line_pl_wo_cbC.set_data([0,max(w)],[self.wall.crushing_limit_lbs_no_cb/(s/12.0),self.wall.crushing_limit_lbs_no_cb/(s/12.0)])
                
            self.line_delta_180C.set_data([0,max(w)],[self.wall.height_in/180.0,self.wall.height_in/180.0])
            self.line_delta_240C.set_data([0,max(w)],[self.wall.height_in/240.0,self.wall.height_in/240.0])
            self.line_delta_360C.set_data([0,max(w)],[self.wall.height_in/360.0,self.wall.height_in/360.0])
            self.line_delta_600C.set_data([0,max(w)],[self.wall.height_in/600.0,self.wall.height_in/600.0])
            
            ax1C.set_xlim(0, max(w)+20)
            ax1C.set_ylim(0, max(p)+200)
            ax2C.set_ylim(0, max(d)+0.75)
            
            ax1C.set_title(title)
            
            pmfig.savefig(os.path.join(path,file))
        
        plt.close('all')
        
    def run_user_loads(self, *event):
        #Initialize the "No Good" Count
        ng_count = 0
        
        #Get New user defined spacing from user load tab
        s_in = float(self.user_calc_spacing.get())
        
        #Check that spacing is greater than the stud width
        if s_in<self.wall.b_in:
            tkMessageBox.showerror("ERROR!!","Spacing is less than wall stud width.")
        else:
            pass
        
        #Initialize the output strings - used to make exporting the results easier
        self.user_load_res_string_output = ''
        self.user_vert_load_string = '\nVertical Loads:\n'
        self.user_lat_load_string = 'Lateral Loads:\n'
        
        e = self.e_in
        loads_plf = []
        loads_lbs = []
        grav_delta = []
        grav_shear = []
        
        
        #Wall Self Weight to be added to DL
        self.user_vert_load_string = self.user_vert_load_string + 'Self Weight: ,{0}, psf x ,{1}, ft = '.format(self.user_sw.get(),self.user_sw_height_ft.get())
        
        sw_plf = float(self.user_sw.get())*float(self.user_sw_height_ft.get())

        self.user_sw_label.configure(text='ft = {0:.3f} plf'.format(sw_plf))
        self.user_vert_load_string = self.user_vert_load_string + ',{0:.2f}, plf\n'.format(sw_plf)
        
        sw_lbs = sw_plf*(s_in/12.0)
        sw_delta = 0
        sw_shear = 0
        
        i=0
        for load in self.user_vert_loads_psf:
            self.user_vert_load_string = self.user_vert_load_string + '{0} ,{1}, psf x ,{2}, ft = '.format(self.user_vert_load_labels[i],load.get(),self.user_vert_loads_trib[i].get())
            
            load_psf = float(load.get())
            load_trib = float(self.user_vert_loads_trib[i].get())
            loads_plf.append(load_psf * load_trib)
            loads_lbs.append(loads_plf[i]*(s_in/12.0))
            
            self.user_load_trib_plf_label[i].configure(text='ft = {0:.3f} plf @ e = {1:.3f} in'.format(loads_plf[i],e))
            self.user_vert_load_string = self.user_vert_load_string + ',{0:.3f}, plf @ e = ,{1:.3f}, in\n'.format(loads_plf[i], e)
            
            grav_delta.append(((loads_lbs[i]*e)*self.wall.height_in**2)/(16.0*self.wall.E_prime_psi*self.wall.I_in4))
            grav_shear.append((loads_lbs[i]*e) / self.wall.height_in)
            i+=1
        loads_lbs.append(0)
        grav_delta.append(0)
        grav_shear.append(0)
        
        loads_lbs[0] = loads_lbs[0] + sw_lbs
        grav_delta[0] = grav_delta[0] + sw_delta
        grav_shear[0] = grav_shear[0] + sw_shear
        
        lat_plf = []
        lat_inlbs = []
        lat_delta = []
        lat_shear = []
        i=0
        for lat_load in self.user_lat_loads_psf:
            
            lat_load_psf = float(lat_load.get())
            lat_plf.append(lat_load_psf*(s_in/12.0))
            
            self.user_lat_load_string = self.user_lat_load_string + '{0} ,{1}, psf x ,{2:.2f}, in x 1/12 ft/in = ,{3:.2f}, plf\n'.format(self.user_lat_load_labels[i],lat_load.get(),s_in,lat_plf[i])
            
            lat_inlbs.append(((lat_plf[i]*((self.wall.height_in)/12.0)**2)/8.0)*12.0)
            lat_delta.append((1728*5*lat_plf[i]*(self.wall.height_in/12.0)**4)/(384*self.wall.E_prime_psi*self.wall.I_in4))
            lat_shear.append((((lat_plf[i]*(self.wall.height_in))/12.0)/2.0))
            i+=1
        
        i=0
        p_plot = []
        m_plot = []
        d_plot = []
        ratio_text = ''
        for combo in self.load_combos:
            self.user_load_res_string_output = self.user_load_res_string_output + '{0},{1},'.format(combo[0],combo[1])
            fc_prime = self.wall.fc_prime_calc(combo[1])
            fb_prime = self.wall.fb_prime_calc(combo[1])
            fv_prime = self.wall.fv_prime_psi_cd
            
            p = 0
            m = 0
            v = 0
            delta = 0
            for c in range(2,8):
                p = p + (loads_lbs[c-2]*combo[c])
                delta = delta + (grav_delta[c-2]*combo[c])
                v = v + (grav_shear[c-2]*combo[c])
                
                if c == 3:
                    m = m + (lat_inlbs[0]*combo[c])
                    delta = delta + (lat_delta[0]*combo[c])
                    v = v + (lat_shear[0]*combo[c])
                    
                elif c == 7:
                    m = m + (lat_inlbs[1]*combo[c])
                    delta = delta + (lat_delta[1]*combo[c])
                    v = v + (lat_shear[1]*combo[c])
                else:
                    m = m
                    delta = delta
                    v = v
            
            fc = p / self.wall.area_in2
            fb = m / self.wall.s_in3
            fv = (3.0 * v) / (2.0*self.wall.b_in*self.wall.d_in)
            if delta == 0:
                delta_ratio = 0
            else:
                delta_ratio = self.wall.height_in/delta
            if e == 0:
                if m==0:
                    ratio = fc/fc_prime
                    ratio_text = " (fc/Fc')"
                elif p==0:
                    ratio = fb/fb_prime
                    ratio_text = " (fb/Fb')"
                else:
                    if fc/self.wall.fcE_psi > 1.0:
                        ratio = 100
                        ratio_text = " (fc > FcE)"
                    else:
                        ratio = (fc/fc_prime)**2 + (fb / (fb_prime*(1-(fc/self.wall.fcE_psi))))
                        ratio_text = " (3.9-3)"
                
                ratio_v = fv / fv_prime
                ratio = max(ratio,ratio_v)
                
                if ratio == ratio_v:
                    ratio_text = " (fv/Fv')"
                else:
                    ratio_text = ratio_text
                
            else:
                if fc/self.wall.fcE_psi > 1.0:
                    ratio = 100
                    ratio_text = " (fc > FcE)"
                else:
                    ratio = (fc/fc_prime)**2 + ((fb+(fc*(6*e/self.wall.d_in)*(1+(0.234*(fc/self.wall.fcE_psi)))))/ (fb_prime*(1-(fc/self.wall.fcE_psi))))
                    ratio_text = " (15.4-1)"
                ratio_v = fv / fv_prime
                ratio = max(ratio,ratio_v)
                if ratio == ratio_v:
                    ratio_text = " (fv/Fv')"
                else:
                    ratio_text = ratio_text
            
            if ratio > 1.0 or s_in<self.wall.b_in:
                user_status = 'NG'
                ng_count = ng_count +1
            else:
                user_status = 'OK'
                ng_count = ng_count
            
            if p > self.wall.crushing_limit_lbs:
                self.user_p_res_labels[i].configure(text='{0:.2f}**'.format(p))
                self.user_load_res_string_output = self.user_load_res_string_output + '{0:.2f}**,'.format(p)
            elif p > self.wall.crushing_limit_lbs_no_cb:
                self.user_p_res_labels[i].configure(text='{0:.2f}*'.format(p))
                self.user_load_res_string_output = self.user_load_res_string_output + '{0:.2f}*,'.format(p)
            else:
                self.user_p_res_labels[i].configure(text='{0:.2f}'.format(p))
                self.user_load_res_string_output = self.user_load_res_string_output + '{0:.2f},'.format(p)
                
            self.user_fc_res_labels[i].configure(text='{0:.3f}'.format(fc))
            self.user_load_res_string_output = self.user_load_res_string_output + '{0:.3f},'.format(fc)
            
            self.user_kel_res_labels[i].configure(text='{0:.2f}'.format(self.wall.height_in/self.wall.d_in))
            self.user_load_res_string_output = self.user_load_res_string_output + '{0:.2f},'.format(self.wall.height_in/self.wall.d_in)
            
            self.user_FcE_res_labels[i].configure(text='{0:.2f}'.format(self.wall.fcE_psi))
            self.user_load_res_string_output = self.user_load_res_string_output + '{0:.2f},'.format(self.wall.fcE_psi)
            
            self.user_c_labels[i].configure(text='{0:.1f}'.format(self.wall.c_cp))
            self.user_load_res_string_output = self.user_load_res_string_output + '{0:.1f},'.format(self.wall.c_cp)
            
            self.user_cp_labels[i].configure(text='{0:.3f}'.format(self.wall.cp))
            self.user_load_res_string_output = self.user_load_res_string_output + '{0:.3f},'.format(self.wall.cp)
            
            self.user_fcprime_res_labels[i].configure(text='{0:.2f}'.format(fc_prime))
            self.user_load_res_string_output = self.user_load_res_string_output + '{0:.2f},'.format(fc_prime)
            
            self.user_fc_fc_res_labels[i].configure(text='{0:.3f}'.format(fc/fc_prime))
            self.user_load_res_string_output = self.user_load_res_string_output + '{0:.3f},'.format(fc/fc_prime)
            
            self.user_m_res_labels[i].configure(text='{0:.2f}'.format(m))
            self.user_load_res_string_output = self.user_load_res_string_output + '{0:.2f},'.format(m)
            
            self.user_fb_res_labels[i].configure(text='{0:.3f}'.format(fb))
            self.user_load_res_string_output = self.user_load_res_string_output + '{0:.3f},'.format(fb)
            
            self.user_fbprime_res_labels[i].configure(text='{0:.2f}'.format(fb_prime))
            self.user_load_res_string_output = self.user_load_res_string_output + '{0:.2f},'.format(fb_prime)
            
            self.user_fb_fb_res_labels[i].configure(text='{0:.3f}'.format(fb/fb_prime))
            self.user_load_res_string_output = self.user_load_res_string_output + '{0:.3f},'.format(fb/fb_prime)
            
            self.user_v_res_labels[i].configure(text='{0:.2f}'.format(v))
            self.user_load_res_string_output = self.user_load_res_string_output + '{0:.2f},'.format(v)
            
            self.user_fv_res_labels[i].configure(text='{0:.2f}'.format(fv))
            self.user_load_res_string_output = self.user_load_res_string_output + '{0:.2f},'.format(fv)
            
            self.user_fvprime_res_labels[i].configure(text='{0:.2f}'.format(fv_prime))
            self.user_load_res_string_output = self.user_load_res_string_output + '{0:.2f},'.format(fv_prime)
            
            self.user_fv_fv_res_labels[i].configure(text='{0:.3f}'.format(fv/fv_prime))
            self.user_load_res_string_output = self.user_load_res_string_output + '{0:.3f},'.format(fv/fv_prime)
            
            self.user_ratio_res_labels[i].configure(text='{0:.3f}{1}'.format(ratio,ratio_text))
            self.user_load_res_string_output = self.user_load_res_string_output + '{0:.3f}{1},'.format(ratio,ratio_text)
            
            self.user_deltaratio_res_labels[i].configure(text='{1:.3f} in (H/{0:.1f})'.format(delta_ratio,delta))
            self.user_load_res_string_output = self.user_load_res_string_output +'{1:.3f} in (H/{0:.1f}),'.format(delta_ratio,delta)
            
            if user_status == 'OK':
                self.user_status_res_labels[i].configure(text='{0}'.format(user_status),background='green')
            else:
                self.user_status_res_labels[i].configure(text='{0}'.format(user_status),background='red')
            self.user_load_res_string_output = self.user_load_res_string_output + '{0}\n'.format(user_status)
                        
            p_plot.append(p)
            m_plot.append(m)
            d_plot.append(delta)
            
            i+=1
        
        self.user_pmD.set_data(m_plot,p_plot)
        self.user_mdD.set_data(m_plot,d_plot)
        
        self.canvasD.draw()
        
        if ng_count > 0:
            return 1
        else:
            return 0
        
            
        
    def solve_user_loads(self, *event):
        #optimize spacing
        a=0
        b=24 #upper bound limit on spacing for Cr=1.15
        c=0
        
        loop_max = 500
        tol = 0.0001
        loop = 0
        self.user_calc_spacing.set(b)
        check = self.run_user_loads()
        if check == 0:
            self.user_calc_spacing.set(b)
            self.run_user_loads()
        else:
            while loop<loop_max:
                c = (a+b)/2.0
                self.user_calc_spacing.set(c)
                
                check = self.run_user_loads()
                
                if check == 0 :
                    a = c
                else:
                    b = c
                    
                if (b-a)/2.0 <= tol:
                    loop = loop_max
                    c = math.floor(c*4)/4                
                    self.user_calc_spacing.set(c)
                    self.run_user_loads()
                elif c<self.wall.b_in:
                    loop = loop_max
                    self.user_calc_spacing.set(0)
                    self.run_user_loads()

                else:
                    loop+=1
    def export_user_load_results(self,*event):
        #Run the user loads so export results are always current
        self.run_user_loads()
        
        #Get New user defined spacing from user load tab
        s_in = float(self.user_calc_spacing.get())
        
        #generate file name and confirm path exists if not create it
        b = self.b_nom.get()
        d = self.d_nom.get()
        h = self.wall_height.get()
        p = self.pressure.get()
        cd = self.cd.get()
        grade = self.grade.get()
        min_ecc = self.min_ecc_yn.get()
        if min_ecc == 1:
            e_string_file = '-Axial_Ecc_Included'
        else:
            e_string_file =''
            
        label = '{0}x{1}_height-{2}_ft_pressure-{3}_psf_Cd-{4}'.format(b,d,h,p,cd)
        path = os.path.join(os.path.expanduser('~'),'Desktop','RESULTS','Wood_Walls', label)
        self.path_exists(path)
        
        name = label+e_string_file+'_user_load_results.csv'
        chart = label+e_string_file+'_user_load_results_nomograph.jpg'
        
        self.FigD.savefig(os.path.join(path,chart))
        
        title = 'Nominal: ,{0},x,{1}, Height:,{4}, ft, Species:, {6} ,Grade:, {5}\nActual: ,{2:.2f}, in x,{3:.2f}, in\n'.format(self.b_nom.get(),self.d_nom.get(),self.b_actual,self.d_actual,h,grade, self.species.get())
        
        file = open(os.path.join(path,name),'w')
        file.write('User Load Results - IBC 2012 - ASD\n')
        file.write(title)
        file.write('Design Stud Spacing: ,{0:.3f}, in\n'.format(s_in))
        file.write(self.user_vert_load_string+'\n')      
        file.write(self.user_lat_load_string+'\n')
        file.write("Combo:,Cd,P (lbs), fc (psi),Ke Le_d/d,FcE (psi),c,Cp,Fc' (psi),fc/Fc',M_lat (in-lbs),fb_lat (psi),Fb' (psi),fb/Fb',V (lbs),fv (psi),Fv' (psi),fv/Fv',Ratio,D (H/--),Status\n")
        file.write(self.user_load_res_string_output)
        file.write('* - indicates load greater than wall plate crushing w/o Cb - {0:.3f} lbs\n'.format(self.wall.crushing_limit_lbs_no_cb))
        file.write('** - indicates load greater than wall plate crushing w/ Cb - {0:.3f} lbs\n'.format(self.wall.crushing_limit_lbs))
        file.write('\n'+self.wall.assumptions)
        file.close()
        
        
def main():            
    root = tk.Tk()
    root.title("Wood Stud Wall - 2-4x Studs - North American Species (Not Southern Pine) - V0.9 BETA")
    Master_window(root)
    root.minsize(1024,700)
    root.mainloop()

if __name__ == '__main__':
    main()   

            

