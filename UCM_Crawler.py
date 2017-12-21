# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 18:42:53 2015

@author: gps919873

Call Manager IP Phone Crawler

The idea is to have a command line:

CCM-CRAWLER <IP RANGE>

What will do:

1 - Scan IP Range and check if IP is up
2 - Create a list of UP ips
3 - Extract HTML page of each IP
4 - Check if it is a CCM Phone
5 - Convert HTML page on csv file
6 - Extract relevant data and add to a list
7 - Export a csv with the data of the phones in the range


Version 01 -    Creates raw csv files
Version 02 -    TODO - Transpose CSV files
                TODO - Append the CSV files (adding IP address info)
                TODO - format on Excel friendly way
Version 03 - Python 3.4 - beautiful Soup

"""
from sys import argv
script, ip_range, output_file = argv
from bs4 import BeautifulSoup
import netaddr
#from HTMLParser import HTMLParser
from urllib import request, error
#import sys
#import getopt
#import os.path
#import glob
#import re
import csv

### Fist Parsing of HTML page
def first_pass(url):
    """ This function connects to a given URL and create an HTML
    object from it's page """"
    try:
        page = request.urlopen(url)
        # If an error is found, try to inform why and continue to next IP
        #    except URLError as e:
    except error.URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print( 'Reason: ', e.reason)
                return None
            elif hasattr(e, 'code'):
                print( 'The server couldn\'t fulfill the request.')
                print( 'Error code: ', e.code)
                return None
    except KeyboardInterrupt as ki:
            raise ki
            return None
    except:
        print("unknown error")
        return None
    else:
        return page

def HTML_table(page):
    """ This function gets one HTML object, search for <table>
    selects third table, and return it as a BeautifulSoup object.
    The idea is that such table contains info on Cisco IP phones"""
    if page == None:
        return None
    else:
        bsObj = BeautifulSoup(page,"html.parser")
        my_tables = bsObj.find_all('table')
        if len(my_tables) == 3:
            needed_table = my_tables[2]
            trs = needed_table.find_all('tr')
            return trs
        else:
            trs = None
            return trs
### Parse thru Beautiful Soup and get a list with the info needed

def csv_table(trs):
    """ This function process the table (BeautifulSoup object) and creates
    as list with the information on this table""""

    my_data = []
    new_data = []
    cell = []
    if trs == None:
        my_data = []
    else:
         for tr in trs[:]:
             tds = tr.find_all("td")
 #            cl1 = str(tds[0].get_text())
             cl2 = str(tds[2].get_text())
             my_data.extend([cl2])
#             print(cell)
    return my_data

# Create an object CDIR
subnet = netaddr.IPNetwork(ip_range)[100:120]

semi_final = []

# CreatebsObj = BeautifulSoup(request.urlopen(url)
# loop from all Ips on object, less first and last addresses
for ip in (subnet):
    # Craft filename for singular IP file
    filename = "ip-%s-" % str(ip) + str(output_file) + ".csv"
    #create URL for each IP
    url = "http://%s/CGI/Java/Serviceability?adapter=device.statistics.device" % ip

    #transposed = "ip-%s-trasnposed-" % ip + str(output_file)
    print('scanning',str(ip),'\nURL: ', str(url))
    # Craft url to be contacted for info
    # Try to access URL
    page = first_pass(url)
    trs = HTML_table(page)
    tds = csv_table(trs)
    semi_final.append(tds)
print(semi_final)
with open(output_file, "w",newline='') as f:
    writer = csv.writer(f)
    writer.writerows(semi_final)
