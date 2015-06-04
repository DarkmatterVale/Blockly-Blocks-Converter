#!/usr/bin/python
# Filename: c_converter.py


#importing required libraries
import os, sys, re


#initializing storage variables for final content
final_variables   = ""
final_includes    = ""
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
    global final_includes
    global final_content

    # Getting all of the lines of code in the method
    lines = text.split( '\n' )
    
    # Getting title of the block
    unaltered_title = lines[0].split( " " )[1]
    unaltered_title = unaltered_title[ 0 : re.search( r'\(', unaltered_title ).start() ]
    
    block_title = unaltered_title

    for line in lines:
        words = line.split( ' ' )
        
        if len( words ) > 1:
            for key in spinblocks.keys():
                variable = re.sub( ";", "", words[1] )
            
                if key in words[0] and variable not in final_variables:
                    # Find variables and replace them with correct variable values
                   text = re.sub( variable, '" + ' + variable + ' + "', text )

                    # Adding the variable to the list of variables needed to be added into the
                   final_variables += "... " + key + " " + variable

    # Creating variables
    variables       = final_variables.split( "..." )
    includes        = final_includes.split( "..." )
    block_variables = ""
    block_includes  = ""
    
    for variable in variables:
        if variable == '':
            continue
        
        block_variables += '\tBlockly.propc.setups_[ "' + variable.split( ' ' )[1] + '" ] = "' + variable + ';";\n'
    
    for include in includes:
        if include == '':
            continue
        
        include_name = include.split( ' ' )[1]
        
        if '<' in include_name:
            include_name = re.sub( r'\<', '', include_name )
            include_name = re.sub( r'\>', '', include_name )
        elif '"' in include_name:
            include_name = re.sub( r'\"', '', include_name )

        block_includes += '\tBlockly.propc.definitions_[ "' + include_name + '" ] = "' + include + '";\n'

    # Resetting global variables that are now obsolete
    final_variables = ""
    
    print "..."
    print block_variables
    print "..."
    print block_includes
    print "..."

    return text


def filter_global( text ):
    # Getting global variables
    global final_variables
    global final_includes

    # Parse include statements and generate final includes
    text = text.split( '\n' )

    for index in xrange( 0, len( text ) - 1, 1 ):
        words = text[ index ].split( " " )
        
        if '#' in text[ index ] and words[0] not in spinblocks.keys() and 'null' not in words[0]:
            final_includes += "..." + text[ index ]
            
            text[ index ] = "\n"
        elif words[0] in spinblocks.keys() or 'null' in words[0]:
            if '(' in text[ index ] and ')' in text[ index ] and ';' not in text[index]:
                text = "\n".join([ll.rstrip() for ll in text if ll.strip()])
                text = "\n" + text
        
                return text
            elif '(' not in text[ index ] and ')' not in text[ index ] and ';' in text[ index ]:
                final_variables += "..." + words[0] + " " + re.sub( ";", "", words[1] )

                text[ index ] = "\n"
            elif '(' in text[ index ] and ')' in text[ index ] and ';' in text[index]:
                text[ index ] = "\n"
    
    text = "\n".join([ll.rstrip() for ll in text if ll.strip()])
    text = "\n" + text

    return text

spinblocks = {
    'void': function,
    'int': function,
    'char': function,
}


def split_into_blocks(text):
    # Splitting the methods and variables
    return filter(None, re.split('(\nvoid)|(int)|(char)',text))


def compile( text, new_file_name ):
    # Adding new line to text fixing random issue caused by parsing
    text = "\n" + text
    
    # Initializing global variables
    global final_variables
    global final_includes
    global final_content
    
    # Reset content variables
    final_variables = ""
    final_includes  = ""
    final_content   = ""
    
    #Filter out useless things in code
    text = filter_comments( text )
    text = filter_global( text )
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
            if ';' in textblock[i].split('\n')[0]:
                textblock[i - 2] += label + textblock[i]
                
                textblock[i - 1] = "\nnull"
            
            try:
                if '(' in textblock[i - 2].split('\n')[0] and not ')' in textblock[i - 2].split('\n')[0]:
                    textblock[i - 2] += label + textblock[i]
                
                    textblock[i - 1] = "\nnull"
                elif ',' in textblock[i - 2].split('\n')[0].split( " " )[1]:
                    textblock[i - 2] += label + textblock[i]
                
                    textblock[i - 1] = "\nnull"
            except:
                pass

    ## This code assumes that there is code before your main code
    for i in xrange(0,len(textblock)-1,2):
        label = textblock[i].split('\n')[1]
        print label
        
        if label in spinblocks.keys():
            content[label] += label + spinblocks[label](textblock[i+1], label)
            content[label] += "\n\n"

    # Assembling final code
    finalcontent = "\n\n"
    finalcontent += content['void']
    finalcontent += content['int']
    finalcontent += content['char']

    # Eventually, this code will be put into a file. At this point in time, the program is just printing the code for debugging purposes
    print finalcontent