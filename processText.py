import ConfigParser
import re
from string import punctuation

config = ConfigParser.ConfigParser()
config.read('config')

def processTweet(tweet):
    '''
    Strips text of tweet into list of lower case words without punctuation.  Replaces links and user names with URL
    and AT_USER respectively.
    :param tweet: <str> of tweet
    :return:
    '''

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


stopwords = getStopWordList(config.get('stopwords', 'stopword_file'))