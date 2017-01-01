# Sentiment Analysis

This project utilizes Tweepy to live stream tweets filtered by "overwatch".  The text of the tweet is stripped of low-value words and run through TextBlob's sentiment classifier to determine the sentiment of a tweet (-1.0 <= x <= 1.0).  An accumulator variable is used to aggregate the total sentiment and push that value to Plotly every second.

# State of Project

Functioning:
  * Live streaming tweets related to "overwatch"
  * Classifying tweet as positive or negative
  * Streaming accumulated sentiment to Plotly every second

 Future work includes:
  * Store historical data on MySQL server for queries
  * Host query features on Flask developed website
  * Run permanently on server (local machine or EC2 instance)

# Notes

Gotchas
  * Occasionally (~1 observation per 200 tweets), a tweet's creation time is earlier than the received time
  * Plotly has 10000 max points for streaming graphs; @ 1 point/sec, it's possible to see ~166 minutes worth of live data at any given time (currently set at 600 / 10 minutes)

# License

Open sourced under the MIT license. See the included LICENSE file for more information.
