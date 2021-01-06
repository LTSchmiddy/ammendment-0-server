from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.orm import session

from utils.json_class import JsonClass

import core_db
from .users import User

from . import common

class Post(core_db.Base, common.RefsUser):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('user.id'))
    
    created_on = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    content = Column(Text)
    
    additional = Column(JSON, nullable=True)

    def __repr__(self):
        return f'<Post {self.id} by user {self.user_id}>'
