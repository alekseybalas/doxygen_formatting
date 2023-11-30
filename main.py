#!/usr/bin/env python3

'''
1. open file
2. scan all strings
3. !!! find doxygen patterns and change strings
4. save file
5. close file



3.1 find /** string part
3.2 detect block type 
if block contains \file tag - it is header (skip block)
else - format strings with tags
3.3 if detected */ - clear block flag
'''

import argparse
from glob import glob
import json
import os
import sys
import zipfile
import struct
import shutil
import enum
from dataclasses import dataclass
from typing import Optional

@dataclass
class CommentDescriptor:
    block_type: str
    is_block_opened: bool
    is_block_closed: bool

    def __init__(self, block_type: str, is_block_opened: bool, is_block_closed: bool = False):
        self.block_type = block_type
        self.is_block_opened = is_block_opened
        self.is_block_closed = is_block_closed

class CommentBlockType(enum.Enum):
    GENERAL = 0
    HEADER = 1
    FUNCTION = 2

DOXY_BRIEF = '* \\brief'
DOXY_NOTE = '* \\note'
DOXY_PARAM = "* \\param"
DOXY_RETURN = '* \\return'
DOXY_RETVAL = '* \\retval'
DOXY_DETAILS = '* \\details'
DOXY_FILE = '* \\file'
DOXY_AUTHOR = '* \\author'
OPEN_COMMENT = '/**'
CLOSE_COMMENT = '*/'

alignment_star = 10
alignment_tag = 10
alignment_description = 10

tags = [DOXY_BRIEF, DOXY_NOTE, DOXY_PARAM, DOXY_RETURN, DOXY_RETVAL, DOXY_DETAILS, DOXY_FILE, DOXY_AUTHOR]

def line_processing(line: str) -> Optional[str]:
    for tag in tags:
        if line.find(tag.strip()) != -1:
            return tag_processing(tag, line)
    return None
            
def tag_processing(tag: str, line: str) -> Optional[str]:
    
    if tag == OPEN_COMMENT:
        return None
    
    if tag == CLOSE_COMMENT:
        return None
    
    if tag == DOXY_PARAM:
        buffer = line.split()
        print(buffer)
        print(f'{buffer[0]:{alignment_star}}{buffer[1]:{alignment_tag}}{buffer[2]:{alignment_description}}')
        return None
    
    if tag == DOXY_RETVAL:
        buffer = line.split()
        print(buffer)
        return None
    

def main():
    print("run main()")

    parser = argparse.ArgumentParser(
        description="Doxygen formatter.")
    parser.add_argument(
        "-s", "--silent", help="Enable silent mode.", action='store_true')
    parser.add_argument("-od", "--output_dir", type=str,
                        default="output", help="Output directory.")
    parser.add_argument("-bt", "--build_type", type=str,
                        default="C", help="Type of the build.")
    parser.add_argument("input_file", type=str,  help="Target source file.")

    args = parser.parse_args()

    with open(args.input_file, "r+") as file:

        #TODO lines = [line for line in file]
        for line in file:
            print(line.strip())
            formatted_line = line_processing(line)
            if formatted_line != None:
                #file.write(formatted_line)
                print('DEBUG: NEW LINE:')
                print(formatted_line)

    file.close()

    file_stats = os.stat(args.input_file)
    #print(type(stats.st_size))
    print(hex(file_stats.st_size))

    new_size = (file_stats.st_size).to_bytes(4, 'little')
    print(hex(new_size[3]))
    print(hex(new_size[2]))
    print(hex(new_size[1]))
    print(hex(new_size[0]))


if __name__ == "__main__":
    main()