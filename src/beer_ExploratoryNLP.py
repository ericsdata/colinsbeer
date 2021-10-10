

## Hugging face trial

### Use review textst to classify styles

from typing import Sequence
import db_ec
import pandas as pd
import numpy as np

import torch
from sklearn.model_selection import train_test_split




conn = db_ec.connect_db(r'..\data\beerdb.sqlite')

## REad in data
dat = pd.read_sql('SELECT review_text, style FROM reviews;',conn)
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


## Split data for ML validation 
dat_list = train_test_split(dat, test_size= 0.3, random_state=1144, shuffle=True, stratify=None)
##  Full data
train = dat_list[0]

test = dat_list[1]

x_labels = torch.tensor(train['style_id'].values)

x_text = train.review_text.to_list()

few_reviews = x_text [0:5]





from transformers import AutoTokenizer, AutoModelForSequenceClassification


## Sequence is single str of text
sequence = few_reviews

 ## Import BERT Model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

## Moddel inputs holds two arrays
    ## input_ids: list of id of word vector
    ## attention_mask
    
model_inputs = tokenizer(sequence, padding = True, truncation = True, return_tensors= 'pt')


## List of IDs
ids = tokenizer.convert_tokens_to_ids(model_inputs)



#batch = tokenizer(few_reviews, padding="max_length", truncation=True, return_tensors="pt")

## !!! Attaching class to model inputs
model_inputs['labels'] = torch.tensor(train['style_id'].values)

### Choosing tokenizer
####    A) Keep reviews by uid
####    B) Sentence strings associated with a particular style

output = model(**model_inputs)

i = 0

for out in range(0,len(output)):

    print(output[i])
    i+=1