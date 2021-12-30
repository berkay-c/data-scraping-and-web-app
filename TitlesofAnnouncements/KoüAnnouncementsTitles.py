#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 13:27:51 2021

@author: berkay
"""

# Tagging the titles in the Announcements section

import requests
from bs4 import BeautifulSoup

r = requests.get("http://bilgisayar.kocaeli.edu.tr/duyurular.php")
soup = BeautifulSoup(r.content,"html.parser")
result=soup.find_all("h4",{"style":"overflow:hidden;text-overflow: ellipsis;white-space: nowrap;"})

for link in result:
    print(link.text)