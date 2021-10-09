

## Hugging face trial

### Use review textst to classify styles

import db_ec
import pandas as pd
import numpy as np

import torch
from sklearn.model_selection import train_test_split

from transformers import AutoTokenizer, AutoModelForSequenceClassification


conn = db_ec.connect_db(r'data\beerdb.sqlite')

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

train = dat_list[0]

test = dat_list[1]

x_labels = torch.tensor(train['style_id'].values)

x_text = train.review_text.to_list()

 ## Import BERT Model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")


batch = tokenizer(x_text, padding=True, truncation=True, return_tensors="pt")
batch['labels'] = torch.tensor(train['style_id'].values)