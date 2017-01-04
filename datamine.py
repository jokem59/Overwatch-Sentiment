#!usr/bin/python

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
import json
import ConfigParser
import datetime
import re
import time
import plotly.plotly as py
import processText as pt
import plotlySetup


config = ConfigParser.ConfigParser()
config.read('/Users/JoeK/config_files/owconfig')

stopwords = pt.getStopWordList(config.get('stopwords', 'stopword_file'))
access_token = config.get('twittertokens', 'access_token')
access_token_secret = config.get('twittertokens', 'access_token_secret')
consumer_key = config.get('twittertokens', 'consumer_key')
consumer_secret = config.get('twittertokens', 'consumer_secret')

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

            text = pt.processTweet(tweet['text'])
            text = pt.replaceTwoOrMore(text)
            feature_vector = pt.getFeatureVector(text)
            for word in feature_vector:
                if word in stopwords:
                    feature_vector.remove(word)

            # use for testing purposes
            text = ' '.join(feature_vector)
            date_time = pt.parseDateTime(tweet['created_at'])
            sentiment_analysis = TextBlob(text)

            self.accumulated_sentiment += sentiment_analysis.sentiment.polarity

            x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            y = self.accumulated_sentiment

            plotly_stream.write(dict(x=x, y=y))

            time.sleep(1)

            print date_time#self.accumulated_sentiment#self.accumulated_sentiment #, sentiment_analysis.sentiment.subjectivity, time
            #print time, sentiment_analysis.sentiment, text

    def on_error(self, status):
        if status == 420:
            # returning False in on_data disconnects the stream
            return False


if __name__ == '__main__':

    # handles Twitter authentication and the connection to Twitter Streaming API
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # creates a twitter stream object
    twitter_stream = Stream(auth, listener)
    # creates a plotly stream object
    plotly_stream = plotlySetup.setupPlotly(600)

    twitter_stream.filter(track=['overwatch'])

