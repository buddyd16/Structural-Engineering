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
        tk.Label(self.snow_data_frame, text="Pg (psf):", font=self.helv_res).grid(row=0, column=0)
        self.pg_psf_gui = tk.StringVar()
        self.inputs.append(self.pg_psf_gui)
        self.pg_psf_gui.set('25.0')
        self.pg_entry = tk.Entry(self.snow_data_frame, textvariable=self.pg_psf_gui, width=10)
        self.pg_entry.grid(row=0, column=1)

        #snow_density_pcf = min((0.13*pg_psf) + 14, 30)
        #Ce = 1.0
        #Ct = 1.0
        #Cs = 1.0
        #I = 1.0
        #pf_psf = 0.7*Ce*Ct*I*pg_psf
        #ps_psf = Cs*pf_psf
        #hb_ft = ps_psf/snow_density_pcf
        self.snow_data_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

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
        
def main():
    root = tk.Tk()
    root.title("Snow Drift by Polygons - Alpha")
    main_window(root)
    root.minsize(1280,800)
    root.mainloop()

if __name__ == '__main__':
    main()
