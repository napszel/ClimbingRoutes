# Climbing Routes of Gaswerk and Milandia Climbing Centers

http://napszel.com/climbingroutes

The project ‘Climbing Routes’ is a web application that displays up to date information of the currently available boulder and sport routes at Gaswerk and Milandia climbing gyms of Zürich, Switzerland.

Data is downloaded from the official websites (http://www.kletterzentrum.com/routenfinder/) and updated automatically once a day.

The displayed table is searchabe (for all fields) and filterable/sortable for each column.

You can ready about each feature in the [project's pdf documentation](climbing-routes-documentation.pdf).

## The code

It uses DataTable, a table plug-in for jQuery (https://datatables.net/)

A bash scripts downloads the data from the kletterzentrum's website and saves the data to an sqlite3 db. Then a python script generates the index.html file based on the db. (Hence, index.html is not included in git)


