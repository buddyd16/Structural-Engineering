# -*- coding: utf-8 -*-

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
import math as m
import Tkinter as tk
import tkMessageBox
import ttk
import tkFont
import tkFileDialog

class main_window:

    def __init__(self, master):

        self.master = master
        self.inputs = []
        self.calc_balance = 0
        
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

        self.g_plan_canvas = tk.Canvas(self.g_plan_frame, width=50, height=50, bd=2, relief='sunken', background="gray60")
        #self.g_plan_canvas.bind("<Configure>", self.draw_plan)
        self.g_plan_canvas.pack(side = tk.LEFT, anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        #Geometry - Elevation/Section
        self.g_elev  = ttk.Frame(self.nb_graphs)
        self.nb_graphs.add(self.g_elev , text='Drift Section')

        self.g_elev_frame = tk.Frame(self.g_elev, bd=2, relief='sunken', padx=1,pady=1)
        self.g_elev_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        self.g_elev_canvas = tk.Canvas(self.g_elev_frame, width=50, height=50, bd=2, relief='sunken', background="gray60")
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

        # Ce - ground snow load
        tk.Label(self.snow_data_frame, text="Ce :", font=self.helv).grid(row=1, column=0, sticky=tk.E)
        self.ce_gui = tk.StringVar()
        self.inputs.append(self.ce_gui)
        self.ce_gui.set('1.0')
        self.ce_entry = tk.Entry(self.snow_data_frame, textvariable=self.ce_gui, width=10)
        self.ce_entry.grid(row=1, column=1)

        # Ct - ground snow load
        tk.Label(self.snow_data_frame, text="Ct :", font=self.helv).grid(row=2, column=0, sticky=tk.E)
        self.ct_gui = tk.StringVar()
        self.inputs.append(self.ct_gui)
        self.ct_gui.set('1.0')
        self.ct_entry = tk.Entry(self.snow_data_frame, textvariable=self.ct_gui, width=10)
        self.ct_entry.grid(row=2, column=1)

        # Cs - ground snow load
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
        tk.Label(self.segment_data_frame, text="i = interior -- segments must be defined clockwise", font=self.helv).grid(row=6, column=0, columnspan=3, sticky=tk.W)        
        
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

        # Button to Change Segment

        # Button to Romove Segment

        # List box of segments
        # GUI segment list is different from used segment list
        # used segment list will be determined at run time and 
        # will pull the most current GUI segment list to perform
        # calculations and GUI Canvas drawing


        # Call function to display license dialog on app start
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
                    "\nA copy of the License can be viewed at:\n https://github.com/buddyd16/Structural-Engineering/blob/master/LICENSE")
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

def main():
    root = tk.Tk()
    root.title("Snow Drift by Polygons - Alpha")
    main_window(root)
    root.minsize(1024,768)
    root.mainloop()

if __name__ == '__main__':
    main()
