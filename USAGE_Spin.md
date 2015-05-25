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