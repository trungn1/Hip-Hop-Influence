from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.cluster import KMeans, DBSCAN
import pandas as pd
import numpy as np
import vaderSentiment
from nltk.corpus import stopwords
from sklearn.metrics import silhouette_score
from nltk.stem.porter import PorterStemmer

def combined_txt_file(file_list):
    '''
    Input: A list of txt filename
    Output: A combined dataframe
    '''
    combined = pd.DataFrame(['artist', 'date_published','song_name','page','full_lyrics'])
    for txt_file in file_list:
        temp_df = pd.read_csv(txt_file, delimiter=';;;')
        combined.append(temp_df)
    return combined


def top_10(kmc, vectorizer):
    '''
    Input: Accepts the KMeans model and the the TFIDF (vectorizer) object
    Output:Prints the 10 most important features(words) for each of the clusters
    '''
    words = np.array(vectorizer.get_feature_names())
    for cluster in kmc.cluster_centers_:
        top10 = np.argsort(cluster)[-10:]
        print words[top10]

if __name__ == '__main__':
    #tranform nlp
    output_files = ['../output/output_1.txt','../output/output_2.txt','../output/output_3.txt','../output/output_4.txt']
    combined = combined_txt_file(output_files)
    #create the mask for where the lyrics are not blank


    # #stem the words before I vectorize the words
    # p_stemmer = PorterStemmer()
    # texts = [p_stemmer.stem(i) for i in stopped_tokens]

    # remove the rows where there are no lyrics
    mask = ~(combined.full_lyrics.isdnull())
    clean_df = combined.ix[mask]

    # make sure that all the lyrics are lower cased
    song_vector = clean_df['full_lyrics'].apply(lambda x: x.lower())

    # I will not filter out stop words since it is important to song lyrics
    vectorizer = TfidfVectorizer(max_features=5000)
    word_matrix = vectorizer.fit_transform(song_vector)
    model = KMeans().fit(word_matrix)
    #get vocabulary

    #Initiate a model
    model = KMeans().fit(word_matrix)

    print "cluster centers:"
    print model.cluster_centers_

    # 3. Find the top 10 features for each cluster.
    top_centroids = model.cluster_centers_.argsort()[:,-1:-11:-1]
    print "top features for each cluster:"
    for num, centroid in enumerate(top_centroids):
        print "{}: {}".format(num, ", ".join(vocabs[i] for i in centroid))


    with open('../data/kmean.pkl', 'w') as f:
        cPickle.dump(model, f)
