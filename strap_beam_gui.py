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
import math as m
import Analysis.pin_pin_beam_equations_classes as ppbeam
import Concrete.concrete_beam_classes as concbeam
from numpy import zeros
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter.messagebox as tkMessageBox
import tkinter.filedialog as tkFileDialog

class main_window:

    def __init__(self, master):

        self.master = master

        self.shearl_s = zeros(10)
        self.shearc_s = zeros(10)
        self.shearr_s = zeros(10)

        self.momentl_s = zeros(10)
        self.momentc_s = zeros(10)
        self.momentr_s = zeros(10)

        self.shearl_u = zeros(10)
        self.shearc_u = zeros(10)
        self.shearr_u = zeros(10)

        self.momentl_u = zeros(10)
        self.momentc_u = zeros(10)
        self.momentr_u = zeros(10)

        self.xsl = zeros(10)
        self.xsc = zeros(10)
        self.xsr = zeros(10)

        self.ll = 4
        self.lc = 4
        self.lr = 4

        self.static_run = 0
        
        self.inputs = []
        
        self.f_size = 8
        self.helv = tkFont.Font(family=' Courier New',size=self.f_size, weight='bold')
        self.helv_norm = tkFont.Font(family=' Courier New',size=self.f_size)
        self.helv_res = tkFont.Font(family=' Courier New',size=self.f_size, weight='bold', underline = True)

        self.menubar = tk.Menu(self.master)
        self.menu = tk.Menu(self.menubar, tearoff=0)
        self.menu_props = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label = "File", menu=self.menu)
        self.menu.add_command(label="Save", command=self.save_inputs)
        self.menu.add_command(label="Open", command=self.open_existing)
        self.menu.add_separator()
        self.menu.add_command(label="Quit", command=self.quit_app)
        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            self.master.tk.call(master, "config", "-menu", self.menubar)

        #Main Frames
        self.base_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.base_frame.pack(side=tk.BOTTOM, padx= 1, pady= 1, fill=tk.X)
        #Base Frame Items
        w=20
        h=2
        color='cornflower blue'
        self.b_refresh_figs = tk.Button(self.base_frame,text="Refresh Figures", command=self.refresh_figs, font=self.helv, width=w, height=h, bg=color)
        self.b_refresh_figs.pack(side=tk.LEFT)
        self.b_calc = tk.Button(self.base_frame,text="Calc/ReCalc", command=self.run_calcs, font=self.helv, width=w, height=h, bg=color)
        self.b_calc.pack(side=tk.LEFT)
        self.b_quit = tk.Button(self.base_frame,text="Quit", command=self.quit_app, font=self.helv, width=w, height=h, bg='red3')
        self.b_quit.pack(side=tk.RIGHT)

        self.graphics_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)

        self.graphics_frame_l = tk.Frame(self.graphics_frame, padx=1,pady=1)
        self.graphics_frame_l.pack(side = tk.LEFT, anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        self.graphics_frame_r = tk.Frame(self.graphics_frame, padx=1,pady=1)

        tk.Label(self.graphics_frame_r, text="Status:", font=self.helv_res).grid(row=0, column=0, padx=5)
        self.status_ftg1_q = tk.IntVar()
        tk.Checkbutton(self.graphics_frame_r , text=' : FTG_L BRG', variable=self.status_ftg1_q, font=self.helv, state=tk.DISABLED).grid(row=1, column=0, sticky = tk.W)
        self.status_ftg2_q = tk.IntVar()
        tk.Checkbutton(self.graphics_frame_r , text=' : FTG_R BRG', variable=self.status_ftg2_q, font=self.helv, state=tk.DISABLED).grid(row=1, column=1, sticky = tk.W)
        self.status_sumv = tk.IntVar()
        tk.Checkbutton(self.graphics_frame_r , text=' : Sum V = 0', variable=self.status_sumv, font=self.helv, state=tk.DISABLED).grid(row=2, column=0, sticky = tk.W)
        self.status_summ = tk.IntVar()
        tk.Checkbutton(self.graphics_frame_r , text=' : Sum M = 0', variable=self.status_sumv, font=self.helv, state=tk.DISABLED).grid(row=2, column=1, sticky = tk.W)
        self.status_ftg1v = tk.IntVar()
        tk.Checkbutton(self.graphics_frame_r , text=' : FTG_L Shear', variable=self.status_ftg1v, font=self.helv, state=tk.DISABLED).grid(row=3, column=0, sticky = tk.W)
        self.status_ftg1f = tk.IntVar()
        tk.Checkbutton(self.graphics_frame_r , text=' : FTG_L Flexure', variable=self.status_ftg1f, font=self.helv, state=tk.DISABLED).grid(row=3, column=1, sticky = tk.W)
        self.status_ftg2v = tk.IntVar()
        tk.Checkbutton(self.graphics_frame_r , text=' : FTG_R Shear', variable=self.status_ftg2v, font=self.helv, state=tk.DISABLED).grid(row=4, column=0, sticky = tk.W)
        self.status_ftg2f = tk.IntVar()
        tk.Checkbutton(self.graphics_frame_r , text=' : FTG_R Flexure', variable=self.status_ftg2f, font=self.helv, state=tk.DISABLED).grid(row=4, column=1, sticky = tk.W)
        self.status_sv = tk.IntVar()
        tk.Checkbutton(self.graphics_frame_r , text=' : Strap Shear', variable=self.status_sv, font=self.helv, state=tk.DISABLED).grid(row=5, column=0, sticky = tk.W)
        self.status_sf = tk.IntVar()
        tk.Checkbutton(self.graphics_frame_r , text=' : Strap Flexure', variable=self.status_sf, font=self.helv, state=tk.DISABLED).grid(row=5, column=1, sticky = tk.W)

        self.graphics_frame_r.pack(side = tk.RIGHT, anchor='ne')

        self.graphics_frame.pack(side=tk.TOP, padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        self.data_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.data_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)


        #Main Notebooks
        self.nb_graphs = ttk.Notebook(self.graphics_frame_l)
        self.nb_graphs.pack(fill=tk.BOTH, expand=1)

        self.nb_data = ttk.Notebook(self.data_frame)
        self.nb_data.pack(fill=tk.BOTH, expand=1)

        #Graphics Frame tabs and canvases
        #Geometry - Plan
        self.g_plan = ttk.Frame(self.nb_graphs)
        self.nb_graphs.add(self.g_plan, text='Geometry - Plan')

        self.g_plan_frame = tk.Frame(self.g_plan, bd=2, relief='sunken', padx=1,pady=1)
        self.g_plan_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        self.g_plan_canvas = tk.Canvas(self.g_plan_frame, width=50, height=50, bd=2, relief='sunken', background="gray60")
        self.g_plan_canvas.bind("<Configure>", self.draw_plan)
        self.g_plan_canvas.pack(side = tk.LEFT, anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        #Geometry - Elevation/Section
        self.g_elev  = ttk.Frame(self.nb_graphs)
        self.nb_graphs.add(self.g_elev , text='Geometry - Elevation/Section')

        self.g_elev_frame = tk.Frame(self.g_elev, bd=2, relief='sunken', padx=1,pady=1)
        self.g_elev_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        self.g_elev_canvas = tk.Canvas(self.g_elev_frame, width=50, height=50, bd=2, relief='sunken', background="gray60")
        self.g_elev_canvas.bind("<Configure>", self.draw_elevation)
        self.g_elev_canvas.pack(side = tk.LEFT, anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        #Free Body Diagram
        self.g_fbd = ttk.Frame(self.nb_graphs)
        self.nb_graphs.add(self.g_fbd, text='Free Body Diagram')

        self.g_fbd_frame = tk.Frame(self.g_fbd, bd=2, relief='sunken', padx=1,pady=1)
        self.g_fbd_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        self.g_fbd_canvas = tk.Canvas(self.g_fbd_frame, width=50, height=50, bd=2, relief='sunken', background="gray60")
        self.g_fbd_canvas.bind("<Configure>", self.draw_fbd)
        self.g_fbd_canvas.pack(side = tk.LEFT, anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        
        #Beam Diagram
        self.g_beam = ttk.Frame(self.nb_graphs)
        self.nb_graphs.add(self.g_beam, text='Static Beam Diagram')

        self.g_beam_frame = tk.Frame(self.g_beam, bd=2, relief='sunken', padx=1,pady=1)
        self.g_beam_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        self.g_beam_canvas = tk.Canvas(self.g_beam_frame, width=50, height=200, bd=2, relief='sunken', background="gray60")
        self.g_beam_canvas.bind("<Configure>", self.draw_static_beam)
        self.g_beam_canvas.bind("<Button-1>", self.draw_static_beam_mouse)
        self.g_beam_canvas.bind("<B1-Motion>", self.draw_static_beam_mouse)
        self.g_beam_canvas.pack(side = tk.LEFT, anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        self.val_at_x = self.g_beam_canvas.create_line(0, 0,0,0,fill="gray90", width=1, dash=(4,4))
        self.val_at_x_text = self.g_beam_canvas.create_line(0, 0,0,0,fill="gray90", width=1, dash=(4,4))

        self.graph_b_frame = tk.Frame(self.g_beam_frame, bd=2, relief='sunken', padx=4 ,pady=1)

        self.show_vs = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame , text=' : Show Vs', variable=self.show_vs, command = self.draw_static_beam, font=self.helv).grid(row=0, column=1, sticky = tk.W)
        self.show_ms = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame , text=' : Show Ms', variable=self.show_ms, command = self.draw_static_beam, font=self.helv).grid(row=1, column=1, sticky = tk.W)
        self.show_vu = tk.IntVar()
        self.show_vu.set(1)
        tk.Checkbutton(self.graph_b_frame , text=' : Show Vu', variable=self.show_vu, command = self.draw_static_beam, font=self.helv).grid(row=2, column=1, sticky = tk.W)
        self.show_mu = tk.IntVar()
        self.show_mu.set(1)
        tk.Checkbutton(self.graph_b_frame , text=' : Show Mu', variable=self.show_mu, command = self.draw_static_beam, font=self.helv).grid(row=3, column=1, sticky = tk.W)
        self.show_m_tension = tk.IntVar()
        self.show_m_tension.set(1)
        tk.Checkbutton(self.graph_b_frame , text=' : Show M\nOn Tension\nFace', variable=self.show_m_tension, command = self.draw_static_beam, font=self.helv).grid(row=4, column=1, sticky = tk.W)

        self.graph_b_frame.pack(side=tk.RIGHT, anchor='e')

        #Strap Beam Diagrams
        #self.g_strap = ttk.Frame(self.nb_graphs)
        #self.nb_graphs.add(self.g_strap, text='Strap Beam Diagrams')

        #self.g_strap_frame = tk.Frame(self.g_strap, bd=2, relief='sunken', padx=1,pady=1)
        #self.g_strap_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        #Data/calc Frame tabs
        #Geometry
        self.geo_input = ttk.Frame(self.nb_data)
        self.nb_data.add(self.geo_input, text='Geometry and Basic Input')

        self.geo_data_frame = tk.Frame(self.geo_input, bd=2, relief='sunken', padx=1,pady=1)
        self.geo_data_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        #Static Analysis for Soil Reaction
        self.statics_input = ttk.Frame(self.nb_data)
        self.nb_data.add(self.statics_input, text='Statics for Soil Reaction - Analysis')

        self.statics_data_frame = tk.Frame(self.statics_input, bd=2, relief='sunken', padx=1,pady=1)
        self.statics_data_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        #Detailed Static Analysis
        self.analysis_tab = ttk.Frame(self.nb_data)
        self.nb_data.add(self.analysis_tab, text='Ultimate Detailed Results - Analysis')

        self.analysis_data_frame = tk.Frame(self.analysis_tab, bd=2, relief='sunken', padx=1,pady=1)
        self.analysis_data_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        #Footing Designs
        self.ftg_design_tab = ttk.Frame(self.nb_data)
        self.nb_data.add(self.ftg_design_tab, text='Footings - Design')

        self.ftg_design_frame = tk.Frame(self.ftg_design_tab, bd=2, relief='sunken', padx=1,pady=1)
        self.ftg_design_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        #Strap Beam Design
        self.strap_design_tab = ttk.Frame(self.nb_data)
        self.nb_data.add(self.strap_design_tab, text='Strap Beam - Design')

        self.strap_design_frame = tk.Frame(self.strap_design_tab, bd=2, relief='sunken', padx=1,pady=1)
        self.strap_design_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        #Load Casing
        self.load_case_tab = ttk.Frame(self.nb_data)
        self.nb_data.add(self.load_case_tab, text='Multiple Load Cases')

        self.load_case_frame = tk.Frame(self.load_case_tab, bd=2, relief='sunken', padx=1,pady=1)
        self.load_case_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)
        
        #Data/Calc Frame Items
        #Geometry and Basic items
        self.data_frame_builder()

        #Static Analysis for Soil Reaction
        self.static_analysis_frame_builder()

        #Analysis data
        self.analysis_res_frame_builder()

        #Footing Design Items
        self.ftg_design_frame_builder()

        #Strap Beam Design Items
        self.strap_design_frame_builder()
        
        #Load Case Tab Items
        self.load_case_count = 0
        self.load_case_list = []
        self.load_case_res_list = []
        self.load_clicked = False
        
        self.load_case_add_frame = tk.Frame(self.load_case_frame, bd=2, relief='sunken', padx=1,pady=1)
        self.load_case_add_frame.pack(side=tk.LEFT ,anchor='nw', fill=tk.BOTH,expand=1)
        
        self.load_case_add_button_frame = tk.Frame(self.load_case_add_frame, bd=2, relief='sunken', padx=1,pady=1)
        self.load_case_add_button_frame.pack(side=tk.TOP)
        
        self.load_case_add_list_frame = tk.Frame(self.load_case_add_frame, bd=2, relief='sunken', padx=1,pady=1)
        self.load_case_add_list_frame.pack(side=tk.TOP)
        
        tk.Label(self.load_case_add_button_frame, text="P1,service: (kips) ", font=self.helv_res).grid(row=0, column=1, padx=4)
        tk.Label(self.load_case_add_button_frame, text="P1,ultimate: (kips) ", font=self.helv_res).grid(row=0, column=2, padx=4)
        tk.Label(self.load_case_add_button_frame, text="P2,service: (kips) ", font=self.helv_res).grid(row=0, column=3, padx=4)
        tk.Label(self.load_case_add_button_frame, text="P2,ultimate: (kips) ", font=self.helv_res).grid(row=0, column=4, padx=4)
        tk.Label(self.load_case_add_button_frame, text="DL,service factor:", font=self.helv_res).grid(row=0, column=5, padx=4)
        tk.Label(self.load_case_add_button_frame, text="DL,ultimate factor:", font=self.helv_res).grid(row=0, column=6, padx=4)
        
        self.p1s_case = tk.StringVar()
        self.p1s_case.set(100)
        self.p1s_case_entry = tk.Entry(self.load_case_add_button_frame, textvariable=self.p1s_case, width=10)
        self.p1s_case_entry.grid(row=1, column=1)
        
        self.p1u_case = tk.StringVar()
        self.p1u_case.set(140)
        self.p1u_case_entry = tk.Entry(self.load_case_add_button_frame, textvariable=self.p1u_case, width=10)
        self.p1u_case_entry.grid(row=1, column=2)
        
        self.p2s_case = tk.StringVar()
        self.p2s_case.set(200)
        self.p2s_case_entry = tk.Entry(self.load_case_add_button_frame, textvariable=self.p2s_case, width=10)
        self.p2s_case_entry.grid(row=1, column=3)
        
        self.p2u_case = tk.StringVar()
        self.p2u_case.set(280)
        self.p2u_case_entry = tk.Entry(self.load_case_add_button_frame, textvariable=self.p2u_case, width=10)
        self.p2u_case_entry.grid(row=1, column=4)
        
        self.dls_case = tk.StringVar()
        self.dls_case.set(1.0)
        self.dls_case_entry = tk.Entry(self.load_case_add_button_frame, textvariable=self.dls_case, width=10)
        self.dls_case_entry.grid(row=1, column=5)
        
        self.dlu_case = tk.StringVar()
        self.dlu_case.set(1.0)
        self.dlu_case_entry = tk.Entry(self.load_case_add_button_frame, textvariable=self.dlu_case, width=10)
        self.dlu_case_entry.grid(row=1, column=6)
        
        self.b_add_case = tk.Button(self.load_case_add_button_frame,text="Add Load Case", command=self.add_load_case, font=self.helv, width=15, height=1, bg=color)
        self.b_add_case.grid(row=2, column=1, padx=4, pady=4)
        
        self.b_change_case = tk.Button(self.load_case_add_button_frame,text="Change Selected", command=self.change_load_case, font=self.helv, width=15, height=1, bg=color)
        self.b_change_case.grid(row=2, column=2, padx=4, pady=4)
        
        self.b_del_case = tk.Button(self.load_case_add_button_frame,text="Remove Selected", command=self.del_load_case, font=self.helv, width=15, height=1, bg=color)
        self.b_del_case.grid(row=2, column=3, padx=4, pady=4)
        
        self.b_del_case = tk.Button(self.load_case_add_button_frame,text="Import CSV", command=self.import_csv, font=self.helv, width=15, height=1, bg=color)
        self.b_del_case.grid(row=2, column=4, padx=4, pady=4)
        
        self.b_run_case = tk.Button(self.load_case_add_button_frame,text="Run All", command=self.run_load_cases, font=self.helv, width=10, height=1, bg=color)
        self.b_run_case.grid(row=2, column=6, padx=4, pady=4)
        
        self.load_case_scrollbar = tk.Scrollbar(self.load_case_add_list_frame, orient="vertical", command=self.load_case_scroll)
        self.load_case_scrollbar.grid(row=0, column=2, sticky=tk.NS)
        
        self.load_case_listbox = tk.Listbox(self.load_case_add_list_frame, height = 22, width = 60, font=self.helv, yscrollcommand=self.load_case_scrollbar.set, exportselection=0)
        self.load_case_listbox.grid(row=0, column=0)
        self.load_case_listbox.bind("<<ListboxSelect>>",self.load_case_click)
        
        self.load_case_res_listbox = tk.Listbox(self.load_case_add_list_frame, height = 22, width = 130, font=self.helv, yscrollcommand=self.load_case_scrollbar.set, exportselection=0)
        self.load_case_res_listbox.grid(row=0, column=3)
        
        self.draw_plan()
        self.draw_elevation()
        self.license_display()
    
    def license_display(self, *event):
        license_string = (
"""Copyright (c) 2019, Donald N. Bockoven III\n
All rights reserved.\n\n
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n
https://github.com/buddyd16/Structural-Engineering/blob/master/LICENSE"""
)
        tkMessageBox.showerror("License Information",license_string)
        self.master.focus_force()
        
    def data_frame_builder(self):
        #Left
        tk.Label(self.geo_data_frame, text="Left Foundation:", font=self.helv_res).grid(row=0, column=0)
        self.b1 = tk.StringVar()
        self.inputs.append(self.b1)
        self.b1.set(4)
        tk.Label(self.geo_data_frame, text="B,left = ", font=self.helv).grid(row=1, column=0, sticky = tk.E)
        self.b1_entry = tk.Entry(self.geo_data_frame, textvariable=self.b1, width=10, validate="key", validatecommand=self.reset_status)
        self.b1_entry.grid(row=1, column=1)
        tk.Label(self.geo_data_frame, text="ft", font=self.helv).grid(row=1, column=2)

        self.d1 = tk.StringVar()
        self.inputs.append(self.d1)
        self.d1.set(4)
        tk.Label(self.geo_data_frame, text="D,left = ", font=self.helv).grid(row=2, column=0, sticky = tk.E)
        self.d1_entry = tk.Entry(self.geo_data_frame, textvariable=self.d1, width=10, validate="key", validatecommand=self.reset_status)
        self.d1_entry.grid(row=2, column=1)
        tk.Label(self.geo_data_frame, text="ft", font=self.helv).grid(row=2, column=2)

        self.h1 = tk.StringVar()
        self.inputs.append(self.h1)
        self.h1.set(12)
        tk.Label(self.geo_data_frame, text="H,left = ", font=self.helv).grid(row=3, column=0, sticky = tk.E)
        self.h1_entry = tk.Entry(self.geo_data_frame, textvariable=self.h1, width=10, validate="key", validatecommand=self.reset_status)
        self.h1_entry.grid(row=3, column=1)
        tk.Label(self.geo_data_frame, text="in", font=self.helv).grid(row=3, column=2)
        tk.Label(self.geo_data_frame, text="Left Column:", font=self.helv_res).grid(row=4, column=0, pady=5)

        self.cb1 = tk.StringVar()
        self.inputs.append(self.cb1)
        self.cb1.set(12)
        tk.Label(self.geo_data_frame, text="Bc,left = ", font=self.helv).grid(row=5, column=0, sticky = tk.E)
        self.cb1_entry = tk.Entry(self.geo_data_frame, textvariable=self.cb1, width=10, validate="key", validatecommand=self.reset_status)
        self.cb1_entry.grid(row=5, column=1)
        tk.Label(self.geo_data_frame, text="in", font=self.helv).grid(row=5, column=2)

        self.cd1 = tk.StringVar()
        self.inputs.append(self.cd1)
        self.cd1.set(12)
        tk.Label(self.geo_data_frame, text="Dc,left = ", font=self.helv).grid(row=6, column=0, sticky = tk.E)
        self.cd1_entry = tk.Entry(self.geo_data_frame, textvariable=self.cd1, width=10, validate="key", validatecommand=self.reset_status)
        self.cd1_entry.grid(row=6, column=1)
        tk.Label(self.geo_data_frame, text="in", font=self.helv).grid(row=6, column=2)

        tk.Label(self.geo_data_frame, text="Left Eccentricty:", font=self.helv_res).grid(row=7, column=0, pady=5)
        self.ce1 = tk.StringVar()
        self.inputs.append(self.ce1)
        self.ce1.set(12)
        tk.Label(self.geo_data_frame, text="e,left = ", font=self.helv).grid(row=8, column=0, sticky = tk.E)
        self.ce1_entry = tk.Entry(self.geo_data_frame, textvariable=self.ce1, width=10, validate="key", validatecommand=self.reset_status)
        self.ce1_entry.grid(row=8, column=1)
        tk.Label(self.geo_data_frame, text="in", font=self.helv).grid(row=8, column=2)

        tk.Label(self.geo_data_frame, text="Loads: ", font=self.helv_res).grid(row=9, column=0)
        self.p1_service_kips = tk.StringVar()
        self.inputs.append(self.p1_service_kips)
        self.p1_service_kips.set(100)
        tk.Label(self.geo_data_frame, text="Pl,service = ", font=self.helv).grid(row=10, column=0, sticky = tk.E)
        self.p1_service_entry = tk.Entry(self.geo_data_frame, textvariable=self.p1_service_kips, width=10, validate="key", validatecommand=self.reset_status)
        self.p1_service_entry.grid(row=10, column=1)
        tk.Label(self.geo_data_frame, text="kips", font=self.helv).grid(row=10, column=2)

        self.p1_ultimate_kips = tk.StringVar()
        self.inputs.append(self.p1_ultimate_kips)
        self.p1_ultimate_kips.set(140)
        tk.Label(self.geo_data_frame, text="Pl,ultimate = ", font=self.helv).grid(row=11, column=0, sticky = tk.E)
        self.p1_ultimate_entry = tk.Entry(self.geo_data_frame, textvariable=self.p1_ultimate_kips, width=10, validate="key", validatecommand=self.reset_status)
        self.p1_ultimate_entry.grid(row=11, column=1)
        tk.Label(self.geo_data_frame, text="kips", font=self.helv).grid(row=11, column=2)

        tk.Label(self.geo_data_frame, text="Basic Calcs: ", font=self.helv_res).grid(row=12, column=0, pady=5)

        self.left_sw_kips = tk.StringVar()
        self.left_sw_kips.set('--')
        tk.Label(self.geo_data_frame, text="SW = ", font=self.helv).grid(row=13, column=0, sticky = tk.E)
        self.left_sw_entry = tk.Entry(self.geo_data_frame, textvariable=self.left_sw_kips, width=10, state=tk.DISABLED)
        self.left_sw_entry.grid(row=13, column=1)
        tk.Label(self.geo_data_frame, text="kips", font=self.helv).grid(row=13, column=2)
        
        self.left_ig_in4 = tk.StringVar()
        self.left_ig_in4.set('--')
        tk.Label(self.geo_data_frame, text="Ig,left ftg = ", font=self.helv).grid(row=14, column=0, sticky = tk.E)
        tk.Entry(self.geo_data_frame, textvariable=self.left_ig_in4, width=10, state=tk.DISABLED).grid(row=14, column=1)
        tk.Label(self.geo_data_frame, text="in^4", font=self.helv).grid(row=14, column=2)
        
        #Right
        tk.Label(self.geo_data_frame, text="Right Foundation:", font=self.helv_res).grid(row=0, column=3)
        self.b2 = tk.StringVar()
        self.inputs.append(self.b2)
        self.b2.set(6)
        tk.Label(self.geo_data_frame, text="B,right = ", font=self.helv).grid(row=1, column=3, sticky = tk.E)
        self.b2_entry = tk.Entry(self.geo_data_frame, textvariable=self.b2, width=10, validate="key", validatecommand=self.reset_status)
        self.b2_entry.grid(row=1, column=4)
        
        tk.Label(self.geo_data_frame, text="ft", font=self.helv).grid(row=1, column=5)        
        self.d2 = tk.StringVar()
        self.inputs.append(self.d2)
        self.d2.set(6)
        tk.Label(self.geo_data_frame, text="D,right = ", font=self.helv).grid(row=2, column=3, sticky = tk.E)
        self.d2_entry = tk.Entry(self.geo_data_frame, textvariable=self.d2, width=10, validate="key", validatecommand=self.reset_status)
        self.d2_entry.grid(row=2, column=4)
        
        tk.Label(self.geo_data_frame, text="ft", font=self.helv).grid(row=2, column=5)
        self.h2 = tk.StringVar()
        self.inputs.append(self.h2)
        self.h2.set(12)
        tk.Label(self.geo_data_frame, text="H,right = ", font=self.helv).grid(row=3, column=3, sticky = tk.E)
        self.h2_entry = tk.Entry(self.geo_data_frame, textvariable=self.h2, width=10, validate="key", validatecommand=self.reset_status)
        self.h2_entry.grid(row=3, column=4)
        tk.Label(self.geo_data_frame, text="in", font=self.helv).grid(row=3, column=5)
        
        tk.Label(self.geo_data_frame, text="Right Column:", font=self.helv_res).grid(row=4, column=3, pady=5)
        
        self.cb2 = tk.StringVar()
        self.inputs.append(self.cb2)
        self.cb2.set(12)
        tk.Label(self.geo_data_frame, text="Bc,right = ", font=self.helv).grid(row=5, column=3, sticky = tk.E)
        self.cb2_entry = tk.Entry(self.geo_data_frame, textvariable=self.cb2, width=10, validate="key", validatecommand=self.reset_status)
        self.cb2_entry.grid(row=5, column=4)
        tk.Label(self.geo_data_frame, text="in", font=self.helv).grid(row=5, column=5)
        
        self.cd2 = tk.StringVar()
        self.inputs.append(self.cd2)
        self.cd2.set(12)
        tk.Label(self.geo_data_frame, text="Dc,right = ", font=self.helv).grid(row=6, column=3, sticky = tk.E)
        self.cd2_entry = tk.Entry(self.geo_data_frame, textvariable=self.cd2, width=10, validate="key", validatecommand=self.reset_status)
        self.cd2_entry.grid(row=6, column=4)
        tk.Label(self.geo_data_frame, text="in", font=self.helv).grid(row=6, column=5)
        
        tk.Label(self.geo_data_frame, text="Right Eccentricty:", font=self.helv_res).grid(row=7, column=3, pady=5)
        self.ce2 = tk.StringVar()
        self.inputs.append(self.ce2)
        self.ce2.set(0)
        tk.Label(self.geo_data_frame, text="e,right = ", font=self.helv).grid(row=8, column=3, sticky = tk.E)
        self.ce2_entry = tk.Entry(self.geo_data_frame, textvariable=self.ce2, width=10, validate="key", validatecommand=self.reset_status)
        self.ce2_entry.grid(row=8, column=4)
        tk.Label(self.geo_data_frame, text="in", font=self.helv).grid(row=8, column=5)

        tk.Label(self.geo_data_frame, text="Loads: ", font=self.helv_res).grid(row=9, column=3, pady=5)
        self.p2_service_kips = tk.StringVar()
        self.inputs.append(self.p2_service_kips)
        self.p2_service_kips.set(100)
        tk.Label(self.geo_data_frame, text="Pr,service = ", font=self.helv).grid(row=10, column=3, sticky = tk.E)
        self.p2_service_entry = tk.Entry(self.geo_data_frame, textvariable=self.p2_service_kips, width=10, validate="key", validatecommand=self.reset_status)
        self.p2_service_entry.grid(row=10, column=4)
        tk.Label(self.geo_data_frame, text="kips", font=self.helv).grid(row=10, column=5)

        self.p2_ultimate_kips = tk.StringVar()
        self.inputs.append(self.p2_ultimate_kips)
        self.p2_ultimate_kips.set(140)
        tk.Label(self.geo_data_frame, text="Pr,ultimate = ", font=self.helv).grid(row=11, column=3, sticky = tk.E)
        self.p2_ultimate_entry = tk.Entry(self.geo_data_frame, textvariable=self.p2_ultimate_kips, width=10, validate="key", validatecommand=self.reset_status)
        self.p2_ultimate_entry.grid(row=11, column=4)
        tk.Label(self.geo_data_frame, text="kips", font=self.helv).grid(row=11, column=5)

        tk.Label(self.geo_data_frame, text="Basic Calcs: ", font=self.helv_res).grid(row=12, column=3, pady=5)

        self.right_sw_kips = tk.StringVar()
        self.right_sw_kips.set('--')
        tk.Label(self.geo_data_frame, text="SW = ", font=self.helv).grid(row=13, column=3, sticky = tk.E)
        self.right_sw_entry = tk.Entry(self.geo_data_frame, textvariable=self.right_sw_kips, width=10, state=tk.DISABLED)
        self.right_sw_entry.grid(row=13, column=4)
        tk.Label(self.geo_data_frame, text="kips", font=self.helv).grid(row=13, column=5)
        
        self.right_ig_in4 = tk.StringVar()
        self.right_ig_in4.set('--')
        tk.Label(self.geo_data_frame, text="Ig,right ftg = ", font=self.helv).grid(row=14, column=3, sticky = tk.E)
        tk.Entry(self.geo_data_frame, textvariable=self.right_ig_in4, width=10, state=tk.DISABLED).grid(row=14, column=4)
        tk.Label(self.geo_data_frame, text="in^4", font=self.helv).grid(row=14, column=5)

        #Strap
        tk.Label(self.geo_data_frame, text="Strap:", font=self.helv_res).grid(row=0, column=6)
        self.bs = tk.StringVar()
        self.inputs.append(self.bs)
        self.bs.set(12)
        tk.Label(self.geo_data_frame, text="Bs = ", font=self.helv).grid(row=1, column=7, sticky = tk.E)
        self.bs_entry = tk.Entry(self.geo_data_frame, textvariable=self.bs, width=10, validate="key", validatecommand=self.reset_status)
        self.bs_entry.grid(row=1, column=8)
        tk.Label(self.geo_data_frame, text="in", font=self.helv).grid(row=1, column=9)

        self.hs = tk.StringVar()
        self.inputs.append(self.hs)
        self.hs.set(24)
        tk.Label(self.geo_data_frame, text="Hs = ", font=self.helv).grid(row=2, column=7, sticky = tk.E)
        self.hs_entry = tk.Entry(self.geo_data_frame, textvariable=self.hs, width=10, validate="key", validatecommand=self.reset_status)
        self.hs_entry.grid(row=2, column=8)
        tk.Label(self.geo_data_frame, text="in", font=self.helv).grid(row=2, column=9)

        self.s_extension_in = tk.StringVar()
        self.inputs.append(self.s_extension_in)
        self.s_extension_in.set('3')
        tk.Label(self.geo_data_frame, text="Extension Beyond C2 = ", font=self.helv).grid(row=3, column=7, sticky = tk.E)
        self.s_ls_entry = tk.Entry(self.geo_data_frame, textvariable=self.s_extension_in, width=10)
        self.s_ls_entry.grid(row=3, column=8)
        tk.Label(self.geo_data_frame, text="in", font=self.helv).grid(row=3, column=9)

        self.s_elev_in = tk.StringVar()
        self.inputs.append(self.s_elev_in)
        self.s_elev_in.set('3')
        tk.Label(self.geo_data_frame, text="B/strap - B/ftg = ", font=self.helv).grid(row=4, column=7, sticky = tk.E)
        self.s_ls_entry = tk.Entry(self.geo_data_frame, textvariable=self.s_elev_in, width=10)
        self.s_ls_entry.grid(row=4, column=8)
        tk.Label(self.geo_data_frame, text="in", font=self.helv).grid(row=4, column=9)

        self.s_ls_ft = tk.StringVar()
        self.s_ls_ft.set('--')
        tk.Label(self.geo_data_frame, text="Ls = ", font=self.helv).grid(row=5, column=7, sticky = tk.E)
        self.s_ls_entry = tk.Entry(self.geo_data_frame, textvariable=self.s_ls_ft, width=10, state=tk.DISABLED)
        self.s_ls_entry.grid(row=5, column=8)
        tk.Label(self.geo_data_frame, text="ft", font=self.helv).grid(row=5, column=9)

        self.s_sw_klf = tk.StringVar()
        self.s_sw_klf.set('--')
        tk.Label(self.geo_data_frame, text="SW = ", font=self.helv).grid(row=6, column=7, sticky = tk.E)
        self.s_sw_entry = tk.Entry(self.geo_data_frame, textvariable=self.s_sw_klf, width=10, state=tk.DISABLED)
        self.s_sw_entry.grid(row=6, column=8)
        tk.Label(self.geo_data_frame, text="klf", font=self.helv).grid(row=6, column=9)

        self.s_swl_kips = tk.StringVar()
        self.s_swl_kips.set('--')
        tk.Label(self.geo_data_frame, text="SW over Left = ", font=self.helv).grid(row=7, column=7, sticky = tk.E)
        self.s_swl_entry = tk.Entry(self.geo_data_frame, textvariable=self.s_swl_kips, width=10, state=tk.DISABLED)
        self.s_swl_entry.grid(row=7, column=8)
        tk.Label(self.geo_data_frame, text="kips", font=self.helv).grid(row=7, column=9)

        self.s_swm_kips = tk.StringVar()
        self.s_swm_kips.set('--')
        tk.Label(self.geo_data_frame, text="SW, Ls = ", font=self.helv).grid(row=8, column=7, sticky = tk.E)
        self.s_swm_entry = tk.Entry(self.geo_data_frame, textvariable=self.s_swm_kips, width=10, state=tk.DISABLED)
        self.s_swm_entry.grid(row=8, column=8)
        tk.Label(self.geo_data_frame, text="kips", font=self.helv).grid(row=8, column=9)

        self.s_swr_kips = tk.StringVar()
        self.s_swr_kips.set('--')
        tk.Label(self.geo_data_frame, text="SW over Right = ", font=self.helv).grid(row=9, column=7, sticky = tk.E)
        self.s_swr_entry = tk.Entry(self.geo_data_frame, textvariable=self.s_swr_kips, width=10, state=tk.DISABLED)
        self.s_swr_entry.grid(row=9, column=8)
        tk.Label(self.geo_data_frame, text="kips", font=self.helv).grid(row=9, column=9)
        
        self.strap_ig_in4 = tk.StringVar()
        self.strap_ig_in4.set('--')
        tk.Label(self.geo_data_frame, text="Ig,strap = ", font=self.helv).grid(row=10, column=7, sticky = tk.E)
        tk.Entry(self.geo_data_frame, textvariable=self.strap_ig_in4, width=10, state=tk.DISABLED).grid(row=10, column=8)
        tk.Label(self.geo_data_frame, text="in^4", font=self.helv).grid(row=10, column=9)
        
        self.igs_over_igl = tk.StringVar()
        self.igs_over_igl.set('--')
        tk.Label(self.geo_data_frame, text="Ig,strap / Ig,left = ", font=self.helv).grid(row=11, column=7, sticky = tk.E)
        tk.Entry(self.geo_data_frame, textvariable=self.igs_over_igl, width=10, state=tk.DISABLED).grid(row=11, column=8)
        
        self.igs_over_igr = tk.StringVar()
        self.igs_over_igr.set('--')
        tk.Label(self.geo_data_frame, text="Ig,strap / Ig,right = ", font=self.helv).grid(row=12, column=7, sticky = tk.E)
        tk.Entry(self.geo_data_frame, textvariable=self.igs_over_igr, width=10, state=tk.DISABLED).grid(row=12, column=8)
        
        #Distance between Columns
        tk.Label(self.geo_data_frame, text="Distance Between Columns:", font=self.helv_res).grid(row=0, column=10)
        tk.Label(self.geo_data_frame, text="Lc-c = ", font=self.helv).grid(row=1, column=10, sticky = tk.E)
        self.lcc = tk.StringVar()
        self.inputs.append(self.lcc)
        self.lcc.set(20)
        self.lcc_entry = tk.Entry(self.geo_data_frame, textvariable=self.lcc, width=10, validate="key", validatecommand=self.reset_status)
        self.lcc_entry.grid(row=1, column=11)
        tk.Label(self.geo_data_frame, text="ft", font=self.helv).grid(row=1, column=12)

        #Common Items - Fy, F'c, etc.
        tk.Label(self.geo_data_frame, text="Common Inputs:", font=self.helv_res).grid(row=0, column=13)

        tk.Label(self.geo_data_frame, text="Q,allow = ", font=self.helv).grid(row=1, column=13, sticky = tk.E)
        self.Qa_ksf = tk.StringVar()
        self.inputs.append(self.Qa_ksf)
        self.Qa_ksf.set(3)
        self.qa_entry = tk.Entry(self.geo_data_frame, textvariable=self.Qa_ksf, width=10, validate="key", validatecommand=self.reset_status)
        self.qa_entry.grid(row=1, column=14)
        tk.Label(self.geo_data_frame, text="ksf", font=self.helv).grid(row=1, column=15)
        
        tk.Label(self.geo_data_frame, text="DL,Service factor = ", font=self.helv).grid(row=2, column=13, sticky = tk.E)
        self.dl_service_factor = tk.StringVar()
        self.inputs.append(self.dl_service_factor)
        self.dl_service_factor.set(1.0)
        self.dl_service_factor_entry = tk.Entry(self.geo_data_frame, textvariable=self.dl_service_factor, width=10, validate="key", validatecommand=self.reset_status)
        self.dl_service_factor_entry.grid(row=2, column=14)
        
        tk.Label(self.geo_data_frame, text="DL,Ult. factor = ", font=self.helv).grid(row=3, column=13, sticky = tk.E)
        self.dl_factor = tk.StringVar()
        self.inputs.append(self.dl_factor)
        self.dl_factor.set(1.2)
        self.dl_factor_entry = tk.Entry(self.geo_data_frame, textvariable=self.dl_factor, width=10, validate="key", validatecommand=self.reset_status)
        self.dl_factor_entry.grid(row=3, column=14)

        tk.Label(self.geo_data_frame, text="Fy = ", font=self.helv).grid(row=4, column=13, sticky = tk.E)
        self.Fy_ksi = tk.StringVar()
        self.inputs.append(self.Fy_ksi)
        self.Fy_ksi.set(60)
        self.fy_entry = tk.Entry(self.geo_data_frame, textvariable=self.Fy_ksi, width=10, validate="key", validatecommand=self.reset_status)
        self.fy_entry.grid(row=4, column=14)
        tk.Label(self.geo_data_frame, text="ksi", font=self.helv).grid(row=4, column=15)

        tk.Label(self.geo_data_frame, text="F'c = ", font=self.helv).grid(row=5, column=13, sticky = tk.E)
        self.Fpc_ksi = tk.StringVar()
        self.inputs.append(self.Fpc_ksi)
        self.Fpc_ksi.set(3)
        self.fpc_entry = tk.Entry(self.geo_data_frame, textvariable=self.Fpc_ksi, width=10, validate="key", validatecommand=self.reset_status)
        self.fpc_entry.grid(row=5, column=14)
        tk.Label(self.geo_data_frame, text="ksi", font=self.helv).grid(row=5, column=15)

        tk.Label(self.geo_data_frame, text="Density = ", font=self.helv).grid(row=6, column=13, sticky = tk.E)
        self.density_pcf = tk.StringVar()
        self.inputs.append(self.density_pcf)
        self.density_pcf.set(150)
        self.density_entry = tk.Entry(self.geo_data_frame, textvariable=self.density_pcf, width=10, validate="key", validatecommand=self.reset_status)
        self.density_entry.grid(row=6, column=14)
        tk.Label(self.geo_data_frame, text="pcf", font=self.helv).grid(row=6, column=15)

    def static_analysis_frame_builder(self):
        self.stat_service_frame = tk.LabelFrame(self.statics_data_frame, text="Service:", bd=1, relief='sunken', padx=5, pady=2)
        self.stat_service_frame.grid(row=0, column=0, padx=5)

        self.stat_ult_frame = tk.LabelFrame(self.statics_data_frame, text="Ultimate:", bd=1, relief='sunken', padx=5, pady=2)
        self.stat_ult_frame.grid(row=0, column=1, padx=5)
        wstat = 15
        tk.Label(self.stat_service_frame, text="Source:", font=self.helv_res).grid(row=0, column=0, padx=5)
        tk.Label(self.stat_service_frame, text="Load (kips):", font=self.helv_res).grid(row=0, column=1, padx=5)
        tk.Label(self.stat_service_frame, text="Location (ft):", font=self.helv_res).grid(row=0, column=2, padx=5)
        tk.Label(self.stat_service_frame, text="Moment Arm (ft):", font=self.helv_res).grid(row=0, column=3, padx=5)
        tk.Label(self.stat_service_frame, text="Moment (ft-kips):", font=self.helv_res).grid(row=0, column=4, padx=5)
        self.service_statics = []
        self.service_statics.append(tk.Listbox(self.stat_service_frame, height = 10, width = wstat, font=self.helv))
        self.service_statics.append(tk.Listbox(self.stat_service_frame, height = 10, width = wstat, font=self.helv))
        self.service_statics.append(tk.Listbox(self.stat_service_frame, height = 10, width = wstat, font=self.helv))
        self.service_statics.append(tk.Listbox(self.stat_service_frame, height = 10, width = wstat, font=self.helv))
        self.service_statics.append(tk.Listbox(self.stat_service_frame, height = 10, width = wstat, font=self.helv))
        self.service_statics[0].grid(row=1, column=0)
        self.service_statics[1].grid(row=1, column=1)
        self.service_statics[2].grid(row=1, column=2)
        self.service_statics[3].grid(row=1, column=3)
        self.service_statics[4].grid(row=1, column=4)

        tk.Label(self.stat_ult_frame, text="Source:", font=self.helv_res).grid(row=0, column=0, padx=5)
        tk.Label(self.stat_ult_frame, text="Load (kips):", font=self.helv_res).grid(row=0, column=1, padx=5)
        tk.Label(self.stat_ult_frame, text="Location (ft):", font=self.helv_res).grid(row=0, column=2, padx=5)
        tk.Label(self.stat_ult_frame, text="Moment Arm (ft):", font=self.helv_res).grid(row=0, column=3, padx=5)
        tk.Label(self.stat_ult_frame, text="Moment (ft-kips):", font=self.helv_res).grid(row=0, column=4, padx=5)
        self.ultimate_statics = []
        self.ultimate_statics.append(tk.Listbox(self.stat_ult_frame, height = 10, width = wstat, font=self.helv))
        self.ultimate_statics.append(tk.Listbox(self.stat_ult_frame, height = 10, width = wstat, font=self.helv))
        self.ultimate_statics.append(tk.Listbox(self.stat_ult_frame, height = 10, width = wstat, font=self.helv))
        self.ultimate_statics.append(tk.Listbox(self.stat_ult_frame, height = 10, width = wstat, font=self.helv))
        self.ultimate_statics.append(tk.Listbox(self.stat_ult_frame, height = 10, width = wstat, font=self.helv))
        self.ultimate_statics[0].grid(row=1, column=0)
        self.ultimate_statics[1].grid(row=1, column=1)
        self.ultimate_statics[2].grid(row=1, column=2)
        self.ultimate_statics[3].grid(row=1, column=3)
        self.ultimate_statics[4].grid(row=1, column=4)

    def analysis_res_frame_builder(self):
        self.nb_res = ttk.Notebook(self.analysis_data_frame)

        self.nb_res.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        self.l_res_tab = ttk.Frame(self.nb_res)
        self.nb_res.add(self.l_res_tab, text='FTG_L EDGE TO P1')

        self.res_l_frame = tk.Frame(self.l_res_tab, bd=2, relief='sunken', padx=1,pady=1)
        tk.Label(self.res_l_frame, text="X (ft)", font=self.helv_res).grid(row=0, column=1)
        tk.Label(self.res_l_frame, text="V (Kips)", font=self.helv_res).grid(row=0, column=2)
        tk.Label(self.res_l_frame, text="M (ft-Kips)", font=self.helv_res).grid(row=0, column=3)

        self.results_scrollbar_l = tk.Scrollbar(self.res_l_frame, orient="vertical", command=self.det_res_scroll_l)
        self.results_scrollbar_l.grid(row=1, column=4, sticky=tk.NS)

        self.xl_listbox = tk.Listbox(self.res_l_frame, height = 20, width = 16, font=self.helv, yscrollcommand=self.results_scrollbar_l.set)
        self.xl_listbox.grid(row=1, column=1)
        self.lv_listbox = tk.Listbox(self.res_l_frame, height = 20, width = 16, font=self.helv, yscrollcommand=self.results_scrollbar_l.set)
        self.lv_listbox.grid(row=1, column=2)
        self.lm_listbox = tk.Listbox(self.res_l_frame, height = 20, width = 16, font=self.helv, yscrollcommand=self.results_scrollbar_l.set)
        self.lm_listbox.grid(row=1, column=3)

        self.res_l_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        self.c_res_tab = ttk.Frame(self.nb_res)
        self.nb_res.add(self.c_res_tab, text='P1 TO P2')

        self.res_c_frame = tk.Frame(self.c_res_tab, bd=2, relief='sunken', padx=1,pady=1)
        tk.Label(self.res_c_frame, text="X (ft)", font=self.helv_res).grid(row=0, column=1)
        tk.Label(self.res_c_frame, text="V (Kips)", font=self.helv_res).grid(row=0, column=2)
        tk.Label(self.res_c_frame, text="M (ft-Kips)", font=self.helv_res).grid(row=0, column=3)

        self.results_scrollbar = tk.Scrollbar(self.res_c_frame, orient="vertical", command=self.det_res_scroll)
        self.results_scrollbar.grid(row=1, column=4, sticky=tk.NS)

        self.xc_listbox = tk.Listbox(self.res_c_frame, height = 20, width = 16, font=self.helv, yscrollcommand=self.results_scrollbar.set)
        self.xc_listbox.grid(row=1, column=1)
        self.cv_listbox = tk.Listbox(self.res_c_frame, height = 20, width = 16, font=self.helv, yscrollcommand=self.results_scrollbar.set)
        self.cv_listbox.grid(row=1, column=2)
        self.cm_listbox = tk.Listbox(self.res_c_frame, height = 20, width = 16, font=self.helv, yscrollcommand=self.results_scrollbar.set)
        self.cm_listbox.grid(row=1, column=3)

        self.res_c_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        self.r_res_tab = ttk.Frame(self.nb_res)
        self.nb_res.add(self.r_res_tab, text='P2 TO FTG_R EDGE')

        self.res_r_frame = tk.Frame(self.r_res_tab, bd=2, relief='sunken', padx=1,pady=1)
        tk.Label(self.res_r_frame, text="X (ft)", font=self.helv_res).grid(row=0, column=1)
        tk.Label(self.res_r_frame, text="V (Kips)", font=self.helv_res).grid(row=0, column=2)
        tk.Label(self.res_r_frame, text="M (ft-Kips)", font=self.helv_res).grid(row=0, column=3)

        self.results_scrollbar_r = tk.Scrollbar(self.res_r_frame, orient="vertical", command=self.det_res_scroll_r)
        self.results_scrollbar_r.grid(row=1, column=4, sticky=tk.NS)

        self.xr_listbox = tk.Listbox(self.res_r_frame, height = 20, width = 16, font=self.helv, yscrollcommand=self.results_scrollbar_r.set)
        self.xr_listbox.grid(row=1, column=1)
        self.rv_listbox = tk.Listbox(self.res_r_frame, height = 20, width = 16, font=self.helv, yscrollcommand=self.results_scrollbar_r.set)
        self.rv_listbox.grid(row=1, column=2)
        self.rm_listbox = tk.Listbox(self.res_r_frame, height = 20, width = 16, font=self.helv, yscrollcommand=self.results_scrollbar_r.set)
        self.rm_listbox.grid(row=1, column=3)

        self.res_r_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

    def ftg_design_frame_builder(self):
        self.ftg_left_frame = tk.LabelFrame(self.ftg_design_frame, text="Left Foundation:", bd=1, relief='sunken', padx=2, pady=2)
        self.ftg_left_inputs_frame = tk.Frame(self.ftg_left_frame)
        self.ftg_left_inputs_frame.pack(side=tk.LEFT, anchor='nw')
        self.ftg_left_calc_frame = tk.Frame(self.ftg_left_frame)
        self.ftg_left_calc_frame.pack(side=tk.RIGHT ,anchor='ne', fill=tk.BOTH,expand=1)
        self.ftg_left_frame.grid(row=0, column=0, padx=5)

        self.ftg_right_frame = tk.LabelFrame(self.ftg_design_frame, text="Right Foundation:", bd=1, relief='sunken', padx=2, pady=2)
        self.ftg_right_inputs_frame = tk.Frame(self.ftg_right_frame)
        self.ftg_right_inputs_frame.pack(side=tk.LEFT, anchor='nw')
        self.ftg_right_calc_frame = tk.Frame(self.ftg_right_frame)
        self.ftg_right_calc_frame.pack(side=tk.RIGHT, anchor='ne', fill=tk.BOTH,expand=1)
        self.ftg_right_frame.grid(row=0, column=1, padx=5)

        wftg_entry = 7
        #Left
        tk.Label(self.ftg_left_inputs_frame, text="B = ", font=self.helv).grid(row=1, column=0, sticky = tk.E)
        tk.Entry(self.ftg_left_inputs_frame, textvariable=self.b1, width=wftg_entry, validate="key", validatecommand=self.reset_status).grid(row=1, column=1)
        tk.Label(self.ftg_left_inputs_frame, text="ft", font=self.helv).grid(row=1, column=2)

        tk.Label(self.ftg_left_inputs_frame, text="D = ", font=self.helv).grid(row=2, column=0, sticky = tk.E)
        tk.Entry(self.ftg_left_inputs_frame, textvariable=self.d1, width=wftg_entry, validate="key", validatecommand=self.reset_status).grid(row=2, column=1)
        tk.Label(self.ftg_left_inputs_frame, text="ft", font=self.helv).grid(row=2, column=2)

        tk.Label(self.ftg_left_inputs_frame, text="H = ", font=self.helv).grid(row=3, column=0, sticky = tk.E)
        tk.Entry(self.ftg_left_inputs_frame, textvariable=self.h1, width=wftg_entry, validate="key", validatecommand=self.reset_status).grid(row=3, column=1)
        tk.Label(self.ftg_left_inputs_frame, text="in", font=self.helv).grid(row=3, column=2)
        tk.Label(self.ftg_left_inputs_frame, text="Column:", font=self.helv_res).grid(row=4, column=0, pady=5)

        tk.Label(self.ftg_left_inputs_frame, text="B = ", font=self.helv).grid(row=5, column=0, sticky = tk.E)
        tk.Entry(self.ftg_left_inputs_frame, textvariable=self.cb1, width=wftg_entry, validate="key", validatecommand=self.reset_status).grid(row=5, column=1)
        tk.Label(self.ftg_left_inputs_frame, text="in", font=self.helv).grid(row=5, column=2)

        tk.Label(self.ftg_left_inputs_frame, text="D = ", font=self.helv).grid(row=6, column=0, sticky = tk.E)
        tk.Entry(self.ftg_left_inputs_frame, textvariable=self.cd1, width=wftg_entry, validate="key", validatecommand=self.reset_status).grid(row=6, column=1)
        tk.Label(self.ftg_left_inputs_frame, text="in", font=self.helv).grid(row=6, column=2)

        tk.Label(self.ftg_left_inputs_frame, text="Eccentricty:", font=self.helv_res).grid(row=7, column=0, pady=5)
        tk.Label(self.ftg_left_inputs_frame, text="e = ", font=self.helv).grid(row=8, column=0, sticky = tk.E)
        tk.Entry(self.ftg_left_inputs_frame, textvariable=self.ce1, width=wftg_entry, validate="key", validatecommand=self.reset_status).grid(row=8, column=1)
        tk.Label(self.ftg_left_inputs_frame, text="in", font=self.helv).grid(row=8, column=2)

        tk.Label(self.ftg_left_inputs_frame, text="Loads: ", font=self.helv_res).grid(row=9, column=0, pady=5)
        tk.Label(self.ftg_left_inputs_frame, text="Pl,service = ", font=self.helv).grid(row=10, column=0, sticky = tk.E)
        tk.Entry(self.ftg_left_inputs_frame, textvariable=self.p1_service_kips, width=wftg_entry, validate="key", validatecommand=self.reset_status).grid(row=10, column=1)
        tk.Label(self.ftg_left_inputs_frame, text="kips", font=self.helv).grid(row=10, column=2)

        tk.Label(self.ftg_left_inputs_frame, text="Pl,ultimate = ", font=self.helv).grid(row=11, column=0, sticky = tk.E)
        tk.Entry(self.ftg_left_inputs_frame, textvariable=self.p1_ultimate_kips, width=wftg_entry, validate="key", validatecommand=self.reset_status).grid(row=11, column=1)
        tk.Label(self.ftg_left_inputs_frame, text="kips", font=self.helv).grid(row=11, column=2)

        self.left_bar_size = tk.StringVar()
        self.inputs.append(self.left_bar_size)
        self.left_bar_size.set('3')
        self.left_bar_size_label = tk.Label(self.ftg_left_inputs_frame, text="Bar Size (#) : ", font=self.helv)
        self.left_bar_size_label.grid(row=12,column=0, pady=2)
        self.left_bar_size_menu = tk.OptionMenu(self.ftg_left_inputs_frame, self.left_bar_size, '3', '4', '5','6','7','8','9','10','11','14','18', command=self.reset_status)
        self.left_bar_size_menu.config(font=self.helv)
        self.left_bar_size_menu.grid(row=12, column=1, padx= 2, sticky=tk.W)

        self.left_ftg_calc_txtbox = tk.Text(self.ftg_left_calc_frame, height = 25, width = 70, bg= "grey90", font= self.helv_norm, wrap=tk.WORD)
        self.left_ftg_calc_txtbox.grid(row=0, column=0, sticky='nsew')

        self.left_ftg_scroll = tk.Scrollbar(self.ftg_left_calc_frame, command=self.left_ftg_calc_txtbox.yview)
        self.left_ftg_scroll.grid(row=0, column=1, sticky='nsew')
        self.left_ftg_calc_txtbox['yscrollcommand'] = self.left_ftg_scroll.set

        #Right
        tk.Label(self.ftg_right_inputs_frame, text="B = ", font=self.helv).grid(row=1, column=0, sticky = tk.E)
        tk.Entry(self.ftg_right_inputs_frame, textvariable=self.b2, width=wftg_entry, validate="key", validatecommand=self.reset_status).grid(row=1, column=1)
        tk.Label(self.ftg_right_inputs_frame, text="ft", font=self.helv).grid(row=1, column=2)

        tk.Label(self.ftg_right_inputs_frame, text="D = ", font=self.helv).grid(row=2, column=0, sticky = tk.E)
        tk.Entry(self.ftg_right_inputs_frame, textvariable=self.d2, width=wftg_entry, validate="key", validatecommand=self.reset_status).grid(row=2, column=1)
        tk.Label(self.ftg_right_inputs_frame, text="ft", font=self.helv).grid(row=2, column=2)

        tk.Label(self.ftg_right_inputs_frame, text="H = ", font=self.helv).grid(row=3, column=0, sticky = tk.E)
        tk.Entry(self.ftg_right_inputs_frame, textvariable=self.h2, width=wftg_entry, validate="key", validatecommand=self.reset_status).grid(row=3, column=1)
        tk.Label(self.ftg_right_inputs_frame, text="in", font=self.helv).grid(row=3, column=2)

        tk.Label(self.ftg_right_inputs_frame, text="Column:", font=self.helv_res).grid(row=4, column=0, pady=5)

        tk.Label(self.ftg_right_inputs_frame, text="B = ", font=self.helv).grid(row=5, column=0, sticky = tk.E)
        tk.Entry(self.ftg_right_inputs_frame, textvariable=self.cb2, width=wftg_entry, validate="key", validatecommand=self.reset_status).grid(row=5, column=1)
        tk.Label(self.ftg_right_inputs_frame, text="in", font=self.helv).grid(row=5, column=2)

        tk.Label(self.ftg_right_inputs_frame, text="D = ", font=self.helv).grid(row=6, column=0, sticky = tk.E)
        tk.Entry(self.ftg_right_inputs_frame, textvariable=self.cd2, width=wftg_entry, validate="key", validatecommand=self.reset_status).grid(row=6, column=1)
        tk.Label(self.ftg_right_inputs_frame, text="in", font=self.helv).grid(row=6, column=2)

        tk.Label(self.ftg_right_inputs_frame, text="Eccentricty:", font=self.helv_res).grid(row=7, column=0, pady=5)

        tk.Label(self.ftg_right_inputs_frame, text="e = ", font=self.helv).grid(row=8, column=0, sticky = tk.E)
        tk.Entry(self.ftg_right_inputs_frame, textvariable=self.ce2, width=wftg_entry, validate="key", validatecommand=self.reset_status).grid(row=8, column=1)
        tk.Label(self.ftg_right_inputs_frame, text="in", font=self.helv).grid(row=8, column=2)

        tk.Label(self.ftg_right_inputs_frame, text="Loads: ", font=self.helv_res).grid(row=9, column=0, pady=5)

        tk.Label(self.ftg_right_inputs_frame, text="Pr,service = ", font=self.helv).grid(row=10, column=0, sticky = tk.E)
        tk.Entry(self.ftg_right_inputs_frame, textvariable=self.p2_service_kips, width=wftg_entry, validate="key", validatecommand=self.reset_status).grid(row=10, column=1)
        tk.Label(self.ftg_right_inputs_frame, text="kips", font=self.helv).grid(row=10, column=2)

        tk.Label(self.ftg_right_inputs_frame, text="Pr,ultimate = ", font=self.helv).grid(row=11, column=0, sticky = tk.E)
        tk.Entry(self.ftg_right_inputs_frame, textvariable=self.p2_ultimate_kips, width=wftg_entry, validate="key", validatecommand=self.reset_status).grid(row=11, column=1)
        tk.Label(self.ftg_right_inputs_frame, text="kips", font=self.helv).grid(row=11, column=2)

        self.right_bar_size = tk.StringVar()
        self.inputs.append(self.right_bar_size)
        self.right_bar_size.set('3')
        self.right_bar_size_label = tk.Label(self.ftg_right_inputs_frame, text="Bar Size (#) : ", font=self.helv)
        self.right_bar_size_label.grid(row=12,column=0, pady=2)
        self.right_bar_size_menu = tk.OptionMenu(self.ftg_right_inputs_frame, self.right_bar_size, '3', '4', '5','6','7','8','9','10','11','14','18', command=self.reset_status)
        self.right_bar_size_menu.config(font=self.helv)
        self.right_bar_size_menu.grid(row=12, column=1, padx= 2, sticky=tk.W)

        self.right_ftg_calc_txtbox = tk.Text(self.ftg_right_calc_frame, height = 25, width = 70, bg= "grey90", font= self.helv_norm, wrap=tk.WORD)
        self.right_ftg_calc_txtbox.grid(row=0, column=0, sticky='nsew')

        self.right_ftg_scroll = tk.Scrollbar(self.ftg_right_calc_frame, command=self.right_ftg_calc_txtbox.yview)
        self.right_ftg_scroll.grid(row=0, column=1, sticky='nsew')
        self.right_ftg_calc_txtbox['yscrollcommand'] = self.right_ftg_scroll.set

    def strap_design_frame_builder(self):
        self.strap_inputs_frame = tk.Frame(self.strap_design_frame)
        self.strap_inputs_frame.pack(side=tk.LEFT, anchor='nw')
        self.strap_calc_frame = tk.Frame(self.strap_design_frame)
        self.strap_calc_frame.pack(side=tk.RIGHT ,anchor='ne', fill=tk.BOTH, expand=1)


        tk.Label(self.strap_inputs_frame, text="B = ", font=self.helv).grid(row=0, column=0, sticky = tk.E)
        tk.Entry(self.strap_inputs_frame, textvariable=self.bs, width=10, validate="key", validatecommand=self.reset_status).grid(row=0, column=1)
        tk.Label(self.strap_inputs_frame, text="in", font=self.helv).grid(row=0, column=2)

        tk.Label(self.strap_inputs_frame, text="H = ", font=self.helv).grid(row=1, column=0, sticky = tk.E)
        tk.Entry(self.strap_inputs_frame, textvariable=self.hs, width=10, validate="key", validatecommand=self.reset_status).grid(row=1, column=1)
        tk.Label(self.strap_inputs_frame, text="in", font=self.helv).grid(row=1, column=2)

        self.strap_vbar_size = tk.StringVar()
        self.inputs.append(self.strap_vbar_size)
        self.strap_vbar_size.set('3')
        self.strap_vbar_size_label = tk.Label(self.strap_inputs_frame, text="Shear\nBar Size (#) : ", font=self.helv)
        self.strap_vbar_size_label.grid(row=2,column=0, pady=2)
        self.strap_vbar_size_menu = tk.OptionMenu(self.strap_inputs_frame, self.strap_vbar_size, '3', '4', '5', command=self.reset_status)
        self.strap_vbar_size_menu.config(font=self.helv)
        self.strap_vbar_size_menu.grid(row=2, column=1, padx= 2, sticky=tk.W)

        self.strap_bar_size = tk.StringVar()
        self.inputs.append(self.strap_bar_size)
        self.strap_bar_size.set('3')
        self.strap_bar_size_label = tk.Label(self.strap_inputs_frame, text="Flexure\nBar Size (#) : ", font=self.helv)
        self.strap_bar_size_label.grid(row=4,column=0, pady=2)
        self.strap_bar_size_menu = tk.OptionMenu(self.strap_inputs_frame, self.strap_bar_size, '3', '4', '5','6','7','8','9','10','11','14','18', command=self.reset_status)
        self.strap_bar_size_menu.config(font=self.helv)
        self.strap_bar_size_menu.grid(row=4, column=1, padx= 2, sticky=tk.W)

        self.strap_calc_txtbox = tk.Text(self.strap_calc_frame, height = 25, width = 70, bg= "grey90", font= self.helv_norm, wrap=tk.WORD)
        self.strap_calc_txtbox.grid(row=0, column=0, sticky='nsew')

        self.strap_scroll = tk.Scrollbar(self.strap_calc_frame, command=self.strap_calc_txtbox.yview)
        self.strap_scroll.grid(row=0, column=1, sticky='nsew')
        self.strap_calc_txtbox['yscrollcommand'] = self.strap_scroll.set
        
    def det_res_scroll(self, *args):
        self.xc_listbox.yview(*args)
        self.cv_listbox.yview(*args)
        self.cm_listbox.yview(*args)

    def det_res_scroll_l(self, *args):
        self.xl_listbox.yview(*args)
        self.lv_listbox.yview(*args)
        self.lm_listbox.yview(*args)

    def det_res_scroll_r(self, *args):
        self.xr_listbox.yview(*args)
        self.rv_listbox.yview(*args)
        self.rm_listbox.yview(*args)

    def load_case_scroll(self, *args):
        self.load_case_listbox.yview(*args)
        self.load_case_res_listbox.yview(*args)
        
    def reset_status(self,*args):
        self.status_ftg1_q.set(0)
        self.status_ftg2_q.set(0)
        self.status_sumv.set(0)
        self.status_summ.set(0)
        self.status_ftg1v.set(0)
        self.status_ftg1f.set(0)
        self.status_ftg2v.set(0)
        self.status_ftg2f.set(0)
        self.status_sv.set(0)
        self.status_sf.set(0)

        self.b_refresh_figs.configure(text="Refresh Figures\n**NOT CURRENT**")
        self.b_calc.configure(text="Calc/ReCalc\n**NOT CURRENT**")

        return True

    def run_calcs(self):
        self.basic_calcs()

        #Refresh figures at the same time as running the calcs
        #So user doesn't have to push both buttons
        self.refresh_figs()

        self.b_calc.configure(text="Calc/ReCalc")

    def quit_app(self):
        self.master.destroy()
        self.master.quit()

    def refresh_figs(self):
        self.draw_plan()
        self.draw_elevation()

        self.b_refresh_figs.configure(text="Refresh Figures")

    def draw_plan(self, *event):
        space = 10
        self.g_plan_canvas.delete("all")
        w = self.g_plan_canvas.winfo_width()
        h = self.g_plan_canvas.winfo_height()

        b1_ft = float(self.b1.get())
        d1_ft = float(self.d1.get())
        e1_ft = float(self.ce1.get())/12.0

        cb1_ft = (float(self.cb1.get()))/12.0
        cd1_ft = (float(self.cd1.get()))/12.0

        b2_ft = float(self.b2.get())
        d2_ft = float(self.d2.get())
        e2_ft = float(self.ce2.get())/12.0

        cb2_ft = (float(self.cb2.get()))/12.0
        cd2_ft = (float(self.cd2.get()))/12.0

        bs_in = float(self.bs.get())
        bs_ft = bs_in/12.0
        s_ext_ft = float(self.s_extension_in.get())/12.0

        lcc_ft = float(self.lcc.get())

        ls_ft = lcc_ft - (b1_ft/2.0) - ((b1_ft/2.0)-e1_ft) - (b2_ft/2.0) - e2_ft

        l = b1_ft + ls_ft + b2_ft

        h_scale = max(d1_ft,d2_ft) / (h-(2*space))

        w_scale = l / (w-(2*space))

        scale = max(h_scale, w_scale)

        #left ftg
        x0 = space
        x1 = space+(b1_ft/scale)
        y0 = (h/2)+((d1_ft*0.5)/scale)
        y1 = (h/2)-((d1_ft*0.5)/scale)

        self.g_plan_canvas.create_rectangle(x0,y0,x1,y1, fill = "blue", width=2)

        #right ftg
        x2 = x1+(ls_ft/scale)
        x3 = x2 + (b2_ft/scale)
        y2 = (h/2)+((d2_ft*0.5)/scale)
        y3 = (h/2)-((d2_ft*0.5)/scale)

        self.g_plan_canvas.create_rectangle(x2,y2,x3,y3, fill = "blue", width=2)

        #strap
        x4 = space
        x5 = x2 + ((b2_ft/2.0)/scale) + (e2_ft/scale) + ((cb2_ft/2.0)/scale) + (s_ext_ft/scale)
        y4 = (h/2)+((bs_ft*0.5)/scale)
        y5 = (h/2)-((bs_ft*0.5)/scale)

        self.g_plan_canvas.create_rectangle(x4,y4,x5,y5, fill = "red", width=2)

        #left col
        x6 = space + (e1_ft/scale) - ((cb1_ft/2.0)/scale)
        x7 = space + (e1_ft/scale) + ((cb1_ft/2.0)/scale)
        y6 = (h/2)+((cd1_ft/2.0)/scale)
        y7 = (h/2)-((cd1_ft/2.0)/scale)

        self.g_plan_canvas.create_rectangle(x6,y6,x7,y7, fill = "green", width=2)

        #right column
        x8 = space + ((e1_ft+lcc_ft)/scale) - ((cb2_ft/2.0)/scale)
        x9 = space + ((e1_ft+lcc_ft)/scale) + ((cb2_ft/2.0)/scale)
        y8 = (h/2)+((cd2_ft/2.0)/scale)
        y9 = (h/2)-((cd2_ft/2.0)/scale)

        self.g_plan_canvas.create_rectangle(x8,y8,x9,y9, fill = "green", width=2)

        #center lines
        self.g_plan_canvas.create_line((b1_ft/2.0)/scale + space, 0, (b1_ft/2.0)/scale + space, h)
        self.g_plan_canvas.create_line((b1_ft + ls_ft + (b2_ft/2))/scale + space, 0, (b1_ft + ls_ft + (b2_ft/2))/scale + space, h)
        self.g_plan_canvas.create_line(0, h/2.0, w, h/2.0)

    def draw_elevation(self, *event):
        space = 10
        self.g_elev_canvas.delete("all")
        w = self.g_elev_canvas.winfo_width()
        h = self.g_elev_canvas.winfo_height()

        b1_ft = float(self.b1.get())
        h1_ft = float(self.h1.get())/12.0
        e1_ft = float(self.ce1.get())/12.0

        cb1_ft = (float(self.cb1.get()))/12.0
        cd1_ft = (float(self.cd1.get()))/12.0

        b2_ft = float(self.b2.get())
        h2_ft = float(self.h2.get())/12.0
        e2_ft = float(self.ce2.get())/12.0

        cb2_ft = (float(self.cb2.get()))/12.0
        cd2_ft = (float(self.cd2.get()))/12.0


        hs_in = float(self.hs.get())
        hs_ft = hs_in/12.0
        s_ext_ft = float(self.s_extension_in.get())/12.0
        s_elev = float(self.s_elev_in.get())

        lcc_ft = float(self.lcc.get())

        ls_ft = lcc_ft - (b1_ft/2.0) - ((b1_ft/2.0)-e1_ft) - (b2_ft/2.0) - e2_ft

        l = b1_ft + ls_ft + b2_ft

        h_scale = ((s_elev/12.0) + hs_ft + 1) / (h-(2*space))

        w_scale = l / (w-(2*space))

        scale = max(h_scale, w_scale)

        #left ftg
        xl0 = space
        yl0 = h - space
        xl1 = space + b1_ft/scale
        yl1 = (h - space) - h1_ft/scale

        self.g_elev_canvas.create_rectangle(xl0,yl0,xl1,yl1, fill = "blue", width=2)

        #Right Ftg
        xr1 = xl1 + (ls_ft/scale)
        yr1 = yl0
        xr2 = xr1 + (b2_ft/scale)
        yr2 = (h - space) - h2_ft/scale

        self.g_elev_canvas.create_rectangle(xr1,yr1,xr2,yr2, fill = "blue", width=2)

        #Strap
        sx1 = xl0
        sy1 = yl1
        sx2 = xl1
        sy2 = yl1
        sx3 = sx2
        sy3 = (h-space) - ((s_elev/12.0)/scale)
        sx4 = xr1
        sy4 = sy3
        sx5 = sx4
        sy5 = yr2
        sx6 = xr1 + ((b2_ft/2.0) + e2_ft + (cb2_ft/2.0) + (s_ext_ft))/scale
        sy6 = sy5
        sx7 = sx6
        sy7 = sy3 - hs_ft/scale
        sx8 = sx1
        sy8 = sy7

        self.g_elev_canvas.create_polygon(sx1,sy1,sx2,sy2,sx3,sy3,sx4,sy4,sx5,sy5,sx6,sy6,sx7,sy7,sx8,sy8, fill="red", outline="black", width=2)

        #Left Column
        xcl1 = space + (e1_ft - (cb1_ft/2.0))/scale
        ycl1 = sy8
        xcl2 = xcl1 + cb1_ft/scale
        ycl2 = space

        self.g_elev_canvas.create_rectangle(xcl1,ycl1,xcl2,ycl2, fill = "green", width=2)

        #Right Column
        xcr1 = xr1 + ((b2_ft/2.0)+e2_ft-(cb2_ft/2.0))/scale
        ycr1 = sy8
        xcr2 = xcr1 + cb2_ft/scale
        ycr2 = space

        self.g_elev_canvas.create_rectangle(xcr1,ycr1,xcr2,ycr2, fill = "green", width=2)

        #ftg center lines
        self.g_elev_canvas.create_line((b1_ft/2.0)/scale + space, 0, (b1_ft/2.0)/scale + space, h)
        self.g_elev_canvas.create_line((b1_ft + ls_ft + (b2_ft/2))/scale + space, 0, (b1_ft + ls_ft + (b2_ft/2))/scale + space, h)

    def basic_calcs(self):
        #Caclulate Self Weights and quick check on footing dimensions assuming a concentric load

        #Common data items

        qa_ksf = float(self.Qa_ksf.get())
        fpc_ksi = float(self.Fpc_ksi.get())
        sw_pcf = float(self.density_pcf.get())
        fpc_psi = fpc_ksi * 1000.0
        dl_factor = float(self.dl_factor.get())
        dl_service_factor = float(self.dl_service_factor.get())
        fy_ksi = float(self.Fy_ksi.get())

        self.rebar = concbeam.reinforcement(fy_ksi)

        lcc_ft = float(self.lcc.get())

        #Common data items - Formatted output text
        self.commons_out_text = '{:*^85}\n'.format('  Strap Beam - Analysis and Design - v. alpha  ')
        self.commons_out_text = self.commons_out_text + 'For best formatting of this file use a monospace font type such as: Courier New\n'
        self.commons_out_text = self.commons_out_text + 'and a Font Size of : 8\n'
        self.commons_out_text = self.commons_out_text + '\n-- {0:-<82}\n'.format('Common Inputs ')
        self.commons_out_text = self.commons_out_text + '{0:<22} {1:<12.3f}ksf  (Allowable Soil Bearing)\n'.format('Q,allow :', qa_ksf)
        self.commons_out_text = self.commons_out_text + "{0:<22} {1:<12.3f}ksi  (Used for both Foundations and Strap Beam)\n".format("F'c :",fpc_ksi)
        self.commons_out_text = self.commons_out_text + '{0:<22} {1:<12.3f}pcf  (Used for self weights)\n'.format('Concrete Density :',sw_pcf)
        self.commons_out_text = self.commons_out_text + '{0:<22} {1:<12.3f}(Used to factor self weight for Service values)\n'.format('DL Factor Service :', dl_service_factor)
        self.commons_out_text = self.commons_out_text + '{0:<22} {1:<12.3f}(Used to factor self weight for Ultimate values)\n'.format('DL Factor Ultimate :', dl_factor)
        self.commons_out_text = self.commons_out_text + '{0:<22} {1:<12.3f}ksi  (Reinforcing Steel Yield Strength)\n'.format('Fy :',fy_ksi)
        self.commons_out_text = self.commons_out_text + '\n{0:<22} {1:<12.3f}ft  (Center to Center distance between columns)\n'.format('L,cc :',lcc_ft)
        
        #Strap
        bs_in = float(self.bs.get())
        bs_ft = bs_in/12.0
        hs_in = float(self.hs.get())
        hs_ft = hs_in/12.0
        s_ext_ft = float(self.s_extension_in.get())/12.0
        s_elev = float(self.s_elev_in.get())
        
        I_strap_in4 = (bs_in * hs_in*hs_in*hs_in) / 12.0
        self.strap_ig_in4.set('{0:.3f}'.format(I_strap_in4))

        self.strap_sw_klf = (bs_ft*hs_ft*sw_pcf)/1000.0
        self.s_sw_klf.set('{0:.3f}'.format(self.strap_sw_klf))

        #Left Foundation

        b1_ft = float(self.b1.get())
        d1_ft = float(self.d1.get())
        h1_ft = float(self.h1.get())/12.0
        e1_ft = float(self.ce1.get())/12.0
        
        I_left_in4 = (d1_ft*12 * h1_ft*12* h1_ft*12* h1_ft*12)/12.0
        self.left_ig_in4.set('{0:.3f}'.format(I_left_in4))
        self.igs_over_igl.set('{0:.3f}'.format(I_strap_in4 / I_left_in4))

        cb1_ft = (float(self.cb1.get()))/12.0
        cd1_ft = (float(self.cd1.get()))/12.0

        p1s_kips = float(self.p1_service_kips.get())
        p1u_kips = float(self.p1_ultimate_kips.get())

        self.ftg1_A_sqft = b1_ft*d1_ft
        self.ftg1_sw_kips = (b1_ft*d1_ft*h1_ft*sw_pcf) / 1000.0

        self.left_sw_kips.set('{0:.3f}'.format(self.ftg1_sw_kips))

        self.left_fnd_out_text = '\n-- {0:-<82}\n'.format('Left Foundation ')
        self.left_fnd_out_text = self.left_fnd_out_text + '{0:<10} {1:<7.3f} ft\n'.format('B =',b1_ft)
        self.left_fnd_out_text = self.left_fnd_out_text + '{0:<10} {1:<7.3f} ft\n'.format('D =',d1_ft)
        self.left_fnd_out_text = self.left_fnd_out_text + '{0:<10} {1:<7.3f} ft\n'.format('H =',h1_ft)
        self.left_fnd_out_text = self.left_fnd_out_text + '\n{0:<10} B x D = {1:<7.3f} ft^2\n'.format('A =',self.ftg1_A_sqft)
        self.left_fnd_out_text = self.left_fnd_out_text + '{0:<10} B x D x H x Concrete Density = {1:<7.3f} kips\n'.format('Self Wt =',self.ftg1_sw_kips)

        self.left_col_out_text = '\n-- {0:-<82}\n'.format('Left Column ')
        self.left_col_out_text = self.left_col_out_text + '{0:<14} {1:<7.3f} ft\n'.format('B =',cb1_ft)
        self.left_col_out_text = self.left_col_out_text + '{0:<14} {1:<7.3f} ft\n'.format('D =',cd1_ft)
        self.left_col_out_text = self.left_col_out_text + '{0:<14} {1:<7.3f} ft (left edge of footing to center of column - parallel to B)\n'.format('e =',e1_ft)
        self.left_col_out_text = self.left_col_out_text + '- Loads -\n{0:<14} {1:<7.3f} kips\n'.format('P,service =',p1s_kips)
        self.left_col_out_text = self.left_col_out_text + '{0:<14} {1:<7.3f} kips\n'.format('P,ultimate =',p1u_kips)

        #Right Foundation
        b2_ft = float(self.b2.get())
        d2_ft = float(self.d2.get())
        h2_ft = float(self.h2.get())/12.0
        e2_ft = float(self.ce2.get())/12.0

        I_right_in4 = (d2_ft*12 * h2_ft*12* h2_ft*12* h2_ft*12)/12.0
        self.right_ig_in4.set('{0:.3f}'.format(I_right_in4))
        self.igs_over_igr.set('{0:.3f}'.format(I_strap_in4 / I_right_in4))
        
        cb2_ft = (float(self.cb2.get()))/12.0
        cd2_ft = (float(self.cd2.get()))/12.0

        p2s_kips = float(self.p2_service_kips.get())
        p2u_kips = float(self.p2_ultimate_kips.get())

        self.ftg2_A_sqft = b2_ft*d2_ft
        self.ftg2_sw_kips = (b2_ft*d2_ft*h2_ft*sw_pcf) / 1000.0

        self.right_sw_kips.set('{0:.3f}'.format(self.ftg2_sw_kips))

        self.right_fnd_out_text = '\n-- {0:-<82}\n'.format('Right Foundation ')
        self.right_fnd_out_text = self.right_fnd_out_text + '{0:<10} {1:<7.3f} ft\n'.format('B =',b2_ft)
        self.right_fnd_out_text = self.right_fnd_out_text + '{0:<10} {1:<7.3f} ft\n'.format('D =',d2_ft)
        self.right_fnd_out_text = self.right_fnd_out_text + '{0:<10} {1:<7.3f} ft\n'.format('H =',h2_ft)
        self.right_fnd_out_text = self.right_fnd_out_text + '\n{0:<10} B x D = {1:<7.3f} ft^2\n'.format('A =',self.ftg2_A_sqft)
        self.right_fnd_out_text = self.right_fnd_out_text + '{0:<10} B x D x H x Concrete Density = {1:<7.3f} kips\n'.format('Self Wt =',self.ftg2_sw_kips)

        self.right_col_out_text = '\n-- {0:-<82}\n'.format('Right Column ')
        self.right_col_out_text = self.right_col_out_text + '{0:<14} {1:<7.3f} ft\n'.format('B =',cb2_ft)
        self.right_col_out_text = self.right_col_out_text + '{0:<14} {1:<7.3f} ft\n'.format('D =',cd2_ft)
        self.right_col_out_text = self.right_col_out_text + '{0:<14} {1:<7.3f} ft (center of footing to center of column - parallel to B)\n'.format('e =',e2_ft)
        self.right_col_out_text = self.right_col_out_text + '- Loads -\n{0:<14} {1:<7.3f} kips\n'.format('P,service =',p2s_kips)
        self.right_col_out_text = self.right_col_out_text + '{0:<14} {1:<7.3f} kips\n'.format('P,ultimate =',p2u_kips)

        ls_ft = lcc_ft - (b1_ft/2.0) - ((b1_ft/2.0)-e1_ft) - (b2_ft/2.0) - e2_ft

        self.s_ls_ft.set('{0:.3f}'.format(ls_ft))
        self.s_swm_kips.set('{0:.3f}'.format(ls_ft*self.strap_sw_klf))

        strap_h_over_ftg1 = hs_ft - h1_ft + (s_elev/12.0)
        s_sw_over_ftg1 = (strap_h_over_ftg1 * bs_ft*sw_pcf)/1000.0
        self.s_swl_kips.set('{0:.3f}'.format(b1_ft*s_sw_over_ftg1))

        strap_h_over_ftg2 = hs_ft - h2_ft + (s_elev/12.0)
        s_sw_over_ftg2 = (strap_h_over_ftg2 * bs_ft*sw_pcf)/1000.0
        strap_l_over_ftg2 = ((b2_ft/2.0) + e2_ft + (cb2_ft/2.0) + (s_ext_ft))
        self.s_swr_kips.set('{0:.3f}'.format(strap_l_over_ftg2*s_sw_over_ftg2))

        self.strap_out_text = '\n-- {0:-<82}\n'.format('Strap Beam ')
        self.strap_out_text = self.strap_out_text + '{0:<14} {1:<7.3f} ft\n'.format('Bs =',bs_ft)
        self.strap_out_text = self.strap_out_text + '{0:<14} {1:<7.3f} ft\n'.format('Hs =',hs_ft)
        self.strap_out_text = self.strap_out_text + 'Ls = Lcc - B,l/2 - (B,l/2 - e,l) - B,r/2 - e,r = {0:<7.3f} ft\n'.format(ls_ft)
        self.strap_out_text = self.strap_out_text + '\n{0:<20} {1:<7.3f} ft\n'.format('Ext. Beyond Column:',s_ext_ft)
        self.strap_out_text = self.strap_out_text + '{0:<20} {1:<7.3f} in\n(Delta in elevation from bottom of strap to bottom of footing)\n'.format('Strap Elevation:',s_elev)
        self.strap_out_text = self.strap_out_text + '\n{0:<12} {2:<43} {1:<7.3f} klf\n'.format('Self Wt. =',self.strap_sw_klf,'Bs x Hs x Concrete Density =')
        self.strap_out_text = self.strap_out_text + '\n{0:<12} {2:<43} {1:<7.3f} ft\n(Depth of Strap above left footing)\n'.format('Hs,l =',strap_h_over_ftg1, '(Hs - H,l) + (Strap Elevation/12.0) =')
        self.strap_out_text = self.strap_out_text + '\n{0:<12} {2:<43} {1:<7.3f} klf\n'.format('Self Wt.,l =',s_sw_over_ftg1, 'Bs x Hs,l x Concrete Density =')
        self.strap_out_text = self.strap_out_text + '\n{0:<12} {2:<43} {1:<7.3f} ft\n(Depth of Strap above right footing)\n'.format('Hs,r =',strap_h_over_ftg2, '(Hs - H,r) + (Strap Elevation/12.0) =')
        self.strap_out_text = self.strap_out_text + '\n{0:<12} {2:<43} {1:<7.3f} klf\n'.format('Self Wt.,r =',s_sw_over_ftg2, 'Bs x Hs,r x Concrete Density =')
        self.strap_out_text = self.strap_out_text + '\n{0:<12} {2:<43} {1:<7.3f} ft\n(length of strap over right footing)\n'.format('Ls,r =',strap_l_over_ftg2,'B,r/2 + e,r + Bcol,r/2 + Strap Extension =')

        #Waterfall to the statics calculation function
        self.statics_calcs()

    def statics_calcs(self):
        self.statics_out_text = '\n\n\n\n\n\n\n\n\n\n\n\n{0:-^85}\n{1:-^85}\n{2:-^85}\n'.format('-',' Statics for Soil Reactions - Service and Ultimate ','-')
        self.service_out_text = '\n{0:-^85}\n'.format('  SERVICE  ')
        self.service_out_text = self.service_out_text + '{0:^17}{1:^17}{2:^17}{3:^17}{4:^17}\n'.format('Source','Load (kips)', 'Location (ft)', 'Moment Arm (ft)','Moment (ft-kips)')
        self.service_out_text = self.service_out_text + '{0:_^85}\n'.format('_')
        self.ultimate_out_text = '\n\n{0:-^85}\n'.format('  ULTIMATE  ')
        self.ultimate_out_text = self.ultimate_out_text + '{0:^17}{1:^17}{2:^17}{3:^17}{4:^17}\n'.format('Source','Load (kips)', 'Location (ft)', 'Moment Arm (ft)','Moment (ft-kips)')
        self.ultimate_out_text = self.ultimate_out_text + '{0:_^85}\n'.format('_')

        #Solve for service and ultimate soil reactions by taking moments about left reaction and sum of vertical forces
        service = []
        ultimate = []
        #Common data items
        sw_pcf = float(self.density_pcf.get())
        qa_ksf = float(self.Qa_ksf.get())
        fpc_ksi = float(self.Fpc_ksi.get())
        fpc_psi = fpc_ksi * 1000.0
        dl_factor = float(self.dl_factor.get())
        dl_service_factor = float(self.dl_service_factor.get())

        #Strap
        bs_in = float(self.bs.get())
        bs_ft = bs_in/12.0
        hs_in = float(self.hs.get())
        hs_ft = hs_in/12.0
        s_ext_ft = float(self.s_extension_in.get())/12.0
        s_elev = float(self.s_elev_in.get())

        strap_sw_klf = (bs_ft*hs_ft*sw_pcf)/1000.0

        #Left Foundation
        b1_ft = float(self.b1.get())
        d1_ft = float(self.d1.get())
        h1_ft = float(self.h1.get())/12.0
        e1_ft = float(self.ce1.get())/12.0

        cb1_ft = (float(self.cb1.get()))/12.0
        cd1_ft = (float(self.cd1.get()))/12.0

        #Right Foundation
        b2_ft = float(self.b2.get())
        d2_ft = float(self.d2.get())
        h2_ft = float(self.h2.get())/12.0
        e2_ft = float(self.ce2.get())/12.0

        cb2_ft = (float(self.cb2.get()))/12.0
        cd2_ft = (float(self.cd2.get()))/12.0


        lcc_ft = float(self.lcc.get())

        ls_ft = lcc_ft - (b1_ft/2.0) - ((b1_ft/2.0)-e1_ft) - (b2_ft/2.0) - e2_ft

        p1s_kips = float(self.p1_service_kips.get())
        p1u_kips = float(self.p1_ultimate_kips.get())

        p1_loc = (b1_ft/2.0) - e1_ft

        service.append(['P1', p1s_kips, e1_ft, p1_loc, -1.0*p1s_kips*p1_loc])
        ultimate.append(['P1', p1u_kips, e1_ft, p1_loc, -1.0*p1u_kips*p1_loc])

        ftg1_A_sqft = b1_ft*d1_ft
        ftg1_sw_kips = (b1_ft*d1_ft*h1_ft*sw_pcf) / 1000.0
        ftg1_sw_loc = 0
        ftg1_sw_u_kips = dl_factor * ftg1_sw_kips

        service.append(['FTG_L', ftg1_sw_kips * dl_service_factor, b1_ft/2.0, 0, 0])
        ultimate.append(['FTG_L', ftg1_sw_u_kips, b1_ft/2.0, 0, 0])

        strap_h_over_ftg1 = hs_ft - h1_ft + (s_elev/12.0)
        s_sw_over_ftg1 = (strap_h_over_ftg1 * bs_ft*sw_pcf)/1000.0
        s_swl_kips = b1_ft*s_sw_over_ftg1

        service.append(['Strap/FTG_L', s_swl_kips * dl_service_factor, (b1_ft/2.0), 0, 0])
        ultimate.append(['Strap/FTG_L', s_swl_kips*dl_factor, (b1_ft/2.0), 0, 0])

        service.append(['Strap', strap_sw_klf*ls_ft * dl_service_factor, b1_ft + (ls_ft/2.0), (b1_ft/2.0) + (ls_ft/2.0), (strap_sw_klf*ls_ft * dl_service_factor)*((b1_ft/2.0) + (ls_ft/2.0))])
        ultimate.append(['Strap', strap_sw_klf*ls_ft*dl_factor, b1_ft + (ls_ft/2.0), (b1_ft/2.0) + (ls_ft/2.0), (strap_sw_klf*ls_ft*dl_factor)*((b1_ft/2.0) + (ls_ft/2.0))])

        strap_h_over_ftg2 = hs_ft - h2_ft + (s_elev/12.0)
        s_sw_over_ftg2 = (strap_h_over_ftg2 * bs_ft*sw_pcf)/1000.0
        strap_l_over_ftg2 = ((b2_ft/2.0) + e2_ft + (cb2_ft/2.0) + (s_ext_ft))
        s_swr_kips = strap_l_over_ftg2*s_sw_over_ftg2

        ps = s_swr_kips
        pu = dl_factor*ps
        x = b1_ft + ls_ft + strap_l_over_ftg2
        xm = (b1_ft/2.0) + ls_ft + (strap_l_over_ftg2/2.0)
        ms = ps*xm
        mu = pu*xm
        service.append(['Strap/FTG_R', ps * dl_service_factor, x, xm, ms * dl_service_factor])
        ultimate.append(['Strap/FTG_R', pu, x, xm, mu])


        self.ftg2_A_sqft = b2_ft*d2_ft
        self.ftg2_sw_kips = (b2_ft*d2_ft*h2_ft*sw_pcf) / 1000.0
        ps = self.ftg2_sw_kips
        pu = dl_factor*ps
        x = b1_ft + ls_ft + b2_ft/2.0
        xm = (b1_ft/2.0) + ls_ft + (b2_ft/2.0)
        ms = ps*xm
        mu = pu*xm
        service.append(['FTG_R', ps * dl_service_factor, x, xm, ms * dl_service_factor])
        ultimate.append(['FTG_R', pu, x, xm, mu])

        p2s_kips = float(self.p2_service_kips.get())
        p2u_kips = float(self.p2_ultimate_kips.get())

        p2_loc = (b1_ft/2.0) + ls_ft + (b2_ft/2.0) + e2_ft

        service.append(['P2', p2s_kips, p2_loc+(b1_ft/2.0), p2_loc, p2s_kips*p2_loc])
        ultimate.append(['P2', p2u_kips, p2_loc+(b1_ft/2.0), p2_loc, p2u_kips*p2_loc])

        for box in self.service_statics:
            box.delete(0,tk.END)
        for box in self.ultimate_statics:
            box.delete(0,tk.END)

        i=0
        ms = 0
        ps = 0
        for item in service:
            self.service_statics[0].insert(tk.END, item[0])
            self.service_statics[1].insert(tk.END, '{0:.3f}'.format(item[1]))
            self.service_statics[2].insert(tk.END, '{0:.3f}'.format(item[2]))
            self.service_statics[3].insert(tk.END, '{0:.3f}'.format(item[3]))
            self.service_statics[4].insert(tk.END, '{0:.3f}'.format(item[4]))
            ms = ms + item[4]
            ps = ps + item[1]

            self.service_out_text = self.service_out_text + '{0:>17}{1:^17.3f}{2:^17.3f}{3:^17.3f}{4:^17.3f}\n'.format(item[0], item[1], item[2], item[3], item[4])

            if i % 2 == 0:
                self.service_statics[0].itemconfigure(i, background="pale green")
                self.service_statics[1].itemconfigure(i, background="pale green")
                self.service_statics[2].itemconfigure(i, background="pale green")
                self.service_statics[3].itemconfigure(i, background="pale green")
                self.service_statics[4].itemconfigure(i, background="pale green")
            else:
                pass
            i+=1

        i=0
        mu = 0
        pu = 0
        for item in ultimate:
            self.ultimate_statics[0].insert(tk.END, item[0])
            self.ultimate_statics[1].insert(tk.END, '{0:.3f}'.format(item[1]))
            self.ultimate_statics[2].insert(tk.END, '{0:.3f}'.format(item[2]))
            self.ultimate_statics[3].insert(tk.END, '{0:.3f}'.format(item[3]))
            self.ultimate_statics[4].insert(tk.END, '{0:.3f}'.format(item[4]))
            mu = mu + item[4]
            pu = pu + item[1]

            self.ultimate_out_text = self.ultimate_out_text + '{0:>17}{1:^17.3f}{2:^17.3f}{3:^17.3f}{4:^17.3f}\n'.format(item[0], item[1], item[2], item[3], item[4])

            if i % 2 == 0:
                self.ultimate_statics[0].itemconfigure(i, background="pale green")
                self.ultimate_statics[1].itemconfigure(i, background="pale green")
                self.ultimate_statics[2].itemconfigure(i, background="pale green")
                self.ultimate_statics[3].itemconfigure(i, background="pale green")
                self.ultimate_statics[4].itemconfigure(i, background="pale green")
            else:
                pass
            i+=1

        R2_moment_arm = (b1_ft/2.0) + ls_ft + (b2_ft/2.0)
        R2_loc = b1_ft + ls_ft + (b2_ft/2.0)
        R2s = ms / R2_moment_arm
        R2u = mu / R2_moment_arm

        R1s = ps - R2s
        R1u = pu - R2u

        service.append(['R1',R1s,b1_ft/2.0,0,0])
        ultimate.append(['R1',R1u,b1_ft/2.0,0,0])

        service.append(['R2',R2s,R2_loc,R2_moment_arm,R2s*R2_moment_arm])
        ultimate.append(['R2',R2u,R2_loc,R2_moment_arm,R2u*R2_moment_arm])

        if 0.999999<((R2s*R2_moment_arm) / ms) <1.000001 and 0.999999<((R2u*R2_moment_arm) / mu)<1.000001:
            self.status_summ.set(1)
        else:
            self.status_summ.set(0)

        if 0.999999 < ((R2s + R1s) / ps) < 1.000001  and 0.999999 < ((R2u + R1u) / pu) < 1.000001:
            self.status_sumv.set(1)
        else:
            self.status_sumv.set(0)

        self.service_statics[0].insert(tk.END, 'Totals: ')
        self.service_statics[1].insert(tk.END, '{0:.3f}'.format(ps))
        self.service_statics[2].insert(tk.END, '--')
        self.service_statics[3].insert(tk.END, '--')
        self.service_statics[4].insert(tk.END, '{0:.3f}'.format(ms))
        self.ultimate_statics[0].insert(tk.END, 'Totals: ')
        self.ultimate_statics[1].insert(tk.END, '{0:.3f}'.format(pu))
        self.ultimate_statics[2].insert(tk.END, '--')
        self.ultimate_statics[3].insert(tk.END, '--')
        self.ultimate_statics[4].insert(tk.END, '{0:.3f}'.format(mu))

        self.service_out_text = self.service_out_text + '{0:_^85}\n'.format('_')
        self.service_out_text = self.service_out_text + '{0:>17}{1:^17.3f}{2:^17}{3:^17}{4:^17.3f}\n'.format('Totals:', ps, '--', '--', ms)
        self.service_out_text = self.service_out_text + '{0:_^85}\n'.format('_')
        self.service_out_text = self.service_out_text + '{0:>17}{1:^17.3f}{2:^17.3f}{3:^17.3f}{4:^17.3f}\n'.format('R1',R1s,b1_ft/2.0,0,0)
        self.service_out_text = self.service_out_text + '{0:>17}{1:^17.3f}{2:^17.3f}{3:^17.3f}{4:^17.3f}\n'.format('R2',R2s,R2_loc,R2_moment_arm,R2s*R2_moment_arm)


        self.ultimate_out_text = self.ultimate_out_text + '{0:_^85}\n'.format('_')
        self.ultimate_out_text = self.ultimate_out_text + '{0:>17}{1:^17.3f}{2:^17}{3:^17}{4:^17.3f}\n'.format('Totals:', pu, '--', '--', mu)
        self.ultimate_out_text = self.ultimate_out_text + '{0:_^85}\n'.format('_')
        self.ultimate_out_text = self.ultimate_out_text + '{0:>17}{1:^17.3f}{2:^17.3f}{3:^17.3f}{4:^17.3f}\n'.format('R1',R1u,b1_ft/2.0,0,0)
        self.ultimate_out_text = self.ultimate_out_text + '{0:>17}{1:^17.3f}{2:^17.3f}{3:^17.3f}{4:^17.3f}\n\n\n'.format('R2',R2u,R2_loc,R2_moment_arm,R2u*R2_moment_arm)

        self.ultimate_statics[0].insert(tk.END, ultimate[-1][0])
        self.ultimate_statics[1].insert(tk.END, '{0:.3f}'.format(ultimate[-1][1]))
        self.ultimate_statics[2].insert(tk.END, '{0:.3f}'.format(ultimate[-1][2]))
        self.ultimate_statics[3].insert(tk.END, '{0:.3f}'.format(ultimate[-1][3]))
        self.ultimate_statics[4].insert(tk.END, '{0:.3f}'.format(ultimate[-1][4]))

        self.ultimate_statics[0].insert(tk.END, ultimate[-2][0])
        self.ultimate_statics[1].insert(tk.END, '{0:.3f}'.format(ultimate[-2][1]))
        self.ultimate_statics[2].insert(tk.END, '{0:.3f}'.format(ultimate[-2][2]))
        self.ultimate_statics[3].insert(tk.END, '{0:.3f}'.format(ultimate[-2][3]))
        self.ultimate_statics[4].insert(tk.END, '{0:.3f}'.format(ultimate[-2][4]))


        self.service_statics[0].insert(tk.END, service[-1][0])
        self.service_statics[1].insert(tk.END, '{0:.3f}'.format(service[-1][1]))
        self.service_statics[2].insert(tk.END, '{0:.3f}'.format(service[-1][2]))
        self.service_statics[3].insert(tk.END, '{0:.3f}'.format(service[-1][3]))
        self.service_statics[4].insert(tk.END, '{0:.3f}'.format(service[-1][4]))

        self.service_statics[0].insert(tk.END, service[-2][0])
        self.service_statics[1].insert(tk.END, '{0:.3f}'.format(service[-2][1]))
        self.service_statics[2].insert(tk.END, '{0:.3f}'.format(service[-2][2]))
        self.service_statics[3].insert(tk.END, '{0:.3f}'.format(service[-2][3]))
        self.service_statics[4].insert(tk.END, '{0:.3f}'.format(service[-2][4]))

        colors = ['cornflower blue','cornflower blue','yellow2']
        y=0
        for i in [9,8,7]:

            self.service_statics[0].itemconfigure(i, background=colors[y])
            self.service_statics[1].itemconfigure(i, background=colors[y])
            self.service_statics[2].itemconfigure(i, background=colors[y])
            self.service_statics[3].itemconfigure(i, background=colors[y])
            self.service_statics[4].itemconfigure(i, background=colors[y])

            self.ultimate_statics[0].itemconfigure(i, background=colors[y])
            self.ultimate_statics[1].itemconfigure(i, background=colors[y])
            self.ultimate_statics[2].itemconfigure(i, background=colors[y])
            self.ultimate_statics[3].itemconfigure(i, background=colors[y])
            self.ultimate_statics[4].itemconfigure(i, background=colors[y])

            y +=1

        self.service = service
        self.ultimate = ultimate

        self.simple_beam_loads()

    def simple_beam_loads(self):

        #Strap
        bs_in = float(self.bs.get())
        bs_ft = bs_in/12.0
        hs_in = float(self.hs.get())
        hs_ft = hs_in/12.0
        s_ext_ft = float(self.s_extension_in.get())/12.0

        #Left Foundation
        b1_ft = float(self.b1.get())
        d1_ft = float(self.d1.get())
        h1_ft = float(self.h1.get())/12.0
        e1_ft = float(self.ce1.get())/12.0

        cb1_ft = (float(self.cb1.get()))/12.0
        cd1_ft = (float(self.cd1.get()))/12.0

        #Right Foundation
        b2_ft = float(self.b2.get())
        d2_ft = float(self.d2.get())
        h2_ft = float(self.h2.get())/12.0
        e2_ft = float(self.ce2.get())/12.0

        cb2_ft = (float(self.cb2.get()))/12.0
        cd2_ft = (float(self.cd2.get()))/12.0

        p1s_kips = float(self.p1_service_kips.get())
        p1u_kips = float(self.p1_ultimate_kips.get())
        p2s_kips = float(self.p2_service_kips.get())
        p2u_kips = float(self.p2_ultimate_kips.get())

        p1u_klf = p1u_kips/cb1_ft
        p2u_klf = p2u_kips/cb2_ft
        p1s_klf = p1s_kips/cb1_ft
        p2s_klf = p2s_kips/cb2_ft

        lcc_ft = float(self.lcc.get())

        ls_ft = lcc_ft - (b1_ft/2.0) - ((b1_ft/2.0)-e1_ft) - (b2_ft/2.0) - e2_ft

        self.ll = e1_ft
        self.lc = lcc_ft
        self.lr = (b2_ft/2.0) - e2_ft

        self.loads_s_l = []
        self.loads_s_c = []
        self.loads_s_r = []

        self.loads_u_l = []
        self.loads_u_c = []
        self.loads_u_r = []

        self.loads_scale = []

        self.extra_l_station = [0]
        self.extra_c_station = [0]
        self.extra_r_station = [0]

        #Loads on the Left Cantilever - ftg1 sw , strap on ftg1 sw, and ftg1 pressure
        w_s_ftg1 = self.service[1][1] / b1_ft
        w_u_ftg1 = self.ultimate[1][1] / b1_ft

        self.loads_scale.append(w_s_ftg1)

        self.loads_s_l.append(ppbeam.cant_left_udl(w_s_ftg1,0,self.ll,self.ll,self.lc))
        self.loads_u_l.append(ppbeam.cant_left_udl(w_u_ftg1,0,self.ll,self.ll,self.lc))

        w_s_softg1 = self.service[2][1] / b1_ft
        w_u_softg1 = self.ultimate[2][1] / b1_ft

        self.loads_scale.append(w_s_softg1)

        self.loads_s_l.append(ppbeam.cant_left_udl(w_s_softg1,0,self.ll,self.ll,self.lc))
        self.loads_u_l.append(ppbeam.cant_left_udl(w_u_softg1,0,self.ll,self.ll,self.lc))

        w_s_qftg1 = (self.service[-2][1] / b1_ft) * -1.0
        w_u_qftg1 = (self.ultimate[-2][1] / b1_ft) * -1.0

        self.loads_scale.append(w_s_qftg1)

        self.loads_s_l.append(ppbeam.cant_left_udl(w_s_qftg1,0,self.ll,self.ll,self.lc))
        self.loads_u_l.append(ppbeam.cant_left_udl(w_u_qftg1,0,self.ll,self.ll,self.lc))

        #column 1
        self.loads_u_l.append(ppbeam.cant_left_udl(p1u_klf,(e1_ft - (cb1_ft/2.0)),self.ll,self.ll,self.lc))
        self.loads_s_l.append(ppbeam.cant_left_udl(p1s_klf,(e1_ft - (cb1_ft/2.0)),self.ll,self.ll,self.lc))

        self.extra_l_station.append((e1_ft - (cb1_ft/2.0)))

        #Loads on the Right Cantilever - ftg2 sw, 3" + C2,b /2.0 of strap beam on ftg2, and ftg2 pressure
        w_s_ftg2 = self.service[5][1] / b2_ft
        w_u_ftg2 = self.ultimate[5][1] / b2_ft

        self.loads_scale.append(w_s_ftg2)

        self.loads_s_r.append(ppbeam.cant_right_udl(w_s_ftg2,0,self.lr,self.lr,self.lc))
        self.loads_u_r.append(ppbeam.cant_right_udl(w_u_ftg2,0,self.lr,self.lr,self.lc))

        w_s_softg2 = self.service[4][1] / ((b2_ft/2.0) + e2_ft + (cb2_ft/2.0) + s_ext_ft)
        w_u_softg2 = self.ultimate[4][1] / ((b2_ft/2.0) + e2_ft + (cb2_ft/2.0) + s_ext_ft)
        b_r_s = (cb2_ft/2.0) + (s_ext_ft)

        if b_r_s > self.lr:
            b_r_s = self.lr
        else:
            b_r_s = b_r_s

        self.loads_scale.append(w_s_softg2)
        self.extra_r_station.append(b_r_s)

        self.loads_s_r.append(ppbeam.cant_right_udl(w_s_softg2,0,b_r_s,self.lr,self.lc))
        self.loads_u_r.append(ppbeam.cant_right_udl(w_u_softg2,0,b_r_s,self.lr,self.lc))

        w_s_qftg2 = (self.service[-1][1] / b2_ft) * -1.0
        w_u_qftg2 = (self.ultimate[-1][1] / b2_ft) * -1.0

        self.loads_scale.append(w_s_qftg2)

        self.loads_s_r.append(ppbeam.cant_right_udl(w_s_qftg2,0,self.lr,self.lr,self.lc))
        self.loads_u_r.append(ppbeam.cant_right_udl(w_u_qftg2,0,self.lr,self.lr,self.lc))

        #column 2
        ac2 = (cb2_ft/2.0)
        if ac2 > self.lr:
            ac2 = self.lr
        else:
            ac2 = ac2
        self.loads_u_r.append(ppbeam.cant_right_udl(p2u_klf,0,ac2,self.lr,self.lc))
        self.loads_s_r.append(ppbeam.cant_right_udl(p2s_klf,0,ac2,self.lr,self.lc))
        self.extra_r_station.append((cb2_ft/2.0))
        #Loads on Center Span
        a_ftg1 = 0
        b_ftg1 = b1_ft - e1_ft
        self.extra_c_station.append(b_ftg1)

        #ftg1
        self.loads_s_c.append(ppbeam.udl(w_s_ftg1,0,b_ftg1,self.lc))
        self.loads_u_c.append(ppbeam.udl(w_u_ftg1,0,b_ftg1,self.lc))

        #strap on ftg1
        self.loads_s_c.append(ppbeam.udl(w_s_softg1,0,b_ftg1,self.lc))
        self.loads_u_c.append(ppbeam.udl(w_u_softg1,0,b_ftg1,self.lc))

        #ftg1 - Q and Qu
        self.loads_s_c.append(ppbeam.udl(w_s_qftg1,0,b_ftg1,self.lc))
        self.loads_u_c.append(ppbeam.udl(w_u_qftg1,0,b_ftg1,self.lc))


        #strap between footings
        a_strap = b_ftg1
        b_strap = a_strap + ls_ft

        self.extra_c_station.append(b_strap)

        w_s_strap = self.service[3][1] / ls_ft
        w_u_strap = self.ultimate[3][1] / ls_ft

        self.loads_scale.append(w_s_strap)

        self.loads_s_c.append(ppbeam.udl(w_s_strap,a_strap,b_strap,self.lc))
        self.loads_u_c.append(ppbeam.udl(w_u_strap,a_strap,b_strap,self.lc))

        #ftg2
        self.loads_s_c.append(ppbeam.udl(w_s_ftg2,b_strap,self.lc,self.lc))
        self.loads_u_c.append(ppbeam.udl(w_u_ftg2,b_strap,self.lc,self.lc))

        #strap on ftg2
        self.loads_s_c.append(ppbeam.udl(w_s_softg2,b_strap,self.lc,self.lc))
        self.loads_u_c.append(ppbeam.udl(w_u_softg2,b_strap,self.lc,self.lc))

        #ftg2 - Q and Qu
        self.loads_s_c.append(ppbeam.udl(w_s_qftg2,b_strap,self.lc,self.lc))
        self.loads_u_c.append(ppbeam.udl(w_u_qftg2,b_strap,self.lc,self.lc))

        #column 1
        self.loads_u_c.append(ppbeam.udl(p1u_klf,0,cb1_ft/2.0,self.lc))
        self.loads_s_c.append(ppbeam.udl(p1s_klf,0,cb1_ft/2.0,self.lc))
        #column 2
        self.loads_u_c.append(ppbeam.udl(p2u_klf,(self.lc - (cb2_ft/2.0)),self.lc,self.lc))
        self.loads_s_c.append(ppbeam.udl(p2s_klf,(self.lc - (cb2_ft/2.0)),self.lc,self.lc))
        self.extra_c_station.append(cb1_ft/2.0)
        self.extra_c_station.append((self.lc - (cb2_ft/2.0)))

        self.simple_beam_service_analysis()

    def simple_beam_service_analysis(self):
            iters = 100

            step_left = self.ll/(iters+0.00)
            step_backspan = self.lc/(iters+0.00)
            step_right = self.lr/(iters+0.00)

            xsl = zeros(iters+1)
            xsc = zeros(iters+1)
            xsr = zeros(iters+1)

            reaction_left = 0
            reaction_right = 0

            xsl[0]=0
            xsc[0]=0
            xsr[0]=0

            for i in range(1,(iters+1)):
                if xsl[i-1] + step_left > self.ll:
                    xsl[i] = self.ll
                else:
                    xsl[i] = xsl[i-1] + step_left

                if xsc[i-1] + step_backspan > self.lc:
                    xsc[i] = self.lc
                else:
                    xsc[i] = xsc[i-1] + step_backspan

                if xsr[i-1] + step_right > self.lr:
                    xsr[i] = self.lr
                else:
                    xsr[i] = xsr[i-1] + step_right


            xsl = np.append(xsl, self.extra_l_station)
            xsc = np.append(xsc, self.extra_c_station)
            xsr = np.append(xsr, self.extra_r_station)

            xsl = np.sort(xsl)
            xsc = np.sort(xsc)
            xsr = np.sort(xsr)

            xsl = np.unique(xsl)
            xsc = np.unique(xsc)
            xsr = np.unique(xsr)

            i = max(xsl.shape[0], xsc.shape[0], xsr.shape[0])

            if xsl.shape[0] < i :
                a = i - xsl.shape[0]
                for x in range(0,a):
                    xsl = np.append(xsl, self.ll)
            else:
                pass
            if xsc.shape[0] < i :
                a = i - xsc.shape[0]
                for x in range(0,a):
                    xsc = np.append(xsc, self.lc)
            else:
                pass
            if xsr.shape[0] < i :
                a = i - xsr.shape[0]
                for x in range(0,a):
                    xsr = np.append(xsr, self.lr)
            else:
                pass

            shearl = zeros(i)
            shearc = zeros(i)
            shearr = zeros(i)

            momentl = zeros(i)
            momentc = zeros(i)
            momentr = zeros(i)

            for load in self.loads_s_l:
                reaction_left = reaction_left + load.rr + load.backspan.rl
                reaction_right = reaction_right + load.backspan.rr

                shearl = shearl + load.v(xsl)
                shearc = shearc + load.backspan.v(xsc)

                momentl = momentl + load.m(xsl)
                momentc = momentc + load.backspan.m(xsc)


            for load in self.loads_s_c:
                reaction_left = reaction_left + load.rl
                reaction_right = reaction_right  + load.rr

                shearc = shearc + load.v(xsc)

                momentc = momentc + load.m(xsc)


            for load in self.loads_s_r:
                reaction_left = reaction_left + load.backspan.rl
                reaction_right = reaction_right + load.backspan.rr + load.rl

                shearc = shearc + load.backspan.v(xsc)
                shearr = shearr + load.v(xsr)

                momentc = momentc + load.backspan.m(xsc)
                momentr = momentr + load.m(xsr)


            self.shearl_s = shearl
            self.shearc_s = shearc
            self.shearr_s = shearr

            self.momentl_s = momentl
            self.momentc_s = momentc
            self.momentr_s = momentr

            self.reaction_left_s = reaction_left
            self.reaction_right_s = reaction_right

            self.xsl = xsl
            self.xsc = xsc + xsl[-1]
            self.xsr = xsr + self.xsc[-1]

            self.draw_fbd()

            self.simple_beam_ultimate_analysis()

    def simple_beam_ultimate_analysis(self):
        iters = 100

        step_left = self.ll/(iters+0.00)
        step_backspan = self.lc/(iters+0.00)
        step_right = self.lr/(iters+0.00)

        xsl = zeros(iters+1)
        xsc = zeros(iters+1)
        xsr = zeros(iters+1)

        reaction_left = 0
        reaction_right = 0

        xsl[0]=0
        xsc[0]=0
        xsr[0]=0

        for i in range(1,(iters+1)):
            if xsl[i-1] + step_left > self.ll:
                xsl[i] = self.ll
            else:
                xsl[i] = xsl[i-1] + step_left

            if xsc[i-1] + step_backspan > self.lc:
                xsc[i] = self.lc
            else:
                xsc[i] = xsc[i-1] + step_backspan

            if xsr[i-1] + step_right > self.lr:
                xsr[i] = self.lr
            else:
                xsr[i] = xsr[i-1] + step_right


        xsl = np.append(xsl, self.extra_l_station)
        xsc = np.append(xsc, self.extra_c_station)
        xsr = np.append(xsr, self.extra_r_station)

        xsl = np.sort(xsl)
        xsc = np.sort(xsc)
        xsr = np.sort(xsr)

        xsl = np.unique(xsl)
        xsc = np.unique(xsc)
        xsr = np.unique(xsr)

        i = max(xsl.shape[0], xsc.shape[0], xsr.shape[0])

        if xsl.shape[0] < i :
            a = i - xsl.shape[0]
            for x in range(0,a):
                xsl = np.append(xsl, self.ll)
        else:
            pass
        if xsc.shape[0] < i :
            a = i - xsc.shape[0]
            for x in range(0,a):
                xsc = np.append(xsc, self.lc)
        else:
            pass
        if xsr.shape[0] < i :
            a = i - xsr.shape[0]
            for x in range(0,a):
                xsr = np.append(xsr, self.lr)
        else:
            pass

        shearl = zeros(i)
        shearc = zeros(i)
        shearr = zeros(i)

        momentl = zeros(i)
        momentc = zeros(i)
        momentr = zeros(i)

        for load in self.loads_u_l:
            reaction_left = reaction_left + load.rr + load.backspan.rl
            reaction_right = reaction_right + load.backspan.rr

            shearl = shearl + load.v(xsl)
            shearc = shearc + load.backspan.v(xsc)

            momentl = momentl + load.m(xsl)
            momentc = momentc + load.backspan.m(xsc)


        for load in self.loads_u_c:
            reaction_left = reaction_left + load.rl
            reaction_right = reaction_right  + load.rr

            shearc = shearc + load.v(xsc)

            momentc = momentc + load.m(xsc)


        for load in self.loads_u_r:
            reaction_left = reaction_left + load.backspan.rl
            reaction_right = reaction_right + load.backspan.rr + load.rl

            shearc = shearc + load.backspan.v(xsc)
            shearr = shearr + load.v(xsr)

            momentc = momentc + load.backspan.m(xsc)
            momentr = momentr + load.m(xsr)


        self.shearl_u = shearl
        self.shearc_u = shearc
        self.shearr_u = shearr

        self.momentl_u = momentl
        self.momentc_u = momentc
        self.momentr_u = momentr

        self.reaction_left_u = reaction_left
        self.reaction_right_u = reaction_right

        self.static_run = 1

        self.xl_listbox.delete(0,tk.END)
        self.lv_listbox.delete(0,tk.END)
        self.lm_listbox.delete(0,tk.END)

        self.xc_listbox.delete(0,tk.END)
        self.cv_listbox.delete(0,tk.END)
        self.cm_listbox.delete(0,tk.END)

        self.xr_listbox.delete(0,tk.END)
        self.rv_listbox.delete(0,tk.END)
        self.rm_listbox.delete(0,tk.END)


        #Left detailed results to GUI
        color = "pale green"
        i=0
        for x in xsl:
            self.xl_listbox.insert(tk.END,'{0:.4f}'.format(x))

            if i % 2 == 0:
                self.xl_listbox.itemconfigure(i, background=color)
            else:
                pass
            i+=1

        i=0
        for v in self.shearl_u:
            self.lv_listbox.insert(tk.END,'{0:.4f}'.format(v))

            if i % 2 == 0:
                self.lv_listbox.itemconfigure(i, background=color)
            else:
                pass
            i+=1

        i=0
        for m in self.momentl_u:
            self.lm_listbox.insert(tk.END,'{0:.4f}'.format(m))

            if i % 2 == 0:
                self.lm_listbox.itemconfigure(i, background=color)
            else:
                pass
            i+=1

        #Center/Main detailed results to GUI
        i=0
        for x in xsc:
            self.xc_listbox.insert(tk.END,'{0:.4f}'.format(x))

            if i % 2 == 0:
                self.xc_listbox.itemconfigure(i, background=color)
            else:
                pass
            i+=1

        i=0
        for v in self.shearc_u:
            self.cv_listbox.insert(tk.END,'{0:.4f}'.format(v))

            if i % 2 == 0:
                self.cv_listbox.itemconfigure(i, background=color)
            else:
                pass
            i+=1

        i=0
        for m in self.momentc_u:
            self.cm_listbox.insert(tk.END,'{0:.4f}'.format(m))

            if i % 2 == 0:
                self.cm_listbox.itemconfigure(i, background=color)
            else:
                pass
            i+=1

        #Right detailed results to GUI
        i=0
        for x in xsr:
            self.xr_listbox.insert(tk.END,'{0:.4f}'.format(x))

            if i % 2 == 0:
                self.xr_listbox.itemconfigure(i, background=color)
            else:
                pass
            i+=1

        i=0
        for v in self.shearr_u:
            self.rv_listbox.insert(tk.END,'{0:.4f}'.format(v))

            if i % 2 == 0:
                self.rv_listbox.itemconfigure(i, background=color)
            else:
                pass
            i+=1

        i=0
        for m in self.momentr_u:
            self.rm_listbox.insert(tk.END,'{0:.4f}'.format(m))

            if i % 2 == 0:
                self.rm_listbox.itemconfigure(i, background=color)
            else:
                pass
            i+=1

        self.ult_results_out_text = '\n\n{0:-^85}\n{1:-^85}\n{2:-^85}\n'.format('-',' Ultimate Results at Select Stations ','-')
        self.ult_results_out_text = self.ult_results_out_text+'\n\n{0:-^85}\n'.format('  Left Edge of Left Footing to Center of left Column  ')
        self.ult_results_out_text = self.ult_results_out_text+'{0:^14}{1:^14}{2:^14}\n'.format('X (ft)','Vu (kips)','Mu (ft-kips)')
        self.ult_results_out_text = self.ult_results_out_text+'{0:_^42}\n'.format('_')
        i=0
        for i in range(0, len(xsl)):
            self.ult_results_out_text = self.ult_results_out_text+'{0:^14.3f}{1:^14.3f}{2:^14.3f}\n'.format(xsl[i],shearl[i],momentl[i])
        self.ult_results_out_text = self.ult_results_out_text+'\n\n{0:-^85}\n'.format('  Center of left Column to Center of Right Column ')
        self.ult_results_out_text = self.ult_results_out_text+'{0:^14}{1:^14}{2:^14}\n'.format('X (ft)','Vu (kips)','Mu (ft-kips)')
        self.ult_results_out_text = self.ult_results_out_text+'{0:_^42}\n'.format('_')
        i=0
        for i in range(0, len(xsc)):
            self.ult_results_out_text = self.ult_results_out_text+'{0:^14.3f}{1:^14.3f}{2:^14.3f}\n'.format(xsc[i],shearc[i],momentc[i])

        self.ult_results_out_text = self.ult_results_out_text+'\n\n{0:-^85}\n'.format('  Center of Right Column to Right Edge of Right Footing')
        self.ult_results_out_text = self.ult_results_out_text+'{0:^14}{1:^14}{2:^14}\n'.format('X (ft)','Vu (kips)','Mu (ft-kips)')
        self.ult_results_out_text = self.ult_results_out_text+'{0:_^42}\n'.format('_')
        i=0
        for i in range(0, len(xsr)):
            self.ult_results_out_text = self.ult_results_out_text+'{0:^14.3f}{1:^14.3f}{2:^14.3f}\n'.format(xsr[i],shearr[i],momentr[i])


        self.xsl = xsl
        self.xsc = xsc + xsl[-1]
        self.xsr = xsr + self.xsc[-1]

        self.draw_static_beam()
        self.ftg_design()

    def simple_beam_ultimate_analysisx(self,x):

        reaction_left = 0
        reaction_right = 0

        shearl = 0
        shearc = 0
        shearr = 0

        momentl = 0
        momentc = 0
        momentr = 0

        for load in self.loads_u_l:
            reaction_left = reaction_left + load.rr + load.backspan.rl
            reaction_right = reaction_right + load.backspan.rr

            shearl = shearl + load.vx(x)
            shearc = shearc + load.backspan.vx(x)

            momentl = momentl + load.mx(x)
            momentc = momentc + load.backspan.mx(x)


        for load in self.loads_u_c:
            reaction_left = reaction_left + load.rl
            reaction_right = reaction_right  + load.rr

            shearc = shearc + load.vx(x)

            momentc = momentc + load.mx(x)


        for load in self.loads_u_r:
            reaction_left = reaction_left + load.backspan.rl
            reaction_right = reaction_right + load.backspan.rr + load.rl

            shearc = shearc + load.backspan.vx(x)
            shearr = shearr + load.vx(x)

            momentc = momentc + load.backspan.mx(x)
            momentr = momentr + load.mx(x)

        v = [shearl, shearc, shearr]
        m = [momentl, momentc, momentr]

        return v,m

    def draw_static_beam(self, *event):
        self.g_beam_canvas.delete("all")

        w = self.g_beam_canvas.winfo_width()
        h = self.g_beam_canvas.winfo_height()
        hg = (h/2.0)

        ll = self.ll
        lc = self.lc
        lr = self.lr

        initial = 25

        sf = (w-(2*initial)) / (ll+lc+lr)

        self.static_beam_x_sf = sf

        l = (w-(2*initial)) + initial
        s1 = (sf * ll) + initial
        s2 = ((ll+lc) * sf) + initial

        self.g_beam_canvas.create_line(initial, h/2, l, h/2, fill="black", width=2)

        xl = self.xsl
        xc = self.xsc
        xr = self.xsr
        
        if self.show_m_tension.get() == 1:
            factor = -1.0
        else:
            factor = 1.0

        if self.static_run == 1:
            section_string = ['P1','Face of FTG_L', 'Face of FTG_R','P2']
            row_ftgl = np.where(xc == (self.extra_c_station[1]+xl[-1]))
            row_ftg2 = np.where(xc == (self.extra_c_station[2]+xl[-1]))
            reporting = [0,row_ftgl[0][0], row_ftg2[0][0], xc[-1]]

            i = 0
            for station in self.extra_c_station:

                if i == 0:
                    self.g_beam_canvas.create_text((((station+ll) * sf) + initial), 24, justify=tk.CENTER, text= section_string[i]+'\nRls:{0:.2f} kips\nRlu:{1:.2f} kips'.format(self.reaction_left_s,self.reaction_left_u))
                    self.g_beam_canvas.create_line(((station+ll) * sf) + initial, 0,((station+ll) * sf) + initial,h,fill="gray90", width=1, dash=(4,4))
                elif i < 3:
                    ms = self.momentc_s[reporting[i]]
                    mu = self.momentc_u[reporting[i]]

                    self.g_beam_canvas.create_text((((station+ll) * sf) + initial), 24, justify=tk.CENTER, text= section_string[i]+'\nMs:{0:.2f} ft-kips\nMu:{1:.2f} ft-kips'.format(ms,mu))
                    self.g_beam_canvas.create_line(((station+ll) * sf) + initial, 0,((station+ll) * sf) + initial,h,fill="gray90", width=1, dash=(4,4))
                else:
                    pass
                i+=1

            self.g_beam_canvas.create_line(s2, 0,s2,h,fill="gray90", width=1, dash=(4,4))
            self.g_beam_canvas.create_text(s2, 24, justify=tk.CENTER, text= section_string[-1]+'\nRrs:{0:.2f} kips\nRru:{1:.2f} kips'.format(self.reaction_right_s,self.reaction_right_u))
        else:
            pass

        if self.show_vs.get() == 1 and self.show_vu.get() == 0:
            if max(max(max(self.shearc_s), max(self.shearl_s), max(self.shearr_s)), abs(min(min(self.shearc_s), min(self.shearl_s), min(self.shearr_s)))) == 0:
                v_sf = (hg - 10)
            else:
                v_sf = (hg - 10) / max(max(max(self.shearc_s), max(self.shearl_s), max(self.shearr_s)), abs(min(min(self.shearc_s), min(self.shearl_s), min(self.shearr_s))))

            self.g_beam_canvas.create_line((xl[-1] * sf) + initial, hg - (self.shearl_s[-1] * v_sf),(xc[0] * sf) + initial,hg - (self.shearc_s[0] * v_sf),fill="red", width=2)
            self.g_beam_canvas.create_line((xc[-1] * sf) + initial, hg - (self.shearc_s[-1] * v_sf),(xr[0] * sf) + initial,hg - (self.shearr_s[0] * v_sf),fill="red", width=2)

            for i in range(1,len(self.shearc_s)):
                self.g_beam_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.shearl_s[i-1] * v_sf),(xl[i] * sf) + initial,hg - (self.shearl_s[i] * v_sf),fill="red", width=2)
                self.g_beam_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.shearc_s[i-1] * v_sf),(xc[i] * sf) + initial,hg - (self.shearc_s[i] * v_sf),fill="red", width=2)
                self.g_beam_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.shearr_s[i-1] * v_sf),(xr[i] * sf) + initial,hg - (self.shearr_s[i] * v_sf),fill="red", width=2)
        else:
            pass

        if self.show_ms.get() == 1 and self.show_mu.get() == 0:
            if max(max(max(self.momentc_s*factor),max(self.momentl_s*factor),max(self.momentr_s*factor)), abs(min(min(self.momentc_s*factor),min(self.momentl_s*factor),min(self.momentr_s*factor)))) == 0:
                m_sf = (hg - 10)
            else:
                m_sf = (hg - 10) / max(max(max(self.momentc_s*factor),max(self.momentl_s*factor),max(self.momentr_s*factor)), abs(min(min(self.momentc_s*factor),min(self.momentl_s*factor),min(self.momentr_s*factor))))

            for i in range(1,len(self.momentc_s)):
                self.g_beam_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.momentl_s[i-1]*factor * m_sf),(xl[i] * sf) + initial,hg - (self.momentl_s[i]*factor * m_sf),fill="green", width=2)
                self.g_beam_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.momentc_s[i-1]*factor * m_sf),(xc[i] * sf) + initial,hg - (self.momentc_s[i]*factor * m_sf),fill="green", width=2)
                self.g_beam_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.momentr_s[i-1]*factor * m_sf),(xr[i] * sf) + initial,hg - (self.momentr_s[i]*factor * m_sf),fill="green", width=2)
        else:
            pass

        if self.show_vu.get() == 1:
            if max(max(max(self.shearc_u), max(self.shearl_u), max(self.shearr_u)), abs(min(min(self.shearc_u), min(self.shearl_u), min(self.shearr_u)))) == 0:
                v_uf = (hg - 10)
            else:
                v_uf = (hg - 10) / max(max(max(self.shearc_u), max(self.shearl_u), max(self.shearr_u)), abs(min(min(self.shearc_u), min(self.shearl_u), min(self.shearr_u))))

            self.g_beam_canvas.create_line((xl[-1] * sf) + initial, hg - (self.shearl_u[-1] * v_uf),(xc[0] * sf) + initial,hg - (self.shearc_u[0] * v_uf),fill="maroon", width=2)
            self.g_beam_canvas.create_line((xc[-1] * sf) + initial, hg - (self.shearc_u[-1] * v_uf),(xr[0] * sf) + initial,hg - (self.shearr_u[0] * v_uf),fill="maroon", width=2)

            for i in range(1,len(self.shearc_u)):
                self.g_beam_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.shearl_u[i-1] * v_uf),(xl[i] * sf) + initial,hg - (self.shearl_u[i] * v_uf),fill="maroon", width=2)
                self.g_beam_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.shearc_u[i-1] * v_uf),(xc[i] * sf) + initial,hg - (self.shearc_u[i] * v_uf),fill="maroon", width=2)
                self.g_beam_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.shearr_u[i-1] * v_uf),(xr[i] * sf) + initial,hg - (self.shearr_u[i] * v_uf),fill="maroon", width=2)

                self.g_beam_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.shearl_u[i-1] * v_uf),(xl[i-1] * sf) + initial,hg,fill="violet red", width=1)
                self.g_beam_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.shearc_u[i-1] * v_uf),(xc[i-1] * sf) + initial,hg,fill="violet red", width=1)
                self.g_beam_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.shearr_u[i-1] * v_uf),(xr[i-1] * sf) + initial,hg,fill="violet red", width=1)

            if self.show_vs.get() == 1:
                self.g_beam_canvas.create_line((xl[-1] * sf) + initial, hg - (self.shearl_s[-1] * v_uf),(xc[0] * sf) + initial,hg - (self.shearc_s[0] * v_uf),fill="red", width=2)
                self.g_beam_canvas.create_line((xc[-1] * sf) + initial, hg - (self.shearc_s[-1] * v_uf),(xr[0] * sf) + initial,hg - (self.shearr_s[0] * v_uf),fill="red", width=2)

                for i in range(1,len(self.shearc_s)):
                    self.g_beam_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.shearl_s[i-1] * v_uf),(xl[i] * sf) + initial,hg - (self.shearl_s[i] * v_uf),fill="red", width=2)
                    self.g_beam_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.shearc_s[i-1] * v_uf),(xc[i] * sf) + initial,hg - (self.shearc_s[i] * v_uf),fill="red", width=2)
                    self.g_beam_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.shearr_s[i-1] * v_uf),(xr[i] * sf) + initial,hg - (self.shearr_s[i] * v_uf),fill="red", width=2)
            else:
                pass
        else:
            pass

        if self.show_mu.get() == 1:
            if max(max(max(self.momentc_u*factor),max(self.momentl_u*factor),max(self.momentr_u*factor)), abs(min(min(self.momentc_u*factor),min(self.momentl_u*factor),min(self.momentr_u*factor)))) == 0:
                m_uf = (hg - 10)
            else:
                m_uf = (hg - 10) / max(max(max(self.momentc_u*factor),max(self.momentl_u*factor),max(self.momentr_u*factor)), abs(min(min(self.momentc_u*factor),min(self.momentl_u*factor),min(self.momentr_u*factor))))

            for i in range(1,len(self.momentc_u)):
                self.g_beam_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.momentl_u[i-1]*factor * m_uf),(xl[i] * sf) + initial,hg - (self.momentl_u[i]*factor * m_uf),fill="dark green", width=2)
                self.g_beam_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.momentc_u[i-1]*factor * m_uf),(xc[i] * sf) + initial,hg - (self.momentc_u[i]*factor * m_uf),fill="dark green", width=2)
                self.g_beam_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.momentr_u[i-1]*factor * m_uf),(xr[i] * sf) + initial,hg - (self.momentr_u[i]*factor * m_uf),fill="dark green", width=2)

                self.g_beam_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.momentl_u[i-1]*factor * m_uf),(xl[i-1] * sf) + initial,hg,fill="green4", width=1)
                self.g_beam_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.momentc_u[i-1]*factor * m_uf),(xc[i-1] * sf) + initial,hg,fill="green4", width=1)
                self.g_beam_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.momentr_u[i-1]*factor * m_uf),(xr[i-1] * sf) + initial,hg,fill="green4", width=1)

            if self.show_ms.get() == 1:
                for i in range(1,len(self.momentc_s)):
                    self.g_beam_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.momentl_s[i-1]*factor * m_uf),(xl[i] * sf) + initial,hg - (self.momentl_s[i]*factor * m_uf),fill="green", width=2)
                    self.g_beam_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.momentc_s[i-1]*factor * m_uf),(xc[i] * sf) + initial,hg - (self.momentc_s[i]*factor * m_uf),fill="green", width=2)
                    self.g_beam_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.momentr_s[i-1]*factor * m_uf),(xr[i] * sf) + initial,hg - (self.momentr_s[i]*factor * m_uf),fill="green", width=2)
            else:
                pass
        else:
            pass

    def draw_static_beam_mouse(self, event, *args):
        w = self.g_beam_canvas.winfo_width()
        h = self.g_beam_canvas.winfo_height()

        if self.static_run == 1:
            self.g_beam_canvas.delete(self.val_at_x)
            self.g_beam_canvas.delete(self.val_at_x_text)
            initial = 25

            sf = self.static_beam_x_sf

            ll = self.ll
            lc = self.lc
            lr = self.lr

            x_screen = event.x
            x = x_screen - initial

            if x > (ll*sf) and x < ((ll+lc) * sf):
                x_anal = (x/sf) - ll

                v,m = self.simple_beam_ultimate_analysisx(x_anal)

                self.val_at_x_text = self.g_beam_canvas.create_text(w/2.0, (h-26), justify=tk.CENTER, text= '@ Xc = {0:.2f} ft\nVu:{1:.2f} kips\nMu:{2:.2f} ft-kips'.format(x_anal,v[1],m[1]))
            elif x > ((ll+lc)*sf):
                x_anal = (x/sf) - (ll+lc)

                if x_anal > lr:
                    pass
                else:
                    v,m = self.simple_beam_ultimate_analysisx(x_anal)

                    self.val_at_x_text = self.g_beam_canvas.create_text(w/2.0, (h-26), justify=tk.CENTER, text= '@ Xr = {0:.2f} ft\nVu:{1:.2f} kips\nMu:{2:.2f} ft-kips'.format(x_anal,v[2],m[2]))
            else:
                x_anal = x/sf
                if x_anal < 0:
                    pass
                else:
                    v,m = self.simple_beam_ultimate_analysisx(x_anal)

                    self.val_at_x_text = self.g_beam_canvas.create_text(w/2.0, (h-26), justify=tk.CENTER, text= '@ Xl = {0:.2f} ft\nVu:{1:.2f} kips\nMu:{2:.2f} ft-kips'.format(x_anal,v[0],m[0]))

            self.val_at_x = self.g_beam_canvas.create_line(x_screen, 0,x_screen,h,fill="blue", width=1, dash=(6,6))


        else:
            pass

    def draw_fbd(self,*event):
        self.g_fbd_canvas.delete("all")

        #Strap
        bs_in = float(self.bs.get())
        bs_ft = bs_in/12.0
        hs_in = float(self.hs.get())
        hs_ft = hs_in/12.0
        s_ext_ft = float(self.s_extension_in.get())/12.0

        #Left Foundation
        b1_ft = float(self.b1.get())
        d1_ft = float(self.d1.get())
        h1_ft = float(self.h1.get())/12.0
        e1_ft = float(self.ce1.get())/12.0

        cb1_ft = (float(self.cb1.get()))/12.0
        cd1_ft = (float(self.cd1.get()))/12.0

        #Right Foundation
        b2_ft = float(self.b2.get())
        d2_ft = float(self.d2.get())
        h2_ft = float(self.h2.get())/12.0
        e2_ft = float(self.ce2.get())/12.0

        cb2_ft = (float(self.cb2.get()))/12.0
        cd2_ft = (float(self.cd2.get()))/12.0

        lcc_ft = float(self.lcc.get())

        ls_ft = lcc_ft - (b1_ft/2.0) - ((b1_ft/2.0)-e1_ft) - (b2_ft/2.0) - e2_ft

        w = self.g_fbd_canvas.winfo_width()
        h = self.g_fbd_canvas.winfo_height()
        hg = (h/2.0)

        ll = self.ll
        lc = self.lc
        lr = self.lr

        initial = 25

        sf = (w-(2*initial)) / (ll+lc+lr)

        l = (w-(2*initial)) + initial
        s1 = (sf * ll) + initial
        s2 = ((ll+lc) * sf) + initial

        self.g_fbd_canvas.create_line(initial, h/2, l, h/2, fill="black", width=2)

        #ftg1 - sw
        fx1 = initial
        fy1 = h/2.0
        fx2 = fx1
        fy2 = (h/2.0) - 30
        fx3 = fx2 + (b1_ft * sf)
        fy3 = fy2
        fx4 = fx3
        fy4 = fy1
        self.g_fbd_canvas.create_line(fx1,fy1,fx2,fy2,fx3,fy3,fx4,fy4, fill="blue", width=2, arrow=tk.BOTH)

        #ftg1 - strap
        fsx1 = fx1
        fsy1 = fy2
        fsx2 = fsx1
        fsy2 = fsy1 - 15
        fsx3 = fsx2 + (b1_ft * sf)
        fsy3 = fsy2
        fsx4 = fsx3
        fsy4 = fsy1
        self.g_fbd_canvas.create_line(fsx1,fsy1,fsx2,fsy2,fsx3,fsy3,fsx4,fsy4, fill="red", width=2, arrow=tk.BOTH)

        #ftg1 - q
        fqx1 = fx1
        fqy1 = fy1
        fqx2 = fqx1
        fqy2 = fqy1 + 50
        fqx3 = fqx2 + (b1_ft * sf)
        fqy3 = fqy2
        fqx4 = fqx3
        fqy4 = fqy1
        self.g_fbd_canvas.create_line(fqx1,fqy1,fqx2,fqy2,fqx3,fqy3,fqx4,fqy4, fill="sienna4", width=2, arrow=tk.BOTH)

        #p1
        px1 = fx1 + (e1_ft * sf) - ((cb1_ft/2.0) * sf)
        py1 = fsy2
        px2 = px1
        py2 = py1 - 60
        px3 = px1 + (cb1_ft*sf)
        py3 = py2
        px4 = px3
        py4 = fsy2
        self.g_fbd_canvas.create_line(px1,py1,px2,py2,px3,py3,px4,py4, fill="black", width=2, arrow=tk.BOTH)

        #strap
        sx1 = fx3
        sy1 = fsy1
        sx2 = sx1
        sy2 = sy1 - 30
        sx3 = sx2 + (ls_ft * sf)
        sy3 = sy2
        sx4 = sx3
        sy4 = sy1
        self.g_fbd_canvas.create_line(sx1,sy1,sx2,sy2,sx3,sy3,sx4,sy4, fill="red", width=2, arrow=tk.BOTH)

        #ftg2 - sw
        f2x1 = sx3
        f2y1 = fy1
        f2x2 = f2x1
        f2y2 = f2y1 - 30
        f2x3 = f2x2 + (b2_ft * sf)
        f2y3 = f2y2
        f2x4 = f2x3
        f2y4 = f2y1
        self.g_fbd_canvas.create_line(f2x1,f2y1,f2x2,f2y2,f2x3,f2y3,f2x4,f2y4, fill="blue", width=2, arrow=tk.BOTH)

        #ftg2 - q
        f2qx1 = sx3
        f2qy1 = fy1
        f2qx2 = f2qx1
        f2qy2 = f2qy1 + 40
        f2qx3 = f2qx2 + (b2_ft * sf)
        f2qy3 = f2qy2
        f2qx4 = f2qx3
        f2qy4 = f2qy1
        self.g_fbd_canvas.create_line(f2qx1,f2qy1,f2qx2,f2qy2,f2qx3,f2qy3,f2qx4,f2qy4, fill="sienna4", width=2, arrow=tk.BOTH)

        #ftg2 strap
        f2sx1 = f2x1
        f2sy1 = f2y2
        f2sx2 = f2sx1
        f2sy2 = f2sy1 - 15
        f2sx3 = f2sx2 + (((b2_ft * 0.5) + e2_ft + (cb2_ft*0.5) + s_ext_ft) * sf)
        f2sy3 = f2sy2
        f2sx4 = f2sx3
        f2sy4 = f2sy1
        self.g_fbd_canvas.create_line(f2sx1,f2sy1,f2sx2,f2sy2,f2sx3,f2sy3,f2sx4,f2sy4, fill="red", width=2, arrow=tk.BOTH)

        #p2
        p2x1 = f2sx2 + (((b2_ft * 0.5) + e2_ft - (cb2_ft/2.0)) * sf)
        p2y1 = f2sy2
        p2x2 = p2x1
        p2y2 = p2y1 - 60
        p2x3 = p2x1 + (cb2_ft*sf)
        p2y3 = p2y2
        p2x4 = p2x3
        p2y4 = p2y1
        self.g_fbd_canvas.create_line(p2x1,p2y1,p2x2,p2y2,p2x3,p2y3,p2x4,p2y4, fill="black", width=2, arrow=tk.BOTH)

    def ftg_design(self):
        self.left_ftg_calc_txtbox.delete(1.0,tk.END)
        self.right_ftg_calc_txtbox.delete(1.0,tk.END)

        self.ftg1_text = '\n{1:-^85}\n-- {0:-<82}\n{2:-^85}\n'.format('Left Foundation Calculations: ','-','-')
        self.ftg2_text = '\n{1:-^85}\n-- {0:-<82}\n{2:-^85}\n'.format('Right Foundation Calculations: ','-','-')

        #Common data items
        sw_pcf = float(self.density_pcf.get())
        qa_ksf = float(self.Qa_ksf.get())
        fpc_ksi = float(self.Fpc_ksi.get())
        fpc_psi = fpc_ksi * 1000.0
        dl_factor = float(self.dl_factor.get())
        fy_ksi = float(self.Fy_ksi.get())
        fy_psi = fy_ksi * 1000.0

        if fpc_psi <= 4000:
            beta1 = 0.85
        elif fpc_psi <= 8000:
            beta1 = 0.85 - ((0.05*(fpc_psi-4000))/1000)
        else:
            beta1 = 0.65


        #Strap
        bs_in = float(self.bs.get())
        bs_ft = bs_in/12.0

        #Left Foundation
        b1_ft = float(self.b1.get())
        b1_in = b1_ft * 12.0
        d1_ft = float(self.d1.get())
        d1ftg_in = d1_ft * 12.0
        h1_ft = float(self.h1.get())/12.0
        h1_in = h1_ft * 12.0
        e1_ft = float(self.ce1.get())/12.0
        e1_in = e1_ft * 12.0

        cb1_ft = (float(self.cb1.get()))/12.0
        cd1_ft = (float(self.cd1.get()))/12.0

        #Right Foundation
        b2_ft = float(self.b2.get())
        b2_in = b2_ft * 12.0
        d2_ft = float(self.d2.get())
        d2ftg_in = d2_ft * 12.0
        h2_ft = float(self.h2.get())/12.0
        h2_in = h2_ft * 12.0
        e2_ft = float(self.ce2.get())/12.0
        e2_in = e2_ft * 12.0

        cb2_ft = (float(self.cb2.get()))/12.0
        cd2_ft = (float(self.cd2.get()))/12.0

        lcc_ft = float(self.lcc.get())

        #Bar Sizes
        bar_right = self.rebar.bar[int(self.right_bar_size.get())]
        bar_left = self.rebar.bar[int(self.left_bar_size.get())]
        bar_left_size = int(self.left_bar_size.get())
        bar_right_size = int(self.right_bar_size.get())

        #Left Foundation Calculations
        a1 = self.ftg1_A_sqft
        sw1 = self.ftg1_sw_kips
        self.ftg1_text = self.ftg1_text + 'A = B * D = {0:.2f} ft^2\nSelf Wt = A * H/12 * Density = {1:.2f} kips\n'.format(a1,sw1)

        r1s = self.service[-2][1]
        r1u = self.ultimate[-2][1]
        qa1 = r1s / a1
        qu1 = r1u / a1
        
        self.ftg1_qa = qa1

        self.ftg1_text = self.ftg1_text + '\n-- {0:-<82}\n'.format('Bearing: ')
        if qa1 <= qa_ksf:
            self.ftg1_text = self.ftg1_text + 'Qa = R1,service / A = {0:.2f} kips / A = {1:.2f} ksf < Q,allow = {2:.2f} ksf -- OK\nQu = R1,ultimate / A = {3:.2f} kips / A = {4:.2f} ksf\n'.format(r1s,qa1,qa_ksf,r1u,qu1)
            self.status_ftg1_q.set(1)
        else:
            self.ftg1_text = self.ftg1_text + 'Qa = R1,service / A = {0:.2f} kips / A = {1:.2f} ksf > Q,allow = {2:.2f} ksf -- **NG**\nQu = R1,ultimate / A = {3:.2f} kips / A = {4:.2f} ksf\n'.format(r1s,qa1,qa_ksf,r1u,qu1)
            self.status_ftg1_q.set(0)

        #Left - Flexure
        self.ftg1_text = self.ftg1_text + '\n-- {0:-<82}\n'.format('Flexure: ')
        d1_in = h1_in - 3 - (bar_left[0]/2.0)
        self.ftg1_text = self.ftg1_text + 'd = H - 3" - Dia. bar/2 = {0:.2f} - 3 - {1:.2f}/2 = {2:.2f} in\n'.format(h1_in,bar_left[0], d1_in)
        lb1 = (d1_ft/2.0) - (bs_ft/2.0)
        Mu1 = ((qu1 * b1_ft)*lb1) * (lb1/2.0)
        Mu1_inlbs = Mu1 * 12.0 * 1000.0

        self.ftg1_text = self.ftg1_text + 'Face of Ftg to Face of Strap = L = D/2 - Bstrap/2 = {0:.2f} ft\n'.format(lb1)
        self.ftg1_text = self.ftg1_text + 'Mu = Qu * B * L^2 / 2.0 = {0:.2f} ft-kips\n'.format(Mu1)

        rho1 = (0.85*fpc_psi*(1-(1-(Mu1_inlbs/(0.838*b1_in*(d1_in**2)*fpc_psi)))**0.5))/fy_psi
        rho_max = 0.319 * beta1 * (fpc_psi/fy_psi)
        as1_calc = rho1*b1_in*d1_in
        as1_min = 0.0018*b1_in*h1_in
        as1_req = max(as1_calc, as1_min)
        bars1 = max(m.ceil(as1_req / bar_left[1]),2)
        spacing = (b1_in - 6.0) / (bars1-1)
        max_spacing = min(3*h1_in,18)
        bars_max = m.ceil((b1_in - 6.0) / max_spacing) + 1
        spacing_act = (b1_in - 6.0) / (max(bars1,bars_max)-1)
        
        self.ftg1_bars_text = '({1})#{0}'.format(bar_left_size, max(bars_max,bars1))

        #development - ACI 318-08 12.2.3
        cb_l = min(3+(bar_left[0]/2), 0.5*spacing_act)
        psi_t = 1.0
        psi_e = 1.0
        if bar_left_size < 7:
            psi_s = 0.8
        else:
            psi_s = 1.0

        ld = ((3.0/40.0)*1*(fy_psi/fpc_psi**0.5)*((psi_t*psi_e*psi_s)/(min(cb_l/bar_left[0],2.5))))*bar_left[0]
        as_reduction = as1_req / (max(bars_max,bars1)*bar_left[1])
        ld_min = 12
        ld_reduced = ld*as_reduction
        ld_use = max(ld_min,ld_reduced)
        ld_avail = (d1ftg_in/2.0) - 3.0 - (bs_in/2.0)
        ld_test = ld_avail >= ld_use

        if rho1 > rho_max:
            self.status_ftg1f.set(0)
            self.ftg1_text = self.ftg1_text + '\nrho,req = {0:.4f} > rho,t = {1:.4f} -- **NG**\n'.format(rho1, rho_max)

        elif ld_test == False:
            self.status_ftg1f.set(0)
            self.ftg1_text = self.ftg1_text + '\nrho,req = {0:.4f} > rho,t = {1:.4f} -- OK\n'.format(rho1, rho_max)
            self.ftg1_text = self.ftg1_text + '\nrho,req = {0:.4f} < rho,t = {1:.4f} -- OK\n'.format(rho1, rho_max)
            self.ftg1_text = self.ftg1_text + 'As = rho*b*d = {0:.2f} in^2\n'.format(as1_calc)
            self.ftg1_text = self.ftg1_text + 'As,min = 0.0018*b*h = {0:.2f} in^2\n'.format(as1_min)
            self.ftg1_text = self.ftg1_text + 'As,req = max[As,As,min] = {0:.2f} in^2 -- ({1})#{2} Bars\n'.format(as1_req, bars1, bar_left_size)
            self.ftg1_text = self.ftg1_text + '\nBar Spacing = B - 6 in / (#bars - 1) = {0:.2f} in\n'.format(spacing)
            self.ftg1_text = self.ftg1_text + 'Max. Spacing = min of 3*H or 18 in = {0:.2f} in\n'.format(max_spacing)
            self.ftg1_text = self.ftg1_text + 'Bars for Max. Spacing = ({0})#{1} Bars --- Use ({2})#{1} Bars @ {3:.2f} in o.c.\n'.format(bars_max,bar_left_size, max(bars_max,bars1), spacing_act)
            self.ftg1_text = self.ftg1_text + '\nDevelopment Length of bars:\n'
            self.ftg1_text = self.ftg1_text + 'cb = min of cover+0.5db and 0.5*bar Spacing = {0:.3f}\n'.format(cb_l)
            self.ftg1_text = self.ftg1_text + 'lambda = 1.0\npsi,t = 1.0\npsi,e = 1.0\npsi,s = {0}\n'.format(psi_s)
            self.ftg1_text = self.ftg1_text + "ld = [(3/40)*(Fy/ lambda * sqrt(F'c))*(psi,t psi,e psi,s/(cb/db))]*db [ACI 318-08 eq 12-2]\nwhere cb/db <= 2.5 -- cb/db= {1:.3f}\nld = {0:.3f} in\n".format(ld, cb_l/bar_left[0])
            self.ftg1_text = self.ftg1_text + 'Reduction of As,req/As = {0:.3f}\n'.format(as_reduction)
            self.ftg1_text = self.ftg1_text + 'ld,reduced = {0:.3f} in\n'.format(ld_reduced)
            self.ftg1_text = self.ftg1_text + 'ld,min = 12.0 in\n'
            self.ftg1_text = self.ftg1_text + 'Use max of ld, reduced amd ld,min = {0:.3f} in\n'.format(ld_use)
            self.ftg1_text = self.ftg1_text + 'ld,available = D - 3 - Bs/2 = {0:.3f} in\n'.format(ld_avail)
            self.ftg1_text = self.ftg1_text + 'ld > ld,available -- **NG**\n'

        else:
            self.status_ftg1f.set(1)
            self.ftg1_text = self.ftg1_text + '\nrho,req = {0:.4f} < rho,t = {1:.4f} -- OK\n'.format(rho1, rho_max)
            self.ftg1_text = self.ftg1_text + 'As = rho*b*d = {0:.2f} in^2\n'.format(as1_calc)
            self.ftg1_text = self.ftg1_text + 'As,min = 0.0018*b*h = {0:.2f} in^2\n'.format(as1_min)
            self.ftg1_text = self.ftg1_text + 'As,req = max[As,As,min] = {0:.2f} in^2 -- ({1})#{2} Bars\n'.format(as1_req, bars1, bar_left_size)
            self.ftg1_text = self.ftg1_text + '\nBar Spacing = B - 6 in / (#bars - 1) = {0:.2f} in\n'.format(spacing)
            self.ftg1_text = self.ftg1_text + 'Max. Spacing = min of 3*H or 18 in = {0:.2f} in\n'.format(max_spacing)
            self.ftg1_text = self.ftg1_text + 'Bars for Max. Spacing = ({0})#{1} Bars --- Use ({2})#{1} Bars @ {3:.2f} in o.c.\n'.format(bars_max,bar_left_size, max(bars_max,bars1), spacing_act)
            self.ftg1_text = self.ftg1_text + '\nDevelopment Length of bars:\n'
            self.ftg1_text = self.ftg1_text + 'cb = min of cover+0.5db and 0.5*bar Spacing = {0:.3f}\n'.format(cb_l)
            self.ftg1_text = self.ftg1_text + 'lambda = 1.0\npsi,t = 1.0\npsi,e = 1.0\npsi,s = {0}\n'.format(psi_s)
            self.ftg1_text = self.ftg1_text + "ld = [(3/40)*(Fy/ lambda * sqrt(F'c))*(psi,t psi,e psi,s/(cb/db))]*db [ACI 318-08 eq 12-2]\nwhere cb/db <= 2.5 -- cb/db= {1:.3f}\nld = {0:.3f} in\n".format(ld, cb_l/bar_left[0])
            self.ftg1_text = self.ftg1_text + 'Reduction of As,req/As = {0:.3f}\n'.format(as_reduction)
            self.ftg1_text = self.ftg1_text + 'ld,reduced = {0:.3f} in\n'.format(ld_reduced)
            self.ftg1_text = self.ftg1_text + 'ld,min = 12.0 in\n'
            self.ftg1_text = self.ftg1_text + 'Use max of ld, reduced amd ld,min = {0:.3f} in\n'.format(ld_use)
            self.ftg1_text = self.ftg1_text + 'ld,available = D - 3 - Bs/2 = {0:.3f} in\n'.format(ld_avail)
            self.ftg1_text = self.ftg1_text + 'ld < ld,available -- OK\n'

        #Left - Shear
        self.ftg1_text = self.ftg1_text + '\n-- {0:-<82}\n'.format('Flexural Shear: ')
        #ACI 318-08 equation 11-3
        aci_11_31 = 2.0*1.0*b1_in*d1_in*(fpc_psi**0.5)*(1/1000.0)

        phi_vc_flexural_shear1 = aci_11_31 * 0.75

        self.ftg1_text = self.ftg1_text + "Phi = 0.75\nVc = 2*1*B*d*sqrt(F'c) / 1000 lbs/kips = {0:.2f} kips [ACI 318-08 eq 11-3]\nPhi*Vc = {1:.2f} kips\n".format(aci_11_31,phi_vc_flexural_shear1)

        x1_ft = lb1 - (d1_in/12.0)

        vu_flexural_shear1 = qu1*b1_ft*x1_ft
        self.ftg1_text = self.ftg1_text + 'X = L,flexure - d/2 = {0:.2f} ft\nVu = Qu * B * X = {1:.2f} kips\n'.format(x1_ft,vu_flexural_shear1)

        if vu_flexural_shear1 > phi_vc_flexural_shear1:
            self.status_ftg1v.set(0)
            self.ftg1_text = self.ftg1_text + 'Vu > Phi*Vc -- **NG**'
        else:
            self.status_ftg1v.set(1)
            self.ftg1_text = self.ftg1_text + 'Vu < Phi*Vc -- OK'


        a2 = self.ftg2_A_sqft
        sw2 = self.ftg2_sw_kips
        self.ftg2_text = self.ftg2_text + 'A = B * D = {0:.2f} ft^2\nSelf Wt = A * H/12 * Density = {1:.2f} kips\n'.format(a2,sw2)
        r2s = self.service[-1][1]
        r2u = self.ultimate[-1][1]
        qa2 = r2s / a2
        qu2 = r2u / a2
        
        self.ftg2_qa = qa2

        self.ftg2_text = self.ftg2_text + '\n-- {0:-<82}\n'.format('Bearing: ')
        if qa2 <= qa_ksf:
            self.ftg2_text = self.ftg2_text + 'Qa = R2,service / A = {0:.2f} kips / A = {1:.2f} ksf < Q,allow = {2:.2f} ksf -- OK\nQu = R2,ultimate / A = {3:.2f} kips / A = {4:.2f} ksf\n'.format(r2s,qa2,qa_ksf,r2u,qu2)
            self.status_ftg2_q.set(1)
        else:
            self.ftg2_text = self.ftg2_text + 'Qa = R2,service / A = {0:.2f} kips / A = {1:.2f} ksf > Q,allow = {2:.2f} ksf -- **NG**\nQu = R2,ultimate / A = {3:.2f} kips / A = {4:.2f} ksf\n'.format(r2s,qa2,qa_ksf,r2u,qu2)
            self.status_ftg2_q.set(0)

        right_m_status = [0,0]
        right_v_status = [0,0]

        #Right - Flexure - N/S
        self.ftg2_text = self.ftg2_text + '\n-- {0:-<82}\n'.format('Flexure - N/S : ')
        d2_in = h2_in - 3 - (bar_right[0]/2.0)
        self.ftg2_text = self.ftg2_text + 'd = H - 3" - Dia. bar/2 = {0:.2f} - 3 - {1:.2f}/2 = {2:.2f} in\n'.format(h2_in,bar_right[0], d2_in)
        lb2 = (d2_ft/2.0) - (bs_ft/2.0)
        Mu2 = ((qu2 * b2_ft)*lb2) * (lb2/2.0)
        Mu2_inlbs = Mu2 * 12.0 * 1000.0

        self.ftg2_text = self.ftg2_text + 'Face of Ftg to Face of Strap = L = D/2 - Bstrap/2 = {0:.2f} ft\n'.format(lb2)
        self.ftg2_text = self.ftg2_text + 'Mu = Qu * B * L^2 / 2.0 = {0:.2f} ft-kips\n'.format(Mu2)

        rho2 = (0.85*fpc_psi*(1-(1-(Mu2_inlbs/(0.838*b2_in*(d2_in**2)*fpc_psi)))**0.5))/fy_psi
        rho_max = 0.319 * beta1 * (fpc_psi/fy_psi)
        as2_calc = rho2*b2_in*d2_in
        as2_min = 0.0018*b2_in*h2_in
        as2_req = max(as2_calc, as2_min)
        bars2 = m.ceil(as2_req / bar_right[1])
        spacing2 = (b2_in - 6.0) / (bars2-1)
        max_spacing2 = min(3*h2_in,18)
        bars_max2 = m.ceil((b2_in - 6.0) / max_spacing2) + 1
        spacing_act2 = (b2_in - 6.0) / (max(bars2,bars_max2)-1)
        
        self.ftg2_barsns_text = '({1})#{0}'.format(bar_right_size, max(bars_max2,bars2))
        
        #development - ACI 318-08 12.2.3
        cb_l2 = min(3+(bar_right[0]/2), 0.5*spacing_act2)
        psi_t2 = 1.0
        psi_e2 = 1.0
        if bar_right_size < 7:
            psi_s2 = 0.8
        else:
            psi_s2 = 1.0

        ld2 = ((3.0/40.0)*1*(fy_psi/fpc_psi**0.5)*((psi_t2*psi_e2*psi_s2)/(min(cb_l2/bar_right[0],2.5))))*bar_right[0]
        as_reduction2 = as2_req / (max(bars_max2,bars2)*bar_right[1])
        ld_reduced2 = ld2*as_reduction2
        ld_use2 = max(ld_min,ld_reduced2)
        ld_avail2 = (d2ftg_in/2.0) - 3.0 - (bs_in/2.0)
        ld_test2 = ld_avail2 >= ld_use2

        if rho2 > rho_max:
            right_m_status[0] = 0
            self.ftg2_text = self.ftg2_text + '\nrho,req = {0:.4f} > rho,t = {1:.4f} -- **NG**\n'.format(rho2, rho_max)

        elif ld_test2 == False:
            right_m_status[0] = 0
            self.ftg2_text = self.ftg2_text + '\nrho,req = {0:.4f} < rho,t = {1:.4f} -- OK\n'.format(rho2, rho_max)
            self.ftg2_text = self.ftg2_text + 'As = rho*B*d = {0:.2f} in^2\n'.format(as2_calc)
            self.ftg2_text = self.ftg2_text + 'As,min = 0.0018*B*h = {0:.2f} in^2\n'.format(as2_min)
            self.ftg2_text = self.ftg2_text + 'As,req = max[As,As,min] = {0:.2f} in^2 -- ({1})#{2} Bars\n'.format(as2_req, bars2, bar_right_size)
            self.ftg2_text = self.ftg2_text + '\nBar Spacing = B - 6 in / (#bars - 1) = {0:.2f} in\n'.format(spacing2)
            self.ftg2_text = self.ftg2_text + 'Max. Spacing = min of 3*H or 18 in = {0:.2f} in\n'.format(max_spacing2)
            self.ftg2_text = self.ftg2_text + 'Bars for Max. Spacing = ({0})#{1} --- Use ({2})#{1} Bars @ {3:.2f} in o.c.\n'.format(bars_max2,bar_right_size, max(bars_max2, bars2), spacing_act2)
            self.ftg2_text = self.ftg2_text + '\nDevelopment Length of bars:\n'
            self.ftg2_text = self.ftg2_text + 'cb = min of cover+0.5db and 0.5*bar Spacing = {0:.3f}\n'.format(cb_l2)
            self.ftg2_text = self.ftg2_text + 'lambda = 1.0\npsi,t = 1.0\npsi,e = 1.0\npsi,s = {0}\n'.format(psi_s2)
            self.ftg2_text = self.ftg2_text + "ld = [(3/40)*(Fy/ lambda * sqrt(F'c))*(psi,t psi,e psi,s/(cb/db))]*db [ACI 318-08 eq 12-2]\nwhere cb/db <= 2.5 -- cb/db= {1:.3f}\nld = {0:.3f} in\n".format(ld2, cb_l2/bar_right[0])
            self.ftg2_text = self.ftg2_text + 'Reduction of As,req/As = {0:.3f}\n'.format(as_reduction2)
            self.ftg2_text = self.ftg2_text + 'ld,reduced = {0:.3f} in\n'.format(ld_reduced2)
            self.ftg2_text = self.ftg2_text + 'ld,min = 12.0 in\n'
            self.ftg2_text = self.ftg2_text + 'Use max of ld, reduced amd ld,min = {0:.3f} in\n'.format(ld_use2)
            self.ftg2_text = self.ftg2_text + 'ld,available = D - 3 - Bs/2 = {0:.3f} in\n'.format(ld_avail2)
            self.ftg2_text = self.ftg2_text + 'ld > ld,available -- **NG**\n'
        else:
            right_m_status[0] = 1
            self.ftg2_text = self.ftg2_text + '\nrho,req = {0:.4f} < rho,t = {1:.4f} -- OK\n'.format(rho2, rho_max)
            self.ftg2_text = self.ftg2_text + 'As = rho*B*d = {0:.2f} in^2\n'.format(as2_calc)
            self.ftg2_text = self.ftg2_text + 'As,min = 0.0018*B*h = {0:.2f} in^2\n'.format(as2_min)
            self.ftg2_text = self.ftg2_text + 'As,req = max[As,As,min] = {0:.2f} in^2 -- ({1})#{2} Bars\n'.format(as2_req, bars2, bar_right_size)
            self.ftg2_text = self.ftg2_text + '\nBar Spacing = B - 6 in / (#bars - 1) = {0:.2f} in\n'.format(spacing2)
            self.ftg2_text = self.ftg2_text + 'Max. Spacing = min of 3*H or 18 in = {0:.2f} in\n'.format(max_spacing2)
            self.ftg2_text = self.ftg2_text + 'Bars for Max. Spacing = ({0})#{1} --- Use ({2})#{1} Bars @ {3:.2f} in o.c.\n'.format(bars_max2,bar_right_size, max(bars_max2, bars2), spacing_act2)
            self.ftg2_text = self.ftg2_text + '\nDevelopment Length of bars:\n'
            self.ftg2_text = self.ftg2_text + 'cb = min of cover+0.5db and 0.5*bar Spacing = {0:.3f}\n'.format(cb_l2)
            self.ftg2_text = self.ftg2_text + 'lambda = 1.0\npsi,t = 1.0\npsi,e = 1.0\npsi,s = {0}\n'.format(psi_s2)
            self.ftg2_text = self.ftg2_text + "ld = [(3/40)*(Fy/ lambda * sqrt(F'c))*(psi,t psi,e psi,s/(cb/db))]*db [ACI 318-08 eq 12-2]\nwhere cb/db <= 2.5 -- cb/db= {1:.3f}\nld = {0:.3f} in\n".format(ld2, cb_l2/bar_right[0])
            self.ftg2_text = self.ftg2_text + 'Reduction of As,req/As = {0:.3f}\n'.format(as_reduction2)
            self.ftg2_text = self.ftg2_text + 'ld,reduced = {0:.3f} in\n'.format(ld_reduced2)
            self.ftg2_text = self.ftg2_text + 'ld,min = 12.0 in\n'
            self.ftg2_text = self.ftg2_text + 'Use max of ld, reduced amd ld,min = {0:.3f} in\n'.format(ld_use2)
            self.ftg2_text = self.ftg2_text + 'ld,available = D - 3 - Bs/2 = {0:.3f} in\n'.format(ld_avail2)
            self.ftg2_text = self.ftg2_text + 'ld < ld,available -- OK\n'


        #right - Shear - N/S
        self.ftg2_text = self.ftg2_text + '\n-- {0:-<82}\n'.format('Flexural Shear - N/S : ')
        #ACI 318-08 equation 11-3
        aci_11_32 = 2.0*1.0*b2_in*d2_in*(fpc_psi**0.5)*(1/1000.0)

        phi_vc_flexural_shear2 = aci_11_32 * 0.75

        self.ftg2_text = self.ftg2_text + "Phi = 0.75\nVc = 2*1*B*d*sqrt(F'c) / 1000 lbs/kips = {0:.2f} kips [ACI 318-08 eq 11-3]\nPhi*Vc = {1:.2f} kips\n".format(aci_11_32,phi_vc_flexural_shear2)

        x2_ft = lb2 - (d2_in/12.0)

        vu_flexural_shear2 = qu2*b2_ft*x2_ft
        self.ftg2_text = self.ftg2_text + 'X = L,flexure - d/2 = {0:.2f} ft\nVu = Qu * B * X = {1:.2f} kips\n'.format(x2_ft,vu_flexural_shear2)

        if vu_flexural_shear2 > phi_vc_flexural_shear2:
            right_v_status[0] = 0
            self.ftg2_text = self.ftg2_text + 'Vu > Phi*Vc -- **NG**'
        else:
            right_v_status[0] = 1
            self.ftg2_text = self.ftg2_text + 'Vu < Phi*Vc -- OK'

        #Right - Flexure - E/W
        self.ftg2_text = self.ftg2_text + '\n\n-- {0:-<82}\n'.format('Flexure - E/W : ')
        d2_inew = h2_in - 3 - bar_right[0] - (bar_right[0]/2.0)
        self.ftg2_text = self.ftg2_text + 'd = H - 3" - Dia. bar - Dia. bar/2 = {0:.2f} - 3 - {1:.2f} - {1:.2f}/2 = {2:.2f} in\n'.format(h2_in,bar_right[0], d2_inew)
        x_mew = cb2_ft/2.0
        xc_mew = lcc_ft - (cb2_ft/2.0)

        vew,mew = self.simple_beam_ultimate_analysisx(x_mew)
        vcew,mcew = self.simple_beam_ultimate_analysisx(xc_mew)

        Mu2ew = max(mew[2],mcew[1])

        Mu2_inlbsew = Mu2ew * 12.0 * 1000.0

        self.ftg2_text = self.ftg2_text + '\nMu, at face of column, left = {0:.2f} ft-kips\nMu, at face of column, right = {1:.2f} ft-kips\nMu, design = {2:.2f} ft-kips\n'.format(mcew[1],mew[2],Mu2ew)

        rho2ew = (0.85*fpc_psi*(1-(1-(Mu2_inlbsew/(0.838*b2_in*(d2_inew**2)*fpc_psi)))**0.5))/fy_psi
        rho_max = 0.319 * beta1 * (fpc_psi/fy_psi)
        as2_calcew = rho2ew*(d2ftg_in)*d2_inew
        as2_minew = 0.0018*d2ftg_in*h2_in
        as2_reqew = max(as2_calcew, as2_minew)
        bars2ew = m.ceil(as2_reqew / bar_right[1])
        spacing2ew = (d2ftg_in - 6.0) / (bars2ew-1)
        max_spacing2ew = min(3*h2_in,18)
        bars_max2ew = m.ceil((d2ftg_in - 6.0) / max_spacing2ew) + 1
        spacing_act2ew = (d2ftg_in - 6.0) / (max(bars2ew,bars_max2ew)-1)
        
        self.ftg2_barsew_text = '({1})#{0}'.format(bar_right_size, max(bars_max2ew,bars2ew))
        
        #development - ACI 318-08 12.2.3
        cb_l2ew = min(3+(bar_right[0]/2)+bar_right[0], 0.5*spacing_act2ew)
        psi_t2ew = 1.0
        psi_e2ew = 1.0
        if bar_right_size < 7:
            psi_s2ew = 0.8
        else:
            psi_s2ew = 1.0

        ld2ew = ((3.0/40.0)*1*(fy_psi/fpc_psi**0.5)*((psi_t2ew*psi_e2ew*psi_s2ew)/(min(cb_l2ew/bar_right[0],2.5))))*bar_right[0]
        as_reduction2ew = as2_reqew / (max(bars_max2ew,bars2ew)*bar_right[1])
        ld_reduced2ew = ld2ew*as_reduction2ew
        ld_use2ew = max(ld_min,ld_reduced2ew)
        ld_avail2ew = (b2_in/2.0) - 3.0 - ((cb2_ft*12.0)/2.0) - (e2_ft*12.0)
        ld_test2ew = ld_avail2ew >= ld_use2ew

        if rho2ew > rho_max:
            right_m_status[1] = 0
            self.ftg2_text = self.ftg2_text + '\nrho,req = {0:.4f} > rho,t = {1:.4f} -- **NG**\n'.format(rho2ew, rho_max)
        elif ld_test2ew == False:
            right_m_status[1] = 0
            self.ftg2_text = self.ftg2_text + '\nrho,req = {0:.4f} < rho,t = {1:.4f} -- OK\n'.format(rho2ew, rho_max)
            self.ftg2_text = self.ftg2_text + 'As = rho*D*d = {0:.2f} in^2\n'.format(as2_calcew)
            self.ftg2_text = self.ftg2_text + 'As,min = 0.0018*D*h = {0:.2f} in^2\n'.format(as2_minew)
            self.ftg2_text = self.ftg2_text + 'As,req = max[As,As,min] = {0:.2f} in^2 -- ({1})#{2} Bars\n'.format(as2_reqew, bars2ew, bar_right_size)
            self.ftg2_text = self.ftg2_text + '\nBar Spacing = D - 6 in / (#bars - 1) = {0:.2f} in\n'.format(spacing2ew)
            self.ftg2_text = self.ftg2_text + 'Max. Spacing = min of 3*H or 18 in = {0:.2f} in\n'.format(max_spacing2ew)
            self.ftg2_text = self.ftg2_text + 'Bars for Max. Spacing = ({0})#{1} --- Use ({2})#{1} Bars @ {3:.2f} in o.c.\n'.format(bars_max2ew,bar_right_size, max(bars_max2ew, bars2ew), spacing_act2ew)
            self.ftg2_text = self.ftg2_text + '\nDevelopment Length of bars:\n'
            self.ftg2_text = self.ftg2_text + 'cb = min of cover+db+0.5db and 0.5*bar Spacing = {0:.3f}\n'.format(cb_l2ew)
            self.ftg2_text = self.ftg2_text + 'lambda = 1.0\npsi,t = 1.0\npsi,e = 1.0\npsi,s = {0}\n'.format(psi_s2ew)
            self.ftg2_text = self.ftg2_text + "ld = [(3/40)*(Fy/ lambda * sqrt(F'c))*(psi,t psi,e psi,s/(cb/db))]*db [ACI 318-08 eq 12-2]\nwhere cb/db <= 2.5 -- cb/db= {1:.3f}\nld = {0:.3f} in\n".format(ld2ew, cb_l2ew/bar_right[0])
            self.ftg2_text = self.ftg2_text + 'Reduction of As,req/As = {0:.3f}\n'.format(as_reduction2ew)
            self.ftg2_text = self.ftg2_text + 'ld,reduced = {0:.3f} in\n'.format(ld_reduced2ew)
            self.ftg2_text = self.ftg2_text + 'ld,min = 12.0 in\n'
            self.ftg2_text = self.ftg2_text + 'Use max of ld, reduced amd ld,min = {0:.3f} in\n'.format(ld_use2ew)
            self.ftg2_text = self.ftg2_text + 'ld,available = B/2 - 3 - B,col/2 - e2 = {0:.3f} in\n'.format(ld_avail2ew)
            self.ftg2_text = self.ftg2_text + 'ld > ld,available -- **NG**\n'
        else:
            right_m_status[1] = 1
            self.ftg2_text = self.ftg2_text + '\nrho,req = {0:.4f} < rho,t = {1:.4f} -- OK\n'.format(rho2ew, rho_max)
            self.ftg2_text = self.ftg2_text + 'As = rho*D*d = {0:.2f} in^2\n'.format(as2_calcew)
            self.ftg2_text = self.ftg2_text + 'As,min = 0.0018*D*h = {0:.2f} in^2\n'.format(as2_minew)
            self.ftg2_text = self.ftg2_text + 'As,req = max[As,As,min] = {0:.2f} in^2 -- ({1})#{2} Bars\n'.format(as2_reqew, bars2ew, bar_right_size)
            self.ftg2_text = self.ftg2_text + '\nBar Spacing = D - 6 in / (#bars - 1) = {0:.2f} in\n'.format(spacing2ew)
            self.ftg2_text = self.ftg2_text + 'Max. Spacing = min of 3*H or 18 in = {0:.2f} in\n'.format(max_spacing2ew)
            self.ftg2_text = self.ftg2_text + 'Bars for Max. Spacing = ({0})#{1} --- Use ({2})#{1} Bars @ {3:.2f} in o.c.\n'.format(bars_max2ew,bar_right_size, max(bars_max2ew, bars2ew), spacing_act2ew)
            self.ftg2_text = self.ftg2_text + '\nDevelopment Length of bars:\n'
            self.ftg2_text = self.ftg2_text + 'cb = min of cover+db+0.5db and 0.5*bar Spacing = {0:.3f}\n'.format(cb_l2ew)
            self.ftg2_text = self.ftg2_text + 'lambda = 1.0\npsi,t = 1.0\npsi,e = 1.0\npsi,s = {0}\n'.format(psi_s2ew)
            self.ftg2_text = self.ftg2_text + "ld = [(3/40)*(Fy/ lambda * sqrt(F'c))*(psi,t psi,e psi,s/(cb/db))]*db [ACI 318-08 eq 12-2]\nwhere cb/db <= 2.5 -- cb/db= {1:.3f}\nld = {0:.3f} in\n".format(ld2ew, cb_l2ew/bar_right[0])
            self.ftg2_text = self.ftg2_text + 'Reduction of As,req/As = {0:.3f}\n'.format(as_reduction2ew)
            self.ftg2_text = self.ftg2_text + 'ld,reduced = {0:.3f} in\n'.format(ld_reduced2ew)
            self.ftg2_text = self.ftg2_text + 'ld,min = 12.0 in\n'
            self.ftg2_text = self.ftg2_text + 'Use max of ld, reduced amd ld,min = {0:.3f} in\n'.format(ld_use2ew)
            self.ftg2_text = self.ftg2_text + 'ld,available = B/2 - 3 - B,col/2 - e2 = {0:.3f} in\n'.format(ld_avail2ew)
            self.ftg2_text = self.ftg2_text + 'ld < ld,available -- OK\n'

        #right - Shear - E/W
        self.ftg2_text = self.ftg2_text + '\n-- {0:-<82}\n'.format('Flexural Shear - E/W : ')
        #ACI 318-08 equation 11-3
        aci_11_32ew = 2.0*1.0*d2ftg_in*d2_inew*(fpc_psi**0.5)*(1/1000.0)

        phi_vc_flexural_shear2ew = aci_11_32ew * 0.75

        self.ftg2_text = self.ftg2_text + "Phi = 0.75\nVc = 2*1*D*d*sqrt(F'c) / 1000 lbs/kips = {0:.2f} kips [ACI 318-08 eq 11-3]\nPhi*Vc = {1:.2f} kips\n".format(aci_11_32ew,phi_vc_flexural_shear2ew)

        x_vew = (cb2_ft /2.0)+(d2_inew/12.0)
        xc_vew = lcc_ft - (cb2_ft/2.0) - (d2_inew/12.0)

        vew,mew = self.simple_beam_ultimate_analysisx(x_vew)
        vewl, mewl = self.simple_beam_ultimate_analysisx(xc_vew)

        vu_right = abs(vew[2])
        vu_left = abs(vewl[1])

        vu_flexural_shear2ew = max(vu_left, vu_right)

        self.ftg2_text = self.ftg2_text + '\nVu at d from column face, left = {0:.2f} kips\nVu at d from column face, right = {1:.2f} kips\nVu,design = max of above = {2:.2f}\n\n'.format(vu_left,vu_right,vu_flexural_shear2ew)

        if vu_flexural_shear2ew > phi_vc_flexural_shear2ew:
            right_v_status[1] = 0
            self.ftg2_text = self.ftg2_text + 'Vu > Phi*Vc -- **NG**'
        else:
            right_v_status[1] = 1
            self.ftg2_text = self.ftg2_text + 'Vu < Phi*Vc -- OK'

        self.left_ftg_calc_txtbox.insert(tk.END, self.ftg1_text)
        self.right_ftg_calc_txtbox.insert(tk.END, self.ftg2_text)

        if right_m_status == [1,1]:
            self.status_ftg2f.set(1)
        else:
            self.status_ftg2f.set(0)
        if right_v_status == [1,1]:
            self.status_ftg2v.set(1)
        else:
            self.status_ftg2v.set(0)

        self.strap_design()

    def strap_design(self):
        self.strap_calc_txtbox.delete(1.0,tk.END)

        self.strap_text = '\n{1:-^85}\n-- {0:-<82}\n{2:-^85}\n'.format('Strap Beam Calculations: ','-','-')
        self.strap_text = self.strap_text + 'Cover to Shear Bars: 1-1/2 in.\n'

        cover = 1.50

        #Common data items
        sw_pcf = float(self.density_pcf.get())
        qa_ksf = float(self.Qa_ksf.get())
        fpc_ksi = float(self.Fpc_ksi.get())
        fpc_psi = fpc_ksi * 1000.0
        dl_factor = float(self.dl_factor.get())
        fy_ksi = float(self.Fy_ksi.get())
        fy_psi = fy_ksi * 1000.0

        if fpc_psi <= 4000:
            beta1 = 0.85
        elif fpc_psi <= 8000:
            beta1 = 0.85 - ((0.05*(fpc_psi-4000))/1000)
        else:
            beta1 = 0.65

        lcc_ft = float(self.lcc.get())

        #column widths
        cb1_ft = (float(self.cb1.get()))/12.0
        cb2_ft = (float(self.cb2.get()))/12.0

        #Strap
        bs_in = float(self.bs.get())
        bs_ft = bs_in/12.0
        hs_in = float(self.hs.get())
        hs_ft = hs_in/12.0

        #Bar Sizes
        bar_v = self.rebar.bar[int(self.strap_vbar_size.get())]
        bar_m = self.rebar.bar[int(self.strap_bar_size.get())]
        bar_v_size = int(self.strap_vbar_size.get())
        bar_m_size = int(self.strap_bar_size.get())

        self.strap_text = self.strap_text + '\n-- {0:-<82}\n'.format('Flexure : ')

        mu = min(self.momentc_u)
        mu_inlbs = abs(mu) * 12.0 * 1000.0
        
        mu_max = max(self.momentc_u)
        mu_max_inlbs = abs(mu_max) * 12.0 * 1000.0

        self.strap_text = self.strap_text + 'Mu,min = {0:.2f} ft-kips\n'.format(mu)
        self.strap_text = self.strap_text + 'Mu,max = {0:.2f} ft-kips\n'.format(mu_max)

        d_in = hs_in - cover - bar_v[0] - (bar_m[0]/2.0)
        self.strap_text = self.strap_text + 'd = h - cover - Dia. shear bar - Dia. flexure bar/2.0 = {0:.2f} in.\n'.format(d_in)

        R = mu_inlbs / (0.9*bs_in*d_in*d_in)

        #quadratic solution
        c = -1.0*R
        b = fy_psi
        a = (-0.588*fy_psi*fy_psi) / fpc_psi

        rho1 = (-b + ((b**2) - (4*a*c))**0.5)/(2*a)
        rho2 = (-b - ((b**2) - (4*a*c))**0.5)/(2*a)
        rho = min(rho1, rho2)
        rho_max = 0.319 * beta1 * (fpc_psi/fy_psi)
        as_calc = rho*bs_in*d_in
        as_min = max((3*(fpc_psi**0.5)/fy_psi)*bs_in*d_in, 200.0*bs_in*d_in*(1/fy_psi))
        as_req = max(as_calc, as_min)
        bars = as_req / bar_m[1]
        
        self.strap_bars_text = '({0})#{1}'.format(m.ceil(bars), bar_m_size)

        if rho > rho_max:
            self.status_sf.set(0)
            self.strap_text = self.strap_text + 'phi = 0.9\n'
            self.strap_text = self.strap_text + 'R = Mu_inlbs / phi*b*d^2 = {0:.3f}\n'.format(R)
            self.strap_text = self.strap_text + "A = -0.588 *Fy^2 / F'c = {0:.3f}\n".format(a)
            self.strap_text = self.strap_text + 'B = Fy = {0:.2f}\n'.format(b)
            self.strap_text = self.strap_text + 'C = -R\n'
            self.strap_text = self.strap_text + 'rho+/- = -B +/- sqrt(B^2 - 4AC) / 2A = {0:.5f} or {1:.5f}\n'.format(rho1, rho2)
            self.strap_text = self.strap_text + 'rho,req = min of rho+/- = {0:.4f} > rho,t = {1:.4f} -- **NG**\n'.format(rho, rho_max)
        else:
            self.status_sf.set(1)
            self.strap_text = self.strap_text + 'phi = 0.9\n'
            self.strap_text = self.strap_text + '\nR = Mu_inlbs / phi*b*d^2 = {0:.3f}\n'.format(R)
            self.strap_text = self.strap_text + "A = -0.588 *Fy^2 / F'c = {0:.3f}\n".format(a)
            self.strap_text = self.strap_text + 'B = Fy = {0:.2f}\n'.format(b)
            self.strap_text = self.strap_text + 'C = -R\n'
            self.strap_text = self.strap_text + '\nrho+/- = -B +/- sqrt(B^2 - 4AC) / 2A = {0:.5f} or {1:.5f}\n'.format(rho1, rho2)
            self.strap_text = self.strap_text + 'rho,req = min of rho+/- = {0:.4f} < rho,t = {1:.4f} -- OK\n'.format(rho, rho_max)
            self.strap_text = self.strap_text + '\nAs = rho*b*d = {0:.2f} in^2\n'.format(as_calc)
            self.strap_text = self.strap_text + "As,min = max(200*b*d / fy , 3 sqrt(f'c) /fy *b*d) = {0:.2f} in^2\n".format(as_min)
            self.strap_text = self.strap_text + 'As,req = max[As,As,min] = {0:.2f} in^2 -- ({1})#{2} Bars\n'.format(as_req, m.ceil(bars), bar_m_size)

        #Shear
        self.strap_text = self.strap_text + '\n-- {0:-<82}\n'.format('Shear : ')
        #ACI 318-08 equation 11-3
        aci_11_3 = 2.0*1.0*bs_in*d_in*(fpc_psi**0.5)*(1/1000.0)

        phi_vc_flexural_shear = aci_11_3 * 0.75

        self.strap_text = self.strap_text + "Phi = 0.75\nVc = 2*1*b*d*sqrt(F'c) / 1000 lbs/kips = {0:.2f} kips [ACI 318-08 eq 11-3]\nPhi*Vc = {1:.2f} kips\n0.5*Phi*Vc = {2:.2f} kips\n".format(aci_11_3,phi_vc_flexural_shear, 0.5*phi_vc_flexural_shear)

        xl = (cb1_ft/2.0) + (d_in/12.0)
        xr = lcc_ft - (d_in/12.0) - (cb2_ft/2.0)

        vl, ml = self.simple_beam_ultimate_analysisx(xl)
        vr, mr = self.simple_beam_ultimate_analysisx(xr)

        Vu_left = abs(vl[1])

        Vu = Vu_left

        self.strap_text = self.strap_text + '\nVu - d from left = {0:.2f} kips\n--Shear at right resisted by foundation shear core (see ftg E/W design)--\n'.format(Vu_left)

        vs_max = 8*bs_in*d_in*fpc_psi**0.5
        phi_vs_max = vs_max*0.75
        vn_max = phi_vc_flexural_shear + phi_vs_max
        if Vu > vn_max:
            self.status_sv.set(0)
            self.strap_text = self.strap_text + "\nVs,req > 8*b*d*sqrt(f'c) -- **NG**\n"
        else:
            self.status_sv.set(1)
            if Vu > phi_vc_flexural_shear:
                self.strap_text = self.strap_text + '\n**Shear Reinforcement is required**\n\n'

                vs_left = (Vu_left - phi_vc_flexural_shear)/0.75
                av = (2*bar_v[1])
                s_left = (av * fy_psi * d_in) / (vs_left*1000.0)
                s_min = min(d_in/2.0,24.0)
                s_left_req = min(s_left, s_min)

                self.strap_text = self.strap_text + 'Left End:\n'
                self.strap_text = self.strap_text + 'Vs req. left = Vu left - Phi*Vc / Phi = {0:.2f} kips\n'.format(vs_left)
                self.strap_text = self.strap_text + 'Av = 2 * As,v = 2 * {0:.3f} in^2 = {1:.3f} in^2\n'.format(bar_v[1],2*bar_v[1])
                self.strap_text = self.strap_text + 's = As,v * Fy * d / Vs = {0:.2f} in\n'.format(s_left)
                self.strap_text = self.strap_text + 's,min = min of d/2 or 24 in = {0:.2f} in\n'.format(s_min)
                self.strap_text = self.strap_text + '\nUse: (2) Legs of #{0} Bars @ {1:.2f} in O.C.\n'.format(bar_v_size, s_left_req)

                self.strap_text = self.strap_text + '\nRight End:\n'
                self.strap_text = self.strap_text + 'Shear resisted by shear core of right foundation'


            elif Vu > (0.5*phi_vc_flexural_shear):
                self.strap_text = self.strap_text + '\n**Minimum Shear Reinforcement is required**\n\n'
                av_min_s = max((50*bs_in)/fy_psi, 0.75*(fpc_psi**0.5)*(bs_in/fy_psi))
                s_min = min(d_in/2.0,24.0)
                s_av = (2*bar_v[1]) / av_min_s
                s = min(s_min, s_av)
                self.strap_text = self.strap_text + 'Av, min = {0:.3f}*s\n'.format(av_min_s)
                self.strap_text = self.strap_text + 'Av = 2 * As,v = 2 * {0:.3f} in^2 = {1:.3f} in^2\n'.format(bar_v[1],2*bar_v[1])
                self.strap_text = self.strap_text + 's = {0:.2f} in\n'.format(s_av)
                self.strap_text = self.strap_text + 's,min = min of d/2 or 24 in = {0:.2f} in\n'.format(s_min)
                self.strap_text = self.strap_text + '\nUse: #{0} bars with 2-legs @ {1:.2f} in O.C.\n'.format(bar_v_size,s)

            else:
                self.strap_text = self.strap_text + '\nVu < 0.5*Phi*Vc -- OK, No Shear Reinforcement Required'

        self.strap_calc_txtbox.insert(tk.END, self.strap_text)

        self.save_output()

    def save_output(self):
        file = open('strap_results.txt','w')

        file.write(self.commons_out_text)
        file.write(self.left_fnd_out_text)
        file.write(self.left_col_out_text)
        file.write(self.right_fnd_out_text)
        file.write(self.right_col_out_text)
        file.write(self.strap_out_text)
        file.write(self.statics_out_text)
        file.write(self.service_out_text)
        file.write(self.ultimate_out_text)
        file.write(self.ftg1_text)
        file.write('\n')
        file.write(self.ftg2_text)
        file.write('\n')
        file.write(self.strap_text)
        file.write(self.ult_results_out_text)

        file.close()
    
    def add_load_case(self, *args):
        self.load_case_count +=1
        
        count = self.load_case_count
        p1s = self.p1s_case.get()
        p1u = self.p1u_case.get()
        p2s = self.p2s_case.get()
        p2u = self.p2u_case.get()
        dls = self.dls_case.get()
        dlu = self.dlu_case.get()
        
        self.load_case_list.append([count,p1s,p1u,p2s,p2u,dls,dlu])
        
        self.fill_case_list()
        
    def load_case_click(self, *args):
        if self.load_case_listbox.size()==0:
            self.load_clicked = False
            pass
        else:
            self.case_index_click = self.load_case_listbox.curselection()[0]
            count = self.case_index_click + 1
            self.p1s_case.set(self.load_case_list[count-1][1])
            self.p1u_case.set(self.load_case_list[count-1][2])
            self.p2s_case.set(self.load_case_list[count-1][3])
            self.p2u_case.set(self.load_case_list[count-1][4])
            self.dls_case.set(self.load_case_list[count-1][5])
            self.dlu_case.set(self.load_case_list[count-1][6])
            
            self.p1_service_kips.set(self.load_case_list[count-1][1])
            self.p1_ultimate_kips.set(self.load_case_list[count-1][2])
            self.p2_service_kips.set(self.load_case_list[count-1][3])
            self.p2_ultimate_kips.set(self.load_case_list[count-1][4])
            self.dl_service_factor.set(self.load_case_list[count-1][5])
            self.dl_factor.set(self.load_case_list[count-1][6])
            
            self.run_calcs()
            
            if self.load_case_res_listbox.size()==0:
                pass
            else:
                self.load_case_res_listbox.select_clear(0, self.load_case_res_listbox.size() - 1)   #Clear the current selected item
                self.load_case_res_listbox.select_set(self.case_index_click)           #Select the new item
                if self.load_case_res_listbox.yview != self.load_case_listbox.yview():
                    self.load_case_res_listbox.yview_moveto(self.load_case_listbox.yview()[0])                #Set the scrollbar to the selection of the listbox
            
            self.load_clicked = True
    
    def change_load_case(self, *args):
        if self.load_clicked == False or self.load_case_listbox.size()==0:
            pass
        else:
            count = self.case_index_click + 1
            p1s = self.p1s_case.get()
            p1u = self.p1u_case.get()
            p2s = self.p2s_case.get()
            p2u = self.p2u_case.get()
            dls = self.dls_case.get()
            dlu = self.dlu_case.get()
            
            self.load_case_list[count-1] = [count,p1s,p1u,p2s,p2u,dls,dlu]
            
            self.fill_case_list()
        
    def del_load_case(self, *args):
        if self.load_clicked == False or self.load_case_listbox.size()==0:
            pass
        else:
            count = self.case_index_click + 1

            del self.load_case_list[count-1]
            self.load_case_count -=1
            
            i = 1
            for case in self.load_case_list:
                case[0] = i
                i+=1
            
            if len(self.load_case_list) >= 1:
                self.fill_case_list()
            else:
                pass
            
    def fill_case_list(self, *args):
        self.load_case_res_listbox.delete(0,tk.END)
        self.load_case_listbox.delete(0,tk.END)
        
        self.load_case_res_list = []
        
        for case in self.load_case_list:
            string = '{0},{1},{2},{3},{4},{5},{6}'.format(case[0],case[1],case[2],case[3],case[4],case[5],case[6])
            self.load_case_listbox.insert(tk.END,string)
            
            if case[0] % 2 == 0:
                self.load_case_listbox.itemconfigure(case[0]-1, background='pale green')
            else:
                pass
        
    def import_csv(self, *args):
        
        filename = tkFileDialog.askopenfilename()
        
        extension = filename.split('.')[-1]
        
        if filename is None:
            return
        
        elif extension not in ['csv','CSV']:
            tkMessageBox.showerror("ERROR!!","Selected File not a .csv or .CSV file")
            return
        
        else:
            file = open(filename,'r') 
            
            data_raw = file.readlines()

            file.close()
            
            self.load_case_list = []
            
            i = 0
            for line in data_raw:
                data_split = line.split(',')
                data_split[-1] = data_split[-1].rstrip('\n')
                data_split.insert(0,i)
                if i == 0:
                    pass
                else:
                    self.load_case_list.append(data_split)
                    self.load_case_count = i
                
                i+=1
            
            self.fill_case_list()
        
    def run_load_cases(self, *args):
        self.load_case_res_listbox.delete(0,tk.END)
        self.load_case_res_list = []
        
        if len(self.load_case_list) >= 1:
            for case in self.load_case_list:
                p1s = case[1]
                p1u = case[2]
                p2s = case[3]
                p2u = case[4]
                dls = case[5]
                dlu = case[6]
                
                self.p1_service_kips.set(p1s)
                self.p1_ultimate_kips.set(p1u)
                self.p2_service_kips.set(p2s)
                self.p2_ultimate_kips.set(p2u)
                self.dl_service_factor.set(dls)
                self.dl_factor.set(dlu)
                
                self.run_calcs()
                
                
                status_list = [self.status_ftg1_q.get(), self.status_ftg2_q.get(), 
                                self.status_sumv.get(), self.status_summ.get(), 
                                self.status_ftg1v.get(), self.status_ftg1f.get(), 
                                self.status_ftg2v.get(), self.status_ftg2f.get(), 
                                self.status_sv.get(), self.status_sf.get()]
                
                if len(status_list) == sum(status_list):
                    status = 'OK'
                else:
                    status = 'NG'
                
                qal = self.ftg1_qa
                barsl = self.ftg1_bars_text
                qar = self.ftg2_qa
                barsrew = self.ftg2_barsew_text
                barsrns = self.ftg2_barsns_text
                strap_bars = self.strap_bars_text
                
                run_list = [case[0],status,qal,barsl,qar,barsrew,barsrns,strap_bars]
                
                self.load_case_res_list.append(run_list)
            
            for result in self.load_case_res_list:
                string = '{0} -- Qa,left:{1:.2f} ksf - left ftg: {2} -- Qa,right: {3:.2f} ksf - right ftg: {4} E/W - {5} N/S -- Strap Bm: {6}'.format(result[1],result[2],result[3],result[4],result[5],result[6],result[7])
                
                self.load_case_res_listbox.insert(tk.END,string)
                    
                if result[0] % 2 == 0 and result[1]=='OK':
                    self.load_case_res_listbox.itemconfigure(result[0]-1, background='pale green')
                    self.load_case_listbox.itemconfigure(result[0]-1, background='pale green')
                
                elif result[1]=='NG':
                    self.load_case_listbox.itemconfigure(result[0]-1, background='red')
                    self.load_case_res_listbox.itemconfigure(result[0]-1, background='red')
                else:
                    self.load_case_res_listbox.itemconfigure(result[0]-1, background='white')
                    self.load_case_listbox.itemconfigure(result[0]-1, background='white')
        else:
            pass
        
    def save_inputs(self, *args):
        
        out_file = tkFileDialog.asksaveasfile(mode='w', defaultextension=".strapbm")
        
        if out_file is None:
            return
        
        for data in self.inputs:
            text = '{0}\n'.format(data.get())
            out_file.write(text)
        
        out_file.close()
    
    def open_existing(self, *args):
    
        filename = tkFileDialog.askopenfilename()
        
        extension = filename.split('.')[-1]
        
        
        if filename is None:
            return
        elif extension not in ['strapbm']:
            tkMessageBox.showerror("ERROR!!","Selected File not a .strapbm file")
            return
        else:
            calc_file = open(filename,'r')
            calc_data = calc_file.readlines()
            calc_file.close()
            
            i=0
            for line in calc_data:
                value = line.rstrip('\n')
                self.inputs[i].set(value)
                i+=1
        
def main():
    root = tk.Tk()
    root.title("Strap Beam - Alpha")
    main_window(root)
    root.minsize(1280,800)
    root.mainloop()

if __name__ == '__main__':
    main()
