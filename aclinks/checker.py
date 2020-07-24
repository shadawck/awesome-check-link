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
        try:
            r = requests.head(l[1][2],allow_redirects=True)
            if r.status_code != 200:
                # If test_https return true, we alert the user that the link is not down and need an update, else add to "down" list 
                if r.status_code == 301 and test_https(l[1][2], __verbose):
                    __verbose and print("At line", l[0] , ":" , l[1][2], ":", "The site just switched for HTTPS.")
                    continue # Do not add the link to down list

                down.append(
                    (
                        l[0],
                        l[1][2]
                    )
                )
                __verbose and print("At line", l[0] , ":" , l[1][2], ":", r.reason, "(", r.status_code, ")")
                if __exit:
                    r.raise_for_status()
        except requests.exceptions.ConnectionError:
            print("At line", l[0], ":", "Connection to :", l[1][2], "reach Timeout.", "Request Timeout ( 408 )")
            down.append(
                    (
                        l[0],
                        l[1][2]
                    )
            )
        except requests.exceptions.InvalidSchema:
            print("At line", l[0], ":", "There is a misspelling in the url:", l[1][2])

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

def test_https(link, __verbose):
    """
    If you get a 301 header and the url is a HTTP one, the possibility is that the url moved to HTTPS.
    so we need to check for https. If the updated link with https send a 200 it's ok, we can keep the url and replace with update url

    Args: 
        link (string): The url which return a "Moved Permanently ( 301 )"

    Return:
        bool. Return True if the updated HTTPS link return a 200. Else return False.
    """

    split = link.split(":") 
    # Useless to continue if the link is already in HTTPS
    if split[0] == "https": 
        return False
    
    updated_link = "https:" + split[-1]
    r = requests.head(updated_link)
    if r.status_code != 200:
        return False
    
    return True

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
        try:
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
        except requests.exceptions.ConnectionError:
            print("At line", l[0], ":", "Connection to :", l[1][2], "reach Timeout.", "Request Timeout ( 408 )")
            link_data.append(
                (
                    l[0],
                    l[1][2],
                    408      # 408 Request Timeout
                )
            )
    return link_data
