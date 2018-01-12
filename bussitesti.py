# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 18:18:58 2018

@author: Aleksi Roima
"""

"""
Vehicle acitivity: Ajoneuvokohtaiset tiedot, milloin milläkin pysäkillä
TARVITAAN: lineRef, directionRef
Linjat ja niiltä katseltavat pysäkit
3, Orivedenkatu, 3723, 12
directionRef = 1:
4, Opiskelijankatu 23, 3577, ?
directionRef = 1
6, Tieteenkatu 7, 3737, 7
directionRef = 1

"""
# linjat, pysäkit, pysäkkijärjestynro
wanted_stops = "3723,3577,3737"


# Haetaan data
import requests
import json
from datetime import datetime, timedelta

# =============================================================================
# act_url = 'http://data.itsfactory.fi/journeys/api/1/vehicle-activity'
# 
# act_response = requests.get(act_url)
# look_list = []
# if (act_response.ok):
#     act_json = json.loads(act_response.content)
#     for line in act_json['body']:
#         bus_line = line['monitoredVehicleJourney']
#         if ((bus_line['lineRef'] in wanted[0]) and (bus_line['directionRef'] == "1")):
#             print("Tuli1")
#             for stop in bus_line['onwardCalls']:
#                 if (((bus_line['lineRef'] == wanted[0][0]) and (wanted[1][0] in stop['stopPointRef']))
#                     #or ((bus_line['lineRef'] == wanted[0][1]) and (wanted[1][1] in stop['stopPointRef']))
#                     or ((bus_line['lineRef'] == wanted[0][2]) and (wanted[1][2] in stop['stopPointRef']))):
#                     print("Tuli2")
#                     look_list.append(bus_line)
#     
# =============================================================================



    
stop_url = 'http://data.itsfactory.fi/journeys/api/1/stop-monitoring?stops=%s' % (wanted_stops)
stop_response = requests.get(stop_url)

# Linjan nimi, alkuperäinen saapumisaika, ennustettu saapumisaika
arrivals = []
if (stop_response.ok):
    stop_json = json.loads(stop_response.content)
    for key, val in stop_json['body'].items():
        for bus_line in val: 
            if (bus_line['directionRef'] == "1"):
                arrivals.append([bus_line['lineRef']
                , bus_line['call']['aimedArrivalTime']
                , bus_line['call']['expectedArrivalTime']])

for row in arrivals:
    scheduled = datetime.strptime(row[1], '%Y-%m-%dT%H:%M:%S+02:00')
    expected = datetime.strptime(row[2], '%Y-%m-%dT%H:%M:%S+02:00')
    delay = expected - scheduled
    print("Bussilinja: ", row[0], 
          "Suunniteltu: ", str(scheduled.hour) + ":" + str(scheduled.minute), 
          "Arvioitu: ", str(expected.hour) + ":" + str(expected.minute), 
          "Myöhästyy: ", str(int(delay.seconds/60)))


                
                
                
                
                
                
                
                
                
                