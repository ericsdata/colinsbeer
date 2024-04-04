'''
beerID  name                     review_count
42935	Trader Joes Hofbrau Bock	239
43176	Trader Joes Vienna Style Lager	239
46471	Ridgeway IPA	239
65888	Saranac Brown Ale	239
117319	Harpoon 100 Barrel Series #30 - Island Creek Oyster Stout	238
2519	Shipyard Chamberlain Pale Ale	238
29028	De Hemel Nieuw Ligt Grand Cru	238
3202	Penn Dark Lager Beer	238
4302	Gearys London Porter	238
56242	East End Gratitude	238
'''


import db_ec
import BeerBrush as bb
import pandas as pd
### Beer IDs - these beers had less than two hundred reviews. Let's try gneerating text for these reviewws
beer_ids = tuple( ['42935','43176','46471','65888','117319',
                '2519','29028','3202','4302','56242'] )


conn = db_ec.connect_db(r'..\data\beerdb.sqlite')
cur = conn.cursor()

SQL_q = '''SELECT beerID, overall, review_text 
            FROM reviews 
            WHERE beerID in {}'''.format(beer_ids)


cur.execute(SQL_q)
dat = cur.fetchall()

train_text = []
for rev in dat:
    rev = list(rev)

    rev[1] = str(int(round(bb.cleanScores(rev[1]),0)))

    train_text.append(' '.join(rev))
