import pandas as pd
import numpy as np
import cPickle as pickle
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split


def transform_data(X_train, X_test):
    '''
    Input:
    OUtput: Returns the vectorizer and the matrix for X_train and X_test
    '''
    #vectorize only the lyrics
    vectorizer = TfidfVectorizer(max_features=5000)
    train_vector = vectorizer.fit_transform(X_train.ix[:,'full_lyrics'])
    test_vector = vectorizer.transform(X_test.ix[:, 'full_lyrics'])
    return vectorizer, train_vector, test_vector




if __name__ == '__main__':

    features = ['Num_words', 'Top_7_word_freq', 'gangsta_rating']

    with open('combined.pkl', 'r') as f:
        combined = pickle.load(f)

    #create a test-train split
    X_train, X_test, y_train, y_test  = train_test_split(combined, combined['classes'],
                                                            test_size=0.25,
                                                            random_state=100)

    # transform data
    vectorizer, train_tfidf, test_tfidf = transform_data(X_train, X_test)

    #combining the tfidf with the features
    combine_train_X = np.concatenate([train_tfidf, X_train[features].as_matrix()],axis=1)
    combine_test_X = np.concatenate([test_tfidf, X_test[features].as_matrix()],axis=1)

    #training and testing the model
    model = MultinomialNB(alpha=0.01)
    model.fit(combine_train_X, y_train)
    predicted = model.predict(combine_test_X)
    print confusion_matrix(y_test, predicted )
    print 'Accuracy score: {}'.format(accuracy_score(y_test, predicted))
    print 'Recall score: {}'.format(recall_score(y_test, predicted,average=None))
    print 'Precision score: {}'.format(precision_score(y_test, predicted, average=None))
    print 'F1 score: {}'.format(f1_score(y_test, predicted, average=None))

    # Final Model
    #               Predicted
    #             E    W    DS
    #        E [[3516  161  655]
    # True   W  [1203 1454  710]
    #        DS [ 711  179 2960]]

    # Accuracy score: 0.686639535891
    # Recall score: [ 0.81163435  0.43183843  0.76883117]
    # Precision score: [ 0.64751381  0.81047938  0.68439306]
    # F1 score: [ 0.72034419  0.56345669  0.72415902]

    with open('/data/naives_bayes.pkl', 'w') as f:
        pickle.dump(model, f)

    with open('/data/vectorizer.pkl', 'w') as f:
        pickle.dump(vectorizer, f)
