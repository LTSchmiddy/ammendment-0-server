from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship

import core_db

class User(core_db.Base):
    __tablename__ = 'user'
    id = Column(Text, primary_key=True)
    mac_address = Column(Text, unique=True)
    email = Column(Text, unique=True)
    password = Column(Text, nullable=False)
    
    current_token = Column(Text, nullable=False)
    token_created = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    
    display_name = Column(Text, nullable=False)
    created_on = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)

    additional = Column(JSON, nullable=True)

    def __repr__(self):
        return f'<User {self.id}>'


