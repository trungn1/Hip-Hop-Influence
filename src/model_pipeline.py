from sklearn.feature_extraction.text import TfidfVectorizer
import vaderSentiment
from nltk.corpus import stopwords

#standform nlp

df = pd.read_csv('songlist.txt',delim=';')
df.columns = ['Genre', 'Artist', 'date_published', 'Lyrics']
vectorizer = TfidfVectorizer(stop_words='english')

# i may need a cleaning function that parses the words and stems it
vector = vectorizer.fit_transform(df['Lyrics'])


#get sentiment

#get vocabulary


stop = set(stopwords.words('english'))
sentence = "this is a foo bar sentence"
print [i for i in sentence.lower().split() if i not in stop]
['foo', 'bar', 'sentence']
