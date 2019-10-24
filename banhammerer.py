#!/usr/bin/env python3
# https://stackoverflow.com/questions/48414657/load-a-list-of-urls-from-a-csv-file-and-parse-them-one-by-one-for-the-same-data?rq=1
# https://stackoverflow.com/questions/3334809/python-urllib2-how-to-send-cookie-with-urlopen-request
# https://www.geeksforgeeks.org/python-program-to-validate-an-ip-address/
# https://www.geeksforgeeks.org/print-colors-python-terminal/
import csv
import argparse
import os
import sys
import re
from urllib.request import build_opener
from bs4 import BeautifulSoup


def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))


def __prep_args():
    """Sets up arguments for script.

    In order to clean up the if __name__ block, we pulled out the argument
    definition and placed it in a private funtion.  This may not be the
    approved solution, but I like it.

    Returns:
        argparse.Namespace: The return value.
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--ipfile")
    group.add_argument("-I", "--ip")
    parser.add_argument("-c", "--cookies")
    args = parser.parse_args()
    # print(type(args))
    return args


def prepIPs(infile):
    contents = []
    with open(infile, 'r') as csvf:
        ips = csv.reader(csvf)
        for ip in ips:
            if validateIP(ip[0]):
                url = prepURL(ip)
                # Add each url list to contents list
                contents.append(url)
                # print(url[0])
            else:
                pass
    return contents


def prepIP(ip):
    contents = []
    if validateIP(ip):
        url = prepURL([ip])
        contents.append(url)
    else:
        pass
    return contents


def prepURL(ip):
    # Add your website here
    domain = ""
    # Add your key here.  This should be kept secret,
    # protect it like a password!
    key = ""
    # form proper url as first list item
    url = [f"{domain}/wp-admin/?banhammer-key={key}&banhammer-ip={ip[0]}"]
    # add the ip that that url is blocking as the second list item
    url.append(ip[0])
    # return this url list.  We do this to simplify progress reporting later,
    # instead of parsing the IP back out of the URL
    return url


def validateIP(ip):
    # Regular expression to match valid IPv4 adderesses
    regexip = (r'^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.'
               r'(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.'
               r'(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.'
               r'(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$')
    # Regular expression to match private IP ranges
    regexpvt = (r'^(0?10\.)|'
                r'(192\.168\.)|'
                r'((172)\.(0?1[6-9]|0?2[0-9]|0?3[0-1])\.)|'
                r'(127\.)')
    # Check to see if the address is valid
    if re.search(regexip, ip):
        # prGreen(f"[+] {ip} is a valid IPv4 Address")
        # if re.search(regex4, ip):
        #     prGreen(f"[+] {ip} is a private IP address")
        # Next check to see if it is a private IP
        if re.search(regexpvt, ip):
            # prGreen(f"[+] {ip} is a private IP address")
            return False
        else:
            # prYellow(f"[!] {ip} is a public IP address")
            return True
    else:
        # prRed(f"[-] {ip} is NOT a valid IPv4 Address")
        return False


def hammer(contents):
    total = len(contents)
    track = 1
    # Parse through each url in the list.
    for url in contents:
        try:
            # create an object to formulate our request
            opener = build_opener()
            opener.addheaders.append(('User-Agent', (r'Mozilla/5.0 (Windows '
                                                     r'NT 10.0; Win64; x64; '
                                                     r'rv:69.0) Gecko/20100101'
                                                     r' Firefox/69.0')))
            opener.addheaders.append(('Referrer', 'https://www.google.com/'))
            # Log in on browser and look at the session cookies
            # Add cookies below
            # Looks like 2 may be needed:
            # wordpress_sec* and
            # wordpress_logged_in*
            # EDIT No longer working for unknown reason
            opener.addheaders.append(('Cookie',
                                      (r'wordpress_test_cookie=; '
                                       r'wordpress_logged_in_*=; '
                                       r'wp-settings-time-1=; '
                                       r'wordpress_sec_*=')))
            # Open the url
            page = opener.open(url[0]).read()
            # Scrape the results to report on success of request
            soup = BeautifulSoup(page, "html.parser")
            # Find the div with class notice which contains the results of our
            # request, assuming we're logged in and the url is crafted
            # correctly
            notice = soup.find_all("div", {"class": "notice"})
            # Check the notice to report whether or not we were successful
            if "exists" in str(notice):
                print(f"[-] {track}/{total} {url[1]} already in Tower")
            elif "Target added to Tower" in str(notice):
                print(f"[+] {track}/{total} {url[1]} added to Tower")
            else:
                print(f"[!] {track}/{total} {url[1]} unknown error?")
                print(soup)
            # print('soup')
        except Exception as e:
            print(f"[!] {track}/{total} {e}")
        track += 1
    return 0


if __name__ == "__main__":
    # Set up the arguments, namely the input file
    args = __prep_args()
    if args.ipfile:
        # make sure that infile exists
        if os.path.exists(args.ipfile):
            contents = prepIPs(args.ipfile)
        else:
            sys.exit("No valid input, exiting")
    elif args.ip:
        contents = prepIP(args.ip)
    else:
        sys.exit("no valid input, exiting")
    hammer(contents)
    # for content in contents:
    #     prGreen(content)
