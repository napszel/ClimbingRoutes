#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from pprint import pprint

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
          place = parts[0].split("=")[1];
          if (place == 'gas') {
            place = "Gaswerk";
          } else {
            place = "Milandia";
          }
          type = parts[2];
          if (type == 'bould') {
            type = "Boulder";
          } else {
            type = "Sport";
          }
          this.page.title = place + ' ' + type + ' route #' + parts[1];
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
<th title="Field #15" class="narrow">Pl.</th>
<th title="Field #1" class="narrow">#</th>
<th title="Field #3">Route Name</th>
<th title="Field #6" class="narrow">Gr.</th>
<th title="Field #2" class="narrow">&#128172;</th>
<th title="Field #8">Setter's Name</th>
<th title="Field #18" class="middle">Date</th>
<th title="Field #12" class="middle">Color</th>
<th title="Field #20" class="smallish">Bould./Sport</th>
<th title="Field #21">Belay</th>
<th title="Field #13">Sector</th>
<th title="Field #10" class="smallish">Neu/<br/>Last Call</th>
<th title="Field #19" class="narrow">Kids</th>
</tr>
</thead>
<tfoot>
<tr>
<th title="Field #15" class="narrow">Mil/Gas</th>
<th title="Field #1" class="narrow">#</th>
<th title="Field #3">Filer by route name</th>
<th title="Field #6">6a+</th>
<th title="Field #2"></th>
<th title="Field #8">Filter by setter's name</th>
<th title="Field #18">Filter by date</th>
<th title="Field #12">Color</th>
<th title="Field #20">Bould/Sport</th>
<th title="Field #21">Toppas/Vorsteig/Toprope</th>
<th title="Field #13">Filter by sector name</th>
<th title="Field #10">Neu/Last Call</th>
<th title="Field #19">Kids</th>
</tr>
</tfoot>
<tbody>
"""

data = json.load(open('routes.json'))

def getElement(s):
    return "<td>" + s + "</td>"

for route in data:
    route_identifier=""
    
    table += "<tr>"

    if route['address'] == 'Milandia':
        table += getElement("Mil")
        route_identifier += "mil:"
    else:
        table += getElement("Gas")
        route_identifier += "gas:"

    table += getElement(str(route['nr']))
    route_identifier += str(route['nr']) + ":"

    table += "<td>" + route['title']
    if route['subtitle']:
        table += " (" + route['subtitle'] + ")"
    table += "</td>"

    table += getElement(route['difficulty'])

    if route['type'] == 'Boulder':
        route_identifier += "bould"
    else:
        route_identifier += "sport"

    table += "<td class=\"centered tiny\"><a href=\"?route-comment=" + route_identifier + "\" target=\"_blank\">&#128172;</a></td>"

    table += getElement(route['builders'])
    
    wrongdate = route['builddateFormatted'].split('.')
    gooddate = wrongdate[2] + "-" + wrongdate[1] + "-" + wrongdate[0]
    table += getElement(gooddate)

    table += getElement(route['gripcolor'])

    if route['type'] == 'Boulder':
        table += getElement("Bould")
        table += getElement("Mats")
    else:
        table += getElement("Sport")
        table += getElement(route['type'])
        
    table += getElement(route['sector'])
    table += getElement(route['statusLabel'])

    if route['children']:
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
