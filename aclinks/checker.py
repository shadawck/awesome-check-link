import re 
import os
import requests


def extract_links(file):
    """Extract all links in the md file
    Args:
        file (str) : The file to scan 
    Return:
        list. List of all extracted links and their line number. 
        Data Strucure : 
            [(line_0, matchObject_0) , ... , (line_n, matchObject_n)]
        
        For matchOject look at python regex documentation : https://docs.python.org/fr/3.6/library/re.html#re.regex.search

    """

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

def get_down_links(file, links, __verbose, __exit):
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
            down.append(
                (
                    l[0],
                    l[1][2]
                )
            )
            __verbose and print("At line", l[0] , ":" , l[1][2], ":", r.reason, "(", r.status_code, ")")
            if __exit:
                r.raise_for_status()
    return down


# For next version
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


def get_all_status(file, links, __verbose, __exit):
    """Get status for all links of the md file 
    Args:
        file (str) : The file to scan.
        links (list) : List of links to check for status.
        __verbose : Add more to output 
    
    Return: 
        list. list of line number, links, and status.
        Data Strucure : 
            [(line_0, link_0, status_0) , ... , (line_n, link_n, status_n)]
        

    """
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
        __verbose and print("At line", l[0], ":", l[1][2], ":", r.reason, "(", r.status_code, ")" )
        if __exit:
            r.raise_for_status()
    return link_data

