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
import plotly.tools as tls
import plotly.graph_objs as go
import processText as pt


config = ConfigParser.ConfigParser()
config.read('config')

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
            date_time = tweet['created_at']
            sentiment_analysis = TextBlob(text)

            self.accumulated_sentiment += sentiment_analysis.sentiment.polarity

            x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            y = self.accumulated_sentiment

            s.write(dict(x=x, y=y))

            time.sleep(1)

            print self.accumulated_sentiment#self.accumulated_sentiment #, sentiment_analysis.sentiment.subjectivity, time
            #print time, sentiment_analysis.sentiment, text

    def on_error(self, status):
        if status == 420:
            #returning Flase in on_data disconnects the stream
            return False


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # creates a stream object
    stream = Stream(auth, listener)

    # Setup plotly
    stream_ids = tls.get_credentials_file()['stream_ids']

    # Get stream id from stream id list
    stream_id = stream_ids[0]

    # Make instance of stream id object
    stream_1 = go.Stream(
        token=stream_id,  # link stream id to 'token' key
        maxpoints=600  # keep a max of 80 pts on screen
    )

    # Initialize trace of streaming plot by embedding the unique stream_id
    trace1 = go.Scatter(
        x=[],
        y=[],
        mode='lines',
        stream=stream_1  # (!) embed stream id, 1 per trace
    )

    data = go.Data([trace1])

    # Add title to layout object
    layout = go.Layout(
        title='Twitter Overwatch Sentiment',
        xaxis=dict(
            title='Date & Time',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Aggregate Sentiment',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        )
    )
    # Make a figure object
    fig = go.Figure(data=data, layout=layout)

    # Send fig to Plotly, initialize streaming plot, open new tab
    py.iplot(fig, filename='python-streaming')

    # We will provide the stream link object the same token that's associated with the trace we wish to stream to
    s = py.Stream(stream_id)

    # We then open a connection
    s.open()

    time.sleep(5)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['overwatch'])

