#!/usr/bin/env python3
# https://stackoverflow.com/questions/48414657/load-a-list-of-urls-from-a-csv-file-and-parse-them-one-by-one-for-the-same-data?rq=1
#https://stackoverflow.com/questions/3334809/python-urllib2-how-to-send-cookie-with-urlopen-request
import csv
from urllib.request import build_opener
from bs4 import BeautifulSoup

contents = []
# Add your website here
domain = ""
# Add your key here.  This should be kept secret, protect it like a password!
key = ""

# Open file in read mode
with open('urls.csv', 'r') as csvf:
    ips = csv.reader(csvf)
    for ip in ips:
        url = [f"{domain}/wp-admin/?banhammer-key={key}&banhammer-ip={ip[0]}"]
        url.append(ip[0])
        # Add each url to list contents
        contents.append(url)
        # print(url[0])

total = len(contents)
track = 1
# Parse through each url in the list.
for url in contents:
    try:
        # create an object to formulate our request
        opener = build_opener()
        # Log in on browser and look at the session cookies
        # Add cookies below
        # Looks like 2 may be needed:
        # wordpress_sec* and
        # wordpress_logged_in*
        opener.addheaders.append(('Cookie', ''))
        opener.addheaders.append(('Cookie', ''))
        # opener.addheaders.append(('Cookie', ''))
        # opener.addheaders.append(('Cookie', ''))
        # opener.addheaders.append(('Cookie', ''))
        # Open the url
        page = opener.open(url[0]).read()
        # Scrape the results to report on success of request
        soup = BeautifulSoup(page, "html.parser")
        # Find the div with class notice which contains the results of our
        # request, assuming we're logged in and the url is crafted correctly
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
