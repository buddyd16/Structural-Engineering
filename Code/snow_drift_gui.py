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
import snow_drift_by_polygons as snow_drift

class main_window:

    def __init__(self, master):

        self.master = master
        self.inputs = []
        self.calc_balance = 0
        self.segment_list = []
        self.segment_list_gui = []
        self.drift_run = 0
        
        # Font Set
        self.f_size = 8
        self.helv = tkFont.Font(family=' Courier New',size=self.f_size, weight='bold')
        self.helv_norm = tkFont.Font(family=' Courier New',size=self.f_size)
        self.helv_res = tkFont.Font(family=' Courier New',size=self.f_size, weight='bold', underline = True)
        
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
        w=20
        h=2
        color='cornflower blue'
        self.b_quit = tk.Button(self.base_frame,text="Quit", command=self.quit_app, font=self.helv, width=w, height=h, bg='red3')
        self.b_quit.pack(side=tk.RIGHT)
        
        self.graphics_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)

        self.graphics_frame_l = tk.Frame(self.graphics_frame, padx=1,pady=1)
        self.graphics_frame_l.pack(side = tk.LEFT, anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        self.graphics_frame_r = tk.Frame(self.graphics_frame, padx=1,pady=1)
        
        self.graphics_frame_r.pack(side = tk.RIGHT, anchor='ne')

        self.graphics_frame.pack(side=tk.RIGHT, padx= 1, pady= 1, fill=tk.BOTH, expand=1)

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
        self.nb_graphs.add(self.g_plan, text='Plan')

        self.g_plan_frame = tk.Frame(self.g_plan, bd=2, relief='sunken', padx=1,pady=1)
        self.g_plan_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        self.g_plan_canvas = tk.Canvas(self.g_plan_frame, width=50, height=50, bd=2, relief='sunken', background="black")
        self.g_plan_canvas.bind("<Configure>", self.draw_drift)
        self.g_plan_canvas.pack(side = tk.LEFT, anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        #Geometry - Elevation/Section
        self.g_elev  = ttk.Frame(self.nb_graphs)
        self.nb_graphs.add(self.g_elev , text='Drift Section')

        self.g_elev_frame = tk.Frame(self.g_elev, bd=2, relief='sunken', padx=1,pady=1)
        self.g_elev_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        self.g_elev_canvas = tk.Canvas(self.g_elev_frame, width=50, height=50, bd=2, relief='sunken', background="black")
        #self.g_elev_canvas.bind("<Configure>", self.draw_elevation)
        self.g_elev_canvas.pack(side = tk.LEFT, anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        
        #Data/calc Frame tabs
        #Basic Snow
        self.snow_input = ttk.Frame(self.nb_data)
        self.nb_data.add(self.snow_input, text='Basic Snow Input')

        self.snow_data_frame = tk.Frame(self.snow_input, bd=2, relief='sunken', padx=1,pady=1)
        
        # Pg - ground snow load
        tk.Label(self.snow_data_frame, text="Pg (psf):", font=self.helv).grid(row=0, column=0, sticky=tk.E)
        self.pg_psf_gui = tk.StringVar()
        self.inputs.append(self.pg_psf_gui)
        self.pg_psf_gui.set('25.0')
        self.pg_entry = tk.Entry(self.snow_data_frame, textvariable=self.pg_psf_gui, width=10)
        self.pg_entry.grid(row=0, column=1)

        # Ce - exposure factor
        tk.Label(self.snow_data_frame, text="Ce :", font=self.helv).grid(row=1, column=0, sticky=tk.E)
        self.ce_gui = tk.StringVar()
        self.inputs.append(self.ce_gui)
        self.ce_gui.set('1.0')
        self.ce_entry = tk.Entry(self.snow_data_frame, textvariable=self.ce_gui, width=10)
        self.ce_entry.grid(row=1, column=1)

        # Ct - thermal factor
        tk.Label(self.snow_data_frame, text="Ct :", font=self.helv).grid(row=2, column=0, sticky=tk.E)
        self.ct_gui = tk.StringVar()
        self.inputs.append(self.ct_gui)
        self.ct_gui.set('1.0')
        self.ct_entry = tk.Entry(self.snow_data_frame, textvariable=self.ct_gui, width=10)
        self.ct_entry.grid(row=2, column=1)

        # Cs - slope factor
        tk.Label(self.snow_data_frame, text="Cs :", font=self.helv).grid(row=3, column=0, sticky=tk.E)
        self.cs_gui = tk.StringVar()
        self.inputs.append(self.cs_gui)
        self.cs_gui.set('1.0')
        self.cs_entry = tk.Entry(self.snow_data_frame, textvariable=self.cs_gui, width=10)
        self.cs_entry.grid(row=3, column=1)

        # I - Importance Factor
        tk.Label(self.snow_data_frame, text="I :", font=self.helv).grid(row=4, column=0, sticky=tk.E)
        self.I_gui = tk.StringVar()
        self.inputs.append(self.I_gui)
        self.I_gui.set('1.0')
        self.I_entry = tk.Entry(self.snow_data_frame, textvariable=self.I_gui, width=10)
        self.I_entry.grid(row=4, column=1)
        
        self.b_snow_basic = tk.Button(self.snow_data_frame,text="Calc Balance Snow", command=self.snow_step_1, font=self.helv, width=w, height=h, bg=color)
        self.b_snow_basic.grid(row=5, column=1)
       
        tk.Label(self.snow_data_frame, text="Snow Density (pcf) :", font=self.helv).grid(row=6, column=0, sticky=tk.E)
        tk.Label(self.snow_data_frame, text="min. of:", font=self.helv).grid(row=7, column=0, sticky=tk.E)
        tk.Label(self.snow_data_frame, text="0.13*Pg + 14", font=self.helv).grid(row=7, column=1)
        tk.Label(self.snow_data_frame, text="30", font=self.helv).grid(row=8, column=1)
        self.snow_density_pcf_gui = tk.Label(self.snow_data_frame, text="--", font=self.helv_res)
        self.snow_density_pcf_gui.grid(row=8, column=2)
        
        #Pf - Flat Roof Snow Load
        tk.Label(self.snow_data_frame, text="Pf (psf) :", font=self.helv).grid(row=9, column=0, sticky=tk.E)
        tk.Label(self.snow_data_frame, text="0.7*Ce*Ct*I*Pg", font=self.helv).grid(row=9, column=1)
        self.pf_psf_gui = tk.Label(self.snow_data_frame, text="--", font=self.helv_res)
        self.pf_psf_gui.grid(row=9, column=2)

        #Ps - ??
        tk.Label(self.snow_data_frame, text="Ps (psf) :", font=self.helv).grid(row=10, column=0, sticky=tk.E)
        tk.Label(self.snow_data_frame, text="Cs*Pf", font=self.helv).grid(row=10, column=1)
        self.ps_psf_gui = tk.Label(self.snow_data_frame, text="--", font=self.helv_res)
        self.ps_psf_gui.grid(row=10, column=2)       
        
        #Hb - depth of balance snow load
        tk.Label(self.snow_data_frame, text="Hb (ft) :", font=self.helv).grid(row=11, column=0, sticky=tk.E)
        tk.Label(self.snow_data_frame, text="Ps/Snow Density", font=self.helv).grid(row=11, column=1)
        self.hb_ft_gui = tk.Label(self.snow_data_frame, text="--", font=self.helv_res)
        self.hb_ft_gui.grid(row=11, column=2)   

        self.snow_data_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        #Segment Add Frame
        self.segment_input = ttk.Frame(self.nb_data)
        self.nb_data.add(self.segment_input, text='Segment Input')

        self.segment_data_frame = tk.Frame(self.segment_input, bd=2, relief='sunken', padx=1,pady=1)
        #Start X
        tk.Label(self.segment_data_frame, text="x1 (ft) :", font=self.helv).grid(row=0, column=0, sticky=tk.E)
        self.segment_start_x_ft = tk.StringVar()
        self.segment_start_x_ft.set('0.0')
        self.start_x_entry = tk.Entry(self.segment_data_frame, textvariable=self.segment_start_x_ft, width=10)
        self.start_x_entry.grid(row=0, column=1)

        #Start Y
        tk.Label(self.segment_data_frame, text="y1 (ft) :", font=self.helv).grid(row=1, column=0, sticky=tk.E)
        self.segment_start_y_ft = tk.StringVar()
        self.segment_start_y_ft.set('0.0')
        self.start_y_entry= tk.Entry(self.segment_data_frame, textvariable=self.segment_start_y_ft, width=10)
        self.start_y_entry.grid(row=1, column=1)

        #End X
        tk.Label(self.segment_data_frame, text="x2 (ft) :", font=self.helv).grid(row=2, column=0, sticky=tk.E)
        self.segment_end_x_ft = tk.StringVar()
        self.segment_end_x_ft.set('0.0')
        self.end_x_entry= tk.Entry(self.segment_data_frame, textvariable=self.segment_end_x_ft, width=10)
        self.end_x_entry.grid(row=2, column=1)

        #End Y
        tk.Label(self.segment_data_frame, text="y2 (ft) :", font=self.helv).grid(row=3, column=0, sticky=tk.E)
        self.segment_end_y_ft = tk.StringVar()
        self.segment_end_y_ft.set('0.0')
        self.end_y_entry= tk.Entry(self.segment_data_frame, textvariable=self.segment_end_y_ft, width=10)
        self.end_y_entry.grid(row=3, column=1)

        #Location Exterior (Counter-Clock-Wise) vs Interior (Clock-Wise)
        tk.Label(self.segment_data_frame, text="Location (e or i):", font=self.helv).grid(row=4, column=0, sticky=tk.E)
        self.segment_location = tk.StringVar()
        self.segment_location.set('e')
        self.segment_add_menu = tk.OptionMenu(self.segment_data_frame, self.segment_location, 'e', 'i')
        self.segment_add_menu.config(font=self.helv)
        self.segment_add_menu.grid(row=4, column=1, padx= 2, sticky=tk.W)
        tk.Label(self.segment_data_frame, text="e = exterior -- segments must be defined counter clockwise", font=self.helv).grid(row=5, column=0, columnspan=3, sticky=tk.W)
        tk.Label(self.segment_data_frame, text="i = interior -- segments must be defined counter clockwise", font=self.helv).grid(row=6, column=0, columnspan=3, sticky=tk.W)        
        
        #Segment Height - min of 3" or 0.25 ft
        tk.Label(self.segment_data_frame, text="Hc (ft): ", font=self.helv).grid(row=7, column=0, sticky=tk.E)
        self.segment_hc_ft = tk.StringVar()
        self.segment_hc_ft.set('0.25')
        self.hc_entry= tk.Entry(self.segment_data_frame, textvariable=self.segment_hc_ft, width=10)
        self.hc_entry.grid(row=7, column=1)
        self.segment_data_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        # Important note
        tk.Label(self.segment_data_frame, text="Note: base program assumption is exterior segments form a closed polygon\nclose off free edges with an Hc = 0.001 ft.", font=self.helv).grid(row=8, column=0,columnspan=3, sticky=tk.E)

        # Button to Add Segment
        self.b_add_segment = tk.Button(self.segment_data_frame,text="Add Segment", command=self.add_segment, font=self.helv, width=15, height=h, bg=color)
        self.b_add_segment.grid(row=9, column=0)
        
        # Button to Romove Segment
        self.b_remove_segment = tk.Button(self.segment_data_frame,text="Remove Last", command=self.remove_segment, font=self.helv, width=15, height=h, bg=color)
        self.b_remove_segment.grid(row=9, column=1)
        
        # List box of segments
        # GUI segment list is different from used segment list
        # used segment list will be determined at run time and 
        # will pull the most current GUI segment list to perform
        # calculations and GUI Canvas drawing
        self.segment_list_frame = tk.Frame(self.segment_data_frame, padx=1,pady=1)
        self.segment_list_frame.grid(row=10, column=0,columnspan=3)
        
        self.segment_listbox = tk.Listbox(self.segment_list_frame,width=75, height=20, font=self.helv)
        self.segment_listbox.pack(side=tk.LEFT, fill=tk.Y)
        
        self.segment_listbox_scroll = tk.Scrollbar(self.segment_list_frame, orient="vertical")
        self.segment_listbox_scroll.config(command=self.segment_listbox.yview)
        self.segment_listbox_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.segment_listbox.config(yscrollcommand = self.segment_listbox_scroll.set)
        
        # Button to Run Drift All
        self.b_run = tk.Button(self.segment_data_frame,text="Calc Drifts", command=self.run_drift_all, font=self.helv, width=15, height=h, bg=color)

        self.b_run.grid(row=11, column=0)

        # Button to export DXF
        self.b_run = tk.Button(self.segment_data_frame,text="Export DXF", command=self.exp_dxf, font=self.helv, width=15, height=h, bg=color)
        self.b_run.grid(row=11, column=1)

        self.draw_drift()
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

    def snow_step_1(self, *event):
        self.pg_psf = float(self.pg_psf_gui.get())
        self.snow_density_pcf = min((0.13*self.pg_psf) + 14, 30)
        self.snow_density_pcf_gui.config(text='{0:.3f}'.format(self.snow_density_pcf))

        self.ce = float(self.ce_gui.get())
        self.ct = float(self.ct_gui.get())
        self.I = float(self.I_gui.get())
        self.cs = float(self.cs_gui.get())

        self.pf_psf = 0.7*self.ce*self.ct*self.I*self.pg_psf
        self.pf_psf_gui.config(text='{0:.3f}'.format(self.pf_psf))

        self.ps_psf = self.cs*self.pf_psf
        self.ps_psf_gui.config(text='{0:.3f}'.format(self.ps_psf))
        self.hb_ft = self.ps_psf/self.snow_density_pcf
        self.hb_ft_gui.config(text='{0:.3f}'.format(self.hb_ft))
        
        self.calc_balance = 1
    
    def add_segment(self, *event):
        self.drift_run = 0
        x0 = float(self.segment_start_x_ft.get())
        y0 = float(self.segment_start_y_ft.get())
        x1 = float(self.segment_end_x_ft.get())
        y1 = float(self.segment_end_y_ft.get())
        
        location = self.segment_location.get()
        
        hc_ft = float(self.segment_hc_ft.get())

        uid = len(self.segment_list)
        
        start = [x0,y0]
        end = [x1,y1]
        
        text = 'Segment: i[{0:.2f},{1:.2f}] j[{2:.2f},{3:.2f}],{4},height: {5:.2f}ft'.format(x0,y0,x1,y1,location,hc_ft)
        
        self.segment_list_gui.append(text)
        self.segment_list.append(snow_drift.Line([x0,y0],[x1,y1],hc_ft,uid,location))
        
        self.fill_gui_segment_list()
        self.draw_drift()
        
    def remove_segment(self, *event):
        self.drift_run = 0
        del self.segment_list_gui[-1]
        del self.segment_list[-1]

        self.fill_gui_segment_list()
        self.draw_drift()
    
    def fill_gui_segment_list(self,*event):
        self.segment_listbox.delete(0,tk.END)
        
        for item in self.segment_list_gui:
            self.segment_listbox.insert(tk.END,item)
            

    def draw_drift(self, *event):
        self.g_plan_canvas.delete("all")
        w = self.g_plan_canvas.winfo_width()
        h = self.g_plan_canvas.winfo_height()
        
        # x y arrows
        coord_start = 10
        self.g_plan_canvas.create_line(coord_start,h-coord_start,coord_start+50,h-coord_start, fill='green', width=1, arrow=tk.LAST)
        self.g_plan_canvas.create_text(coord_start+50,h-(coord_start+8), text='x', fill='green')
        self.g_plan_canvas.create_line(coord_start,h-coord_start,coord_start,h-(coord_start+50), fill='green', width=1, arrow=tk.LAST)
        self.g_plan_canvas.create_text(coord_start+8,h-(coord_start+50), text='y', fill='green')
        
        if len(self.segment_list) == 0:
            pass
        else:
            min_x = min(min([line.start[0] for line in self.segment_list]), min([line.end[0] for line in self.segment_list]))
            min_y = min(min([line.start[1] for line in self.segment_list]), min([line.end[1] for line in self.segment_list]))
            
            max_x = max(max([line.start[0] for line in self.segment_list]), max([line.end[0] for line in self.segment_list])) - min_x
            max_y = max(max([line.start[1] for line in self.segment_list]), max([line.end[1] for line in self.segment_list])) - min_y
            
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

            
            for line in self.segment_list:
                x0 = ((line.start[0] - min_x) * sf_x) + initial
                y0 = h - (((line.start[1] - min_y) * sf_y) + initial)
                x1 = ((line.end[0] - min_x) * sf_x) + initial
                y1 = h - (((line.end[1] - min_y) * sf_y) + initial)
                
                if line.location == 'e':
                    color = 'blue'
                else:
                    color = 'red'

                self.g_plan_canvas.create_line(x0,y0,x1,y1, fill=color, width=2)

                if self.drift_run == 0:
                    pass
                else:
                    k=0
                    prev_label = ''
                    for point in line.internal_points_x:
                        x2 = ((line.internal_points_x[k] - min_x) * sf_x) + initial
                        y2 = h - (((line.internal_points_y[k] - min_y) * sf_y) + initial)
                        x3 = ((line.drift_line_x[k] - min_x) * sf_x) + initial
                        y3 = h - (((line.drift_line_y[k] - min_y) * sf_y) + initial)
                        self.g_plan_canvas.create_line(x2,y2,x3,y3, fill='green', width=2)

                        k+=1
                

    def run_drift_all(self, *event):
        if len(self.segment_list) <3:
            pass
        else:
            snow_drift.drift_all(self.segment_list, self.snow_density_pcf, self.pg_psf,25, 0)
            self.drift_run = 1
            self.draw_drift()
               
    def exp_dxf(self, *event):
        if self.drift_run == 0:
            pass
        else:
            snow_drift.export_dxf('test.dxf', self.segment_list) 
      
def main():
    root = tk.Tk()
    root.title("Snow Drift by Polygons - Alpha")
    main_window(root)
    root.minsize(1024,768)
    root.mainloop()

if __name__ == '__main__':
    main()
