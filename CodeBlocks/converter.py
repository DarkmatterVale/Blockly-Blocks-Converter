#!/usr/bin/python
# Filename: converter.py


#importing required libraries
import os, sys, re


#initializing variables
firstfunction     = ""


#initializing storage variables for final content
final_variables   = ""
final_objects     = ""
final_content     = ""


def filter_comments(text):
    text = re.sub("{{(.*?)}}","",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub("{(.*?)}","",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub("(?<=\d)_(?=\d)","",text)                           # remove underscores in numbers
    text = "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])
    text = "\n" + text
    
    return text


def parse_comments( text ):
    global final_variables
    global final_content
    updated_variables = re.findall( r"'.*", text )
    
    block_category = ""
    block_name = ""

    for var in updated_variables:
        var = re.sub("'", "", var )
            
        if "VAR_NAME:" in var:
            var = re.sub( "VAR_NAME:", "", var )
                
            final_variables += " " + var
            final_content += '\tBlockly.Spin.setups_[ "LameStation_' + var + '" ] = "int ' + var + '";\n'
        if "CATEGORY:" in var:
            var = re.sub( "CATEGORY:", "", var )
            
            block_category = var
        if "NAME:" in var:
            var = re.sub( "NAME:", "", var )
                
            block_name = var

    text = re.sub( "'.*", "", text )

    return text, block_category, block_name


def function_2_0( text, label ):
    #initializing global variables
    global final_variables
    global final_content
    global final_objects
    
    #initializing local variables
    block_category = ""
    block_name     = ""
    
    text = text.split('\n',1)
    prototype = text[0]
    if ':' in prototype:
        if '|' in prototype:
            title = prototype.split('[:|]')[0]
            alias=  prototype.split('[:|]')[1]
            temp =  prototype.split('[:|]')[2]
        else:
            title = prototype.split(':')[0]
            alias = prototype.split(':')[1]
            temp =  ""
    else:
        alias = ""
        if '|' in prototype:
            title = prototype.split('|')[0]
            temp =  prototype.split('|')[1]
        else:
            temp = ""
            title = prototype
    temps = re.findall(r"[\w]+",temp)
    title = title.strip()

    if label == 'PUB':
        global firstfunction
        if firstfunction == None:
            firstfunction = title

    #parsing comments in each block, then removing whatever is left
    text[1], block_category, block_name = parse_comments( text[1] )

    #creating interface code
    interface_spin_title = "Blockly.Language." + title + " = {\n"
    interface_spin_code = "\tcategory: 'LameStation',\n\thelpUrl: '',\n\tinit: function() {\n\t\tthis.appendDummyInput( " + '"" )\n\t\t\t.appendTitle( "' + title + '" );\n'
    final_content_ui = ""

    inputs = final_variables.split()
    for input in inputs:
        temp_code = "\t\tthis.appendValueInput( " + "'" + input + "'" + ' )\n\t\t\t.appendTitle( "get ' + input + '" );\n'

        final_content_ui += temp_code

    interface_spin_code += final_content_ui + "\t\tthis.setPreviousStatement( true, null );\n\t\tthis.setNextStatement( true, null );\n\t}\n};"

    #creating spin code
    block_spin_title = "Blockly.Spin." + title + " = function() {\n"
    final_content_variables = ""

    inputs = final_variables.split()
    for input in inputs:
        final_content_variables += "\tvar " + input + " = Blockly.Spin.valueToCode( this, '" + input + "' );\n"

        text[1] = re.sub( input, '" + ' + input + ' + "', text[1] )

    block_spin_code = '\tvar code = "' + text[1] + '";\n\treturn code;'

    final_content_block = final_content + "\n" + final_objects + "\n" + final_content_variables + "\n" + block_spin_code + "\n};"

    #creating final code for block
    text = interface_spin_title + interface_spin_code + "\n\n" + block_spin_title + final_content_block
    
    return text


def data(text, label):
    return ""


def objects(text, label):
    global final_objects
    
    declarations_ = text.split('\n')
    for declaration in declarations_:
        split_declaration = declaration.split()
        
        if split_declaration:
        
            final_objects += '\tBlockly.Spin.definitions_[ "LameStation_' + split_declaration[0] + '" ] = ' + "'" + declaration + "';\n"
    
    return ""


def constants(text, label):
    text = re.sub("[\t ]*(.*)","\g<1>",text)
    
    text = re.sub("[\t ]*_clkmode(.*)","",text)
    text = re.sub("[\t ]*_xinfreq(.*)","",text)
    return text


def variables(text, label):
    return text


spinblocks = {
    'PUB' : function_2_0,
    'PRI' : function_2_0,
    'DAT' : data,
    'VAR' : variables,
    'CON' : constants,
    'OBJ' : objects,
}


def split_into_blocks(text):
    return filter(None, re.split('(\nPUB)|(\nDAT)|(\nPRI)|(\nVAR)|(\nCON)|(\nOBJ)',text))


def compile( f, new_file_name ):
    f = filter_comments(f)
            
    textblock = split_into_blocks(f)
            
    # Zero out and initialize content variable
    content = {}
    for b in spinblocks.keys():
        content[b] = ""
        
    ## This code assumes that there is code before your main code
    for i in xrange(0,len(textblock)-1,2):
        label = textblock[i].split('\n')[1]
        print label
        if label in spinblocks.keys():
            content[label] += spinblocks[label](textblock[i+1], label)
            content[label] += "\n\n"

    # Final Formatting

    # Assemble pieces into final page for upload
    finalcontent = "\n\n"
    finalcontent += content['OBJ']
    finalcontent += content['CON']
    finalcontent += content['VAR']
    finalcontent += content['PRI']
    finalcontent += content['PUB']
    finalcontent += content['DAT']
            
    # add boiler plate
    template = open('../templates/block_template.py','r').read()
    assembled =  template
    assembled += finalcontent
    assembled += firstfunction
            
    newfilename = os.path.basename( new_file_name )+'.js'
    
    newfile = open(newfilename,'w')
    newfile.write(assembled)
    newfile.close()

    return True