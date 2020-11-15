from sqlalchemy import *
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import settings

db_type_conversions = {
    bool: Boolean,
    int: Integer,
    float: Float,
    str: String,
    list: JSON,
    dict: JSON,
}

# engine = create_engine('sqlite:///library.db', echo=True)

Base = declarative_base()

from db import tables

db_engine: Engine = None
Session = None

def init():
    global Session, db_engine
    db_engine = create_engine(settings.current['database']['db-address'], echo=settings.current['database']['echo'])
    Base.metadata.create_all(db_engine)
    Session = scoped_session(sessionmaker(bind=db_engine))



