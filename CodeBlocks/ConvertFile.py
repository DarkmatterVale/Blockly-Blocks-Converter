import os, sys, re
import argparse
import webbrowser
import Tkinter as tk
import ttk as ttk
import tkMessageBox
import tkFileDialog
import spin_converter as convert

class ConvertFile( tk.Tk ):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # initialize values
        self.new_file = tk.StringVar()
        
        self.title("BlocklyProp Code Converter")
        
        self.initialize()
        self.initialize_menu()

    def initialize(self):
        self.grid()
        
        self.text_input = tk.Text( self, height = 4, width = 5, borderwidth=10 )
        self.text_input.grid(column=0, row=2, stick='nesw', padx=3, pady=10)
        self.text_input.insert(tk.END, 'Add Spin code here', '')
        
        self.lbl_ip_address = ttk.Label(self, anchor=tk.E, text='Tool for converting Spin files into blocks')
        self.lbl_ip_address.grid(column=0, row=0, sticky='nesw', padx=3, pady=10)
        
        self.lbl_file = ttk.Label(self, anchor=tk.E, text='File to create ( name ):')
        self.lbl_file.grid(column=0, row=1, sticky='nesw', padx=3, pady=10)
        
        self.ent_file = ttk.Entry(self, textvariable=self.new_file)
        self.ent_file.grid(column=1, row=1, sticky='nesw', padx=3, pady=10)
        
        self.btn_convert = ttk.Button(self, text='Convert', command=self.convert)
        self.btn_convert.grid(column=0, row=3, sticky='nesw', padx=3, pady=10)
        
        self.grid_columnconfigure(0, minsize=100)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(2, minsize=400)
        self.resizable(True, True)
        self.minsize(500, 500)
        
        self.protocol("WM_DELETE_WINDOW", self.handle_close)
    
    def initialize_menu( self ):
        menubar = tk.Menu( self )
        
        file_menu = tk.Menu( menubar, tearoff=0 )
        file_menu.add_command( label="Add File", command=self.add_file )
        file_menu.add_separator()
        file_menu.add_command( label="Save File", command=self.save_file )
        menubar.add_cascade( label="File", menu=file_menu )
    
        about_menu = tk.Menu( menubar, tearoff=0 )
        about_menu.add_command( label="Checkout Source Code", command=self.handle_browser_sourcecode )
        about_menu.add_separator()
        about_menu.add_command( label="About BlocklyCodeBlocks", command=self.handle_about )
        menubar.add_cascade( label="About", menu=about_menu )
    
        self.config( menu=menubar )
    
    def add_file( self ):
        new_file = open( tkFileDialog.askopenfilename(), 'r' ).read()
    
        self.text_input.insert( tk.END, "\n" + new_file, '' )
    
    def save_file( self ):
        pass
    
    def handle_browser_sourcecode( self ):
        webbrowser.open_new( "http://github.com/DarkmatterVale/BlocklyCodeBlocks" )
    
    def handle_about( self ):
        tkMessageBox.showinfo( "About BlocklyCodeBlocks", "CurrentVersion: v1.1.0\n\nAuthors: Vale Tolpegin\n\nCopyright 2015 Parallax Inc\n\nRelease Notes:\nv1.1.0\n\t-Updated GUI with some menu support\nv1.0.0\n\t-First version of the parser\n\t-First version of the GUI with basic code conversion support" )
    
    def convert( self ):
        converted = convert.compile( self.text_input.get("1.0", tk.END), self.new_file.get() )
        
        if converted:
            tkMessageBox.askokcancel("INFO", "Code successfully converted.\n\nNew file created:\n" + self.new_file.get() )
        else:
            tkMessageBox.askokcancel("ERROR", "File not converted." )

    def handle_close(self):
        if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
            self.quit()


if __name__ == '__main__':
    bp_client = ConvertFile()
    
    bp_client.mainloop()
