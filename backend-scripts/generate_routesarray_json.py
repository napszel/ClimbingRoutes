#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from pprint import pprint
import sqlite3

conn = sqlite3.connect('../generated/routes.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

bigtable = []
for route in c.execute('SELECT routes.*, postcount.posts, postcount.commenter, postcount.latest FROM routes LEFT JOIN postcount ON routes.dat = postcount.dat AND routes.typ = postcount.typ AND routes.place = postcount.place AND routes.rid = postcount.rid ORDER BY routes.dat DESC'):
    table = {}

    place = route['place']
    table["place"] = place.capitalize()

    route_rid = str(route['rid'])
    table["rid"] = route_rid

    route_vlid = str(route['vlid'])
    table["vlid"] = route_vlid

    name = route['name']
    table["name"] = name

    full_name = route['full_name']
    table["full_name"] = full_name

    table["grade"] = route['grade']

    route_type = route['typ']
    date = route['dat']

    route_identifier = date + ":" + route_type + ":" + place + ":" + route_rid
    table["pk"] = route_identifier

    if route['posts'] == None:
        table["last_commenter"] = None
        table["last_comment_time"] = None
        table["comment_count"] = None
    else:
        table["last_commenter"] = route['commenter']
        table["last_comment_time"] = route['latest'].split("T")[0] + " " + route['latest'].split("T")[1]
        table["comment_count"] = route['posts']

    table["setter"] = route['setter']
    table["date"] = date
    table["color"] = route['color']
    table["typ"] = route['typ'].capitalize()

    belays = []
    if route['toprope']:
        belays.append("Toprope")
    if route['toppas']:
        belays.append("Toppas")
    if route['lead']:
        belays.append("Lead")
    if belays:
        table["belay"] = str(belays).replace("'","").strip("[]")
    else:
        table["belay"] = "Mats"
            
    table["sector"] = route['sector']
    table["vlsector"] = route['vlsector']

    if route['new_'] or route['lastcall'] or route['retired']:
        if route['new_']:
            table["state"] = "New"
        if route['lastcall']:
            table["state"] = "Last Call"
        if route['retired']:
            table["state"] = "Retired"
    else:
        table["state"] = None

    if route['kids']:
        table["kids"] = True
    else:
        table["kids"] = False

    table["imgurl"] = route['imgurl']
    table["color_codes"] = route['color_codes']

    bigtable.append(table)

html = open('../generated/routesarray.js', 'w')
html.write("routesarray = " + json.dumps(bigtable) + "\n")
html.close()
