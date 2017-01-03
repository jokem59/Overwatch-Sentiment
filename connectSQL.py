from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import ConfigParser


config = ConfigParser.ConfigParser()
config.read('/Users/JoeK/config_files/owconfig')

sql_pword = config.get('mysql', 'db_pword')

Base = automap_base()

# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine('mysql+mysqldb://root:' + sql_pword + '@127.0.0.1:3306/owsentiment', echo=True)

# reflect the tables
Base.prepare(engine, reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.
Tweets = Base.classes.tweets

session = Session(engine)

# rudimentary relationships are produced
session.add(Tweets(date='2017-01-03', time='20:09', sentiment=0.7463, subjectivity=0.0, text='sick play bro'))
session.commit()