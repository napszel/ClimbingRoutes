#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from pprint import pprint
import sqlite3
import sys


def get_unique_colors(color_codes):
  unique_colors = []
  color_with_class = color_codes.split(':')
  for i in range(1, 5):
    unique_colors.append(color_with_class[i].split(';')[0].strip())

  # remove duplicates and sort:
  unique_colors = list(dict.fromkeys(unique_colors))
  unique_colors.sort()

  # flatten to string
  unique_colors_as_string = ' '.join(unique_colors)

  return unique_colors_as_string

  
conn = sqlite3.connect('../generated/routes.db')

conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("select color_codes, dat, typ, place, rid from routes where retired = True and color_codes is not null;")
routes = c.fetchall()

c2 = conn.cursor()
for route in routes:
    fixed_color_codes = get_unique_colors(route['color_codes'])
    dat = route['dat']
    typ = route['typ']
    place = route['place']
    rid = route['rid']
        
    c2.execute("update routes set color_codes= ? where dat= ? and typ= ? and place= ? and rid= ? ", (fixed_color_codes, dat, typ, place, rid))
    conn.commit()
    
conn.close()

