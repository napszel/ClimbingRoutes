#!venv/bin/python

from pprint import pprint
from requests import post

from disqusapi import DisqusAPI
disqus = DisqusAPI("tomRM9FzpoPUBVaTpj9EzJBi7EGtRRJHAK9LWO1LKQxphtyHLRF9Ryq7zrnhWGZc", "g0hQCAzqMrVq2M8DFwpQmnviE22ZSYw4AsuQbRkMTniMD3W5lpIzyvqWEbFNRHt2")
disqus.threads.list(forum='climbingroutes')
