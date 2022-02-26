
'''
Functions to run that will read source data for beer project
Further handle loading of different databases
'''

import gzip
import sqlite3 #create sql connection and db
import numpy as np
import re
import db_ec

def extractJSON(file_loc):
    ### One loop - if/thens can be improved upon
    #### Use a while loop
    with gzip.open(file_loc, 'rt') as f:
        single_beer = [] ## list to hold records for a single review
        beer_list = [] ## list to hold all reviews

        for line in f:
            
            ### Need to set up JSON type data
            #### Split into two groups from colon
            line_grouped = re.match(r'(^.*?:)(.*)', line) #read first line
            
            #### TODO set it up
            ## Determine whether line is final row record, delimited by \n
            if lineformatted != "\n":
                single_beer.append(lineformatted.lstrip().rstrip('\n'))
            elif lineformatted == "\n":
                beer_list.append(tuple(single_beer))
                single_beer = []
            else:
                print("something has gone wrong")

f = re.match(r'(^.*?:)(.*)',t_str)