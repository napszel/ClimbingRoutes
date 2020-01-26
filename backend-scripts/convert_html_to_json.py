#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import codecs
import pprint
from collections import OrderedDict
import time
import json
from datetime import date
import sys

today = date.today()
formatted_today = today.strftime("%Y%m%d")

milandia_html = '../daily-saves/{}-mil-routes.html'.format(formatted_today)
gaswerk_html = '../daily-saves/{}-gas-routes.html'.format(formatted_today)

def fill_in_full_names(all_routes):
  try:
    full_names = open("nevek.jo", "r")
  except (FileNotFoundError):
#    print("nevek.jo file not found in directory. No full_name matching done.")
    return {}
    
  names_list = full_names.readlines()
  numbers_names = {}
  for item in names_list:
    name = item.split(':')[1].strip()
    number = int(item.split(':')[0])
    numbers_names[number] = name

  full_name_all_routes = []
  for route in all_routes:
    next_route = route.copy()
    if next_route['number'] in numbers_names:
      next_route['full_name'] = numbers_names[next_route['number']]
    full_name_all_routes.append(next_route)
      
  return full_name_all_routes


def parse_html_to_routes_dict(html, place):
  page = codecs.open(html, 'r')
  soup = BeautifulSoup(page, "lxml")

  routes_table = soup.findAll("table", {"class" : 'table table-striped iframe-table'})[0].find("tbody")
  routes = []
  
  for route in routes_table.findAll("tr"):
    next_route = OrderedDict()

    next_route['place'] = place
    next_route['number'] = int(route.find("a", {"class": 'route_name'}).get('href').split('/')[4])
    next_route['name'] = route.find("a", {"class": 'route_name'}).text
    next_route['full_name'] = None
    next_route['grade'] = route.find("td", {"class": 'grade'}).text
    next_route['setter'] = route.find("td", {"class": 'route_setter'}).text
    next_route['dat'] = time.strftime('%Y-%m-%d', time.localtime(int(route.find("td", {"class": 'date'}).text)))
    next_route['color_codes'] = route.find("div", {"class": 'iframe-circle'}).get("style")
    next_route['typ'] = 'sport'
    next_route['vlsector'] = route.find("td", {"class": 'sector'}).find('a').text
    next_route['new_'] = 1 if route.find("div", {"class": 'new-small-badge'}) else 0
    
    routes.append(next_route)
  
  boulders_table = soup.findAll("table", {"class" : 'table table-striped iframe-table'})[1].find("tbody")
  boulders = []
  
  for boulder in boulders_table.findAll("tr"):
    next_boulder = OrderedDict()
    
    next_boulder['place'] = place
    next_boulder['number'] = int(boulder.find("a", {"class": 'boulder_name'}).get('href').split('/')[4])
    next_boulder['name'] = boulder.find("a", {"class": 'boulder_name'}).text
    next_boulder['full_name'] = None
    next_boulder['grade'] = boulder.find("td", {"class": 'grade'}).text
    next_boulder['setter'] = boulder.find("td", {"class": 'route_setter'}).text
    next_boulder['dat'] = time.strftime('%Y-%m-%d', time.localtime(int(boulder.find("td", {"class": 'date'}).text)))
    next_boulder['color_codes'] = boulder.find("div", {"class": 'iframe-circle'}).get("style")
    next_boulder['typ'] = 'bould'
    next_boulder['vlsector'] = boulder.find("td", {"class": 'sector'}).find('a').text
    next_boulder['new_'] = 1 if boulder.find("div", {"class": 'new-small-badge'}) else 0
    
    boulders.append(next_boulder)

  return routes, boulders

def main(args=None):
  milandia_routes, milandia_boulders = parse_html_to_routes_dict(milandia_html, "mil")
  gaswerk_routes, gaswerk_boulders = parse_html_to_routes_dict(gaswerk_html, "gas")
  
  all_routes = milandia_boulders + gaswerk_routes + gaswerk_boulders + milandia_routes

  full_name_all_routes = fill_in_full_names(all_routes)
  
  print(json.dumps(full_name_all_routes, indent=4, ensure_ascii=False))

if __name__ == '__main__':
  df = main()
