#!venv/bin/python

from requests import get
import sys
from disqusapi import DisqusAPI
import json

disqus = DisqusAPI("tomRM9FzpoPUBVaTpj9EzJBi7EGtRRJHAK9LWO1LKQxphtyHLRF9Ryq7zrnhWGZc", "g0hQCAzqMrVq2M8DFwpQmnviE22ZSYw4AsuQbRkMTniMD3W5lpIzyvqWEbFNRHt2")

if (sys.argv[1] == 'all'):
    r = get("https://disqus.com/api/3.0/posts/list.json?access_token=195f3a87b41a4996ba83fd3941c231ec&api_key=g0hQCAzqMrVq2M8DFwpQmnviE22ZSYw4AsuQbRkMTniMD3W5lpIzyvqWEbFNRHt2&api_secret=tomRM9FzpoPUBVaTpj9EzJBi7EGtRRJHAK9LWO1LKQxphtyHLRF9Ryq7zrnhWGZc&forum=" + "climbingroutes")
else:
    r = get("https://disqus.com/api/3.0/posts/details.json?access_token=195f3a87b41a4996ba83fd3941c231ec&api_key=g0hQCAzqMrVq2M8DFwpQmnviE22ZSYw4AsuQbRkMTniMD3W5lpIzyvqWEbFNRHt2&api_secret=tomRM9FzpoPUBVaTpj9EzJBi7EGtRRJHAK9LWO1LKQxphtyHLRF9Ryq7zrnhWGZc&post=" + str(sys.argv[1]))

print(json.dumps(r.json(), indent=2))
