from datetime import datetime
from utils.json_class import JsonClass
from sqlalchemy import *
from sqlalchemy.orm import relationship

import core_db

from . import common

# We'll change this via the settings later:
default_session_uses_allowed = 5

class Session(core_db.Base, common.RefsUser, JsonClass):
    __tablename__ = 'session'
    id = Column(Text, primary_key=True)
    bits = Column(Text, nullable=False)
    created_on = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    allowed_uses = Column(Integer, nullable=False, default=default_session_uses_allowed)
    current_uses = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Session {self.id} for user {self.user_id}>'





