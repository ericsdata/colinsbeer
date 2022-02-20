# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 13:39:26 2020

@author: eachr
"""


import os
import sqlite3
import csv
import pandas as pd

from sqlite3 import Error


##function to create database BikesDB

def create_db_connection(path):
    
    conn = None
    try:
        conn = sqlite3.connect(path)
        print(sqlite3.version)
        
    except Error as e:
        print(e)
    
    finally:
        if conn:
            conn.close()

##Function to connect to db connection object
    
def connect_db(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return conn

##Function for creating tables
def create_table(conn, create_table_stmt):
    """ create a table from the create_table_stmt statement
    :param conn: Connection object
    :param create_table_stmt: a CREATE TABLE statement
    :return:
    """
    ##create cursosr object
    try:
        c = conn.cursor()
        c.execute(create_table_stmt)
    except Error as e:
        print(e)
        
##convert input string to boolean
def str2bool(v):
    if str(v).lower() in ("yes", "true", "t", "1", "y"):
        return True
    elif str(v).lower() in ("no", "false", "f", "0", "n"):
        return False
    else:
        return print("Invalid selection for boolean value")
    
def executeStatement(conn , statement : str, params : list):
    '''
    Generic funciton to return dataframes from query

    Arguments
        conn : db_connect object
        statement : sql string of query, (can be paramterized)
        params: list of ordered parameters for querty
    
    Returns
        data : pd dataframe of query results
    '''
    try:
        data =  pd.read_sql(statement
                    ,conn
                    ,params= params)
    except Error as e:
        print(e)

    return data