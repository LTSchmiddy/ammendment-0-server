from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship

import core_db

from . import common

class AuthAttempt(core_db.Base, common.RefsUser):
    __tablename__ = 'auth_attempt'
    id = Column(Text, primary_key=True)
    bits = Column(Text, nullable=False)
    created_on = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<AuthAttempt {self.id} for user {self.user_id}>'



