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
    text = parse_comments( text )
    text = "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])
    text = "\n" + text
    
    return text


def parse_comments( text ):
    global final_variables
    global final_content
    updated_variables = re.findall( r"'.*", text )

    for var in updated_variables:
        var = re.sub("'", "", var )
        var = var.split()
        
        for var_component in var:
            if "VAR_NAME:" in var_component:
                temp_var = re.sub( "VAR_NAME:", "", var_component )
                
                final_variables += " " + temp_var
                final_content += '\tBlockly.spin.setups_[ "LameStation_' + temp_var + '" ] = "int ' + temp_var + '";\n'

    text = re.sub( "'.*", "", text )

    return text


def function_2_0( text, label ):
    global final_variables
    global final_content
    
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

    #creating interface code
    interface_spin_title = "Blockly.Language." + title + " = {\n"
    interface_spin_code = "\tcategory: 'LameStation',\n\thelpUrl: '',\n\tinit: function() {\n"
    final_content_ui = ""

    inputs = final_variables.split()
    for input in inputs:
        temp_code = "\t\tthis.appendValueInput( " + "'" + input + "'" + ' )\n\t\t\t.appendTitle( "get ' + input + '" );\n'

        final_content_ui += temp_code

    interface_spin_code += final_content_ui + "\t\tthis.setPreviousStatement( true, null );\n\t\tthis.setNextStatement( true, null );\n\t}\n}"

    #creating spin code
    block_spin_title = "Blockly.spin." + title + " = function() {\n"
    final_content_variables = ""

    inputs = final_variables.split()
    for input in inputs:
        final_content_variables += "\tvar " + input + " = Blockly.Spin.valueToCode( this, '" + input + "' );\n"

        text[1] = re.sub( input, '" + ' + input + ' + "', text[1] )

    block_spin_code = '\tvar code = "' + text[1] + '";\n\treturn code;'

    final_content_block = final_content + "\n" + final_content_variables + "\n" + block_spin_code + "\n};"

    #creating final code for block
    text = interface_spin_title + interface_spin_code + "\n\n" + block_spin_title + final_content_block
    
    return text


def data(text, label):
    return ""


def variables(text, label):
    pat = re.compile('\n[\t ]*(byte|word|long)[ \t]+(\w+)\[(.+?)\].*')
    text = re.sub(pat,"\n\g<2> = [0]*\g<3>",text)
    pat = re.compile('\n[\t ]*(byte|word|long)[ \t]+(\w+).*')
    text = re.sub(pat,"\n\g<2> = None",text)
    
    return text


def constants(text, label):
    text = re.sub("[\t ]*(.*)","\g<1>",text)
    
    text = re.sub("[\t ]*_clkmode(.*)","",text)
    text = re.sub("[\t ]*_xinfreq(.*)","",text)
    return text


def objects(text, label):
    text = re.sub("\n[\t ]*(.*)[\t ]*:[ \t]*\"(.+?)\"","\nimport \g<2> as \g<1>",text)
    text = re.sub("/",".",text)
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