# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 19:12:15 2018

@author: Aleksi Roima
"""

import feedparser
import psycopg2
import credentials as cre
from time import gmtime, strftime

rss_url = 'https://feeds.yle.fi/uutiset/v1/majorHeadlines/YLE_UUTISET.rss'
feed = feedparser.parse(rss_url)

time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())


headline_list = [ [feed['entries'][0]['title'], time_now] 
                , [feed['entries'][1]['title'], time_now]
                , [feed['entries'][2]['title'], time_now]
                , [feed['entries'][3]['title'], time_now]
                , [feed['entries'][4]['title'], time_now]
                ]

# Add data to database
try:
    conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (cre.dbname, cre.user, cre.host, cre.password))
    cur = conn.cursor()
    sql = 'INSERT INTO dashboard_headlinetable(headline, loadtime) VALUES (%s, %s);'
    cur.executemany(sql, headline_list)
    conn.commit()
    cur.close()
except(Exception, psycopg2.DatabaseError) as error:
    print(error)