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
import beer_data_load as bdl


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

## extract Tuples is used for RDBs
beer_list = bdl.extractTuples(r'..\data\SNAP-Ratebeer.txt.gz')


## beer_json = bdl.extractJSON(r'..\data\SNAP-Ratebeer.txt.gz')

cur.executemany('''INSERT INTO reviews
            (name, beerID, brewerId, AB, style, appearance,aroma,
            palate,taste, overall, time, profileName, review_text) 
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', beer_list
            )
conn.commit()

