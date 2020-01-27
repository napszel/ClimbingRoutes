#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from pprint import pprint
import sqlite3
import sys

conn = sqlite3.connect('../generated/routes.db')

try:
    c = conn.cursor()

    c.execute("UPDATE routes SET retired=1")
    c.execute("UPDATE routes SET new_=0")

    data = json.load(open('../generated/json_from_html_with_full_names.json'))
    mapping = json.load(open('../intermediate_calculations/mappingv2.json'))

    for route in data:
        # things to get and insert to table:
        # dat, typ, place, rid, vlid, name, full_name, grade, setter, color_codes, vlsector, new_, retired

        # Mapping magic
        vlid = route['number']
        if str(vlid) in mapping:
            # Found a match in old DB. Keep the old date as I checked and they messed it up 18 times.
            old_route = mapping[str(vlid)]
            dat = old_route[0]
            rid = old_route[3]
        else:
            # If not matching found both ids will be the new and the date is from the new DB
            rid = route['number']
            dat = route['dat']

        typ = route['typ']
        place = route['place']
        name = route['name']
        full_name = route['full_name']
        grade = route['grade']
        setter = route['setter']
        color_codes = route['color_codes']
        vlsector = route['vlsector']
        new_ = True if route['new_'] == 1 else False
        retired = False

        next_route_to_insert = [(rid, vlid, dat, typ, place, name, full_name, grade, setter, color_codes, vlsector, new_, retired)]
        
        c.executemany("INSERT OR REPLACE INTO routes (rid, vlid, dat, typ, place, name, full_name, grade, setter, color_codes, vlsector, new_, retired) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", next_route_to_insert)

    conn.commit()
except conn.Error as err:
    print(err)
    print("Transaction failed! ROLLBACK")
    conn.rollback()
    
conn.close()

