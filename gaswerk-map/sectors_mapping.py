#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.parse
import sys

problematic_sectors = {
    "boulderraum" : '"Boulderraum II "',
    "3d-wand-indoors" : '3D-Wand indoors',
    "gelbe-wand" : 'Gelbe Wand',
    "toppas-rechts" : 'Toppas rechts',
    "reality-wall" : 'Reality Wall',
    "halle-1-galerie-2" : 'Halle 1 Galerie 2',
    "toppas-links" : 'Toppas links',
    "toprope-wand" : 'Toprope-Wand',
    "geneigte-platte" : 'Geneigte Platte',
    "boulderraum-iii" : 'Boulderraum III',
    "halle-1-turm": 'Halle 1 Turm',
    "halle-2-ngerwand": 'Halle 2 Anfängerwand',
    "halle-2-galerie-3": 'Halle 2 Galerie 3',
    "halle-1-galerie-1": '"Halle 1  Galerie 1"',
    "halle-3-kinderwand": 'Halle 3 Kinderwand',
    "outdoor-arco-wand": 'Outdoor Arco-Wand',
    "outdoor-3d-wand": 'Outdoor 3D-Wand',
    "new-age": 'Outdoor New Age',
    "halle-5": 'Halle 5',
    "dachliland": 'Dächliland',
    "schnaggli": 'Schnäggli',
    "affenkafig": 'Affenkäfig',
    "wilde13": 'Wilde 13',
    "das-dach": 'Das Dach',
    "die-platte": 'Die Platte',
    "base-camp": 'Base Camp',
    "red-carpet": 'Red Carpet',
    "break-point": 'Break Point',
    "fight-club": 'Fight Cub'
}

if len(sys.argv) < 2:
    print("usage:")
    print("python sectors_mapping.py gaswerk_map_by_ps.html > gaswerk_map.html")
    print("python sectors_mapping.py milandia_map_by_ps.html > milandia_map.html")
    sys.exit()
    
f = open(sys.argv[1])

soup = BeautifulSoup(f, 'html.parser')

for link in soup.find_all('a'):
    full_href = link.get('href') # ../generated/index.html#boulderraum
    sector = full_href[full_href.find('#')+1:] # boulderraum
    if sector in problematic_sectors:
        new_sector = problematic_sectors[sector] # "boulderraum ii "
        new_sector_escaped = urllib.parse.quote(new_sector.encode("utf-8")) # %22boulderraum%20ii%20%22
        new_href = full_href.replace(sector, new_sector_escaped)
        link['href'] = new_href

html = soup.prettify("utf-8")
sys.stdout.buffer.write(html)


