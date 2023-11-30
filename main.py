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
from abc import ABCMeta, abstractmethod 

#TODO: try to use https://pypi.org/project/transitions/ https://github.com/pytransitions/transitions

class CommentBlockType(enum.Enum):
    GENERAL = 0
    HEADER = 1
    FUNCTION = 2
    UNDEFINED = 3

@dataclass
class CommentDescriptor:
    block_type: CommentBlockType
    is_block_opened: bool
    #is_block_closed: bool

@dataclass
class AlligmentDescriptor:
    star: int
    tag: int
    descr: int


'''
TODO: investigate function prototypes
@abstractmethod 
def doxy_brief_handler():
    pass 

'''


cmnt_descr = CommentDescriptor(
    CommentBlockType.UNDEFINED, False)

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

aligm_descr = AlligmentDescriptor(2, 12, 12)

tags = [DOXY_BRIEF, DOXY_NOTE, DOXY_PARAM, DOXY_RETURN,
        DOXY_RETVAL, DOXY_DETAILS, DOXY_FILE, DOXY_AUTHOR]

'''
/**
 * \brief     Sets number of remote threads.
 * \details   Number of remote threads that can be reserved by \ref nrf_rpc_os_remote_reserve is limited by `count` parameter. After initialization `count` is
 *            assumed to be zero.
 * \param[in] count - Number of remote threads.
 * \return            None.
 
/**
 * \brief     nRF RPC OS-dependent initialization.
 * \param[in] callback - Work callback that will be called when something was send to a thread pool.
 * \return               0 on success or negative error code.
 */
'''

def formatting_3_part_line(line: str) -> str:
    buffer = line.split()
    #print(buffer)
    comment = buffer[2:]
    comment = " ".join(comment)
    print(
        f' {buffer[0]:{aligm_descr.star}}{buffer[1]:{aligm_descr.tag}}{comment:{aligm_descr.descr}}')

    return f' {buffer[0]:{aligm_descr.star}}{buffer[1]:{aligm_descr.tag}}{comment:{aligm_descr.descr}}'

def doxy_brief_handler(line: str) -> str:
    return formatting_3_part_line(line)


def doxy_note_handler(line: str) -> str:
    return formatting_3_part_line(line)


def doxy_param_handler(line: str) -> str:

    return ""


def doxy_return_handler(line: str) -> str:
    return formatting_3_part_line(line)


def doxy_retval_handler(line: str) -> str:

    return ""


def doxy_details_handler(line: str) -> str:
    return formatting_3_part_line(line)


def doxy_file_handler(line: str) -> str:

    return ""


def doxy_author_handler(line: str) -> str:

    return ""


def open_coment_handler(line: str) -> None:

    return None


def close_comment_handler(line: str) -> None:

    return None



handlers = {DOXY_BRIEF: doxy_brief_handler,
            DOXY_NOTE: doxy_note_handler,
            DOXY_PARAM: doxy_param_handler,
            DOXY_RETURN: doxy_return_handler,
            DOXY_RETVAL: doxy_retval_handler,
            DOXY_DETAILS: doxy_details_handler,
            DOXY_FILE: doxy_file_handler,
            DOXY_AUTHOR: doxy_author_handler,
            OPEN_COMMENT: open_coment_handler,
            CLOSE_COMMENT: close_comment_handler}


def line_processing(line: str) -> Optional[str]:
    for tag in tags:
        if line.find(tag.strip()) != -1:
            return tag_processing(tag, line)
    return None


def tag_processing(tag: str, line: str) -> Optional[str]:

    if tag == (CLOSE_COMMENT or DOXY_FILE or DOXY_AUTHOR):
        cmnt_descr.is_block_opened = False
        return None

    if tag == OPEN_COMMENT:
        cmnt_descr.is_block_opened = True
        return None

    return handlers[tag](line)
    if cmnt_descr.is_block_opened == True:
        return handlers[tag](line)
    else:
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

        # TODO lines = [line for line in file]
        for line in file:
            #print(line.strip())
            formatted_line = line_processing(line)
            if formatted_line != None:
                pass
                #file.write(formatted_line)
                #print('DEBUG: NEW LINE:')
                print(formatted_line)

    file.close()

if __name__ == "__main__":
    main()
