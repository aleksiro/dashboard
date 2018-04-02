# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 21:12:12 2018

@author: Aleksi Roima
"""
from time import sleep
import weather_forecast_to_database as weather
import sensehat_to_database as sensehat
import bus_data_to_database as bus

# If test_mode is true SenseHat measures are not really measured but taken as random integers
TEST_MODE = True

def main():
    i = 0
    while True:
        if (TEST_MODE == True):
            sensehat.run_test_data()
        else:
            sensehat.run_sense_data()
        if (i == 60):
            i = 0
            # Get weather data to database
            weather.run_weather_data()
            # Get bus data to database
            bus.run_bus_data()
        sleep(1)
        i += 1
        print(i)
        
if __name__ == "__main__":
    main()