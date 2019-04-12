#!/usr/bin/python

# -*- coding: utf-8 -*-

import json
from pprint import pprint
import sqlite3

html = open('../beta.html', 'w')

conn = sqlite3.connect('../generated/routes.db')
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

# Add break points so super long words don't mess up the UI
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

    <script src="generated/routesarray-beta.js"></script>
    <script src="javascript-beta.js"></script>
    
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.min.css" media="screen"/>
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/responsive/2.2.1/css/responsive.dataTables.min.css" media="screen"/>
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/1.5.1/css/buttons.dataTables.min.css" media="screen"/>
    
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.3.1/css/solid.css" integrity="sha384-VGP9aw4WtGH/uPAOseYxZ+Vz/vaTb1ehm1bwx92Fm8dTrE+3boLfF1SpAtB1z7HW" crossorigin="anonymous">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.3.1/css/fontawesome.css" integrity="sha384-1rquJLNOM3ijoueaaeS5m+McXPJCGdr5HcA03/VHXxcp2kX2sUrQDmFc3jR5i/C7" crossorigin="anonymous">

    <link rel="stylesheet" type="text/css" href="style-beta.css" media="screen" />
    <link rel="shortcut icon" href="images/favicon.png" type="image/png"/>
  </head>
  
  <body>
   <script>
    function goBack() {
      window.history.back(); 
    }
   </script>

  <div id="route_root" style="display: none">
    <div class="flex header shadowbox">
      <button onclick="goBack()" class="back_button"><img src="images/back.png"/></button>
      <div id="title-div"></div>
      <a href="profile.html"><i class="fas fa-user"></i></a>
    </div>
    <hr/>

    <div id="wrapper" class="shadowbox">
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
          <label id="heart" class="opinion faded" title="I like this route"><i class="fas fa-heart"></i></label>
          <label id="hard" class="opinion faded" title="Too hard for this grade"><i class="fas fa-cogs"></i></label>
          <label id="easy" class="opinion faded" title="Too easy for this grade"><i class="fas fa-feather-alt"></i></label>

          <label id="status" style="display: none"></label><br/>
          <label id="number"></label><br/>
          <label id="name"></label><br/>
          <label><span id="grade" class="table-grade"></span></label><br/>
          <label id="date_and_setter"></label><br/>
          <a href="#map_sector"><label id="sector-link"></label></a><br/>
          <label id="kids"></label><br/>
       </div>
    </div>
    <div id="results" class="shadowbox">
        <label id="your-results">Your latest result</label>
        <form id="results-form">
        <label class="result-button"><i class="fas fa-eye"></i> On-sighted</label>
        <label class="result-button"><i class="fas fa-bolt"></i> Flashed</label>
        <label class="result-button"><i class="fas fa-dot-circle"></i> Red-pointed</label>
        <label id="attempt-button" class="result-button"><i class="fas fa-sort-numeric-up"></i> Attempted</label>

         <input type="radio" name="attempts" id="attempt1" class="radio"><label for="attempt1">1 stop</label>
         <input type="radio" name="attempts" id="attempt2" class="radio"><label for="attempt2">2 stops</label>
         <input type="radio" name="attempts" id="attempt3" class="radio"><label for="attempt3">2 stops</label>
         <input type="radio" name="attempts" id="gaveup" class="radio"><label for="gaveup">Gave up</label>

        <label class="result-button"><i class="fas fa-project-diagram"></i> Toproped</label>

        </form>

        <div class="plotly">
          <iframe width="500" height="250" frameborder="0" scrolling="no" src="//plot.ly/~napszel/1.embed?showlink=false"></iframe>
        </div>
    </div>

    <div id="disqus_thread" class="shadowbox"></div>
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

    <hr/>
    <div id="map_sector" class="shadowbox">
       <label id="sector"></label>
       <a id="map_link" target="_blank"><img id="map"></a>
    </div>
  </div>

  <div id="main_table" style="display: none">
    <div class="header">
      <label class="title">Climbing Routes of <a class=\"underline\" href="http://www.kletterzentrum.com/unser-angebot/kletterzentrum-gaswerk/">Gaswerk</a> and <a class=\"underline\" href="http://www.kletterzentrum.com/unser-angebot/kletterzentrum-milandia/">Milandia</a></label>
    </div>
    <hr/>
    <div id="quick-buttons">
      <div id="map-buttons">
        <input type="button" class="button" id="gaswerk_map" value="Map of Gaswerk Routes" onclick="window.location.assign('gaswerk-map/gaswerk-leads/gaswerk_beta_map.html');" />
        <input type="button" class="button" id="gaswerk_boulders" value="Map of Gaswerk Boulders" onclick="window.location.assign('gaswerk-map/gaswerk-boulders/gaswerk_beta_boulder_map.html');" />
        <input type="button" class="button" id="milandia_map" value="Map of Milandia Routes" onclick="window.location.assign('milandia-map/milandia-leads/milandia_beta_map.html')" />
        <input type="button" class="button" id="milandia_boulders" value="Map of Milandia Boulders" onclick="window.location.assign('milandia-map/milandia-boulders/milandia_beta_boulder_map.html')" />
      </div>
      <div id="quick-filter">
        <label class="quick-filter">Quick Filters:</label>
        <input type="button" class="button" id="mil" value="Milandia" onclick="applyFilter('Mil', '#pl-filter')" />
        <input type="button" class="button" id="gas" value="Gaswerk" onclick="applyFilter('Gas', '#pl-filter')" />
        <label class="quick-filter">|</label>
        <input type="button" class="button" id="sport" value="Sport" onclick="applyFilter('Sport', '#type-filter')" />
        <input type="button" class="button" id="bould" value="Boulder" onclick="applyFilter('Bould', '#type-filter')" />
        <label class="quick-filter">|</label>
        <input type="button" class="grade-button blue" id="5c" value="5c" onclick="applyFilter('5c', '#gr-filter')" />
        <input type="button" class="grade-button blue" id="6a" value="6a" onclick="applyFilter('6a', '#gr-filter')" />
        <input type="button" class="grade-button blue" id="6aplus" value="6a+" onclick="applyFilter('6a\\\+', '#gr-filter')" />
        <input type="button" class="grade-button blue" id="6b" value="6b" onclick="applyFilter('6b', '#gr-filter')" />
        <input type="button" class="grade-button blue" id="6bplus" value="6b+" onclick="applyFilter('6b\\\+', '#gr-filter')" />
        <input type="button" class="grade-button red" id="6c" value="6c" onclick="applyFilter('6c', '#gr-filter')" />
        <label class="quick-filter">|</label>
        <input type="button" class="grade-button yellow" id="B1" value="B1" onclick="applyFilter('B1', '#gr-filter')" />
        <input type="button" class="grade-button yellow" id="B1plus" value="B1+" onclick="applyFilter('B1\\\+', '#gr-filter')" />
        <input type="button" class="grade-button green" id="B2" value="B2" onclick="applyFilter('B2', '#gr-filter')" />
        <input type="button" class="grade-button green" id="B2plus" value="B2+" onclick="applyFilter('B2\\\+', '#gr-filter')" />
        <input type="button" class="grade-button blue" id="B3" value="B3" onclick="applyFilter('B3', '#gr-filter')" />
        <input type="button" class="grade-button blue" id="B3plus" value="B3+" onclick="applyFilter('B3\\\+', '#gr-filter')" />
      </div>
    </div>

"""

html.write(html_headers)

table = """
<table id="example" class="stripe row-border" cellspacing="0" width="100%">
<thead>
<tr>
<th title="Place - Gaswerk or Milandia" class="twenty">Pl.</th>
<th title="Route number" class="twenty">#</th>
<th title="Route name" class="twohundred">Route</th>
<th title="Grade" class="twenty">Gr.</th>
<th title="Setter name">Setter</th>
<th title="Setting date" class="ninety">Setting&nbsp;Date</th>
<th title="Route color" class="hundredten">Color</th>
<th title="Type - Boulder or Sport" class="fourty">Bould/ Sport</th>
<th title="Belay type - Toprope, Lead, Toppas" class="hundredten">Belay</th>
<th title="Sector" class="twohundred">Sector</th>
<th title="New or Last call" class="sixty">New/Last Call</th>
<th title="Status - Active or Retired" class="sixty">Active/ Retired</th>
<th title="For kids" class="twenty">Kids</th>
<th title="Latest comment" class="hundredten">Latest Comment</th>
<th title="Sum of all comments" class="twenty">All</th>
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
<th title="status" placeholder="Active/Retired"/>
<th title="kids" placeholder="Kids" />
<th title="comment" placeholder="Latest comment" />
<th title="sum" placeholder="no. of comm." />
</tr>
</tfoot>
<tbody>
"""

def getColorFromGrade(grade, type):
    if type == "sport":
        no = int(grade[0:1])
        l = grade[1:2]
        if (no < 5):
            return "yellow";
        if (no == 5):
            if (l == "c"):
                return "blue";
            else:
                return "yellow";
        if (no == 6):
            if (l == "c"):
                return "red";
            else:
                return "blue";
        if (no == 7):
            if (l == "c"):
                return "black";
            else:
                return "red";
        if (no > 7):
            return "black"
    else:
        no = int(grade[1:2]);
        if no <= 1:
            return "yellow";
        if no == 2:
            return "green";
        if no == 3:
            return "blue";
        if no == 4:
            return "red";
        if no >= 5:
            return "black";

def getElement(s):
    return "<td>" + s + "</td>"

for route in c.execute('SELECT routes.*, postcount.posts, postcount.commenter, postcount.latest FROM routes LEFT JOIN postcount ON routes.dat = postcount.dat AND routes.typ = postcount.typ AND routes.place = postcount.place AND routes.rid = postcount.rid ORDER BY dat DESC'):
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

    color = getColorFromGrade(route['grade'], route['typ'])
    table += "<td><span class=\"table-grade " + color + "\">" + route['grade'] + "</span></td>"

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
        table += getElement("Kids")
    else:
        table += getElement("")

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
<a class=\"underline\" href="https://github.com/napszel/ClimbingRoutes" target="_blank" rel="noopener noreferrer">Napszel</a>, 2019
</div>
</div>
</body>
</html>
"""
html.write(html_end)
html.close
