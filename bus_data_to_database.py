# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 18:18:58 2018

@author: Aleksi Roima
"""

import credentials as cre


import requests
import json
import psycopg2
from datetime import date, datetime
from operator import itemgetter
from time import gmtime, strftime, sleep


# Get data and create list which includes tuples that have busline and arrival time to the bus stop
def get_busses(url, arrivals):
    right_busses = [["3A", "3B", "4", "6"], ["3723", "3577", "3737"]]
    response = requests.get(url)
    if (response.ok):
        json_data = json.loads(response.content)
        for bus in json_data[0]['departures']:
            if (bus['direction'] == "1"):
                if (((json_data[0]['code'] == right_busses[1][0]) and ((bus['code'] == right_busses[0][0]) or (bus['code'] == right_busses[0][1])))
                or ((json_data[0]['code'] == right_busses[1][1]) and (bus['code'] == right_busses[0][2]))
                or ((json_data[0]['code'] == right_busses[1][2]) and (bus['code'] == right_busses[0][3]))):
                    arrivals.append([bus['code'], bus['time']])
    
# What's the longest time that we will want to see the busses arrival
timelimit = "100"
# The needed API urls to get the data
urls = [ 'http://api.publictransport.tampere.fi/prod/?request=stop&user=%s&pass=%s&code=3723&format=json&dep_limit=20&time_limit=%s' % (cre.username, cre.passphrase, timelimit)
        , 'http://api.publictransport.tampere.fi/prod/?request=stop&user=%s&pass=%s&code=3577&format=json&dep_limit=20&time_limit=%s' % (cre.username, cre.passphrase, timelimit)
        , 'http://api.publictransport.tampere.fi/prod/?request=stop&user=%s&pass=%s&code=3737&format=json&dep_limit=20&time_limit=%s' % (cre.username, cre.passphrase, timelimit)]


arrivals = []
for url in urls:
    get_busses(url, arrivals)
    
# Karsitaan jäljellä vain bussit, jotka lähtevät 5 min - 100 min päästä:

for bus in arrivals:
    # The clock doesnt continue until 26 like the data sais
    if (bus[1][0:2] == "24"):
        bus[1] = bus[1].replace("24", "00", 1)
    elif (bus[1][0:2] == "25"):
        bus[1] = bus[1].replace("25", "01", 1)
    elif (bus[1][0:2] == "26"):
        bus[1] = bus[1].replace("26", "02", 1)
    bus[1] = int((datetime.combine(date.min, datetime.strptime(bus[1], '%H%M').time()) - datetime.combine(date.min, datetime.now().time())).total_seconds() / 60)
    # Bug that will occur during midnight. Quickfix, not a good one
    if bus[1] < -1000:
        bus[1] = 6

# Sort by arrival time
arrivals = sorted(arrivals, key=itemgetter(1))
deletables = []
i = 0
while i != -1:
    # Don't show busses that arrive too fast and we don't have time to walk for
    if arrivals[i][1] < 3:
        deletables.append(i)
        i += 1
    else:
        i = -1
for i in sorted(deletables, reverse=True):
    arrivals.pop(i)

#Print information about useful busses            
for bus in arrivals:
    print("Bus", bus[0], "will arrive to stop after", bus[1], "minutes")

# Edit the data in such form that it will be easily written to the table, also add time of upload
values_list = []
time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
minutes = []
busses = []
for row in arrivals:
    values_list.append((row[0], str(row[1]), time_now))


# Add data to database
try:
    conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (cre.dbname, cre.user, cre.host, cre.password))
    cur = conn.cursor()
    sql = 'INSERT INTO bus_schedule_table(line, time, loadtime) VALUES (%s, %s, %s)'
    cur.executemany(sql, values_list)
    conn.commit()
    cur.close()
except(Exception, psycopg2.DatabaseError) as error:
    print(error)

            
