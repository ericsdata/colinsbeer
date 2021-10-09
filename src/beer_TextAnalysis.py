# -*- coding: utf-8 -*-
"""
Created on Tue May 26 19:43:33 2020

@author: colin
"""
#Text Analysis -- Beer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import os
import sqlite3
from fractions import Fraction


os.chdir(r"C:\Users\colin\Desktop\Coursera Python\Beer Analysis") 

#conn = sqlite3.connect('beerdb.sqlite')
#cur = conn.cursor()

#reviews = pd.read_sql_query('SELECT * FROM reviews', con = conn)
#reviews2 = reviews
#reviews2 = reviews[:10000]

reviews2 = pd.read_csv('BeerReviewsSample.csv')

reviews2['overall'] = [float(Fraction(x)) for x in reviews2['overall']]


#Create new df with just columns needed
sentiment = reviews2[['overall','review_text']]

#First method: binary review - split into good or bad 
mean_rating = reviews2['overall'].mean() #0.67
sentiment['rating_binary'] = np.where(reviews2['overall'] > mean_rating, 1, 0)

#View the distribution - 56% are "positive"
pos_neg_cross = pd.crosstab(index = sentiment['rating_binary'], columns = "Total Count")

#Split reviews into test and train randomly
sent_train, sent_test = train_test_split(sentiment, test_size=0.3)

#Start vectorization process #https://towardsdatascience.com/sentiment-analysis-with-python-part-1-5ce197074184
#Each column is a unique word across all the dfs. each row is a review. when that word appears in the sentence
#a one will populate the matrix. matrix is sparse since it is mostly 0

#One hot encoding 
cv = CountVectorizer(binary = True)
cv.fit(sent_train['review_text'])
x = cv.transform(sent_train['review_text']) #sparse matrix training data
x_test = cv.transform(sent_test['review_text']) #sparse matrix testing data

#Build a classifier using logistic regression
#x_train = sent_train['review_text']
#x_rating = sent_train['overall']
#y_train = sent_test['review_text']
#y_rating = sent_test['overall']

y = sent_train['rating_binary']
y_test = sent_test['rating_binary']

x_train, x_rating, y_train, y_rating = train_test_split(
    x, y, train_size = 0.75
)

for c in [0.01, 0.05, 0.25, 0.5, 1]:
    
    lr = LogisticRegression(C=c)
    lr.fit(x_train, y_train)
    print ("Accuracy for C=%s: %s" 
           % (c, accuracy_score(y_rating, lr.predict(x_rating))))
    

#C = 1, regularization tuning parameter, has highest accuracy use for model
final_model = LogisticRegression(C=1)
final_model.fit(x, y)
print ("Final Accuracy: %s" 
       % accuracy_score(y_test, final_model.predict(x_test)))


#five most discriminating words
feature_to_coef = {
    word: coef for word, coef in zip(
        cv.get_feature_names(), final_model.coef_[0]
    )
}
for best_positive in sorted(
    feature_to_coef.items(), 
    key=lambda x: x[1], 
    reverse=True)[:15]:
    print (best_positive)

    
for best_negative in sorted(
    feature_to_coef.items(), 
    key=lambda x: x[1])[:15]:
    print (best_negative)
    
    
#Scoring each review running correlation with rating
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
sentiment["review_clean"] = sentiment["review_text"].apply(lambda x: clean_text(x))

from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()
sentiment["sentiments"] = sentiment["review_clean"].apply(lambda x: sid.polarity_scores(x))
sentiment_df = pd.concat([sentiment.drop(['sentiments'], axis=1), sentiment['sentiments'].apply(pd.Series)], axis=1)

# add number of characters column
sentiment_df["nb_chars"] = sentiment_df["review_clean"].apply(lambda x: len(x))

# add number of words column
sentiment_df["nb_words"] = sentiment_df["review_clean"].apply(lambda x: len(x.split(" ")))

# create doc2vec vector columns
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(sentiment_df["review_clean"].apply(lambda x: x.split(" ")))]

# train a Doc2Vec model with our text data
model = Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=4)

# transform each document into a vector data
doc2vec_df = sentiment_df["review_clean"].apply(lambda x: model.infer_vector(x.split(" "))).apply(pd.Series)
doc2vec_df.columns = ["doc2vec_vector_" + str(x) for x in doc2vec_df.columns]
sent_analyzer_df = pd.concat([sentiment_df, doc2vec_df], axis=1)

# add tf-idfs columns
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(min_df = 10)
tfidf_result = tfidf.fit_transform(sentiment_df["review_clean"]).toarray()
tfidf_df = pd.DataFrame(tfidf_result, columns = tfidf.get_feature_names())
tfidf_df.columns = ["word_" + str(x) for x in tfidf_df.columns]
tfidf_df.index = sentiment_df.index
sentiment_df = pd.concat([sentiment_df, tfidf_df], axis=1)


# highest positive sentiment reviews (with more than 5 words)
sentiment_df[sentiment_df["nb_words"] >= 5].sort_values("pos", ascending = False)[["review_text", "pos"]].head(10)

# lowest negative sentiment reviews (with more than 5 words)
sentiment_df[sentiment_df["nb_words"] >= 5].sort_values("neg", ascending = False)[["review_text", "neg"]].head(10)


import seaborn as sns

sentiment_df['sentiment'] = np.where(sentiment_df['overall'] < 6.7, 0, 1)

for x in [0, 1]:
    subset = sentiment_df[sentiment_df['sentiment'] == x]
    
    # Draw the density plot
    if x == 0:
        label = 0
    else:
        label = 1
    sns.distplot(subset['compound'], hist = False, label = label)

