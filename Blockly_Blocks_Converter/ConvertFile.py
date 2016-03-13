import os, sys, re
import argparse
import webbrowser
import Tkinter as tk
import ttk as ttk
import tkMessageBox
import tkFileDialog
import spin_converter as spin_convert
from c_converter_class import CConverter


class ConvertFile(tk.Tk):
    """
    A GUI converter for BlocklyProp blocks
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Instantiating converters
        self.cconverter = CConverter()

        # Initialize GUI
        self.new_file = tk.StringVar()
        self.title("Blockly-Blocks-Converter")
        self.initialize()
        self.initialize_menu()

    def initialize(self):
        self.grid()

        self.text_input = tk.Text(self, height = 4, width = 5, borderwidth=10)
        self.text_input.grid(column=0, row=2, stick='nesw', padx=3, pady=10, columnspan=2)
        self.text_input.insert(tk.END, 'Add code here', '')

        self.lbl_ip_address = ttk.Label(self, anchor=tk.E, text='Tool for converting Spin/C code into BlocklyProp blocks')
        self.lbl_ip_address.grid(column=0, row=0, sticky='', padx=3, pady=10, columnspan=2)

        self.lbl_file = ttk.Label(self, anchor=tk.E, text='File to create (name):')
        self.lbl_file.grid(column=0, row=1, sticky='nesw', padx=3, pady=10)

        self.ent_file = ttk.Entry(self, textvariable=self.new_file)
        self.ent_file.grid(column=1, row=1, sticky='nesw', padx=3, pady=10)

        self.btn_convert = ttk.Button(self, text='Convert', command=self.convert)
        self.btn_convert.grid(column=0, row=3, sticky='nesw', padx=3, pady=10, columnspan=2)

        self.grid_columnconfigure(0, minsize=100)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(2, minsize=400)
        self.resizable(True, True)
        self.minsize(500, 500)

        self.protocol("WM_DELETE_WINDOW", self.handle_close)

    def initialize_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Add File", command=self.add_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save File", command=self.save_file)
        menubar.add_cascade(label="File", menu=file_menu)

        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="Checkout source code", command=self.handle_browser_sourcecode)
        about_menu.add_separator()
        about_menu.add_command(label="About Blockly-Blocks-Converter", command=self.handle_about)
        menubar.add_cascade(label="About", menu=about_menu)

        self.config(menu=menubar)

    def add_file(self):
        new_file = open(tkFileDialog.askopenfilename(), 'r').read()

        self.text_input.insert(tk.END, "\n" + new_file, '')

    def save_file(self):
        # @TODO: Implement code-window file saving here
        pass

    def handle_browser_sourcecode(self):
        webbrowser.open_new("http://github.com/DarkmatterVale/Blockly-Blocks-Converter")

    def handle_about(self):
        tkMessageBox.showinfo("About Blockly-Blocks-Converter", "CurrentVersion: v1.1.0\n\nAuthors: Vale Tolpegin\n\nCopyright 2015 Parallax Inc\n")

    def convert(self):
        code = self.text_input.get("1.0", tk.END)

        converted = False
        if "PUB" in code:
            converted = spin_convert.compile(code, self.new_file.get())
        else:
            converted = self.cconverter.compile(code, self.new_file.get())

        if converted:
            tkMessageBox.askokcancel("INFO", "Code successfully converted.\n\nNew file created:\n" + self.new_file.get())
        else:
            tkMessageBox.askokcancel("ERROR", "File not converted.")

    def handle_close(self):
        if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
            self.quit()
