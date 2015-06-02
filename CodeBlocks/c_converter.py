#!/usr/bin/python
# Filename: c_converter.py


#importing required libraries
import os, sys, re


#initializing storage variables for final content
final_variables   = ""
final_content     = ""
variable_category = "Blockly-Blocks-Converter"


def filter_comments(text):
    # Filtering out & parsing global comments
    text = parse_global_comments( text )
    
    # Joining lines to make the final text look nice
    text = "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])
    text = "\n" + text
    
    return text


def parse_global_comments( text ):
    # Get global variables
    global variable_category
    
    # Find all comments
    comments = re.findall( r"//.*", text )
    
    # Looking for set commands the program is parsing for
    for comment in comments:
        comment = re.sub("//", "", comment )
        if "VAR_CATEGORY:" in var:
            comment = re.sub( "VAR_CATEGORY:", "", comment )
            
            variable_category = comment

    return text


def parse_comments( text ):
    # Getting global variables
    global final_variables
    global final_content
    global variable_category
    
    # Finding all of the 1 line comments in the method
    comments = re.findall( r"//.*", text )
    
    # TO DO: implement comment parsing

    text = re.sub( "//.*", "", text )
    text = "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])
    text = "\n" + text

    return text


def function( text, label ):
    #initializing global variables
    global final_variables
    global final_content

    # TO DO: Add function parsing
    
    return text

spinblocks = {
    'void': function,
    'int': function,
}


def split_into_blocks(text):
    # Splitting the methods and variables
    return filter(None, re.split('(\nvoid)|(int)',text))


def compile( text, new_file_name ):
    # Adding new line to text fixing random issue caused by parsing
    text = "\n" + text
    
    # Initializing global variables
    global final_variables
    global final_content
    
    # Reset content variables
    final_objects     = ""
    final_content     = ""
    
    #Filter out useless things in code
    text = filter_comments( text )
    textblock = split_into_blocks( text )
    
    # Zero out and initialize content variable
    content = {}
    for b in spinblocks.keys():
        content[b] = ""

    # If variables in a method, set those variables back up to the method. Otherwise, they are each found as seperate methods ( since int, for example, can be both a method and a variable )
    variables = ""
    for i in xrange( len(textblock) - 1, 0, -2 ):
        if '\n' not in textblock[i - 1]:
            textblock[i - 1] = '\n' + textblock[i - 1]

        label = textblock[i-1].split('\n')[1]
        
        if label in spinblocks.keys():
            if ';' in spinblocks[label](textblock[i], label).split('\n')[0]:
                textblock[i - 2] += label + spinblocks[label](textblock[i], label)
                
                textblock[i] = "\n"
    
    ## This code assumes that there is code before your main code
    for i in xrange(0,len(textblock)-1,2):
        label = textblock[i].split('\n')[1]
        print label
        
        if label in spinblocks.keys() and spinblocks[label](textblock[i+1], label) != '\n':
            content[label] += label + spinblocks[label](textblock[i+1], label)
            content[label] += "\n\n"

    # Assembling final code
    finalcontent = "\n\n"
    finalcontent += content['void']
    finalcontent += content['int']

    # Eventually, this code will be put into a file. At this point in time, the program is just printing the code for debugging purposes
    print finalcontent