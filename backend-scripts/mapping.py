#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from pprint import pprint
import sqlite3
import sys

def get_the_real_names():
    full_names = open("../generated/nevek.jo", "r")
    names_list = full_names.readlines()
    numbers_names = {}
    for item in names_list:
        name = item.split(':')[1].strip()
        number = int(item.split(':')[0])
        numbers_names[number] = name

    return numbers_names


def fix_json_with_full_names(real_names_with_numbers):
    jd = json.load(open('../generated/json_from_html.json'))
    correct_routes_json = []
    for route in jd:
        next_route = route.copy()
        next_route['name'] = real_names_with_numbers[next_route['number']]
        correct_routes_json.append(next_route)

    return correct_routes_json


def do_the_matching(jd):
    conn = sqlite3.connect('../generated/routes.db')
    db = conn.cursor()
    db.execute('SELECT count(*) from routes')
    print("Number of routes in old DB: {}".format(db.fetchone()))
    
#    jd = json.load(open('../generated/json_from_html.json'))
    print("Number of routes in new json: {}".format(len(jd)))

    not_matched_routes = []
    too_many_matches = []

    matched_routes = {}

    for route in jd:
        # Boulders can't be matched by name as they didn't have names before, and now they just can a color as name
        if route['typ'] == 'bould':
            continue

        # If route is newer than the last I have in my DB it can't be matched 
        route_date = route['dat'].split('-')
        if int(route_date[0]) == 2019 and (int(route_date[1]) > 11 or (int(route_date[1]) == 11 and int(route_date[2]) > 18)):
            continue

        # No way to match these combination routes but we never climb them anyway
        if route['name'] == 'Kombination' or route['name'] == 'Kombo':
            continue
    
        new_name = "%{}%".format(route['name'])
        db.execute('SELECT dat, typ, place, rid from routes where name like ?', (new_name,))
        matched_name = db.fetchall()
        
        if (len(matched_name) == 0):
            not_matched_routes.append(route['name'])
            continue
    
        if (len(matched_name) > 1):
            too_many_matches.append(route['name'])
            continue

        matched_routes[route['number']] = matched_name[0]

    print("No matches for ")
    print(not_matched_routes)
    print("Number of not matched routes: {}".format(len(not_matched_routes)))
    print("Too many routes matched to ")
    print(too_many_matches)
    print(matched_routes)
    
    conn.close()
    

def main(args=None):
    real_names_with_numbers = get_the_real_names()
    correct_routes_json = fix_json_with_full_names(real_names_with_numbers)
    do_the_matching(correct_routes_json)

    #print(json.dumps(correct_routes_json, indent=4, ensure_ascii=False))

if __name__ == '__main__':
  df = main()
