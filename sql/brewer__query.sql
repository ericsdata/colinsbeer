
SELECT  beerID, 
                brewerId, 
                style,
                AB, 
                appearance,
                aroma, 
                palate,
                taste,
                overall 
                    
FROM reviews

WHERE brewerID in (SELECT brewerID 
                    FROM reviews  
                    GROUP BY brewerID 
                    HAVING COUNT(review_text) > 10) ;