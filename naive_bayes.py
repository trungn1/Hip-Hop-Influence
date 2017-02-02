from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
import pandas as pd
import numpy as np
from collections import Counter
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier

def clean_lyrics(lyrics):
    '''
    Input: A string of lyrics
    Output: Returns a string of lyrics that has been lowered, stemmed, and stripped of punctuation
    '''
    #creating a stemmed object
    ps = PorterStemmer()
    # splitting the lyrics and
    lyrics_split = lyrics.lower().split()
    lyrics_split = [ps.stem(word.strip(punctuation)) for word in lyrics_split]
    joined_lyrics = ' '.join(lyrics_split)
    return joined_lyrics


def top_words(lyrics, num=7):
    '''
    Input: Song lyrics
    Output: Percentage frequency of top x number of word
    '''
    #split the lyrics into a list
    lyrics = lyrics.lower().split()

    #use a counter to get the most word frequency
    counter = Counter(lyrics)
    counter_sum = float(sum(counter.values()))
    for key in counter.iterkeys():
        counter[key] /= counter_sum
    highest_freq_words = counter.most_common(num)
    freq_sum = sum([word[1] for word in highest_freq_words])
    return freq_sum

def rating(lyrics):
    '''
    Input: A stemmed lyrics
    Return: Frequncy of wor
    '''
    check_word = set(['gun', 'bullet', 'murder', 'death', 'cop', 'popo', 'weed', 'cocaine', 'heroin', 'blunt', 'clip', 'punk',
                    'snitch', 'brutality', 'methadone', 'amphetamines', 'ecstacy', 'marijuana', 'crack'])
    counter = Counter(lyrics.split())
    counter_sum = float(sum(counter.values()))
    frequency = 0
    # looping through the set of word to check for and add their occurances
    for word in check_word:
        frequency += counter[word]
    return frequency/counter_sum


def combined_txt_file(file_list):
    '''
    Input: A list of txt filename
    Output: A combined dataframe that removes null lyrics
    '''
    combined = pd.DataFrame(columns=['artist', 'date_published','song_name','page','full_lyrics'])
    # loops through all the text files containing the lyrics
    for txt_file in output_files:
        temp_df = pd.read_csv(txt_file, delimiter=';;;', engine='python')
        combined = combined.append(temp_df)
    #account for data that has lyrics
    mask = ~ (combined['full_lyrics'].isnull())
    clean  = combined.ix[mask]

    clean['full_lyrics'] = clean['full_lyrics'].apply(clean_lyrics)

    #add feature_1 - number of unique words
    clean['Num_words'] = clean['full_lyrics'].apply(lambda x: len(set(x.lower().split())))

    #add feature_2 - number of repetitions
    clean['Top_7_word_freq'] = clean['full_lyrics'].apply(top_words)

    #add feature_3 - count of gangsta terms. Apply a count that determines the frequncy of these words as a percentage of the doucment
    clean['gangsta_rating'] = clean['full_lyrics'].apply(ratings)

    return clean

def create_labeled_dataframe(txt_file):
    labels = pd.read_csv(txt_file, delimiter='|')
    labels['classes'] = labels['classification'].apply(_binary)
    return labels

def _binary(string):
    '''
    Input: A string
    Output: An int ditating which class
    '''
    if string.startswith('East'):
        return 1
    elif string.startswith('West'):
        return 2
    else:
        return 3

def _cross_val_split(df, hold_out_per=.8):
    '''
    Input: A dataframe, and a percentage of songs to hold out
    Output: a
    '''
    #columns to return - if add additional features here
    features = ['full_lyrics', 'Num_words', 'Top_7_word_freq', gangsta_rating]
    #get the max id
    max_id = max(df.artist_id.unique())
    # to hold out
    to_hold_out = set(np.random.randint(1, max_id, size=int(hold_out_per * max_id)))
    #set a column to dictate which to hold off
    df['to_train'] = df['artist_id'].apply(lambda x: int(x) in to_hold_out).astype(int)
    #set a mask variable
    mask = df['to_train']== 1
    train_X = df.loc[mask, features]
    train_y = df.loc[mask,'classes']
    #negate the mask to get the testing set
    test_X = df.loc[~mask, features]
    test_y = df.loc[~mask,'classes']
    return train_X, train_y, test_X, test_y

def cross_validation(df, classifier_list, k=3):
    '''
    Input: A pandas dataframe, your X matrix
    Output: None, prints out score for the cross validations
    '''
    # this loop is to do cross-fold validations
    features = ['Num_words', 'Top_7_word_freq', 'gangsta_rating']
    for _ in range(k):
        # # do a tfidf transformer
        #perfrom a test train split to cross validate
        train_X, train_y, test_X, test_y = _cross_val_split(df)

        # #vectorize only the lyrics
        # vectorizer = TfidfVectorizer(max_features=10000)
        # train_vector = vectorizer.fit_transform(train_X['full_lyrics'])
        # test_vector = vectorizer.transform(test_X['full_lyrics'])

        # #combining the train vector to array to add them together
        # train = pd.DataFrame(train_vector.toarray())
        # test = pd.DataFrame(test_vector.toarray())


        #tokenize the results
        cv = CountVectorizer()
        count_vector = cv.fit_transform(train_X['full_lyrics'])
        test_vector = cv.transform(test_X['full_lyrics'])

        train = pd.DataFrame(count_vector.toarray())
        test = pd.DataFrame(test_vector.toarray())


        #
        # #reset index to match them all up
        # train.reset_index(inplace=True)
        # test.reset_index(inplace=True)
        # train_X.reset_index(inplace=True)
        # test_X.reset_index(inplace=True)
        #combining the tfidf with the features
        combine_train_X = pd.merge(train, train_X[features], left_index=True, right_index=True, how='outer')
        combine_test_X = pd.merge(test, test_X[features], left_index=True, right_index=True, how='outer')
        combine_train_X = combine_train_X.drop('index', 1)
        combine_test_X = combine_test_X.drop('index', 1)

        for classifier in classifier_list:
            print "\n____________{}____________".format(classifier.__class__.__name__)

            #creating a model
            classifier.fit(combine_train_X, train_y)
            print 'done fitting'
            predicted = classifier.predict(combine_test_X)
            print 'done predicting'
            confusion_matrix(test_y, predicted)
            print confusion_matrix(test_y, predicted)
            print 'Accuracy score: {}'.format(accuracy_score(test_y, predicted))
            print 'Recall score: {}'.format(recall_score(test_y, predicted,average=None))
            print 'Precision score: {}'.format(precision_score(test_y, predicted, average=None))
            print 'Number of training data: {}'.format(combine_train_X.shape[0])
            print 'Number of test data: {}'.format(combine_test_X.shape[0])

if __name__ == '__main__':

    output_files = ['output/output_1.txt','output/output_2.txt','output/output_3.txt','output/output_4.txt']

    #creating the combined dataframe
    combined = combined_txt_file(output_files)

    #create the labels table
    labels = create_labeled_dataframe('artist_classification.txt')

    #create a new joined dataframe
    result = combined.merge(labels, left_on='artist', right_on=' artist', how='inner')

    #create a test-train split and never look at it again
    X_train, X_test, y_train, y_test  = train_test_split(result, result['classes'],
                                                            test_size=0.25,
                                                            random_state=42)


    # #CROSS VALIDATION
    # cross_validation(X_train,[ MultinomialNB(), RandomForestClassifier(), GradientBoostingClassifier(), AdaBoostClassifier()])
    cross_validation(X_train,[ MultinomialNB()])


    # with open('/data/naives_bayes.pkl', 'w') as f:
    #     cPickle.dump(model, f)
