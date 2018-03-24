#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from pprint import pprint
import sqlite3

html = open('../index.html', 'w')

conn = sqlite3.connect('routes.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

html_headers = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>~ Climbing Routes ~</title>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/responsive/2.2.1/js/dataTables.responsive.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/1.5.1/js/dataTables.buttons.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/1.5.1/js/buttons.colVis.min.js"></script>

    <script src="routesarray.js"></script>
    <script src="javascript.js"></script>
    
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.min.css" media="screen"/>
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/responsive/2.2.1/css/responsive.dataTables.min.css" media="screen"/>
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/1.5.1/css/buttons.dataTables.min.css" media="screen"/>
    
    <link rel="stylesheet" type="text/css" href="style.css" media="screen" />
    <link rel="shortcut icon" href="favicon.png" type="image/png"/>
  </head>
  
  <body>
  <div id="route_root" style="display: none">
    <div id="header"></div>
      <div id="wrapper">
        <div id="images">
          <table>
            <tr>
              <td><img id="hold"/></td>
              <td><img id="lead"/></td>
              <td><img id="toprope"/></td>
            </tr>
              <td id="hold_caption"></td>
              <td id="lead_caption"></td>
              <td id="toprope_caption"></td>
            </tr>
          </table>
        </div>
        <div id="details">
          <label id="status" style="display: none"></label><br/>
          <label id="number"></label><br/>
          <label id="name"></label><br/>
          <label id="grade"></label><br/>
          <label id="date_and_setter"></label><br/>
          <label id="kids"></label>
        </div>
      </div>
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
<th title="Field #1" class="twenty">Pl.</th>
<th title="Field #2" class="twenty">#</th>
<th title="Field #3">Route Name</th>
<th title="Field #4" class="twenty">Gr.</th>
<th title="Field #5" class="hundredten">Lates comment</th>
<th title="Field #6" class="twenty">sum</th>
<th title="Field #7">Setter's Name</th>
<th title="Field #8" class="ninety">Date</th>
<th title="Field #9" class="hundredten">Color</th>
<th title="Field #10" class="fourty">Bould / Sport</th>
<th title="Field #11" class="hundredten">Belay</th>
<th title="Field #12">Sector</th>
<th title="Field #13" class="sixty">New / Last Call / Retired</th>
<th title="Field #14" class="twenty">Kids</th>
</tr>
</thead>
<tfoot>
<tr>
<th title="Field #1">Mil/Gas</th>
<th title="Field #2">#</th>
<th title="Field #3">Filer by route name</th>
<th title="Field #4">6a+</th>
<th title="Field #5">Lates comment</th>
<th title="Field #6">no. of comments</th>
<th title="Field #7">Filter by setter's name</th>
<th title="Field #8">Filter by date</th>
<th title="Field #9">Color</th>
<th title="Field #10">Bould/Sport</th>
<th title="Field #11">Toppas/Lead/Toprope</th>
<th title="Field #12">Filter by sector name</th>
<th title="Field #13">New/Last Call/Retired</th>
<th title="Field #14">Kids</th>
</tr>
</tfoot>
<tbody>
"""

def getElement(s):
    return "<td>" + s + "</td>"

for route in c.execute('SELECT routes.*, postcount.posts, postcount.commenter, postcount.latest FROM routes LEFT JOIN postcount ON routes.dat = postcount.dat AND routes.typ = postcount.typ AND routes.place = postcount.place AND routes.rid = postcount.rid ORDER BY dat DESC'):
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

    if route['posts'] == None:
        table += "<td class=\"tiny\"><a href=\"?route-comment=" + route_identifier + "\" target=\"_blank\"> leave a comment</a></td>"
        table += "<td class=\"centered tiny\"><a href=\"?route-comment=" + route_identifier + "\" target=\"_blank\">0</a></td>"
    else:
        commenter = route['commenter']
        latest_comment = route['latest'].split("T")[0] + " " + route['latest'].split("T")[1]
        table += "<td class=\"tiny\"><a href=\"?route-comment=" + route_identifier + "\" target=\"_blank\">" + latest_comment + "<br/>" + commenter + "</a></td>"
        table += "<td class=\"centered tiny\"><a href=\"?route-comment=" + route_identifier + "\" target=\"_blank\">" + str(route['posts']) + "</a></td>"

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
</body>
</html>
"""
html.write(html_end)
html.close
