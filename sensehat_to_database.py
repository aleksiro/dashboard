# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 09:06:55 2018

@author: Aleksi Roima
"""
import psycopg2
import credentials as cre
#from sense_hat import SenseHat
from time import gmtime, strftime, sleep

time_now = strftime("%Y-%m-%d%H:%M:%S", gmtime())

#sense = SenseHat()

while True:

    try:
        loadtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        
# =============================================================================
#         valuelist = []
#         for i in range (0, 6):
#             valuelist.append(sense.temperature(), sense.humidity(), strftime("%H:%M:%S", gmtime(), ))
#             sleep(10)
#             i += 1
#         
# =============================================================================
        conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (cre.dbname, cre.user, cre.host, cre.password))
        
        cur = conn.cursor()
        
        loadtime = strftime("%m-%d %H:%M:%S", gmtime())
        valuelist = [[25.5, 64.1, "10:10:00", loadtime], [24.9, 65.1, "10:10:10", loadtime], [24.0, 65.6, "10:10:20", loadtime],
                     [23.8, 65.3, "10:10:30", loadtime], [23.6, 65.0, "10:10:40", loadtime], [23.5, 65.2, "10:10:50", loadtime]]
        
        sql = 'INSERT INTO sense_hat_table(temperature, humidity, measuretime, loadtime) VALUES (%s, %s, %s, %s)'
        cur.executemany(sql, valuelist)
        conn.commit()
        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    sleep(10)
    print('meni')
    