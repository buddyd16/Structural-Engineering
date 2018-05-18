# -*- coding: utf-8 -*-
"""
Created on Fri May 04 14:06:27 2018

@author: DonB
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
import math
import aisc_database_class
import Tkinter as tk
import ttk
import tkFont

class Master_window:

    def __init__(self, master):
        
        self.master = master
        
        #Set Fonts to Use
        self.f_size = 8
        self.helv = tkFont.Font(family='Helvetica',size=self.f_size, weight='bold')
        self.helv_res = tkFont.Font(family='Helvetica',size=self.f_size, weight='bold', underline = True)
        
        #Build the MenuBar
        self.menubar = tk.Menu(self.master)
        self.menu = tk.Menu(self.menubar, tearoff=0)
        self.menu_props = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label = "File", menu=self.menu)
        self.menu.add_command(label="Quit", command=self.quit_app)
        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            self.master.tk.call(master, "config", "-menu", self.menubar)
        
        #Build the shape database
        self.aisc_db = aisc_database_class.aisc_15th_database()
        
        #Main and Base Frames
        self.main_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.main_frame.pack(anchor='c', padx= 1, pady= 1, fill=tk.BOTH, expand=1)
        self.base_frame = tk.Frame(master, bd=2, relief='sunken', padx=1,pady=1)
        self.base_frame.pack(side=tk.BOTTOM, padx= 1, pady= 1, fill=tk.X)
        
        #Quit App Button
        self.b_quit = tk.Button(self.base_frame,text="Quit", command=self.quit_app, font=self.helv)
        self.b_quit.pack(side=tk.RIGHT)
        
        self.left_frame = tk.Frame(self.main_frame, padx=1, pady=1)
        self.left_frame.grid(row=1, column=1)
         
        self.picker_frame = tk.Frame(self.left_frame, padx=1, pady=1)
        self.picker_frame.grid(row=1, column=1)
        self.defs_frame = tk.Frame(self.left_frame, padx=1, pady=1)
        self.defs_frame.grid(row=2, column=1)
        
        self.def_title = tk.Label(self.defs_frame, text='-- ', font=self.helv)
        self.def_title.grid(row=1, column=1, padx=4)
        
        self.def_text = tk.Text(self.defs_frame, height = 10, width = 60, bg= "grey90", font=self.helv, wrap=tk.WORD)
        self.def_text.grid(row=1, column=2, padx=4, pady=10)   
        
        self.shape_picked = tk.StringVar()
        self.shape_picked.set('W')
        shape_types = self.aisc_db.shape_types
        shape_types.sort()
        self.shape_type_picker = tk.OptionMenu(self.picker_frame, self.shape_picked, *shape_types, command=self.shape_change)
        self.shape_type_picker.configure(width=20)
        self.shape_type_picker.grid(row=0, column=1)
        
        self.shape_scrollbar_r = tk.Scrollbar(self.picker_frame, orient="vertical", command=self.shapes_scroll)
        self.shape_scrollbar_r.grid(row=1, column=2, sticky=tk.NS)
        
        self.shape_listbox = tk.Listbox(self.picker_frame, height = 40, width = 35, font=self.helv, yscrollcommand=self.shape_scrollbar_r.set)
        self.shape_listbox.grid(row=1, column=1)
        self.shape_listbox.bind("<<ListboxSelect>>", self.shape_click)

        self.shape_data_scrollbar_r = tk.Scrollbar(self.picker_frame, orient="vertical", command=self.shapes_data_scroll)
        self.shape_data_scrollbar_r.grid(row=1, column=4, sticky=tk.NS)
        
        self.shape_data_listbox = tk.Listbox(self.picker_frame, height = 40, width = 50, font=self.helv, yscrollcommand=self.shape_data_scrollbar_r.set)
        self.shape_data_listbox.grid(row=1, column=3)
        self.shape_data_listbox.bind("<<ListboxSelect>>", self.property_click)
        
        self.shape_selection_list = []
        self.shape_props_list = []
        self.shape_prop_labels = self.aisc_db.labels
        
        #Calc Input Data Frame
        self.calc_frame = tk.Frame(self.main_frame, padx=1, pady=1)
        self.calc_frame.grid(row=1, column=2)
        
        self.cb_gui = tk.StringVar()
        self.cb_gui.set('1.0')
        tk.Label(self.calc_frame, text='Cb = ', font=self.helv).grid(row=1, column=1, padx=4)
        self.cb_gui_entry = tk.Entry(self.calc_frame, textvariable=self.cb_gui, width=10)
        self.cb_gui_entry.grid(row=1,column=2, sticky = tk.W)

        self.lb_gui = tk.StringVar()
        self.lb_gui.set('10.0')
        tk.Label(self.calc_frame, text='Lb (ft) = ', font=self.helv).grid(row=2, column=1, padx=4)
        self.lb_gui_entry = tk.Entry(self.calc_frame, textvariable=self.lb_gui, width=10)
        self.lb_gui_entry.grid(row=2,column=2, sticky = tk.W)  

        self.lv_gui = tk.StringVar()
        self.lv_gui.set('5.0')
        tk.Label(self.calc_frame, text='Lv (ft) = ', font=self.helv).grid(row=3, column=1, padx=4)
        self.lv_gui_entry = tk.Entry(self.calc_frame, textvariable=self.lv_gui, width=10)
        self.lv_gui_entry.grid(row=3,column=2, sticky = tk.W)
        
        self.E_gui = tk.StringVar()
        self.E_gui.set('29000.0')
        tk.Label(self.calc_frame, text='E (ksi) = ', font=self.helv).grid(row=4, column=1, padx=4)
        self.E_gui_entry = tk.Entry(self.calc_frame, textvariable=self.E_gui, width=10)
        self.E_gui_entry.grid(row=4,column=2, sticky = tk.W)
        
        self.fy_gui = tk.StringVar()
        self.fy_gui.set('50.0')
        tk.Label(self.calc_frame, text='Fy (ksi) = ', font=self.helv).grid(row=5, column=1, padx=4)
        self.fy_gui_entry = tk.Entry(self.calc_frame, textvariable=self.fy_gui, width=10)
        self.fy_gui_entry.grid(row=5,column=2, sticky = tk.W)
        
        self.b_refresh = tk.Button(self.calc_frame,text="Refresh\nCalcs", command=self.shape_calcs, font=self.helv)
        self.b_refresh.grid(row=6, column=2)
        
        #Calc Results Frame
        self.calc_res_frame = tk.LabelFrame(self.main_frame, text='Shape:', bd=1, relief='sunken', padx=2, pady=2, font=self.helv)
        self.calc_res_frame.grid(row=1, column=3)
        
        self.flexure_label = tk.Label(self.calc_res_frame, text='--', justify=tk.LEFT, font=self.helv)
        self.flexure_label.grid(row=1, column=1, rowspan=6, sticky = tk.NW)
        
        self.flexure_weak_label = tk.Label(self.calc_res_frame, text='--', justify=tk.LEFT, font=self.helv)
        self.flexure_weak_label.grid(row=1, column=2, rowspan=6, sticky = tk.NW)
        
        self.shear_label = tk.Label(self.calc_res_frame, text='--', justify=tk.LEFT, font=self.helv)
        self.shear_label.grid(row=1, column=3, rowspan=6, sticky = tk.NW)
        
        self.shear_weak_label = tk.Label(self.calc_res_frame, text='--', justify=tk.LEFT, font=self.helv)
        self.shear_weak_label.grid(row=1, column=4, rowspan=6, sticky = tk.NW)
        
        self.definitions = self.aisc_db.definitions
                

    def quit_app(self):
        self.master.destroy()
        self.master.quit()
    
    def shapes_scroll(self, *args):
        self.shape_listbox.yview(*args)

    def shapes_data_scroll(self, *args):
        self.shape_data_listbox.yview(*args)
        
    def shape_change(self, *args):
        self.shape_listbox.delete(0,tk.END)
        shape = self.shape_picked.get()
        
        no_shape = 0
        
        if shape == 'W':
            self.shape_selection_list, self.shape_props_list = self.aisc_db.WF()
        elif shape == 'WT':
            self.shape_selection_list, self.shape_props_list = self.aisc_db.WT()
        elif shape == 'ST':
            self.shape_selection_list, self.shape_props_list = self.aisc_db.ST()
        elif shape == 'S':
            self.shape_selection_list, self.shape_props_list = self.aisc_db.S()
        elif shape == 'PIPE':
            self.shape_selection_list, self.shape_props_list = self.aisc_db.PIPE()
        elif shape == 'MT':
            self.shape_selection_list, self.shape_props_list = self.aisc_db.MT()
        elif shape == 'MC':
            self.shape_selection_list, self.shape_props_list = self.aisc_db.MC()
        elif shape == 'M':
            self.shape_selection_list, self.shape_props_list = self.aisc_db.M()
        elif shape == '2L':
            self.shape_selection_list, self.shape_props_list = self.aisc_db.LL()
        elif shape == 'L':
            self.shape_selection_list, self.shape_props_list = self.aisc_db.L()
        elif shape == 'HSS-SQR':
            self.shape_selection_list, self.shape_props_list = self.aisc_db.HSS_SQR()
        elif shape == 'HSS-RND':
            self.shape_selection_list, self.shape_props_list = self.aisc_db.HSS_RND()
        elif shape == 'HSS-RECT':
            self.shape_selection_list, self.shape_props_list = self.aisc_db.HSS_RECT()
        elif shape == 'HP':
            self.shape_selection_list, self.shape_props_list = self.aisc_db.HP()
        elif shape == 'C':
            self.shape_selection_list, self.shape_props_list = self.aisc_db.C()
        else:
            no_shape = 1
        
        if no_shape == 0:
            i=0
            for x in self.shape_selection_list:
                self.shape_listbox.insert(tk.END, x)
                
                if i % 2 == 0:
                    self.shape_listbox.itemconfigure(i, background="pale green")
                else:
                    pass
                i+=1
        else:
            pass

    def shape_click(self, *args):
                
        selection = self.shape_listbox.curselection()
        self.shape_defs = []
        
        if selection == ():
            pass
        else:
            self.shape_data_listbox.delete(0,tk.END)

            i=0
            count = 0
            for prop in self.shape_props_list[selection[0]]:
                if prop == '0.0000':
                    pass
                else:
                    prop_string = '{0} = {1} {2}'.format(self.shape_prop_labels[i],prop, self.aisc_db.units[i])
                    self.shape_data_listbox.insert(tk.END, prop_string)
                    
                    if count % 2 == 0:
                        self.shape_data_listbox.itemconfigure(count, background="pale green")
                    else:
                        pass
                    count+=1
                    
                    if 0 < i <84:
                        self.shape_defs.append(self.definitions[i-1])
                    else:
                        self.shape_defs.append(self.definitions[i-83])
                i+=1           

            self.W = self.shape_props_list[selection[0]]
            
            self.shape_calcs()
    
    def property_click(self, *args):
        
        selection = self.shape_data_listbox.curselection()
        index = selection[0]
        
        self.def_title.configure(text=self.shape_defs[index][0])
        self.def_text.delete(1.0,tk.END)
        self.def_text.insert(tk.END,self.shape_defs[index][1])
            
    def shape_calcs(self, *args):
            
            W = self.W
            self.calc_res_frame.configure(text='Shape: {0}'.format(W[2]))
            flexure_string = 'Flexure - Strong:\n'
            flexure_weak_string = 'Flexure - Weak:\n'
            shear_string = 'Shear - Strong:\n'
            shear_weak_string = 'Shear - Weak:\n'
            
            cb = float(self.cb_gui.get())
            Lb = float(self.lb_gui.get())*12.0
            E = float(self.E_gui.get())
            fy = float(self.fy_gui.get())
            Lv = float(self.lv_gui.get())*12.0
            
            shape = W[2]
            
            if W[0] == 'W' or W[0] == 'HP' or W[0] == 'S' or W[0] == 'M' or W[0] == 'C' or W[0] == 'MC':
                #Shape Flexure strong/weak and Shear strong/weak section props
                d = float(W[6])
                shear_string = shear_string + '{1}\nd = {0}\n'.format(W[6], shape)
                tw = float(W[16])
                shear_string = shear_string + 'tw = {0}\n'.format(W[16])
                zx = float(W[39])
                flexure_string = flexure_string + '{1}\nZx = {0}\n'.format(W[39], shape)
                cw = float(W[50])
                flexure_string = flexure_string + 'Cw = {0}\n'.format(W[50])
                rts = float(W[74])
                flexure_string = flexure_string + 'RTS = {0}\n'.format(W[74])
                J = float(W[49])
                flexure_string = flexure_string + 'J = {0}\n'.format(W[49])
                ry = float(W[45])
                flexure_string = flexure_string + 'ry = {0}\n'.format(W[45])
                sx = float(W[40])
                flexure_string = flexure_string + 'Sx = {0}\n'.format(W[40])
                ho = float(W[75])
                flexure_string = flexure_string + 'ho = {0}\n'.format(W[75])
                bf = float(W[11])
                flexure_string = flexure_string + 'bf = {0}\n'.format(W[11])
                shear_weak_string = shear_weak_string + '{1}\nbf = {0}\n'.format(W[11], shape)
                tf = float(W[19])
                flexure_string = flexure_string + 'tf = {0}\n'.format(W[19])
                shear_weak_string = shear_weak_string + 'tf = {0}\n'.format(W[19])
                h_tw = float(W[35])
                flexure_string = flexure_string + 'h/tw = {0}\n'.format(W[35])
                shear_string = shear_string + 'h/tw = {0}\n'.format(W[35])
                Iy = float(W[42])
                flexure_string = flexure_string + 'Iy = {0}\n'.format(W[35])
                
                zy = float(W[43])
                flexure_weak_string = flexure_weak_string + '{1}\nZy = {0}\n'.format(W[43], shape)
                sy = float(W[44])
                flexure_weak_string = flexure_weak_string + 'Sy = {0}\n'.format(W[44])
                
                #Slenderness
                
                #Strong axis Flange and web
                if W[0] == 'C' or W[0] == 'MC':
                    lam_f = bf / tf
                else:
                    lam_f = bf / (2.0*tf)
                    
                lam_w = h_tw
                
                lam_pf = 0.38 * (E/fy)**0.5
                lam_rf = 1.0 * (E/fy)**0.50
                
                lam_pw = 3.76 * (E/fy)**0.5
                lam_rw = 5.70 * (E/fy)**0.5
                
                if lam_f < lam_pf:
                    flange_compact = 'Compact'
                elif lam_f < lam_rf:
                    flange_compact = 'Non-Compact'
                else:
                    flange_compact = 'Slender'
                
                if lam_w < lam_pw:
                    web_compact = 'Compact'
                elif lam_w < lam_rw:
                    web_compact = 'Non-Compact'
                else:
                    web_compact = 'Slender'
                    
                flexure_string = flexure_string + '\nSlenderness:\nFlange is: {0}\n'.format(flange_compact)
                flexure_string = flexure_string + 'Web is: {0}\n'.format(web_compact)
                
                flexure_weak_string = flexure_weak_string + '\nSlenderness:\nFlange is: {0}\n'.format(flange_compact)
                
                #F2.1 - Yielding
                mn_y = fy * zx
                mp = mn_y
                flexure_string = flexure_string + '\nF2.1 Yielding:\nmp = {0:.2f} ft-kips (F2-1)\n'.format(mp/12.0)
                
                #F2.2 - Lateral Torsional Buckling
                if Lb == 0:
                    mn = mn_y
                    flexure_string = flexure_string + '\nF2.2 Lateral Torsional Buckling:\nN/A\n'
                else:
                    Lp = 1.76 * ry * (E/fy)**0.5
                    flexure_string = flexure_string + '\nF2.2 Lateral Torsional Buckling:\nLp = {0:.2f} ft (F2-5)\n'.format(Lp/12.0)
                    
                    if W[0] == 'C' or W[0] == 'MC':
                        c = (ho / 2.0) * (Iy/cw)**0.5
                        flexure_string = flexure_string + 'c = {0:.3f} (F2-8b)\n'.format(c) 
 
                    else:
                        c = 1.0
                        flexure_string = flexure_string + 'c = 1.0 (F2-8a)\n'
                    
                    Lr = 1.95*rts*(E/(0.7*fy))*(((J*c)/(sx*ho))**0.5)*(1.0 + (1.0 + 6.76*((((0.7*fy)/E))*((sx*ho)/(J*c)))**2)**0.5)**0.5
                    flexure_string = flexure_string + 'Lr = {0:.2f} ft (F2-6)\n'.format(Lr/12.0)
                    
                    Fcr = ((cb*(math.pi**2)*E)/(Lb/rts)**2) * (1.0 + (0.078 * ((J*c)/(sx*ho))*(Lb/rts)**2))**0.5
                    flexure_string = flexure_string + 'Fcr = {0:.2f} ksi (F2-4)\n'.format(Fcr)
                    
                    if Lb <= Lp:
                        mn = mn_y
                        flexure_string = flexure_string + 'N/A - Lb < Lp\n'
                        
                    elif Lp < Lb <= Lr:
                        mn_ltb = cb * (mn_y - ((mn_y - 0.7*fy*sx)*((Lb - Lp) / (Lr - Lp))))
                        flexure_string = flexure_string + 'Mn_ltb = {0:.2f} ft-kips (F2-2)\n'.format(mn_ltb/12.0)
                        mn = min(mn_ltb,mn_y)
                    
                    else:
                        mn_ltb = Fcr * sx
                        flexure_string = flexure_string + 'Mn_ltb = {0:.2f} ft-kips (F2-3)\n'.format(mn_ltb/12.0)
                        mn = min(mn_ltb, mn_y)
                
                #F3.2 - Compression Flange Local Buckling
                flexure_string = flexure_string + '\nF3.2 - Compression Flange Local Buckling\n'
                
                if W[0] == 'C' or W[0] == 'MC':
                    lam = bf / tf
                    flexure_string = flexure_string + 'Lambda = {0:.2f}\n'.format(lam)
                else:
                    lam = bf / (2.0*tf)
                    flexure_string = flexure_string + 'Lambda = {0:.2f}\n'.format(lam)
                    
                lam_pf = 0.38*(E/fy)**0.5
                flexure_string = flexure_string + 'Lambda,pf = {0:.2f}\n'.format(lam_pf)
                
                lam_rf = 1.0*(E/fy)**0.5
                flexure_string = flexure_string + 'Lambda,rf = {0:.2f}\n'.format(lam_rf)
                
                kc = min(max(4.0 / (h_tw)**0.5, 0.35),0.76)
                flexure_string = flexure_string + 'kc = {0:.3f}\n'.format(kc)
                
                if lam <= lam_pf:
                    mn_cflb = mp
                    flexure_string = flexure_string + 'N/A - Lambda < Lambda,pf\n'
                elif lam <= lam_rf:
                    mn_cflb = mp - ((mp - 0.7*fy*sx)*((lam - lam_pf)/(lam_rf - lam_pf)))
                    flexure_string = flexure_string + 'Mn_cflb = {0:.2f} ft-kips (F3-1)\n'.format(mn_cflb/12.0)
                else:
                    mn_cflb = 0.9*E*kc*sx / lam**2
                    flexure_string = flexure_string + 'Mn_cflb = {0:.2f} ft-kips (F3-2)\n'.format(mn_cflb/12.0)
                    
                mn = min(mn,mn_cflb)
                
                flexure_string = flexure_string + '\n\nMn = {0:.2f} ft-kips\nPhi = 0.9\nPhi*Mn = {1:.2f} ft-kips'.format(mn/12.0,0.9*(mn/12.0))
                
                #F6 - Weak Axis Bending
                #F6.1 - Yielding
                mp_weak = fy * zy
                mn_weak = min(mp_weak, 1.6*fy*sy)
                
                flexure_weak_string = flexure_weak_string + '\nF6.1 - Yielding:\nMp = {0:.2f} ft-kips\n'.format(mp_weak/12.0)
                flexure_weak_string = flexure_weak_string + '\nMn = min(Fy*Zy and 1.6*Fy*Sy)\nMn = {0:.2f} ft-kips\n'.format(mn_weak/12.0)
                
                #6.2 - Flange Local Buckling
                flexure_weak_string = flexure_weak_string + '\nF6.2 - Flange Local Buckling\n'
                
                if W[0] == 'C' or W[0] == 'MC':
                    lam = bf / tf
                    fcr = (0.69*E) / (lam*lam)
                    flexure_weak_string = flexure_weak_string + 'Lambda = {0:.2f}\n'.format(lam)
                else:
                    lam = bf / (2.0*tf)
                    fcr = (0.69*E) / (lam*lam)
                    flexure_weak_string = flexure_weak_string + 'Lambda = {0:.2f}\n'.format(lam)
                    
                lam_pf = 0.38*(E/fy)**0.5
                flexure_weak_string = flexure_weak_string + 'Lambda,pf = {0:.2f}\n'.format(lam_pf)
                
                lam_rf = 1.0*(E/fy)**0.5
                flexure_weak_string = flexure_weak_string + 'Lambda,rf = {0:.2f}\n'.format(lam_rf)                
                
                if lam <= lam_pf:
                    mn_flb = mn_weak
                    flexure_weak_string = flexure_weak_string + 'N/A - Lambda < Lambda,pf\n'
                elif lam <= lam_rf:
                    mn_flb = mp_weak - ((mp_weak - 0.7*fy*sy)*((lam - lam_pf)/(lam_rf - lam_pf)))
                    flexure_weak_string = flexure_weak_string + 'Fcr = {1:.2f} ksi\nMn_flb = {0:.2f} ft-kips (F6-2)\n'.format(mn_flb/12.0, fcr)
                else:
                    mn_flb = fcr * sy
                    flexure_weak_string = flexure_weak_string + 'Fcr = {1:.2f} ksi\nMn_flb = {0:.2f} ft-kips (F6-3)\n'.format(mn_flb/12.0, fcr)
                    
                mn_weak = min(mn_weak, mn_flb)
                flexure_weak_string = flexure_weak_string + '\n\nMn = {0:.2f} ft-kips\nPhi = 0.9\nPhi*Mn = {1:.2f} ft-kips'.format(mn_weak/12.0,0.9*(mn_weak/12.0))
                
                #Shear
                
                #G2.1 - Nominal Shear Strength
                shear_string = shear_string + '\nG2.1 - Nominal Shear Strength\n'
                
                if W[0] == 'C' or W[0] == 'MC':
                    #G2.1b
                    kv = 5.0
                    shear_string = shear_string + 'kv = 5.0 [G2-1 (i)]\n'
                    if h_tw <= 1.10 * ((kv*E)/fy)**0.5:
                        Cv = 1.0
                        shear_string = shear_string + 'Cv = {0:.2f} [G2-1b (i)][G2-3]\n'.format(Cv)
                    elif h_tw <= 1.37 * ((kv*E)/fy)**0.5:
                        Cv = (1.10 * ((kv*E)/fy)**0.5)/h_tw
                        shear_string = shear_string + 'Cv = {0:.2f} [G2-1b (ii)][G2-4]\n'.format(Cv)
                    else:
                        Cv = (1.51*E*kv)/(h_tw*h_tw*fy)
                        shear_string = shear_string + 'Cv = {0:.2f} [G2-1b (iii)][G2-5]\n'.format(Cv)
                    phi_v = 0.90

                else:
                    #G2.1a - rolled I shape?
                    if h_tw <= 2.24*(E/fy)**0.5:
                        Cv = 1.0
                        shear_string = shear_string + 'Cv = {0:.2f} [G2-1a][G2-2]\n'.format(Cv)
                        phi_v = 1.0
                    else:
                        #G2.1b
                        kv = 5.0
                        shear_string = shear_string + 'kv = 5.0 [G2-1b (i)]\n'
                        if h_tw <= 1.10 * ((kv*E)/fy)**0.5:
                            Cv = 1.0
                            shear_string = shear_string + 'Cv = {0:.2f} [G2-1b (i)][G2-3]\n'.format(Cv)
                        elif h_tw <= 1.37 * ((kv*E)/fy)**0.5:
                            Cv = (1.10 * ((kv*E)/fy)**0.5)/h_tw
                            shear_string = shear_string + 'Cv = {0:.2f} [G2-1b (ii)][G2-4]\n'.format(Cv)
                        else:
                            Cv = (1.51*E*kv)/(h_tw*h_tw*fy)
                            shear_string = shear_string + 'Cv = {0:.2f} [G2-1b (iii)][G2-5]\n'.format(Cv)
                        phi_v = 0.90
                
                Aw = d*tw
                shear_string = shear_string + 'Aw = {0:.2f} in2\n'.format(Aw)
                
                vn = 0.6*fy*Aw*Cv
                shear_string = shear_string + '\nVn = {0:.2f} kips [G2-1]\n'.format(vn)
                shear_string = shear_string + 'Phi = {0:.2f}\n'.format(phi_v)
                shear_string = shear_string + 'Phi*Vn = {0:.2f} kips\n'.format(phi_v*vn)
                
                #G7 - Weak Axis Shear
                shear_weak_string = shear_weak_string + '\nG7 - Weak Axis Shear in Singly\nand Doubly Symmetric Shapes\n'
                kv_weak = 1.2
                shear_weak_string = shear_weak_string + 'kv = 1.2 [G7]\n'
                bf_tf = bf/tf
                if bf_tf <= 1.10 * ((kv_weak*E)/fy)**0.5:
                    Cv_weak = 1.0
                    shear_weak_string = shear_weak_string + 'Cv = {0:.2f} [G2-1b (i)][G2-3]\n'.format(Cv_weak)
                elif bf_tf <= 1.37 * ((kv_weak*E)/fy)**0.5:
                    Cv_weak = (1.10 * ((kv_weak*E)/fy)**0.5)/bf_tf
                    shear_weak_string = shear_weak_string + 'Cv = {0:.2f} [G2-1b (ii)][G2-4]\n'.format(Cv_weak)
                else:
                    Cv_weak = (1.51*E*kv_weak)/(bf_tf*bf_tf*fy)
                    shear_weak_string = shear_weak_string + 'Cv = {0:.2f} [G2-1b (iii)][G2-5]\n'.format(Cv_weak)
                phi_v_weak = 0.90
                
                Aw_weak = 2*bf*tf
                shear_weak_string = shear_weak_string + 'Aw = 2*bf*tf= {0:.2f} in2 [G7]\n'.format(Aw_weak)
                
                vn_weak = 0.6*fy*Aw_weak*Cv_weak
                shear_weak_string = shear_weak_string + '\nVn = {0:.2f} kips [G2-1]\n'.format(vn_weak)
                shear_weak_string = shear_weak_string + 'Phi = {0:.2f}\n'.format(phi_v_weak)
                shear_weak_string = shear_weak_string + 'Phi*Vn = {0:.2f} kips\n'.format(phi_v_weak*vn_weak)
                
            elif W[0] == 'HSS-RECT' or W[0] == 'HSS-SQR':
                #Shape Flexure strong/weak and Shear strong/weak section props
                zx = float(W[39])
                flexure_string = flexure_string + '{1}\nZx = {0}\n'.format(W[39], shape)
                zy = float(W[43])
                flexure_weak_string = flexure_weak_string + '{1}\nZy = {0}\n'.format(W[43], shape)
                sx = float(W[40])
                flexure_string = flexure_string + 'Sx = {0}\n'.format(W[40])
                sy = float(W[44])
                flexure_weak_string = flexure_weak_string + 'Sy = {0}\n'.format(W[44])
                b = float(W[14])
                flexure_string = flexure_string + 'b = {0}\n'.format(W[14])
                shear_weak_string = shear_weak_string + '{1}\nb = {0}\n'.format(W[14], shape)
                h = float(W[9])
                flexure_weak_string = flexure_weak_string + 'h = {0}\n'.format(W[9])
                shear_string = shear_string + '{1}\nh = {0}\n'.format(W[9], shape)
                t = float(W[23])
                flexure_string = flexure_string + 't_des = {0}\n'.format(W[23])
                flexure_weak_string = flexure_weak_string + 't_des = {0}\n'.format(W[23])
                shear_string = shear_string + 't_des = {0}\n'.format(W[23])
                shear_weak_string = shear_weak_string + 't_des = {0}\n'.format(W[23])
                b_t = float(W[34])
                flexure_string = flexure_string + 'b/t_des = {0}\n'.format(W[34])
                h_t = float(W[36])
                flexure_weak_string = flexure_weak_string + 'h/t_des = {0}\n'.format(W[36])
                Ix =  float(W[38])
                flexure_string = flexure_string + 'Ix = {0}\n'.format(W[38])
                Iy = float(W[42])
                flexure_weak_string = flexure_weak_string + 'Iy = {0}\n'.format(W[42])
                B = float(W[13])
                H = float(W[8])
                
                #Slenderness
                
                #Strong
                if b_t <= 1.12 * (E/fy)**0.5:
                    flange_compact = 'Compact'
                elif b_t <= 1.40 * (E/fy)**0.5:
                    flange_compact = 'Non-Compact'
                else:
                    flange_compact = 'Slender'
                
                if h_t <= 2.42 * (E/fy)**0.5:
                    web_compact = 'Compact'
                elif h_t <= 5.70 * (E/fy)**0.5:
                    web_compact = 'Non-Compact'
                else:
                    web_compact = 'Slender'
                
                #Weak
                if h_t <= 1.12 * (E/fy)**0.5:
                    flange_weak_compact = 'Compact'
                elif h_t <= 1.40 * (E/fy)**0.5:
                    flange_weak_compact = 'Non-Compact'
                else:
                    flange_weak_compact = 'Slender'
                
                if b_t <= 2.42 * (E/fy)**0.5:
                    web_weak_compact = 'Compact'
                elif b_t <= 5.70 * (E/fy)**0.5:
                    web_weak_compact = 'Non-Compact'
                else:
                    web_weak_compact = 'Slender'
                    
                flexure_string = flexure_string + '\nSlenderness:\nFlange is: {0}\n'.format(flange_compact)
                flexure_string = flexure_string + 'Web is: {0}\n'.format(web_compact)
                
                flexure_weak_string = flexure_weak_string + '\nSlenderness:\nFlange is: {0}\n'.format(flange_weak_compact)
                flexure_weak_string = flexure_weak_string + 'Web is: {0}\n'.format(web_weak_compact)
                
                #Seff - Strong
                if flange_compact == 'Slender':
                    be = (1.92 * t * (E/fy)**0.5) * (1 - ((0.38/b_t)*(E/fy)**0.5))
                    
                    if be < b:
                         flexure_string = flexure_string + '\nbeff = {0:.3f} in [F7-4]\n'.format(be)
                         br = b - be
                         Ieff_x = Ix - (2 * (((br*t*t*t)/12.0) + (br*t*((H-t)/2)**2)))
                         flexure_string = flexure_string + 'Ieff,x = {0:.3f} in\n(Conservatively removes\n inefective compression\n flange from tension side also)\n'.format(Ieff_x)
                         Seff_x = Ieff_x / (H/2)
                         flexure_string = flexure_string + 'Seff,x = {0:.3f} in\n'.format(Seff_x)
                    else:
                         flexure_string = flexure_string + '\nbeff = {0:.3f} in\n'.format(b)
                         flexure_string = flexure_string + 'Ieff,x = {0:.3f} in\n'.format(Ix)
                         flexure_string = flexure_string + 'Seff,x = {0:.3f} in\n'.format(sx)
                         Seff_x = sx
                else:
                    pass
                
                #Seff - Weak
                if flange_weak_compact == 'Slender':
                    be = (1.92 * t * (E/fy)**0.5) * (1 - ((0.38/h_t)*(E/fy)**0.5))
                    
                    if be < h:
                         flexure_weak_string = flexure_weak_string + '\nbeff = {0:.3f} in [F7-4]\n'.format(be)
                         br = h - be
                         Ieff_y = Iy - (2 * (((br*t*t*t)/12.0) + (br*t*((B-t)/2)**2)))
                         flexure_weak_string = flexure_weak_string + 'Ieff,y = {0:.3f} in\n(Conservatively removes\n inefective compression\n flange from tension side also)\n'.format(Ieff_y)
                         Seff_y = Ieff_y / (B/2)
                         flexure_weak_string = flexure_weak_string + 'Seff,y = {0:.3f} in\n'.format(Seff_y)
                    else:
                         flexure_weak_string = flexure_weak_string + '\nbeff = {0:.3f} in\n'.format(h)
                         flexure_weak_string = flexure_weak_string + 'Ieff,y = {0:.3f} in\n'.format(Iy)
                         flexure_weak_string = flexure_weak_string + 'Seff,y = {0:.3f} in\n'.format(sy)
                         Seff_y = sy
                else:
                    pass
                
                #F7.1 - Yielding
                flexure_string = flexure_string + '\nF7.1 - Yielding\n'
                flexure_weak_string = flexure_weak_string + '\nF7.1 - Yielding\n'
                
                mp = fy*zx
                flexure_string = flexure_string + 'Mp = {0:.3f} ft-kips\n'.format(mp/12.0)
                mp_weak = fy*zy
                flexure_weak_string = flexure_weak_string + 'Mp = {0:.3f} ft-kips\n'.format(mp_weak/12.0)
                
                #F7.2 - Flange Local Buckling
                flexure_string = flexure_string + '\nF7.2 - Flange Local Buckling\n'
                flexure_weak_string = flexure_weak_string + '\nF7.2 - Flange Local Buckling\n'
                
                #Strong
                if flange_compact == 'Compact':
                    flexure_string = flexure_string + 'N/A\n'
                    mn_flb = mp
                
                elif flange_compact == 'Non-Compact':
                    mn_flb = mp - ((mp - (fy*sx)) * ((3.57*b_t*(fy/E)**0.5)-4.0))
                    mn_flb = min(mn_flb,mp)
                    flexure_string = flexure_string + 'Mn,flb = {0:.3f} ft-kips\n'.format(mn_flb/12.0)
                else:
                    mn_flb = fy * Seff_x
                    flexure_string = flexure_string + 'Mn,flb = {0:.3f} ft-kips\n'.format(mn_flb/12.0)
                
                #Weak
                if flange_weak_compact == 'Compact':
                    flexure_weak_string = flexure_weak_string + 'N/A\n'
                    mn_weak_flb = mp_weak
                
                elif flange_weak_compact == 'Non-Compact':
                    mn_weak_flb = mp_weak - ((mp_weak - (fy*sy)) * ((3.57*h_t*(fy/E)**0.5)-4.0))
                    mn_weak_flb = min(mn_weak_flb,mp_weak)
                    flexure_weak_string = flexure_weak_string + 'Mn,flb = {0:.3f} ft-kips\n'.format(mn_weak_flb/12.0)
                else:
                    mn_weak_flb = fy * Seff_y
                    flexure_weak_string = flexure_weak_string + 'Mn,flb = {0:.3f} ft-kips\n'.format(mn_weak_flb/12.0)

                #F7.3 - Web Local Buckling
                flexure_string = flexure_string + '\nF7.3 - Web Local Buckling\n'
                flexure_weak_string = flexure_weak_string + '\nF7.3 - Web Local Buckling\n'
                
                #Strong
                if web_compact == 'Compact':
                    flexure_string = flexure_string + 'N/A\n'
                    mn_wlb = mp
                
                elif web_compact == 'Non-Compact':
                    mn_wlb = mp - ((mp - (fy*sx)) * ((0.305*h_t*(fy/E)**0.5)-0.738))
                    mn_wlb = min(mn_wlb,mp)
                    flexure_string = flexure_string + 'Mn,wlb = {0:.3f} ft-kips\n'.format(mn_wlb/12.0)
                else:
                    mn_wlb = 0
                    flexure_string = flexure_string + 'Mn,wlb = {0:.3f} ft-kips\n'.format(mn_wlb/12.0)
                
                #Weak
                if web_weak_compact == 'Compact':
                    flexure_weak_string = flexure_weak_string + 'N/A\n'
                    mn_weak_wlb = mp_weak
                
                elif web_weak_compact == 'Non-Compact':
                    mn_weak_wlb = mp_weak - ((mp_weak - (fy*sy)) * ((0.305*b_t*(fy/E)**0.5)-0.738))
                    mn_weak_wlb = min(mn_weak_wlb,mp_weak)
                    flexure_weak_string = flexure_weak_string + 'Mn,wlb = {0:.3f} ft-kips\n'.format(mn_weak_wlb/12.0)
                else:
                    mn_weak_wlb = 0
                    flexure_weak_string = flexure_weak_string + 'Mn,wlb = {0:.3f} ft-kips\n'.format(mn_weak_wlb/12.0)
                
                #strong
                mn = min(mp, mn_flb, mn_wlb)
                phi = 0.9
                phi_mn = phi*mn
                
                flexure_string = flexure_string + '\n\nMn = {0:.3f} ft-kips\nphi = {1:.2f}\nphi*Mn = {2:.3f} ft-kips'.format(mn/12.0, phi, phi_mn/12.0)

                #weak
                mn_weak = min(mp_weak, mn_weak_flb, mn_weak_wlb)
                phi_mn_weak = phi*mn_weak
                
                flexure_weak_string = flexure_weak_string + '\n\nMn = {0:.3f} ft-kips\nphi = {1:.2f}\nphi*Mn = {2:.3f} ft-kips'.format(mn_weak/12.0, phi, phi_mn_weak/12.0)                

                #Shear
                
                #G5 - Nominal Shear Strength
                shear_string = shear_string + '\nG5 - Rectangular HSS and Box Members\n'
                
                #G5 -> G2.1b
                kv = 5.0
                shear_string = shear_string + 'kv = 5.0 [G5]\n'
                if h_t <= 1.10 * ((kv*E)/fy)**0.5:
                    Cv = 1.0
                    shear_string = shear_string + 'Cv = {0:.2f} [G2-1b (i)][G2-3]\n'.format(Cv)
                elif h_t <= 1.37 * ((kv*E)/fy)**0.5:
                    Cv = (1.10 * ((kv*E)/fy)**0.5)/h_t
                    shear_string = shear_string + 'Cv = {0:.2f} [G2-1b (ii)][G2-4]\n'.format(Cv)
                else:
                    Cv = (1.51*E*kv)/(h_t*h_t*fy)
                    shear_string = shear_string + 'Cv = {0:.2f} [G2-1b (iii)][G2-5]\n'.format(Cv)
                phi_v = 0.90
                
                Aw = 2*h*t
                shear_string = shear_string + 'Aw = 2*h*t = {0:.2f} in2 [G5]\n'.format(Aw)
                
                vn = 0.6*fy*Aw*Cv
                shear_string = shear_string + '\nVn = {0:.2f} kips [G2-1]\n'.format(vn)
                shear_string = shear_string + 'Phi = {0:.2f}\n'.format(phi_v)
                shear_string = shear_string + 'Phi*Vn = {0:.2f} kips\n'.format(phi_v*vn)
                
                #G7 - Weak Axis Shear
                shear_weak_string = shear_weak_string + '\nG5 - Rectangular HSS and Box Members\n'
                kv_weak = 5
                shear_weak_string = shear_weak_string + 'kv = 5 [G5]\n'
                if b_t <= 1.10 * ((kv_weak*E)/fy)**0.5:
                    Cv_weak = 1.0
                    shear_weak_string = shear_weak_string + 'Cv = {0:.2f} [G2-1b (i)][G2-3]\n'.format(Cv_weak)
                elif b_t <= 1.37 * ((kv_weak*E)/fy)**0.5:
                    Cv_weak = (1.10 * ((kv_weak*E)/fy)**0.5)/b_t
                    shear_weak_string = shear_weak_string + 'Cv = {0:.2f} [G2-1b (ii)][G2-4]\n'.format(Cv_weak)
                else:
                    Cv_weak = (1.51*E*kv_weak)/(b_t*bf_tf*fy)
                    shear_weak_string = shear_weak_string + 'Cv = {0:.2f} [G2-1b (iii)][G2-5]\n'.format(Cv_weak)
                phi_v_weak = 0.90
                
                Aw_weak = 2*b*t
                shear_weak_string = shear_weak_string + 'Aw = 2*b*t= {0:.2f} in2 [G7]\n'.format(Aw_weak)
                
                vn_weak = 0.6*fy*Aw_weak*Cv_weak
                shear_weak_string = shear_weak_string + '\nVn = {0:.2f} kips [G2-1]\n'.format(vn_weak)
                shear_weak_string = shear_weak_string + 'Phi = {0:.2f}\n'.format(phi_v_weak)
                shear_weak_string = shear_weak_string + 'Phi*Vn = {0:.2f} kips\n'.format(phi_v_weak*vn_weak)                
                    
            elif W[0] == 'HSS-RND' or W[0] == 'PIPE':
                #Shape Flexure strong/weak and Shear strong/weak section props
                shear_weak_string = ''
                flexure_weak_string = ''
                
                D_t = float(W[37])
                flexure_string = flexure_string + '{1}\nD/t = {0}\n'.format(W[37], shape)
                shear_string = shear_string + '{1}\nD/t = {0}\n'.format(W[37], shape)
                Z = float(W[39])
                flexure_string = flexure_string + 'Z = Zx = Zy = {0}\n'.format(W[39])
                S = float(W[40])
                flexure_string = flexure_string + 'S = Sx = Sy = {0}\n'.format(W[40])
                Ag = float(W[5])
                shear_string = shear_string + 'Ag = {0}\n'.format(W[5])
                OD = float(W[10])
                shear_string = shear_string + 'OD = {0}\n'.format(W[10])
                shear_string = shear_string + 'Lv = {0:.2f} in\n'.format(Lv)
                
                if D_t > 0.45 * E/fy:
                    flexure_string = flexure_string + '\nD/t > 0.45E/Fy\n'
                else:
                    flexure_string = flexure_string + '\nD/t < 0.45E/Fy = {0:.3f}\n'.format(0.45 * E/fy)
                    #F8.1 - Yielding
                    flexure_string = flexure_string + '\nF8.1 - Yielding\n'
                    mp = fy*Z
                    flexure_string = flexure_string + 'Mp = {0:.3f} ft-kips [F8-1]\n'.format(mp/12.0)
                    
                    #Slenderness and F8.2 - Local Buckling
                    flexure_string = flexure_string + '\nF8.2 - Local Buckling'
                    if D_t <= 0.7*E/fy:
                        flexure_string = flexure_string + '\nSlenderess: Compact\n'
                        m_lb = mp
                        flexure_string = flexure_string + '\nN/A\n'
                        
                    elif D_t <= 0.31*E/fy:
                        flexure_string = flexure_string + '\nSlenderess: Non-Compact\n'
                        m_lb = (((0.021*E)/D_t) + fy)*S
                        flexure_string = flexure_string + 'M_lb = {0:.3f} ft-kips [F8-2]\n'.format(m_lb/12.0)
                        
                    else:
                        flexure_string = flexure_string + '\nSlenderess: Slender\n'
                        Fcr = 0.33*E / D_t
                        m_lb = Fcr*S
                        flexure_string = flexure_string + 'Fcr = {1:.3f} ksi [F8-4]\nM_lb = {0:.3f} ft-kips [F8-3]\n'.format(m_lb/12.0)
                    
                    mn = min(mp,m_lb)
                    phi = 0.9
                    phi_mn = phi * mn
                    
                    flexure_string = flexure_string + '\n\nMn = {0:.3f} ft-kips\nphi = {1:.2f}\nphi*Mn = {2:.3f} ft-kips'.format(mn/12.0, phi, phi_mn/12.0)
                
                #Shear
                shear_string = shear_string + '\nG6 - Round HSS\n'
                
                fcr_g6_2a = (1.6*E) / (((Lv/OD)**0.5)*(D_t)**(5/4.0))
                shear_string = shear_string + '\nFcr = {0:.3f} ksi [G6-2a]\n'.format(fcr_g6_2a)
                
                fcr_g6_2b = (0.78*E) / D_t**(3/2.0)
                shear_string = shear_string + '\nFcr = {0:.3f} ksi [G6-2b]\n'.format(fcr_g6_2b)
                
                fcr = min(0.6*fy,max(fcr_g6_2a, fcr_g6_2b))
                shear_string = shear_string + '\nFcr shall not exceed 0.6Fy = {1:.3f} ksi\nFcr = {0:.3f} ksi \n'.format(fcr,0.6*fy)
                
                vn = fcr*Ag*0.5
                phi_v = 0.9

                shear_string = shear_string + '\nVn = {0:.2f} kips [G6-1]\n'.format(vn)
                shear_string = shear_string + 'Phi = {0:.2f}\n'.format(phi_v)
                shear_string = shear_string + 'Phi*Vn = {0:.2f} kips\n'.format(phi_v*vn)                
            
            elif W[0] == '2L' or W[0] == 'MT' or W[0] == 'ST' or W[0] == 'WT':
                pass
                
            else:
                pass
            
            self.flexure_label.configure(text=flexure_string)
            self.flexure_weak_label.configure(text=flexure_weak_string)
            self.shear_label.configure(text=shear_string)
            self.shear_weak_label.configure(text=shear_weak_string)

        
def main():
    root = tk.Tk()
    root.title("Steel Calculator")
    Master_window(root)
    root.minsize(1024,768)
    root.mainloop()

if __name__ == '__main__':
    main()   
