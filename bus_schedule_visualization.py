# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 22:06:27 2018

@author: Aleksi Roima
"""


import credentials as cre
import psycopg2

# Wanted columns for the visualization
busses = []
times = []
# Get data from database
try:
    conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (cre.dbname, cre.user, cre.host, cre.password))
    cur = conn.cursor()
    cur.execute('SELECT * FROM busscheduletable')
    for row in cur:
        busses.append(row[0])
        times.append(row[1])
    cur.close()
except(Exception, psycopg2.DatabaseError) as error:
    print(error)




import plotly
import plotly.graph_objs as go


plotly.tools.set_credentials_file(username=cre.py_username, api_key=cre.py_api_key)
plotly.tools.set_config_file(world_readable=True,
                             sharing='public')

# Add alternative row colors to the table
def return_row_color(i):
    if (i % 2 == 0):
        return 'B9E5F3'
    else: 
        return 'D0EEF7'
    
import plotly.plotly as py
headerColor = '456A76'
cell_color_list = []
i = 0
while i < len(busses):
    cell_color_list.append(return_row_color(i))
    i += 1

# Create table
trace = go.Table(
    header=dict(values=['Bussi', 'Saapumiseen (min)'],
                line = dict(color='#7D7F80'),
                fill = dict(color=headerColor),
                align = ['center'],
                font = dict(color='white', size=14)),
    cells=dict(values=[busses, times],
               line = dict(color='white'),
               fill = dict(color=[cell_color_list]),
               align = ['center'],
               font = dict(color='333333', size=12)))
                
layout = dict(width=480, height=500)
data = [trace]
fig = dict(data=data, layout=layout)
py.iplot(fig, filename='bussitesti')