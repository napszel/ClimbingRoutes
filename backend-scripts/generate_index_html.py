#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from pprint import pprint
import sqlite3

html = open('../index.html', 'w')

conn = sqlite3.connect('routes.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
}

break_characters = "- "

# Escape HTML characters
def html_escape(text):
    return "".join(html_escape_table.get(c, c) for c in text)

# Add break points so super long words doesn't mess up the UI
def html_escape_and_add_break_points(text):
    super_long_word = 24
    bits = []
    chars = ""
    for i in range(0, len(text)):
        if text[i] in break_characters:
            if chars:
                bits += [(chars, False)]
                chars = ""
            bits += [(text[i], False)]
        else:
            chars += text[i]
            if len(chars) > super_long_word:
                bits += [(chars, True)]
                chars = ""

    if chars:
        bits += [(chars, False)]

    result = ""

    for bit in bits:
        result += html_escape(bit[0])
        if bit[1]:
            result += "&#8203;"

    return result


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
          <table id="images_table">
            <tr>
              <td><img id="lead"/></td>
              <td><img id="toprope"/></td>
              <td><img id="hold"/></td>
            </tr>
              <td id="lead_caption"></td>
              <td id="toprope_caption"></td>
              <td id="hold_caption"></td>
            </tr>
          </table>
        </div>
        <div id="details">
          <label id="status" style="display: none"></label><br/>
          <label id="number"></label><br/>
          <label id="name"></label><br/>
          <label id="grade"></label><br/>
          <label id="date_and_setter"></label><br/>
          <label id="kids"></label><br/>
        </div>
      </div>
      <div id="map_sector">
         <label id="sector"></label>
         <a id="map_link" target="_blank"><img id="map"></a>
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
<table id="example" class="compact stripe row-border" cellspacing="0" width="100%">
<thead>
<tr>
<th title="pl" class="twenty">Pl.</th>
<th title="no" class="twenty">#</th>
<th title="name" class="twohundred">Route</th>
<th title="gr" class="twenty">Gr.</th>
<th title="setter">Setter</th>
<th title="date" class="ninety">Setting&nbsp;Date</th>
<th title="color" class="hundredten">Color</th>
<th title="type" class="fourty">Bould/ Sport</th>
<th title="belay" class="hundredten">Belay</th>
<th title="sector" class="twohundred">Sector</th>
<th title="new" class="sixty">New/Last Call</th>
<th title="status" class="sixty">Active/ Retired</th>
<th title="kids" class="twenty">Kids</th>
<th title="comment" class="hundredten">Latest Comment</th>
<th title="sum" class="twenty">All</th>
</tr>
</thead>
<tfoot>
<tr>
<th title="pl" placeholder="Mil/Gas" />
<th title="no" placeholder="#" />
<th title="name" placeholder="Filer by route name" />
<th title="gr" placeholder="6a+" />
<th title="setter" placeholder="Filter by route setter" />
<th title="date" placeholder="Filter by date" />
<th title="color" placeholder="Color" />
<th title="type" placeholder="Bould/Sport" />
<th title="belay" placeholder="Toppas/Lead/Toprope" />
<th title="sector" placeholder="Filter by sector name" />
<th title="new" placeholder="New/Last Call"/>
<th title="status" placeholder="Active/Retired" default="Active"/>
<th title="kids" placeholder="Kids" />
<th title="comment" placeholder="Latest comment" />
<th title="sum" placeholder="no. of comm." />
</tr>
</tfoot>
<tbody>
"""

def getElement(s):
    return "<td>" + s + "</td>"

for route in c.execute('SELECT routes.*, postcount.posts, postcount.commenter, postcount.latest FROM routes LEFT JOIN postcount ON routes.dat = postcount.dat AND routes.typ = postcount.typ AND routes.place = postcount.place AND routes.rid = postcount.rid WHERE retired=0 ORDER BY dat DESC'):
    table += "<tr>"

    place = route['place']
    table += getElement(place.capitalize())

    route_number = str(route['rid'])
    table += getElement(route_number)

    route_type = route['typ']
    date = route['dat']

    route_identifier = date + ":" + route_type + ":" + place + ":" + route_number

    table += "<td><a href=\"?route-comment=" + route_identifier + "\" >" + html_escape_and_add_break_points(route['name'])
    if route['subname']:
        table += " (" + route['subname'] + ")"
    table += "</a></td>"

    table += getElement(route['grade'])

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

    if route['new_'] or route['lastcall']:
        if route['new_']:
            table += getElement("New")
        if route['lastcall']:
            table += getElement("Last Call")
    else:
        table += getElement("")

    if route['retired']:
        table += getElement("Retired")
    else:
        table += getElement("Active")
    
    if route['kids']:
        table += "<td class=\"centered\">Y</td>"
    else:
        table += "<td class=\"centered\">N</td>"

    if route['posts'] == None:
        table += "<td class=\"tiny\"><a href=\"?route-comment=" + route_identifier + "\" > leave a comment</a></td>"
        table += "<td class=\"centered tiny\"><a href=\"?route-comment=" + route_identifier + "\" >0</a></td>"
    else:
        splcommenter = route['commenter'].split(" ")
        commenter = " ".join(splcommenter[0:1])
        latest_comment = route['latest'].split("T")[0]
        table += "<td class=\"tiny\"><a href=\"?route-comment=" + route_identifier + "\" >" + latest_comment + "<br/>" + commenter + "</a></td>"
        table += "<td class=\"centered tiny\"><a href=\"?route-comment=" + route_identifier + "\" >" + str(route['posts']) + "</a></td>"

    table += "</tr>"
    

table += """
</tbody>
</table>"""
html.write(table)

html_end = """
<div id="credits">
<a class=\"underline\" href="https://github.com/napszel/ClimbingRoutes" target="_blank" rel="noopener noreferrer">Napszel</a>, 2018
</div>
</div>
</body>
</html>
"""
html.write(html_end)
html.close
