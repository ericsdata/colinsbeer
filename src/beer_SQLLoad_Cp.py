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

db_ec.create_db_connection(r'..\data\beerdb.db')


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

beer_list = []


with gzip.open(r'..\data\SNAP-Ratebeer.txt.gz', 'rt') as f:
     for line in f:
        lineformatted = re.sub(r'^.*?:', '', line)
        beer_list.append(lineformatted.lstrip().rstrip('\n'))



 #Look into pd.DataFrame.to_sql https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
y = 12138000
n = 10

for i in range(n):
    y = int(12138000 + 14000)
    i = i+1
    print(y)
    print(i)
    beer_short = beer_list[int(y-14000):y]
    x = len(beer_short)/14
    reviews_split = None
    reviews_split = np.array_split(beer_short, x)
    
    #x1 = len(beer_list)/14
    #beers_split = np.array_split(beer_short, x1)
    
    for entry in range(len(reviews_split)):
        
        name        = reviews_split[entry][0]
        beerID      = reviews_split[entry][1]   
        brewerId    = reviews_split[entry][2]
        AB          = reviews_split[entry][3]    
        style       = reviews_split[entry][4]
        appearance  = reviews_split[entry][5]
        aroma       = reviews_split[entry][6]
        palate      = reviews_split[entry][7]
        taste       = reviews_split[entry][8]  
        overall     = reviews_split[entry][9]
        time        = reviews_split[entry][10]
        profileName = reviews_split[entry][11]
        review_text = reviews_split[entry][12]
    
        #print(name)
    
        cur.execute('''INSERT INTO reviews
            (name, beerID, brewerId, AB, style, appearance,aroma,
            palate,taste, overall, time, profileName, review_text) 
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', 
            ( name, beerID, brewerId, AB, style, appearance,aroma,
            palate,taste, overall, time, profileName, review_text) )
    
        conn.commit()


