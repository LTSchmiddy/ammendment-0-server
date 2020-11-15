from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship

import db

class User(db.Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    display_name = Column(Text, nullable=False)
    created_on = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)

    def __repr__(self):
        return f'<User {self.id}>'


