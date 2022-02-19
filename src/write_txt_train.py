
from typing import Sequence
import db_ec
import pandas as pd
import numpy as np
import math


def write_training_data(conn, target, size = 10000):


    ## REad in data
    dat = pd.read_sql('SELECT DISTINCT beerID, brewerId, overall, review_text, style FROM reviews ;'
                    ,conn
                    , params= {"size":size})

    ### Set up reviews for NLP by adding CLS SEP tags

    #dat['review_text'] = ["[CLS] " + query + " [SEP]" for query in dat['review_text']]

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

    ## Fix the rating format
    def adjustOverallScore_binary(unformatted_score):
        score = float(unformatted_score.split('/20')[0]) / 20 ### Split and format
        return score

    def adjustOverallScore_down(unformatted_score):
        score = float(unformatted_score.split('/20')[0]) / 20 ### Split and format
        return int(round(score*10,0))

   # dat['level_score'] = dat['overall'].apply(adjustOverallScore_down)
    dat['overall_f'] = dat['overall'].apply(adjustOverallScore_binary)

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
    write_training_data(conn, target = 'good_score', size = 50000)