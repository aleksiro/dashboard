# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 21:40:06 2018

@author: Aleksi Roima
"""

import credentials as cre

import psycopg2
import plotly
import plotly.plotly as py
import plotly.dashboard_objs as dashboard


# Wanted columns for the visualization
try:
    conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (cre.dbname, cre.user, cre.host, cre.password))
    cur = conn.cursor()
    sql = """ SELECT temperature, rf_temperature, icon_code
            FROM weathertable
            WHERE loadtime = (SELECT MAX(loadtime)
                              FROM weathertable)
    """
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
except(Exception, psycopg2.DatabaseError) as error:
    print(error)


my_dboard = dashboard.Dashboard()
plotly.tools.set_credentials_file(username=cre.py_username, api_key=cre.py_api_key)
plotly.tools.set_config_file(world_readable=True,
                             sharing='public')

text = """
# Nyt %s°C #
## Tuntuu kuin %s °C ##
![alt text](https://www.weatherbit.io/static/img/icons/%s.png)

# Kolmen tunnin kuluttua %s°C #
## Tuntuu kuin %s °C ##
![alt text](https://www.weatherbit.io/static/img/icons/%s.png)

# Huomenna %s°C #
## Tuntuu kuin %s °C ##
![alt text](https://www.weatherbit.io/static/img/icons/%s.png)

# Ylihuomenna %s°C #
## Tuntuu kuin %s °C ##
![alt text](https://www.weatherbit.io/static/img/icons/%s.png)
 
""" % (result[0][0], result[0][1], result[0][2]
        , result[1][0], result[1][1], result[1][2]
        , result[2][0], result[2][1], result[2][2]
        , result[3][0], result[3][1], result[3][2]
        )



box_l_u = {
    'type': 'box',
    'boxType': 'text',
    'text': text,
    'title': 'Säätila ja -ennuste'
}


my_dboard.insert(box_l_u, 0)
py.dashboard_ops.upload(my_dboard, 'dassikkatesti')
