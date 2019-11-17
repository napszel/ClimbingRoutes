#!venv/bin/python
# -*- coding: utf-8 -*-

import json
from pprint import pprint
import sqlite3
from disqusapi import DisqusAPI, Paginator

all_the_threads = {}

disqus = DisqusAPI("tomRM9FzpoPUBVaTpj9EzJBi7EGtRRJHAK9LWO1LKQxphtyHLRF9Ryq7zrnhWGZc", "g0hQCAzqMrVq2M8DFwpQmnviE22ZSYw4AsuQbRkMTniMD3W5lpIzyvqWEbFNRHt2")
# paginate through ALL THE threads
j = 1
for i in Paginator(disqus.threads.list, limit='100', forum='climbingroutes'):
    print("Caching thread " + str(j))
    j += 1
    all_the_threads[i['id']] = i

conn = sqlite3.connect('../generated/routes.db')

try:
    c = conn.cursor()

    # Get the ID of the last seen post
    get_id = c.execute("SELECT postid FROM lastseenpost")
    last_postid = c.fetchone()[0]
    
    # Ge the list of posts (comments) form Disqus. This returns a list of all posts ordered by date, starting with the most recent.
    posts_list = Paginator(disqus.posts.list, limit='100', forum='climbingroutes', sortType='date', order='asc')

    i = 1
    for post in posts_list:
        print("Handling post " + str(i))
        i += 1
        latest = post['createdAt']
        commenter = post['author']['name']

        # get the thread of the comment
        thread = all_the_threads[post['thread']]

        thread_posts_count = thread['posts']
        thread_link = thread['link']
        threadid = thread['id']

        route_id_start = thread_link.find("route-comment=") + 14
        route_id = thread_link[route_id_start:].split('&')[0]
        route_id_parts = route_id.split(':')
        dat = route_id_parts[0]
        typ = route_id_parts[1]
        place = route_id_parts[2]
        rid = route_id_parts[3]
        
        next_post_to_insert = [(dat, typ, place, rid, threadid, thread_posts_count, latest, commenter)]
        c.executemany("INSERT OR REPLACE INTO postcount VALUES (?,?,?,?,?,?,?,?)", next_post_to_insert)

    conn.commit()
except conn.Error:
    print("Transaction failed! ROLLBACK")
    conn.rollback()
    
conn.close()

