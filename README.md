# Rapalytics

## Motivation
* Wanted to find out if rap song lyrics are distinct enough to determine which region the artist came from. Each genre of music has distinct style that is comprised on the rhhythm, beat, tempo, lyrics, artist voice. However, I wanted to constrain the problem to only look at songs lyrics. There is a perception in the rap community that each of the threee main region of rap, East Coast, West Coast, and Dirty South, have very unique lyrical style. This assumption was the main motivation that drove my 

## Technologies and Dependencies
* python
* numpy
* pandas
* bs4
* requests
* NLTK
* sklearn
* matplotlib
* AWS EC2

## Collections of Datasets
* Obtained **125K** songs from rap genius
* Region labels were pulled from Wikipedia


## Results
* With a multi-class classification, Multinomial Naive Bayes achieved **68%** Accuracy

![Alt text](/images/alt_word_growth_by_region.png?raw=true "Unique Word Growth")