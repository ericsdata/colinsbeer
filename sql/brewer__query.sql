

SELECT DISTINCT beerID, 
                brewerId, 
                style,
                AB, 
                appearance,
                aroma, 
                palate,
                taste,
                overall 
                    
FROM reviews

HAVING COUNT(DISTINCT review_text) > 10 ;