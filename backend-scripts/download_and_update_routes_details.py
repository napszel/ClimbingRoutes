#!venv/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import requests
import re
import html

conn = sqlite3.connect('../generated/routes.db')
conn.row_factory = sqlite3.Row

headers = {'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'X-Requested-With': 'XMLHttpRequest'}

# Download urls are always one of four formats, Only route type matters.
# https://gyms.vertical-life.info/en/gaswerk-greifensee/iframe/64264/iframe_route_detail
# https://gyms.vertical-life.info/en/gaswerk-greifensee/iframe/126018/iframe_boulder_detail
# https://gyms.vertical-life.info/en/gaswerk-schlieren/iframe/64264/iframe_route_detail
# https://gyms.vertical-life.info/en/gaswerk-schlieren/iframe/126018/iframe_boulder_detail
route_details_url = "https://gyms.vertical-life.info/en/gaswerk-%s/iframe/%s/iframe_%s_detail"

# Match name whic is inside <h4> tag.
# <h4>Feedbackkulturparadigmenwechsel 6a+<\/h4>
# Additional patterns are needed to filter out
# - route/boulder grade which is included on the details page in the title
# - label for not zlagged routes
# <h4>Download the Vertical-Life Climbing app and mark your climbs!</h4>
name_pattern = re.compile('.*route-info.*<h4>(.+?) \S*<\\\\/h4>.*route-topo.*')

# Match first jpg image on the details page which is after 'holder' div and before 'wall-holder'
# <div id="holder" ... data-image-src="https://d1ffqbcmevre4q.cloudfront.net/e90e4c8a080771d0028b7f753e46e45e.jpg">...<div id="wall-holder"...
sector_url_pattern = re.compile('.*<div id=\\\\"holder\\\\".*data-image-src=\\\\"https://d1ffqbcmevre4q\.cloudfront\.net/(.+?\.jpg)\\\\">.*id=\\\\"wall-holder\\\\".*')

try:
    c = conn.cursor()
    
    for route in conn.cursor().execute('SELECT dat, typ, place, rid, name, vlid FROM routes WHERE sectorimg IS NULL AND vlid IS NOT NULL AND vlid != "" AND retired=0'):
        
        print('Check route rid:', route['rid'], ' vlid:', route['vlid'])
        
        db_name = route['name']
        vlid = str(route['vlid'])
        dat = route['dat']
        typ = route['typ']
        place = route['place']
        rid = route['rid']

        if typ == 'bould':
            full_typ = 'boulder'
        else:    
            full_typ = 'route'

        if place == 'mil':
            full_place = 'greifensee'
        else:    
            full_place = 'schlieren'
        
        download_url = route_details_url %(full_place, vlid, full_typ)
        
        print(download_url)
        
        response = requests.get(download_url, headers=headers)
        
        if not response.ok:
            print('Wrong response for route "', db_name, '",', vlid, '[', download_url, ']. Continue')
            continue
        
        if name_pattern.match(response.text):
            full_name = html.unescape(name_pattern.search(response.text).group(1))
            if db_name != full_name:
                print("Name needs update! Database name:", db_name, " Full name: ", full_name)
        
        sector_img = None
        if sector_url_pattern.match(response.text):
            sector_img = sector_url_pattern.search(response.text).group(1)
            print("Sector image: ", sector_img)
        
        if db_name != full_name or sector_img is not None:
            print("Updating the route rid:", rid)
            c.execute("UPDATE routes SET name=?, sectorimg=? WHERE dat=? AND typ=? AND place=? AND rid=?", (full_name, sector_img, dat, typ, place, rid))

    conn.commit()
except conn.Error:
    print("Transaction failed! ROLLBACK")
    conn.rollback()

conn.close()
