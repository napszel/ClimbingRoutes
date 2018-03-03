# Climbing Routes of Gaswerk and Milandia Climbing Centers

http://napszel.com/climbingroutes

This website displays a list of all climbing routes of Milandia and Gaswerk climbing centers of Zurich, Switzerland. 

The data is taken from their official website: http://www.kletterzentrum.com/routenfinder/.

The displayed table is searchabe (for all fields) and filterable/sortable for each column.

## The code

It uses DataTable, a table plug-in for jQuery (https://datatables.net/)

A bash scripts downloads the data from the kletterzentrum's website and saves the data to an sqlite3 db. Then a python script generates the index.html file based on the db. (Hence, index.html is not included in git)


