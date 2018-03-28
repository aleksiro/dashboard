# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 19:56:36 2018

@author: Aleksi Roima
"""

import credentials as cre

import requests
import json
import psycopg2
from datetime import datetime
from time import gmtime, strftime

# Weather at the moment
lat = '61.4528'
lon = '23.8416'
time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())

# Get weather information from asked moment
url_now = 'http://api.weatherbit.io/v2.0/current?key=%s&lang=fi&lat=%s&lon=%s' % (cre.weather_api_key, lat, lon)
response = requests.get(url_now)
if (response.ok):
    json_data = json.loads(response.content)
    json_data = json_data['data'][0]
    weather_now = [ json_data['temp']
                    , json_data['app_temp']
                    , json_data['weather']['icon']
                    , json_data['weather']['description'] 
                    , 'Nyt'
                    , time_now]



# Get weather forecast 3 hours from now, tomorrow and day after tomorrow
url_forecast = 'http://api.weatherbit.io/v2.0/forecast/hourly?key=%s&lang=fi&lat=%s&lon=%s' % (cre.weather_api_key, lat, lon)
# Count the hour three hours from now 
wanted_near_forecast =  str(int(datetime.now().hour) + 3)
if (wanted_near_forecast == '24'):
    wanted_near_forecast = '00'
elif (wanted_near_forecast == '25'):
    wanted_near_forecast = '01'
elif (wanted_near_forecast == '26'):
    wanted_near_forecast = '02'
elif (wanted_near_forecast == '27'):
    wanted_near_forecast = '03'

response = requests.get(url_forecast)
if (response.ok):
    json_forecast_data = json.loads(response.content)
    iteration = 0
    i = 0
    for row in json_forecast_data['data']:
        iteration += 1
        if (row['datetime'].split(':')[1] == wanted_near_forecast):
            three_hour_forecast = [row['temp'], row['app_temp'], row['weather']['icon'], row['weather']['description'], '3h kuluttua', time_now]
            i += 1
        elif ((row['datetime'].split(':')[1] == '12') and (i == 1)):
            tomorrow_forecast = [row['temp'], row['app_temp'], row['weather']['icon'], row['weather']['description'], 'Huomenna', time_now]
            i += 1
        elif (((row['datetime'].split(':')[1] == '12') and (i == 2)) or (iteration == len(json_forecast_data['data']))):
            day_after_tomorrow_forecast = [row['temp'], row['app_temp'], row['weather']['icon'], row['weather']['description'], 'Ylihuomenna', time_now]
            i += 1


# Add data to database
try:
    conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (cre.dbname, cre.user, cre.host, cre.password))
    cur = conn.cursor()
    sql = 'INSERT INTO weather_table(temperature, rf_temperature, icon_code, weather_type, forecast_type, loadtime) VALUES (%s, %s, %s, %s, %s, %s)'
    cur.executemany(sql, [weather_now, three_hour_forecast, tomorrow_forecast, day_after_tomorrow_forecast])
    conn.commit()
    cur.close()
except(Exception, psycopg2.DatabaseError) as error:
    print(error)
            
