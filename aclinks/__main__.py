#!/usr/bin/env python3

"""Awesome Check Links 

Usage:  
    aclinks [--verbose --exit --down] -f FILE
    aclinks (-h | --help | --version)

Options:
    -f --file       Markdown file to scan.
    -e --exit       Stop your build pipeline if a site is down
    -d --down       Show only down links and their line number.
    -v --verbose    Verbose mode. Print more to stdout.
    -h --help       Show this help.
    --version       Show version.

"""

from aclinks import aclinks as acl
from pprint import pprint
from docopt import docopt 
 

if __name__ == "__main__":
    arguments = docopt(__doc__, version='Awesome check links')

    ########## CLI VAR ##########

    __verbose = arguments["--verbose"]
    __down = arguments["--down"]
    __exit = arguments["--exit"]

    __file = arguments["FILE"]
    __file_ext = __file.split(".")[-1]

    if __file_ext != "md":
        print("aclinks take only md file ! ")
        exit()

    links = acl.extract_links(__file)
    

    if __down:
        down_links = acl.get_down_links(__file, links,__verbose, __exit)        
    
    else : 
        acl.get_all_status(__file, links,__verbose, __exit)


    