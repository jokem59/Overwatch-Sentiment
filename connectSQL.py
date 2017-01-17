#!usr/bin/python

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import MySQLdb
import ConfigParser

# config = ConfigParser.ConfigParser()
# config.read('/Users/JoeK/config_files/owconfig')
def connectSQL(config):
    '''
    Using SQLAlchemy declarative system, creates engine connecting MySQL DB with Base objects
    :param config: ConfigParser object with sql_pword information
    :return: Base Class and Session object to communicate with DB
    '''
    sql_pword = config.get('mysql', 'db_pword')

    Base = automap_base()

    # engine; have one table setup in owsentiment DB
    engine = create_engine('mysql+mysqldb://root:' + sql_pword + '@127.0.0.1:3306/owsentiment', echo=False)

    # reflect the tweets table
    Base.prepare(engine, reflect=True)

    # mapped classes are now created with names by default matching that of the table name
    Tweets = Base.classes.tweets

    session = Session(engine)

    return Tweets, session

def insertSQL(Tweets, session, date, time, sentiment, subjectivity, text):
    '''
    Inserts passed data into MySQL table associated with session object
    :param Tweets: mapped class to SQL table
    :param session: object that acts as 'handle' to owsentiment database
    :param date: <str> from tweet
    :param time: <str> from tweet
    :param sentiment: <float> from tweet
    :param subjectivity: <float> from tweet
    :param text: <str> from tweet
    :return: None
    '''
    # rudimentary relationships are produced
    session.add(Tweets(date=date, time=time, sentiment=sentiment, subjectivity=subjectivity, text=text))
    session.commit()

def connectDb(config):

    sql_host = config.get('mysql', 'db_host')
    sql_user = config.get('mysql', 'db_user')
    sql_pword = config.get('mysql', 'db_pword')
    sql_name = config.get('mysql', 'db_name')

    # Open database connection
    db = MySQLdb.connect(sql_host, sql_user, sql_pword, sql_name)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("SELECT * FROM tweets;")

    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()

    print data

    # disconnect from server
    db.close()

def getSQL(config):

    sql_host = config.get('mysql', 'db_host')
    sql_user = config.get('mysql', 'db_user')
    sql_pword = config.get('mysql', 'db_pword')
    sql_name = config.get('mysql', 'db_name')


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('/Users/JoeK/config_files/owconfig')

    connectDb(config)