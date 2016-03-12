import os
import re
import sys


class CConverter():
    """
    Convert C-code into BlocklyProp blocks
    """

    def __init__(self):
        # Initialize final component variables
        self.final_variables = ""
        self.final_includes = ""
        self.final_content = ""
        self.variable_category = "Blockly-Blocks-Converter"
        self.blocks = {
            'void': self.function,
            'int': self.function,
            'char': self.function,
        }

    def filter_comments(self, text):
        """
        Filters comments out of the code "text" and returns the remainder.
        """
        # Filtering out comments located outside of methods
        text = self.filter_global_comments(text)

        # Joining lines to make the final text look nice
        text = "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])
        text = "\n" + text

        return text

    def filter_global_comments(self, text):
        # Find all comments
        comments = re.findall( r"//.*", text )

        # Looking for set commands the program is parsing for
        for comment in comments:
            comment = re.sub("//", "", comment)

            # If the user is specifying the category of the block
            if "VAR_CATEGORY:" in comment:
                comment = re.sub( "VAR_CATEGORY:", "", comment )

                self.variable_category = comment

        return text

    def filter_global(self, text):
        # Parse include statements and generate final includes
        text = text.split( '\n' )

        for index in xrange( 0, len( text ) - 1, 1 ):
            words = text[ index ].split( " " )

            if '#' in text[ index ] and words[0] not in self.blocks.keys() and 'null' not in words[0]:
                self.final_includes += "... " + text[ index ]

                text[ index ] = "\n"
            elif words[0] in self.blocks.keys() or 'null' in words[0]:
                if '(' in text[ index ] and ')' in text[ index ] and ';' not in text[index]:
                    text = "\n".join([ll.rstrip() for ll in text if ll.strip()])
                    text = "\n" + text

                    return text
                elif '(' not in text[ index ] and ')' not in text[ index ] and ';' in text[ index ]:
                    if words[1] == "*":
                        if '[' not in words[2]:
                            self.final_variables += "..." + words[0] + " * " + re.sub( ";", "", words[2] )
                    elif '[' not in words[1]:
                        self.final_variables += "..." + words[0] + " " + re.sub( ";", "", words[1] )

                    text[ index ] = "\n"
                elif '(' in text[ index ] and ')' in text[ index ] and ';' in text[index]:
                    text[ index ] = "\n"

        text = "\n".join([ll.rstrip() for ll in text if ll.strip()])
        text = "\n" + text

        return text

    def function(self, text, label):
        # Getting all of the lines of code in the method
        lines = text.split( '\n' )

        # Getting title of the block
        unaltered_title = lines[0].split( " " )[1]
        unaltered_title = unaltered_title[ 0 : re.search( r'\(', unaltered_title ).start() ]

        block_title = unaltered_title

        words = lines[0].split( ' ' )
        for index in range( 0, len( words ) - 1 ):
            for key in spinblocks.keys():
                if key in words[ index ]:
                    if words[ index + 1 ] == "*":
                        if '[' in words[ index + 2 ]:
                            continue

                        variable = words[ index + 1 ]
                    else:
                        if '[' in words[ index + 1 ]:
                            continue

                        variable = words[ index + 2 ]

                    if ',' in variable:
                        variable = re.sub( ',', '', variable )

                    if words[ index + 1 ] == "*":
                        self.final_variables += "..." + key + " * " + variable
                    else:
                        self.final_variables += "..." + key + " " + variable

        methods = ""
        for line in lines:
            words = line.split( ' ' )

            if len( words ) > 1:
                for key in spinblocks.keys():
                    if words[1] == "*":
                        variable = re.sub( ";", "", words[2] )
                    else:
                        variable = re.sub( ";", "", words[1] )

                    if key in words[0] and variable not in self.final_variables:
                        # Adding the variable to the list of variables needed to be added into the
                        if words[1] == "*":
                            if '[' not in words[ 2 ]:
                                self.final_variables += "... " + key + " * " + variable
                        else:
                            if '[' not in words[ 1 ]:
                                self.final_variables += "... " + key + " " + variable

                if '(' in line and ')' in line and ';' in line:
                    for word in words:
                        if '(' in word:
                            method_name = re.sub( '(', '', word )

                            if method_name in methods:
                                pass
                            else:
                                methods += ',' + block_tile + ' ' + method_name

        # Creating variables
        variables               = self.final_variables.split( "..." )
        includes                = self.final_includes.split( "..." )
        block_variables         = ""
        block_includes          = ""
        final_content_ui        = ""
        final_content_variables = ""
        block_category          = "BlocklyConverter"

        for variable in variables:
            if variable == '':
                continue

            words = variable.split( ' ' )

            if words[1] == "*":
                block_variables += '\tBlockly.propc.setups_[ "' + variable.split( ' ' )[2] + '" ] = "' + variable + ';";\n'

                temp_code = "\t\tthis.appendValueInput( " + "'" + variable.split( ' ' )[2] + "'" + ' )\n\t\t\t.appendTitle( "get ' + variable.split( ' ' )[2] + '" );\n'

                final_content_ui += temp_code

                final_content_variables += "\tvar " + variable.split( ' ' )[2] + " = Blockly.propc.valueToCode( this, '" + variable.split( ' ' )[2] + "' );\n"
            else:
                block_variables += '\tBlockly.propc.setups_[ "' + variable.split( ' ' )[1] + '" ] = "' + variable + ';";\n'

                temp_code = "\t\tthis.appendValueInput( " + "'" + variable.split( ' ' )[1] + "'" + ' )\n\t\t\t.appendTitle( "get ' + variable.split( ' ' )[1] + '" );\n'

                final_content_ui += temp_code

                final_content_variables += "\tvar " + variable.split( ' ' )[1] + " = Blockly.propc.valueToCode( this, '" + variable.split( ' ' )[1] + "' );\n"

        for include in includes:
            if include == '':
                continue

            include_name = include.split( ' ' )[2]

            if '<' in include_name:
                include_name = re.sub( r'\<', '', include_name )
                include_name = re.sub( r'\>', '', include_name )
            elif '"' in include_name:
                include_name = re.sub( r'\"', '', include_name )

            block_includes += '\tBlockly.propc.definitions_[ "' + include_name + '" ] = "' + include + '";\n'

        interface_title = "\nBlockly.Language." + block_title + " = {\n"
        interface_code = "\tcategory: '" + block_category + "',\n\thelpUrl: '',\n\tinit: function() {\n\t\tthis.appendDummyInput( " + '"" )\n\t\t\t.appendTitle( "' + block_title + '" );\n'
        interface_code += final_content_ui + "\t\tthis.setPreviousStatement( true, null );\n\t\tthis.setNextStatement( true, null );\n\t}\n};"

        block_code_title = "Blockly.propc." + block_title + " = function() {\n"
        block_code = '\tvar code = "' + label + text + '";\n\treturn code;'


        final_content_block = final_content_variables + "\n" + block_includes + "\n" + block_variables + "\n" + block_code + "\n};"
        text = interface_title + interface_code + "\n\n" + block_code_title + final_content_block

        return text

    def split_into_blocks(self, text):
        """
        Splitting the methods and variables
        """
        return filter(None, re.split('(\nvoid)|(\nint)|(\nchar)|(int)|(char)',text))

    def compile(self, text, new_file_name):
        """
        Converts the C code into a BlocklyProp block
        """
        # Adding new line to text fixing random issue claused by parsing
        text = "\n" + text

        # Reset content variables
        self.final_variables = ""
        self.final_includes  = ""
        self.final_content   = ""
        self.variable_category = "Blockly-Blocks-Converter"

        # Filter out useless things in code
        text = self.filter_comments(text)
        text = self.filter_global(text)
        code_blocks = self.split_into_blocks(text)

        # Zero out and initialize content variable
        content = {}
        for b in self.blocks.keys():
            content[b] = ""

        # If variables in a method, set those variables back up to the method.
        #   Otherwise, they are each found as seperate methods (since int, for
        #   example, can be both a method and a variable).
        variables = ""
        for i in xrange( len(code_blocks) - 1, 0, -2 ):
            if '\n' not in code_blocks[i - 1]:
                code_blocks[i - 1] = '\n' + code_blocks[i - 1]

            label = code_blocks[i-1].split('\n')[1]

            if label in self.blocks.keys():
                if ';' in code_blocks[i].split('\n')[0]:
                    code_blocks[i - 2] += label + code_blocks[i]

                    code_blocks[i - 1] = "\nnull"

                try:
                    if '(' in code_blocks[i - 2].split('\n')[0] and not ')' in code_blocks[i - 2].split('\n')[0]:
                        code_blocks[i - 2] += label + code_blocks[i]

                        code_blocks[i - 1] = "\nnull"
                    elif ',' in code_blocks[i - 2].split('\n')[0].split( " " )[1]:
                        code_blocks[i - 2] += label + code_blocks[i]

                        code_blocks[i - 1] = "\nnull"
                except:
                    pass

        # This code assumes that there is code before your main code
        for i in xrange(0,len(code_blocks)-1,2):
            label = code_blocks[i].split('\n')[1]

            if label in self.blocks.keys():
                content[label] += self.blocks[label](code_blocks[i+1], label)
                content[label] += "\n\n"

        # Assembling final code
        finalcontent = "\n\n"
        finalcontent += content['void']
        finalcontent += content['int']
        finalcontent += content['char']

        # Getting the template and assembling the content
        template = open('../templates/block_template_c.py','r').read()
        assembled =  template
        assembled += finalcontent

        # Saving the new content
        newfilename = os.path.join("../conversions", str(os.path.basename(new_file_name) + '.js'))
        newfile = open(newfilename,'w')
        newfile.write(assembled)
        newfile.close()

        return True
