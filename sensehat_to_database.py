# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 09:06:55 2018

@author: Aleksi Roima
"""
import psycopg2
import credentials as cre
from time import gmtime, strftime
from random import randint

def run_test_data():
    try:
        conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (cre.dbname, cre.user, cre.host, cre.password))
        cur = conn.cursor()
        valuelist = [randint(30,50), randint(50,80), strftime("%Y-%m-%d %H:%M:%S", gmtime())]
        sql = 'INSERT INTO sense_hat_table(temperature, humidity, loadtime) VALUES (%s, %s, %s)'
        cur.execute(sql, valuelist)
        conn.commit()
        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


def run_sense_data():    
    from sense_hat import SenseHat
    try:
        sense = SenseHat()
        conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (cre.dbname, cre.user, cre.host, cre.password))
        cur = conn.cursor()
        valuelist = [sense.temperature(), sense.humidity(), strftime("%Y-%m-%d %H:%M:%S", gmtime())]
        sql = 'INSERT INTO sense_hat_table(temperature, humidity, loadtime) VALUES (%s, %s, %s)'
        cur.execute(sql, valuelist)
        conn.commit()
        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)