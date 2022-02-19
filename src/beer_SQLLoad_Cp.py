# -*- coding: utf-8 -*-
"""
Created on Mon May 25 09:40:30 2020

@author: colin
"""

#Load packages
import os
import gzip
import sqlite3 #create sql connection and db
import numpy as np
import re
import db_ec

#load data
#os.chdir(r"C:\Users\colin\Desktop\Coursera Python\Beer Analysis") 

#db_ec.create_db_connection(r'..\data\beerdb.db')


#connect to SQL db  
conn = db_ec.connect_db(r'..\data\beerdb.sqlite')
cur = conn.cursor()

#Do DB set-up
cur.executescript('''
DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews (
    name        TEXT,
    beerID      TEXT,
    brewerId    TEXT,
    AB          TEXT,
    style       TEXT,
    appearance  TEXT,
    aroma       TEXT,
    palate      TEXT,
    taste       TEXT,
    overall     TEXT,
    time        TEXT,
    profileName TEXT,
    review_text TEXT  
)

''')



### One loop - if/thens can be improved upon
#### Use a while loop
with gzip.open(r'..\data\SNAP-Ratebeer.txt.gz', 'rt') as f:
     single_beer = [] ## list to hold records for a single review
     beer_list = [] ## list to hold all reviews

     for line in f:
        
        lineformatted = re.sub(r'^.*?:', '', line) #read first line
        
        ## Determine whether line is final row record, delimited by \n
        if lineformatted != "\n":
            single_beer.append(lineformatted.lstrip().rstrip('\n'))
        elif lineformatted == "\n":
            beer_list.append(tuple(single_beer))
            single_beer = []
        else:
            print("something has gone wrong")

        

cur.executemany('''INSERT INTO reviews
            (name, beerID, brewerId, AB, style, appearance,aroma,
            palate,taste, overall, time, profileName, review_text) 
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', beer_list
            )
conn.commit()

