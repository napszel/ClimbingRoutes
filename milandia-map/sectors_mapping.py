#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.parse
import sys

problematic_sectors = {
    "toppas-i" : '"Toppas I$"',
    "flower-tower": 'Flower Tower',
    "trib": 'Tribüne',
    "toppas-ii": 'Toppas II',
    "trango-tower": 'Trango Tower',
    "kleiner-block": 'Kleiner Block',
    "cerro-torre": 'Cerro Torre',
    "grosser-block": 'Grosser Block',
    "tower": '"^tower$"',
    "grotte": '"Grotte$"',
    "grotte-links": 'Grotte, Turm links',
    "grotte-rechts": 'Grotte, Turm rechts'
}

if len(sys.argv) < 2:
    print("usage:")
    print("python sectors_mapping.py gaswerk_map_by_ps.html > gaswerk_map.html")
    print("python sectors_mapping.py milandia_map_by_ps.html > milandia_map.html")
    sys.exit()
    
f = open(sys.argv[1])

soup = BeautifulSoup(f, 'html.parser')

for link in soup.find_all('a'):
    full_href = link.get('href') # ../index.html#boulderraum
    sector = full_href[full_href.find('#')+1:] # boulderraum
    if sector in problematic_sectors:
        new_sector = problematic_sectors[sector] # "boulderraum ii "
        new_sector_escaped = urllib.parse.quote(new_sector.encode("utf-8")) # %22boulderraum%20ii%20%22
        new_href = full_href.replace(sector, new_sector_escaped) # ../index.html#%22boulderraum%20ii%20%22
        link['href'] = new_href

html = soup.prettify("utf-8")
sys.stdout.buffer.write(html)


