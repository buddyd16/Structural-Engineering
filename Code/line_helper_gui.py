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
import Tkinter as tk


class Main_window:

    def __init__(self, master):
        self.master = master
        ## Main Frame        
        self.main_frame = tk.Frame(master, bd=2, relief='sunken', padx=10,pady=20)
        self.main_frame.pack(anchor='c', padx= 10, pady= 20)
        
        ## Entry Frame
        self.frame_entry = tk.Frame(self.main_frame, padx=5, pady=5)        
        
        self.enter_label = tk.Label(self.frame_entry, text="Enter Lines in counterclock wise order")
        self.enter_label.grid(row=0,column=0, pady=5)
        
        self.start_x = tk.StringVar()
        self.start_x_label = tk.Label(self.frame_entry, text="Start x (ft) : ")
        self.start_x_label.grid(row=1,column=0, pady=5)
        self.start_x_entry = tk.Entry(self.frame_entry,textvariable=self.start_x)
        self.start_x_entry.grid(row=1,column=1, pady=5)
        
        self.start_y = tk.StringVar()
        self.start_y_label = tk.Label(self.frame_entry, text="Start y (ft) : ")
        self.start_y_label.grid(row=2,column=0, pady=5)
        self.start_y_entry = tk.Entry(self.frame_entry,textvariable=self.start_y)
        self.start_y_entry.grid(row=2,column=1, pady=5)
        
        
        self.end_x = tk.StringVar()
        self.end_x_label = tk.Label(self.frame_entry, text="End x (ft) : ")
        self.end_x_label.grid(row=3,column=0, pady=5)
        self.end_x_entry = tk.Entry(self.frame_entry,textvariable=self.end_x)
        self.end_x_entry.grid(row=3,column=1, pady=5)
        
        self.end_y = tk.StringVar()
        self.end_y_label = tk.Label(self.frame_entry, text="End y (ft) : ")
        self.end_y_label.grid(row=4,column=0, pady=5)
        self.end_y_entry = tk.Entry(self.frame_entry,textvariable=self.end_y)
        self.end_y_entry.grid(row=4,column=1, pady=5)
        
        self.hc_in = tk.StringVar()
        self.hc_in_label = tk.Label(self.frame_entry, text="Hc (ft) : ")
        self.hc_in_label.grid(row=5,column=0, pady=5)
        self.hc_in_entry = tk.Entry(self.frame_entry,textvariable=self.hc_in)
        self.hc_in_entry.grid(row=5,column=1, pady=5)
        
        self.loc = tk.StringVar()
        self.loc.set('e')
        self.loc_label = tk.Label(self.frame_entry, text="e or i : ")
        self.loc_label.grid(row=6,column=0, pady=5)
        choice = ['e','i']
        self.loc_entry = tk.OptionMenu(self.frame_entry,self.loc, *choice)
        self.loc_entry.grid(row=6,column=1, pady=5)
        
        self.b_prev = tk.Button(self.frame_entry,text="Start = Last End", command=self.prev_point)
        self.b_prev.grid(row=1,column=2, padx=5, pady=5)
        
        self.b_add = tk.Button(self.frame_entry,text="Add Line", command=self.add_line)
        self.b_add.grid(row=7,column=1, pady=5)
        
        self.x = tk.StringVar()
        self.x_label = tk.Label(self.frame_entry, text="x_out: ")
        self.x_label.grid(row=1,column=3, pady=5)
        self.x_entry = tk.Entry(self.frame_entry,textvariable=self.x, width=100)
        self.x_entry.grid(row=1,column=4, pady=5)
        
        self.y = tk.StringVar()
        self.y_label = tk.Label(self.frame_entry, text="y_out: ")
        self.y_label.grid(row=2,column=3, pady=5)
        self.y_entry = tk.Entry(self.frame_entry,textvariable=self.y, width=100)
        self.y_entry.grid(row=2,column=4, pady=5)
        
        self.hc_out = tk.StringVar()
        self.hc_out_label = tk.Label(self.frame_entry, text="hc_out : ")
        self.hc_out_label.grid(row=3,column=3, pady=5)
        self.hc_out_entry = tk.Entry(self.frame_entry,textvariable=self.hc_out, width=100)
        self.hc_out_entry.grid(row=3,column=4, pady=5)
        
        self.loc_out = tk.StringVar()
        self.loc_out_label = tk.Label(self.frame_entry, text="loc_out : ")
        self.loc_out_label.grid(row=4,column=3, pady=5)
        self.loc_out_entry = tk.Entry(self.frame_entry,textvariable=self.loc_out, width=100)
        self.loc_out_entry.grid(row=4,column=4, pady=5)
        
        self.frame_entry.pack(side=tk.LEFT)

        ## Results Frame        
        self.results_frame = tk.Frame(self.main_frame, padx=5, pady=5)


        self.results_frame.pack(side=tk.LEFT)
        ## Outside Main Frame
        self.b1 = tk.Button(master,text="Close", command=self.quit_app)
        self.b1.pack(side=tk.RIGHT, padx=5, pady=5)        
        
        self.b2 = tk.Button(master,text="Write Output to txt File", command=self.write_output)
        self.b2.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.prev_x = 0
        self.prev_y = 0
        
    def quit_app(self):
        self.master.destroy()
        self.master.quit()
    
    def prev_point(self):
        self.start_x.set(self.prev_x)
        self.start_y.set(self.prev_y)
    
    def add_line(self):
        x1 = self.start_x.get()
        x2 = self.end_x.get()
        
        y1 = self.start_y.get()
        y2 = self.end_y.get()
        
        if [x1,y1] == [x2,y2]:
            pass
        else:
            self.prev_x = x2
            
            string_x = self.x.get() + '{0},{1},'.format(x1,x2)
            self.x.set(string_x)
            
            self.prev_y = y2
                  
            hc = self.hc_in.get()
            loc = self.loc.get()        
            string_y = self.y.get() + '{0},{1},'.format(y1,y2)
            self.y.set(string_y)
            string_hc = self.hc_out.get() + '{0},'.format(hc)
            self.hc_out.set(string_hc)
            string_loc = self.loc_out.get() + "'{0}',".format(loc)
            self.loc_out.set(string_loc)
    
    def write_output(self):
        file = open('Line_Helper_output.txt','w')
        
        file.write(self.x.get())
        file.write('\n')
        file.write(self.y.get())
        file.write('\n')
        file.write(self.hc_out.get())
        file.write('\n')
        file.write(self.loc_out.get())
        file.write('\n')
        file.close()

def main(): 
    root = tk.Tk()
    root.title("Wall Line Helper For Drift")
    app = Main_window(root)
    root.minsize(800,600)
    root.mainloop()

if __name__ == '__main__':
    main()