# -*- coding: utf-8 -*-
import Tkinter as tk
import ttk
import tkFont
import pin_pin_beam_equations_classes as ppbeam
from numpy import zeros
import math

class Master_window:

    def __init__(self, master):
        
        self.master = master
        
        self.loads_scale = [0.1]
        
        self.reaction_left = 0
        self.reaction_right = 0
        
        self.shearl = zeros(501)
        self.shearc = zeros(501)
        self.shearr = zeros(501)
        
        self.momentl = zeros(501)
        self. momentc = zeros(501)
        self.momentr = zeros(501)
        
        self.slopel = zeros(501)
        self.slopec = zeros(501)
        self.sloper = zeros(501)
        
        self.deltal = zeros(501)
        self.deltac = zeros(501)
        self.deltar = zeros(501)
        
        self.f_size = 8
        helv = tkFont.Font(family='Helvetica',size=self.f_size, weight='bold')
        self.menubar = tk.Menu(self.master)
        self.menu = tk.Menu(self.menubar, tearoff=0)
        self.menu_props = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label = "File", menu=self.menu)
        self.menu.add_command(label="Quit", command=self.quit_app)
        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            self.master.tk.call(master, "config", "-menu", self.menubar)
        
        #Main Frames
        self.main_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.main_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        self.base_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.base_frame.pack(side=tk.BOTTOM, padx= 1, pady= 1, fill=tk.X, expand=1)
        
        #Beam Canvas
        self.beam_canvas_frame = tk.Frame(self.main_frame, bd=2, relief='sunken', padx=1,pady=1)
        self.bm_canvas = tk.Canvas(self.beam_canvas_frame, width=750, height=150, bd=2, relief='sunken')
        self.bm_canvas.bind("<Configure>", self.bm_canvas_draw)
        self.bm_canvas.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        self.beam_canvas_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        
        self.nb = ttk.Notebook(self.main_frame)
        self.nb.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        
        #Tab 1 - Span Data
        self.page1 = ttk.Frame(self.nb)
        self.nb.add(self.page1, text='Span Information')
        
        self.pg1_frame = tk.Frame(self.page1, bd=2, relief='sunken', padx=1,pady=1, width=300, height=500)
        
        tk.Label(self.pg1_frame, text="Left Cantilever (ft):").grid(row=1,column=1, sticky = tk.E)
        tk.Label(self.pg1_frame, text="Center Span (ft):").grid(row=2,column=1, sticky = tk.E)
        tk.Label(self.pg1_frame, text="Right Cantilever (ft):").grid(row=3,column=1, sticky = tk.E)
        
        self.left_cant_ft = tk.StringVar() 
        self.span_ft = tk.StringVar()
        self.right_cant_ft = tk.StringVar()
        
        self.left_cant_ft.set(0.0)
        self.span_ft.set(10.0)
        self.right_cant_ft.set(0.0)
        
        self.left_cant_entry = tk.Entry(self.pg1_frame, textvariable=self.left_cant_ft, width=10)
        self.left_cant_entry.grid(row=1,column=2, sticky = tk.W)
        self.span_entry = tk.Entry(self.pg1_frame, textvariable=self.span_ft, width=10)
        self.span_entry.grid(row=2,column=2, sticky = tk.W)
        self.right_cant_entry = tk.Entry(self.pg1_frame, textvariable=self.right_cant_ft, width=10)
        self.right_cant_entry.grid(row=3,column=2, sticky = tk.W)
        
        tk.Label(self.pg1_frame, text="E (ksi):").grid(row=4,column=1, sticky = tk.E)
        tk.Label(self.pg1_frame, text="I (in^4):").grid(row=5,column=1, sticky = tk.E)
        
        self.E_ksi = tk.StringVar() 
        self.I_in4 = tk.StringVar()
        
        self.E_ksi.set(29000)
        self.I_in4.set(30.8)
        
        self.E_entry = tk.Entry(self.pg1_frame, textvariable=self.E_ksi, width=10)
        self.E_entry.grid(row=4,column=2, sticky = tk.W)
        self.I_entry = tk.Entry(self.pg1_frame, textvariable=self.I_in4, width=10)
        self.I_entry.grid(row=5,column=2, sticky = tk.W)
        
        tk.Label(self.pg1_frame, text="Add Loads:").grid(row=6,column=1, sticky = tk.E)
        tk.Label(self.pg1_frame, text="P,M,W1 (kips, ft-kips, klf):").grid(row=7,column=1, sticky = tk.E)
        tk.Label(self.pg1_frame, text="W2 (kips, ft-kips, klf):").grid(row=8,column=1, sticky = tk.E)
        tk.Label(self.pg1_frame, text="a (ft):").grid(row=9,column=1, sticky = tk.E)
        tk.Label(self.pg1_frame, text="b (ft):").grid(row=10,column=1, sticky = tk.E)
        tk.Label(self.pg1_frame, text="Load Type:").grid(row=11,column=1, sticky = tk.E)
        tk.Label(self.pg1_frame, text="Load Location:").grid(row=12,column=1, sticky = tk.E)
        
        self.w1_gui = tk.StringVar() 
        self.w2_gui = tk.StringVar() 
        self.a_gui = tk.StringVar() 
        self.b_gui = tk.StringVar()
        
        self.w1_gui.set(0)
        self.w2_gui.set(0)
        self.a_gui.set(0) 
        self.b_gui.set(0)
        
        self.w1_gui_entry = tk.Entry(self.pg1_frame, textvariable=self.w1_gui, width=10)
        self.w1_gui_entry.grid(row=7,column=2, sticky = tk.W)
        self.w2_gui_entry = tk.Entry(self.pg1_frame, textvariable=self.w2_gui, width=10)
        self.w2_gui_entry.grid(row=8,column=2, sticky = tk.W)
        self.a_gui_entry = tk.Entry(self.pg1_frame, textvariable=self.a_gui, width=10)
        self.a_gui_entry.grid(row=9,column=2, sticky = tk.W)
        self.b_gui_entry = tk.Entry(self.pg1_frame, textvariable=self.b_gui, width=10) 
        self.b_gui_entry.grid(row=10,column=2, sticky = tk.W)
        
        self.b_run = tk.Button(self.pg1_frame,text = "Update", command = self.update)
        self.b_run.grid(row=1,column=3, sticky = tk.W)        
        
        self.load_type = tk.StringVar()
        self.load_type.set('Point')
        load_types = ['Point','Moment','UDL','TRAP']
        self.load_type_selection = tk.OptionMenu(self.pg1_frame, self.load_type, *load_types)
        self.load_type_selection.grid(row=11,column=2, sticky = tk.W)
        
        self.load_loc = tk.StringVar()
        self.load_loc.set('Center')
        load_locals = ['Left','Center','Right']
        self.load_loc_selection = tk.OptionMenu(self.pg1_frame, self.load_loc, *load_locals)
        self.load_loc_selection.grid(row=12,column=2, sticky = tk.W)
        
        self.b_add_load = tk.Button(self.pg1_frame,text = "Add New Load", command = self.add_load)
        self.b_add_load.grid(row=7, column=3, sticky = tk.W)       
        
        self.b_remove_load = tk.Button(self.pg1_frame,text = "Remove Last Load", command = self.remove_load)
        self.b_remove_load.grid(row=8, column=3, sticky = tk.W) 
        
        self.show_v = tk.IntVar()
        tk.Checkbutton(self.pg1_frame, text=' : Show V', variable=self.show_v, command = self.bm_canvas_draw).grid(row=1, column=5, sticky = tk.W)
        self.show_m = tk.IntVar()
        tk.Checkbutton(self.pg1_frame, text=' : Show M', variable=self.show_m, command = self.bm_canvas_draw).grid(row=2, column=5, sticky = tk.W)
        self.show_s = tk.IntVar()
        tk.Checkbutton(self.pg1_frame, text=' : Show S', variable=self.show_s, command = self.bm_canvas_draw).grid(row=3, column=5, sticky = tk.W)
        self.show_d = tk.IntVar()
        tk.Checkbutton(self.pg1_frame, text=' : Show D', variable=self.show_d, command = self.bm_canvas_draw).grid(row=4, column=5, sticky = tk.W)
        self.show_r = tk.IntVar()
        tk.Checkbutton(self.pg1_frame, text=' : Show Reactions', variable=self.show_r, command = self.bm_canvas_draw ).grid(row=5, column=5, sticky = tk.W) 
        
        self.res_labels = []
        self.res_list = ['Results:','--','--','Cant. Left:','--','--','--','--','Center Span:','--','--','--','--','Cant. Right:','--','--','--','--']
        for i in range(0,18):
            self.res_labels.append(tk.Label(self.pg1_frame, text= self.res_list[i]))
            self.res_labels[i].grid(row=i+1,column=6, sticky = tk.W)
        
        self.pg1_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)

        #Tab 2 - Loads
        self.page2 = ttk.Frame(self.nb)
        self.nb.add(self.page2, text='Loads')

        self.pg2_frame = tk.Frame(self.page2, bd=2, relief='sunken', padx=1,pady=1, width=300, height=500)
        
        self.pg2_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)   
        
        self.b_quit = tk.Button(self.base_frame,text="Quit", command=self.quit_app, font=helv)
        self.b_quit.pack(side=tk.RIGHT)
        
        self.loads_left = []
        self.loads_center = [] 
        self.loads_right = []
        
        self.has_run = 0
        
        #self.left_cant_ft.trace('w', self.run)
        #self.span_ft.trace('w', self.run)
        #self.right_cant_ft.trace('w', self.run)
        
        self.load_last_add = []
              
        self.run()

            
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
            
            initial = 30.0
            support = initial / 2.0
            
            ll = float(self.left_cant_ft.get())
            lc = float(self.span_ft.get())
            lr = float(self.right_cant_ft.get())
            
            sf = (w-(2*initial)) / (ll+lc+lr)
            
            l = (w-(2*initial)) + initial
            s1 = (sf * ll) + initial
            s2 = ((ll+lc) * sf) + initial
            
            self.bm_canvas.create_line(initial, h/2, l, h/2, fill="black")
            self.bm_canvas.create_line(s1, h/2, (s1+support), (h/2)+support, (s1-support), (h/2)+support,s1, h/2, fill="black")
            self.bm_canvas.create_line(s2, h/2, (s2+support), (h/2)+support, (s2-support), (h/2)+support,s2, h/2, fill="black")
            
            
            hg = (h/2.0)
            loads_sf = (hg - 10) / max(max(self.loads_scale), abs(min(self.loads_scale)))
            
            for load in self.loads_left:
                x = load.x_graph
                y = load.y_graph
                for i in range(1,len(x)):
                    self.bm_canvas.create_line((x[i-1]* sf)+initial,hg - (y[i-1] * loads_sf),(x[i]* sf)+initial,hg - (y[i] * loads_sf), fill = "blue")
                    
            for load in self.loads_center:
                x = load.x_graph
                y = load.y_graph
                for i in range(1,len(x)):
                    self.bm_canvas.create_line(((x[i-1] + ll)* sf)+initial,hg - (y[i-1] * loads_sf),((x[i]+ll)* sf)+initial,hg - (y[i] * loads_sf), fill = "blue")
                    
            for load in self.loads_right:
                x = load.x_graph
                y = load.y_graph
                for i in range(1,len(x)):
                    self.bm_canvas.create_line(((x[i-1]+ll+lc)* sf)+initial,hg - (y[i-1] * loads_sf),((x[i]+ll+lc)* sf)+initial,hg - (y[i] * loads_sf), fill = "blue")
            
            if self.has_run == 1:        
                xl = self.xsl
                xc = self.xsc
                xr = self.xsr
            else:
                pass
                    
            if self.show_v.get() == 1:
                               
                v_sf = (hg - 10) / max(max(max(self.shearc), max(self.shearl), max(self.shearr)), abs(min(min(self.shearc), min(self.shearl), min(self.shearr))))
                
                
                for i in range(1,len(self.shearc)):
                    self.bm_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.shearl[i-1] * v_sf),(xl[i] * sf) + initial,hg - (self.shearl[i] * v_sf),fill="red")
                    self.bm_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.shearc[i-1] * v_sf),(xc[i] * sf) + initial,hg - (self.shearc[i] * v_sf),fill="red")
                    self.bm_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.shearr[i-1] * v_sf),(xr[i] * sf) + initial,hg - (self.shearr[i] * v_sf),fill="red")
            
            if self.show_m.get() == 1:
                                  
                m_sf = (hg - 10) / max(max(max(self.momentc),max(self.momentl),max(self.momentr)), abs(min(min(self.momentc),min(self.momentl),min(self.momentr))))
                
                for i in range(1,len(self.momentc)):
                    self.bm_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.momentl[i-1] * m_sf),(xl[i] * sf) + initial,hg - (self.momentl[i] * m_sf),fill="green")
                    self.bm_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.momentc[i-1] * m_sf),(xc[i] * sf) + initial,hg - (self.momentc[i] * m_sf),fill="green")
                    self.bm_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.momentr[i-1] * m_sf),(xr[i] * sf) + initial,hg - (self.momentr[i] * m_sf),fill="green")
            
            if self.show_s.get() == 1:
                                  
                s_sf = (hg - 10) / max(max(max(self.slopec),max(self.slopel),max(self.sloper)), abs(min(min(self.slopec),min(self.slopel),min(self.sloper))))
                
                for i in range(1,len(self.slopec)):
                    self.bm_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.slopel[i-1] * s_sf),(xl[i] * sf) + initial,hg - (self.slopel[i] * s_sf),fill="magenta")
                    self.bm_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.slopec[i-1] * s_sf),(xc[i] * sf) + initial,hg - (self.slopec[i] * s_sf),fill="magenta")
                    self.bm_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.sloper[i-1] * s_sf),(xr[i] * sf) + initial,hg - (self.sloper[i] * s_sf),fill="magenta")
            
            if self.show_d.get() == 1:
                                  
                d_sf = (hg - 10) / max(max(max(self.deltac),max(self.deltal),max(self.deltar)), abs(min(min(self.deltac),min(self.deltal),min(self.deltar))))
                
                for i in range(1,len(self.deltac)):
                    self.bm_canvas.create_line((xl[i-1] * sf) + initial, hg - (self.deltal[i-1] * d_sf),(xl[i] * sf) + initial,hg - (self.deltal[i] * d_sf),fill="pink")
                    self.bm_canvas.create_line((xc[i-1] * sf) + initial, hg - (self.deltac[i-1] * d_sf),(xc[i] * sf) + initial,hg - (self.deltac[i] * d_sf),fill="pink")
                    self.bm_canvas.create_line((xr[i-1] * sf) + initial, hg - (self.deltar[i-1] * d_sf),(xr[i] * sf) + initial,hg - (self.deltar[i] * d_sf),fill="pink")

            if self.show_r.get() == 1:
                                  
                r_sf = (hg - 10) / max(max(max(self.rly),max(self.rry)), abs(min(min(self.rlx),min(self.rly))))
                
                for i in range(1,len(self.rlx)):
                    self.bm_canvas.create_line((self.rlx[i-1] * sf) + initial, hg - (self.rly[i-1] * r_sf),(self.rlx[i] * sf) + initial,hg - (self.rly[i] * r_sf),fill="black")
                    self.bm_canvas.create_line((self.rrx[i-1] * sf) + initial, hg - (self.rry[i-1] * r_sf),(self.rrx[i] * sf) + initial,hg - (self.rry[i] * r_sf),fill="black")

    def add_load(self, *event):
        
        ll = float(self.left_cant_ft.get())
        lc = float(self.span_ft.get())
        lr = float(self.right_cant_ft.get())
        
        load_location = self.load_loc.get()
        
        load_type = self.load_type.get()
        
        w1 = float(self.w1_gui.get())
        w2 = float(self.w2_gui.get())
        a = float(self.a_gui.get())
        b = float(self.b_gui.get())
        
        self.loads_scale.append(w1)
        self.loads_scale.append(w2)
        
        #['Left','Center','Right']
        if load_location == 'Left':
            self.load_last_add.append('L')
            #['Point','Moment','UDL','TRAP']
            if load_type == 'Point':
                self.loads_left.append(ppbeam.cant_left_point(w1,a,ll,lc))
            
            elif load_type == 'Moment':
                self.loads_left.append(ppbeam.cant_left_point_moment(w1,a,ll,lc))
                
            elif load_type == 'UDL':
                self.loads_left.append(ppbeam.cant_left_udl(w1,a,b,ll,lc))
            
            elif load_type == 'TRAP':
                self.loads_left.append(ppbeam.cant_left_trap(w1,w2,a,b,ll,lc))
            else:
                pass
        
        elif load_location == 'Center':
            self.load_last_add.append('C')
            #['Point','Moment','UDL','TRAP']
            if load_type == 'Point':
                self.loads_center.append(ppbeam.pl(w1,a,lc))
            
            elif load_type == 'Moment':
                self.loads_center.append(ppbeam.point_moment(w1,a,lc))
                
            elif load_type == 'UDL':
                self.loads_center.append(ppbeam.udl(w1,a,b,lc))
            
            elif load_type == 'TRAP':
                self.loads_center.append(ppbeam.trap(w1,w2,a,b,lc))
            else:
                pass
            
        elif load_location == 'Right':
            self.load_last_add.append('R')
            #['Point','Moment','UDL','TRAP']
            if load_type == 'Point':
                self.loads_right.append(ppbeam.cant_right_point(w1,a,lr,lc))
            
            elif load_type == 'Moment':
                self.loads_right.append(ppbeam.cant_right_point_moment(w1,a,lr,lc))
                
            elif load_type == 'UDL':
                self.loads_right.append(ppbeam.cant_right_udl(w1,a,b,lr,lc))
            
            elif load_type == 'TRAP':
                self.loads_right.append(ppbeam.cant_right_trap(w1,w2,a,b,lr,lc))
            else:
                pass
            
        else:
            pass
        
        self.run()
        self.bm_canvas_draw()

    def remove_load(self, *event):
        
        if len(self.load_last_add) == 0:
            pass
        else:
            span = self.load_last_add[-1]
            
            if span == 'L':
                del self.loads_left[-1]
            
            elif span == 'C':
                del self.loads_center[-1]
                
            else:
                del self.loads_right[-1]
        
        del self.load_last_add[-1]
        
        self.run()
        self.bm_canvas_draw()
        

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

        if self.left_cant_ft.get() == '' or self.span_ft.get()== '' or self.right_cant_ft.get() == '':
            pass
        
        else:
            self.ll = float(self.left_cant_ft.get())
            self.lc = float(self.span_ft.get())
            self.lr = float(self.right_cant_ft.get())

    
            E = float(self.E_ksi.get()) * 144        #144 is conversion from ksi to ksf - 12^2
            I = float(self.I_in4.get()) / 12.0**4    #covert from in^4 to ft^4        
            
            step_left = self.ll/500.0
            step_backspan = self.lc/500.0
            step_right = self.lr/500.0
            
            xsl = zeros(501)
            xsc = zeros(501)
            xsr = zeros(501)
            
            reaction_left = 0
            reaction_right = 0
            
            shearl = zeros(501)
            shearc = zeros(501)
            shearr = zeros(501)
            
            momentl = zeros(501)
            momentc = zeros(501)
            momentr = zeros(501)
            
            slopel = zeros(501)
            slopec = zeros(501)
            sloper = zeros(501)
            
            deltal = zeros(501)
            deltac = zeros(501)
            deltar = zeros(501)
            
            xsl[0]=0
            xsc[0]=0
            xsr[0]=0
            
            for i in range(1,501):
                xsl[i] = xsl[i-1] + step_left
                xsc[i] = xsc[i-1] + step_backspan
                xsr[i] = xsr[i-1] + step_right
            
            if self.ll == 0:
                load_left = [ppbeam.cant_left_point(0,0,self.ll,self.lc)]
            
            else:
                load_left = self.loads_left
            
            if len(self.loads_center) == 0:
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
                sloper = sloper + ppbeam.cant_right_nl(load.backspan.eisx(self.lc)).eis(xsr)
                
                deltal = deltal + load.eid(xsl)
                deltac = deltac + load.backspan.eid(xsc)
                deltar = deltar + ppbeam.cant_right_nl(load.backspan.eisx(self.lc)).eid(xsr)
            
            for load in load_center:
                reaction_left = reaction_left + load.rl
                reaction_right = reaction_right  + load.rr
                
                shearc = shearc + load.v(xsc)
                
                momentc = momentc + load.m(xsc)
               
                slopel = slopel + ppbeam.cant_left_nl(load.eisx(0),self.ll).eis(xsl)
                slopec = slopec + load.eis(xsc)
                sloper = sloper + ppbeam.cant_right_nl(load.eisx(self.lc)).eis(xsr)
                
                deltal = deltal + ppbeam.cant_left_nl(load.eisx(0),self.ll).eid(xsl)
                deltac = deltac + load.eid(xsc)
                deltar = deltar + ppbeam.cant_right_nl(load.eisx(self.lc)).eid(xsr)
            
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
            
            self.deltal = (deltal / (E*I))*12.0
            self.deltac = (deltac / (E*I))*12.0
            self.deltar = (deltar / (E*I))*12.0
            
            self.rlx, self.rly = self.reaction_graph(reaction_left, self.ll)
            self.rrx, self.rry = self.reaction_graph(reaction_right, self.ll+self.lc)
            
            self.res_labels[1].configure(text = 'Rl = {0:.3f} kips'.format(reaction_left))
            self.res_labels[2].configure(text = 'Rr = {0:.3f} kips'.format(reaction_right))
            
            self.res_labels[4].configure(text = 'Vmax = {0:.3f} kips - Vmin = {1:.3f} kips'.format(max(shearl), min(shearl)))
            self.res_labels[5].configure(text = 'Mmax = {0:.3f} ft-kips - Mmin = {1:.3f} ft-kips'.format(max(momentl), min(momentl)))
            self.res_labels[6].configure(text = 'Smax = {0:.5f} rad - Smin = {1:.5f} rad'.format(max(self.slopel), min(self.slopel)))
            self.res_labels[7].configure(text = 'Dmax = {0:.4f} in - Dmin = {1:.4f} in'.format(max(self.deltal), min(self.deltal)))
            
            self.res_labels[9].configure(text = 'Vmax = {0:.3f} kips - Vmin = {1:.3f} kips'.format(max(shearc), min(shearc)))
            self.res_labels[10].configure(text = 'Mmax = {0:.3f} ft-kips - Mmin = {1:.3f} ft-kips'.format(max(momentc), min(momentc)))
            self.res_labels[11].configure(text = 'Smax = {0:.5f} rad - Smin = {1:.5f} rad'.format(max(self.slopec), min(self.slopec)))
            self.res_labels[12].configure(text = 'Dmax = {0:.4f} in - Dmin = {1:.4f} in'.format(max(self.deltac), min(self.deltac)))
            
            self.res_labels[14].configure(text = 'Vmax = {0:.3f} kips - Vmin = {1:.3f} kips'.format(max(shearr), min(shearr)))
            self.res_labels[15].configure(text = 'Mmax = {0:.3f} ft-kips - Mmin = {1:.3f} ft-kips'.format(max(momentr), min(momentr)))
            self.res_labels[16].configure(text = 'Smax = {0:.5f} rad - Smin = {1:.5f} rad'.format(max(self.sloper), min(self.sloper)))
            self.res_labels[17].configure(text = 'Dmax = {0:.4f} in - Dmin = {1:.4f} in'.format(max(self.deltar), min(self.deltar)))
            
            #convert x coordinates to global
            self.xsl = xsl
            self.xsc = xsc + xsl[-1]
            self.xsr = xsr + self.xsc[-1]
            
            self.has_run = 1
            self.bm_canvas_draw()
    
    def update(self, *event):
        
        del self.loads_right[:]
        del self.loads_left[:]
        del self.loads_center[:]
        del self.load_last_add[:]
        
        self.run()
       
def main():
    root = tk.Tk()
    root.title("Simple Beam")
    Master_window(root)
    root.minsize(800,600)
    root.mainloop()

if __name__ == '__main__':
    main()   

            

