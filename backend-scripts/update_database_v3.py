#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from pprint import pprint
import sqlite3
import sys

WebColorMap = {}
# English
WebColorMap["beige"] = "#DEB887" #was F5F5DC
WebColorMap["black"] = "#000000"
WebColorMap["blue"] = "#0000FF"
WebColorMap["brown"] = "#A52A2A"
WebColorMap["grey"] = "#808080"
WebColorMap["green"] = "#008000"
WebColorMap["orange"] = "#FFA500"
WebColorMap["pink"] = "#FFC0CB"
WebColorMap["red"] = "#FF0000"
WebColorMap["purple"] = "#800080"
WebColorMap["white"] = "#FFFFFF"
WebColorMap["yellow"] = "#FFFF00"

InverseMap = {} # Used for filling in color_codes for the old routes that only had color names
# German
InverseMap["rot"] = "#FF0000"
InverseMap["grun"] = "#008000"
InverseMap["weiss"] = "#FFFFFF"
InverseMap["braun"] = "#A52A2A"
InverseMap["blau"] = "#0000FF"
InverseMap["violett"] = "#FFC0CB"
InverseMap["gelb"] = "#FFFF00"
InverseMap["schwarz"] = "#000000"
InverseMap["grau"] = "#808080"
InverseMap["orange"] = "#FFA500"
InverseMap["pink"] = "#FFC0CB"
InverseMap["beige"] = "#DEB887"

# Special
InverseMap["marmor"] = "#FFFFFF #000000"
InverseMap["kombo"] = "#FFFF00"
InverseMap["jamaica"] = "#008000 #FFFF00 #000000"
InverseMap["holz"] = "#A4826A"
InverseMap["spezial"] = "#FF0000 #FFC0CB #FFFF00 #FFA500"


def rgbFromStr(s):
    # s starts with a #.
    r, g, b = int(s[1:3],16), int(s[3:5], 16),int(s[5:7], 16)
    return r, g, b

def findNearestColorName(code, map = WebColorMap):
    R, G, B = rgbFromStr(code)
    mindiff = None
    for key in map:
        r, g, b = rgbFromStr(map[key])
        diff = abs(R-r)*256 + abs(G-g)*256 + abs(B-b)*256
        if mindiff is None or diff < mindiff:
            mindiff = diff
            mincolorname = key
    return mincolorname

conn = sqlite3.connect('../generated/routes.db')

# Read routes from json and update the database. It keeps old routes (not on the wall any more) as is, except
# set Retired to True.
try:
    c = conn.cursor()

    c.execute("UPDATE routes SET retired=1")
    c.execute("UPDATE routes SET new_=0")

    data = json.load(open('../generated/json_from_html.json'))
    mapping = json.load(open('../intermediate_calculations/mappingv2.json'))

    for route in data:
        # things to get and insert to table:
        # dat, typ, place, rid, vlid, name, full_name, grade, setter, color_codes, vlsector, new_, retired

        # Mapping magic
#        vlid = route['number']
#        print(route['dat'], route['typ'], route['place'], route['number'], route['full_name'], route['grade'], route['setter'], route['color_codes'], route['vlsector'])
#        if str(vlid) in mapping:
#            # Found a match in old DB. Keep the old date as I checked and they messed it up 18 times.
#            old_route = mapping[str(vlid)]
#            dat = old_route[0]
#            rid = old_route[3]
#        else:
#            # If not matching found both ids will be the new and the date is from the new DB
#            rid = route['number']
#            dat = route['dat']

        vlid = route['number']
        rid = vlid
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
        
        c.executemany("INSERT INTO routes (rid, vlid, dat, typ, place, name, full_name, grade, setter, color_codes, vlsector, new_, retired) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT (dat, typ, place, rid) DO UPDATE SET vlid=excluded.vlid, name=excluded.name, full_name=excluded.full_name, grade=excluded.grade, setter=excluded.setter, color_codes=excluded.color_codes, vlsector=excluded.vlsector, new_=excluded.new_, retired=excluded.retired", next_route_to_insert)

    conn.commit()
except conn.Error as err:
    print(err)
    print("Update database transaction failed! ROLLBACK")
    conn.rollback()


# Fill in the color column based on color_codes
conn.row_factory = sqlite3.Row

try:
    select_query = conn.cursor()
    select_query.execute("SELECT dat, typ, place, rid, color_codes FROM routes WHERE color_codes IS NOT NULL AND COLOR IS NULL;")
    routes_without_color = select_query.fetchall()

    update_query = conn.cursor()
    for route in routes_without_color:
        color_names = []
        colors_list = route['color_codes'].split(' ')
        for color in colors_list:
            color_names.append(findNearestColorName(color))
        color_names.sort()
        color_names_as_string = ','.join(color_names)

        dat = route['dat']
        typ = route['typ']
        place = route['place']
        rid = route['rid']
        update_query.execute("update routes set color= ? where dat= ? and typ= ? and place= ? and rid= ? ", (color_names_as_string, dat, typ, place, rid))
        conn.commit()
        
except conn.Error as err:
    print(err)
    print("Update color based on color_codes transaction failed! ROLLBACK")
    conn.rollback()


# Fill in the color_codes column based on color
try:
    select2_query = conn.cursor()
    select2_query.execute("SELECT dat, typ, place, rid, color FROM ROUTES WHERE color_codes IS NULL AND color IS not NULL;")
    routes_without_color_codes = select2_query.fetchall()

    update2_query = conn.cursor()
    for route in routes_without_color_codes:
        color_codes = []
        # Braun-Grün
        color_names_list = route['color'].lower().replace(u'ü', 'u').split('-')
        # ['braun', 'grun']
        color_names_list.sort()
        for color in color_names_list:
            color_codes.append(InverseMap[color])
        color_codes.sort()
        color_codes_as_string = ' '.join(color_codes)

        dat = route['dat']
        typ = route['typ']
        place = route['place']
        rid = route['rid']
        update2_query.execute("update routes set color_codes= ? where dat= ? and typ= ? and place= ? and rid= ? ", (color_codes_as_string, dat, typ, place, rid))
        conn.commit()
        
except conn.Error as err:
    print(err)
    print("Update color_codes based on color transaction failed! ROLLBACK")
    conn.rollback()
    
conn.close()

