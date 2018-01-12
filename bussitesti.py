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

import credentials as cre


import requests
import json
from datetime import date, datetime, timedelta

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



# =============================================================================
#     
# stop_url = 'http://data.itsfactory.fi/journeys/api/1/stop-monitoring?stops=%s' % (wanted_stops)
# stop_response = requests.get(stop_url)
# 
# # Linjan nimi, alkuperäinen saapumisaika, ennustettu saapumisaika
# arrivals = []
# if (stop_response.ok):
#     stop_json = json.loads(stop_response.content)
#     for key, val in stop_json['body'].items():
#         for bus_line in val: 
#             if (bus_line['directionRef'] == "1"):
#                 arrivals.append([bus_line['lineRef']
#                 , bus_line['call']['aimedArrivalTime']
#                 , bus_line['call']['expectedArrivalTime']])
# 
# for row in arrivals:
#     scheduled = datetime.strptime(row[1], '%Y-%m-%dT%H:%M:%S+02:00')
#     expected = datetime.strptime(row[2], '%Y-%m-%dT%H:%M:%S+02:00')
#     delay = expected - scheduled
#     print("Bussilinja: ", row[0], 
#           "Suunniteltu: ", str(scheduled.hour) + ":" + str(scheduled.minute), 
#           "Arvioitu: ", str(expected.hour) + ":" + str(expected.minute), 
#           "Myöhästyy: ", str(int(delay.seconds/60)))
# # Ei saada kuin noin 10 min eteenpäin
# =============================================================================


#api.publictransport.tampere.fi/prod/?request=stop&user=aleksiroima&pass=kjsfdx1954qpo&code=Vanha&format=json

# Kokeillaan toisesta rajapinnasta jos saisi enemmän dataa
# Haetaan data ja luodaan lista, joka pitää sisällään tupleja, joissa linjan nimi ja saapumisaika pysäkille
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
                 
urls = [ 'http://api.publictransport.tampere.fi/prod/?request=stop&user=%s&pass=%s&code=3723&format=json&dep_limit=20&time_limit=360' % (cre.username, cre.passphrase)
        , 'http://api.publictransport.tampere.fi/prod/?request=stop&user=%s&pass=%s&code=3577&format=json&dep_limit=20&time_limit=360' % (cre.username, cre.passphrase)
        , 'http://api.publictransport.tampere.fi/prod/?request=stop&user=%s&pass=%s&code=3737&format=json&dep_limit=20&time_limit=360' % (cre.username, cre.passphrase)]


arrivals = []
for url in urls:
    get_busses(url, arrivals)
    
# Karsitaan jäljellä vain bussit, jotka lähtevät 5 min - 2 h päästä:

    
for bus in arrivals:
    # Koska kello ei mene 26 asti:
    if (bus[1][0:2] == "24"):
        bus[1] = bus[1].replace("24", "00", 1)
    elif (bus[1][0:2] == "25"):
        bus[1] = bus[1].replace("25", "01", 1)
    elif (bus[1][0:2] == "26"):
        bus[1] = bus[1].replace("26", "02", 1)
    bus[1] = int((datetime.combine(date.min, datetime.strptime(bus[1], '%H%M').time()) - datetime.combine(date.min, datetime.now().time())).total_seconds() / 60)
    if bus[1] < -1000:
        bus[1] = 6
    if ((bus[1] < 5) or (bus[1] > 100)):
        arrivals.remove(bus)

from operator import itemgetter
#arrivals = sorted(arrivals, key=itemgetter(1))
                
                
























                
                
                