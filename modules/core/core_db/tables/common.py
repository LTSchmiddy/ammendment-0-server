from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

import core_db

# This is a fix for recursive imports
User = None

class RefsUser:
    @declared_attr
    def user_id(cls):
        return Column(Text, ForeignKey('user.id'))
    
    @property
    def user(self) -> User:
    # def user(self):
        # from .users import User
        session = core_db.get_session()
        
        retVal = session.query(User).filter(User.id==self.user_id).first()
        session.remove()
        return retVal


from .users import User

__all__ = ('RefsUser',)