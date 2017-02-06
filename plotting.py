import matplotlib.pyplot as plt

def plot_artist(dataframe, col_name, criteria, name):
    '''
    Input: The dataframe, column name, criteria
    Output: Return the count of words over time of an artist
    '''
    words = set()
    date = defaultdict(int)
    #for plotting
    dates = []
    counts = []

    for row, index in dataframe.iterrows():
        if dataframe.ix[row, col_name] == criteria:

            to_add = dataframe.ix[row, 'word_set']
            try:
                words.update(to_add)
            except TypeError:
                words.add(to_add)
            published = dataframe.ix[row, 'date_published']
            date[published] = len(words)

#     # cycle through the dates to find the highest values
    for day, values in date.iteritems():
        dates.append(day)
        counts.append(values)

    plt.plot(dates, counts,'o', label=criteria)
    plt.title('Word Growth over time for {}'.format(name))
    plt.xlabel('Date')
    plt.ylabel('Size of Vocabulary')
    return words


def top_words(df):
    '''
    Input
    '''

    for index, row in combined_with_label.iterrows():
        artist = combined_with_label.ix[index, 'classification']
        words = combined_with_label.ix[index, 'word_set']
        region_dict[artist].update(words)


def create_unique_word(df, criteria):
    '''
    Input:
    Output: Return the top 10 words by each region
    '''
    #make a regional word dictionary
    region_dict = defaultdict(set)
    for index, row in df.iterrows():
        artist = df.ix[index, 'classification']
        words = df.ix[index, 'word_set']
        region_dict[artist].update(words)

    # create a set to compare words
    other = set(region_dict.keys())
    other.remove(criteria)

    criteria_word_set = region_dict[criteria]
    other_word_set = set()
    for region in other:
        set
    criteria_set = region_dict[criteria]
    region_dict[criteria] -

    #check the counter dictionary to determine which words have the highest counter
    top_10_words
    return top_10_words
