#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from pprint import pprint
import sqlite3

html = open('../index.html', 'w')

html_headers = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>~ Climbing Routes ~</title>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js"></script>
    <script src="javascript.js"></script>
    
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.min.css" media="screen"/>
    
    <link rel="stylesheet" type="text/css" href="style.css" media="screen" />
    <link rel="shortcut icon" href="favicon.png" type="image/png"/>
  </head>
  
  <body>
  <div id="route_root" style="display: none">
    <div id="header"></div>
    <hr/>
    <div id="disqus_thread"></div>
     <script>
        var disqus_config = function () {
          var startHash = window.location.search;
          this.page.url = 'http://napszel.com/climbingroutes' + startHash;
          this.page.identifier = '';
          parts = startHash.split(":");
          date = parts[0].split("=")[1];
          type = parts[1]
          place = parts[2]
          number = parts[3]
          if (place == 'gas') {
            place = "Gaswerk";
          } else {
            place = "Milandia";
          }
          if (type == 'bould') {
            type = "Boulder";
          } else {
            type = "Sport";
          }
          this.page.title = date + ' ' + place + ' ' + type + ' route #' + number;
        };
      (function() { // DON'T EDIT BELOW THIS LINE
      var d = document, s = d.createElement('script');
      s.src = 'https://climbingroutes.disqus.com/embed.js';
      s.setAttribute('data-timestamp', +new Date());
      (d.head || d.body).appendChild(s);
      })();
    </script>
    <noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
  </div>

  <div id="main_table" style="display: none">
    <div class="buttons_container">
      <label class="title">Climbing Routes of <a class=\"underline\" href="http://www.kletterzentrum.com/unser-angebot/kletterzentrum-gaswerk/">Gaswerk</a> and <a class=\"underline\" href="http://www.kletterzentrum.com/unser-angebot/kletterzentrum-milandia/">Milandia</a></label>
      <input type="button" class="button" id="gaswerk_map" value="Map of Gaswerk" onclick="window.open('gaswerk_map.png')" />
      <input type="button" class="button" id="milandia_map" value="Map of Milandia" onclick="window.open('milandia_map.png')" />
    </div>
    <hr/>

"""

html.write(html_headers)

table = """
<table id="example" class="display compact order-column" cellspacing="0" width="100%">
<thead>
<tr>
<th title="Field #15" class="twenty">Pl.</th>
<th title="Field #1" class="twenty">#</th>
<th title="Field #3">Route Name</th>
<th title="Field #6" class="twenty">Gr.</th>
<th title="Field #2" class="twenty">Comments</th>
<th title="Field #8">Setter's Name</th>
<th title="Field #18" class="ninety">Date</th>
<th title="Field #12" class="hundredten">Color</th>
<th title="Field #20" class="fourty">Bould / Sport</th>
<th title="Field #21" class="hundredten">Belay</th>
<th title="Field #13">Sector</th>
<th title="Field #10" class="sixty">New / Last Call / Retired</th>
<th title="Field #19" class="twenty">Kids</th>
</tr>
</thead>
<tfoot>
<tr>
<th title="Field #15">Mil/Gas</th>
<th title="Field #1">#</th>
<th title="Field #3">Filer by route name</th>
<th title="Field #6">6a+</th>
<th title="Field #2"></th>
<th title="Field #8">Filter by setter's name</th>
<th title="Field #18">Filter by date</th>
<th title="Field #12">Color</th>
<th title="Field #20">Bould/Sport</th>
<th title="Field #21">Toppas/Lead/Toprope</th>
<th title="Field #13">Filter by sector name</th>
<th title="Field #10">New/Last Call/Retired</th>
<th title="Field #19">Kids</th>
</tr>
</tfoot>
<tbody>
"""
conn = sqlite3.connect('routes.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

def getElement(s):
    return "<td>" + s + "</td>"

for route in c.execute('SELECT * FROM routes ORDER BY dat DESC'):
    table += "<tr>"

    place = route['place']
    table += getElement(place.capitalize())

    route_number = str(route['rid'])
    table += getElement(route_number)

    table += "<td>" + route['name']
    if route['subname']:
        table += " (" + route['subname'] + ")"
    table += "</td>"

    table += getElement(route['grade'])

    route_type = route['typ']

    date = route['dat']

    route_identifier = date + ":" + route_type + ":" + place + ":" + route_number
    table += "<td class=\"centered tiny\"><a href=\"?route-comment=" + route_identifier + "\" target=\"_blank\">&#128172;</a></td>"

    table += getElement(route['setter'])
    table += getElement(date)
    table += getElement(route['color'])
    table += getElement(route['typ'].capitalize())

    belays = []
    if route['toprope']:
        belays.append("Toprope")
    if route['toppas']:
        belays.append("Toppas")
    if route['lead']:
        belays.append("Lead")
    if belays:
        table += getElement(str(belays).replace("'","").strip("[]"))
    else:
        table += getElement("Mats")
            
    table += getElement(route['sector'])

    if route['new_'] or route['lastcall'] or route['retired']:
        if route['new_']:
            table += getElement("New")
        if route['lastcall']:
            table += getElement("Last Call")
        if route['retired']:
            table += getElement("Retired")
    else:
        table += getElement("")

    if route['kids']:
        table += "<td class=\"centered\">Y</td>"
    else:
        table += "<td class=\"centered\">N</td>"

    table += "</tr>"
    

table += """
</tbody>
</table>"""
html.write(table)

html_end = """
<div id="credits">
<a class=\"underline\" href="https://github.com/napszel/ClimbingRoutes" target="_blank" rel="noopener noreferrer">Napszel,</a> 2018
</div>
</div>
<!--<script id="dsq-count-scr" src="//climbingroutes.disqus.com/count.js" async></script>-->
</body>
</html>
"""
html.write(html_end)
html.close
