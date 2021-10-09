# -*- coding: utf-8 -*-
"""
Created on Tue May 26 08:50:29 2020

@author: colin
"""
import pandas as pd
import os
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from fractions import Fraction
import datetime as dt

os.chdir(r"C:\Users\colin\Desktop\Coursera Python\Beer Analysis") 

conn = sqlite3.connect('beerdb.sqlite')
cur = conn.cursor()

#Retrieve entire table 
reviews = pd.read_sql_query('SELECT * FROM reviews', con = conn)
reviews2 = reviews
reviews2 = reviews[:100000]

#Check data types and change relevant dfs to numeric

#Convert relevant columns to float
reviews2['overall'] = [float(Fraction(x)) for x in reviews2['overall']]
reviews2['taste'] = [float(Fraction(x)) for x in reviews2['taste']]
reviews2['palate'] = [float(Fraction(x)) for x in reviews2['palate']]
reviews2['aroma'] = [float(Fraction(x)) for x in reviews2['aroma']]
reviews2['appearance'] = [float(Fraction(x)) for x in reviews2['appearance']]

#drop reviews if have hte same review for beer/brewery
reviews2 = reviews2.drop_duplicates(subset = ['review_text', 'name', 'brewerId'], keep = 'first')
#pd.DataFrame.to_csv(reviews2, 'BeerReviewsSample.csv')

#Time is in unix , first need to convert to an integer
#reviews2['time'] = (dt.datetime.utcfromtimestamp(reviews2['time'].astype(int)))

time_list = []
for row in range(len(reviews2)):
    time_list.append(dt.datetime.utcfromtimestamp(int(reviews['time'][row])))

reviews2['review_date'] = time_list
#reviews2['date'] =   (dt.datetime.strptime(i, "%Y-%m-%d") for i in time_list)

date_count = reviews2.groupby([reviews2['review_date'].dt.date])['review_date'].count()


#AB has empty dashes - conver those to missing values
reviews2['AB'] = reviews2['AB'].replace('-', np.nan)
reviews2['AB'] = pd.to_numeric(reviews2['AB'], errors='coerce')

print(list(reviews2.dtypes))


#Remove any duplicates (weird load process with stop and go)
reviews2 = reviews2.drop_duplicates()
reviews_groupedbeer = reviews2.groupby('beerID').agg({'review_text': 'count',
        'overall':'mean',
        'taste':'mean',
        'palate':'mean',
        'aroma':'mean',
        'appearance':'mean', 
        'AB' : 'mean'
        })

#Create high level summary some interesting info includes:
#in the 867k reviews: 36k unique beers -- avg 24 per beer, 2.4k unique brewers -- avg 361 reviews per brewer
#almost all had review text;
#
data_summary = reviews.describe()

#Does style impact rating?
style_agg = reviews2.groupby('style').agg({'review_text': 'count',
        'overall':'mean',
        'taste':'mean',
        'palate':'mean',
        'aroma':'mean',
        'appearance':'mean', 
        'AB' : 'mean'
        })

f, axes = plt.pyplot.subplots(2,1)
sns.scatterplot(x = style_agg['AB'], y = style_agg['overall'], size = style_agg['review_text'], ax = axes[0])
sns.distplot(reviews2['overall'], ax = axes[1], bins = 10)

#using coursera example
import matplotlib.gridspec as gridspec

plt.figure()

gspec = gridspec.GridSpec(3,3)
top_hist = plt.subplot(gspec[0,1:])
side_hist = plt.subplot(gspec[1:,0])
scatter = plt.subplot(gspec[1:,1:])

scatter.scatter(x = style_agg['AB'], y = style_agg['overall'])
side_hist.hist(reviews2['overall'], orientation = 'horizontal', facecolor = 'gray', bins = 20)
top_hist.hist(reviews2['AB'], bins = 20,  range=[0,15], facecolor = 'gray')
#side_hist.set_title = 'Distribution of ABV'
#top_hist.set_title = 'Distribution of Ratings'
#scatter.set_title = 'Style average ABV and Rating'
    
    
ax = plt.gca()

for ax in [top_hist, scatter]:
    ax.set_xlim = [0,15]
for ax in [side_hist, scatter]:
    ax.set_ylim = [0,1]

##DISITRIBUTIONS

#overall -- by review and by beer. Expect beer to be more normally distributed
sns.distplot(reviews_groupedbeer['overall'], bins = 20)
sns.distplot(reviews2['overall'], bins = 20)


#Relationship between overall score and abv
sns.scatterplot(x = reviews2['AB'], y = reviews2['overall'])

#Correlation matrix
corr = reviews_groupedbeer.corr()
ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
);


##TIME

