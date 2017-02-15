# Rapalytics

## Motivation
Each genre of music has it's own style that is determined based on the rhythm, beat, tempo, lyrics, and the voice of the artist. Rap is a unique genre of music where the artist are particularly prideful of where they grew up and the distinct sound of that region.

My motivation was to find out if the lyrics were distinct enough to determine which region the artist came from.

## Technologies and Dependencies
* python
* numpy
* pandas
* bs4
* requests
* NLTK
* sklearn
* matplotlib
* cPickle
* AWS EC2

## Collection of Datasets
* Utilized wikipedia to obtain a list of all Hip-Hop and R&B artists, regional classification was also extracted (if available)

* From that list, I created a web scraper to go onto Rap Genius and obtain  all the songs for each of the artist

* My final dataset contained **125K** songs


## Feature Engineering
There are some generalization and assumptions within the music community about the distinct divide between East and West Coast rap. These perception were more prominent in the 1990's but I wanted to see if they were still currently valid.

* East-Coast songs is considered more creative in terms of lyrics and had more of a story like structure. Features relating to unique number of words used, frequency of new words used for end rhyme, and term frequencies were created for this region.

* West-Coast music is considered more 'gangsta' and dealt with more violent topics such as guns, drugs, police brutality, etc. To capture this, I seeded a list of words to determine if a certain song dealt with those topics.

* Dirty-South music is atypical of what you would hear in clubs. It has lots of catch phrases, is repetitive, and has an upbeat tempo. Features created from these assumptions were term frequencies of the top 7 most commonly used word - this was to check how repetitive a song was.


## Results
* With a multi-class classification, Multinomial Naive Bayes achieved **68%** Accuracy


## Insights

To confirm my perceptions, I aggregated the number of unique words over time, the number of unique words was my proxy for determining creativity within a certain region.

From the graph, it does seem that East Coast is more 'creative' although West coast is not far behind. The other assumptions about Dirty-South was also validated - it has significantly less unique words than the other two regions.

![Alt text](/images/alt_word_growth_by_region.png?raw=true "Unique Word Growth")

To see if the generalization I made about each region were also valid on the artist level, a scatterplot was made plotting the number of songs versus the number of words for each artist.


![Alt text](/images/alt_cluster.png?raw=true "Rapper Ranking")

* I would have expected a larger clustering of East-Cost rapper in terms of being of the higher end of the spectrum (word-count wise). This did not seem to be the case and there seems to be transcendent artists from each region that are highly popular and creative

* Influential rappers such as Tupac and Biggie, unsurprisingly, feel in the middle of the pack due to their relatively short career
