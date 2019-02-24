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

    data = json.load(open('../generated/routes.json'))

    for route in data:
        # things to get and insert to table:
        # dat, typ, place, rid, name, subname, grade, setter, color, toprope, toppas, lead, sector, new_, lastcall, retired, kids, imgurl
        # dat (date)
        dat = route['RouteErstellungsdatum'].split('T')[0]

        # typ (type), toprope, roppas, lead
        typ = "bould"
        toprope = False
        toppas = False
        lead = False
        
        route_type = route['ClimbingRoutesRouteType']
        if route_type != 'Boulder':
            typ = "sport"
            toprope = route['IstTopRope']
            toppas = route['IstToppas']
            lead = route['IstVorstieg']

        place = route['OrtBez']
        if place == 'Greifensee':
            place = "mil"
        else:
            place = "gas"

        rid = route['RoutenNr']
        
        if typ == "bould":
            name = "Boulder #" + str(rid)
        else:
            name = route['RouteBez'].strip()

        if typ == "sport":
            subname = route['BemerkungRoutenschild']
        else:
            subname = ""
        grade = route['SchwierigkeitsgradBez']
        setter = route['RoutenbauerVornameNachname']

        color = route['GrifffarbeBez']
    
        sector = route['SektorBez']

        # new_, lastcall, retired
        new_ = False
        lastcall = False
        retired = False
    
        status = route['RoutenAlterStatusID']
        if status == 1:
            new_ = True
        else:
            if status == 2:
                lastcall = True

        kids = route['IstKinderfreundlich']

        imgurl = '_routenFarben/' +str(route['GrifffarbeID']) + '.png'

        next_route_to_insert = [(dat, typ, place, rid, name, subname, grade, setter, color, toprope, toppas, lead, sector, new_, lastcall, retired, kids, imgurl)]
    
        c.executemany("INSERT OR REPLACE INTO routes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", next_route_to_insert)

    conn.commit()
except conn.Error:
    print("Transaction failed! ROLLBACK")
    conn.rollback()
    
conn.close()

