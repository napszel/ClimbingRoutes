#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from pprint import pprint
import sqlite3

conn = sqlite3.connect('../generated/routes.db')

try:
    c = conn.cursor()

    c.execute("UPDATE routes SET retired=1")
    c.execute("UPDATE routes SET new_=0")
    c.execute("UPDATE routes SET lastcall=0")

    data = json.load(open('../generated/json_from_html_with_full_names.json'))

    # TODO: read in the mapping file too

    for route in data:
        # things to get and insert to table:
        # dat, typ, place, rid, vlid, name, full_name, grade, setter, color, color_codes, toprope, toppas, lead,
        # sector, vlsector, new_, lastcall, retired, kids, imgurl
        
        dat = route['dat']
        typ = route['typ']
        place = route['place']
        
        # TODO rid/vlid logic here

        name = route['name']
        full_name = route['full_name']
        grade = route['grade']
        setter = route['setter']
        color_codes = route['color_codes']
        vlsector = route['vlsector']

        # TODO validation before insert!
        
        next_route_to_insert = [(dat, typ, place, rid, name, grade, setter, color, toprope, toppas, lead, sector, new_, lastcall, retired, kids, imgurl)]
    
        c.executemany("INSERT OR REPLACE INTO routes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", next_route_to_insert)

    conn.commit()
except conn.Error:
    print("Transaction failed! ROLLBACK")
    conn.rollback()
    
conn.close()

