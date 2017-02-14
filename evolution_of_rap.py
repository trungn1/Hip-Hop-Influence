import pandas as pd
import numpy as np
from string import punctuation
import cPickle as pickle
from nltk.corpus.reader import cmudict
import matplotlib.pyplot as plt
from collections import Counter, defaultdict, OrderedDict
from naive_bayes import combined_txt_file, output_files, create_labeled_dataframe


def create_word_dict(df, col_name):
    '''
    Input: A dataframe and a column name to index
    Output: Return a dictionary with the key of col and a set of words
    '''
    #makes a default dictionary
    list_dict = defaultdict(set)
    #go through all the rows in the dataframe
    for index, row in df.iterrows():
        aggregation = df.ix[index, col_name]
        words = df.ix[index, 'word_set']
        list_dict[aggregation].update(words)
    return list_dict

def create_count_dictionary(dictionary):
    count_dict = defaultdict(int)
    for key, values in dictionary.iteritems():
        count_dict[key] = len(values)
    return count_dict

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
    #removes all record without a date
    initial_date_mask = df['date_published'].isnull()
    df = df.ix[~initial_date_mask]
    df.reset_index(inplace=True)
    df = df.drop('index', 1)

    #This mask is used to determine which one has a date in the date_published field
    real_date_mask = df['date_published'].apply(lambda x: x.split()[-1].isdigit())
    final = df.ix[real_date_mask]
    final.reset_index(inplace=True)
    final = final.drop('index', 1)

    #convert this to a date time object
    final['date_published'] = final['date_published'].apply(test_time)

    #Remove the records for songs without a valid datetime object
    none_mask = final['date_published'].isnull()
    final = final.ix[~none_mask]
    return final

if __name__ == '__main__':
    # making a combined list about 125K
    combined = combined_txt_file(output_files)
    combined['word_set'] = combined['full_lyrics'].apply(word_set)

    #create the labels table
    labels = create_labeled_dataframe('artist_classification.txt')

    #create a new joined dataframe about 46K
    combined_with_label = combined.merge(labels, left_on='artist', right_on=' artist', how='inner')

    #using the combined_with_label dataframe, you need to get the dictionary of the words
    artist_dict = create_word_dict(combined_with_label, 'artist')
    class_dict = create_word_dict(combined_with_label, 'classification')

    #creating a data frame with only real time
    clean_df = convert_df_to_datetime(combined_with_label)

    #saving the dataframe with the songs and region label
    with open ('combined_with_label.pkl', 'w') as f:
        pickle.dump(combined_with_label, f)

    #saving the dataframe with the songs, region label, and datetime obj
    with open('clean_date_data.pkl', 'w') as f:
        pickle.dump(clean_df, f)
