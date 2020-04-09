import re 
import os
import requests
from pprint import pprint

file = "../docs/README.md"


def extract_links(file):

    found = []
    pattern = re.compile('\[(.+)\]\(([^ ]+)\)')

    for i, line in enumerate(open(file)):
        for match in re.finditer(pattern, line):
            if match.group(2).startswith("http"): # only select link which start with 'http'
                found.append(
                    (
                        i+1, # line 
                        match
                    )
                )
    return found



def get_down_links(file, links, __verbose):
    """

    Args: 
        links (list) : List of links and their line number
    
    Return:
        list. List of down website 
    
    """
    down = []

    for l in links :
        r = requests.head(l[1][2])
        if r.status_code != 200:
            down.append(l[1][2])
            __verbose and print(l[1][2], ":", r.reason, "(", r.status_code, ")" )
    return down


def remove_down_links(file, line_numbers):
    """In a file, delete the lines at line number in given list"""
    is_skipped = False
    counter = 0
    # Create name of dummy / temporary file
    dummy_file = file + '.bak'
    # Open original file in read only mode and dummy file in write mode
    with open(file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Line by line copy data from original file to dummy file
        for line in read_obj:
            # If current line number exist in list then skip copying that line
            if counter not in line_numbers:
                write_obj.write(line)
            else:
                is_skipped = True
            counter += 1
 
    # If any line is skipped then rename dummy file as original file
    if is_skipped:
        os.remove(file)
        os.rename(dummy_file, file)
    else:
        os.remove(dummy_file)


def get_all_status(file, links, __verbose):

    link_data = []

    for l in links :
        r = requests.head(l[1][2])
        link_data.append(
            (
                l[0],
                l[1][2],
                r.reason
            )
        )
        __verbose and print(l[1][2], ":", r.reason, "(", r.status_code, ")" )

    return link_data


pprint(get_all_status(file, extract_links(file), 1))

