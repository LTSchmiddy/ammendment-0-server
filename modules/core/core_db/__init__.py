import module_loader
host: module_loader.AZeroModuleHost = None

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

Base = declarative_base()

from . import tables

db_engine: Engine = None
Session: scoped_session = None

def get_session() -> scoped_session:
    return scoped_session(sessionmaker(bind=db_engine))

# Required Functions:
def init(name: str, path: str, args: dict[str, str]):
    global Session, db_engine
    db_engine = create_engine(settings.current['database']['db-address'], echo=settings.current['database']['echo'])
    Base.metadata.create_all(db_engine)
    Session = scoped_session(sessionmaker(bind=db_engine))



