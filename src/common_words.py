#find common words for each beer
#https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk

import pandas as pd
import os
os.chdir(r"C:\Users\colin\Desktop\Coursera Python\Beer Analysis") 
reviews2 = pd.read_csv('BeerReviewsSample.csv')
from collections import Counter 


import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 
nltk.download('punkt')
#Group df by beer name and append text
reviews2['review_text'] = str(reviews2['review_text'])
test = reviews2.groupby(['name'], as_index = False).agg({'review_text': ' '.join})

a = test[:1]['review_text']
a = str(a)
b = a.split()
word_counter = {}
for word in b:
    if word in word_counter:
        word_counter[word] +=1
    else:
        word_counter[word] = 1

popular_words = sorted(word_counter, key = word_counter.get, reverse = True)    

#USE NLTK TO PULL OUT ADJECTIVES FOR EACH WORD
stop_words = set(stopwords.words('english')) 

tokenized = sent_tokenize(a)
for i in tokenized: 
      
    # Word tokenizers is used to find the words  
    # and punctuation in a string 
    wordsList = nltk.word_tokenize(i) 
  
    # removing stop words from wordList 
    wordsList = [w for w in wordsList if not w in stop_words]  
  
    #  Using a Tagger. Which is part-of-speech  
    # tagger or POS-tagger.  
    tagged = nltk.pos_tag(wordsList) 
  
    print(tagged)  

tagged['JJ']


#get list of most common words 

#take only first 20 words within each review
reviews2 = pd.read_csv('BeerReviewsSample.csv')
reviews2.fillna('')

review_text = list(reviews2['review_text'])

words = []
for i in range(len(review_text)):
    words.append(str(review_text[i]).split()[:15])

all_words = ''.join(map(str, words))
all_words_list = all_words.split()

word_tokens = word_tokenize(all_words) 
  
stop_words = set(stopwords.words('english')) 

wordsList = [w for w in all_words_list if not w in stop_words]  

Counter = Counter(wordsList) 
most_occur = Counter.most_common(30) 
print(most_occur)
