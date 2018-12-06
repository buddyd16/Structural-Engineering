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
        self.graphics_frame.pack(side=tk.RIGHT, padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        self.data_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.data_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
       
        #Main Notebooks
        self.nb_data = ttk.Notebook(self.data_frame)
        self.nb_data.pack(fill=tk.BOTH, expand=1)
        
        #Graphics Frame tabs and canvases
        #Geometry - Plan
        self.g_plan_frame = tk.Frame(self.graphics_frame, bd=2, relief='sunken', padx=1,pady=1)
        self.g_plan_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)

        self.g_plan_canvas = tk.Canvas(self.g_plan_frame, width=50, height=50, bd=2, relief='sunken', background="gray60")
        self.g_plan_canvas.bind("<Configure>", self.draw_bolts)
        self.g_plan_canvas.pack(side = tk.LEFT, anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        
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
        self.bolt_input_canvas = tk.Canvas(self.bolt_frame, background="gray")
        self.bolt_canvas_frame = tk.Frame(self.bolt_input_canvas)
        self.scrollforcanvas = tk.Scrollbar(self.bolt_frame, orient="vertical", command=self.bolt_input_canvas.yview)
        self.scrollforcanvas.pack(side=tk.RIGHT, fill="y")
        self.bolt_input_canvas.pack(side=tk.LEFT, fill="both", expand=True)
        self.bolt_input_canvas.create_window((3,6), window=self.bolt_canvas_frame, anchor="nw", tags="self.bolt_canvas_frame")
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
        
        self.data_frame.pack(fill=tk.BOTH,expand=1, padx=5, pady=5)
        
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
    
    def add_bolt(self, *event):
        self.hasrun=0
        self.bolt_count +=1
        
        for element in self.bolt_gui_elements:
            element.destroy()
            
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
            
            res = bolt_ic.brandt(xloc,yloc,p_xloc,p_yloc,p_angle)
            
            self.IC = res[1]
            Cu = res[2]
            
            self.ic_x_gui.set("{0:.3f}".format(self.IC[0]))
            self.ic_y_gui.set("{0:.3f}".format(self.IC[1]))
            self.cu_gui.set("{0:.3f}".format(Cu))
            
            self.hasrun=1
            self.draw_bolts()
            
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
            
            px_2 = (m.cos(m.radians(p_angle))*5)+ p_xloc
            py_2 = (m.sin(m.radians(p_angle))*5) + p_yloc
            
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
            
            initial = 70
            
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
            
        
def main():
    root = tk.Tk()
    root.title("Bolt Group Coefficient - Alpha")
    main_window(root)
    root.minsize(1024,768)
    root.mainloop()

if __name__ == '__main__':
    main()
