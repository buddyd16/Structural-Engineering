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

import Tkinter as tk
import tkFont
import tkMessageBox

class Master_window:

    def __init__(self, master):
        
        ## BUILD SHAPE DICTIONARY AND ATTRIBUTE LISTS
        file = open('aisc_shapes_historic_clean.csv','r')
        
        data_raw = file.readlines()
        
        file.close()

        file = open('aisc_historic_shape_defs.csv','r')
        
        defs_raw = file.readlines()
        
        file.close()
        
        self.shape_defs = []
        data = []
        for line in data_raw:
            line = line.split(',')
            line[-1]=line[-1].rstrip('\n')
            data.append(line)
            
        for line in defs_raw:
            line = line.split(',')
            line[-1]=line[-1].rstrip('\n')
            self.shape_defs.append(line)
   
        edition_raw = []   
        [edition_raw.append(d[0]) for d in data[1:]]
        
        self.edition = list(set(edition_raw))
        
        self.shape_sets = []
        self.shapes = []
        for x in range(0,len(self.edition)):
            self.shape_sets.append([])
            self.shapes.append([])
        
        for d in data[1:]:
            index = self.edition.index(d[0])
            self.shape_sets[index].append(d[2])
        
        for i in range(0,len(self.shape_sets)):
            s = list(set(self.shape_sets[i]))
            self.shape_sets[i] = s
        
        self.values_list = data[0][4:]
        for x in range(0,len(self.shape_sets)):
            for y in range(0,len(self.shape_sets[x])):
                self.shapes[x].append({})
        count = 1
        shape = ''
        st=''
        for d in data[1:]:
            index_1 = self.edition.index(d[0])
            index_2 = self.shape_sets[index_1].index(d[2])
            if d[3] == shape[:-1*len(st)] or d[3] == shape:
                st = '_{0}'.format(count)
                shape = d[3]+st
                count+=1
            else:
                shape = d[3]
                st=''
                count=1
            shape_data = d[4:]
            temp_shape_dict = {shape: shape_data}
            self.shapes[index_1][index_2].update(temp_shape_dict)
        
        ## BEGIN BUILDING MAIN GUI WINDOW ##
        self.widgets=[]
        self.master = master
        self.f_size = 8
        helv = tkFont.Font(family='Helvetica',size=self.f_size, weight='bold')
        self.menubar = tk.Menu(self.master)
        self.menu = tk.Menu(self.menubar, tearoff=0)
        self.menu_props = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label = "File", menu=self.menu)
        self.menu.add_command(label="Quit", command=self.quit_app)
        self.menubar.add_cascade(label = "Window Properties", menu=self.menu_props)
        self.menu_props.add_command(label="Increase Font Size", command=self.font_size_up)
        self.menu_props.add_command(label="Decrease Font Size", command=self.font_size_down)
        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            self.master.tk.call(master, "config", "-menu", self.menubar)
        
        #Main Frames
        self.main_frame = tk.Frame(master, bd=2, relief='sunken', padx=5,pady=5)
        self.main_frame.pack(anchor='c', padx= 5, pady= 5, fill=tk.BOTH, expand=1)
        self.base_frame = tk.Frame(master, bd=2, relief='sunken', padx=5,pady=5)
        self.base_frame.pack(side=tk.BOTTOM, padx= 5, pady= 5, fill=tk.X, expand=1)

        #Picker Frame
        self.picker_frame = tk.Frame(self.main_frame, padx=2, pady=2)
        self.menu_frame = tk.Frame(self.picker_frame, padx=0, pady=0)
        self.edition_type = tk.StringVar()
        self.edition_type.set(self.edition[0])
        self.edition_type_label = tk.Label(self.menu_frame, text="AISC Edition : ", font=helv)
        self.widgets.append(self.edition_type_label)
        self.edition_type_label.pack(side=tk.TOP, fill=tk.X, expand=True)
        self.edition_type_menu = tk.OptionMenu(self.menu_frame, self.edition_type, *self.edition, command=self.edition_change)
        self.edition_type_menu.config(font=helv)
        self.edition_type_menu.pack(side=tk.TOP, fill=tk.X, expand=True)
        self.shape_type = tk.StringVar()
        self.shape_type.set(self.shape_sets[0][0])
        self.shape_type_label = tk.Label(self.menu_frame, text="Steel Shape Type : ", font=helv)
        self.widgets.append(self.shape_type_label)
        self.shape_type_label.pack(side=tk.TOP, fill=tk.X, expand=True)
        self.shape_type_menu = tk.OptionMenu(self.menu_frame, self.shape_type, *self.shape_sets[0], command=self.shape_change)
        self.shape_type_menu.config(font=helv)
        self.shape_type_menu.pack(side=tk.TOP, fill=tk.X, expand=True)
        self.menu_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

        self.shape_frame = tk.LabelFrame(self.picker_frame, text="Section:", bd=1, relief='sunken', padx=5, pady=5, font=helv)
        self.widgets.append(self.shape_frame)
        
        self.shape_menu = tk.Listbox(self.shape_frame, height = 20, width = 40, font=helv)
        self.widgets.append(self.shape_menu)
        for section in sorted(self.shapes[0][0].keys()):
            self.shape_menu.insert(tk.END, section)
        self.shape_menu.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        
        self.shape_scrollbar = tk.Scrollbar(self.shape_frame, orient="vertical")
        self.shape_menu.config(yscrollcommand=self.shape_scrollbar.set)
        self.shape_scrollbar.config(command=self.shape_menu.yview)
        self.shape_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.shape_menu.bind("<<ListboxSelect>>",self.shape_click)
        self.shape_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.picker_frame.pack(side=tk.LEFT)
        
        self.data_frame = tk.LabelFrame(self.main_frame, text="Section Properties - AISC 14th Edition:", bd=1, relief='sunken', padx=5, pady=5, font=helv)
        self.widgets.append(self.data_frame)
        self.properties_labels = []
        for i in range(0,len(self.values_list)):
            self.properties_labels.append('{0}: -- {1}'.format(self.values_list[i],self.shape_defs[i][1]))
        j=0
        z=0
        self.properties_list = tk.Listbox(self.data_frame, height = 40, width = 30, font=helv, exportselection=0)
        for line in self.properties_labels:
            self.properties_list.insert(tk.END, line)
        self.properties_list.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        self.properties_list.bind("<<ListboxSelect>>",self.prop_list_click)
        self.widgets.append(self.properties_list)
        self.properties_list_values = tk.Listbox(self.data_frame, height = 40, width = 15, font=helv, exportselection=0)
        self.properties_list_values.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        self.properties_list_values.bind("<<ListboxSelect>>",self.prop_list_value_click)
        self.widgets.append(self.properties_list_values)
        self.data_frame.pack(side=tk.LEFT)
        
        self.f_size_frame = tk.Frame(self.base_frame, padx=5,pady=5)
        self.f_size_label = tk.Label(self.f_size_frame, text='Font Size ('+str(self.f_size)+'):', font=helv)
        self.widgets.append(self.f_size_label)
        self.f_size_label.grid(row=0,column=0)
        self.b_f_size_minus = tk.Button(self.f_size_frame,text="-", command=self.font_size_down, font=helv)
        self.widgets.append(self.b_f_size_minus)
        self.b_f_size_minus.grid(row=0, column=1, padx=1, pady=1)
        self.b_f_size_plus = tk.Button(self.f_size_frame,text="+", command=self.font_size_up, font=helv)
        self.widgets.append(self.b_f_size_plus)
        self.b_f_size_plus.grid(row=0, column=2, padx=1, pady=1)
        self.f_size_frame.pack(side=tk.LEFT)
        
        self.value_def_frame = tk.Frame(self.base_frame, padx=5,pady=5)
        self.value_def = tk.StringVar()
        self.value_def.set(self.values_list[0])
        self.value_def_menu = tk.OptionMenu(self.value_def_frame, self.value_def, *self.values_list, command=self.value_definitions)
        self.value_def_menu.config(font=helv)
        self.value_def_menu.grid(row=0, column=0, padx=1, pady=1)
        self.value_def_label = tk.Label(self.value_def_frame, text=self.shape_defs[0][0], font=helv, wraplength=400, justify=tk.LEFT)
        self.widgets.append(self.value_def_label)
        self.value_def_label.grid(row=0, column=1, padx=10, pady=1)
        filters = ['=','<','>','Between']
        self.value_filter = tk.StringVar()
        self.value_filter.set('=')
        self.value_filter_menu = tk.OptionMenu(self.value_def_frame, self.value_filter, *filters, command=self.value_filter_menu_switch)
        self.value_filter_menu.config(font=helv)
        self.value_filter_menu.grid(row=1, column=0, padx=1, pady=1)
        self.filter_a = tk.StringVar()
        self.entry_filter_a = tk.Entry(self.value_def_frame,textvariable=self.filter_a, font = helv, width = 15)
        self.widgets.append(self.entry_filter_a)
        self.entry_filter_a.grid(row=1, column=1, padx=1, pady=1)
        self.filter_b = tk.StringVar()
        self.entry_filter_b = tk.Entry(self.value_def_frame,textvariable=self.filter_b, font = helv, width = 15)
        self.widgets.append(self.entry_filter_b)
        self.entry_filter_b.grid(row=2, column=1, padx=1, pady=1)
        self.entry_filter_b.configure(state="disabled")
        self.b_value_filter = tk.Button(self.value_def_frame,text="Filter By Selected Value", command=self.value_filter_function)
        self.b_value_filter.grid(row=1, column=2, padx=1, pady=1)
        self.widgets.append(self.b_value_filter)
        self.b_reset_filter = tk.Button(self.value_def_frame,text="Reset Shape List", command=self.shape_change)
        self.b_reset_filter.grid(row=1, column=3, padx=1, pady=1)
        self.widgets.append(self.b_reset_filter)
        self.value_def_frame.pack(side=tk.LEFT, padx= 5, pady= 5)
        
        self.b_quit = tk.Button(self.base_frame,text="Quit", command=self.quit_app, font=helv)
        self.widgets.append(self.b_quit)
        self.b_quit.pack(side=tk.RIGHT)
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
        
    def edition_change(self, *event):
        self.shape_type_menu.destroy()
        edition = self.edition_type.get()
        edition_index = self.edition.index(edition)
        self.shape_type_menu = tk.OptionMenu(self.menu_frame, self.shape_type, *self.shape_sets[edition_index], command=self.shape_change)
        helv = tkFont.Font(family='Helvetica',size=self.f_size, weight='bold')
        self.shape_type_menu.config(font=helv)
        self.shape_type_menu.pack(side=tk.TOP, fill=tk.X, expand=True)
        self.shape_type.set(self.shape_sets[edition_index][0])
        
    def shape_change(self, *event):
        self.shape_menu.delete(0,tk.END)
        edition = self.edition_type.get()
        edition_index = self.edition.index(edition)
        new_shape_type = self.shape_type.get()
        new_shape_type_index = self.shape_sets[edition_index].index(new_shape_type)
        new_section_list = self.shapes[edition_index][new_shape_type_index]
        for section in new_section_list:
            self.shape_menu.insert(tk.END, section)
        self.shape_menu.selection_set(0)
        self.shape_click()
        self.shape_frame.configure(text='Section: ')
        
    def prop_list_click(self, *event):
        pindex = self.properties_list.index(self.properties_list.curselection())
        self.properties_list_values.selection_clear(0,tk.END)
        self.properties_list_values.selection_set(pindex)
        
    def prop_list_value_click(self, *event):
        pindex = self.properties_list_values.index(self.properties_list_values.curselection())
        self.properties_list.selection_clear(0,tk.END)
        self.properties_list.selection_set(pindex)
        
    def shape_click(self, *event):
        shape = self.shape_menu.get(self.shape_menu.curselection())
        edition = self.edition_type.get()
        edition_index = self.edition.index(edition)
        shape_type = self.shape_type.get()
        shape_type_index = self.shape_sets[edition_index].index(shape_type)
        section_props = self.shapes[edition_index][shape_type_index].get(shape)

        self.data_frame.configure(text="Section Properties - "+edition+":  --  Selected Shape: "+shape)

        props_counter = 0
        props_list = []
        props = []
        l = 0
        self.properties_list.delete(0,tk.END)
        self.properties_list_values.delete(0,tk.END)
        for i in range(0,len(self.values_list)):
            if section_props[i] == '0':
               pass
            else:
                if self.shape_defs[i][1] == '-':
                    string = '{0} : '.format(self.values_list[i])
                    props.append(string)
                    l=max(len(string),l)
                    
                    self.properties_list_values.insert(tk.END, section_props[i])

                else:
                    string = '{0} ({1}) : '.format(self.values_list[i],self.shape_defs[i][1])
                    props.append(string)
                    l=max(len(string),l)
                    self.properties_list_values.insert(tk.END, section_props[i])
                props_list.append(self.values_list[i])
                props_counter+=1
                
        for line in props:
            # x = len(line)
            # count = (l+1) - x
            # st = '  '*count
            # line = st + line
            self.properties_list.insert(tk.END,line)

        self.properties_list.configure(height=len(props), width = l+1)
        self.properties_list_values.configure(height=len(props))
        self.value_def_menu.destroy()
        self.value_def_menu = tk.OptionMenu(self.value_def_frame, self.value_def, *props_list, command=self.value_definitions)
        helv = tkFont.Font(family='Helvetica',size=self.f_size, weight='bold')
        self.value_def_menu.config(font=helv)
        self.value_def_menu.grid(row=0, column=0, padx=1, pady=1)
        self.value_def.set(props_list[0])
        self.value_definitions()
        
    def value_definitions(self, *event):
        index = self.values_list.index(self.value_def.get())
        self.value_def_label.configure(text = self.shape_defs[index][0])
        
    def font_size_up(self, *event):
        self.f_size = self.f_size+1
        helv = tkFont.Font(family='Helvetica',size=self.f_size, weight='bold')
        self.f_size_label.configure(text='Font Size ('+str(self.f_size)+'):')
        self.edition_type_menu.config(font=helv)
        self.shape_type_menu.config(font=helv)
        for widget in self.widgets:
            widget.configure(font=helv)
    
    def font_size_down(self, *event):
        if self.f_size-1 < 6:
            self.f_size = 6
        else:
            self.f_size = self.f_size-1
            
        helv = tkFont.Font(family='Helvetica',size=self.f_size, weight='bold')
        self.f_size_label.configure(text='Font Size ('+str(self.f_size)+'):')
        self.edition_type_menu.config(font=helv)
        self.shape_type_menu.config(font=helv)
        for widget in self.widgets:
            widget.configure(font=helv)
    
    def value_filter_menu_switch(self, *event):
        option = self.value_filter.get()
        if option == 'Between':
            self.entry_filter_b.configure(state="normal")
        else:
            self.entry_filter_b.configure(state="disabled")
            
    def value_filter_function(self, *event):
        a = self.filter_a.get()
        b = self.filter_b.get()
        filter_type = self.value_filter.get()
        self.shape_menu.delete(0,tk.END)
        
        value_index = self.values_list.index(self.value_def.get())
        edition = self.edition_type.get()
        edition_index = self.edition.index(edition)
        shape_type = self.shape_type.get()
        shape_type_index = self.shape_sets[edition_index].index(shape_type)
        
        filtered_section_list = []

        d = self.shapes[edition_index][shape_type_index]
        new_section_list = sorted(d, key=lambda k: (float(d[k][value_index])))
        
        if a == '':
            pass
        
        else:
            if filter_type == 'Between' and b == '':
                pass
                
            elif filter_type == 'Between':
                string = 'Section: - Sorted By: {0} Between {1} and {2}'.format(self.values_list[value_index],a,b)
                for key in new_section_list:
                    if float(a) > float(b):
                        a = self.filter_b.get()
                        b = self.filter_a.get()
                    else:
                        pass
                    if float(d[key][value_index]) >= float(a) and float(d[key][value_index]) <= float(b):
                        filtered_section_list.append(key)
                    else:
                        pass
            elif filter_type == '<':
                string = 'Section: - Sorted By: {0} < {1}'.format(self.values_list[value_index],a)
                for key in new_section_list:
                    if float(d[key][value_index]) <= float(a):
                        filtered_section_list.append(key)
                    else:
                        pass
            elif filter_type == '>':
                string = 'Section: - Sorted By: {0} > {1}'.format(self.values_list[value_index],a)
                for key in new_section_list:
                    if float(d[key][value_index]) >= float(a):
                        filtered_section_list.append(key)
                    else:
                        pass
            elif filter_type == '=':
                string = 'Section: - Sorted By: {0} = {1}'.format(self.values_list[value_index],a)
                for key in new_section_list:
                    if float(d[key][value_index]) == float(a):
                        filtered_section_list.append(key)
                    else:
                        pass
        if len(filtered_section_list) == 0:
            self.shape_menu.delete(0,tk.END)
            
        else:
            for section in filtered_section_list:
                 self.shape_menu.insert(tk.END, section)
        self.shape_frame.configure(text=string)
        
def main():
    root = tk.Tk()
    root.title("AISC 14th Edition - Shape Database")
    app = Master_window(root)
    root.minsize(800,600)
    root.mainloop()

if __name__ == '__main__':
    main()   
