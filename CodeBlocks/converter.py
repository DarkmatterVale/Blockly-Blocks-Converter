#!/usr/bin/python
# Filename: converter.py


#importing required libraries
import os, sys, re


#initializing variables
firstfunction = ""


def filter_comments(text):
    text = re.sub("{{(.*?)}}","",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub("{(.*?)}","",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub("'.*","",text)
    text = re.sub("(?<=\d)_(?=\d)","",text)                           # remove underscores in numbers
    text = "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])
    text = "\n" + text
    
    return text


def filter_operators(text):
    text = re.sub(":=","=",text)
    text = re.sub("//","%",text)
    text = re.sub("=>",">=",text)
    text = re.sub("=<","<=",text)
    text = re.sub("@","",text)
    
    return text


def function_2_0( text, label ):
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

    block_spin_title = "Blockly.spin." + title + " = function() {\n"
    block_spin_code = '\tvar code = "' + text[1] + '";\n\treturn code;'

    text = block_spin_title + block_spin_code + "\n}"
    
    return text


def function(text, label):
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
    alias = alias.strip()
    
    print title
    print "  ",alias
    print "  ",temps
    
    
    if label == 'PUB':
        global firstfunction
        if firstfunction == None:
            firstfunction = title

    # Fix aliases
    if not alias == "":
        text[1] = re.sub(alias,"result",text[1])
        text[1] = filter_operators(text[1])
    
    # Fix parameters
    if not re.search("\(.*\)", title):
        title += '()'

    # Add parentheses to function calls
    text[1] = re.sub("(\w+\.\w+)(?![.a-zA-Z_\(])","\g<1>()", text[1])


    # eat sub-object hashes
    text[1] = re.sub("(\w+)#(\w+)","\g<1>.\g<2>", text[1])
    
    # handle inc/dec operators
    text[1] = re.sub("(\w+)\+\+","\g<1> += 1", text[1])
    text[1] = re.sub("(\w+)--","\g<1> -= 1", text[1])
    
    text[1] = re.sub("(\w+\[.+?\])\+\+","\g<1> += 1", text[1])
    text[1] = re.sub("(\w+\[.+?\])--","\g<1> -= 1", text[1])
    
    # flow control
    text[1] = re.sub("(\s*)repeat[ \t]*\n","\g<1>while True:\n", text[1])    # repeat
    text[1] = re.sub("(\s*)repeat[ \t]+(\w+)[ \t]+from[ \t]+(.+)[ \t]+to[ \t]+(.+)[ \t]*\n","\g<1>for \g<2> in range(\g<3>, \g<4>):\n", text[1])    # repeat from to
    text[1] = re.sub("(\s*)until[ \t]+(.*)[ \t]*\n","\g<1>    if \g<2>\g<1>        break\n", text[1])   # until
    
    
    text[1] = re.sub("(\s*if.*)[ \t]*","\g<1>:", text[1])     # repeat
    text[1] = re.sub("(\s*else.*)[ \t]*","\g<1>:", text[1])     # repeat
    
    # miscellaneous
    text[1] = re.sub("(\w+)\?","random.getrandbits(32)",text[1])        # random
    text[1] = re.sub("\$([0-9A-Fa-f]+)","int(\"0x\g<1>\",0)",text[1])   # hex
    text[1] = re.sub("string\((.*?)\)","\g<1>",text[1])                 # string
    text[1] = re.sub("\",[ \t]*10[ \t]*,\"","\\\n",text[1])             # newlines
    
    text[1] = re.sub("cnt","0",text[1])
    
    
    indentlevel = len(text[1].split('\n')[0]) - len(text[1].split('\n')[0].lstrip())
    #    print indentlevel, text[1]
    
    # add function header
    header = "def " + title + ":\n"
    for t in temps:
        header += " "*indentlevel + t + " = 0\n"

    text[1] = header + text[1]

    return text[1]

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
    'PRI' : function,
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