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
    :return: post processed <str> object
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
    '''
    Looks for words like 'Cooooooolllll' and converts word to 'Cool'
    :param s: <str>
    :return: processed <str>
    '''
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)


def getStopWordList(stopWordListFileName):
    '''
    Returns a <list> with all stopwords in specified file
    :param stopWordListFileName: <str> of file path
    :return: <list> of stopwords
    '''
    stopWords = []
    stopWords.append('ATUSER')
    stopWords.append('URL')

    with open(stopWordListFileName) as f:
        line = f.readline()
        for line in f.readlines():
            stopWords.append(line.strip())

    return stopWords


def getFeatureVector(tweet):
    '''
    Converts <str> tweet into a <list> of feature vectors (words)
    :param tweet: <str> of tweet
    :return: <list> of words with stopwords stripped
    '''
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