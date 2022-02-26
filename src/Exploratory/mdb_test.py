'''
File created to test Mongo DB capabilities

Requires some set up at https://www.mongodb.com/
https://www.mongodb.com/languages/python
'''

import getpass

### Create a mongodb client
def get_database(db_name,user, pwd, cluster):
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://<%s>:<%s>@%s.mongodb.net/%s"%(user,pwd,cluster,db_name)

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['user_shopping_list']


password = getpass.getpass('gimme ur password')
user_name = 'colinsbeer'
db_name = 'beerdata'
clus_name = 'cluster0.w17uo'

conn = get_database(db_name, user_name, password, clus_name)

col_name = conn['user_1_items']