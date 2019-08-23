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
import Tkinter as tk
import ttk
import tkFont
import pin_pin_beam_equations_classes as ppbeam
from numpy import zeros
import numpy as np
import scipy.integrate as sci_int
import math
import os
import webbrowser
import tkMessageBox
import tkFileDialog

class Master_window:

    def __init__(self, master):

        self.master = master

        self.inputs = []

        self.loads_scale = [0.0001]
        self.load_last_add = []

        self.reaction_left = 0
        self.reaction_right = 0

        self.shearl = zeros(501)
        self.shearc = zeros(501)
        self.shearr = zeros(501)

        self.momentl = zeros(501)
        self.momentc = zeros(501)
        self.momentr = zeros(501)

        self.slopel = zeros(501)
        self.slopec = zeros(501)
        self.sloper = zeros(501)

        self.deltal = zeros(501)
        self.deltac = zeros(501)
        self.deltar = zeros(501)

        self.f_size = 10
        helv = tkFont.Font(family='Helvetica',size=self.f_size, weight='bold')
        helv_res = tkFont.Font(family='Helvetica',size=self.f_size, weight='bold', underline = True)

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
        self.main_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.main_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)


        #Beam Canvas
        self.beam_canvas_frame = tk.Frame(self.main_frame, bd=2, relief='sunken', padx=1,pady=1)
        self.bm_canvas = tk.Canvas(self.beam_canvas_frame, width=750, height=200, bd=2, relief='sunken', background="black")
        self.bm_canvas.bind("<Configure>", self.bm_canvas_draw)
        self.bm_canvas.bind("<Button-1>", self.draw_static_beam_mouse)
        self.bm_canvas.bind("<B1-Motion>", self.draw_static_beam_mouse)
        self.bm_canvas.pack(side = tk.LEFT, anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        self.val_at_x = self.bm_canvas.create_line(0, 0,0,0,fill="gray90", width=1, dash=(4,4))
        self.val_at_x_text = self.bm_canvas.create_line(0, 0,0,0,fill="gray90", width=1, dash=(4,4))

        self.beam_canvas_frame.pack(side=tk.TOP, anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        self.graph_b_frame = tk.Frame(self.beam_canvas_frame, bd=2, relief='sunken', padx=4 ,pady=1)

        self.show_l = tk.IntVar()
        self.show_l.set(1)
        tk.Checkbutton(self.graph_b_frame, text=' : Show Loads', variable=self.show_l, command = self.bm_canvas_draw, font=helv).grid(row=1, column=1, sticky = tk.W)
        self.show_v = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show V', variable=self.show_v, command = self.bm_canvas_draw, font=helv).grid(row=2, column=1, sticky = tk.W)
        self.show_m = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show M', variable=self.show_m, command = self.bm_canvas_draw, font=helv).grid(row=3, column=1, sticky = tk.W)
        self.show_s = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show S', variable=self.show_s, command = self.bm_canvas_draw, font=helv).grid(row=4, column=1, sticky = tk.W)
        self.show_d = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show D', variable=self.show_d, command = self.bm_canvas_draw, font=helv).grid(row=5, column=1, sticky = tk.W)
        self.show_r = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show Reactions', variable=self.show_r, command = self.bm_canvas_draw, font=helv).grid(row=6, column=1, sticky = tk.W)
        self.show_stations = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show Stations', variable=self.show_stations, command = self.bm_canvas_draw, font=helv).grid(row=7, column=1, sticky = tk.W)
        self.show_m_tension = tk.IntVar()
        self.show_m_tension.set(1)
        tk.Checkbutton(self.graph_b_frame, text=' : Show M on\ntension face', variable=self.show_m_tension, command = self.bm_canvas_draw, font=helv).grid(row=8, column=1, sticky = tk.W)

        self.graph_b_frame.pack(side=tk.RIGHT, anchor='e')

        self.nb = ttk.Notebook(self.main_frame)
        self.nb.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        #Tab 1 - Span Data
        self.page1 = ttk.Frame(self.nb)
        self.nb.add(self.page1, text='Span Information')

        self.pg1_frame = tk.Frame(self.page1, bd=2, relief='sunken', padx=1,pady=1)

        self.bm_info_frame = tk.Frame(self.pg1_frame, bd=2, relief='sunken', padx=2,pady=1)

        tk.Label(self.bm_info_frame, text="Left Cantilever (m):", font=helv).grid(row=1,column=1, sticky = tk.E)
        tk.Label(self.bm_info_frame, text="Center Span (m):", font=helv).grid(row=2,column=1, sticky = tk.E)
        tk.Label(self.bm_info_frame, text="Right Cantilever (m):", font=helv).grid(row=3,column=1, sticky = tk.E)

        self.left_cant_ft = tk.StringVar()
        self.inputs.append(self.left_cant_ft)
        self.span_ft = tk.StringVar()
        self.inputs.append(self.span_ft)
        self.right_cant_ft = tk.StringVar()
        self.inputs.append(self.right_cant_ft)

        self.left_cant_ft.set(0.0)
        self.span_ft.set(10.0)
        self.right_cant_ft.set(0.0)

        self.left_cant_entry = tk.Entry(self.bm_info_frame, textvariable=self.left_cant_ft, width=10)
        self.left_cant_entry.grid(row=1,column=2, sticky = tk.W)
        self.span_entry = tk.Entry(self.bm_info_frame, textvariable=self.span_ft, width=10)
        self.span_entry.grid(row=2,column=2, sticky = tk.W)
        self.right_cant_entry = tk.Entry(self.bm_info_frame, textvariable=self.right_cant_ft, width=10)
        self.right_cant_entry.grid(row=3,column=2, sticky = tk.W)

        tk.Label(self.bm_info_frame, text="E (Mpa):", font=helv).grid(row=4,column=1, sticky = tk.E)
        tk.Label(self.bm_info_frame, text="I (mm^4):", font=helv).grid(row=5,column=1, sticky = tk.E)

        self.E_ksi = tk.StringVar()
        self.inputs.append(self.E_ksi)
        self.I_in4 = tk.StringVar()
        self.inputs.append(self.I_in4)

        self.E_ksi.set(199948)
        self.I_in4.set(1.28199e7)

        self.E_entry = tk.Entry(self.bm_info_frame, textvariable=self.E_ksi, width=10)
        self.E_entry.grid(row=4,column=2, sticky = tk.W)
        self.I_entry = tk.Entry(self.bm_info_frame, textvariable=self.I_in4, width=10)
        self.I_entry.grid(row=5,column=2, sticky = tk.W)


        tk.Label(self.bm_info_frame, text="Stations:", font=helv).grid(row=6,column=1, sticky = tk.E)
        self.stations = tk.StringVar()
        self.inputs.append(self.stations)
        self.stations_sb= tk.Spinbox(self.bm_info_frame, values=(4, 10, 20, 25, 50, 100, 200, 500, 1000), textvariable=self.stations, command=self.run)
        self.stations_sb.grid(row=6, column=2)


        self.b_run = tk.Button(self.bm_info_frame,text = "Update", command = self.update, font=helv)
        self.b_run.grid(row=1,column=3, sticky = tk.W)

        self.bm_info_frame.pack(side=tk.LEFT, anchor='nw', padx=4 ,pady=1)

        self.res_frame = tk.Frame(self.pg1_frame, bd=2, relief='sunken', padx=4 ,pady=1)

        self.res_labels = []
        self.res_list = ['Results:','--','--','Cant. Left:','--','--','--','--','Center Span:','--','--','--','--','Cant. Right:','--','--','--','--']
        label_fonts = [helv_res,helv,helv,helv_res,helv,helv,helv,helv,helv_res,helv,helv,helv,helv,helv_res,helv,helv,helv,helv]
        for i in range(0,18):
            self.res_labels.append(tk.Label(self.res_frame, text= self.res_list[i], font=label_fonts[i]))
            self.res_labels[i].grid(row=i+1,column=1, sticky = tk.W)

        self.resx_label = tk.Label(self.res_frame, text="x = ", font=helv)
        self.resx_label.grid(row=1,column=2)
        self.resx_var = tk.StringVar()
        self.resx_var.set(1.0)
        self.resx_entry = tk.Entry(self.res_frame, textvariable = self.resx_var, width=10)
        self.resx_entry.grid(row=1, column=3)
        tk.Label(self.res_frame, text = ' ft', font=helv).grid(row=1, column=4)

        self.b_runx = tk.Button(self.res_frame, text="Res. @ X", command = self.runx, font=helv)
        self.b_runx.grid(row=1, column=4)

        self.resx_labels = []
        self.resx_list = ['Results @ x :','Cant. Left:','--','--','--','--','Center Span:','--','--','--','--','Cant. Right:','--','--','--','--']
        label_fontsx = [helv_res,helv_res,helv,helv,helv,helv,helv_res,helv,helv,helv,helv,helv_res,helv,helv,helv,helv]
        for i in range(0,16):
            self.resx_labels.append(tk.Label(self.res_frame, text= self.resx_list[i], font=label_fontsx[i]))
            self.resx_labels[i].grid(row=i+2,column=3, sticky = tk.W)

        self.res_frame.pack(side=tk.LEFT, anchor='nw', padx=4 ,pady=1)

        self.res_calc_multi_frame = tk.Frame(self.pg1_frame, bd=2, relief='sunken', padx=4 ,pady=1)

        self.fixed_left = tk.IntVar()
        self.inputs.append(self.fixed_left)
        self.fixed_left_check = tk.Checkbutton(self.res_calc_multi_frame , text=' : Fixed Left', variable=self.fixed_left, font=helv)
        self.fixed_left_check.grid(row=0, column=0, sticky = tk.W)

        self.fixed_right = tk.IntVar()
        self.inputs.append(self.fixed_right)
        self.fixed_right_check = tk.Checkbutton(self.res_calc_multi_frame , text=' : Fixed Right', variable=self.fixed_right, font=helv)
        self.fixed_right_check.grid(row=0, column=2, sticky = tk.W)

        tk.Label(self.res_calc_multi_frame, text = 'Support Locations (m):\nex. 10,20,30,...,Xi', font=helv).grid(row=1, column=0, columnspan= 3)
        self.internal_supports = tk.StringVar()
        self.inputs.append(self.internal_supports)
        tk.Entry(self.res_calc_multi_frame, textvariable = self.internal_supports, width=40).grid(row=2, column=0, columnspan= 3)

        self.b_solve_multi = tk.Button(self.res_calc_multi_frame, text='Solve Fixed End and Interior Reactions', command = self.multi_solve, font=helv)
        self.b_solve_multi.grid(row=3, column=0, columnspan= 3)

        self.multi_result_label = tk.Label(self.res_calc_multi_frame, text = 'Mo = --\nML = --', font=helv)
        self.multi_result_label.grid(row=4, column=0, columnspan= 3)

        self.b_moment_area = tk.Button(self.res_calc_multi_frame, text="Area of Moment Curve and Centroid", command = self.moment_area, font=helv)
        self.b_moment_area.grid(row=5, column=0, columnspan=3)

        self.moment_area_label = tk.Label(self.res_calc_multi_frame, text= '-- kN*m\n-- kN*m', font=helv_res)
        self.moment_area_label.grid(row=6, column=0, columnspan=3)

        self.res_calc_multi_frame.pack(side=tk.LEFT, anchor='nw', padx=4 ,pady=1)

        self.pg1_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        #Tab 2 - Loads
        self.page2 = ttk.Frame(self.nb)
        self.nb.add(self.page2, text='Loads')

        self.pg2_frame = tk.Frame(self.page2, bd=2, relief='sunken', padx=1,pady=1)

        self.add_loads_frame = tk.Frame(self.pg2_frame, bd=2, relief='sunken', padx=4,pady=4)

        tk.Label(self.add_loads_frame, text="Add Loads:", font=helv).grid(row=1,column=1, sticky = tk.W)
        tk.Label(self.add_loads_frame, text="P,M,W1\n(kN, kN*m, kN/m):", font=helv).grid(row=2,column=1, sticky = tk.W)
        tk.Label(self.add_loads_frame, text="W2\n(kN/m):", font=helv).grid(row=2,column=2, sticky = tk.W)
        tk.Label(self.add_loads_frame, text="a (m):", font=helv).grid(row=2,column=3, sticky = tk.W)
        tk.Label(self.add_loads_frame, text="b (m):", font=helv).grid(row=2,column=4, sticky = tk.W)
        tk.Label(self.add_loads_frame, text="Load Type:", font=helv).grid(row=2,column=5, sticky = tk.W)
        tk.Label(self.add_loads_frame, text="Load Location:", font=helv).grid(row=2,column=6, sticky = tk.W)

        self.w1_gui = tk.StringVar()
        self.w2_gui = tk.StringVar()
        self.a_gui = tk.StringVar()
        self.b_gui = tk.StringVar()

        self.w1_gui.set(0)
        self.w2_gui.set(0)
        self.a_gui.set(0)
        self.b_gui.set(0)

        self.w1_gui_entry = tk.Entry(self.add_loads_frame, textvariable=self.w1_gui, width=10)
        self.w1_gui_entry.grid(row=3,column=1, sticky = tk.W)
        self.w2_gui_entry = tk.Entry(self.add_loads_frame, textvariable=self.w2_gui, width=10)
        self.w2_gui_entry.grid(row=3,column=2, sticky = tk.W)
        self.a_gui_entry = tk.Entry(self.add_loads_frame, textvariable=self.a_gui, width=10)
        self.a_gui_entry.grid(row=3,column=3, sticky = tk.W)
        self.b_gui_entry = tk.Entry(self.add_loads_frame, textvariable=self.b_gui, width=10)
        self.b_gui_entry.grid(row=3,column=4, sticky = tk.W)
        self.load_type = tk.StringVar()
        self.load_type.set('Point')
        load_types = ['Point','Moment','UDL','TRAP']
        self.load_type_selection = tk.OptionMenu(self.add_loads_frame, self.load_type, *load_types)
        self.load_type_selection.grid(row=3,column=5, sticky = tk.W)

        self.load_loc = tk.StringVar()
        self.load_loc.set('Center')
        load_locals = ['Left','Center','Right']
        self.load_loc_selection = tk.OptionMenu(self.add_loads_frame, self.load_loc, *load_locals)
        self.load_loc_selection.grid(row=3,column=6, sticky = tk.W)

        self.b_add_load = tk.Button(self.add_loads_frame,text = "Add New Load", command = self.add_load, font=helv)
        self.b_add_load.grid(row=3, column=7, sticky = tk.W)

        self.b_remove_load = tk.Button(self.add_loads_frame,text = "Remove Unchecked Loads", command = self.remove_load, font=helv)
        self.b_remove_load.grid(row=3, column=8, sticky = tk.W)

        self.add_loads_frame.pack(anchor="nw", padx= 4, pady= 4)

        self.loads_scroll_frame = tk.Frame(self.pg2_frame, bd=2, relief='sunken', padx=4,pady=4)
        self.loads_scrollbar = tk.Scrollbar(self.loads_scroll_frame, orient="vertical")
        self.loads_canvas = tk.Canvas(self.loads_scroll_frame, bd=1, scrollregion=(0,0,100,100))

        self.loads_frame = tk.Frame(self.loads_canvas, bd=2, relief='sunken', padx=4,pady=4)

        self.loads_gui_select_var = []
        self.loads_gui = []

        tk.Label(self.loads_frame, text="Use/Delete", font=helv_res).grid(row=0, column=1)
        tk.Label(self.loads_frame, text="P, M, or w1 (kN/m)", font=helv_res).grid(row=0, column=2)
        tk.Label(self.loads_frame, text="w2 (kN/m)", font=helv_res).grid(row=0, column=3)
        tk.Label(self.loads_frame, text="a (m)", font=helv_res).grid(row=0, column=4)
        tk.Label(self.loads_frame, text="b (m)", font=helv_res).grid(row=0, column=5)
        tk.Label(self.loads_frame, text="Span", font=helv_res).grid(row=0, column=6)
        tk.Label(self.loads_frame, text="Type", font=helv_res).grid(row=0, column=7)

        self.loads_frame.pack(anchor="nw", fill=tk.BOTH, expand=1)

        self.loads_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.loads_scrollbar.pack(side=tk.LEFT, fill=tk.Y, expand=tk.FALSE)
        self.loads_scroll_frame.pack(anchor="nw", padx= 4, pady= 4, fill=tk.BOTH, expand=1)

        self.loads_canvas.configure(yscrollcommand=self.loads_scrollbar.set)
        self.loads_scrollbar.configure(command=self.loads_canvas.yview)
        self.loads_canvas.create_window(0,0,window=self.loads_frame, anchor=tk.NW)
        self.loads_canvas.configure(scrollregion=(0,0,1000,1000))

        self.loads_frame.bind("<Configure>", self.ScrollFrameConfig)

        self.pg2_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        #Tab 3 - Detailed Results
        self.page3 = ttk.Frame(self.nb)
        self.nb.add(self.page3, text='Detailed Results')

        self.pg3_frame = tk.Frame(self.page3, bd=2, relief='sunken', padx=1,pady=1)

        self.nb_res = ttk.Notebook(self.pg3_frame)

        self.nb_res.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        self.l_res_tab = ttk.Frame(self.nb_res)
        self.nb_res.add(self.l_res_tab, text='Left Results')

        self.res_l_frame = tk.Frame(self.l_res_tab, bd=2, relief='sunken', padx=1,pady=1)
        tk.Label(self.res_l_frame, text="X (m)", font=helv_res).grid(row=0, column=1)
        tk.Label(self.res_l_frame, text="V (kN)", font=helv_res).grid(row=0, column=2)
        tk.Label(self.res_l_frame, text="M (kN*m)", font=helv_res).grid(row=0, column=3)
        tk.Label(self.res_l_frame, text="S (Rad)", font=helv_res).grid(row=0, column=4)
        tk.Label(self.res_l_frame, text="D (mm)", font=helv_res).grid(row=0, column=5)

        self.results_scrollbar_l = tk.Scrollbar(self.res_l_frame, orient="vertical", command=self.det_res_scroll_l)
        self.results_scrollbar_l.grid(row=1, column=6, sticky=tk.NS)

        self.xl_listbox = tk.Listbox(self.res_l_frame, height = 20, width = 16, font=helv, yscrollcommand=self.results_scrollbar_l.set)
        self.xl_listbox.grid(row=1, column=1)
        self.lv_listbox = tk.Listbox(self.res_l_frame, height = 20, width = 16, font=helv, yscrollcommand=self.results_scrollbar_l.set)
        self.lv_listbox.grid(row=1, column=2)
        self.lm_listbox = tk.Listbox(self.res_l_frame, height = 20, width = 16, font=helv, yscrollcommand=self.results_scrollbar_l.set)
        self.lm_listbox.grid(row=1, column=3)
        self.ls_listbox = tk.Listbox(self.res_l_frame, height = 20, width = 16, font=helv, yscrollcommand=self.results_scrollbar_l.set)
        self.ls_listbox.grid(row=1, column=4)
        self.ld_listbox = tk.Listbox(self.res_l_frame, height = 20, width = 16, font=helv, yscrollcommand=self.results_scrollbar_l.set)
        self.ld_listbox.grid(row=1, column=5)

        self.res_l_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        self.c_res_tab = ttk.Frame(self.nb_res)
        self.nb_res.add(self.c_res_tab, text='Center Results')

        self.res_c_frame = tk.Frame(self.c_res_tab, bd=2, relief='sunken', padx=1,pady=1)
        tk.Label(self.res_c_frame, text="X (m)", font=helv_res).grid(row=0, column=1)
        tk.Label(self.res_c_frame, text="V (kN)", font=helv_res).grid(row=0, column=2)
        tk.Label(self.res_c_frame, text="M (kN*m)", font=helv_res).grid(row=0, column=3)
        tk.Label(self.res_c_frame, text="S (Rad)", font=helv_res).grid(row=0, column=4)
        tk.Label(self.res_c_frame, text="D (mm)", font=helv_res).grid(row=0, column=5)

        self.results_scrollbar = tk.Scrollbar(self.res_c_frame, orient="vertical", command=self.det_res_scroll)
        self.results_scrollbar.grid(row=1, column=6, sticky=tk.NS)

        self.xc_listbox = tk.Listbox(self.res_c_frame, height = 30, width = 16, font=helv, yscrollcommand=self.results_scrollbar.set)
        self.xc_listbox.grid(row=1, column=1)
        self.cv_listbox = tk.Listbox(self.res_c_frame, height = 30, width = 16, font=helv, yscrollcommand=self.results_scrollbar.set)
        self.cv_listbox.grid(row=1, column=2)
        self.cm_listbox = tk.Listbox(self.res_c_frame, height = 30, width = 16, font=helv, yscrollcommand=self.results_scrollbar.set)
        self.cm_listbox.grid(row=1, column=3)
        self.cs_listbox = tk.Listbox(self.res_c_frame, height = 30, width = 16, font=helv, yscrollcommand=self.results_scrollbar.set)
        self.cs_listbox.grid(row=1, column=4)
        self.cd_listbox = tk.Listbox(self.res_c_frame, height = 30, width = 16, font=helv, yscrollcommand=self.results_scrollbar.set)
        self.cd_listbox.grid(row=1, column=5)

        self.res_c_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        self.r_res_tab = ttk.Frame(self.nb_res)
        self.nb_res.add(self.r_res_tab, text='Right Results')

        self.res_r_frame = tk.Frame(self.r_res_tab, bd=2, relief='sunken', padx=1,pady=1)
        tk.Label(self.res_r_frame, text="X (m)", font=helv_res).grid(row=0, column=1)
        tk.Label(self.res_r_frame, text="V (kN)", font=helv_res).grid(row=0, column=2)
        tk.Label(self.res_r_frame, text="M (kN*m)", font=helv_res).grid(row=0, column=3)
        tk.Label(self.res_r_frame, text="S (Rad)", font=helv_res).grid(row=0, column=4)
        tk.Label(self.res_r_frame, text="D (mm)", font=helv_res).grid(row=0, column=5)

        self.results_scrollbar_r = tk.Scrollbar(self.res_r_frame, orient="vertical", command=self.det_res_scroll_r)
        self.results_scrollbar_r.grid(row=1, column=6, sticky=tk.NS)

        self.xr_listbox = tk.Listbox(self.res_r_frame, height = 30, width = 16, font=helv, yscrollcommand=self.results_scrollbar_r.set)
        self.xr_listbox.grid(row=1, column=1)
        self.rv_listbox = tk.Listbox(self.res_r_frame, height = 30, width = 16, font=helv, yscrollcommand=self.results_scrollbar_r.set)
        self.rv_listbox.grid(row=1, column=2)
        self.rm_listbox = tk.Listbox(self.res_r_frame, height = 30, width = 16, font=helv, yscrollcommand=self.results_scrollbar_r.set)
        self.rm_listbox.grid(row=1, column=3)
        self.rs_listbox = tk.Listbox(self.res_r_frame, height = 30, width = 16, font=helv, yscrollcommand=self.results_scrollbar_r.set)
        self.rs_listbox.grid(row=1, column=4)
        self.rd_listbox = tk.Listbox(self.res_r_frame, height = 30, width = 16, font=helv, yscrollcommand=self.results_scrollbar_r.set)
        self.rd_listbox.grid(row=1, column=5)

        self.res_r_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        self.pg3_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        #Tab 4 - Piecewise Beam Functions
        self.page4 = ttk.Frame(self.nb)
        self.nb.add(self.page4, text='Center Span - Piecewise Beam Functions')

        self.pg4_frame = tk.Frame(self.page4, bd=2, relief='sunken', padx=1,pady=1)

        self.pfunc_frame = tk.Frame(self.pg4_frame, bd=2, relief='sunken', padx=1,pady=1)
        self.pfunc_text_box = tk.Text(self.pfunc_frame, bg= "grey90", font= helv, wrap=tk.WORD)
        self.pfunc_text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.pfunc_scroll = tk.Scrollbar(self.pfunc_frame, command=self.pfunc_text_box.yview)
        self.pfunc_scroll.pack(side=tk.LEFT, fill=tk.Y)

        self.pfunc_text_box['yscrollcommand'] = self.pfunc_scroll.set

        self.pfunc_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        self.pg4_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        #self.b_export_pdf = tk.Button(self.base_frame,text="Export PDF", command=self.export_pdf, font=helv)
        #self.b_export_pdf.pack(side=tk.RIGHT)
        self.b_export_html = tk.Button(self.base_frame,text="Export HTML", command=self.write_html_results, font=helv)
        self.b_export_html.pack(side=tk.RIGHT)
        self.b_quit = tk.Button(self.base_frame,text="Quit", command=self.quit_app, font=helv)
        self.b_quit.pack(side=tk.RIGHT)

        self.loads_left = []
        self.loads_center = []
        self.loads_right = []

        self.has_run = 0

        self.build_loads()
        self.run()

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

    def ScrollFrameConfig(self, *event):
        self.loads_canvas.configure(scrollregion=self.loads_canvas.bbox("all"))

    def quit_app(self):
        self.master.destroy()
        self.master.quit()

    def bm_canvas_draw(self,*event):
        if self.left_cant_ft.get() == '' or self.span_ft.get()== '' or self.right_cant_ft.get() == '':
            pass

        else:
            self.bm_canvas.delete("all")
            w = self.bm_canvas.winfo_width()
            h = self.bm_canvas.winfo_height()
            hg = (h/2.0)

            ll = float(self.left_cant_ft.get())
            lc = float(self.span_ft.get())
            lr = float(self.right_cant_ft.get())

            initial = 50

            sf = (w-(2*initial)) / (ll+lc+lr)

            self.canvas_scale_x = sf

            l = (w-(2*initial)) + initial
            s1 = (sf * ll) + initial
            s2 = ((ll+lc) * sf) + initial

            self.bm_canvas.create_line(initial, h/2, l, h/2, fill="white", width=2)
            self.bm_canvas.create_line(s1, h/2, (s1+20), (h/2)+20, (s1-20), (h/2)+20,s1, h/2, fill="white", width=2)
            self.bm_canvas.create_line(s2, h/2, (s2+20), (h/2)+20, (s2-20), (h/2)+20,s2, h/2, fill="white", width=2)

            if self.show_l.get() == 1:

                loads_sf = (hg - 10) / max(max(self.loads_scale), abs(min(self.loads_scale)))

                for load in self.loads_left:
                    x,y = load.chart_load(sf,loads_sf,1)
                    for i in range(1,len(x)):
                        self.bm_canvas.create_line((x[i-1])+initial,hg - (y[i-1]),(x[i])+initial,hg - (y[i]), fill = "blue", width=2)

                for load in self.loads_center:
                    x,y = load.chart_load(sf,loads_sf,1)
                    for i in range(1,len(x)):
                        self.bm_canvas.create_line(((x[i-1] + (ll*sf)))+initial,hg - (y[i-1]),(x[i]+(ll* sf))+initial,hg - (y[i]), fill = "blue", width=2)

                for load in self.loads_right:
                    x,y = load.chart_load(sf,loads_sf,1)
                    for i in range(1,len(x)):
                        self.bm_canvas.create_line((x[i-1]+((ll+lc)* sf))+initial,hg - (y[i-1]),(x[i]+((ll+lc)* sf))+initial,hg - (y[i]), fill = "blue", width=2)

            if self.has_run == 1:
                xl = self.xsl
                xc = self.xsc
                xr = self.xsr
            else:
                pass

            if self.show_v.get() == 1:

                if max(max(max(self.shearc), max(self.shearl), max(self.shearr)), abs(min(min(self.shearc), min(self.shearl), min(self.shearr)))) == 0:
                    v_sf = (hg - 10)
                else:
                    v_sf = (hg - 10) / max(max(max(self.shearc), max(self.shearl), max(self.shearr)), abs(min(min(self.shearc), min(self.shearl), min(self.shearr))))

                self.bm_canvas.create_line((xl[-1] * sf) + initial, hg - (self.shearl[-1] * v_sf),(xc[0] * sf) + initial,hg - (self.shearc[0] * v_sf),fill="red", width=2)
                self.bm_canvas.create_line((xc[-1] * sf) + initial, hg - (self.shearc[-1] * v_sf),(xr[0] * sf) + initial,hg - (self.shearr[0] * v_sf),fill="red", width=2)

                for i in range(1,len(self.shearc)):
                    self.bm_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.shearl[i-1] * v_sf),(xl[i] * sf) + initial,hg - (self.shearl[i] * v_sf),fill="red", width=2)
                    self.bm_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.shearc[i-1] * v_sf),(xc[i] * sf) + initial,hg - (self.shearc[i] * v_sf),fill="red", width=2)
                    self.bm_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.shearr[i-1] * v_sf),(xr[i] * sf) + initial,hg - (self.shearr[i] * v_sf),fill="red", width=2)

                    if self.show_stations.get() == 1:
                        self.bm_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.shearl[i-1] * v_sf),(xl[i-1] * sf) + initial,hg,fill="red3", width=1)
                        self.bm_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.shearc[i-1] * v_sf),(xc[i-1] * sf) + initial,hg,fill="red3", width=1)
                        self.bm_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.shearr[i-1] * v_sf),(xr[i-1] * sf) + initial,hg,fill="red3", width=1)

            if self.show_m.get() == 1:
                if self.show_m_tension.get() == 1:
                    m_factor = -1.0
                else:
                    m_factor = 1.0

                if max(max(max(self.momentc),max(self.momentl),max(self.momentr)), abs(min(min(self.momentc),min(self.momentl),min(self.momentr)))) == 0:
                    m_sf = ((hg - 10))*m_factor
                else:
                    m_sf = ((hg - 10) / max(max(max(self.momentc),max(self.momentl),max(self.momentr)), abs(min(min(self.momentc),min(self.momentl),min(self.momentr)))))*m_factor

                for i in range(1,len(self.momentc)):
                    self.bm_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.momentl[i-1] * m_sf),(xl[i] * sf) + initial,hg - (self.momentl[i] * m_sf),fill="green", width=2)
                    self.bm_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.momentc[i-1] * m_sf),(xc[i] * sf) + initial,hg - (self.momentc[i] * m_sf),fill="green", width=2)
                    self.bm_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.momentr[i-1] * m_sf),(xr[i] * sf) + initial,hg - (self.momentr[i] * m_sf),fill="green", width=2)

                    if self.show_stations.get() == 1:
                        self.bm_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.momentl[i-1] * m_sf),(xl[i-1] * sf) + initial,hg,fill="PaleGreen3", width=1)
                        self.bm_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.momentc[i-1] * m_sf),(xc[i-1] * sf) + initial,hg,fill="PaleGreen3", width=1)
                        self.bm_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.momentr[i-1] * m_sf),(xr[i-1] * sf) + initial,hg,fill="PaleGreen3", width=1)

            if self.show_s.get() == 1:

                if max(max(max(self.slopec),max(self.slopel),max(self.sloper)), abs(min(min(self.slopec),min(self.slopel),min(self.sloper)))) == 0:
                    s_sf = (hg - 10)
                else:
                    s_sf = (hg - 10) / max(max(max(self.slopec),max(self.slopel),max(self.sloper)), abs(min(min(self.slopec),min(self.slopel),min(self.sloper))))

                for i in range(1,len(self.slopec)):
                    self.bm_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.slopel[i-1] * s_sf),(xl[i] * sf) + initial,hg - (self.slopel[i] * s_sf),fill="magenta", width=2)
                    self.bm_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.slopec[i-1] * s_sf),(xc[i] * sf) + initial,hg - (self.slopec[i] * s_sf),fill="magenta", width=2)
                    self.bm_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.sloper[i-1] * s_sf),(xr[i] * sf) + initial,hg - (self.sloper[i] * s_sf),fill="magenta", width=2)

                    if self.show_stations.get() == 1:
                        self.bm_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.slopel[i-1] * s_sf),(xl[i-1] * sf) + initial,hg,fill="orchid2", width=1)
                        self.bm_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.slopec[i-1] * s_sf),(xc[i-1] * sf) + initial,hg,fill="orchid2", width=1)
                        self.bm_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.sloper[i-1] * s_sf),(xr[i-1] * sf) + initial,hg,fill="orchid2", width=1)

            if self.show_d.get() == 1:

                if max(max(max(self.deltac),max(self.deltal),max(self.deltar)), abs(min(min(self.deltac),min(self.deltal),min(self.deltar)))) == 0:
                    d_sf = (hg - 10)
                else:
                    d_sf = (hg - 10) / max(max(max(self.deltac),max(self.deltal),max(self.deltar)), abs(min(min(self.deltac),min(self.deltal),min(self.deltar))))

                for i in range(1,len(self.deltac)):
                    self.bm_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.deltal[i-1] * d_sf),(xl[i] * sf) + initial,hg - (self.deltal[i] * d_sf),fill="grey", width=2)
                    self.bm_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.deltac[i-1] * d_sf),(xc[i] * sf) + initial,hg - (self.deltac[i] * d_sf),fill="grey", width=2)
                    self.bm_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.deltar[i-1] * d_sf),(xr[i] * sf) + initial,hg - (self.deltar[i] * d_sf),fill="grey", width=2)

                    if self.show_stations.get() == 1:
                        self.bm_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.deltal[i-1] * d_sf),(xl[i-1] * sf) + initial,hg,fill="light grey", width=1)
                        self.bm_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.deltac[i-1] * d_sf),(xc[i-1] * sf) + initial,hg,fill="light grey", width=1)
                        self.bm_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.deltar[i-1] * d_sf),(xr[i-1] * sf) + initial,hg,fill="light grey", width=1)

            if self.show_r.get() == 1:

                if max(max(max(self.rly),max(self.rry)), abs(min(min(self.rlx),min(self.rly)))) == 0:
                    r_sf = (hg - 10)
                else:
                    r_sf = (hg - 10) / max(max(max(self.rly),max(self.rry)), abs(min(min(self.rlx),min(self.rly))))

                for i in range(1,len(self.rlx)):
                    self.bm_canvas.create_line((self.rlx[i-1] * sf) + initial, hg - (self.rly[i-1] * r_sf),(self.rlx[i] * sf) + initial,hg - (self.rly[i] * r_sf),fill="light blue", width=2)
                    self.bm_canvas.create_line((self.rrx[i-1] * sf) + initial, hg - (self.rry[i-1] * r_sf),(self.rrx[i] * sf) + initial,hg - (self.rry[i] * r_sf),fill="light blue", width=2)

    def det_res_scroll(self, *args):
        self.xc_listbox.yview(*args)
        self.cv_listbox.yview(*args)
        self.cm_listbox.yview(*args)
        self.cs_listbox.yview(*args)
        self.cd_listbox.yview(*args)

    def det_res_scroll_l(self, *args):
        self.xl_listbox.yview(*args)
        self.lv_listbox.yview(*args)
        self.lm_listbox.yview(*args)
        self.ls_listbox.yview(*args)
        self.ld_listbox.yview(*args)

    def det_res_scroll_r(self, *args):
        self.xr_listbox.yview(*args)
        self.rv_listbox.yview(*args)
        self.rm_listbox.yview(*args)
        self.rs_listbox.yview(*args)
        self.rd_listbox.yview(*args)

    def build_loads(self, *event):

        del self.loads_right[:]
        del self.loads_left[:]
        del self.loads_center[:]

        ll = float(self.left_cant_ft.get())
        lc = float(self.span_ft.get())
        lr = float(self.right_cant_ft.get())

        self.extra_l_station = np.array([0])
        self.extra_c_station = np.array([0])
        self.extra_r_station = np.array([0])


        for load in self.loads_gui_select_var:

            if load[0].get() == 0:

                pass

            else:

                w1 = float(load[1].get())
                w2 = float(load[2].get())
                a = float(load[3].get())
                b = float(load[4].get())
                load_location = load[5].get()
                load_type = load[6].get()

                if load_type == 'Moment':
                    self.loads_scale.append(w1/2.0)
                    self.loads_scale.append(w2)
                else:
                    self.loads_scale.append(w1)
                    self.loads_scale.append(w2)

                #['Left','Center','Right']
                if load_location == 'Left':
                    #['Point','Moment','UDL','TRAP']

                    if load_type == 'Point':
                        self.loads_left.append(ppbeam.cant_left_point(w1,a,ll,lc))
                        b = min(ll,a + 0.0001)
                        c = max(0,a - 0.0001)
                        self.extra_l_station = np.append(self.extra_l_station, [c,a,b])

                    elif load_type == 'Moment':
                        self.loads_left.append(ppbeam.cant_left_point_moment(w1,a,ll,lc))
                        b = min(ll,a + 0.0001)
                        c = max(0,a - 0.0001)
                        self.extra_l_station = np.append(self.extra_l_station, [c,a,b])

                    elif load_type == 'UDL':
                        self.loads_left.append(ppbeam.cant_left_udl(w1,a,b,ll,lc))
                        self.extra_l_station = np.append(self.extra_l_station, [a,b])

                    elif load_type == 'TRAP':
                        self.loads_left.append(ppbeam.cant_left_trap(w1,w2,a,b,ll,lc))
                        self.extra_l_station = np.append(self.extra_l_station, [a,b])
                    else:
                        pass

                elif load_location == 'Center':
                    #['Point','Moment','UDL','TRAP']
                    if load_type == 'Point':
                        self.loads_center.append(ppbeam.pl(w1,a,lc))
                        b = min(lc,a + 0.0001)
                        c = max(0,a - 0.0001)
                        self.extra_c_station = np.append(self.extra_c_station, [c,a,b])

                    elif load_type == 'Moment':
                        self.loads_center.append(ppbeam.point_moment(w1,a,lc))
                        b = min(lc,a + 0.0001)
                        c = max(0,a - 0.0001)
                        self.extra_c_station = np.append(self.extra_c_station, [c,a,b])

                    elif load_type == 'UDL':
                        self.loads_center.append(ppbeam.udl(w1,a,b,lc))
                        self.extra_c_station = np.append(self.extra_c_station, [a,b])

                    elif load_type == 'TRAP':
                        self.loads_center.append(ppbeam.trap(w1,w2,a,b,lc))
                        self.extra_c_station = np.append(self.extra_c_station, [a,b])

                    else:
                        pass

                elif load_location == 'Right':
                    #['Point','Moment','UDL','TRAP']
                    if load_type == 'Point':
                        self.loads_right.append(ppbeam.cant_right_point(w1,a,lr,lc))
                        b = min(lr,a + 0.0001)
                        c = max(0,a - 0.0001)
                        self.extra_r_station = np.append(self.extra_r_station, [c,a,b])

                    elif load_type == 'Moment':
                        self.loads_right.append(ppbeam.cant_right_point_moment(w1,a,lr,lc))
                        b = min(lr,a + 0.0001)
                        c = max(0,a - 0.0001)
                        self.extra_r_station = np.append(self.extra_r_station, [c,a,b])

                    elif load_type == 'UDL':
                        self.loads_right.append(ppbeam.cant_right_udl(w1,a,b,lr,lc))
                        self.extra_r_station = np.append(self.extra_r_station, [a,b])

                    elif load_type == 'TRAP':
                        self.loads_right.append(ppbeam.cant_right_trap(w1,w2,a,b,lr,lc))
                        self.extra_r_station = np.append(self.extra_r_station, [a,b])

                    else:
                        pass

                else:
                    pass

        self.extra_l_station = np.unique(self.extra_l_station)
        self.extra_c_station = np.unique(self.extra_c_station)
        self.extra_r_station = np.unique(self.extra_r_station)

        self.run()
        self.bm_canvas_draw()

    def build_loads_gui(self, *event):
        #Destroy all the individual tkinter gui elements for the current applied loads
        for load_gui in self.loads_gui:
            for gui_element in load_gui:
                gui_element.destroy()

        #Delete all the elements in the List containing the gui elements
        del self.loads_gui[:]
        del self.loads_scale[:]

        n = 0
        for loads in self.loads_gui_select_var:
            load_types = ['Point','Moment','UDL','TRAP']
            load_locals = ['Left','Center','Right']

            if loads[6].get() == 'Moment':
                self.loads_scale.append(float(loads[1].get())/2.0)
            else:
                self.loads_scale.append(float(loads[1].get()))
            self.loads_scale.append(float(loads[2].get()))

            self.loads_gui.append([
                tk.Checkbutton(self.loads_frame, variable=loads[0], command = self.build_loads),
                tk.Entry(self.loads_frame, textvariable=loads[1], width=15),
                tk.Entry(self.loads_frame, textvariable=loads[2], width=15),
                tk.Entry(self.loads_frame, textvariable=loads[3], width=15),
                tk.Entry(self.loads_frame, textvariable=loads[4], width=15),
                tk.OptionMenu(self.loads_frame, loads[5], *load_locals),
                tk.OptionMenu(self.loads_frame, loads[6], *load_types)])

            self.loads_gui[n][0].grid(row=n+1, column=1)
            self.loads_gui[n][1].grid(row=n+1, column=2, padx = 4)
            self.loads_gui[n][2].grid(row=n+1, column=3, padx = 4)
            self.loads_gui[n][3].grid(row=n+1, column=4, padx = 4)
            self.loads_gui[n][4].grid(row=n+1, column=5, padx = 4)
            self.loads_gui[n][5].grid(row=n+1, column=6)
            self.loads_gui[n][6].grid(row=n+1, column=7)
            n+=1

    def add_load(self, *event):

        self.loads_gui_select_var.append([tk.IntVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()])

        n = len(self.loads_gui_select_var)
        self.loads_gui_select_var[n-1][0].set(1)
        self.loads_gui_select_var[n-1][1].set(self.w1_gui.get())
        self.loads_gui_select_var[n-1][2].set(self.w2_gui.get())
        self.loads_gui_select_var[n-1][3].set(self.a_gui.get())
        self.loads_gui_select_var[n-1][4].set(self.b_gui.get())
        self.loads_gui_select_var[n-1][5].set(self.load_loc.get())
        self.loads_gui_select_var[n-1][6].set(self.load_type.get())

        self.build_loads_gui()
        self.build_loads()

    def remove_load(self, *event):
        '''
        for load in self.loads_gui[-1]:
            load.destroy()

        del self.loads_gui[-1]

        del self.loads_gui_select_var[-1]
        '''

        self.loads_gui_select_var = [i for i in self.loads_gui_select_var if i[0].get() == 1]
        self.build_loads_gui()

        self.build_loads()

    def reaction_graph(self,r,x):
        r = -1.0 * r
        arrow_height = r/6.0
        #30 degree arrow
        arrow_plus= x+(arrow_height*math.tan(math.radians(30)))
        arrow_minus= x-(arrow_height*math.tan(math.radians(30)))

        x_graph=[arrow_minus,x,arrow_plus,x,x]
        y_graph=[arrow_height,0,arrow_height,0,r]

        return x_graph, y_graph

    def run(self, *event):
        self.xl_listbox.delete(0,tk.END)
        self.lv_listbox.delete(0,tk.END)
        self.lm_listbox.delete(0,tk.END)
        self.ls_listbox.delete(0,tk.END)
        self.ld_listbox.delete(0,tk.END)

        self.xc_listbox.delete(0,tk.END)
        self.cv_listbox.delete(0,tk.END)
        self.cm_listbox.delete(0,tk.END)
        self.cs_listbox.delete(0,tk.END)
        self.cd_listbox.delete(0,tk.END)

        self.xr_listbox.delete(0,tk.END)
        self.rv_listbox.delete(0,tk.END)
        self.rm_listbox.delete(0,tk.END)
        self.rs_listbox.delete(0,tk.END)
        self.rd_listbox.delete(0,tk.END)

        if self.left_cant_ft.get() == '' or self.span_ft.get()== '' or self.right_cant_ft.get() == '':
            pass

        else:
            self.ll = float(self.left_cant_ft.get())
            self.lc = float(self.span_ft.get())
            self.lr = float(self.right_cant_ft.get())


            E = float(self.E_ksi.get()) * (1/1000) * (1/math.pow(0.001,2))       #convert Mpa = N/mm^2 to kN/m^2
            I = float(self.I_in4.get()) * (math.pow(0.001,4))                   #covert from mm^4 to m^4

            iters = int(self.stations.get())

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

            slopel = zeros(i)
            slopec = zeros(i)
            sloper = zeros(i)

            deltal = zeros(i)
            deltac = zeros(i)
            deltar = zeros(i)

            if self.ll == 0:
                load_left = [ppbeam.cant_left_point(0,0,self.ll,self.lc)]

            else:
                load_left = self.loads_left

            if len(self.loads_center) == 0:
                if self.lc == 0:
                    load_center = [ppbeam.no_load(self.lc)]
                else:
                    load_center = [ppbeam.pl(0,0,self.lc)]
            else:
                load_center = self.loads_center

            if self.lr == 0:
                load_right = [ppbeam.cant_right_point(0,0,self.lr,self.lc)]
            else:
                load_right = self.loads_right


            for load in load_left:
                reaction_left = reaction_left + load.rr + load.backspan.rl
                reaction_right = reaction_right + load.backspan.rr

                shearl = shearl + load.v(xsl)
                shearc = shearc + load.backspan.v(xsc)

                momentl = momentl + load.m(xsl)
                momentc = momentc + load.backspan.m(xsc)

                slopel = slopel + load.eis(xsl)
                slopec = slopec + load.backspan.eis(xsc)
                sloper = sloper + ppbeam.cant_right_nl(load.backspan.eisx(self.lc),self.lr).eis(xsr)

                deltal = deltal + load.eid(xsl)
                deltac = deltac + load.backspan.eid(xsc)
                deltar = deltar + ppbeam.cant_right_nl(load.backspan.eisx(self.lc),self.lr).eid(xsr)

            for load in load_center:
                reaction_left = reaction_left + load.rl
                reaction_right = reaction_right  + load.rr

                shearc = shearc + load.v(xsc)

                momentc = momentc + load.m(xsc)

                slopel = slopel + ppbeam.cant_left_nl(load.eisx(0),self.ll).eis(xsl)
                slopec = slopec + load.eis(xsc)
                sloper = sloper + ppbeam.cant_right_nl(load.eisx(self.lc),self.lr).eis(xsr)

                deltal = deltal + ppbeam.cant_left_nl(load.eisx(0),self.ll).eid(xsl)
                deltac = deltac + load.eid(xsc)
                deltar = deltar + ppbeam.cant_right_nl(load.eisx(self.lc),self.lr).eid(xsr)

            for load in load_right:
                reaction_left = reaction_left + load.backspan.rl
                reaction_right = reaction_right + load.backspan.rr + load.rl

                shearc = shearc + load.backspan.v(xsc)
                shearr = shearr + load.v(xsr)

                momentc = momentc + load.backspan.m(xsc)
                momentr = momentr + load.m(xsr)

                slopel = slopel + ppbeam.cant_left_nl(load.backspan.eisx(0),self.ll).eis(xsl)
                slopec = slopec + load.backspan.eis(xsc)
                sloper = sloper + load.eis(xsr)

                deltal = deltal + ppbeam.cant_left_nl(load.backspan.eisx(0),self.ll).eid(xsl)
                deltac = deltac + load.backspan.eid(xsc)
                deltar = deltar + load.eid(xsr)

            self.shearl = shearl
            self.shearc = shearc
            self.shearr = shearr

            self.momentl = momentl
            self.momentc = momentc
            self.momentr = momentr

            self.slopel = slopel / (E*I)
            self.slopec = slopec / (E*I)
            self.sloper = sloper / (E*I)

            self.deltal = (deltal / (E*I))*1000
            self.deltac = (deltac / (E*I))*1000
            self.deltar = (deltar / (E*I))*1000

            self.rlx, self.rly = self.reaction_graph(reaction_left, self.ll)
            self.rrx, self.rry = self.reaction_graph(reaction_right, self.ll+self.lc)

            self.reaction_left = reaction_left
            self.reaction_right = reaction_right

            self.res_labels[1].configure(text = 'Rl = {0:.3f} kN'.format(reaction_left))
            self.res_labels[2].configure(text = 'Rr = {0:.3f} kN'.format(reaction_right))

            if self.ll == 0:
                self.res_labels[4].configure(text = '--')
                self.res_labels[5].configure(text = '--')
                self.res_labels[6].configure(text = '--')
                self.res_labels[7].configure(text = '--')
            else:
                self.res_labels[4].configure(text = 'Vmax = {0:.3f} kN - Vmin = {1:.3f} kN'.format(max(shearl), min(shearl)))
                self.res_labels[5].configure(text = 'Mmax = {0:.3f} kN*m - Mmin = {1:.3f} kN*m'.format(max(momentl), min(momentl)))
                self.res_labels[6].configure(text = 'Smax = {0:.3E} rad - Smin = {1:.3E} rad'.format(max(self.slopel), min(self.slopel)))
                self.res_labels[7].configure(text = 'Dmax = {0:.3E} mm - Dmin = {1:.3E} mm'.format(max(self.deltal), min(self.deltal)))

            self.res_labels[9].configure(text = 'Vmax = {0:.3f} kN - Vmin = {1:.3f} kN'.format(max(shearc), min(shearc)))
            self.res_labels[10].configure(text = 'Mmax = {0:.3f} kN*m - Mmin = {1:.3f} kN*m'.format(max(momentc), min(momentc)))
            self.res_labels[11].configure(text = 'Smax = {0:.3E} rad - Smin = {1:.3E} rad'.format(max(self.slopec), min(self.slopec)))
            self.res_labels[12].configure(text = 'Dmax = {0:.3E} mm - Dmin = {1:.3E} mm'.format(max(self.deltac), min(self.deltac)))

            if self.lr == 0:
                self.res_labels[14].configure(text = '--')
                self.res_labels[15].configure(text = '--')
                self.res_labels[16].configure(text = '--')
                self.res_labels[17].configure(text = '--')
            else:
                self.res_labels[14].configure(text = 'Vmax = {0:.3f} kN - Vmin = {1:.3f} kN'.format(max(shearr), min(shearr)))
                self.res_labels[15].configure(text = 'Mmax = {0:.3f} kN*m - Mmin = {1:.3f} kN*m'.format(max(momentr), min(momentr)))
                self.res_labels[16].configure(text = 'Smax = {0:.3E} rad - Smin = {1:.3E} rad'.format(max(self.sloper), min(self.sloper)))
                self.res_labels[17].configure(text = 'Dmax = {0:.3E} mm - Dmin = {1:.3E} mm'.format(max(self.deltar), min(self.deltar)))

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
            for v in self.shearl:
                self.lv_listbox.insert(tk.END,'{0:.4f}'.format(v))

                if i % 2 == 0:
                    self.lv_listbox.itemconfigure(i, background=color)
                else:
                    pass
                i+=1

            i=0
            for m in self.momentl:
                self.lm_listbox.insert(tk.END,'{0:.4f}'.format(m))

                if i % 2 == 0:
                    self.lm_listbox.itemconfigure(i, background=color)
                else:
                    pass
                i+=1

            i=0
            for s in self.slopel:
                self.ls_listbox.insert(tk.END,'{0:.3E}'.format(s))

                if i % 2 == 0:
                    self.ls_listbox.itemconfigure(i, background=color)
                else:
                    pass
                i+=1

            i=0
            for d in self.deltal:
                self.ld_listbox.insert(tk.END,'{0:.3E}'.format(d))

                if i % 2 == 0:
                    self.ld_listbox.itemconfigure(i, background=color)
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
            for v in self.shearc:
                self.cv_listbox.insert(tk.END,'{0:.4f}'.format(v))

                if i % 2 == 0:
                    self.cv_listbox.itemconfigure(i, background=color)
                else:
                    pass
                i+=1

            i=0
            for m in self.momentc:
                self.cm_listbox.insert(tk.END,'{0:.4f}'.format(m))

                if i % 2 == 0:
                    self.cm_listbox.itemconfigure(i, background=color)
                else:
                    pass
                i+=1

            i=0
            for s in self.slopec:
                self.cs_listbox.insert(tk.END,'{0:.3E}'.format(s))

                if i % 2 == 0:
                    self.cs_listbox.itemconfigure(i, background=color)
                else:
                    pass
                i+=1

            i=0
            for d in self.deltac:
                self.cd_listbox.insert(tk.END,'{0:.3E}'.format(d))

                if i % 2 == 0:
                    self.cd_listbox.itemconfigure(i, background=color)
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
            for v in self.shearr:
                self.rv_listbox.insert(tk.END,'{0:.4f}'.format(v))

                if i % 2 == 0:
                    self.rv_listbox.itemconfigure(i, background=color)
                else:
                    pass
                i+=1

            i=0
            for m in self.momentr:
                self.rm_listbox.insert(tk.END,'{0:.4f}'.format(m))

                if i % 2 == 0:
                    self.rm_listbox.itemconfigure(i, background=color)
                else:
                    pass
                i+=1

            i=0
            for s in self.sloper:
                self.rs_listbox.insert(tk.END,'{0:.3E}'.format(s))

                if i % 2 == 0:
                    self.rs_listbox.itemconfigure(i, background=color)
                else:
                    pass
                i+=1

            i=0
            for d in self.deltar:
                self.rd_listbox.insert(tk.END,'{0:.3E}'.format(d))

                if i % 2 == 0:
                    self.rd_listbox.itemconfigure(i, background=color)
                else:
                    pass
                i+=1

            #save station to global variables for other processes
            self.xsl_local = xsl
            self.xsc_local = xsc
            self.xsr_local = xsr
            #convert x coordinates to global
            self.xsl = xsl
            self.xsc = xsc + xsl[-1]
            self.xsr = xsr + self.xsc[-1]

            self.has_run = 1
            self.bm_canvas_draw()

            self.loads_piece = []
            self.loads_piece.extend(self.loads_center)

            if self.ll == 0:
                pass
            else:
                if self.lc == 0:
                    pass
                else:
                    self.loads_piece.append(ppbeam.point_moment(momentl[-1],0,xsc[-1]))

            if self.lr == 0:
                pass
            else:
                if self.lc == 0:
                    pass
                else:
                    self.loads_piece.append(ppbeam.point_moment(-1*momentr[0],xsc[-1],xsc[-1]))


            if len(self.loads_piece) == 0:
                pass
            else:
                self.piece_function_gen()

    def runx(self, *event):
        x = float(self.resx_var.get())

        E = float(self.E_ksi.get()) * (1/1000) * (1/math.pow(0.001,2))       #convert Mpa = N/mm^2 to kN/m^2
        I = float(self.I_in4.get()) * (math.pow(0.001,4))                  #covert from mm^4 to m^4

        v,m,s,d = self.analysisx(x)

        shearlx = v[0]
        momentlx = m[0]
        slopelx = s[0] / (E*I)
        deltalx =(d[0] / (E*I))*1000.0

        shearcx = v[1]
        momentcx = m[1]
        slopecx = s[1] / (E*I)
        deltacx =(d[1] / (E*I))*1000.0

        shearrx = v[2]
        momentrx = m[2]
        sloperx = s[2] / (E*I)
        deltarx =(d[2] / (E*I))*1000.0

        self.deltacx = deltacx

        if self.ll == 0 or x > self.ll:

            self.resx_labels[2].configure(text = '--')
            self.resx_labels[3].configure(text = '--')
            self.resx_labels[4].configure(text = '--')
            self.resx_labels[5].configure(text = '--')
        else:
            self.resx_labels[2].configure(text = 'V = {0:.3f} kN'.format(shearlx))
            self.resx_labels[3].configure(text = 'M = {0:.3f} kN*m'.format(momentlx))
            self.resx_labels[4].configure(text = 'S = {0:.3E} rad'.format(slopelx))
            self.resx_labels[5].configure(text = 'D = {0:.3E} mm'.format(deltalx))

        self.resx_labels[7].configure(text = 'V = {0:.3f} kN'.format(shearcx))
        self.resx_labels[8].configure(text = 'M = {0:.3f} kN*m'.format(momentcx))
        self.resx_labels[9].configure(text = 'S = {0:.3E} rad'.format(slopecx))
        self.resx_labels[10].configure(text = 'D = {0:.3E} mm'.format(deltacx))

        if self.lr == 0 or x > self.lr:
            self.resx_labels[12].configure(text = '--')
            self.resx_labels[13].configure(text = '--')
            self.resx_labels[14].configure(text = '--')
            self.resx_labels[15].configure(text = '--')
        else:
            self.resx_labels[12].configure(text = 'V = {0:.3f} kN'.format(shearrx))
            self.resx_labels[13].configure(text = 'M = {0:.3f} kN*m'.format(momentrx))
            self.resx_labels[14].configure(text = 'S = {0:.3E} rad'.format(sloperx))
            self.resx_labels[15].configure(text = 'D = {0:.3E} mm'.format(deltarx))

    def analysisx(self, x):

        if self.left_cant_ft.get() == '' or self.span_ft.get()== '' or self.right_cant_ft.get() == '':
            pass
            return 0
        else:
            self.ll = float(self.left_cant_ft.get())
            self.lc = float(self.span_ft.get())
            self.lr = float(self.right_cant_ft.get())

            x = x

            if x > self.ll:
                xsl = self.ll
            else:
                xsl = x
            xsc = x

            if x > self.lr:
                xsr = self.lr
            else:
                xsr = x

            shearlx = 0
            shearcx = 0
            shearrx = 0

            momentlx = 0
            momentcx = 0
            momentrx = 0

            slopelx = 0
            slopecx = 0
            sloperx = 0

            deltalx = 0
            deltacx = 0
            deltarx = 0

            if self.ll == 0:
                load_left = [ppbeam.cant_left_point(0,0,self.ll,self.lc)]

            else:
                load_left = self.loads_left

            if len(self.loads_center) == 0:
                if self.lc == 0:
                    load_center = [ppbeam.no_load(self.lc)]
                else:
                    load_center = [ppbeam.pl(0,0,self.lc)]
            else:
                load_center = self.loads_center

            if self.lr == 0:
                load_right = [ppbeam.cant_right_point(0,0,self.lr,self.lc)]
            else:
                load_right = self.loads_right


            for load in load_left:

                shearlx = shearlx + load.vx(xsl)
                shearcx = shearcx + load.backspan.vx(xsc)

                momentlx = momentlx + load.mx(xsl)
                momentcx = momentcx + load.backspan.mx(xsc)

                slopelx = slopelx + load.eisx(xsl)
                slopecx = slopecx + load.backspan.eisx(xsc)
                sloperx = sloperx + ppbeam.cant_right_nl(load.backspan.eisx(self.lc),self.lr).eisx(xsr)

                deltalx = deltalx + load.eidx(xsl)
                deltacx = deltacx + load.backspan.eidx(xsc)
                deltarx = deltarx + ppbeam.cant_right_nl(load.backspan.eisx(self.lc),self.lr).eidx(xsr)

            for load in load_center:

                shearcx = shearcx + load.vx(xsc)

                momentcx = momentcx + load.mx(xsc)

                slopelx = slopelx + ppbeam.cant_left_nl(load.eisx(0),self.ll).eisx(xsl)
                slopecx = slopecx + load.eisx(xsc)
                sloperx = sloperx + ppbeam.cant_right_nl(load.eisx(self.lc),self.lr).eisx(xsr)

                deltalx = deltalx + ppbeam.cant_left_nl(load.eisx(0),self.ll).eidx(xsl)
                deltacx = deltacx + load.eidx(xsc)
                deltarx = deltarx + ppbeam.cant_right_nl(load.eisx(self.lc),self.lr).eidx(xsr)

            for load in load_right:

                shearcx = shearcx + load.backspan.vx(xsc)
                shearrx = shearrx + load.vx(xsr)

                momentcx = momentcx + load.backspan.mx(xsc)
                momentrx = momentrx + load.mx(xsr)

                slopelx = slopelx + ppbeam.cant_left_nl(load.backspan.eisx(0),self.ll).eisx(xsl)
                slopecx = slopecx + load.backspan.eisx(xsc)
                sloperx = sloperx + load.eisx(xsr)

                deltalx = deltalx + ppbeam.cant_left_nl(load.backspan.eisx(0),self.ll).eidx(xsl)
                deltacx = deltacx + load.backspan.eidx(xsc)
                deltarx = deltarx + load.eidx(xsr)

            v = [shearlx, shearcx, shearrx]
            m = [momentlx, momentcx, momentrx]
            s = [slopelx, slopecx, sloperx]
            d = [deltalx, deltacx, deltarx]

            return v,m,s,d

    def analysisx_type(self, x, res=1,*event):
        v,m,s,d = self.analysisx(x)
        a = [v,m,s,d]

        out = a[res]

        return -1*out[1]

    def update(self, *event):

        ll = float(self.left_cant_ft.get())
        lc = float(self.span_ft.get())
        lr = float(self.right_cant_ft.get())

        n=0

        if ll > 0:
            self.fixed_left.set(0)
            self.fixed_left_check.configure(state=tk.DISABLED)
        else:
            self.fixed_left_check.configure(state=tk.NORMAL)

        if lr > 0:
            self.fixed_right.set(0)
            self.fixed_right_check.configure(state=tk.DISABLED)
        else:
            self.fixed_right_check.configure(state=tk.NORMAL)

        for load in self.loads_gui_select_var:

            a = float(load[3].get())
            b = float(load[4].get())
            load_location = load[5].get()

            if ll == 0 and load_location == 'Left':
                del self.loads_gui_select_var[n]

                for widgets in self.loads_gui[n]:
                    widgets.destroy()

                del self.loads_gui[n]

            elif lr == 0 and load_location == 'Right':
                del self.loads_gui_select_var[n]

                for widgets in self.loads_gui[n]:
                    widgets.destroy()

                del self.loads_gui[n]

            elif load_location == 'Left' and a > ll:
                load[3].set(0)

            elif load_location == 'Right' and a > lr:
                load[3].set(0)

            elif load_location == 'Left' and b > ll:
                load[4].set(ll)

                if load[3].get() == load[4].get():
                    del self.loads_gui_select_var[n]

                    for widgets in self.loads_gui[n]:
                        widgets.destroy()

                    del self.loads_gui[n]

            elif load_location == 'Right' and b > lr:
                load[4].set(lr)

                if load[3].get() == load[4].get():
                    del self.loads_gui_select_var[n]

                    for widgets in self.loads_gui[n]:
                        widgets.destroy()

                    del self.loads_gui[n]

            elif load_location == 'Center' and a > lc:
                load[3].set(0)

            elif load_location == 'Center' and b > lc:
                load[4].set(lc)

                if load[3].get() == load[4].get():
                    del self.loads_gui_select_var[n]

                    for widgets in self.loads_gui[n]:
                        widgets.destroy()

                    del self.loads_gui[n]
            else:
                pass

            n = n+1

        self.build_loads()

    def moment_area(self, *event):
        if self.has_run == 1:
            pass
        else:
            self.run()

        ml = self.momentl
        mc = self.momentc
        mr = self.momentr

        xsl = self.xsl
        xsc = self.xsc - xsl[-1]
        xsr = self.xsr - self.xsc[-1]

        al = sci_int.cumtrapz(ml, xsl, initial = 0)
        ac = sci_int.cumtrapz(mc, xsc, initial = 0)
        ar = sci_int.cumtrapz(mr, xsr, initial = 0)

        m_xl = []
        m_xc = []
        m_xr = []

        for i in range(0,len(xsl)):
            m_xl.append(ml[i]*xsl[i])
            m_xc.append(mc[i]*xsc[i])
            m_xr.append(mr[i]*xsr[i])

        m_xl_a = sci_int.cumtrapz(m_xl, xsl, initial = 0)
        m_xc_a = sci_int.cumtrapz(m_xc, xsc, initial = 0)
        m_xr_a = sci_int.cumtrapz(m_xr, xsr, initial = 0)

        xl_l = (1/al[-1])*m_xl_a[-1]
        xl_c = (1/ac[-1])*m_xc_a[-1]
        xl_r = (1/ar[-1])*m_xr_a[-1]

        xr_l = xsl[-1] - xl_l
        xr_c = xsc[-1] - xl_c
        xr_r = xsr[-1] - xl_r

        res_string = 'Left:\nA = {0:.4f}   Xleft = {1:.4f} m    Xright = {2:.4f} m\n'.format(al[-1],xl_l,xr_l)
        res_string = res_string+'Center:\nA = {0:.4f}   Xleft = {1:.4f} m    Xright = {2:.4f} m\n'.format(ac[-1],xl_c,xr_c)
        res_string = res_string+'Right:\nA = {0:.4f}   Xleft = {1:.4f} m    Xright = {2:.4f} m\n'.format(ar[-1],xl_r,xr_r)

        self.moment_area_label.configure(text=res_string)

    def multi_solve(self, *args):
        l_ft = float(self.span_ft.get())

        fem = [self.fixed_left.get(),self.fixed_right.get()]

        #######################################################################################################
        #######################################################################################################
        # Solve Simultaneous equation for internal reactions and fixed end moments knowing
        # deflection and end slopes of simple beam at support points:
        #
        # By compatibility for fixed ends initial and final slope should be 0, and deflection
        # at each interior support location should be 0.
        #
        # Function expects consistent units for values, should produce accurate results for
        # both metric and imperial units.
        #
        #[s0, sL, d1....di] = [M0,ML,p1....pi]*[eis0_M0, eis0_ML, eis0_p1......eis0_pi
        #                                       eisL_M0, eisL_ML, eisL_p1......eisL_pi
        #                                       eid_M0_p1,  eid_ML_p1, eid_p11.....eid_pi1
        #                                       eid_M0_pi,  eid_ML_pi, eid_p1i.....eid_pii]
        # Where:
        # s0 = slope at 0 ft, or left end of beam, calculated for the single span simply supported beam
        # sL = slope at L ft, or right end of beam, calculated for the single span simply supported beam
        # d1 = deflection at first interior support 1 location calculated for the single span simply supported beam
        # di = deflection at ith interior support i location calculated for the single span simply supported beam
        #
        # s and d are to be independant of E, modulus of elasticity, and I, moment of inertia, therefore
        # either need to divide by E*I or provide s and d in terms of E*I*s and E*I*d
        #
        # M0 = fixed end moment at 0 ft, or left end
        # Ml = fixed end moment at L ft, or right end
        # p1 = reaction at first interior support
        # pi = reaction at ith interior support
        #
        # eis0_M0 = slope coefficient for M0 at 0 ft, or left end
        # eis0_Ml = slope coefficient for ML at 0 ft, or left end
        # eis0_p1 = slope coefficient for first interior support at 0 ft, or left end
        # eis0_pi = slope coefficient for ith interior support at 0 ft, or left end
        #
        # eisL_M0 = slope coefficient for M0 at L ft, or right end
        # eisL_Ml = slope coefficient for ML at L ft, or right end
        # eisL_p1 = slope coefficient for first interior support at L ft, or right end
        # eisL_pi = slope coefficient for ith interior support at L ft, or right end
        #
        # eid_M0_p1 = deflection coefficient at first interior support for M0
        # eid_M0_p1 = deflection coefficient at first interior support for ML
        # eid_p11 = deflection coefficient at first interior support for first interior reaction
        # eid_pi1 = deflection coefficient at first interior support for ith interior reaction
        #
        # eid_M0_pi = deflection coefficient at ith interior support for M0
        # eid_M0_pi = deflection coefficient at ith interior support for ML
        # eid_p1i = deflection coefficient at ith interior support for first interior reaction
        # eid_pii = deflection coefficient at ith interior support for ith interior reaction
        #
        #######################################################################################################
        #######################################################################################################

        #build the coefficient matrix rows and the deflection values
        delta = []
        coeff_matrix = []

        #Slope at each end of simple beam
        v0,m0,s0,d0 = self.analysisx(0)
        vl,ml,sl,dl = self.analysisx(l_ft)

        delta.append(s0[1])
        delta.append(sl[1])

        #Start Moment Component
        mo = ppbeam.point_moment(1,0,l_ft)
        ml = ppbeam.point_moment(1,l_ft,l_ft)

        coeff_matrix.append([mo.eisx(0)*fem[0],ml.eisx(0)*fem[1]])
        coeff_matrix.append([mo.eisx(l_ft)*fem[0],ml.eisx(l_ft)*fem[1]])

        if self.internal_supports.get() == '':
            pass
        else:
            reaction_points_string = self.internal_supports.get().split(',')
            reaction_points = [float(point) for point in reaction_points_string]

            for support in reaction_points:

                l = l_ft
                a = support

                pl = ppbeam.pl(1,a,l)

                #Deflection at each support location
                v,m,s,d = self.analysisx(a)
                delta.append(d[1])

                coeff_row = []

                coeff_row.append(mo.eidx(a)*fem[0])
                coeff_row.append(ml.eidx(a)*fem[1])

                for point in reaction_points:

                    x = point
                    new_pl = ppbeam.pl(1,x,l)
                    eid_p = new_pl.eidx(a)

                    coeff_row.append(eid_p)

                coeff_matrix[0].append(pl.eisx(0))
                coeff_matrix[1].append(pl.eisx(l))


                coeff_matrix.append(coeff_row)

        d = np.array(delta)
        coeff = np.array(coeff_matrix)

        if fem[0] == 0:
            d = np.delete(d, (0), axis=0)
            coeff = np.delete(coeff, (0), axis=0)
            coeff = np.delete(coeff, (0), axis=1)

        if fem == [1,0]:
            d = np.delete(d, (1), axis=0)
            coeff = np.delete(coeff, (1), axis=0)
            coeff = np.delete(coeff, (1), axis=1)

        elif fem == [0,0]:
            d = np.delete(d, (0), axis=0)
            coeff = np.delete(coeff, (0), axis=0)
            coeff = np.delete(coeff, (0), axis=1)
        else:
            pass

        R = np.linalg.solve(coeff,d)

        res_string = ''
        count = 0
        if fem == [1,1]:
            res_string = res_string + 'M,0 = {0:.4f} kN*m\n'.format(-1*R[0])
            res_string = res_string + 'M,L = {0:.4f} kN*m\n'.format(-1*R[1])
            count = 2

            self.loads_gui_select_var.append([tk.IntVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()])

            n = len(self.loads_gui_select_var)
            self.loads_gui_select_var[n-1][0].set(1)
            self.loads_gui_select_var[n-1][1].set(-1*R[0])
            self.loads_gui_select_var[n-1][2].set(0)
            self.loads_gui_select_var[n-1][3].set(0)
            self.loads_gui_select_var[n-1][4].set(0)
            self.loads_gui_select_var[n-1][5].set('Center')
            self.loads_gui_select_var[n-1][6].set('Moment')

            self.loads_gui_select_var.append([tk.IntVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()])

            n = len(self.loads_gui_select_var)
            self.loads_gui_select_var[n-1][0].set(1)
            self.loads_gui_select_var[n-1][1].set(-1*R[1])
            self.loads_gui_select_var[n-1][2].set(0)
            self.loads_gui_select_var[n-1][3].set(l_ft)
            self.loads_gui_select_var[n-1][4].set(0)
            self.loads_gui_select_var[n-1][5].set('Center')
            self.loads_gui_select_var[n-1][6].set('Moment')

        elif fem == [1,0]:
            res_string = res_string + 'M,0 = {0:.4f} kN*m\n'.format(-1*R[0])
            count = 1

            self.loads_gui_select_var.append([tk.IntVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()])

            n = len(self.loads_gui_select_var)
            self.loads_gui_select_var[n-1][0].set(1)
            self.loads_gui_select_var[n-1][1].set(-1*R[0])
            self.loads_gui_select_var[n-1][2].set(0)
            self.loads_gui_select_var[n-1][3].set(0)
            self.loads_gui_select_var[n-1][4].set(0)
            self.loads_gui_select_var[n-1][5].set('Center')
            self.loads_gui_select_var[n-1][6].set('Moment')

        elif fem == [0,1]:
            res_string = res_string + 'M,L = {0:.4f} kN*m\n'.format(-1*R[0])
            count = 1

            self.loads_gui_select_var.append([tk.IntVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()])

            n = len(self.loads_gui_select_var)
            self.loads_gui_select_var[n-1][0].set(1)
            self.loads_gui_select_var[n-1][1].set(-1*R[0])
            self.loads_gui_select_var[n-1][2].set(0)
            self.loads_gui_select_var[n-1][3].set(l_ft)
            self.loads_gui_select_var[n-1][4].set(0)
            self.loads_gui_select_var[n-1][5].set('Center')
            self.loads_gui_select_var[n-1][6].set('Moment')

        else:
            pass

        if self.internal_supports.get() == '':
            pass
        else:
            for reaction in reaction_points:

                res_string = res_string + 'R @ {0:.3f} ft = {1:.4f} kN\n'.format(reaction,-1*R[count])

                #Add Redundant Interior Reaction as Point Load on Center Span
                self.loads_gui_select_var.append([tk.IntVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()])

                n = len(self.loads_gui_select_var)
                self.loads_gui_select_var[n-1][0].set(1)
                self.loads_gui_select_var[n-1][1].set(-1*R[count])
                self.loads_gui_select_var[n-1][2].set(0)
                self.loads_gui_select_var[n-1][3].set(reaction)
                self.loads_gui_select_var[n-1][4].set(0)
                self.loads_gui_select_var[n-1][5].set('Center')
                self.loads_gui_select_var[n-1][6].set('Point')

                count+=1

        self.multi_result_label.configure(text=res_string)

        self.build_loads_gui()
        self.build_loads()

    def draw_static_beam_mouse(self, event, *args):
        w = self.bm_canvas.winfo_width()
        h = self.bm_canvas.winfo_height()

        self.bm_canvas.delete(self.val_at_x)
        self.bm_canvas.delete(self.val_at_x_text)
        initial = 50

        sf = self.canvas_scale_x

        ll = float(self.left_cant_ft.get())
        lc = float(self.span_ft.get())
        lr = float(self.right_cant_ft.get())

        x_screen = event.x
        x = x_screen - initial

        E = float(self.E_ksi.get()) * (1/1000) * (1/math.pow(0.001,2))       #convert Mpa = N/mm^2 to kN/m^2
        I = float(self.I_in4.get()) * (math.pow(0.001,4))                   #covert from mm^4 to m^4

        text_color = 'yellow'

        if x > (ll*sf) and x < ((ll+lc) * sf):
            x_anal = (x/sf) - ll

            v,m,s,d = self.analysisx(x_anal)

            self.val_at_x_text = self.bm_canvas.create_text(w/2.0, (h-26), justify=tk.CENTER, text= '@ Xc = {0:.2f} m\nV: {1:.2f} kN  M: {2:.2f} kN*m  S: {3:.3E} rad  D: {4:.3E} mm'.format(x_anal,v[1],m[1],s[1]/(E*I),(d[1]/(E*I))*1000.0), fill=text_color)

        elif x > ((ll+lc)*sf):
            x_anal = (x/sf) - (ll+lc)

            if x_anal > lr:
                pass
            else:
                v,m,s,d = self.analysisx(x_anal)

                self.val_at_x_text = self.bm_canvas.create_text(w/2.0, (h-26), justify=tk.CENTER, text= '@ Xr = {0:.2f} m\nV: {1:.2f} kN  M: {2:.2f} kN*m  S: {3:.3E} rad  D: {4:.3E} mm'.format(x_anal,v[2],m[2],s[2]/(E*I),(d[2]/(E*I))*1000.0), fill=text_color)
        else:
            x_anal = x/sf
            if x_anal < 0:
                pass
            else:
                v,m,s,d = self.analysisx(x_anal)

                self.val_at_x_text = self.bm_canvas.create_text(w/2.0, (h-26), justify=tk.CENTER, text= '@ Xl = {0:.2f} m\nV: {1:.2f} kN  M: {2:.2f} kN*m  S: {3:.3E} rad  D: {4:.3E} mm'.format(x_anal,v[0],m[0],s[0]/(E*I),(d[0]/(E*I))*1000.0), fill=text_color)

        self.val_at_x = self.bm_canvas.create_line(x_screen, 0,x_screen,h,fill="blue", width=1, dash=(6,6))

    def write_html_results(self,*args):

        file = open('simple_beam.html','w')
        file.write('<!doctype html>\n')
        file.write('<html>\n\n')
        file.write('<head>\n')
        file.write('<title>Simple Beam Diagrams</title>\n')
        file.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.bundle.js"></script>\n')
        file.write('<style>\n')
        file.write('body {\n  background-color: rgb(245, 245, 245);\n}\n')
        file.write('canvas{\n  width: 500px;\n')
        file.write('  -moz-user-select: none;\n')
        file.write('  -webkit-user-select: none;\n')
        file.write('  -ms-user-select: none;\n}\n')
        file.write('''table {
                    font-family: Arial, Helvetica, sans-serif;
                    border-collapse: collapse;
                    width: 4.9in;
                    font-size: 12px;
                    }

                    td,  th {
                            border: 1px solid #BDC3C7;
                            text-align: center;
                            padding: 2px;
                            }

                     tr:nth-child(even){background-color: #E5E7E9}

                     tr:hover {background-color: #BDC3C7;}

                     th {
                         padding-top: 2px;
                         padding-bottom: 2px;
                         background-color: #D5D8DC;
                         color: #353535;
                 }\n''')
        file.write('</style>\n')
        file.write('</head>\n\n<body>\n')
        file.write('<div>\n')
        file.write('<br>\n<table>\n')
        ins = ['Left Cant. (m):','Center Span (m):','Right Cant. (m):','E (MPa):','I (mm^4):','Stations:','Fixed Left:','Fixed Right:','Interior Supports(m):']
        i=0
        file.write('<tr>\n')
        file.write('<th colspan="2">Inputs:</th>\n')
        file.write('</tr>\n')
        for x in self.inputs:
            file.write('<tr>\n')
            file.write('<td>{0}</td>\n'.format(ins[i]))
            file.write('<td>{0}</td>\n'.format(x.get()))
            file.write('</tr>\n')
            i+=1
        file.write('</table>\n<br>\n')
        file.write('<table>\n')
        file.write('<tr>\n')
        file.write('<th colspan="6">Applied Loads: (includes interior reactions)</th>\n')
        file.write('</tr>\n')
        file.write('<tr>\n<th>P,M, or W1 (kN/kN*m/kN/m)</th>\n<th>W2 (kN/m)</th>\n<th>a (m)</th>\n<th>b (m)</th>\n<th>Location</th>\n<th>Load Type</th>\n</tr>\n')

        for load in self.loads_gui_select_var:
            if load[0].get() == 1:
                file.write('<tr>\n')
                file.write('<td>{0}</td>\n'.format(load[1].get()))
                file.write('<td>{0}</td>\n'.format(load[2].get()))
                file.write('<td>{0}</td>\n'.format(load[3].get()))
                file.write('<td>{0}</td>\n'.format(load[4].get()))
                file.write('<td>{0}</td>\n'.format(load[5].get()))
                file.write('<td>{0}</td>\n'.format(load[6].get()))
                file.write('</tr>\n')

        file.write('</table>\n<br>\n')
        file.write('<table>\n')
        file.write('<tr>\n')
        file.write('<th colspan="2">Results:</th>\n')
        file.write('</tr>\n')
        file.write('<tr>\n<td>Reaction Left (kN):</td>\n<td>{0:.4f}</td>\n</tr>\n'.format(self.reaction_left))
        file.write('<tr>\n<td>Reaction Right (kN):</td>\n<td>{0:.4f}</td>\n</tr>\n'.format(self.reaction_right))
        if self.lc == 0:
            pass
        else:
            file.write('<tr>\n<td colspan="2"><u>Center Span Max/Min Moments (kN*m):</u></td>\n</tr>\n')
            for x in self.zero_shear_loc:
                v,m,s,d = self.analysisx(x)
                file.write('<tr>\n<td>@{0:.4f} m</td>\n<td>{1:.4f}</td>\n</tr>\n'.format(x,m[1]))
            file.write('<tr>\n<td colspan="2"><u>Center Span Max/Min Deflections (mm):</u></td>\n</tr>\n')
            
            E = float(self.E_ksi.get()) * (1/1000) * (1/math.pow(0.001,2))       #convert Mpa = N/mm^2 to kN/m^2
            I = float(self.I_in4.get()) * (math.pow(0.001,4))                   #covert from mm^4 to m^4

            for x in self.zero_slope_loc:
                v,m,s,d = self.analysisx(x)
                file.write('<tr>\n<td>@{0:.3E} m</td>\n<td>{1:.4f}</td>\n</tr>\n'.format(x,(d[1]/(E*I))*1000.0))

        file.write('</table>\n<br>\n</div>\n<br>\n')
        # Equations
        if self.lc == 0:
            pass
        else:
            file.write('<h3>Center Span Piecewise Functions</h3>\n<br>\n{0}<br>\n'.format(ppbeam.PieceFunctionStringHTMLTable(self.piece_eq_center[0],'Shear (kN):')))
            file.write('{0}<br>\n'.format(ppbeam.PieceFunctionStringHTMLTable(self.piece_eq_center[1],'Moment (kN*m):')))
            file.write('{0}<br>\n'.format(ppbeam.PieceFunctionStringHTMLTable(self.piece_eq_center[2],'EI*Slope (rads): [convert EI from mm to m first]')))
            file.write('{0}<br>\n'.format(ppbeam.PieceFunctionStringHTMLTable(self.piece_eq_center[3],'(EI/1000.0)*Deflection (mm):[convert EI from mm to m first]')))

        file.write('<div style="width: 8in;">\n<canvas id="shear"></canvas>\n')
        file.write('<canvas id="moment"></canvas>\n')
        file.write('<canvas id="slope"></canvas>\n')
        file.write('<canvas id="deflection"></canvas>\n</div>\n')
        file.write('</div>\n')

        file.write("<script>\nvar scatterShear = {\ndatasets: [{\n")
        file.write("label: 'Shear',\nshowLine: true,\nlineTension: 0,\nborderColor: 'rgb(255, 0, 0)',\nbackgroundColor: 'rgba(255, 0, 0,0.2)',\npointRadius: 3,\npointBackgroundColor:'rgb(255,0,0)',\ndata: [\n")

        #Shear
        i=0
        text = ''
        for x in self.xsl:
            text = text+'{x: '
            text = text+'{0:.3f},\ny: {1:.3f}'.format(x, self.shearl[i])
            text = text+'},\n'
            i+=1
        i=0
        for x  in self.xsc:
            text = text+'{x: '
            text = text+'{0:.3f},\ny: {1:.3f}'.format(x, self.shearc[i])
            text = text+'},\n'
            i+=1
        i=0
        for x  in self.xsr:
            text = text+'{x: '
            text = text+'{0:.3f},\ny: {1:.3f}'.format(x, self.shearr[i])
            text = text+'},\n'
            i+=1
        text = text[:-3]
        text = text + '}]'

        file.write(text)
        file.write('}]};')
        file.write("\nvar scatterMoment = {\ndatasets: [{\n")
        file.write("label: 'Moment',\nshowLine: true,\nlineTension: 0,\nborderColor: 'rgb(0, 255, 0)',\nbackgroundColor: 'rgba(0, 255, 0,0.2)',\npointRadius: 3,\npointBackgroundColor:'rgb(0,255,0)',\ndata: [\n")

        #moment
        i=0
        text = ''
        for x in self.xsl:
            text = text+'{x: '
            text = text+'{0:.3f},\ny: {1:.3f}'.format(x, self.momentl[i])
            text = text+'},\n'
            i+=1
        i=0
        for x  in self.xsc:
            text = text+'{x: '
            text = text+'{0:.3f},\ny: {1:.3f}'.format(x, self.momentc[i])
            text = text+'},\n'
            i+=1
        i=0
        for x  in self.xsr:
            text = text+'{x: '
            text = text+'{0:.3f},\ny: {1:.3f}'.format(x, self.momentr[i])
            text = text+'},\n'
            i+=1
        text = text[:-3]
        text = text + '}]'

        file.write(text)
        file.write('}]};')
        file.write("\nvar scatterSlope = {\ndatasets: [{\n")
        file.write("label: 'Slope',\nshowLine: true,\nlineTension: 0,\nborderColor: 'rgb(0, 0, 255)',\nbackgroundColor: 'rgba(0, 0, 255,0.2)',\npointRadius: 3,\npointBackgroundColor:'rgb(0,0,255)',\ndata: [\n")

        #slope
        i=0
        text = ''
        for x in self.xsl:
            text = text+'{x: '
            text = text+'{0:.3E},\ny: {1:.3E}'.format(x, self.slopel[i])
            text = text+'},\n'
            i+=1
        i=0
        for x  in self.xsc:
            text = text+'{x: '
            text = text+'{0:.3E},\ny: {1:.3E}'.format(x, self.slopec[i])
            text = text+'},\n'
            i+=1
        i=0
        for x  in self.xsr:
            text = text+'{x: '
            text = text+'{0:.3E},\ny: {1:.3E}'.format(x, self.sloper[i])
            text = text+'},\n'
            i+=1
        text = text[:-3]
        text = text + '}]'

        file.write(text)
        file.write('}]};')
        file.write("\nvar scatterDeflection = {\ndatasets: [{\n")
        file.write("label: 'Deflection',\nshowLine: true,\nlineTension: 0,\nborderColor: 'rgb(51, 51, 51)',\nbackgroundColor: 'rgba(115, 115, 115,0.2)',\npointRadius: 3,\npointBackgroundColor:'rgb(89,89,89)',\ndata: [\n")

        #deflection
        i=0
        text = ''
        for x in self.xsl:
            text = text+'{x: '
            text = text+'{0:.3E},\ny: {1:.3E}'.format(x, self.deltal[i])
            text = text+'},\n'
            i+=1
        i=0
        for x  in self.xsc:
            text = text+'{x: '
            text = text+'{0:.3E},\ny: {1:.3E}'.format(x, self.deltac[i])
            text = text+'},\n'
            i+=1
        i=0
        for x  in self.xsr:
            text = text+'{x: '
            text = text+'{0:.3E},\ny: {1:.3E}'.format(x, self.deltar[i])
            text = text+'},\n'
            i+=1
        text = text[:-3]
        text = text + '}]'

        file.write(text)
        file.write('}]};\n')

        file.write("var ctx = document.getElementById('shear').getContext('2d');\n")
        file.write('window.myScatter = new Chart(ctx, {\n')
        file.write("type: 'scatter',\n")
        file.write('data: scatterShear, \n')
        file.write('options: {\n')
        file.write('title: {\n')
        file.write('display: true,\n')
        file.write("text: 'Shear (kN)'\n")
        file.write('},\n')
        file.write('}\n')
        file.write('});\n')
        file.write("var ctx = document.getElementById('moment').getContext('2d');\n")
        file.write('window.myScatter = new Chart(ctx, {\n')
        file.write("type: 'scatter',\n")
        file.write('data: scatterMoment, \n')
        file.write('options: {\n')
        file.write('title: {\n')
        file.write('display: true,\n')
        file.write("text: 'Moment (kN*m)'\n")
        file.write('},\n')
        file.write('}\n')
        file.write('});\n')
        file.write("var ctx = document.getElementById('slope').getContext('2d');\n")
        file.write('window.myScatter = new Chart(ctx, {\n')
        file.write("type: 'scatter',\n")
        file.write('data: scatterSlope, \n')
        file.write('options: {\n')
        file.write('title: {\n')
        file.write('display: true,\n')
        file.write("text: 'Slope (rad)'\n")
        file.write('},\n')
        file.write('}\n')
        file.write('});\n')
        file.write("var ctx = document.getElementById('deflection').getContext('2d');\n")
        file.write('window.myScatter = new Chart(ctx, {\n')
        file.write("type: 'scatter',\n")
        file.write('data: scatterDeflection, \n')
        file.write('options: {\n')
        file.write('title: {\n')
        file.write('display: true,\n')
        file.write("text: 'Deflection (mm)'\n")
        file.write('},\n')
        file.write('}\n')
        file.write('});\n')
        file.write('</script>\n')
        file.write('</body>\n')
        file.write('</html>\n')
        file.close()

        webbrowser.open('file://'+ os.path.realpath('simple_beam.html'))

    def piece_function_gen(self, *event):
        eq, eqs = ppbeam.center_span_piecewise_function(self.loads_piece)

        self.zero_shear_loc = ppbeam.points_of_zero_shear(eq[0])

        self.zero_moment_loc = ppbeam.points_of_zero_shear(eq[1])

        self.zero_slope_loc = ppbeam.points_of_zero_shear(eq[2])

        self.pfunc_text_box.delete(1.0,tk.END)

        string = 'Shear:\nPoints of 0 Shear:'

        for x in self.zero_shear_loc:
            string = string + ' {0:.4f} m '.format(x)

        string = string + '\n'
        string = string + eqs[0]

        string = string + '\nMoment:\nPoints of 0 Moment:'

        for x in self.zero_moment_loc:
            string = string + ' {0:.4f} m '.format(x)

        string = string + '\n'
        string = string + eqs[1]

        string = string + '\nEI*Slope:\nPoints of 0 Slope:'

        for x in self.zero_slope_loc:
            string = string + ' {0:.4f} m '.format(x)

        string = string + '\n'
        string = string + eqs[2]

        string = string + '\n(EI/1000.0)*Deflection:\n'
        string = string + eqs[3]

        self.pfunc_text_box.insert(tk.END, string)

        color = "pale green"
        self.pfunc_text_box.tag_configure("odd", background=color)
        self.pfunc_text_box.tag_configure("even", background="#ffffff")

        lastline = self.pfunc_text_box.index("end-1c").split(".")[0]
        tag = "odd"
        for i in range(1, int(lastline)):
            self.pfunc_text_box.tag_add(tag, "%s.0" % i, "%s.0" % (i+1))
            tag = "even" if tag == "odd" else "odd"

        self.piece_eq_center = eq

    def save_inputs(self, *args):

        out_file = tkFileDialog.asksaveasfile(mode='w', defaultextension=".simpbm")

        if out_file is None:
            return

        for data in self.inputs:
            text = '{0}\n'.format(data.get())
            out_file.write(text)

        out_file.write('*Loads*\n')
        for load in self.loads_gui_select_var:
            text = '{0},{1},{2},{3},{4},{5},{6}\n'.format(load[0].get(),load[1].get(),load[2].get(),load[3].get(),load[4].get(),load[5].get(),load[6].get())
            out_file.write(text)
        out_file.close()

    def open_existing(self, *args):

        filename = tkFileDialog.askopenfilename()

        extension = filename.split('.')[-1]

        del self.loads_gui_select_var[:]

        if filename is None:
            return
        elif extension not in ['simpbm']:
            tkMessageBox.showerror("ERROR!!","Selected File not a .simpbm file")
            return
        else:
            calc_file = open(filename,'rU')
            calc_data = calc_file.readlines()
            calc_file.close()

            i=0
            load_section = 0
            for line in calc_data:
                value = line.rstrip('\n')
                if value == '*Loads*':
                    load_section = 1
                elif load_section == 0:
                    self.inputs[i].set(value)
                else:
                    load = value.split(',')

                    self.loads_gui_select_var.append([tk.IntVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()])

                    n = len(self.loads_gui_select_var)
                    self.loads_gui_select_var[n-1][0].set(load[0])
                    self.loads_gui_select_var[n-1][1].set(load[1])
                    self.loads_gui_select_var[n-1][2].set(load[2])
                    self.loads_gui_select_var[n-1][3].set(load[3])
                    self.loads_gui_select_var[n-1][4].set(load[4])
                    self.loads_gui_select_var[n-1][5].set(load[5])
                    self.loads_gui_select_var[n-1][6].set(load[6])

                i+=1

            self.build_loads_gui()
            self.build_loads()

def main():
    root = tk.Tk()
    root.title("Simple Beam")
    Master_window(root)
    root.minsize(1280,720)
    root.mainloop()

if __name__ == '__main__':
    main()
