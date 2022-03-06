# colinsbeer

Beer Rating data


## DAta

We have a data file with 2.9 million beer reviews from Beer Advocate (?). Data is stored in text delimited files. 


## Whut ~~r we~~ we are doing


#### **Prediction**
- Language Generation
    - Good example with artist lyrics => https://colab.research.google.com/github/AlekseyKorshuk/huggingartists/blob/master/huggingartists-demo.ipynb#scrollTo=BXCZM6vfRHKo

    - generate descriptions of different beers, by preference
        People who liked the beer said this: ....
        People who didnt like the beer said this: ....


- Run clustering algorithms on tokenized ids of text
    - which beers / beer types are similarly described


#### **Descriptive**
    -  Reviews that are "subjective" vs "objective"
        - Lack of pronouns within review conveys less inovled 
        - *How else could 'reviewer style' be measured?*

    - Breweries
        - How many of each style a brewery makes

=======


### TO DO

- How clean is our data?
    - Newline delimited
    - Missing reviews , scores, brewery identifiers
    - Text 
        - Many reviews start with serving styles
        - Extra spacing


- NoSql? / Database repair

- General code cleanliness and workflow




  
