#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from pprint import pprint
import sqlite3

conn = sqlite3.connect('routes.db')

try:
    c = conn.cursor()

    c.execute("UPDATE routes SET retired=1")
    c.execute("UPDATE routes SET new_=0")
    c.execute("UPDATE routes SET lastcall=0")

    data = json.load(open('routes.json'))

    for route in data:
        # things to get and insert to table:
        # dat, typ, place, rid, name, subname, grade, setter, color, toprope, toppas, lead, sector, new_, lastcall, retired, kids, imgurl
        # dat (date)
        wrongdate = route['builddateFormatted'].split('.')
        dat = wrongdate[2] + "-" + wrongdate[1] + "-" + wrongdate[0]

        # typ (type), toprope, roppas, lead
        typ = "bould"
        toprope = False
        toppas = False
        lead = False
        
        route_type = route['type']
        if route_type != 'Boulder':
            typ = "sport"
            route_type = route_type.replace(" ", "");
            belays = route_type.split(',');
            for belay in belays:
                if belay == 'Toprope':
                    toprope = True
                else:
                    if belay == 'Toppas':
                        toppas = True
                    else:
                        lead = True

        place = route['address']
        if place == 'Milandia':
            place = "mil"
        else:
            place = "gas"

        rid = route['nr']

        name = route['title']

        subname = route['subtitle']
        grade = route['difficulty']
        setter = route['builders']

        color = route['gripcolor']
    
        sector = route['sector']

        # new_, lastcall, retired
        new_ = False
        lastcall = False
        retired = False
    
        status = route['statusLabel']
        if status == 'Neu':
            new_ = True
        else:
            if status == 'Last Call':
                lastcall = True

        kids = route['children']

        imgurl = route['gripImage']

        next_route_to_insert = [(dat, typ, place, rid, name, subname, grade, setter, color, toprope, toppas, lead, sector, new_, lastcall, retired, kids, imgurl)]
    
        c.executemany("INSERT OR REPLACE INTO routes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", next_route_to_insert)

    conn.commit()
except conn.Error:
    print("Transaction failed! ROLLBACK")
    conn.rollback()
    
conn.close()

