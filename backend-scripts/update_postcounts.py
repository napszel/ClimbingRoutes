#!venv/bin/python
# -*- coding: utf-8 -*-

import json
from pprint import pprint
import sqlite3
from disqusapi import DisqusAPI

conn = sqlite3.connect('routes.db')

try:
    c = conn.cursor()

    # Get the ID of the last seen post
    get_id = c.execute("SELECT postid FROM lastseenpost")
    last_postid = c.fetchone()[0]

    # Ge the list of posts (comments) form Disqus. This returns a list of all posts ordered by date, starting with the most recent.
    disqus = DisqusAPI("tomRM9FzpoPUBVaTpj9EzJBi7EGtRRJHAK9LWO1LKQxphtyHLRF9Ryq7zrnhWGZc", "g0hQCAzqMrVq2M8DFwpQmnviE22ZSYw4AsuQbRkMTniMD3W5lpIzyvqWEbFNRHt2")
    posts_list = disqus.posts.list(forum='climbingroutes')

    # Find the first post that we haven't seen yet.
    i_not_seen_post = 0
    for post in posts_list:
        if post['id'] == last_postid:
            break
        i_not_seen_post += 1

    # If the list doesn't contain our last seen post then we have a problem.
    if i_not_seen_post == len(posts_list):
        print("ERROR! Haven't seen any of these posts.")
        exit(1)

    if i_not_seen_post == 0:
        print("Nothing to do. We've seen all of these posts.")
        exit(0)

    # Update our post counts DB table
    list_not_seen_posts = posts_list[0:i_not_seen_post]
    for post in list_not_seen_posts:
        thread = disqus.threads.list(thread=post['thread'])[0]
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
        
        next_post_to_insert = [(dat, typ, place, rid, threadid, thread_posts_count)]
        c.executemany("INSERT OR REPLACE INTO postcount VALUES (?,?,?,?,?,?)", next_post_to_insert)

    # Update our last seen post DB table
    last_post_to_insert = (str(list_not_seen_posts[0]['id']), )
    c.execute("UPDATE lastseenpost SET postid=?", last_post_to_insert)

    conn.commit()
except conn.Error:
    print("Transaction failed! ROLLBACK")
    conn.rollback()
    
conn.close()

