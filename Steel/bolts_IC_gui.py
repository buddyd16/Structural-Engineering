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
import Tkinter as tk
import tkMessageBox
import ttk
import tkFont
import tkFileDialog
import bolt_group_istantaneous_center as bolt_ic

class main_window:

    def __init__(self, master):

        self.master = master
        self.inputs = []
        self.bolt_x_gui = []
        self.bolt_y_gui = []
        self.bolt_gui_elements = []
        self.xloc = []
        self.yloc = []
        self.bolt_count = 0
        self.hasrun=0
        #self.detailed_results_gui = []
        self.aisc_result_labels = []
        self.aisc_has_run = 0
        
        # Font Set
        self.f_size = 8
        self.helv = tkFont.Font(family=' Courier New',size=self.f_size, weight='bold')
        self.helv_norm = tkFont.Font(family=' Courier New',size=self.f_size)
        self.helv_res = tkFont.Font(family=' Courier New',size=self.f_size, weight='bold', underline = True)
        self.mono_f = tkFont.Font(family='Consolas',size=self.f_size)
        
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
        
        #Main Frame
        self.base_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.base_frame.pack(side=tk.BOTTOM, padx= 1, pady= 1, fill=tk.X)
        #Base Frame Items
        w=18
        h=1
        color='cornflower blue'
        self.b_quit = tk.Button(self.base_frame,text="Quit", command=self.quit_app, font=self.helv, width=w, height=h, bg='red3')
        self.b_quit.pack(side=tk.RIGHT)
        
        self.graphics_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.graphics_frame.pack(side=tk.RIGHT, padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        self.data_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.data_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
       
        #Main Notebooks
        self.nb_data = ttk.Notebook(self.data_frame)
        self.nb_data.pack(fill=tk.BOTH, expand=1)
        
        self.nb_graph = ttk.Notebook(self.graphics_frame)
        self.nb_graph.pack(fill=tk.BOTH, expand=1)
        
        #Graphics Frame tabs and canvases
        #Geometry - Plan
        self.graph_tab = ttk.Frame(self.nb_graph)
        self.nb_graph.add(self.graph_tab, text='Graph')
        
        self.g_plan_frame = tk.Frame(self.graph_tab, bd=2, relief='sunken', padx=1,pady=1)
        self.g_plan_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        self.g_plan_canvas = tk.Canvas(self.g_plan_frame, width=50, height=50, bd=2, relief='sunken', background="black")
        self.g_plan_canvas.bind("<Configure>", self.draw_bolts)
        self.g_plan_canvas.pack(side = tk.LEFT, anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        
        #Detailed Out - Tab
        self.detail_tab = ttk.Frame(self.nb_graph)
        self.nb_graph.add(self.detail_tab, text='Detailed Results')
        
        self.detailed_res_frame = tk.Frame(self.detail_tab, bd=2, relief='sunken', padx=1,pady=1)
        self.results_text_box = tk.Text(self.detailed_res_frame, bg= "grey90", font= self.mono_f, wrap=tk.WORD)
        self.results_text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.res_txt_scroll = tk.Scrollbar(self.detailed_res_frame, command=self.results_text_box.yview)
        self.res_txt_scroll.pack(side=tk.LEFT, fill=tk.Y)
        
        self.results_text_box['yscrollcommand'] = self.res_txt_scroll.set
        
        self.detailed_res_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)
        
        #Convergance Graph
        self.converge_graph_tab = ttk.Frame(self.nb_graph)
        self.nb_graph.add(self.converge_graph_tab, text='Convergance Graph')
        
        self.g_converge_frame = tk.Frame(self.converge_graph_tab, bd=2, relief='sunken', padx=1,pady=1)
        self.g_converge_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)
        
        self.g_converge_canvas = tk.Canvas(self.g_converge_frame, width=50, height=50, bd=2, relief='sunken', background="black")
        self.g_converge_canvas.bind("<Configure>", self.draw_converge)
        self.g_converge_canvas.pack(side = tk.LEFT, anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        #C stability Graph
        self.c_stab_graph_tab = ttk.Frame(self.nb_graph)
        self.nb_graph.add(self.c_stab_graph_tab, text='C Stability Graph')
        
        self.g_c_stab_frame = tk.Frame(self.c_stab_graph_tab, bd=2, relief='sunken', padx=1,pady=1)

        self.g_c_stab_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)
        
        self.g_c_stab_canvas = tk.Canvas(self.g_c_stab_frame, width=50, height=50, bd=2, relief='sunken', background="black")
        self.g_c_stab_canvas.bind("<Configure>", self.draw_c_stability)
        self.g_c_stab_canvas.pack(side = tk.LEFT, anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        
        #Data/calc Frame tabs
        #Load location Angle and add bolts
        self.basic_input = ttk.Frame(self.nb_data)
        self.nb_data.add(self.basic_input, text='Geometry Input')
        self.data_frame = tk.Frame(self.basic_input, bd=2, relief='sunken', padx=1,pady=1)
        
        # Load - x
        tk.Label(self.data_frame, text="load x: (in):", font=self.helv).grid(row=0, column=0, sticky=tk.E)
        self.load_x_gui = tk.StringVar()
        self.inputs.append(self.load_x_gui)
        self.load_x_gui.set('5.0')
        self.load_x_entry = tk.Entry(self.data_frame, textvariable=self.load_x_gui, width=10)
        self.load_x_entry.grid(row=0, column=1)

        # Load - y
        tk.Label(self.data_frame, text="load y: (in):", font=self.helv).grid(row=1, column=0, sticky=tk.E)
        self.load_y_gui = tk.StringVar()
        self.inputs.append(self.load_y_gui)
        self.load_y_gui.set('5.0')
        self.load_y_entry = tk.Entry(self.data_frame, textvariable=self.load_y_gui, width=10)
        self.load_y_entry.grid(row=1, column=1)
        
        # Load - angle
        tk.Label(self.data_frame, text="load angle: (degrees):", font=self.helv).grid(row=2, column=0, sticky=tk.E)
        self.load_angle_gui = tk.StringVar()
        self.inputs.append(self.load_angle_gui)
        self.load_angle_gui.set('5.0')
        self.load_angle_entry = tk.Entry(self.data_frame, textvariable=self.load_angle_gui, width=10)
        self.load_angle_entry.grid(row=2, column=1)
        
        tk.Label(self.data_frame, text="Bolts :", font=self.helv).grid(row=3, column=0, sticky=tk.W)
        
        #Start X
        tk.Label(self.data_frame, text="x (in) :", font=self.helv).grid(row=4, column=0, sticky=tk.E)
        self.bolt_x_in = tk.StringVar()
        self.bolt_x_in.set('0.0')
        self.bolt_x_entry = tk.Entry(self.data_frame, textvariable=self.bolt_x_in, width=10)
        self.bolt_x_entry.grid(row=4, column=1)

        #Start Y
        tk.Label(self.data_frame, text="y (in) :", font=self.helv).grid(row=5, column=0, sticky=tk.E)
        self.bolt_y_in = tk.StringVar()
        self.bolt_y_in.set('0.0')
        self.bolt_y_entry= tk.Entry(self.data_frame, textvariable=self.bolt_y_in, width=10)
        self.bolt_y_entry.grid(row=5, column=1)

        # Button to Add Segment
        self.b_add_bolt = tk.Button(self.data_frame,text="Add Bolt", command=self.add_bolt, font=self.helv, width=15, height=h, bg=color)
        self.b_add_bolt.grid(row=6, column=0)
        
        # Button to Romove Segment
        self.b_remove_bolt = tk.Button(self.data_frame,text="Remove Last Bolt", command=self.remove_bolt, font=self.helv, width=15, height=h, bg=color)
        self.b_remove_bolt.grid(row=6, column=1)
        
        self.bolt_frame = tk.Frame(self.data_frame)
        self.bolt_input_canvas = tk.Canvas(self.bolt_frame, background="gray", width=50, height=200)
        self.bolt_canvas_frame = tk.Frame(self.bolt_input_canvas)
        self.scrollforcanvas = tk.Scrollbar(self.bolt_frame, orient="vertical", command=self.bolt_input_canvas.yview)
        self.scrollforcanvas.pack(side=tk.RIGHT, fill="y")
        self.bolt_input_canvas.pack(side=tk.LEFT, fill="both", expand=True)
        self.bolt_input_canvas.create_window(0,0, window=self.bolt_canvas_frame, anchor="nw", tags="self.bolt_canvas_frame")
        self.bolt_input_canvas.configure(yscrollcommand=self.scrollforcanvas.set)
        self.bolt_frame.grid(row=7, column=0, columnspan=3, sticky=tk.NSEW)
        
        self.bolt_canvas_frame.bind("<Configure>", self.onFrameConfigure)
        
        # Button run
        self.b_run = tk.Button(self.data_frame,text="Run", command=self.run, font=self.helv, width=15, height=h, bg=color)
        self.b_run.grid(row=8, column=0)
        
        self.ic_x_gui = tk.StringVar()
        self.ic_x_gui.set("--")
        tk.Label(self.data_frame, text="IC x: (in)", font=self.helv).grid(row=9, column=0, sticky=tk.E)
        tk.Entry(self.data_frame, textvariable=self.ic_x_gui, width=10).grid(row=9, column=1)
        
        self.ic_y_gui = tk.StringVar()
        self.ic_y_gui.set("--")
        tk.Label(self.data_frame, text="IC y: (in)", font=self.helv).grid(row=10, column=0, sticky=tk.E)
        tk.Entry(self.data_frame, textvariable=self.ic_y_gui, width=10).grid(row=10, column=1)
        
        self.cu_gui = tk.StringVar()
        self.cu_gui.set("--")
        tk.Label(self.data_frame, text="Cu: ", font=self.helv).grid(row=11, column=0, sticky=tk.E)
        tk.Entry(self.data_frame, textvariable=self.cu_gui, width=10).grid(row=11, column=1)
        
        self.solution_gui = tk.StringVar()
        self.solution_gui.set("--")
        tk.Label(self.data_frame, text="Solution Useable: ", font=self.helv).grid(row=12, column=0, sticky=tk.E)
        tk.Entry(self.data_frame, textvariable=self.solution_gui, width=10).grid(row=12, column=1)
        
        self.cu_maybe_gui = tk.StringVar()
        self.cu_maybe_gui.set("--")
        tk.Label(self.data_frame, text="Predicted Cu: ", font=self.helv).grid(row=11, column=3, sticky=tk.E)
        tk.Entry(self.data_frame, textvariable=self.cu_maybe_gui, width=10).grid(row=11, column=4)
        
        self.tol_overide_gui = tk.StringVar()
        self.tol_overide_gui.set("--")
        tk.Label(self.data_frame, text="Tolerance Overide: \nDefualt: 1E-6\n-- = no overide", font=self.helv).grid(row=9, column=3, sticky=tk.E)
        tk.Entry(self.data_frame, textvariable=self.tol_overide_gui, width=10).grid(row=9, column=4)
        
        self.tol_achieved_gui = tk.StringVar()
        self.tol_achieved_gui.set("--")
        tk.Label(self.data_frame, text="Tolerance reached:", font=self.helv).grid(row=10, column=3, sticky=tk.E)
        tk.Entry(self.data_frame, textvariable=self.tol_achieved_gui, width=10).grid(row=10, column=4)
        
        self.data_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)
        
        #AISC Table Verification
        self.aisc_verify_input = ttk.Frame(self.nb_data)
        self.nb_data.add(self.aisc_verify_input, text='AISC Table 7.7-7.14 Verification')
        self.aisc_verify_frame = tk.Frame(self.aisc_verify_input, bd=2, relief='sunken', padx=1,pady=1)
        
        # To match AISC table need to know:
        # Number of Columns of Bolts
        # Number of Rows of Bolts
        # Spacing of Columns, in.
        # Spacing of Rows, in.
        # Load Angle from Vertical, degrees
        # x eccentricity from bolt group centroid to load
        # y eccentricity = 0
        
        self.aisc_ex = [2,3,4,5,6,7,8,9,10,12,14,16,18,20,24,28,32,36]
        
        self.aisc_numCols = tk.StringVar()
        self.aisc_numCols.set("1")
        tk.Label(self.aisc_verify_frame, text="Number of Columns:", font=self.helv).grid(row=0, column=0, sticky=tk.E)
        tk.Entry(self.aisc_verify_frame,textvariable=self.aisc_numCols, width=10).grid(row=0, column=1)
        
        self.aisc_numRows = tk.StringVar()
        self.aisc_numRows.set("2")
        tk.Label(self.aisc_verify_frame, text="Number of Rows:", font=self.helv).grid(row=0, column=2, sticky=tk.E)
        tk.Entry(self.aisc_verify_frame,textvariable=self.aisc_numRows, width=10).grid(row=0, column=3)
        
        self.aisc_colspacing = tk.StringVar()
        self.aisc_colspacing.set("2")
        tk.Label(self.aisc_verify_frame, text="Column Spacing (in):", font=self.helv).grid(row=1, column=0, sticky=tk.E)
        tk.Entry(self.aisc_verify_frame,textvariable=self.aisc_colspacing, width=10).grid(row=1, column=1)
        
        self.aisc_rowspacing = tk.StringVar()
        self.aisc_rowspacing.set("3")
        tk.Label(self.aisc_verify_frame, text="Row Spacing (in):", font=self.helv).grid(row=1, column=2, sticky=tk.E)
        tk.Entry(self.aisc_verify_frame,textvariable=self.aisc_rowspacing, width=10).grid(row=1, column=3)
        
        self.aisc_loadangle = tk.StringVar()
        self.aisc_loadangle.set("0")
        tk.Label(self.aisc_verify_frame, text="Load Angle from Vertical (degrees):", font=self.helv).grid(row=2, column=0, columnspan=2, sticky=tk.E)
        tk.Entry(self.aisc_verify_frame,textvariable=self.aisc_loadangle, width=10).grid(row=2, column=2)
        
        tk.Label(self.aisc_verify_frame, text="ex (in):", font=self.helv).grid(row=3, column=0, sticky=tk.E)
        
        i=4
        for ex in self.aisc_ex:
            tk.Label(self.aisc_verify_frame, text='{0}'.format(ex), font=self.helv).grid(row=i, column=0, sticky=tk.E)
            i+=1
        
        # Button run AISC check
        self.b_run_aisc = tk.Button(self.aisc_verify_frame,text="Calc AISC Table", command=self.run_aisc, font=self.helv, width=15, height=h, bg=color)
        self.b_run_aisc.grid(row=i+1, column=0)
        
        self.aisc_verify_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)
        # Call function to display license dialog on app start
        self.license_display()
    
    def license_display(self, *event):
        # Function to display license dialog on app start
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
    
    def add_bolt(self, *event):
        self.hasrun=0
        self.bolt_count +=1
        
        for element in self.bolt_gui_elements:
            element.destroy()
            
        del self.bolt_gui_elements[:]
            
        self.bolt_x_gui.append(tk.StringVar())
        self.bolt_y_gui.append(tk.StringVar())
        
        x = self.bolt_x_in.get()
        y = self.bolt_y_in.get()
        
        self.bolt_x_gui[-1].set(x)
        self.bolt_y_gui[-1].set(y)
        
        for i in range(self.bolt_count):
            c = tk.Label(self.bolt_canvas_frame, text="Bolt {0}".format(i), font=self.helv)
            c.grid(row=i, column=0, sticky=tk.W)
            a = tk.Entry(self.bolt_canvas_frame, textvariable=self.bolt_x_gui[i], width=10)
            a.grid(row=i, column=1)
            b = tk.Entry(self.bolt_canvas_frame, textvariable=self.bolt_y_gui[i], width=10)
            b.grid(row=i, column=2)
            
            self.bolt_gui_elements.append(c)
            self.bolt_gui_elements.append(a)
            self.bolt_gui_elements.append(b)
            
        self.draw_bolts()
        self.onFrameConfigure()
        
    def remove_bolt(self, *event):
        self.hasrun=0
        if self.bolt_count == 0:
            pass
        else:
            self.bolt_count -=1
            
            for element in self.bolt_gui_elements:
                element.destroy()
            
            del self.bolt_x_gui[-1]
            del self.bolt_y_gui[-1]
            
            for i in range(self.bolt_count):
                c = tk.Label(self.bolt_canvas_frame, text="Bolt {0}".format(i), font=self.helv)
                c.grid(row=i, column=0, sticky=tk.W)
                a = tk.Entry(self.bolt_canvas_frame, textvariable=self.bolt_x_gui[i], width=10)
                a.grid(row=i, column=1)
                b = tk.Entry(self.bolt_canvas_frame, textvariable=self.bolt_y_gui[i], width=10)
                b.grid(row=i, column=2)
                
                self.bolt_gui_elements.append(c)
                self.bolt_gui_elements.append(a)
                self.bolt_gui_elements.append(b)
            
            self.draw_bolts()
            self.onFrameConfigure()
            
    def onFrameConfigure(self, *event):
        '''Reset the scroll region to encompass the inner frame'''
        self.bolt_input_canvas.configure(scrollregion=self.bolt_input_canvas.bbox("all"))
    
    def run(self, *event):
        if self.bolt_count < 2:
            pass
        
        else:
            xloc = []
            yloc = []
            
            p_xloc = float(self.load_x_gui.get())
            p_yloc = float(self.load_y_gui.get())
            p_angle = float(self.load_angle_gui.get())
            
            for x in self.bolt_x_gui:
                xloc.append(float(x.get()))
                
            for y in self.bolt_y_gui:
                yloc.append(float(y.get()))
            tol = self.tol_overide_gui.get()
            if tol == "--":
                tol= 0.000001
            else:
                tol=float(tol)
                
            res = bolt_ic.brandt(xloc,yloc,p_xloc,p_yloc,p_angle,tol)
            
            self.IC = res[1]
            self.Cu = res[2]
            self.detailed_out = res[0]
            
            self.ic_x_gui.set("{0:.3f}".format(self.IC[0]))
            self.ic_y_gui.set("{0:.3f}".format(self.IC[1]))
            self.cu_gui.set("{0:.3f}".format(self.Cu))
            self.solution_gui.set(self.detailed_out[12][1])
            self.cu_maybe_gui.set("{0:.3f}".format(self.detailed_out[15][1]))
            self.tol_achieved_gui.set("{:.3E}".format(min(self.detailed_out[17][0])))
            
            self.hasrun=1
            self.draw_bolts()
            self.fill_details()
            self.draw_converge()
            self.draw_c_stability()
            
    def draw_bolts(self,*event):
        self.g_plan_canvas.delete("all")
        w = self.g_plan_canvas.winfo_width()
        h = self.g_plan_canvas.winfo_height()
        
        # x y arrows
        coord_start = 10
        self.g_plan_canvas.create_line(coord_start,h-coord_start,coord_start+50,h-coord_start, fill='green', width=1, arrow=tk.LAST)
        self.g_plan_canvas.create_text(coord_start+50,h-(coord_start+8), text='x', fill='green')
        self.g_plan_canvas.create_line(coord_start,h-coord_start,coord_start,h-(coord_start+50), fill='green', width=1, arrow=tk.LAST)
        self.g_plan_canvas.create_text(coord_start+8,h-(coord_start+50), text='y', fill='green')
        
        # Load angle
        self.g_plan_canvas.create_line(coord_start+70,h-coord_start,coord_start+125,h-(coord_start+50), fill='green', width=1, arrow=tk.FIRST)
        self.g_plan_canvas.create_line(coord_start+70,h-coord_start,coord_start+125,h-coord_start, fill='green', width=1)
        self.g_plan_canvas.create_text(coord_start+100,h-(coord_start+10), text='angle', fill='green')
        
        if self.bolt_count < 2:
            pass
        else:
            xloc = []
            yloc = []
            
            p_xloc = float(self.load_x_gui.get())
            p_yloc = float(self.load_y_gui.get())
            p_angle = float(self.load_angle_gui.get())
            
            px_2 = (m.cos(m.radians(p_angle))*3)+ p_xloc
            py_2 = (m.sin(m.radians(p_angle))*3) + p_yloc
            
            for x in self.bolt_x_gui:
                xloc.append(float(x.get()))
                
            for y in self.bolt_y_gui:
                yloc.append(float(y.get()))
            
            if self.hasrun == 1:
                ic_x = self.IC[0]
                ic_y = self.IC[1]
            else:
                ic_x = xloc[-1]
                ic_y = yloc[-1]
                
            min_x = min(min(xloc),p_xloc,px_2,ic_x)
            min_y = min(min(yloc),p_yloc,py_2,ic_y)
            
            max_x = max(max(xloc),p_xloc,px_2,ic_x) - min_x
            max_y = max(max(yloc),p_yloc,py_2,ic_y) - min_y
            
            max_dim_for_scale = max(max_x,max_y)
            
            initial = 80
            
            if max_x == 0:
                sf_x = (w - (2*initial))
            else:
                sf_x = (w - (2*initial)) / max_dim_for_scale
            
            if max_y == 0:
                sf_y = (h - (2*initial))
            else:
                sf_y = (h - (2*initial)) / max_dim_for_scale
            
            #Load Line
            x0 = ((p_xloc - min_x)*sf_x) + initial
            y0 = h - (((p_yloc - min_y)*sf_y) + initial)
            x1 = ((px_2 - min_x)*sf_x) + initial
            y1 = h - (((py_2 - min_y)*sf_y) + initial)
            self.g_plan_canvas.create_line(x0,y0,x1,y1, fill='blue', width=1, arrow=tk.FIRST)
            
            #Bolts
            for x,y in zip(xloc,yloc):
                x0 = (((x - min_x) * sf_x) + initial)-5
                y0 = h-(((y - min_y)*sf_y)+initial)+5
                x1 = (((x - min_x) * sf_x) + initial)+5
                y1 = h-(((y - min_y)*sf_y)+initial)-5
                self.g_plan_canvas.create_oval(x0,y0,x1,y1, fill='green', width=1)
            
            #IC
            x0 = (((ic_x - min_x) * sf_x) + initial)-5
            y0 = h-(((ic_y - min_y)*sf_y)+initial)+5
            x1 = (((ic_x - min_x) * sf_x) + initial)+5
            y1 = h-(((ic_y - min_y)*sf_y)+initial)-5
            self.g_plan_canvas.create_oval(x0,y0,x1,y1, fill='red', width=1)
            
            #CG
            if self.hasrun == 0:
                cg = [0,0]
            else:
                cg = self.detailed_out[1][1]
            x0 = (((cg[0] - min_x) * sf_x) + initial)-5
            y0 = h-(((cg[1] - min_y)*sf_y)+initial)
            x1 = (((cg[0] - min_x) * sf_x) + initial)+5
            y1 = h-(((cg[1] - min_y)*sf_y)+initial)
            self.g_plan_canvas.create_line(x0,y0,x1,y1, fill='green', width=1)
            
            x0 = (((cg[0] - min_x) * sf_x) + initial)
            y0 = h-(((cg[1] - min_y)*sf_y)+initial)-5
            x1 = (((cg[0] - min_x) * sf_x) + initial)
            y1 = h-(((cg[1] - min_y)*sf_y)+initial)+5
            self.g_plan_canvas.create_line(x0,y0,x1,y1, fill='green', width=1)

    def fill_details(self,*event):
        self.results_text_box.delete(1.0,tk.END)
        if self.hasrun == 0:
            pass
        else:
            string = "Number of Bolts: {0}".format(self.detailed_out[0])
            
            cg = self.detailed_out[1][1]
            
            string = string + "\nBolt Group Centroid: ({0:.3f},{1:.3f})".format(cg[0],cg[1])
            
            string = string + "\nBolt Group J: {0:.3f}".format(self.detailed_out[2][1])
            
            string = string + "\n\nUnit Forces:"
            
            string = string + "\nPx,unit: {0:.3f}\nPy,unit: {1:.3f}\nMo = {2:.3f}".format(self.detailed_out[3][1],self.detailed_out[3][2], self.detailed_out[4][1])
            
            p_xloc = float(self.load_x_gui.get())
            p_yloc = float(self.load_y_gui.get())
            p_angle = float(self.load_angle_gui.get())
            
            ex = abs(self.detailed_out[1][1][0] - p_xloc)
            ey = abs(self.detailed_out[1][1][1] - p_yloc)
            
            px_2 = (m.cos(m.radians(p_angle))*3)+ p_xloc
            py_2 = (m.sin(m.radians(p_angle))*3) + p_yloc
            
            e = abs(((py_2 - p_yloc)*cg[0]) - ((px_2-p_xloc)*cg[1]) + (px_2*p_yloc) - (py_2*p_xloc)) / m.sqrt(((py_2-p_yloc)*(py_2-p_yloc)) + ((px_2 - p_xloc)*(px_2 - p_xloc)))
            
            string = string + "\n\nLoad Location: ({0:.3f},{1:.3f})\nLoad Angle:{2:.3f}\nex = {3:.3f}\ney = {4:.3f}\ne = {5:.3f}".format(p_xloc,p_yloc,p_angle,ex,ey,e)
            
            string = string + "\n\n{0} {1}\n{2} {3}\n".format(self.detailed_out[12][0],self.detailed_out[12][1],self.detailed_out[12][2],self.detailed_out[12][3])
            
            string = string + "\nSum Rx: {0}\nSum Ry: {1}\nSum Mi: {2}\n\nFxx = Px-Rx = {3}\nFyy = Py-Ry = {4}\nF = {5}\nMp = {8}\n\nFprev = {6}\nCuprev = {7}\nax = {9}\nay = {10}".format(self.detailed_out[13][1],self.detailed_out[13][3],self.detailed_out[13][5],self.detailed_out[10][1],self.detailed_out[10][3],self.detailed_out[10][5],self.detailed_out[16][0],self.detailed_out[16][2],self.detailed_out[14][3],self.detailed_out[18][0],self.detailed_out[18][1])
            
            string = string + "\n\n|{0:.^11}|{1:.^11}|{2:.^11}|{3:.^11}|{4:.^11}|{5:.^11}|{6:.^11}|{7:.^11}|{8:.^11}|\n".format("Bolt","x to IC","y to IC","di","deltai","R/Rult","Mi","Fxi","Fyi")
            
            for i in range(self.detailed_out[0]):
                string = string + "|{0:_^11}".format(i+1)
                
                for res in self.detailed_out[13][7]:
                        string = string + "|{0:_^ 11.3f}".format(res[1][i])
                        
                string = string + "|\n"
            self.results_text_box.insert(tk.END, string)

    def draw_converge(self, *events):
        self.g_converge_canvas.delete("all")
        w = self.g_converge_canvas.winfo_width()
        h = self.g_converge_canvas.winfo_height()
        
        if self.hasrun == 0:
            pass
        else:
            
            vals = self.detailed_out[17][0]
            
            norm_vals = [float(i)/max(vals) for i in vals]
            
            count = len(vals)
            
            max_dim_for_scale = count
                        
            initial = 80
            
            sf_x = (w - (2*initial)) / max_dim_for_scale
                
            #x - axis:
            x0 = initial
            y0 = h - initial
            x1 = w - initial
            y1 = h - initial
            self.g_converge_canvas.create_line(x0,y0,x1,y1, fill='green', width=1)
            
            #y - axis
            x0 = initial
            y0 = h - initial
            x1 = initial
            y1 = initial
            self.g_converge_canvas.create_line(x0,y0,x1,y1, fill='green', width=1)
            
            #max val label + line
            x0 = initial
            y0 = initial
            x1 = x0 - 5
            y1 = initial
            self.g_converge_canvas.create_line(x0,y0,x1,y1, fill='green', width=1)

            if max(vals)<0.01:
                string = "{:.3E}".format(max(vals))
            else:
                string = '{0:.3f}'.format(max(vals))

            self.g_converge_canvas.create_text(x1-35,initial, text=string, fill='green')

            #min val label + line
            x0 = initial
            y0 = (h-initial) - (min(norm_vals) * (h - (2*initial)))
            x1 = x0 - 5
            y1 = (h-initial) - (min(norm_vals) * (h - (2*initial)))
            self.g_converge_canvas.create_line(x0,y0,x1,y1, fill='green', width=1)

            if min(vals)<0.01:
                string = "{:.3E}".format(min(vals))
            else:
                string = '{0:.3f}'.format(min(vals))
            self.g_converge_canvas.create_text(x1-35,y0, text=string, fill='green')
           
            x = 0
            for i in range(len(norm_vals)):
                x0 = (((x) * sf_x) + initial)
                y0 = h - initial
                x1 = x0
                y1 = h - (initial-5)
                self.g_converge_canvas.create_line(x0,y0,x1,y1, fill='green', width=1)
                x+=1
            
            x = 0
            for y in range(len(norm_vals)):
                if y+1 > len(norm_vals)-1:
                    pass
                else:                    
                    x0 = (((x) * sf_x) + initial)
                    y0 = (h-initial) - (norm_vals[y] * (h - (2*initial)))
                    x1 = (((x+1) * sf_x) + initial)
                    y1 = (h-initial) - (norm_vals[y+1] * (h - (2*initial)))
                    
                    
                    if y0<=y1:
                        color = "blue"
                    else:
                        color = "red"
                        
                    self.g_converge_canvas.create_line(x0,y0,x1,y1, fill=color, width=1)
                    
                    x+=1

    def draw_c_stability(self, *events):
        self.g_c_stab_canvas.delete("all")
        w = self.g_c_stab_canvas.winfo_width()
        h = self.g_c_stab_canvas.winfo_height()
        
        if self.hasrun == 0:
            pass
        else:
            
            vals = self.detailed_out[17][1]
            
            if max(vals)-min(vals) == 0:
                norm_vals = [(float(i))/(max(vals)) for i in vals]
            else:
                norm_vals = [(float(i)-min(vals))/(max(vals)-min(vals)) for i in vals]
            
            count = len(vals)
            
            max_dim_for_scale = count
                        
            initial = 80
            
            sf_x = (w - (2*initial)) / max_dim_for_scale
            sf_y = (h - (2*initial))
                
            #x - axis:
            x0 = initial
            y0 = h - initial
            x1 = w - initial
            y1 = h - initial
            self.g_c_stab_canvas.create_line(x0,y0,x1,y1, fill='green', width=1)
            

            #y - axis
            x0 = initial
            y0 = h - initial
            x1 = initial
            y1 = initial
            self.g_c_stab_canvas.create_line(x0,y0,x1,y1, fill='green', width=1)
            
            #max val label + line
            x0 = initial
            y0 = initial
            x1 = x0 - 5
            y1 = initial
            self.g_c_stab_canvas.create_line(x0,y0,x1,y1, fill='green', width=1)
            self.g_c_stab_canvas.create_text(x1-35,initial, text='{0:.4f}'.format(max(vals)), fill='green')

            #min val label + line
            x0 = initial
            y0 = (h-initial) - (min(norm_vals) * sf_y)
            x1 = x0 - 5
            y1 = (h-initial) - (min(norm_vals) * sf_y)
            self.g_c_stab_canvas.create_line(x0,y0,x1,y1, fill='green', width=1)
            self.g_c_stab_canvas.create_text(x1-35,y0, text='{0:.4f}'.format(min(vals)), fill='green')
            
            x = 0
            for i in range(len(norm_vals)):
                x0 = (((x) * sf_x) + initial)
                y0 = h - initial
                x1 = x0
                y1 = h - (initial-5)
                self.g_c_stab_canvas.create_line(x0,y0,x1,y1, fill='green', width=1)
                x+=1
            
            x = 0
            for y in range(len(norm_vals)):
                if y+1 > len(norm_vals)-1:
                    pass
                else:                    
                    x0 = (((x) * sf_x) + initial)
                    y0 = (h-initial) - (norm_vals[y] * sf_y)
                    x1 = (((x+1) * sf_x) + initial)
                    y1 = (h-initial) - (norm_vals[y+1] * sf_y)
                                       
                    if y0<=y1:
                        color = "blue"
                    else:
                        color = "red"
                        
                    self.g_c_stab_canvas.create_line(x0,y0,x1,y1, fill=color, width=1)
                    
                    x+=1
                    
    def run_aisc(self, *events):
        self.aisc_has_run = 0
        for element in self.aisc_result_labels:
            element.destroy()
        
        del self.aisc_result_labels[:]
        
        cols = int(self.aisc_numCols.get())
        rows = int(self.aisc_numRows.get())
        colspacing = float(self.aisc_colspacing.get())
        rowspacing = float(self.aisc_rowspacing.get())
        angle_input = float(self.aisc_loadangle.get())
        angle_use = 90 - angle_input
        
        if cols == 0  or rows == 0:
            pass
        else:
        
            x,y = bolt_ic.build_bolt_group(cols, rows, colspacing, rowspacing)
            
            cg = bolt_ic.bolt_group_center(x,y)
            
            i=4
            for ex in self.aisc_ex:
                
                p_xloc = cg[0]+ex
                p_yloc = cg[1]
                p_angle = angle_use
                tol = 0.00001
                res = bolt_ic.brandt(x,y,p_xloc,p_yloc,p_angle,tol)
                
                c_string = '{0:.2f}'.format(res[2])
                label = tk.Label(self.aisc_verify_frame, text=c_string, font=self.helv)
                label.grid(row=i, column=1)
                self.aisc_result_labels.append(label)
                
                i+=1
                
            self.aisc_has_run = 1
            self.send_aisc_geometry(x,y)
    
    def send_aisc_geometry(self,xloc,yloc, *events):
        if self.aisc_has_run == 0:
            pass
        
        else:
            self.hasrun=0
            for element in self.bolt_gui_elements:
                element.destroy()
            
            del self.bolt_gui_elements[:]
            del self.bolt_x_gui[:]
            del self.bolt_y_gui[:]
            
            self.bolt_count = len(xloc)
            
            for i in range(len(xloc)):
            
                self.bolt_x_gui.append(tk.StringVar())
                self.bolt_y_gui.append(tk.StringVar())
                
                x = xloc[i]
                y = yloc[i]
                
                self.bolt_x_gui[-1].set(x)
                self.bolt_y_gui[-1].set(y)
                
            for i in range(self.bolt_count):
                c = tk.Label(self.bolt_canvas_frame, text="Bolt {0}".format(i), font=self.helv)
                c.grid(row=i, column=0, sticky=tk.W)
                a = tk.Entry(self.bolt_canvas_frame, textvariable=self.bolt_x_gui[i], width=10)
                a.grid(row=i, column=1)
                b = tk.Entry(self.bolt_canvas_frame, textvariable=self.bolt_y_gui[i], width=10)
                b.grid(row=i, column=2)
                
                self.bolt_gui_elements.append(c)
                self.bolt_gui_elements.append(a)
                self.bolt_gui_elements.append(b)
                
            self.draw_bolts()
        
def main():
    root = tk.Tk()
    root.title("Bolt Group Coefficient - Alpha")
    main_window(root)
    root.minsize(1150,600)
    root.mainloop()

if __name__ == '__main__':
    main()
