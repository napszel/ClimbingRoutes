#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import codecs
import pprint
from collections import OrderedDict
import time
import json

#test_html = '../daily-saves/test-format.html'
milandia_html = '../daily-saves/20200104-mil-routes.html'
gaswerk_html = '../daily-saves/20200104-gas-routes.html'


def parse_html_to_routes_dict(html, place):
  page = codecs.open(html, 'r')
  soup = BeautifulSoup(page, "lxml")

  routes_table = soup.findAll("table", {"class" : 'table table-striped iframe-table'})[0].find("tbody")
  routes = []
  
  for route in routes_table.findAll("tr"):
    next_route = OrderedDict()

    next_route['place'] = place
    next_route['rid'] = None
    next_route['number'] = int(route.find("a", {"class": 'route_name'}).get('href').split('/')[4])
    next_route['name'] = route.find("a", {"class": 'route_name'}).text
    next_route['grade'] = route.find("td", {"class": 'grade'}).text
    next_route['setter'] = route.find("td", {"class": 'route_setter'}).text
    next_route['dat'] = time.strftime('%Y-%m-%d', time.localtime(int(route.find("td", {"class": 'date'}).text)))
    next_route['color'] = None
    next_route['color-codes'] = route.find("div", {"class": 'iframe-circle'}).get("style")
    next_route['typ'] = 'sport'
    next_route['toprope'] = None
    next_route['toppas'] = None
    next_route['lead'] = None
    next_route['sector'] = route.find("td", {"class": 'sector'}).find('a').text
    next_route['new_'] = 1 if route.find("div", {"class": 'new-small-badge'}) else 0
    next_route['last_call'] = 0
    next_route['kids'] = 0
    next_route['imgurl'] = None
    
    routes.append(next_route)
  
  boulders_table = soup.findAll("table", {"class" : 'table table-striped iframe-table'})[1].find("tbody")
  boulders = []
  
  for boulder in boulders_table.findAll("tr"):
    next_boulder = OrderedDict()
    
    next_boulder['place'] = place
    next_boulder['rid'] = None
    next_boulder['number'] = int(boulder.find("a", {"class": 'boulder_name'}).get('href').split('/')[4])
    next_boulder['name'] = boulder.find("a", {"class": 'boulder_name'}).text
    next_boulder['grade'] = boulder.find("td", {"class": 'grade'}).text
    next_boulder['setter'] = boulder.find("td", {"class": 'route_setter'}).text
    next_boulder['dat'] = time.strftime('%Y-%m-%d', time.localtime(int(boulder.find("td", {"class": 'date'}).text)))
    next_boulder['color'] = None
    next_boulder['color-codes'] = boulder.find("div", {"class": 'iframe-circle'}).get("style")
    next_boulder['typ'] = 'bould'
    next_boulder['toprope'] = 0
    next_boulder['toppas'] = 0
    next_boulder['lead'] = 0
    next_boulder['sector'] = boulder.find("td", {"class": 'sector'}).find('a').text
    next_boulder['new_'] = 1 if boulder.find("div", {"class": 'new-small-badge'}) else 0
    next_boulder['last_call'] = 0
    next_boulder['kids'] = 0
    next_boulder['imgurl'] = None
    
    boulders.append(next_boulder)

  return routes, boulders

def main(args=None):
    milandia_routes, milandia_boulders = parse_html_to_routes_dict(milandia_html, "mil")
    gaswerk_routes, gaswerk_boulders = parse_html_to_routes_dict(gaswerk_html, "gas")

    all_routes = milandia_routes + milandia_boulders + gaswerk_routes + gaswerk_boulders

    print(json.dumps(all_routes, indent=4, ensure_ascii=False))

if __name__ == '__main__':
  df = main()
