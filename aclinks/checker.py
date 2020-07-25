import re 
import os
import requests
from ping3 import ping


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
            r = requests.head(l[1][2],allow_redirects=False)

            if r.status_code != 200:
                
                # CHECK - If test_https return true, we alert the user that the link is not down and need an update, else add to "down" list 
                if r.status_code == 301 and test_https(l[1][2], __verbose):
                    __verbose and print("At line", l[0] , ":" , l[1][2], ":", "The site just switched for HTTPS.", r.reason, "(", r.status_code, ")")
                    continue # Do not add the link to down list

                # CHECK - Check for redirected url for the user to change to redirected url in md file
                isRedirected, urlString = check_history(r,l,__verbose)
                if isRedirected:
                    __verbose and print("At line", l[0] , ":" , l[1][2], ":", "Url is redirected to:", urlString, r.reason, "(", r.status_code, ")")
                    continue # Do not add the link to down list
            
                if r.status_code == 406:
                    if check_not_acceptable_up(r,l,__verbose):
                        continue


                    
                
                
                # Append the rest 
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


def check_not_acceptable_up(r,link, __verbose):
    
    clean_link = link[1][2].split("://")[-1]
        
    try : # TODO -> USE tldrextract to sanitize url
        p = ping(clean_link)

        if p == False:
            __verbose and print("At line", link[0] , ":" , link[1][2], ":", "The site returned", r.reason, "(", r.status_code, ")", "and is DOWN.")
            return False
        elif p == None:
            __verbose and print("At line", link[0] , ":" , link[1][2], ":", "The site returned", r.reason, "(", r.status_code, ")", "Need to check Manually.")
            return False
        else:
            __verbose and print("At line", link[0] , ":" , link[1][2], ":", "The site returned", r.reason, "(", r.status_code, ")", " but is UP.")
            return True
    except UnicodeError:
        print("URL too long and not formated for ping")
        return False 


def check_history(response,link, __verbose):
    """Check link redirection

    Args: 
        reponse () : Response from request.head()
        link (string) : current link to be processed
        __verbose : amount of verbosity for cli

    Returns:
        (bool,string). Return (True, redirectionURL) if the url is redirected. Else return (False, "")

    """
    try:
        redirect_url = response.headers['Location']
        return (True, redirect_url)
    except KeyError:
        __verbose and print("At line", link[0] , ":" , link[1][2], ":", "No redirection performed")
        return (False, "")

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
