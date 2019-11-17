#!venv/bin/python
# -*- coding: utf-8 -*-

import json
from pprint import pprint
import sqlite3
from disqusapi import DisqusAPI

conn = sqlite3.connect('../generated/routes.db')

try:
    c = conn.cursor()

    disqus = DisqusAPI("tomRM9FzpoPUBVaTpj9EzJBi7EGtRRJHAK9LWO1LKQxphtyHLRF9Ryq7zrnhWGZc", "g0hQCAzqMrVq2M8DFwpQmnviE22ZSYw4AsuQbRkMTniMD3W5lpIzyvqWEbFNRHt2")
    all_post_states = ['deleted', 'approved', 'unapproved', 'spam', 'flagged', 'highlighted']
    posts_list = disqus.posts.list(forum='climbingroutes', include=all_post_states, sortType='date', order='desc', limit='100')

    post = posts_list[-1]
    threads = disqus.threads.list(thread=post['thread'])
    thread = threads[0]
    thread_posts_count = thread['posts']
    thread_link = thread['link']
    threadid = thread['id']
    latest = post['createdAt']
    commenter = post['author']['name']

    route_id_start = thread_link.find("route-comment=") + 14
    route_id = thread_link[route_id_start:].split('&')[0]
    route_id_parts = route_id.split(':')
    dat = route_id_parts[0]
    typ = route_id_parts[1]
    place = route_id_parts[2]
    rid = route_id_parts[3]
    
    post_to_insert = [(dat, typ, place, rid, threadid, thread_posts_count, latest, commenter)]
    c.executemany("INSERT OR REPLACE INTO postcount VALUES (?,?,?,?,?,?,?,?)", post_to_insert)

    last_post_to_insert = (str(post['id']), )
    c.execute("DELETE FROM lastseenpost")
    c.execute("INSERT INTO lastseenpost VALUES(?)", last_post_to_insert)

    conn.commit()
except conn.Error:
    print("Transaction failed! ROLLBACK")
    conn.rollback()
    
conn.close()

