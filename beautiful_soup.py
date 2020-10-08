# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 13:44:14 2018

@author: derekolson
"""
#https://nrcs.app.box.com/v/gateway

###############################################################################
import urllib
import urllib.request
from urllib.parse import urlparse

url = "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/1m/Projects/"

with urllib.request.urlopen(url) as response:
    html = response.read()
print(html)

urlparse(url)

R8_states = list('TX', 'OK', 'AR','LA','KY','TN','AL', 'FL', 'GA', 'SC','NC','VA', 'MS')    
###############################################################################    
from bs4 import BeautifulSoup
import requests

r  = requests.get("ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/1m/Projects/")
data = r.text
soup = BeautifulSoup(data)

head = soup.contents[1].contents[0].name




for link in soup.find_all('a'):
    print(link.get('href'))



###############################################################################
import requests
from bs4 import BeautifulSoup as bs
import urllib

_URL = 'https://nrcs.app.box.com/v/gateway'
r = requests.get(_URL)
soup = bs(r.text)
urls = []
names = []
for i, link in enumerate(soup.findAll('a')):
    _FULLURL = _URL + link.get('href')
    print(_FULLURL)
    if _FULLURL.endswith('.pdf'):
        urls.append(_FULLURL)
        names.append(soup.select('a')[i].attrs['href'])

names_urls = zip(names, urls)

for name, url in names_urls:
    print url
    rq = urllib2.Request(url)
    res = urllib2.urlopen(rq)
    pdf = open("pdfs/" + name, 'wb')
    pdf.write(res.read())
    pdf.close()