# CodeBlocks
Spin, C, and Forth program converter that generates blocks for BlocklyProp

CodeBlocks will automatically detect which language you are programming in, and use the appropriate parser.

# Introduction
----------------

CodeBlocks uses Python to convert Spin, C, or Forth files into .js files that contain the blocks inside of Spin file. These converted blocks are usable inside of Blockly.

To build, you will need:
- Python

Once you have installed all the required dependencies, just navigate to this directory in terminal and type 

```
python ConvertFile.py
```

This will open a GUI where you can choose which file you would like to convert. The converted file will then be saved inside of the conversions directory.

# How To Use ( Spin )
----------------

There are a number of items that must be implemented in any Spin code you would like to convert.

## Variables
The variables you would like used need to be specified in the program. When you create a PUB block, like the one below, you must specify that you want test_var_1 and test_var_2 to be declared and be able to be edited by the user.

```
PUB HelloWorld:
    if test_var_1 > test_var_2:
        ---------Whatever else in your code block--------
```

To do this, you must add the VAR_NAME: command inside this PUB block. Below is an example:

```
PUB HelloWorld:
    'VAR_NAME:test_var_1
    'VAR_NAME:test_var_2

    if test_var_1 > test_var_2:
        ---------Whatever else in your code block--------
```

The syntax for this command is: 'VAR_NAME:{ADD YOUR VARIABLE'S NAME HERE}
This will tell the program that you would like this variable to be used and added to the interface ( where users can edit variable values ).

## Variable Categories
Variables will use the standard category of "Blockly-Blocks-Converter". You can edit this though by using the VAR_CATEGORY: command. Below is an example.

```
CON
    long test_con = 10

PUB HelloWorld:
    if test_var_1 > test_var_2:
        ---------Whatever else in your code block--------
```

In this code, the programmer has a constant and 2 variables. This programmer wants to have these variables in the same category as all of the other math variables, and maybe even overwrite some of them. To do this, the programmer adds the VAR_CATEGORY: command right before all of the PUB blocks. Below shows the new code with the VAR_CATEGORY: command used.

```
CON
    long test_con = 10

'VAR_CATEGORY:var_category

PUB HelloWorld:
    if test_var_1 > test_var_2:
        --------Whatever else in your code block--------
```

## Block Names
By default, the name of the PUB statement will be the name of the block when the code is generated. If you would like to change that, you can use the NAME: command. Below is an example.

```
Code to generate block from:
PUB HelloWorld:
    'NAME:my_name
    
    if test_var_1 > test_var_2:
        --------Whatever else in your code block--------

Code generated:
Blockly.Spin.my_name = function() {
    Generated Spin code here
};
```

As you can see, the NAME: command is used to change the name of the block generated. This command is used at the beginning of any PUB block to change that block's name.

## Block Categories
In addition to changing the Block's name, you can change its category. This can be done using the CATEGORY: command at the beginning of the PUB block. Below is an example.

```
Code to generate block from:
PUB HelloWorld:
    'CATEGORY:my_category

    if test_var_1 > test_var_2:
        --------Whatever else in your code block--------

Code generated:
Blockly.Language.HelloWorld = {
    category: 'my_category',
    Generated Spin code here
};
```

The CATEGORY: command's syntax is 'CATEGORY:category_name

# License
----------------

    Copyright (C) 2015 Vale Tolpegin

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

See more in-depth information in the LICENSE file.

# Contributing
----------------

To contribute, simply fork this repository, make your changes/enhancements, and create a PR! Please note though, no changes are ever considered "rock solid". All code submitted can be changed, for any reason.

To submit a bug or feature request, add an issue on this repository's issue tracker.

Thanks for the help!
