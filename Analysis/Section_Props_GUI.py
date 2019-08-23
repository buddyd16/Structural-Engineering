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
import matplotlib
matplotlib.use('TKAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import Tkinter as tk
import os
import math
import tkMessageBox

def path_exists(path):
    res_folder_exist = os.path.isdir(path)

    if res_folder_exist is False:

        os.makedirs(path)

    else:
        pass

    return 'Directory created'

class Main_window:

    def __init__(self, master):
        self.master = master
        ## Main Frame        
        self.main_frame = tk.Frame(master, bd=2, relief='sunken', padx=10,pady=20)
        self.main_frame.pack(anchor='c', padx= 10, pady= 20)
        
        ## Entry Frame
        self.frame_entry = tk.Frame(self.main_frame, padx=5, pady=5)        
        self.section_info = tk.StringVar()
        self.section_info_label = tk.Label(self.frame_entry, text="Section Label : ")
        self.section_info_label.grid(row=0,column=0, pady=5)
        self.section_info_entry = tk.Entry(self.frame_entry,textvariable=self.section_info, validate='all', validatecommand=self.ins_validate)
        self.section_info_entry.bind("<Button-1>", self.ins_validate)
        self.section_info_entry.grid(row=0,column=1, pady=5)
        
        self.section_x = tk.StringVar()
        self.section_x_label = tk.Label(self.frame_entry, text="x (in) : \n (must be +)")
        self.section_x_label.grid(row=1,column=0, pady=5)
        self.section_x_entry = tk.Entry(self.frame_entry,textvariable=self.section_x)
        self.section_x_entry.grid(row=1,column=1, pady=5)
        
        self.section_y = tk.StringVar()
        self.section_y_label = tk.Label(self.frame_entry, text="y (in) : \n (must be +)")
        self.section_y_label.grid(row=2,column=0, pady=5)
        self.section_y_entry = tk.Entry(self.frame_entry,textvariable=self.section_y)
        self.section_y_entry.grid(row=2,column=1, pady=5)
    
        self.lb_coords = tk.Listbox(self.frame_entry,height = 10, width = 20)
        self.lb_coords.grid(row=0, column=2, columnspan=2, rowspan = 4, sticky='WENS', padx=5, pady=5)
        self.lb_coords.bind("<<ListboxSelect>>",self.coord_click)

        self.b_coords_add = tk.Button(self.frame_entry,text="Add Coord.", command=self.add_coord)
        self.b_coords_min = tk.Button(self.frame_entry,text="Remove Coord.", command=self.remove_coord)
        self.b_coords_change = tk.Button(self.frame_entry, text="Change Selected Coord.", command=self.change_coord)
        self.b_coords_close = tk.Button(self.frame_entry, text="Close Shape", command=self.shape_close)
        self.b_coords_close.configure(state="disabled")
        self.b_coords_change.configure(state="disabled")
                
        self.b_coords_add.grid(row=4, column=0, padx=5, pady=5)
        self.b_coords_min.grid(row=4, column=1, padx=5, pady=5)
        self.b_coords_change.grid(row=4, column=2, padx=5, pady=5)
        self.b_coords_close.grid(row=5, column=0, padx=5, pady=5)        
        
        self.shift_x = tk.StringVar()
        self.shift_x_label = tk.Label(self.frame_entry, text="Shift X coords. (in) :")
        self.shift_x_label.grid(row=6,column=0, pady=5)
        self.shift_x_entry = tk.Entry(self.frame_entry,textvariable=self.shift_x)        
        self.shift_x_entry.grid(row=6, column=1, padx=5, pady=5)
        self.b_shift_x = tk.Button(self.frame_entry, text="Shift all X Coords.", command=self.x_adjust)
        self.b_shift_x.grid(row=6, column=2, padx=5, pady=5)
        
        self.shift_y = tk.StringVar()
        self.shift_y_label = tk.Label(self.frame_entry, text="Shift Y coords. (in) :")
        self.shift_y_label.grid(row=7,column=0, pady=5)
        self.shift_y_entry = tk.Entry(self.frame_entry,textvariable=self.shift_y)
        self.shift_y_entry.grid(row=7, column=1, padx=5, pady=5)
        self.b_shift_y = tk.Button(self.frame_entry, text="Shift all Y Coords.", command=self.y_adjust)
        self.b_shift_y.grid(row=7, column=2, padx=5, pady=5)        
        
        self.frame_entry.pack(side=tk.LEFT)
        ## Chart Frame
        self.chart_frame = tk.Frame(self.main_frame, padx=5, pady=5)
       
        
        self.x = [0,1]
        self.y = [0,1]
        

        self.Fig = matplotlib.figure.Figure(figsize=(5,4),dpi=100)
        self.FigSubPlot = self.Fig.add_subplot(111)
        
        self.line1, = self.FigSubPlot.plot(self.x,self.y,'r-')
        self.centroid, = self.FigSubPlot.plot(0,0,'bo')
        self.clabel = self.FigSubPlot.annotate('(x_bar, y_bar)\n({0:.2f} in., {1:.2f} in.)'.format(0,0),xy=(0,0), xytext=(5,-5), ha='left',textcoords='offset points', fontsize=8)    
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.Fig, master=self.chart_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #self.update()        
        
        self.chart_frame.pack(side=tk.LEFT)
        ## Results Frame        
        self.results_frame = tk.Frame(self.main_frame, padx=5, pady=5)

        self.global_results_labels =['Ix (in^4)','Iy (in^4)','Ixy (in^4)','rx (in)','ry (in)','sx (in^3)','sy (in^3)']
        self.global_results = [0,0,0,0,0,0,0]
        self.local_results_labels =['Area (in^2)','Ix'' (in^4)','Iy'' (in^4)','Ixy'' (in^4)','rx'' (in)','ry'' (in)','sx_top (in^3)','sx_bottom (in^3)','sy_left (in^3)','sy_right (in^3)']
        self.local_results = [0,0,0,0,0,0,0,0,0,0]
        
        self.global_labels = []
        self.local_labels = []
        self.global_l = tk.Label(self.results_frame,text="Global :")
        self.global_l.pack(side=tk.TOP, fill=tk.X)
        for i in range(len(self.global_results_labels)):
            self.global_labels.append(tk.Label(self.results_frame, text="{0} : {1:.3f}".format(self.global_results_labels[i],self.global_results[i]), justify='left'))
            self.global_labels[i].pack(side=tk.TOP, fill=tk.X)
        
        self.local_l = tk.Label(self.results_frame,text="Local :")
        self.local_l.pack(side=tk.TOP, fill=tk.X)
        for i in range(len(self.local_results_labels)):
            self.local_labels.append(tk.Label(self.results_frame, text="{0} : {1:.3f}".format(self.local_results_labels[i],self.local_results[i])))
            self.local_labels[i].pack(side=tk.TOP, fill=tk.X)
        
        self.results_frame.pack(side=tk.LEFT)
        ## Outside Main Frame
        self.b1 = tk.Button(master,text="Close", command=self.quit_app)
        self.b1.pack(side=tk.RIGHT, padx=5, pady=5)        
    
        self.brun = tk.Button(master, text="Run", command= self.run_file)
        self.brun.configure(state="disabled")
        self.brun.pack(side=tk.RIGHT, padx=5, pady=5)
        self.label_error = tk.Label(master, text='')
        self.label_error.pack(side=tk.LEFT)
        
        self.ins_validate()
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
    
    def ins_validate(self, *event):
        reserved_chars = ['<','>',':','"','/','\\','|','?','*']        
        if self.section_info_entry.get() == '':
            self.label_error.configure(text = 'Must Provide a section')
        elif 1 in [c in self.section_info_entry.get() for c in reserved_chars]:
            self.label_error.configure(text = 'Section Label must be a valid windows file name')
        elif self.lb_coords.size() < 3:
            self.brun.configure(state ="disabled")
            self.label_error.configure(text = 'Min of 3 points required')
        elif self.lb_coords.get(0) != self.lb_coords.get(tk.END):
            self.label_error.configure(text = 'First and Last Coordinate must be the Same - Shape must be Closed')
            self.b_coords_close.configure(state="normal")
        else:
            self.brun.configure(state="normal")
            self.label_error.configure(text = '')            
       
    def add_coord(self):
        
        if self.section_x_entry.get()=='' or self.section_y_entry.get()=='':
            self.label_error.configure(text = 'Enter Coordinates')
        else:
            coords = '{0},{1}'.format(self.section_x_entry.get(),self.section_y_entry.get())
            self.lb_coords.insert(tk.END,coords)                
    
            self.ins_validate()
            self.refreshFigure()
    
    def remove_coord(self):
    
        self.lb_coords.delete(tk.END)
    
        self.ins_validate()
        self.refreshFigure()
        
    def coord_click(self,*event):
        pass
        if self.lb_coords.size()==0:
            pass
        else:
            self.b_coords_change.configure(state="normal")
            self.selected_coords = self.lb_coords.get(self.lb_coords.curselection()[0]).split(',')
            self.coords_change_index = self.lb_coords.curselection()[0]
            
            self.section_x.set(self.selected_coords[0])
            self.section_y.set(self.selected_coords[1])        
    
    def change_coord(self):
        if self.section_x_entry.get()=='' or self.section_y_entry.get()=='':
            self.label_error.configure(text = 'Enter Coordinates')
        elif float(self.section_x_entry.get())<0 or float(self.section_y_entry.get())<0:
            self.label_error.configure(text = 'Coordinates Must Be Positive')
        else:
            coords = '{0},{1}'.format(self.section_x_entry.get(),self.section_y_entry.get())
            self.lb_coords.delete(self.coords_change_index)
            self.lb_coords.insert(self.coords_change_index,coords)
            self.b_coords_change.configure(state="disabled")
    
            self.ins_validate()
            self.refreshFigure()
        
    def shape_close(self):
        self.lb_coords.insert(tk.END,self.lb_coords.get(0))
        self.b_coords_close.configure(state="disable")
        self.refreshFigure()
        self.ins_validate()

    def x_adjust(self):
        x=[]
        y=[]      
        if self.lb_coords.size()==0:
            pass
        elif self.shift_x_entry.get()=='':
            self.label_error.configure(text = 'Input X amount to Shift')
        else:
            coords_raw = self.lb_coords.get(0,tk.END)
            for line in coords_raw:            
                coords = line.split(',')
                x.append(float(coords[0])+float(self.shift_x_entry.get()))
                y.append(float(coords[1]))
                for i in range(len(x)):
                    new_coords = '{0:.3f},{1:.3f}'.format(x[i],y[i])
                    self.lb_coords.delete(i)
                    self.lb_coords.insert(i,new_coords)
            self.refreshFigure()
            self.ins_validate()
            
    def y_adjust(self):
        x=[]
        y=[]      
        if self.lb_coords.size()==0:
            pass
        elif self.shift_y_entry.get()=='':
            self.label_error.configure(text = 'Input Y amount to Shift')
        else:
            coords_raw = self.lb_coords.get(0,tk.END)
            for line in coords_raw:            
                coords = line.split(',')
                x.append(float(coords[0]))
                y.append(float(coords[1])+float(self.shift_y_entry.get()))
                for i in range(len(x)):
                    new_coords = '{0:.3f},{1:.3f}'.format(x[i],y[i])
                    self.lb_coords.delete(i)
                    self.lb_coords.insert(i,new_coords)
            self.refreshFigure()
            self.ins_validate()
    
    def refreshFigure(self):
        x=[]
        y=[]
        
        if self.lb_coords.size()==0:
            pass
        else:            
            coords_raw = self.lb_coords.get(0,tk.END)
            for line in coords_raw:
                coords = line.split(',')
                x.append(float(coords[0]))
                y.append(float(coords[1]))
            
            self.line1.set_data(x,y)
            ax = self.canvas.figure.axes[0]
            ax.set_xlim(min(x)-0.5, max(x)+0.5)
            ax.set_ylim(min(y)-0.5, max(y)+0.5)        
            self.canvas.draw()
        
    def run_file(self):
        vertices_x = []
        vertices_y = []
        i_x = 0
        i_y = 0
        i_xy = 0
        x_bar = 0
        y_bar = 0
        i_x_bar = 0
        i_y_bar = 0
        i_xy_bar = 0
        r_x = 0
        r_y = 0
        r_x_bar = 0
        r_y_bar = 0
        s_x = 0
        s_y = 0
        s_x_bar_top = 0
        s_x_bar_bottom = 0
        s_y_bar_top = 0
        s_y_bar_bottom = 0
        area = 0
        
        label = self.section_info_entry.get()
        
        path = os.path.join(os.path.expanduser('~'),'Desktop','RESULTS', label)
    
        path_exists(path)        
        
        i=0
        coords_raw = self.lb_coords.get(0,tk.END)        
        for line in coords_raw:
            coords = line.split(',')
            vertices_x.append(float(coords[0]))
            vertices_y.append(float(coords[1]))
        
        num_vertices = len(vertices_x)-1
        #Section property Calculations
           
        i=0
        for i in range(0,num_vertices):
            i_x =i_x + (vertices_y[i]**2+vertices_y[i]*vertices_y[i+1]+vertices_y[i+1]**2)*(vertices_x[i]*vertices_y[i+1]-vertices_x[i+1]*vertices_y[i])
            print str(i_x)
        i_x = i_x/12
        i_x = i_x
            
        i=0
        for i in range(0,num_vertices):
            i_y = i_y + (vertices_x[i]**2+vertices_x[i]*vertices_x[i+1]+vertices_x[i+1]**2)*(vertices_x[i]*vertices_y[i+1]-vertices_x[i+1]*vertices_y[i])
            print str(i_y)
        i_y = i_y/12
        i_y = i_y
            
        i=0
        for i in range(0,num_vertices):
            i_xy = i_xy + (vertices_x[i]*vertices_y[i+1]+2*vertices_x[i]*vertices_y[i]+2*vertices_x[i+1]*vertices_y[i+1]+vertices_x[i+1]*vertices_y[i])*(vertices_x[i]*vertices_y[i+1]-vertices_x[i+1]*vertices_y[i])
            print str(i_xy)
        i_xy = i_xy/24
        i_xy = i_xy
        
        i=0
        for i in range(0,num_vertices):
            area = area + (vertices_x[i]*vertices_y[i+1]-vertices_x[i+1]*vertices_y[i])
            print str(area)
        area = area/2
        
        i=0
        for i in range(0,num_vertices):
            x_bar = x_bar + (vertices_x[i]+vertices_x[i+1])*(vertices_x[i]*vertices_y[i+1]-vertices_x[i+1]*vertices_y[i])
            print str(x_bar)
        x_bar = x_bar / (6*area)
        
        i=0
        for i in range(0,num_vertices):
            y_bar = y_bar + (vertices_y[i]+vertices_y[i+1])*(vertices_x[i]*vertices_y[i+1]-vertices_x[i+1]*vertices_y[i])
            print str(y_bar)
        y_bar = y_bar/(6*area)
        
        i_x_bar = i_x - area*y_bar**2
        i_y_bar = i_y - area*x_bar**2
        i_xy_bar = i_xy - area*y_bar*x_bar
        
        r_x = math.sqrt(abs(i_x/area))
        r_x_bar = math.sqrt(abs(i_x_bar/area))
        r_y = math.sqrt(abs(i_y/area))
        r_y_bar = math.sqrt(abs(i_y_bar/area))
        #s_x = i_x/y_bar
        #s_y = i_y/x_bar
        s_x_bar_top = i_x_bar/abs(max(vertices_y)-y_bar)
        s_x_bar_bottom = i_x_bar/abs(min(vertices_y)-y_bar)
        s_y_bar_top = i_y_bar/abs(min(vertices_x)-x_bar)
        s_y_bar_bottom = i_y_bar/abs(max(vertices_x)-x_bar)
        
        local_results_str=[]
        global_results_str=[]
        
        global_results = [i_x,i_y,i_xy,r_x,r_y,s_x,s_y]
        global_results_str.append(['{:.3f}'.format(x) for x in global_results])
        local_results = [abs(area),i_x_bar,i_y_bar,i_xy_bar,r_x_bar,r_y_bar,s_x_bar_top,s_x_bar_bottom,s_y_bar_top,s_y_bar_bottom]
        local_results_str.append(['{:.3f}'.format(x) for x in local_results])
        
        self.global_results = global_results
        self.local_results = local_results
        
               
        self.centroid.set_data(x_bar,y_bar)
        self.clabel.remove()        
        self.clabel = self.FigSubPlot.annotate('(x_bar, y_bar)\n({0:.2f} in., {1:.2f} in.)'.format(x_bar,y_bar),xy=(x_bar,y_bar), xytext=(5,-5), ha='left',textcoords='offset points', fontsize=8)    
        self.canvas.draw()
        #PDF matplotlib plot output
        for i in range(len(self.global_results_labels)):
            self.global_labels[i].configure(text="{0} : {1:.3f}".format(self.global_results_labels[i],self.global_results[i]))
            
        
        for i in range(len(self.local_results_labels)):
            self.local_labels[i].configure(text="{0} : {1:.3f}".format(self.local_results_labels[i],self.local_results[i]))
            
        
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        
        plt.figure(figsize=(11,8.5))
        
        plt.subplot(1,2,1)
        #plt.xlim(min(vertices_x)-1,max(vertices_x)+1)
        #plt.ylim(min(vertices_y)-1,max(vertices_y)+1)
        plt.axis('equal')
        plt.fill(vertices_x,vertices_y, edgecolor='b', facecolor='r', alpha = 0.4, label='section')
        plt.plot(x_bar,y_bar,'ko',label='centroid')
        plt.annotate('(x_bar, y_bar)\n({0:.2f} in., {1:.2f} in.)'.format(x_bar,y_bar),xy=(x_bar,y_bar), xytext=(5,-5), ha='left',textcoords='offset points', fontsize=8)    
        plt.title(label+' Section')
        
        plt.subplot(1,2,2)
        plt.plot(0,0)
        plt.plot(3,1)
        plt.axis('off')
        plt.text(.1,0.5,('''Global Results:\n
            Ix : {0:.3f} in.^4\n
            Iy : {1:.3f} in.^4\n
            Ixy : {2:.3f} in.^4\n
            rx : {3:.3f} in.\n
            ry : {4:.3f} in.\n
            sx : {5:.3f} in.^3\n
            sy : {6:.3f} in.^3\n
         Local x and y axis:\n
            Area : {7:.3f} in.^2\n
            Ix' : {8:.3f} in.^4\n
            Iy' : {9:.3f} in.^4\n
            Ixy' : {10:.3f} in.^4\n
            rx' : {11:.3f} in.\n
            ry' : {12:.3f} in.\n
            sx'_top : {13:.3f} in.^3\n
            sx'_bottom : {14:.3f} in.^3\n
            sy'_left : {15:.3f} in.^3\n
            sy'_right : {16:.3f} in.^3\n'''.format(i_x,i_y,i_xy,r_x,r_y,s_x,s_y,abs(area),i_x_bar,i_y_bar,i_xy_bar,r_x_bar,r_y_bar,s_x_bar_top,s_x_bar_bottom,s_y_bar_top,s_y_bar_bottom)), horizontalalignment='left', verticalalignment='center', transform=plt.gca().transAxes, fontsize=10, bbox=props)
        
        
        
        plt.savefig(os.path.join(path,label+'_section_chart.pdf'))
        plt.close('all')

def main(): 
    root = tk.Tk()
    root.title("Section Properties")
    app = Main_window(root)
    root.mainloop()

if __name__ == '__main__':
    main()