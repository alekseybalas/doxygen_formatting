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
    max_tag_len: int
    max_variable_len: int
    block_len: int

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

comment_descr = CommentDescriptor(
    CommentBlockType.UNDEFINED, False, 0, 0, 0)

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


def brief_handler(line: str) -> str:
    return line
def note_handler(line: str) -> str:
    return line
def param_handler(line: str) -> str:
    return line
def return_handler(line: str) -> str:
    return line
def retval_handler(line: str) -> str:
    return line
def details_handler(line: str) -> str:
    return line
def file_handler(line: str) -> str:
    return line
def author_handler(line: str) -> str:
    return line
def coment_handler(line: str) -> str:
    return line



handlers2 = {DOXY_BRIEF: brief_handler,
            DOXY_NOTE: note_handler,
            DOXY_PARAM: param_handler,
            DOXY_RETURN: return_handler,
            DOXY_RETVAL: retval_handler,
            DOXY_DETAILS: details_handler,
            DOXY_FILE: file_handler,
            DOXY_AUTHOR: author_handler,
            OPEN_COMMENT: coment_handler,
            CLOSE_COMMENT: comment_handler}


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


def change_all_files_by_mask(mask: str) -> None:
    iter = glob(mask, recursive=False)
    print(iter)
    for file_path in iter:
        print(file_path)
        #file_path = file_path[2:]
        print(file_path)
        open_and_format_file(file_path)

class BlockState(enum.Enum):
    READY = 0
    NOT_READY = 1
    FAILURE = 2
    UNDEFINED = 3

@dataclass
class FormattedBlock():
    block_state: BlockState
    data: list[str]

raw_block: list[str]
raw_block = []

def reformat_block(line: str) -> Optional[FormattedBlock]:
    for line in raw_block:
         for tag in tags:
            handlers2[tag](line)
    raw_block.clear()
    FormattedBlock(BlockState.READY, [])

def init_block(line: str) -> Optional[FormattedBlock]:
    comment_descr.block_len = 1
    comment_descr.block_type = CommentBlockType.UNDEFINED
    comment_descr.is_block_opened = True
    comment_descr.max_tag_len = 0
    comment_descr.max_variable_len = 0
    return FormattedBlock(BlockState.NOT_READY, [])

def block_processing(line: str) -> Optional[FormattedBlock]:
    for tag in tags:
        if line.find(tag) != -1:
            if (tag != OPEN_COMMENT) and (comment_descr.is_block_opened == False):
                return None
            if (tag == OPEN_COMMENT) and (comment_descr.is_block_opened == True):
                return FormattedBlock(BlockState.FAILURE, [])
            #if (tag == OPEN_COMMENT) and (comment_descr.is_block_opened == False):
                #open desc
            #if (tag != OPEN_COMMENT) and (comment_descr.is_block_opened == True):
                #processing
            
            raw_block.append(line)

            if tag == CLOSE_COMMENT:
                #now it needs to return block
                return reformat_block(line)

            if tag == OPEN_COMMENT:
                comment_descr.is_block_opened = True
                #now it needs to reinit block
                return init_block(line)

            if comment_descr.is_block_opened == True:
                handlers[tag](line)
                return FormattedBlock(BlockState.NOT_READY, [])
                
            #else:
                #return None
    if comment_descr.is_block_opened == True:
        raw_block.append(line)        
    else:
        return None   

def open_and_format_file(file_name : str) -> None:

    with open(file_name, "r") as read_file:
        with open('temp__' + file_name, 'w+') as write_file:
            lines = read_file.readlines()

            for line in lines:
                # print(line.strip())
                formatted_block = block_processing(line)
                if formatted_block != None:
                    if formatted_block.block_state == BlockState.NOT_READY:
                        continue
                    if formatted_block.block_state == BlockState.READY:
                        for line in formatted_block.data:
                            write_file.write(line+"\n")
                        continue
                    if formatted_block.block_state == BlockState.FAILURE:
                        print("PARSING ERROR")
                        exit()
                    if formatted_block.block_state == BlockState.UNDEFINED:
                        print("STUB")
                        continue
                else:
                    write_file.write(line)

    #os.remove(file_name)
    #os.rename('temp__' + file_name, file_name)

class Args_temp:
    input_file: str
#args = Args_temp()

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

