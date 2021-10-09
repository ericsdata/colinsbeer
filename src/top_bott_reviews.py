# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 07:28:01 2020

@author: colin
"""

#Beer Top 3 and bottom 3 associated words for each beer chosen
import pandas as pd
import numpy as np
import os
from fractions import Fraction
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer


os.chdir(r"C:\Users\colin\Desktop\Coursera Python\Beer Analysis") 

#Load data 
reviews2 = pd.read_csv('BeerReviewsSample.csv')

#For analysis moving forward, focus on beers with 5+ reviews
beer_counts = pd.DataFrame(reviews2.groupby(['beerID'], as_index = True).size(),  columns = ['Count'])
beer_highn = beer_counts[beer_counts['Count']>10] #for now, restrict top beers to get working prototype
#beer_highn = beer_highn[beer_highn['Count']<100]
beer_highn['beerID'] = beer_highn.index

beerID_list = beer_highn['beerID']

#collab = collab.sample(n = 10000)
top_words_df = reviews2[reviews2['beerID'].isin(beerID_list)]

top_words_df['overall'] = [float(Fraction(x)) for x in top_words_df['overall']]

sentiment_df = top_words_df[['beerID', 'overall', 'review_text']]
mean_rating = sentiment_df['overall'].mean()
sentiment_df['rating_binary'] = np.where(sentiment_df['overall']>mean_rating, 1, 0)


import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

from nltk.corpus import wordnet

def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
    
import string
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
    
#Create function clean text
def clean_text(text):
    # lower text
    text = text.lower()
    # tokenize text and remove puncutation
    text = [word.strip(string.punctuation) for word in text.split(" ")]
    # remove words that contain numbers
    text = [word for word in text if not any(c.isdigit() for c in word)]
    # remove stop words
    stop = stopwords.words('english')
    text = [x for x in text if x not in stop]
    # remove empty tokens
    text = [t for t in text if len(t) > 0]
    # pos tag text
    pos_tags = pos_tag(text)
    # lemmatize text - identifies common roots across words (e.g., connect, connecting, connected)
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]
    # remove words with only one letter
    text = [t for t in text if len(t) > 1]
    # join all
    text = " ".join(text)
    return(text)
    
# clean text data
sentiment_df['review_text'] = sentiment_df['review_text'].astype(str)
sentiment_df["review_clean"] = sentiment_df["review_text"].apply(lambda x: clean_text(x))

from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()
sentiment_df["sentiments"] = sentiment_df["review_clean"].apply(lambda x: sid.polarity_scores(x))
sentiment_df2 = pd.concat([sentiment_df.drop(['sentiments'], axis=1), sentiment_df['sentiments'].apply(pd.Series)], axis=1)

# add number of characters column
sentiment_df2["nb_chars"] = sentiment_df2["review_clean"].apply(lambda x: len(x))

# add number of words column
sentiment_df2["nb_words"] = sentiment_df2["review_clean"].apply(lambda x: len(x.split(" ")))

#Check correlation between 
sentiment_df2['overall'].corr(sentiment_df2['compound'])

highest = []
s_highest =[]
lowest = []
s_lowest =[]
beerID = []
def get_top2_bot2_reviews(sentiment_df, beerIDs):
    for i in beerIDs:
        sentiment = sentiment_df[sentiment_df['nb_words']>10]
        sentiment_filtered = sentiment[sentiment_df2['beerID'] == i].sort_values(by= 'compound', ascending = False)
        highest.append(sentiment_filtered.review_text[:1].tolist())
        s_highest.append(sentiment_filtered.tail(1).review_text.tolist())
        lowest.append(sentiment_filtered.review_text[1:2].tolist())
        s_lowest.append(sentiment_filtered.iloc[[-2]]['review_text'].tolist())
        beerID.append(i)
    sentiment_scored = pd.DataFrame({'highest': highest, 's_highest': s_highest,
                                     'lowest': lowest, 's_lowest':s_lowest, 'beerID': beerID})
    return sentiment_scored
    
    
a = get_top2_bot2_reviews(sentiment_df2, beerID_list)

pd.DataFrame.to_csv(a, 'sentiment_df_06192020.csv')
 