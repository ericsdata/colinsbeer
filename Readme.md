## Intro

Another failed attempt at roping my friend into doing a joint data project -- however this time I was able to rope some data cleaning code off of him. This however let me get to my main purpose a bit easier, testing out the fine tuning of a Hugging Face LLM.

## The Data

My buddy had downloaded a publicly available data set of [BeerAdvocate Data](https://web.archive.org/web/20200114060821/http://memetracker.org/data/web-BeerAdvocate.html), containing over 1.5 million records collected over a ten year time span.

Each record contains information about a specific beer (brewery, abv, style) and impression information (written review, rating, appearance) from BeerAdvocate users.

## The Goal

Fine tune a LLM to provide a written description of a "good beer" vs a "bad beer" of a specific style. 
Ultimately, my adapted source code to do this is hosted on Colab in the `WriteReviews.ipynb` file.

## To Do

- Upload cleaned scripts that demonstrate processing of raw data into train and test samples