# CodeBlocks
Spin, C, and Forth program converter that generates blocks for BlocklyProp

CodeBlocks will automatically detect which language you are programming in, and use the appropriate parser.

NOTE: This is still in development. If you would like the most-recent stable release, please see the releases page.

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

# How To Use Blockly Code Converter
----------------

To use the converter, see the following files.

- USAGE_Spin.md if you are trying to convert Spin files to blocks
- USAGE_C.md if you are trying to convert C file to blocks
- USAGE_Forth.md if you are trying to convert Forth files to blocks

Each of these files have unique requirements for the specific language.

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
