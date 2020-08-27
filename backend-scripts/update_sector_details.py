#!venv/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import csv

mapping_file_name = "sector_img_mapping.csv"

conn = sqlite3.connect('../generated/routes.db')
conn.row_factory = sqlite3.Row

with open(mapping_file_name, mode='r') as mapping_file:
    reader = csv.reader(mapping_file)
    sectors_mapping = {rows[0]:rows for rows in reader}

try:
    c = conn.cursor()
    
    for route in conn.cursor().execute('SELECT dat, typ, place, rid, name, sectorimg FROM routes WHERE sectorimg IS NOT NULL AND sector1 IS NULL'):

        dat = route['dat']
        typ = route['typ']
        place = route['place']
        rid = route['rid']
        sectorimg = route['sectorimg']

        sector1 = sectors_mapping[sectorimg][2] if len(sectors_mapping[sectorimg]) > 2 else None
        sector2 = sectors_mapping[sectorimg][3] if len(sectors_mapping[sectorimg]) > 3 else None
        sector3 = sectors_mapping[sectorimg][4] if len(sectors_mapping[sectorimg]) > 4 else None

        if sector1 is not None:
            c.execute("UPDATE routes SET sector1=?, sector2=?, sector3=? WHERE dat=? AND typ=? AND place=? AND rid=?", (sector1, sector2, sector3, dat, typ, place, rid))

    conn.commit()
except conn.Error:
    print("Transaction failed! ROLLBACK")
    conn.rollback()

conn.close()
