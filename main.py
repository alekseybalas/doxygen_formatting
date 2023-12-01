#!/usr/bin/env python3

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

# TODO: try to use https://pypi.org/project/transitions/ https://github.com/pytransitions/transitions

class CommentBlockType(enum.Enum):
    GENERAL = 0
    HEADER = 1
    FUNCTION = 2
    UNDEFINED = 3


@dataclass
class CommentDescriptor:
    block_type: CommentBlockType
    is_block_opened: bool


    # is_block_closed: bool
'''
@dataclass
class AlligmentDescriptor:
    star: int
    tag: int
    descr: int
    param_name: int
    retval_value: int
    minus: int

aligm_descr = AlligmentDescriptor(2, 12, 12, 12, 12, 2)

    # result = f' {buffer[0]:{aligm_descr.star}}{buffer[1]:{aligm_descr.tag}}{comment:{aligm_descr.descr}}'
    # result = f' {buffer[0]:{aligm_descr.star}}{buffer[1]:{aligm_descr.tag}}{buffer[2]:{aligm_descr.param_name}}{comment:{aligm_descr.descr}}'
    # result = f' {buffer[0]:{aligm_descr.star}}{buffer[1]:{aligm_descr.tag}}{buffer[2]:{aligm_descr.retval_value}}{buffer[3]:{aligm_descr.minus}}{comment:{aligm_descr.descr}}'
'''


@dataclass
class AlligmentDescriptor:
    star: int
    tag: int


@dataclass
class AlligmentDescriptorWithoutName(AlligmentDescriptor):
    descr: int #not used!


@dataclass
class AlligmentDescriptorWithName(AlligmentDescriptor):
    descr: int #not used!
    name_or_value: int
    minus: int


aligm_descr_wo_name = AlligmentDescriptorWithoutName(2, 11, 100)
aligm_descr_w_name = AlligmentDescriptorWithName(2, 11, 9, 9, 2)

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

tags = [DOXY_BRIEF, DOXY_NOTE, DOXY_PARAM, DOXY_RETURN,
        DOXY_RETVAL, DOXY_DETAILS, DOXY_FILE, DOXY_AUTHOR, OPEN_COMMENT, CLOSE_COMMENT]


def formatting_3_part_line(line: str) -> str:
    buffer = line.split()
    comment = buffer[2:]
    comment = " ".join(comment)

    result = f' {buffer[0]:{aligm_descr_wo_name.star}}{buffer[1]:{aligm_descr_wo_name.tag}}{comment:{aligm_descr_wo_name.descr}}'
    print(result)
    return result


def doxy_brief_handler(line: str) -> str:
    return formatting_3_part_line(line)


def doxy_note_handler(line: str) -> str:
    return formatting_3_part_line(line)


def doxy_param_handler(line: str) -> str:
    result = ''
    buffer = line.split()
    if (len(buffer)) > 3:
        if buffer[3] != '-':
            buffer.insert(3, '-')
        comment = buffer[3:]
        comment = " ".join(comment) 
        result = f' {buffer[0]:{aligm_descr_w_name.star}}{buffer[1]:{aligm_descr_w_name.tag}}{buffer[2]:{aligm_descr_w_name.name_or_value}}{comment:{aligm_descr_w_name.descr}}'
        print(result)
    else:
        result = formatting_3_part_line(line)
    
    return result


def doxy_return_handler(line: str) -> str:
    return formatting_3_part_line(line)


def doxy_retval_handler(line: str) -> str:
    buffer = line.split()
    #comment = buffer[4:]
    comment = buffer[3:]
    comment = " ".join(comment)

    #result = f' {buffer[0]:{aligm_descr_w_name.star}}{buffer[1]:{aligm_descr_w_name.tag}}{buffer[2]:{aligm_descr_w_name.name_or_value}}{buffer[3]:{aligm_descr_w_name.minus}}{comment:{aligm_descr_w_name.descr}}'
    result = f' {buffer[0]:{aligm_descr_w_name.star}}{buffer[1]:{aligm_descr_w_name.tag}}{buffer[2]:{aligm_descr_w_name.name_or_value}}{comment:{aligm_descr_w_name.descr}}'
    print(result)
    return result


def doxy_details_handler(line: str) -> str:
    return formatting_3_part_line(line)


def doxy_file_handler(line: str) -> str:
    return line


def doxy_author_handler(line: str) -> str:
    return line


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

    if tag == CLOSE_COMMENT:
        cmnt_descr.is_block_opened = False
        return None

    if tag == DOXY_FILE:
        cmnt_descr.is_block_opened = False
        return None

    if tag == DOXY_AUTHOR:
        cmnt_descr.is_block_opened = False
        return None

    if tag == OPEN_COMMENT:
        cmnt_descr.is_block_opened = True
        return None

    # return handlers[tag](line)
    if cmnt_descr.is_block_opened == True:
        return handlers[tag](line)
    else:
        return None



def change_all_files_by_mask(mask: str) -> None:
    iter = glob(mask, recursive=False)
    print(iter)
    for file_path in iter:
        print(file_path)
        #file_path = file_path[2:]
        print(file_path)
        open_and_format_file(file_path)
        


class Args_temp:
    input_file: str
#args = Args_temp()

def open_and_format_file(file_name : str) -> None:

    with open(file_name, "r") as read_file:
        with open('temp__' + file_name, 'w+') as write_file:
            lines = read_file.readlines()

            for line in lines:
                # print(line.strip())
                formatted_line = line_processing(line)
                if formatted_line != None:
                    write_file.write(formatted_line+"\n")
                else:
                    write_file.write(line)

    os.remove(file_name)
    os.rename('temp__' + file_name, file_name)

def main():
    '''
    parser = argparse.ArgumentParser(
        description="Doxygen formatter.")
    parser.add_argument(
        "-s", "--silent", help="Enable silent mode.", action='store_true')
    parser.add_argument("input_file", type=str,  help="Target source file.")

    args = parser.parse_args()
    '''
    #args.input_file = "app_controller.c"
 
    #change_all_files_by_mask('./**/*.c')
    change_all_files_by_mask('*.c')

if __name__ == "__main__":
    main()

