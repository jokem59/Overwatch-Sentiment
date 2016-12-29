#!usr/bin/python

from string import punctuation
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
import json
import re

#Variables that contains the user credentials to access Twitter API
access_token = "806572379963015170-HnQ46l3UhHucR21gV4VOpknbRjVMVsh"
access_token_secret = "dog4ii3EDptLYWkoE3Ob7z6ahhl9ANZ6gAMCYMczfO4Db"
consumer_key = "mYyBF5XlPEiVtSBWevY09x22o"
consumer_secret = "5g8uTmS1JPn4QOhKIz0yzgQ0c8bwRNrF7tPrsJRvs4tlkg7ry2"

stopwords_file = '/Users/JoeK/nltk_data/corpora/stopwords/english'

# prints status text
class StdOutListener(StreamListener):

    def __init__(self):
        super(StdOutListener, self).__init__()
        self.accumulated_sentiment = 0.0

    def on_status(self, status):
        print status.text

    def on_data(self, data):
        tweet = json.loads(data)

        # excludes official retweets
        if 'text' in tweet and not tweet['retweeted'] and tweet['lang'] == 'en':
            # stops function if a manual retweet
            if re.search('RT @', tweet['text']):
                return

            text = processTweet(tweet['text'])
            text = replaceTwoOrMore(text)
            feature_vector = getFeatureVector(text)
            for word in feature_vector:
                if word in stopwords:
                    feature_vector.remove(word)

            # use for testing purposes
            text = ' '.join(feature_vector)
            time = tweet['created_at']
            sentiment_analysis = TextBlob(text)

            self.accumulated_sentiment += sentiment_analysis.sentiment.polarity

            print self.accumulated_sentiment#self.accumulated_sentiment #, sentiment_analysis.sentiment.subjectivity, time
            #print time, sentiment_analysis.sentiment, text

    def on_error(self, status):
        if status == 420:
            #returning Flase in on_data disconnects the stream
            return False

def processTweet(tweet):
    # process the tweets

    #convert to ascii and ignore all else & remove \n
    tweet = tweet.encode('ascii', 'ignore').replace('\n', ' ')
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #Remove apostorphes
    tweet = tweet.replace("'", '')
    #trim
    tweet = tweet.lstrip().rstrip()
    #remove punctuation
    tweet = tweet.translate(None, punctuation)

    return tweet


def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)


#start getStopWordList
def getStopWordList(stopWordListFileName):
    #read the stopwords file and build a list
    stopWords = []
    stopWords.append('ATUSER')
    stopWords.append('URL')

    with open(stopWordListFileName) as f:
        line = f.readline()
        for line in f.readlines():
            stopWords.append(line.strip())

    return stopWords


#start getfeatureVector
def getFeatureVector(tweet):
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if w in stopwords or val is None:
            continue
        else:
            featureVector.append(w.lower())
    return featureVector


if __name__ == '__main__':

    stopwords = getStopWordList(stopwords_file)

    #This handles Twitter authetification and the connection to Twitter Streaming API
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # creates a stream object
    stream = Stream(auth, listener)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['overwatch'])

