#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 22:15:33 2019

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
import Tkinter as tk
import tkMessageBox
import ttk
import tkFont
import tkFileDialog
import Frame_Moment_Distribution_2D as frame2d

class main_window:

    def __init__(self, master):

        self.master = master
        self.inputs = []
        self.beam_count = 0
        self.beam_inputs = []
        self.beam_gui_list = []
        self.cantL_count = 0
        self.cantL_beam_inputs = []
        self.cantL_beam_gui_list = []
        self.cantR_count = 0
        self.cantR_beam_inputs = []
        self.cantR_beam_gui_list = []
        self.column_up_inputs = []
        self.column_up_gui_list = []
        self.column_down_inputs = []
        self.column_down_gui_list = []
        self.beam_labels = []
        self.gui_load_list = []
        self.load_change_index = 0
        self.frame_built = 0
        self.frame_solved = 0
        self.max_h_up_graph = 0
        self.max_h_dwn_graph = 0

        self.max_m = 0
        self.min_m = 0
        self.max_v = 0
        self.min_v = 0
        self.max_d = 0
        self.min_d = 0
        self.max_s = 0
        self.min_s = 0

        self.nodes_analysis = []
        self.beams_analysis = []
        self.columns_analysis = []

        self.load_types = ['Point','Moment','UDL','TRAP']

        # Font Set
        self.f_size = 10
        self.helv = tkFont.Font(family=' Courier New',size=self.f_size, weight='bold')
        self.helv_norm = tkFont.Font(family=' Courier New',size=self.f_size)
        self.helv_res = tkFont.Font(family=' Courier New',size=self.f_size, weight='bold', underline = True)
        self.mono_f = tkFont.Font(family='Consolas',size=8)

        # Menubar
        self.menubar = tk.Menu(self.master)
        self.menu = tk.Menu(self.menubar, tearoff=0)
        self.menu_props = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label = "File", menu=self.menu)
        #self.menu.add_command(label="Save", command=self.save_inputs)
        #self.menu.add_command(label="Open", command=self.open_existing)
        self.menu.add_separator()
        self.menu.add_command(label="Quit", command=self.quit_app)
        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            self.master.tk.call(master, "config", "-menu", self.menubar)

        #Base Frame
        self.base_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.base_frame.pack(side=tk.BOTTOM, padx= 1, pady= 1, fill=tk.X)
        #Base Frame Items
        w=20
        h=1

        self.b_quit = tk.Button(self.base_frame,text="Quit", command=self.quit_app, font=self.helv, width=w, height=h, bg='red3')
        self.b_quit.pack(side=tk.RIGHT)

        self.b_build_frame = tk.Button(self.base_frame,text="Build the Frame", command=self.build_frame_gui_func, font=self.helv, width=w, height=h, bg='cornflower blue')
        self.b_build_frame.pack(side=tk.LEFT)

        self.b_solve_frame = tk.Button(self.base_frame,text="Solve the Frame",command=self.frame_analysis_gui, font=self.helv, width=w, height=h, bg='gray75',state=tk.DISABLED)
        self.b_solve_frame.pack(side=tk.LEFT)

        self.data_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.data_frame.pack(side=tk.LEFT, padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        #Main Notebooks
        self.nb_data = ttk.Notebook(self.data_frame)
        self.nb_data.pack(fill=tk.BOTH, expand=1)

        # Initial Geometry Input
        self.geo_tab = ttk.Frame(self.nb_data)
        self.nb_data.add(self.geo_tab, text='Geometry')

        self.geo_tab_frame = tk.Frame(self.geo_tab, bd=2, relief='sunken', padx=1,pady=1)

        self.b_add_beam = tk.Button(self.geo_tab_frame, text="Add a Beam",command=self.add_beam_func, font=self.helv, width=w, height=h)
        self.b_add_beam.grid(row=1,column=1)

        self.b_remove_beam = tk.Button(self.geo_tab_frame, text="Remove Last Beam",command=self.remove_last_beam_func, font=self.helv, width=w, height=h, state=tk.DISABLED)
        self.b_remove_beam.grid(row=2,column=1)

        self.b_add_left_cant = tk.Button(self.geo_tab_frame, text="Add Left Cantilever",command=self.add_cant_left_func, font=self.helv, width=w, height=h)
        self.b_add_left_cant.grid(row=1,column=2)

        self.b_remove_left_cant = tk.Button(self.geo_tab_frame, text="Remove Left Cantilever",command=self.remove_left_cant_func, font=self.helv, width=w, height=h, state=tk.DISABLED)
        self.b_remove_left_cant.grid(row=2,column=2)

        self.b_add_right_cant = tk.Button(self.geo_tab_frame, text="Add Right Cantilever",command=self.add_cant_right_func, font=self.helv, width=w, height=h)
        self.b_add_right_cant.grid(row=1,column=3)

        self.b_remove_right_cant = tk.Button(self.geo_tab_frame, text="Remove Right Cantilever",command=self.remove_right_cant_func, font=self.helv, width=w, height=h, state=tk.DISABLED)
        self.b_remove_right_cant.grid(row=2,column=3)

        self.col_bm_notebook = ttk.Notebook(self.geo_tab_frame)
        self.col_bm_notebook.grid(row=3,column=1, columnspan=4)

        self.bm_info_tab = ttk.Frame(self.col_bm_notebook)
        self.col_bm_notebook.add(self.bm_info_tab, text='Beam Data')

        tk.Label(self.bm_info_tab, text='\nLabel:').grid(row=1, column=1)
        tk.Label(self.bm_info_tab, text='\nLength (ft):').grid(row=1, column=2)
        tk.Label(self.bm_info_tab, text='\nE (ksi):').grid(row=1, column=3)
        tk.Label(self.bm_info_tab, text='\nI (in^4):').grid(row=1, column=4)
        tk.Label(self.bm_info_tab, text='|\n|').grid(row=1, column=5)
        tk.Label(self.bm_info_tab, text='Left Cant.\nLabel:').grid(row=1, column=6)
        tk.Label(self.bm_info_tab, text='\nLength (ft):').grid(row=1, column=7)
        tk.Label(self.bm_info_tab, text='\nE (ksi):').grid(row=1, column=8)
        tk.Label(self.bm_info_tab, text='\nI (in^4):').grid(row=1, column=9)
        tk.Label(self.bm_info_tab, text='|\n|').grid(row=1, column=10)
        tk.Label(self.bm_info_tab, text='Right Cant.\nLabel:').grid(row=1, column=11)
        tk.Label(self.bm_info_tab, text='\nLength (ft):').grid(row=1, column=12)
        tk.Label(self.bm_info_tab, text='\nE (ksi):').grid(row=1, column=13)
        tk.Label(self.bm_info_tab, text='\nI (in^4):').grid(row=1, column=14)

        self.colup_info_tab = ttk.Frame(self.col_bm_notebook)
        self.col_bm_notebook.add(self.colup_info_tab, text='Column Up Data')

        tk.Label(self.colup_info_tab, text='N/A:').grid(row=1, column=1)
        tk.Label(self.colup_info_tab, text='Label:').grid(row=1, column=2)
        tk.Label(self.colup_info_tab, text='Height (ft):').grid(row=1, column=3)
        tk.Label(self.colup_info_tab, text='E (ksi):').grid(row=1, column=4)
        tk.Label(self.colup_info_tab, text='I (in^4):').grid(row=1, column=5)
        tk.Label(self.colup_info_tab, text='A (in^2):').grid(row=1, column=6)
        tk.Label(self.colup_info_tab, text='Fixed Top:').grid(row=1, column=7)
        tk.Label(self.colup_info_tab, text='Hinge at Beam:').grid(row=1, column=8)

        self.coldwn_info_tab = ttk.Frame(self.col_bm_notebook)
        self.col_bm_notebook.add(self.coldwn_info_tab, text='Column Down Data')

        tk.Label(self.coldwn_info_tab, text='Label:').grid(row=1, column=1)
        tk.Label(self.coldwn_info_tab, text='Height (ft):').grid(row=1, column=2)
        tk.Label(self.coldwn_info_tab, text='E (ksi):').grid(row=1, column=3)
        tk.Label(self.coldwn_info_tab, text='I (in^4):').grid(row=1, column=4)
        tk.Label(self.coldwn_info_tab, text='A (in^2):').grid(row=1, column=5)
        tk.Label(self.coldwn_info_tab, text='Fixed Base:').grid(row=1, column=6)
        tk.Label(self.coldwn_info_tab, text='Hinge at Beam:').grid(row=1, column=7)

        self.geo_tab_frame.pack(fill=tk.BOTH, expand=1)

        #Loads Frame tabs
        #Loads
        self.loads_tab = ttk.Frame(self.nb_data)
        self.nb_data.add(self.loads_tab, text='Loads')

        self.g_loads_frame = tk.Frame(self.loads_tab, bd=2, relief='sunken', padx=1,pady=1)

        # Load Types and Combinations
        self.g_load_types_frame = tk.Frame(self.g_loads_frame, bd=2, relief='sunken', padx=1,pady=1)

        self.load_kinds = ['SELF','DL','LL','LL_pat']
        self.load_kinds_var_list = []
        self.load_combinations = [['All_DL',1,1,0,0],['ALL_LL',0,0,1,1],['DL_LL',1,1,1,1],['CONC_D',3,3,1,1],['LRFD_1',1.4,1.4,0,0],['LRFD_2',1.2,1.2,1.6,1.6]]
        self.load_combinations_var_list = []
        self.load_combo_gui_items = []

        i=0
        for kind in self.load_kinds:
            a = tk.Label(self.g_load_types_frame, text=kind)
            a.grid(row=1,column=1+i)
            i+=1
            self.load_combo_gui_items.append(a)

        i=0
        for combo in self.load_combinations:
            var_list = []
            j=0
            for item in combo:
                var_list.append(tk.StringVar())
                var_list[-1].set(item)
                if j==0:
                    a = tk.Entry(self.g_load_types_frame, textvariable=var_list[-1], width=8)
                else:
                    a = tk.Entry(self.g_load_types_frame, textvariable=var_list[-1], width=4)
                a.grid(row=2+i,column=j)
                self.load_combo_gui_items.append(a)
                j+=1
            i+=1

        self.g_load_types_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.g_applied_loads_frame = tk.Frame(self.g_loads_frame, bd=2, relief='sunken', padx=1,pady=1)

        tk.Label(self.g_applied_loads_frame, text='On Beam:').grid(row=1,column=1)
        tk.Label(self.g_applied_loads_frame, text='P,M,W1:').grid(row=1,column=2)
        tk.Label(self.g_applied_loads_frame, text='W2:').grid(row=1,column=3)
        tk.Label(self.g_applied_loads_frame, text='a:').grid(row=1,column=4)
        tk.Label(self.g_applied_loads_frame, text='b:').grid(row=1,column=5)
        tk.Label(self.g_applied_loads_frame, text='kind:').grid(row=1,column=6)
        tk.Label(self.g_applied_loads_frame, text='type:').grid(row=1,column=7)

        self.load_span_select = tk.StringVar()
        self.load_span_select.set('BM_1')
        spans = ['BM_1']
        self.load_span_selection = tk.OptionMenu(self.g_applied_loads_frame, self.load_span_select, *spans)
        self.load_span_selection.grid(row=2,column=1, sticky = tk.W)

        self.w1_gui = tk.StringVar()
        self.w2_gui = tk.StringVar()
        self.a_gui = tk.StringVar()
        self.b_gui = tk.StringVar()

        self.w1_gui.set(0)
        self.w2_gui.set(0)
        self.a_gui.set(0)
        self.b_gui.set(0)

        self.w1_gui_entry = tk.Entry(self.g_applied_loads_frame, textvariable=self.w1_gui, width=8)
        self.w1_gui_entry.grid(row=2,column=2, sticky = tk.W)
        self.w2_gui_entry = tk.Entry(self.g_applied_loads_frame, textvariable=self.w2_gui, width=8)
        self.w2_gui_entry.grid(row=2,column=3, sticky = tk.W)
        self.a_gui_entry = tk.Entry(self.g_applied_loads_frame, textvariable=self.a_gui, width=8)
        self.a_gui_entry.grid(row=2,column=4, sticky = tk.W)
        self.b_gui_entry = tk.Entry(self.g_applied_loads_frame, textvariable=self.b_gui, width=8)
        self.b_gui_entry.grid(row=2,column=5, sticky = tk.W)

        self.load_type = tk.StringVar()
        self.load_type.set('Point')
        load_types = ['Point','Moment','UDL','TRAP']
        self.load_type_selection = tk.OptionMenu(self.g_applied_loads_frame, self.load_type, *load_types)
        self.load_type_selection.grid(row=2,column=6, sticky = tk.W)

        self.load_kind_select = tk.StringVar()
        self.load_kind_select.set('DL')
        load_kinds = ['SELF','DL','LL','LL_pat']
        self.load_kind_selection = tk.OptionMenu(self.g_applied_loads_frame, self.load_kind_select, *load_kinds)
        self.load_kind_selection.grid(row=2,column=7, sticky = tk.W)

        self.loads_list_bframe = tk.Frame(self.g_applied_loads_frame, pady=5)
        self.b_add_load = tk.Button(self.loads_list_bframe, text="Add Load",command=self.add_load_gui, font=self.helv, width=12, height=h)
        self.b_add_load.grid(row=1,column=1)

        self.b_change_load = tk.Button(self.loads_list_bframe, text="Edit Load",command=self.change_load_gui, font=self.helv, width=12, height=h, state=tk.DISABLED, bg='gray75')
        self.b_change_load.grid(row=2,column=1)

        self.b_remove_load = tk.Button(self.loads_list_bframe, text="Del Load",command=self.remove_load_gui, font=self.helv, width=12, height=h, state=tk.DISABLED, bg='gray75')
        self.b_remove_load.grid(row=3,column=1)

        self.b_add_all_load = tk.Button(self.loads_list_bframe, text='Add to All', command=self.add_load_to_all_gui, font=self.helv, width=12, height=h)
        self.b_add_all_load.grid(row=4,column=1)

        self.b_remove_all_loads = tk.Button(self.loads_list_bframe, text='*Del All*', command=self.remove_all_loads_gui, font=self.helv, width=12, height=h, bg='red3')
        self.b_remove_all_loads.grid(row=5,column=1)

        self.loads_list_bframe.grid(row=3, column=1, sticky=tk.N)

        self.loads_list_frame = tk.Frame(self.g_applied_loads_frame, pady=5)

        self.loads_scrollbar = tk.Scrollbar(self.loads_list_frame, orient="vertical")
        self.loads_scrollbar.grid(row=1, column=2, sticky=tk.NS)

        self.load_listbox = tk.Listbox(self.loads_list_frame, height = 20, width = 50, font=self.helv, yscrollcommand=self.loads_scrollbar.set)
        self.load_listbox.grid(row=1, column=1)
        self.load_listbox.bind("<<ListboxSelect>>",self.load_listbox_click)

        self.loads_scrollbar.configure(command=self.load_listbox.yview)

        self.loads_list_frame.grid(row=3, column=2, columnspan=6)

        self.g_applied_loads_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.g_loads_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        #Graphics Frame tabs and canvases
        #Geometry - Graph
        self.graph_tab = ttk.Frame(self.nb_data)
        self.nb_data.add(self.graph_tab, text='Graph')

        self.g_a_frame = tk.Frame(self.graph_tab, bd=2, relief='sunken', padx=1,pady=1)
        self.g_a_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        self.g_plan_canvas = tk.Canvas(self.g_a_frame, width=50, height=50, bd=2, relief='sunken', background="black")
        #self.g_plan_canvas.bind("<Configure>", self.build_frame_graph)
        self.g_plan_canvas.pack(side = tk.LEFT, anchor='w', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        self.graph_b_frame = tk.Frame(self.g_a_frame, bd=2, relief='sunken', padx=4 ,pady=1)

        self.show_l = tk.IntVar()
        self.show_l.set(1)
        tk.Checkbutton(self.graph_b_frame, text=' : Show Loads', variable=self.show_l, command=self.build_frame_graph,font=self.helv).grid(row=1, column=1, sticky = tk.W)
        self.show_v = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show V', variable=self.show_v, command=self.build_frame_graph, font=self.helv).grid(row=2, column=1, sticky = tk.W)
        self.show_m = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show M', variable=self.show_m, command=self.build_frame_graph, font=self.helv).grid(row=3, column=1, sticky = tk.W)
        self.show_s = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show S', variable=self.show_s, command=self.build_frame_graph, font=self.helv).grid(row=4, column=1, sticky = tk.W)
        self.show_d = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show D', variable=self.show_d, command=self.build_frame_graph, font=self.helv).grid(row=5, column=1, sticky = tk.W)
        self.show_r = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show Reactions', variable=self.show_r, command=self.build_frame_graph, font=self.helv).grid(row=6, column=1, sticky = tk.W)
        self.show_dfs = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=" : Show DF's", variable=self.show_dfs, command=self.build_frame_graph, font=self.helv).grid(row=7, column=1, sticky = tk.W)
        self.show_m_tension = tk.IntVar()
        self.show_m_tension.set(1)
        tk.Checkbutton(self.graph_b_frame, text=' : Show M on\ntension face', variable=self.show_m_tension, command=self.build_frame_graph, font=self.helv).grid(row=8, column=1, sticky = tk.W)

        self.refresh_graphic = tk.Button(self.graph_b_frame, text="Refresh",command=self.build_frame_graph, font=self.helv, width=10, height=h)
        self.refresh_graphic.grid(row=9, column=1)

        tk.Label(self.graph_b_frame, text='Result Scale:', font=self.helv).grid(row=10, column=1, sticky=tk.W)
        self.res_scale = tk.StringVar()
        self.res_scale.set('50')
        self.res_scale_entry = tk.Entry(self.graph_b_frame, textvariable=self.res_scale, width=8)
        self.res_scale_entry.grid(row=10, column=2, sticky=tk.W)

        self.graph_b_frame.pack(side=tk.RIGHT, anchor='e')

        # Call function to display license dialog on app start
        self.add_beam_func()
        self.license_display()

    def license_display(self, *event):
        # Function to display license dialog on app start
        license_string = ("This program is free software; you can redistribute it and/or modify\n"
                    "it under the terms of the GNU General Public License as published by\n"
                    "the Free Software Foundation; either version 2 of the License, or\n"
                    "(at your option) any later version.\n\n"

                    "This program is distributed in the hope that it will be useful,\n"
                    "but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
                    "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
                    "GNU General Public License for more details.\n\n"

                    "You should have received a copy of the GNU General Public License along"
                    "with this program; if not, write to the Free Software Foundation, Inc.,"
                    "51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA\n"
                    "\nA copy of the License can be viewed at:\n"
                    "https://github.com/buddyd16/Structural-Engineering/blob/master/LICENSE")
        tkMessageBox.showerror("License Information",license_string)
        self.master.focus_force()

    def quit_app(self,*event):
        self.master.quit()
        self.master.destroy()

    def add_beam_func(self,*event):
        self.frame_built = 0
        self.frame_solved = 0
        self.beam_count +=1

        self.b_remove_beam.configure(state=tk.NORMAL)
        self.b_solve_frame.configure(state=tk.DISABLED, bg='red3')

        self.beam_inputs.append([tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()])
        self.beam_inputs[-1][1].set(10)
        self.beam_inputs[-1][2].set(29000)
        self.beam_inputs[-1][3].set(30.8)


        if self.beam_count == 1:
            self.column_up_inputs.append([tk.IntVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.IntVar(),tk.IntVar()])
            self.column_up_inputs.append([tk.IntVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.IntVar(),tk.IntVar()])
            self.column_down_inputs.append([tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.IntVar(),tk.IntVar()])
            self.column_down_inputs.append([tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.IntVar(),tk.IntVar()])

            self.column_up_inputs[-2][1].set('COL_UP_{0}'.format(self.beam_count))
            self.column_up_inputs[-2][2].set(10)
            self.column_up_inputs[-2][3].set(29000)
            self.column_up_inputs[-2][4].set(30.8)
            self.column_up_inputs[-2][5].set(2.96)
            self.column_up_inputs[-2][6].set(1)

            self.column_up_inputs[-1][1].set('COL_UP_{0}'.format(self.beam_count+1))
            self.column_up_inputs[-1][2].set(10)
            self.column_up_inputs[-1][3].set(29000)
            self.column_up_inputs[-1][4].set(30.8)
            self.column_up_inputs[-1][5].set(2.96)
            self.column_up_inputs[-1][6].set(1)

            self.column_down_inputs[-2][0].set('COL_DWN_{0}'.format(self.beam_count))
            self.column_down_inputs[-2][1].set(10)
            self.column_down_inputs[-2][2].set(29000)
            self.column_down_inputs[-2][3].set(30.8)
            self.column_down_inputs[-2][4].set(2.96)
            self.column_down_inputs[-2][5].set(1)

            self.column_down_inputs[-1][0].set('COL_DWN_{0}'.format(self.beam_count+1))
            self.column_down_inputs[-1][1].set(10)
            self.column_down_inputs[-1][2].set(29000)
            self.column_down_inputs[-1][3].set(30.8)
            self.column_down_inputs[-1][4].set(2.96)
            self.column_down_inputs[-1][5].set(1)
        else:
            self.column_up_inputs.append([tk.IntVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.IntVar(),tk.IntVar()])
            self.column_down_inputs.append([tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.IntVar(),tk.IntVar()])

            self.column_up_inputs[-1][1].set('COL_UP_{0}'.format(self.beam_count+1))
            self.column_up_inputs[-1][2].set(self.column_up_inputs[-2][2].get())
            self.column_up_inputs[-1][3].set(self.column_up_inputs[-2][3].get())
            self.column_up_inputs[-1][4].set(self.column_up_inputs[-2][4].get())
            self.column_up_inputs[-1][5].set(self.column_up_inputs[-2][5].get())
            self.column_up_inputs[-1][6].set(self.column_up_inputs[-2][6].get())

            self.column_down_inputs[-1][0].set('COL_DWN_{0}'.format(self.beam_count+1))
            self.column_down_inputs[-1][1].set(self.column_down_inputs[-2][1].get())
            self.column_down_inputs[-1][2].set(self.column_down_inputs[-2][2].get())
            self.column_down_inputs[-1][3].set(self.column_down_inputs[-2][3].get())
            self.column_down_inputs[-1][4].set(self.column_down_inputs[-2][4].get())
            self.column_down_inputs[-1][5].set(self.column_down_inputs[-2][5].get())

        self.beam_inputs[-1][0].set('BM_{0}'.format(self.beam_count))
        self.beam_labels.append('BM_{0}'.format(self.beam_count))
        self.refesh_span_options()

        self.build_bm_gui_table()
        self.build_colup_gui_table()
        self.build_coldwn_gui_table()

    def add_cant_left_func(self,*event):

        if self.cantL_count == 0:
            self.frame_built = 0
            self.frame_solved = 0
            self.cantL_count +=1
            self.b_remove_left_cant.configure(state=tk.NORMAL)
            self.b_add_left_cant.configure(state=tk.DISABLED)
            self.b_solve_frame.configure(state=tk.DISABLED, bg='red3')
            self.cantL_beam_inputs.append([tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()])
            self.cantL_beam_inputs[-1][1].set(5)
            self.cantL_beam_inputs[-1][2].set(29000)
            self.cantL_beam_inputs[-1][3].set(30.8)

            bm = self.cantL_beam_inputs[0]
            bm[0].set('CantL')
            self.beam_labels.append('CantL')
            self.refesh_span_options()

            a = tk.Entry(self.bm_info_tab,textvariable=bm[0], width=8, state=tk.DISABLED)
            a.grid(row=2,column=6)
            b = tk.Entry(self.bm_info_tab,textvariable=bm[1], width=8)
            b.grid(row=2,column=7)
            c = tk.Entry(self.bm_info_tab,textvariable=bm[2], width=8)
            c.grid(row=2,column=8)
            d = tk.Entry(self.bm_info_tab,textvariable=bm[3], width=8)
            d.grid(row=2,column=9)

            self.cantL_beam_gui_list.extend([a,b,c,d])

        else:
            pass

    def remove_left_cant_func(self,*event):
        if self.cantL_count > 0:
            self.frame_built = 0
            self.frame_solved = 0
            self.cantL_count -=1
            self.beam_labels.remove('CantL')
            self.refesh_span_options()
            self.b_remove_left_cant.configure(state=tk.DISABLED)
            self.b_solve_frame.configure(state=tk.DISABLED, bg='red3')
            self.b_add_left_cant.configure(state=tk.NORMAL)
            for element in self.cantL_beam_gui_list:
                element.destroy()

            del self.cantL_beam_gui_list[:]

    def remove_right_cant_func(self,*event):
        if self.cantR_count > 0:
            self.frame_built = 0
            self.frame_solved = 0
            self.cantR_count -=1
            self.beam_labels.remove('CantR')
            self.refesh_span_options()
            self.b_remove_right_cant.configure(state=tk.DISABLED)
            self.b_add_right_cant.configure(state=tk.NORMAL)
            self.b_solve_frame.configure(state=tk.DISABLED, bg='red3')
            for element in self.cantR_beam_gui_list:
                element.destroy()

            del self.cantR_beam_gui_list[:]

    def add_cant_right_func(self,*event):
        if self.cantR_count == 0:
            self.frame_built = 0
            self.frame_solved = 0
            self.cantR_count +=1
            self.b_remove_right_cant.configure(state=tk.NORMAL)
            self.b_add_right_cant.configure(state=tk.DISABLED)
            self.b_solve_frame.configure(state=tk.DISABLED, bg='red3')
            self.cantR_beam_inputs.append([tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()])
            self.cantR_beam_inputs[-1][1].set(5)
            self.cantR_beam_inputs[-1][2].set(29000)
            self.cantR_beam_inputs[-1][3].set(30.8)

            bm = self.cantR_beam_inputs[0]
            bm[0].set('CantR')
            self.beam_labels.append('CantR')
            self.refesh_span_options()

            a = tk.Entry(self.bm_info_tab,textvariable=bm[0], width=8, state=tk.DISABLED)
            a.grid(row=2,column=11)
            b = tk.Entry(self.bm_info_tab,textvariable=bm[1], width=8)
            b.grid(row=2,column=12)
            c = tk.Entry(self.bm_info_tab,textvariable=bm[2], width=8)
            c.grid(row=2,column=13)
            d = tk.Entry(self.bm_info_tab,textvariable=bm[3], width=8)
            d.grid(row=2,column=14)

            self.cantR_beam_gui_list.extend([a,b,c,d])

        else:
            pass

    def remove_last_beam_func(self,*event):
        if self.beam_count <= 1:
            pass
        else:
            self.b_solve_frame.configure(state=tk.DISABLED, bg='red3')
            self.beam_count -=1
            self.frame_built = 0
            self.frame_solved = 0
            self.beam_labels.remove(self.beam_inputs[-1][0].get())

            self.refesh_span_options()

            del self.beam_inputs[-1]
            del self.column_up_inputs[-1]
            del self.column_down_inputs[-1]

            self.build_bm_gui_table()
            self.build_colup_gui_table()
            self.build_coldwn_gui_table()

    def build_bm_gui_table(self,*event):

            for element in self.beam_gui_list:
                element.destroy()

            del self.beam_gui_list[:]

            for i,bm in enumerate(self.beam_inputs):

                a = tk.Entry(self.bm_info_tab,textvariable=bm[0], width=8, state=tk.DISABLED)
                a.grid(row=i+2,column=1, pady=4)
                b = tk.Entry(self.bm_info_tab,textvariable=bm[1], width=8)
                b.grid(row=i+2,column=2)
                c = tk.Entry(self.bm_info_tab,textvariable=bm[2], width=8)
                c.grid(row=i+2,column=3)
                d = tk.Entry(self.bm_info_tab,textvariable=bm[3], width=8)
                d.grid(row=i+2,column=4)

                self.beam_gui_list.extend([a,b,c,d])

    def build_colup_gui_table(self,*event):
        for element in self.column_up_gui_list:
            element.destroy()

        del self.column_up_gui_list[:]

        for i,col in enumerate(self.column_up_inputs):

            a = tk.Checkbutton(self.colup_info_tab,variable=col[0])
            a.grid(row=i+2,column=1)
            b = tk.Entry(self.colup_info_tab,textvariable=col[1], width=12, state=tk.DISABLED)
            b.grid(row=i+2,column=2)
            c = tk.Entry(self.colup_info_tab,textvariable=col[2], width=8)
            c.grid(row=i+2,column=3)
            d = tk.Entry(self.colup_info_tab,textvariable=col[3], width=8)
            d.grid(row=i+2,column=4)
            e = tk.Entry(self.colup_info_tab,textvariable=col[4], width=8)
            e.grid(row=i+2,column=5)
            f = tk.Entry(self.colup_info_tab,textvariable=col[5], width=8)
            f.grid(row=i+2,column=6)
            g = tk.Checkbutton(self.colup_info_tab,variable=col[6])
            g.grid(row=i+2,column=7)
            h = tk.Checkbutton(self.colup_info_tab,variable=col[7])
            h.grid(row=i+2,column=8)

            self.column_up_gui_list.extend([a,b,c,d,e,f,g,h])

    def build_coldwn_gui_table(self,*event):
        for element in self.column_down_gui_list:
            element.destroy()

        del self.column_down_gui_list[:]

        for i,col in enumerate(self.column_down_inputs):

            b = tk.Entry(self.coldwn_info_tab,textvariable=col[0], width=12, state=tk.DISABLED)
            b.grid(row=i+2,column=1)
            c = tk.Entry(self.coldwn_info_tab,textvariable=col[1], width=8)
            c.grid(row=i+2,column=2)
            d = tk.Entry(self.coldwn_info_tab,textvariable=col[2], width=8)
            d.grid(row=i+2,column=3)
            e = tk.Entry(self.coldwn_info_tab,textvariable=col[3], width=8)
            e.grid(row=i+2,column=4)
            f = tk.Entry(self.coldwn_info_tab,textvariable=col[4], width=8)
            f.grid(row=i+2,column=5)
            g = tk.Checkbutton(self.coldwn_info_tab,variable=col[5])
            g.grid(row=i+2,column=6)
            h = tk.Checkbutton(self.coldwn_info_tab,variable=col[6])
            h.grid(row=i+2,column=7)

            self.column_down_gui_list.extend([b,c,d,e,f,g,h])

    def refesh_span_options(self,*event):
        self.load_span_selection['menu'].delete(0,'end')
        for choice in self.beam_labels:
            self.load_span_selection['menu'].add_command(label=choice, command=tk._setit(self.load_span_select, choice))

    def add_load_gui(self,*event):
        span = self.load_span_select.get()
        w1 = float(self.w1_gui.get())
        w2 = float(self.w2_gui.get())
        a = float(self.a_gui.get())
        b = float(self.b_gui.get())
        type = self.load_type.get()
        kind = self.load_kind_select.get()

        self.gui_load_list.append([span,w1,w2,a,b,type,kind])
        self.b_change_load.configure(state=tk.DISABLED, bg='gray75')
        self.b_remove_load.configure(state=tk.DISABLED, bg='gray75')

        self.fill_load_listbox()

    def remove_load_gui(self,*event):
        if len(self.gui_load_list)==0:
            pass
        else:
            del self.gui_load_list[self.load_change_index]
            self.b_change_load.configure(state=tk.DISABLED, bg='gray75')
            self.b_remove_load.configure(state=tk.DISABLED, bg='gray75')
            self.fill_load_listbox()

    def change_load_gui(self,*event):
        del self.gui_load_list[self.load_change_index]
        self.b_change_load.configure(state=tk.DISABLED, bg='gray75')
        self.b_remove_load.configure(state=tk.DISABLED, bg='gray75')
        self.add_load_gui()

    def add_load_to_all_gui(self,*event):

        w1 = float(self.w1_gui.get())
        w2 = float(self.w2_gui.get())
        a = float(self.a_gui.get())
        b = float(self.b_gui.get())
        type = self.load_type.get()
        kind = self.load_kind_select.get()

        for beam_gui in self.beam_inputs:

            span = beam_gui[0].get()
            b_max = float(beam_gui[1].get())

            b_use = min(b,b_max)

            self.gui_load_list.append([span,w1,w2,a,b_use,type,kind])

        self.fill_load_listbox()

    def remove_all_loads_gui(self,*event):
        if len(self.gui_load_list)==0:
            pass
        else:
            del self.gui_load_list[:]
            self.b_change_load.configure(state=tk.DISABLED, bg='gray75')
            self.b_remove_load.configure(state=tk.DISABLED, bg='gray75')
            self.fill_load_listbox()

    def load_listbox_click(self,*event):
        if self.load_listbox.size()==0:
            pass
        else:
            self.b_change_load.configure(state=tk.NORMAL, bg='yellow2')
            self.b_remove_load.configure(state=tk.NORMAL, bg='red3')

            self.selected_load = self.load_listbox.get(self.load_listbox.curselection()[0]).split(',')
            self.load_change_index = self.load_listbox.curselection()[0]

            self.load_span_select.set(self.selected_load[0])
            self.w1_gui.set(self.selected_load[1])
            self.w2_gui.set(self.selected_load[2])
            self.a_gui.set(self.selected_load[3])
            self.b_gui.set(self.selected_load[4])
            self.load_type.set(self.selected_load[5])
            self.load_kind_select.set(self.selected_load[6])

    def fill_load_listbox(self,*event):
        self.b_solve_frame.configure(state=tk.DISABLED, bg='red3')
        self.frame_solved = 0

        self.load_listbox.delete(0,tk.END)

        color = "pale green"
        i=0
        for x in self.gui_load_list:
            self.load_listbox.insert(tk.END,'{0},{1:.3f},{2:.3f},{3:.3f},{4:.3f},{5},{6}'.format(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))

            if i % 2 == 0:
                self.load_listbox.itemconfigure(i, background=color)
            else:
                pass
            i+=1

    def build_frame_gui_func(self,*event):

        del self.beams_analysis[:]
        del self.nodes_analysis[:]
        del self.columns_analysis[:]
        self.max_h_up_graph = 0
        self.max_h_dwn_graph = 0

        self.nodes_analysis.append(frame2d.node(0))

        for beam_gui in self.beam_inputs:

            label = beam_gui[0].get()
            span = float(beam_gui[1].get())
            j = self.nodes_analysis[-1].x + span
            self.nodes_analysis.append(frame2d.node(j))
            newi = self.nodes_analysis[-2]
            newj = self.nodes_analysis[-1]
            E_ksf = float(beam_gui[2].get())*144.0 # k/in^2 * 144 in^2 / 1 ft^2 = 144 k/ft^2
            I_ft4 = float(beam_gui[3].get())*(1 / 20736.0) # in^4 * 1 ft^4 / 12^4 in^4 = ft^4

            beam = frame2d.Beam(newi,newj,E_ksf,I_ft4, [], label)

            self.beams_analysis.append(beam)

        for i,col in enumerate(self.column_down_inputs):
            j_node = self.nodes_analysis[i]
            height=float(col[1].get())
            E=float(col[2].get())*144.0 # k/in^2 * 144 in^2 / 1 ft^2 = 144 k/ft^2
            I=float(col[3].get())*(1 / 20736.0) # in^4 * 1 ft^4 / 12^4 in^4 = ft^4
            A=float(col[4].get())/144.0
            support=col[5].get()
            hinge_near=col[6].get()

            column_dwn = frame2d.Column_Down(j_node, height, E, I, A, support, hinge_near)

            self.max_h_dwn_graph = max(self.max_h_dwn_graph,height)

            self.columns_analysis.append(column_dwn)

        for i,col in enumerate(self.column_up_inputs):

            if col[0].get() == 1:
                pass

            else:
                i_node = self.nodes_analysis[i]
                height=float(col[2].get())
                E=float(col[3].get())*144.0 # k/in^2 * 144 in^2 / 1 ft^2 = 144 k/ft^2
                I=float(col[4].get())*(1 / 20736.0) # in^4 * 1 ft^4 / 12^4 in^4 = ft^4
                A=float(col[5].get())/144.0
                support=col[6].get()
                hinge_near=col[7].get()

                self.max_h_up_graph = max(self.max_h_up_graph,height)

                column_up = frame2d.Column_Up(i_node, height, E, I, A, support, hinge_near)

                self.columns_analysis.append(column_up)

        self.frame_built = 1
        self.frame_solved = 0

        self.b_solve_frame.configure(state=tk.NORMAL, bg='cornflower blue')

        self.build_frame_graph()

    def build_frame_graph(self,*event):
        if self.frame_built == 0:
            pass

        else:
            self.g_plan_canvas.delete("all")
            w = self.g_plan_canvas.winfo_width()
            h = self.g_plan_canvas.winfo_height()
            hg = (h/2.0)

            spacer= 30

            total_length = self.nodes_analysis[-1].x

            scale_x = (w - 2*spacer) / total_length

            scale_y = (hg-spacer)/ max(self.max_h_dwn_graph,self.max_h_up_graph)

            scale = min(scale_x, scale_y)

            for i,node in enumerate(self.nodes_analysis):
                if node == self.nodes_analysis[-1]:
                    pass
                else:
                    x1 = (node.x*scale) + spacer
                    x2 = (self.nodes_analysis[i+1].x*scale)+spacer
                    self.g_plan_canvas.create_line(x1, hg, x2, hg, fill="white", width=2)

            if self.frame_solved == 0:
                pass
            else:
                if self.show_dfs.get() == 1:
                    for beam in self.beams_analysis:
                        string = 'DFi: {0:.3f}\nDFj: {1:.3f} '.format(beam.dfi,beam.dfj)
                        x0 =  (((beam.i.x+beam.j.x)/2)*scale) + spacer

                        self.g_plan_canvas.create_text(x0, hg+12, anchor=tk.N, font=self.mono_f, text=string, fill='cyan')

                if self.show_v.get()==1:
                    v_scale = float(self.res_scale.get())
                    for beam in self.beams_analysis:
                        for i in range(1,len(beam.chart_stations)):
                            x1 = (beam.chart_stations[i-1]+beam.i.x)*scale + spacer
                            x2 = (beam.chart_stations[i]+beam.i.x)*scale + spacer
                            y1 = hg - (beam.station_values()[0][1][i-1] * v_scale)
                            y2 = hg - (beam.station_values()[0][1][i] * v_scale)

                            self.g_plan_canvas.create_line(x1, y1, x2, y2, fill="red", width=2)

                        string = 'Vi: {0:.2f} kips\nVj: {1:.2f} kips'.format(beam.station_values()[0][1][0],beam.station_values()[0][1][-1])
                        x0 =  (((beam.i.x+beam.j.x)/2)*scale) + spacer

                        self.g_plan_canvas.create_text(x0, hg+12, anchor=tk.N, font=self.mono_f, text=string, fill='red')

                if self.show_m.get()==1:
                    if self.show_m_tension.get() == 1:
                        m_scale = float(self.res_scale.get())* -1
                    else:
                        m_scale = float(self.res_scale.get())


                    for beam in self.beams_analysis:
                        string_max = ''
                        string_min = ''
                        for i in range(1,len(beam.chart_stations)):
                            x1 = (beam.chart_stations[i-1]+beam.i.x)*scale + spacer
                            x2 = (beam.chart_stations[i]+beam.i.x)*scale + spacer
                            y1 = hg - (beam.station_values()[0][2][i-1] * m_scale)
                            y2 = hg - (beam.station_values()[0][2][i] * m_scale)

                            self.g_plan_canvas.create_line(x1, y1, x2, y2, fill="green", width=2)


                            if beam.station_values()[0][2][i] == max(beam.station_values()[0][2]) and  beam.station_values()[0][2][i] != beam.station_values()[0][2][-1]:
                                string_max = '\nM,max {0:.2f} ft-kips @ {1:.2f} ft'.format(beam.station_values()[0][2][i],beam.chart_stations[i])


                            if beam.station_values()[0][2][i] == min(beam.station_values()[0][2]) and  beam.station_values()[0][2][i] != beam.station_values()[0][2][-1]:
                                string_min = '\nM,min {0:.2f} ft-kips @ {1:.2f} ft'.format(beam.station_values()[0][2][i],beam.chart_stations[i])

                        x0 =  (((beam.i.x+beam.j.x)/2)*scale) + spacer
                        string = 'Mi {0:.2f} ft-kips\nMj {1:.2f} ft-kips'.format(beam.station_values()[0][2][0],beam.station_values()[0][2][-1])
                        self.g_plan_canvas.create_text(x0, hg+12, anchor=tk.N, font=self.mono_f, text=string+string_max+string_min, fill='green')

                if self.show_s.get()==1:
                    s_scale = float(self.res_scale.get())
                    for beam in self.beams_analysis:
                        for i in range(1,len(beam.chart_stations)):
                            x1 = (beam.chart_stations[i-1]+beam.i.x)*scale + spacer
                            x2 = (beam.chart_stations[i]+beam.i.x)*scale + spacer
                            y1 = hg - ((beam.station_values()[0][3][i-1]/(beam.E*beam.I)) * s_scale)
                            y2 = hg - ((beam.station_values()[0][3][i]/(beam.E*beam.I)) * s_scale)

                            self.g_plan_canvas.create_line(x1, y1, x2, y2, fill="magenta", width=2)

                        string = 'Si: {0:.5f} rad\nSj: {1:.5f} rad'.format(beam.station_values()[0][3][0]/(beam.E*beam.I),beam.station_values()[0][3][-1]/(beam.E*beam.I))
                        x0 =  (((beam.i.x+beam.j.x)/2)*scale) + spacer

                        self.g_plan_canvas.create_text(x0, hg+12, anchor=tk.N, font=self.mono_f, text=string, fill='magenta')

                if self.show_d.get()==1:
                    d_scale = float(self.res_scale.get())
                    for beam in self.beams_analysis:
                        string_max = ''
                        string_min = ''
                        for i in range(1,len(beam.chart_stations)):
                            x1 = (beam.chart_stations[i-1]+beam.i.x)*scale + spacer
                            x2 = (beam.chart_stations[i]+beam.i.x)*scale + spacer
                            y1 = hg - ((beam.station_values()[0][4][i-1]/(beam.E*beam.I)) * d_scale * 12.0)
                            y2 = hg - ((beam.station_values()[0][4][i]/(beam.E*beam.I)) * d_scale * 12.0)

                            self.g_plan_canvas.create_line(x1, y1, x2, y2, fill="gray30", width=2)

                            if beam.station_values()[0][4][i] == max(beam.station_values()[0][4]) and  beam.station_values()[0][4][i] != beam.station_values()[0][4][-1]:
                                string_max = '\nD,max {0:.2f} in @ {1:.2f} ft'.format(12.0*beam.station_values()[0][4][i]/(beam.E*beam.I),beam.chart_stations[i])

                            if beam.station_values()[0][4][i] == min(beam.station_values()[0][4]) and  beam.station_values()[0][4][i] != beam.station_values()[0][4][-1]:
                                string_min = '\nD,min {0:.2f} in @ {1:.2f} ft'.format(12.0*beam.station_values()[0][4][i]/(beam.E*beam.I),beam.chart_stations[i])

                        x0 =  (((beam.i.x+beam.j.x)/2)*scale) + spacer
                        self.g_plan_canvas.create_text(x0, hg+12, anchor=tk.N, font=self.mono_f, text=string_max+string_min, fill='gray30')

            count = 0
            for col in self.columns_analysis:
                if col.type ==  'UP':
                    x = (col.i.x * scale) + spacer
                    h1 = hg
                    h2 = h1 - (col.Length*scale)
                    self.g_plan_canvas.create_line(x, h1, x, h2, fill="white", width=2)
                else:
                    x = (col.j.x * scale) + spacer
                    h1 = hg
                    h2 = h1 + (col.Length*scale)
                    self.g_plan_canvas.create_line(x, h1, x, h2, fill="white", width=2)

                if self.frame_solved == 0:
                    pass
                else:
                    if self.show_dfs.get()==1:
                        dfb = col.dfi
                        dft = col.dfj
                        string = 'DFi: {0:.3f}\nDFj: {1:.3f}'.format(dfb,dft)

                        if col.type == 'UP':
                            if count == 0:
                                self.g_plan_canvas.create_text(x, h1 - (col.Length*scale), anchor=tk.SW,font=self.mono_f, text=string, fill='cyan')
                            else:
                                self.g_plan_canvas.create_text(x, h1 - (col.Length*scale), anchor=tk.S,font=self.mono_f, text=string, fill='cyan')
                        else:
                            if count == 0:
                                self.g_plan_canvas.create_text(x, h1 + (col.Length*scale), anchor=tk.NW,font=self.mono_f, text=string, fill='cyan')
                            else:
                                self.g_plan_canvas.create_text(x, h1 + (col.Length*scale), anchor=tk.N,font=self.mono_f, text=string, fill='cyan')

                    if self.show_v.get()==1:
                        for i in range(1,len(col.chart_stations)):
                            if col.type == 'UP':
                                y1 = h1 - (col.chart_stations[i-1]*scale)
                                y2 = h1 - (col.chart_stations[i]*scale)
                            else:
                                y1 = h2 - (col.chart_stations[i-1]*scale)
                                y2 = h2 - (col.chart_stations[i]*scale)
                            x1 = x - (col.station_values()[1][i-1] * v_scale)
                            x2 = x - (col.station_values()[1][i] * v_scale)

                            self.g_plan_canvas.create_line(x1, y1, x2, y2, fill="red", width=1)

                        vb = col.station_values()[1][0]
                        vt = col.station_values()[1][-1]
                        string = 'Vi: {0:.2f} kips\nVj: {1:.2f} kips'.format(vb,vt)

                        if col.type == 'UP':
                            if count == 0:
                                self.g_plan_canvas.create_text(x, h1 - (col.Length*scale), anchor=tk.SW,font=self.mono_f, text=string, fill='red')
                            else:
                                self.g_plan_canvas.create_text(x, h1 - (col.Length*scale), anchor=tk.S,font=self.mono_f, text=string, fill='red')
                        else:
                            if count == 0:
                                self.g_plan_canvas.create_text(x, h1 + (col.Length*scale), anchor=tk.NW,font=self.mono_f, text=string, fill='red')
                            else:
                                self.g_plan_canvas.create_text(x, h1 + (col.Length*scale), anchor=tk.N,font=self.mono_f, text=string, fill='red')

                    if self.show_m.get()==1:
                        for i in range(1,len(col.chart_stations)):
                            if col.type == 'UP':
                                y1 = h1 - (col.chart_stations[i-1]*scale)
                                y2 = h1 - (col.chart_stations[i]*scale)
                            else:
                                y1 = h2 - (col.chart_stations[i-1]*scale)
                                y2 = h2 - (col.chart_stations[i]*scale)
                            x1 = x - (col.station_values()[2][i-1] * m_scale)
                            x2 = x - (col.station_values()[2][i] * m_scale)

                            self.g_plan_canvas.create_line(x1, y1, x2, y2, fill="green", width=1)

                        mb = col.station_values()[2][0]
                        mt = col.station_values()[2][-1]
                        string = 'Mi: {0:.2f} ft-kips\nMj: {1:.2f} ft-kips'.format(mb,mt)

                        if col.type == 'UP':
                            if count == 0:
                                self.g_plan_canvas.create_text(x, h1 - (col.Length*scale), anchor=tk.SW,font=self.mono_f, text=string, fill='green')
                            else:
                                self.g_plan_canvas.create_text(x, h1 - (col.Length*scale), anchor=tk.S,font=self.mono_f, text=string, fill='green')
                        else:
                            if count == 0:
                                self.g_plan_canvas.create_text(x, h1 + (col.Length*scale), anchor=tk.NW,font=self.mono_f, text=string, fill='green')
                            else:
                                self.g_plan_canvas.create_text(x, h1 + (col.Length*scale), anchor=tk.N,font=self.mono_f, text=string, fill='green')

                    if self.show_s.get()==1:
                        for i in range(1,len(col.chart_stations)):
                            if col.type == 'UP':
                                y1 = h1 - (col.chart_stations[i-1]*scale)
                                y2 = h1 - (col.chart_stations[i]*scale)
                            else:
                                y1 = h2 - (col.chart_stations[i-1]*scale)
                                y2 = h2 - (col.chart_stations[i]*scale)
                            x1 = x - ((col.station_values()[3][i-1]/(col.E*col.I)) * s_scale)
                            x2 = x - ((col.station_values()[3][i]/(col.E*col.I)) * s_scale)

                            self.g_plan_canvas.create_line(x1, y1, x2, y2, fill="magenta", width=1)

                        sb = col.station_values()[3][0]/(col.E*col.I)
                        st = col.station_values()[3][-1]/(col.E*col.I)
                        string = 'Si: {0:.5f} kips\nSj: {1:.5f} kips'.format(sb,st)

                        if col.type == 'UP':
                            if count == 0:
                                self.g_plan_canvas.create_text(x, h1 - (col.Length*scale), anchor=tk.SW,font=self.mono_f, text=string, fill='magenta')
                            else:
                                self.g_plan_canvas.create_text(x, h1 - (col.Length*scale), anchor=tk.S,font=self.mono_f, text=string, fill='magenta')
                        else:
                            if count == 0:
                                self.g_plan_canvas.create_text(x, h1 + (col.Length*scale), anchor=tk.NW,font=self.mono_f, text=string, fill='magenta')
                            else:
                                self.g_plan_canvas.create_text(x, h1 + (col.Length*scale), anchor=tk.N,font=self.mono_f, text=string, fill='magenta')

                    if self.show_d.get()==1:
                        for i in range(1,len(col.chart_stations)):
                            if col.type == 'UP':
                                y1 = h1 - (col.chart_stations[i-1]*scale)
                                y2 = h1 - (col.chart_stations[i]*scale)
                            else:
                                y1 = h2 - (col.chart_stations[i-1]*scale)
                                y2 = h2 - (col.chart_stations[i]*scale)
                            x1 = x - ((col.station_values()[4][i-1]/(col.E*col.I)) * d_scale * 12.0)
                            x2 = x - ((col.station_values()[4][i]/(col.E*col.I)) * d_scale * 12.0)

                            self.g_plan_canvas.create_line(x1, y1, x2, y2, fill="gray30", width=1)
                    count +=1

    def frame_analysis_gui(self, *event):
        sorted_load_list = []

        #sort the load list by beam
        for beam in self.beams_analysis:
            sorted_load_list.append([load for load in self.gui_load_list if load[0]==beam.label])

        # Determine number of Spans and load patterns
        # load patterns will be returned as a list of
        # off, on per span

        num_spans = len(self.beams_analysis)

        # Solve for each load case

        for i,beam in enumerate(self.beams_analysis):
            beam.new_load_list(sorted_load_list[i])

        Consider_shortening = 1

        frame2d.moment_distribution(self.nodes_analysis,self.beams_analysis,self.columns_analysis,Consider_shortening,1e-5)

        for beam in self.beams_analysis:
            beam.build_load_function()

        max_m = 0
        min_m = 0
        for beam in self.beams_analysis:

            if beam.type=='cantilever' and beam.isleft == 1:
                start_slope = beam_charts[0][0][3][0]/(beams[0].E*beams[0].I)

                beam.add_starting_slope(start_slope)
                beam.build_load_function()

            elif beam.type=='cantilever' and beam.isleft == 0:
                start_slope = beams[-3].station_values()[0][3][-1]/(beams[-1].E*beams[-1].I)
                beam.add_starting_slope(start_slope)
                beam.build_load_function()

            max_m = max(max_m,max(beam.station_values()[0][2]))
            min_m = min(min_m,min(beam.station_values()[0][2]))

        self.max_m = max_m
        self.min_m = min_m

        for column in self.columns_analysis:
            column.build_load_function()

        self.frame_solved = 1

        self.build_frame_graph()



def main():
    root = tk.Tk()
    root.title("2D Frame Analysis by Moment Distribution - Alpha")
    main_window(root)
    root.minsize(800,600)
    root.mainloop()

if __name__ == '__main__':
    main()
