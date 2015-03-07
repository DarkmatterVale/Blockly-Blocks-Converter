#!/usr/bin/python
# Filename: converter.py

#initializing variables
converted_true_false = False
file_name = "null"

#init method
def init( filename ):
    #initializing variables
    global converted_true_false
    global file_name
    
    #set filename to be converted
    file_name = filename

    #set variable that keeps track of whether the file has been converted
    converted_true_false = False

#getter method for bool variable converted_true_false
def get_converted_true_false():
    #initializing variables
    global converted_true_false
    
    #returning bool variable
    return converted_true_false

#getter method for string variable file_name
def get_file_name():
    #initializing variables
    global file_name
    
    #returning string variable
    return file_name

#convert method
def convert():
    pass

#method to remove comments in file
def remove_comments():
    pass