#!venv/bin/python

from requests import get
import sys
from disqusapi import DisqusAPI
import pprint

pp = pprint.PrettyPrinter(indent=3)

disqus = DisqusAPI("tomRM9FzpoPUBVaTpj9EzJBi7EGtRRJHAK9LWO1LKQxphtyHLRF9Ryq7zrnhWGZc", "g0hQCAzqMrVq2M8DFwpQmnviE22ZSYw4AsuQbRkMTniMD3W5lpIzyvqWEbFNRHt2")

if (sys.argv[1] == 'all'):
    i = 0
    for post in disqus.posts.list(forum='climbingroutes', sortType='date', order='desc'):
        print("Post " + str(i) + " ==========================================>")
        i = i + 1
        pp.pprint(post)
else:
    post = disqus.posts.details(post=sys.argv[1])
    pp.pprint(post)
