__author__ = 'Neal'
import sqlite3, csv
from bottle import Bottle
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, validates


app = Bottle()
Base = declarative_base()


class WeatherData(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True, autoincrement=True,unique=True)
    email = Column(String, nullable=False,unique=True)
    location = Column(String, nullable=False)


    @validates('email')
    def validate_email(self, key, address):
        '''
        Checks for invalid entries
        :param key:
        :param address:
        :return:
        '''
        assert '@' in address
        return address

    def __init__(self,email,location):
        "Constructor"
        self.email = email
        self.location = location

    def __repr__(self):
        return "Weather Subscriber (email: %s, location: %s" % (self.email, self.location)

    def __str__(self):
        return str(self.email) + ' in ' + str(self.location)

engine = create_engine("sqlite:///weatherdata.db", echo=True)
create_session = sessionmaker(bind=engine)
create_session()
#Base.metadata.create_all() - Turn on in production environment


def create_new(email,location):
    session = create_session()
    new_task = WeatherData(email,location)
    final = ''
    if session.query(WeatherData).filter(WeatherData.email == new_task.email).count() == 0:
        session.add(new_task)
        final = True
    else:
        session.rollback()
        final = False
    session.commit()
    return final

class City_choices():
    city_states= []
    city_locations = {}
    with open('cities_in_us.csv') as csvfile:
        cityreader = csv.reader(csvfile)
        for i in cityreader:
            city_states.append((str(i[0]) + "," + str(i[1])))
            city_locations[str(i[0])] = str(i[1])

    city_states = tuple(["..Select Your City.."] + sorted(city_states))

def get_data_in_db():

    db = sqlite3.connect('weatherdata.db')
    c = db.cursor()
    c.execute("SELECT email,location FROM weather")
    data = c.fetchall()
    user_data = []
    for i in data:
         user_data.append([i[0],[x.strip() for x in i[1].split(',')][0],[x.strip() for x in i[1].split(',')][1]])
    c.close()
    print user_data
    return user_data


if __name__ == '__main__':
    get_data_in_db()