
from typing import Sequence
import db_ec
import pandas as pd
import numpy as np
import math

import clean_beer_data as cbd


def write_training_data(conn, sql_statement, target, size = 40000):
    '''
    Function writtent to read data from data frame, transform

    Arguments
        conn : Data connection able to return queries in data frames
        target : what is target for ml model
        size : choose a size of training data to return 
    
    Returns 
        txt_test.csv - file written to data folder. 70% of size arg, data used for ml training
        txt_test.csv - file written to data folder. data used for ml validation
    '''
    ### TODO 
        ## Make function able to accomodate all types of functions
        ## modularize transformation
        ## Data sourcing
    ## Get all beers
    statement = '''SELECT DISTINCT beerID, 
                                    brewerId, 
                                    overall, 
                                    review_text, 
                                    style 
                    
                    FROM reviews ;'''


    ## Get beers with a lot of reviews
    statement = '''SELECT DISTINCT a.beerID, 
                                    a.brewerId, 
                                    a.overall, 
                                    a.review_text, 
                                    a.style 
                    
                    FROM (SELECT beerID
                                , Count(*) as rCount
                        FROM reviews 
                        WHERE review_text <> ''
                        GROUP BY beerID
                        HAVING rCount > ?

                              
                                ) b 
                Left Join  reviews a
                        ON b.beerID = a.beerID

                


                    ;'''

    sql_file = open(r"..\sql\brewer__query.sql")
    sql_statement = sql_file. read()

    minReviews = 100
    params = []

    ## REad in data
    dat = db_ec.executeStatement(conn,sql_statement, params)

    ### Set up reviews for NLP by adding CLS SEP tags
    #dat['review_text'] = ["[CLS] " + query + " [SEP]" for query in dat['review_text']]
    dat = dat.sample(n = size, replace = False)
    ### Take a random sample


    ## Simplify targets
    dat['style'] = dat['style'].str.replace('India.*', 'India Pale Ale', regex = True)
    dat['style'] = dat['style'].str.replace('Belgi.*', 'Witbier', regex = True)
    ## Convert to numeric ID for NN
    dat['style_id'] = dat['style'].map({
                            'Dunkel' : 1, 
                            'Pilsener':2, 
                            'Low Alcohol': 3, 
                            'India Pale Ale':4,
                            'Oktoberfest/Märzen' : 5, 
                            'American Pale Ale':6, 
                            'Schwarzbier':7,
                            'Witbier' : 8, 
                            'Classic German Pilsener' : 9, 
                            'Scottish Ale' : 10, 
                            'Fruit Beer' :11,
                            'Pale Lager' : 12, 
                            'Premium Lager':13, 
                            'Dunkler Bock':14, 
                            'Heller Bock' :15})

  

   # dat['level_score'] = dat['overall'].apply(adjustOverallScore_down)
    dat['overall_f'] = dat['overall'].apply(cbd.adjustOverallScore)

    dat['good_score'] = dat['overall_f'].apply(lambda x: 1 if x >= .8 else 0)

    

    ### MAke a training set
    from sklearn.model_selection import train_test_split

    #dat = dat[dat.style_id.isin([1,2,3,4,5])]

    ## Split data for ML validation 
    dat_list = train_test_split(dat[['review_text', target]], test_size= 0.3, random_state=1144, shuffle=True, stratify=None)
    ##  Split train and test, push to csv - upload to google colab
    train = dat_list[0]
    train.to_csv(r'..\data\txt_train.csv', index = False)



    test = dat_list[1]
    test.to_csv(r'..\data\txt_test.csv', index = False)


if __name__ == '__main__':
    conn = db_ec.connect_db(r'..\data\beerdb.sqlite')
    write_training_data(conn, target = 'good_score', size = 10000)