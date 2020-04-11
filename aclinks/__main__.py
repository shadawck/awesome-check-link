#!/usr/bin/env python3
# __main__.py

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

from aclinks import checker
from docopt import docopt 
 

def main():
    arguments = docopt(__doc__, version='aclinks 0.1.5')

    ########## CLI VAR ##########

    __verbose = arguments["--verbose"]
    __down = arguments["--down"]
    __exit = arguments["--exit"]

    __file = arguments["FILE"]
    __file_ext = __file.split(".")[-1]

    if __file_ext != "md":
        print("aclinks take only md file ! ")
        exit()

    links = checker.extract_links(__file)
    
    if __down:
        checker.get_down_links(__file, links,__verbose, __exit)        
    
    else : 
        checker.get_all_status(__file, links,__verbose, __exit)


if __name__ == "__main__":
    main()

    