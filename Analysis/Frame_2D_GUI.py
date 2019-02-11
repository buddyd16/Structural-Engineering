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
import Frame_Moment_Distribution_2D as md_2dframe

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

        self.load_types = ['Point','Moment','UDL','TRAP']

        # Font Set
        self.f_size = 10
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

        #Base Frame
        self.base_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.base_frame.pack(side=tk.BOTTOM, padx= 1, pady= 1, fill=tk.X)
        #Base Frame Items
        w=20
        h=1

        self.b_quit = tk.Button(self.base_frame,text="Quit", command=self.quit_app, font=self.helv, width=w, height=h, bg='red3')
        self.b_quit.pack(side=tk.RIGHT)

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
        tk.Label(self.colup_info_tab, text='Fixed Base:').grid(row=1, column=7)
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
        self.g_loads_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        #Graphics Frame tabs and canvases
        #Geometry - Graph
        self.graph_tab = ttk.Frame(self.nb_data)
        self.nb_data.add(self.graph_tab, text='Graph')

        self.g_a_frame = tk.Frame(self.graph_tab, bd=2, relief='sunken', padx=1,pady=1)
        self.g_a_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        self.g_plan_canvas = tk.Canvas(self.g_a_frame, width=50, height=50, bd=2, relief='sunken', background="black")
        #self.g_plan_canvas.bind("<Configure>", self.draw_frame)
        self.g_plan_canvas.pack(side = tk.LEFT, anchor='w', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        self.graph_b_frame = tk.Frame(self.g_a_frame, bd=2, relief='sunken', padx=4 ,pady=1)

        self.show_l = tk.IntVar()
        self.show_l.set(1)
        tk.Checkbutton(self.graph_b_frame, text=' : Show Loads', variable=self.show_l, font=self.helv).grid(row=1, column=1, sticky = tk.W)
        self.show_v = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show V', variable=self.show_v, font=self.helv).grid(row=2, column=1, sticky = tk.W)
        self.show_m = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show M', variable=self.show_m, font=self.helv).grid(row=3, column=1, sticky = tk.W)
        self.show_s = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show S', variable=self.show_s, font=self.helv).grid(row=4, column=1, sticky = tk.W)
        self.show_d = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show D', variable=self.show_d, font=self.helv).grid(row=5, column=1, sticky = tk.W)
        self.show_r = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show Reactions', variable=self.show_r, font=self.helv).grid(row=6, column=1, sticky = tk.W)
        self.show_stations = tk.IntVar()
        tk.Checkbutton(self.graph_b_frame, text=' : Show Stations', variable=self.show_stations, font=self.helv).grid(row=7, column=1, sticky = tk.W)
        self.show_m_tension = tk.IntVar()
        self.show_m_tension.set(1)
        tk.Checkbutton(self.graph_b_frame, text=' : Show M on\ntension face', variable=self.show_m_tension, font=self.helv).grid(row=8, column=1, sticky = tk.W)

        self.graph_b_frame.pack(side=tk.RIGHT, anchor='e')

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
                    "\nA copy of the License can be viewed at:\n"
                    "https://github.com/buddyd16/Structural-Engineering/blob/master/LICENSE")
        tkMessageBox.showerror("License Information",license_string)
        self.master.focus_force()

    def quit_app(self):
        self.master.quit()
        self.master.destroy()

    def add_beam_func(self):

        self.beam_count +=1

        self.b_remove_beam.configure(state=tk.NORMAL)

        self.beam_inputs.append([tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()])

        if self.beam_count == 1:
            self.column_up_inputs.append([tk.IntVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.IntVar(),tk.IntVar()])
            self.column_up_inputs.append([tk.IntVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.IntVar(),tk.IntVar()])
            self.column_down_inputs.append([tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.IntVar(),tk.IntVar()])
            self.column_down_inputs.append([tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.IntVar(),tk.IntVar()])

            self.column_up_inputs[-2][1].set('COL_UP_{0}'.format(self.beam_count))
            self.column_up_inputs[-1][1].set('COL_UP_{0}'.format(self.beam_count+1))
            self.column_down_inputs[-2][0].set('COL_DNW_{0}'.format(self.beam_count))
            self.column_down_inputs[-1][0].set('COL_DWN_{0}'.format(self.beam_count+1))
        else:
            self.column_up_inputs.append([tk.IntVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.IntVar(),tk.IntVar()])
            self.column_down_inputs.append([tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.IntVar(),tk.IntVar()])

            self.column_up_inputs[-1][1].set('COL_UP_{0}'.format(self.beam_count+1))
            self.column_down_inputs[-1][0].set('COL_DWN_{0}'.format(self.beam_count+1))

        self.beam_inputs[-1][0].set('BM_{0}'.format(self.beam_count))

        self.build_bm_gui_table()
        self.build_colup_gui_table()
        self.build_coldwn_gui_table()

    def add_cant_left_func(self):
        if self.cantL_count == 0:
            self.cantL_count +=1
            self.b_remove_left_cant.configure(state=tk.NORMAL)
            self.b_add_left_cant.configure(state=tk.DISABLED)
            self.cantL_beam_inputs.append([tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()])

            bm = self.cantL_beam_inputs[0]
            bm[0].set('CantL')
            a = tk.Entry(self.bm_info_tab,textvariable=bm[0], width=8)
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

    def remove_left_cant_func(self):
        if self.cantL_count > 0:
            self.cantL_count -=1
            self.b_remove_left_cant.configure(state=tk.DISABLED)
            self.b_add_left_cant.configure(state=tk.NORMAL)
            for element in self.cantL_beam_gui_list:
                element.destroy()

            del self.cantL_beam_gui_list[:]

    def remove_right_cant_func(self):
        if self.cantR_count > 0:
            self.cantR_count -=1
            self.b_remove_right_cant.configure(state=tk.DISABLED)
            self.b_add_right_cant.configure(state=tk.NORMAL)
            for element in self.cantR_beam_gui_list:
                element.destroy()

            del self.cantR_beam_gui_list[:]

    def add_cant_right_func(self):
        if self.cantR_count == 0:
            self.cantR_count +=1
            self.b_remove_right_cant.configure(state=tk.NORMAL)
            self.b_add_right_cant.configure(state=tk.DISABLED)
            self.cantR_beam_inputs.append([tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()])

            bm = self.cantR_beam_inputs[0]
            bm[0].set('CantR')
            a = tk.Entry(self.bm_info_tab,textvariable=bm[0], width=8)
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

    def remove_last_beam_func(self):
        if self.beam_count <= 1:
            pass
        else:
            self.beam_count -=1

            del self.beam_inputs[-1]
            del self.column_up_inputs[-1]
            del self.column_down_inputs[-1]

            self.build_bm_gui_table()
            self.build_colup_gui_table()
            self.build_coldwn_gui_table()

    def build_bm_gui_table(self):

            for element in self.beam_gui_list:
                element.destroy()

            del self.beam_gui_list[:]

            for i,bm in enumerate(self.beam_inputs):

                a = tk.Entry(self.bm_info_tab,textvariable=bm[0], width=8)
                a.grid(row=i+2,column=1)
                b = tk.Entry(self.bm_info_tab,textvariable=bm[1], width=8)
                b.grid(row=i+2,column=2)
                c = tk.Entry(self.bm_info_tab,textvariable=bm[2], width=8)
                c.grid(row=i+2,column=3)
                d = tk.Entry(self.bm_info_tab,textvariable=bm[3], width=8)
                d.grid(row=i+2,column=4)

                self.beam_gui_list.extend([a,b,c,d])

    def build_colup_gui_table(self):
        for element in self.column_up_gui_list:
            element.destroy()

        del self.column_up_gui_list[:]

        for i,col in enumerate(self.column_up_inputs):

            a = tk.Checkbutton(self.colup_info_tab,variable=col[0])
            a.grid(row=i+2,column=1)
            b = tk.Entry(self.colup_info_tab,textvariable=col[1], width=12)
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

    def build_coldwn_gui_table(self):
        for element in self.column_down_gui_list:
            element.destroy()

        del self.column_down_gui_list[:]

        for i,col in enumerate(self.column_down_inputs):

            b = tk.Entry(self.coldwn_info_tab,textvariable=col[0], width=12)
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

    def update_graph(self):
        pass

def main():
    root = tk.Tk()
    root.title("2D Frame Analysis by Moment Distribution - Alpha")
    main_window(root)
    root.minsize(1024,700)
    root.mainloop()

if __name__ == '__main__':
    main()
