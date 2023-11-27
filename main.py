#!/usr/bin/env python3

'''
1. open file
2. scan all strings
3. find doxygen patterns
4. change strings
5. save file
6. close file
'''

import argparse
from glob import glob
import json
import os
import sys
import zipfile
import struct
import shutil

DOXY_BRIEF = '* \\brief'
DOXY_NOTE = '* \\note'
DOXY_PARAM = "* \\param"
DOXY_RETURN = '* \\return'
DOXY_RESULT = '* \\result'


def find_by_mask(mask: str) -> None:
    iter = glob(mask, recursive=False)
    print(iter)
    for element in iter:
        print(element)
        #os.remove(element)


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

        #lines = [line for line in file]
        for line in file:
            if line.find(DOXY_PARAM.strip()) != -1:
                print(line.strip())
            #   print(type(line.strip()))
            #print(line.strip())
            #print(type(line.strip()))

            #print(str(line))
            #print(str(type(line)))

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