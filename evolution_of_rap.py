import pandas as pd
import numpy as np
from string import punctuation
import cPickle as pickle
from collections import Counter, defaultdict
from naive_bayes import combined_txt_file, output_files, create_labeled_dataframe

def word_set(lyrics):
    '''
    Input: Lyrics as a list of lines
    Output: a set of unique words for that song
    '''
    lyrics_split = lyrics.lower().split()
    lyrics_split = [word.strip(punctuation) for word in lyrics_split]
    return set(lyrics_split)

def create_dict(df, topic):
    '''
    Input: A topic
    Output:
    '''
    #makes a default dictionary
    list_dict = defaultdict(set)

    #go through all the rows in the dataframe
    for index, row in df.iterrows():
        aggregation = df.ix[index, topic]
        words = df.ix[index, 'word_set']
        list_dict[aggregation].update(words)
    return list_dict

def test_time(time):
    try:
        return pd.to_datetime(time)
    except ValueError:
        return None

def convert_df_to_datetime(df):
    '''
    Input: 
    Output:
    '''
    real_date_mask = date_clean.date_published.apply(lambda x: x.split()[-1].isdigit())
    final = date_clean.ix[real_date_mask]
    final.reset_index(inplace=True)
    final['date_published'] = final['date_published']
    none_mask = final['date_published'].isnull()
    final = final.ix[none_mask]
    final.reset_index(inplace=True)
    return final


if __name__ == '__main__':
    # making a combined list
    combined = combined_txt_file(output_files)
    combined['word_set'] = combined['full_lyrics'].apply(word_set)

    #create the labels table
    labels = create_labeled_dataframe('artist_classification.txt')

    #create a new joined dataframe
    result = combined.merge(labels, left_on='artist', right_on=' artist', how='inner')

    artist_dict = create_dict(combined, 'artist')
    class_dict = create_dict(combined, 'classification')

    #creating a data frame with only real time
    clean_df = convert_df_to_datetime(result)

    with open('data_df.pkl', 'w') as f:
        pickle.dump(clean_df, f)
